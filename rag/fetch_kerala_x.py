"""X/Twitter HOT-TOPICS tier for the pradhana_kerala pipeline (D256).

Headlines tell the WHAT; X search tells the TALK — what Keralites are
actually arguing about right now (the "hot" layer). Same cookie tier as
x_browser_fetch.py: X_AUTH_TOKEN + X_CT0 (process env or HKCU\\Environment
fallback — set 2026-11-05, session expires ~2026-11-27; if X starts
rendering a login wall, re-copy the two cookies from Brave DevTools).

Usage:  python fetch_kerala_x.py [date]
Output: <store>/<date>/x_kerala_hot.md — top posts per query (text, author,
date, url). Anonymous X is login-walled (verified 2026-10-27) — without the
cookies this tier reports gated and logs, it does not fail the pipeline.
"""
import html as _html
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import browser_head
from x_browser_fetch import _user_env

STORE = os.path.join(ROOT, "pipelines", "pradhana_kerala", "store")

# Query set — English + Malayalam, "top" tab (f=top = engagement-ordered)
QUERIES = ["Kerala", "കേരളം", "Kochi OR Thrissur OR Kozhikode"]
MAX_PER_QUERY = 12


def _parse_articles(page_html, base_q):
    """Same article-block pattern as x_browser_fetch.parse_profile:
    status id from the first /status/<id> href, text from tweetText,
    date from <time datetime>."""
    posts, seen = [], set()
    for chunk in re.split(r"<article\b", page_html)[1:]:
        mid = re.search(r'href="/\w+/status/(\d+)"', chunk)
        if not mid:
            continue
        tid = mid.group(1)
        if tid in seen:
            continue
        seen.add(tid)
        mtext = re.search(r'data-testid="tweetText"[^>]*>(.*?)</div>', chunk, re.S)
        mtime = re.search(r"<time\b[^>]*datetime=\"([^\"]+)\"", chunk)
        text = re.sub(r"<[^>]+>", " ", mtext.group(1)) if mtext else ""
        text = re.sub(r"\s+", " ", _html.unescape(text)).strip()
        posts.append({"id": tid, "text": text[:1200],
                      "date": mtime.group(1) if mtime else "",
                      "url": f"https://x.com/i/status/{tid}"})
        if len(posts) >= MAX_PER_QUERY:
            break
    return posts


def fetch_query(query, poll_rounds=20, scrolls=4):
    """One X search in a cookie-injected browser head. Returns (posts, note)."""
    from playwright.sync_api import sync_playwright
    auth_token = _user_env("X_AUTH_TOKEN")
    ct0 = _user_env("X_CT0")
    if not (auth_token and ct0):
        return [], "gated: X_AUTH_TOKEN/X_CT0 not set — anonymous X is login-walled"
    url = f"https://x.com/search?q={quote_plus(query)}&src=typed_query&f=top"
    cookies = []
    for dom in (".x.com", ".twitter.com"):
        cookies.append({"name": "auth_token", "value": auth_token,
                        "domain": dom, "path": "/"})
        cookies.append({"name": "ct0", "value": ct0, "domain": dom, "path": "/"})
    with sync_playwright() as p:
        ctx = browser_head._launch(p, verbose=False)
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
                page.wait_for_timeout(2000)
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
    posts = _parse_articles(html, query)
    if not posts:
        if 'data-testid="tweetText"' not in html:
            return [], "gated: search page rendered no tweet blocks — " \
                       "cookies may be EXPIRED (re-copy from Brave DevTools)"
        return [], "rendered but 0 posts parsed (DOM change?)"
    return posts, None


def run(date=None):
    """All queries -> <store>/<date>/x_kerala_hot.md. Returns post count."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    day_dir = os.path.join(STORE, date)
    os.makedirs(day_dir, exist_ok=True)
    path = os.path.join(day_dir, "x_kerala_hot.md")
    total = 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# X hot topics (Kerala) — {date}\n")
        for q in QUERIES:
            try:
                posts, note = fetch_query(q)
            except Exception as e:
                posts, note = [], f"FAILED: {str(e)[:200]}"
            f.write(f"\n## query: {q}\n")
            if note:
                f.write(f"_{note}_\n")
                continue
            total += len(posts)
            for i, p in enumerate(posts, 1):
                f.write(f"\n{i}. [{p['date']}] {p['url']}\n   {p['text']}\n")
    return total


if __name__ == "__main__":
    n = run(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"x_kerala_hot: {n} posts")
