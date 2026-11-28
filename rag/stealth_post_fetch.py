#!/usr/bin/env python3
"""Stealth per-post page fetch — the depth tier WITHOUT the automation
fingerprint (2026-11-28, D279).

WHY THIS EXISTS:
  The persistent-profile head (reddit_post_fetch.py) runs Playwright's
  BUNDLED Chromium in OLD-HEADLESS mode — even with
  --disable-blink-features=AutomationControlled it leaks headless/build
  signals (headless UA traces, WebGL, empty plugins, the bundled-Chromium
  fingerprint). Reddit's 11-23 "network policy" wall keys on exactly that:
  the SAME egress IP gets only the softer "prove your humanity" tier
  through the engine class, so the hard block is the IP x
  automation-fingerprint, not the IP alone.

  This head uses the mechanism already proven at the TOP tier
  (real_browser_fetch.py passes the wall): a REAL browser binary (Brave),
  but OUR OWN anonymous profile (no user cookies, no user session) and
  OUR OWN port (9223), driven via raw CDP (connect_over_cdp) — no
  Playwright-launched context, no headless mode (headed +
  --start-minimized: invisible on the desktop, clean fingerprint).

  The instance stays WARM between runs (port reuse) — challenge state and
  cookies persist across daily runs, exactly like the old persistent
  profile pattern. Zero dependency on the user's running browser: a
  separate profile dir + port means no interference with his Brave.

USAGE:
  python stealth_post_fetch.py <post_url> [more_urls...] [--top 5]
Prints the same JSON shape as reddit_post_fetch.py:
  {"results": [{url, title, body, comments:[{author, score, text}], note}],
   "note"}. Exit 0 = at least one post rendered, 3 = walled/no content.
"""
import json
import os
import re
import sys
import time

if sys.platform == "win32":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

PORT = 9223
PROFILE = os.path.join(os.path.expanduser("~"), ".dsh", "fetch_creds", "stealth_profile")
PACING_S = 10

BROWSER_CANDIDATES = [
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def _find_browser():
    for c in BROWSER_CANDIDATES:
        if os.path.exists(c):
            return c
    print("ERROR: no real browser binary found (Brave/Edge/Chrome)", file=sys.stderr)
    sys.exit(2)


def _port_live(port=PORT):
    import socket
    s = socket.socket()
    s.settimeout(1.5)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def _ensure_head(exe):
    """Launch our own minimized real-browser instance if :9223 is down.
    Reuse if already warm (challenge state persists across runs)."""
    import subprocess
    if _port_live():
        print("stealth head already warm on :%d" % PORT, file=sys.stderr)
        return
    os.makedirs(PROFILE, exist_ok=True)
    args = [exe, "--user-data-dir=" + PROFILE,
            "--remote-debugging-port=%d" % PORT,
            "--remote-allow-origins=*",
            "--disable-blink-features=AutomationControlled",
            "--no-first-run", "--no-default-browser-check",
            "--disable-features=Translate",
            "--start-minimized"]
    subprocess.Popen(args, shell=False)
    for _ in range(40):
        time.sleep(1)
        if _port_live():
            print("stealth head live on :%d (own profile, minimized)" % PORT, file=sys.stderr)
            return
    print("ERROR: stealth head CDP port never came up", file=sys.stderr)
    sys.exit(2)


def _clean(s, limit):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:limit]


def _is_blocked(html):
    low = html[:30000].lower()
    if "whoa there" in low:
        return "rate-limited (whoa there, pardner)"
    if "<title>blocked</title>" in low or low.startswith("<!doctype html><html><head> <title>blocked"):
        return "blocked page"
    if "prove your humanity" in low and "shreddit-post" not in html:
        return "gated (prove-your-humanity)"
    return None


