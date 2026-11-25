"""X THREAD via the user's REAL Brave over CDP (tier 3b of the X ladder).

Reuses parse_thread from x_thread_fetch.py. Opens a NEW tab in the user's
actual logged-in Brave (zero cookies to copy, zero automation fingerprint),
navigates the status URL, scrolls the conversation to load lazy replies,
extracts all articles (main tweet + replies), then CLOSES the fetch tab
(atexit) so no stray tabs are left.

Usage: python x_thread_cdp.py <status_url> [more_urls...]
Prints one JSON object per URL: {"tweets": [...], "gated": bool, "note": ...}
"""
import atexit
import json
import sys
import time

sys.path.insert(0, r"D:\models\vsCodeMcp\rag")
from x_thread_fetch import parse_thread  # noqa: E402

PORT = 9222


def fetch_thread_cdp(status_url, scrolls=16, wait_ms=3000):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()

        def _close():
            try:
                page.close()
            except Exception:
                pass

        atexit.register(_close)
        try:
            page.emulate_media(color_scheme="dark")
        except Exception:
            pass
        try:
            page.goto(status_url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            pass
        html = ""
        for _ in range(20):
            try:
                html = page.content()
            except Exception:
                time.sleep(2)
                continue
            if 'data-testid="tweetText"' in html:
                break
            time.sleep(2)
        for _ in range(scrolls):
            try:
                page.mouse.wheel(0, 12000)
                page.wait_for_timeout(wait_ms)
            except Exception:
                pass
            try:
                html = page.content()
            except Exception:
                pass
        return parse_thread(html)


if __name__ == "__main__":
    for url in sys.argv[1:]:
        print(json.dumps(fetch_thread_cdp(url), ensure_ascii=False, indent=1))
