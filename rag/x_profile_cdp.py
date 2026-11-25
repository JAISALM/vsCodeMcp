"""CDP: fetch a profile timeline in the user's REAL Brave, parse with the
proven x_browser_fetch.parse_profile. Saves raw HTML + prints parsed JSON."""
import atexit
import json
import sys
import time

sys.path.insert(0, r"D:\models\vsCodeMcp\rag")
import x_browser_fetch  # noqa: E402

PORT = 9222


def fetch_profile_cdp(acct, out_html, scrolls=12, wait_ms=3000):
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
            page.goto(f"https://x.com/{acct}", wait_until="domcontentloaded", timeout=60000)
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
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html)
        return x_browser_fetch.parse_profile(html, acct)


if __name__ == "__main__":
    acct, out = sys.argv[1], sys.argv[2]
    scrolls = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    print(json.dumps(fetch_profile_cdp(acct, out, scrolls), ensure_ascii=False, indent=1))