def _extract_dom(page, url, top):
    """DOM-based extraction (2026-11-28): the raw-HTML regex path misses
    because shreddit lazy-loads comment bodies via faceplate-loader chunks;
    the LIVE DOM carries the rendered text. Nested shreddit-comment elements
    carry the WHOLE thread text — keep only top-level ones (parent is not a
    shreddit-comment)."""
    title = ""
    try:
        title = (page.title() or "").strip()
    except Exception:
        pass
    body = ""
    post = page.query_selector("shreddit-post")
    if post:
        try:
            body = (post.inner_text() or "").strip()
        except Exception:
            body = ""
    comments = []
    seen = set()
    for el in page.query_selector_all("shreddit-comment"):
        try:
            if el.evaluate("el => !!(el.parentElement && el.parentElement.closest('shreddit-comment'))"):
                continue  # nested thread — its text repeats inside the parent
            t = (el.inner_text() or "").strip()
        except Exception:
            continue
        if not t or t in seen:
            continue
        seen.add(t)
        comments.append(t[:2000])
        if len(comments) >= top:
            break
    note = ""
    if not body and not comments:
        note = ("page rendered but no body/comments extracted "
                "(DOM layout change? link-only post?)")
    return title, body, comments


def _extract(html, url, top):
    title = ""
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m:
        t = _clean(m.group(1), 300)
        if t and t != "Blocked":
            title = t
    body = ""
    m = re.search(r"<shreddit-post\b.*?>(.*?)</shreddit-post>", html, re.S)
    post_html = m.group(1) if m else html
    mb = re.search(r'class="[^"]*usd-prose[^"]*"[^>]*>(.*?)</div>', post_html, re.S)
    if mb:
        body = _clean(re.sub(r"<[^>]+>", " ", mb.group(1)), 6000)
    if not body:
        mb = re.search(r'data-test-id="post-content"[^>]*>(.*?)</div>', post_html, re.S)
        if mb:
            body = _clean(re.sub(r"<[^>]+>", " ", mb.group(1)), 6000)
    comments = []
    for ch in re.split(r"<shreddit-comment\b", html)[1:]:
        ma = re.search(r'class="[^"]*author[^"]*"[^>]*>([^<]*)<', ch)
        ms = re.search(r"([0-9][0-9.,kK]*)\s*(?:points|upvotes|votes)", ch)
        mt = re.search(r'class="[^"]*usd-prose[^"]*"[^>]*>(.*?)</div>', ch, re.S)
        if not mt:
            continue
        text = _clean(re.sub(r"<[^>]+>", " ", mt.group(1)), 1200)
        if not text:
            continue
        comments.append({
            "author": _clean(ma.group(1), 60) if ma else "",
            "score": ms.group(1) if ms else "",
            "text": text,
        })
        if len(comments) >= top:
            break
    return title, body, comments


def fetch_posts(urls, top=5, poll_rounds=20):
    from playwright.sync_api import sync_playwright
    exe = _find_browser()
    _ensure_head(exe)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:%d" % PORT)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        try:
            for i, url in enumerate(urls):
                if i:
                    time.sleep(PACING_S)
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                except Exception:
                    pass
                html = ""
                for _ in range(poll_rounds):
                    try:
                        html = page.content()
                    except Exception:
                        time.sleep(2)
                        continue
                    if _is_blocked(html):
                        break
                    if "<shreddit-post" in html and "<shreddit-comment" in html:
                        break
                    time.sleep(2)
                block = _is_blocked(html)
                if block:
                    results.append({"url": url, "title": "", "body": "",
                                    "comments": [], "note": "STOP: %s "
                                    "(remaining posts deferred to next run)" % block})
                    break
                try:
                    page.mouse.wheel(0, 6000)
                    page.wait_for_timeout(2500)
                    html = page.content()
                except Exception:
                    pass
                title, body, comments = _extract_dom(page, url, top)
                note = ""
                if not body and not comments:
                    note = ("page rendered but no body/comments extracted "
                            "(DOM layout change? link-only post?)")
                results.append({"url": url, "title": title, "body": body,
                                "comments": comments, "note": note})
        finally:
            try:
                page.close()
            except Exception:
                pass
    note = ""
    if results and results[0].get("note", "").startswith("STOP"):
        note = results[0]["note"]
    return {"results": results, "note": note}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    r = fetch_posts(a.urls[:8], a.top)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    ok = any(x["body"] or x["comments"] for x in r["results"])
    sys.exit(0 if ok else 3)
