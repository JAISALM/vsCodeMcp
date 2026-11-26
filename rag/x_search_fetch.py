"""X SEARCH via browser head (tier 3 of the X ladder) — the keyword tier.

The account tier (x_browser_fetch.py) only reads TIMELINES of configured
accounts. This fetcher reads X's "Latest" search tab for a query — same
engine class (persistent profile + injected X_AUTH_TOKEN/X_CT0 session
cookies), so it works exactly like a logged-in browser typing the search.

Usage: python x_search_fetch.py "<query>" [--max 15]
Prints JSON: {"query": ..., "tweets": [...], "gated": bool, "note": ...}
Each tweet: {id, user, date, text, url, links} — the per-tweet author is
taken from the article's own header link (search results span many authors).
"""
import argparse
import html as _h
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x_browser_fetch  # noqa: E402  (_user_env cookie helper)


def parse_search(page_html: str):
    tweets, seen = [], set()
    for chunk in re.split(r"<article\b", page_html)[1:]:
        mid = re.search(r'href="(?:https?://[\w.]*\.)?(?:x\.com|twitter\.com|/)?/?(\w+)/status/(\d+)', chunk)
        if not mid:
            continue
        user, tid = mid.group(1), mid.group(2)
        if tid in seen:
            continue
        seen.add(tid)
        mtime = re.search(r"<time\b[^>]*datetime=\"([^\"]+)\"", chunk)
        mtext = re.search(r'data-testid="tweetText"[^>]*>(.*?)</div>', chunk, re.S)
        text = re.sub(r"<[^>]+>", " ", mtext.group(1)) if mtext else ""
        text = re.sub(r"\s+", " ", _h.unescape(text)).strip()
        links = sorted(set(re.findall(r'href="(https?://(?!x\.com|twitter\.com)[^"]+)"', chunk)))
        links = [l for l in links if not any(x in l for x in ("support.x.com", "help.x.com", "business.x.com", "x.com/i/"))]
        tweets.append({
            "id": tid,
            "user": user,
            "date": mtime.group(1) if mtime else "",
            "text": text[:2000],
            "url": f"https://x.com/{user}/status/{tid}",
            "links": links[:8],
        })
    has_tweet_text = 'data-testid="tweetText"' in page_html
    gated = not tweets and not has_tweet_text
    note = ""
    if gated:
        note = ("search page did not render tweet blocks — likely a login wall "
                "(check X_AUTH_TOKEN / X_CT0 user-level env, valid to 2026-11-27) "
                "or a DOM change on the search page.")
    elif not tweets:
        note = "page rendered but no tweet blocks found (DOM layout change?)"
    return tweets, gated, note


def fetch_search(query: str, poll_rounds: int = 25, scrolls: int = 4) -> dict:
    from urllib.parse import quote_plus
    from playwright.sync_api import sync_playwright
    import browser_head
    url = f"https://x.com/search?q={quote_plus(query)}&src=typed_query&f=live"
    auth_token = x_browser_fetch._user_env("X_AUTH_TOKEN")
    ct0 = x_browser_fetch._user_env("X_CT0")
    cookies = []
    for _dom in (".x.com", ".twitter.com"):
        if auth_token:
            cookies.append({"name": "auth_token", "value": auth_token,
                            "domain": _dom, "path": "/"})
        if ct0:
            cookies.append({"name": "ct0", "value": ct0,
                            "domain": _dom, "path": "/"})
    with sync_playwright() as p:
        ctx = browser_head._launch(p, verbose=True)
        if cookies:
            try:
                ctx.add_cookies(cookies)
            except Exception:
                pass
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90 * 1000)
        except Exception:
            pass
        html = ""
        for _ in range(poll_rounds):
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
                page.mouse.wheel(0, 8000)
                page.wait_for_timeout(2500)
            except Exception:
                pass
        try:
            html = page.content()
        except Exception:
            pass
        try:
            ctx.close()
        except Exception:
            pass
    tweets, gated, note = parse_search(html)
    return {"query": query, "tweets": tweets, "gated": gated, "note": note}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--max", type=int, default=15)
    a = ap.parse_args()
    res = fetch_search(a.query)
    res["tweets"] = res["tweets"][:a.max]
    print(json.dumps(res, ensure_ascii=False, indent=1))
