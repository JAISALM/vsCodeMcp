#!/usr/bin/env python3
"""
reddit_browser_fetch.py — fetch a Reddit (or any JS-gated) page using a REAL
local Chromium browser, so the JS bot-challenge ("Prove your humanity") is
solved by actual JS execution. This is exactly what VS Code's integrated
browser does — and why it succeeds where a text-only HTTP fetcher fails.

WHY THIS EXISTS
  DSH's web profile fetches with a text-only HTTP client (curl). It cannot
  execute JS, so on Reddit it only ever sees the challenge page. A real
  browser runs the challenge JS, solves it, and renders the full post.

HOW IT WORKS
  Drives the Playwright Chromium already on this machine
  (C:\\Users\\user\\AppData\\Local\\ms-playwright\\chromium-1234) with a
  PERSISTENT profile (C:\\Users\\user\\.dsh\\fetch_creds\\browser_profile)
  so cookies + challenge state persist across runs. The persistent profile is
  the second half of why VS Code passes (an isolated clean profile gets
  escalated to reCAPTCHA).

USAGE
  python reddit_browser_fetch.py "https://www.reddit.com/r/comfyui/comments/1wxixua/..."
  python reddit_browser_fetch.py <url> --out data\\char_sheet_reddit\\P1.html
  python reddit_browser_fetch.py <url> --text          # print post body only
  python reddit_browser_fetch.py <url> --headed        # show the window (most reliable)

Run with:
  "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\reddit_browser_fetch.py" <url>
"""
import os
import sys
import time
import argparse

# Windows console is cp1252 — force UTF-8 so emoji/special chars don't crash.
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Local Playwright Chromium (same engine VS Code's integrated browser uses).
CHROME = r"C:\Users\user\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe"
# Persistent profile — challenge state + cookies survive across runs.
PROFILE = os.path.expanduser(r"~\.dsh\fetch_creds\browser_profile")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def is_gated(html: str) -> bool:
    head = html[:30000].lower()
    return ("prove your humanity" in head) or ("recaptcha" in head)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default=None, help="save full rendered HTML here")
    ap.add_argument("--text", action="store_true", help="print extracted post text only")
    ap.add_argument("--headed", action="store_true",
                    help="run with a visible window (most reliable vs reCAPTCHA)")
    a = ap.parse_args()

    if not os.path.exists(CHROME):
        print(f"ERROR: Chromium not found at {CHROME}", file=sys.stderr)
        sys.exit(2)

    from playwright.sync_api import sync_playwright
    os.makedirs(PROFILE, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            executable_path=CHROME,
            headless=not a.headed,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent=UA,
            viewport={"width": 1366, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(a.url, wait_until="domcontentloaded", timeout=60000)

        # Let the JS challenge run and redirect. Poll until the gate clears.
        # content() throws while a navigation is in flight — swallow that and
        # keep waiting; the challenge redirect IS a navigation.
        html = ""
        for _ in range(30):
            try:
                html = page.content()
            except Exception:
                time.sleep(2)
                continue
            if not is_gated(html):
                break
            time.sleep(2)
        try:
            page.wait_for_load_state("networkidle", timeout=30000)
        except Exception:
            pass
        try:
            html = page.content()
        except Exception:
            pass
        # Always save the rendered HTML (even when gated) so the tier is
        # inspectable: jsc_token = arithmetic (solvable), recaptcha = escalated.
        if a.out:
            d = os.path.dirname(a.out)
            if d:
                os.makedirs(d, exist_ok=True)
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"saved {len(html)} bytes -> {a.out}", file=sys.stderr)

        if is_gated(html):
            tier = "reCAPTCHA" if "recaptcha" in html.lower() else "arithmetic-jsc"
            print(f"STILL GATED ({tier} tier). arithmetic = retry later (tier "
                  "drops); reCAPTCHA = cool off the IP or use a logged-in "
                  "session.", file=sys.stderr)
            ctx.close()
            sys.exit(3)

        if a.text:
            el = page.query_selector("shreddit-post")
            if el:
                print(el.inner_text())
            else:
                main_el = page.query_selector("main")
                print(main_el.inner_text() if main_el else html[:4000])
        ctx.close()


if __name__ == "__main__":
    main()
