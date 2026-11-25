"""CDP: open a status page in the user's real Brave, repeatedly click the
'Show more' / 'Show probable spam' / 'Show thread' buttons to load every
reply, save the final HTML, and print all extracted tweets + external links.
Closes its own tab on exit."""
import atexit
import html as _h
import json
import re
import sys
import time

sys.path.insert(0, r"D:\models\vsCodeMcp\rag")
PORT = 9222


def run(status_url, out_html, rounds=12):
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
        for i in range(rounds):
            clicked = 0
            for label in ("Show more", "Show probable spam", "Show thread", "Show all replies"):
                for btn in page.query_selector_all("div[role='button']"):
                    try:
                        t = (btn.inner_text() or "").strip()
                        if t == label:
                            btn.scroll_into_view_if_needed()
                            time.sleep(0.4)
                            btn.click()
                            clicked += 1
                    except Exception:
                        pass
            if clicked == 0:
                break
            page.wait_for_timeout(2500)
            try:
                page.mouse.wheel(0, 20000)
                page.wait_for_timeout(2500)
                html = page.content()
            except Exception:
                pass
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"saved {len(html)} chars -> {out_html}", file=sys.stderr)
        return html


def extract(h):
    out, seen = [], set()
    for chunk in re.split(r"<article\b", h)[1:]:
        mid = re.search(r'href="(?:https?://[\w.]*\.)?(?:x\.com|twitter\.com|/)?/?(\w+)/status/(\d+)', chunk)
        if not mid:
            continue
        tid = mid.group(2)
        if tid in seen:
            continue
        seen.add(tid)
        mtime = re.search(r"<time\b[^>]*datetime=\"([^\"]+)\"", chunk)
        links = sorted(set(re.findall(r'href="(https?://(?!x\.com|twitter\.com)[^"]+)"', chunk)))
        links = [l for l in links if not any(x in l for x in ("support.x.com", "help.x.com", "business.x.com", "x.com/i/"))]
        mtext = re.search(r'data-testid="tweetText"[^>]*>(.*?)</div>', chunk, re.S)
        text = re.sub(r"<[^>]+>", " ", mtext.group(1)) if mtext else ""
        text = re.sub(r"\s+", " ", _h.unescape(text)).strip()
        out.append({"id": tid, "date": mtime.group(1) if mtime else "", "text": text[:400], "links": links})
    special = sorted(set(re.findall(r'https?://(?:github\.com|github\.io|huggingface\.co|drive\.google\.com|dropbox\.com|mega\.nz|reflct\.app)[^"\'\\ ]+', h)))
    return out, special


if __name__ == "__main__":
    url, out = sys.argv[1], sys.argv[2]
    h = run(url, out)
    tweets, special = extract(h)
    print(json.dumps({"tweets": tweets, "special_urls": special}, ensure_ascii=False, indent=1))
