#!/usr/bin/env python3
"""
real_browser_fetch.py — fetch a JS-gated / login-walled page by driving the
USER'S REAL logged-in browser (Brave) over CDP. No cookies to copy, no
automation fingerprint, no IP escalation: it IS the user's browser session.

WHY THIS EXISTS (2026-11-23):
  Reddit search now redirects ANONYMOUS requests to a login wall on every
  surface (old.reddit included). Our Playwright head (any profile, with or
  without the session cookie, headless or headed) gets the network-policy
  "whoa there pardner" block — profile-independent (the egress IP is
  flagged for automation). The engine (VS Code's class) only reaches the
  solvable "prove your humanity" challenge tier. The ONE tier that works =
  the user's real logged-in, non-automation-flagged browser. This script
  drives it via Chrome DevTools Protocol — zero cookie management.

PREREQ (one-time, user at the machine):
  Brave must be RESTARTED with the debug flag (a running instance without it
  ignores the flag). The script auto-detects: if nothing is listening on the
  port it launches Brave with the flag, waits, then attaches.

USAGE:
  python real_browser_fetch.py "https://www.reddit.com/search/?q=krea%202" --text
  python real_browser_fetch.py <url> --out data\\page.html
  python real_browser_fetch.py <url> --selector "shreddit-post"

Run with:
  & "C:\\Program Files\\Python310\\python.exe" "D:\\models\\vsCodeMcp\\utilities\\real_browser_fetch.py" <url>
"""
import os
import sys
import time
import atexit
import subprocess
import argparse

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PORT = 9222
BRAVE = None
for cand in (
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\BraveSoftware\Brave-Browser\Application\brave.exe"),
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
):
    if os.path.exists(cand):
        BRAVE = cand
        break


def port_live() -> bool:
    import socket
    s = socket.socket()
    s.settimeout(1.5)
    try:
        s.connect(("127.0.0.1", PORT))
        return True
    except Exception:
        return False
    finally:
        s.close()


def ensure_brave():
    if port_live():
        print(f"CDP already live on :{PORT}", file=sys.stderr)
        return
    if not BRAVE:
        print("ERROR: Brave not found. Launch it manually with: "
              f'"{BRAVE or "brave.exe"}" --remote-debugging-port={PORT}', file=sys.stderr)
        sys.exit(2)
    print(f"launching {BRAVE} with --remote-debugging-port={PORT}", file=sys.stderr)
    # A running Brave without the flag ignores the flag — tell the user.
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq brave.exe"],
                       capture_output=True, text=True)
    if "brave.exe" in r.stdout.lower():
        print("WARNING: Brave is already running WITHOUT the debug flag — "
              "close ALL Brave windows and re-run, or close them and re-run now.",
              file=sys.stderr)
    subprocess.Popen([BRAVE, f"--remote-debugging-port={PORT}",
                      "--remote-allow-origins=*"], shell=False)
    for _ in range(30):
        time.sleep(1)
        if port_live():
            print("CDP live", file=sys.stderr)
            return
    print("ERROR: CDP port never came up", file=sys.stderr)
    sys.exit(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default=None)
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--selector", default=None,
                    help="CSS selector to extract inner_text from (first match)")
    a = ap.parse_args()

    ensure_brave()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        # The fetch tab inherits the browser's default (light) color scheme —
        # force dark to match the user's dark theme (no white flash, 2026-11-23).
        try:
            page.emulate_media(color_scheme="dark")
        except Exception:
            pass
        # Robust close: even if this process is killed mid-run (e.g. a
        # truncated output pipe), the atexit hook closes the fetch tab so no
        # stray tabs are left in the user's real browser.
        def _close_page():
            try:
                page.close()
            except Exception:
                pass
        atexit.register(_close_page)
        try:
            page.goto(a.url, wait_until="domcontentloaded", timeout=60000)
            html = ""
            for _ in range(20):
                try:
                    html = page.content()
                except Exception:
                    time.sleep(2)
                    continue
                low = html.lower()
                if "whoa there" not in low and "prove your humanity" not in low:
                    break
                time.sleep(2)
            try:
                page.wait_for_load_state("networkidle", timeout=25000)
            except Exception:
                pass
            try:
                html = page.content()
            except Exception:
                pass
            if a.out:
                d = os.path.dirname(a.out)
                if d:
                    os.makedirs(d, exist_ok=True)
                with open(a.out, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"saved {len(html)} chars -> {a.out}", file=sys.stderr)
            low = html.lower()
            if "whoa there" in low:
                print("RESULT: still network-policy blocked even in the real browser — "
                      "the IP wall is absolute; a VPN is the only way", file=sys.stderr)
                sys.exit(4)
            if a.text or a.selector:
                if a.selector:
                    el = page.query_selector(a.selector)
                    print(el.inner_text() if el else "(selector not found)")
                else:
                    el = page.query_selector("shreddit-post")
                    if not el:
                        el = page.query_selector("main")
                    print(el.inner_text() if el else html[:4000])
            else:
                print(html[:2000])
        finally:
            _close_page()


if __name__ == "__main__":
    main()
