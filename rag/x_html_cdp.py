"""CDP: save raw HTML of a status page for inspection (no parsing)."""
import atexit
import sys
import time

sys.path.insert(0, r"D:\models\vsCodeMcp\rag")
PORT = 9222


def fetch_html_cdp(status_url, out_path, scrolls=16, wait_ms=3000):
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
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"saved {len(html)} chars -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    url, out = sys.argv[1], sys.argv[2]
    scrolls = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    fetch_html_cdp(url, out, scrolls)
