"""X profile timeline via BROWSER HEAD (tier 3 of the X ladder — the other two
tiers: plain-HTTP syndication + the mcp engine both 429 from this IP).

Anonymous X is LOGIN-WALLED (verified 2026-10-27: the profile page renders a
login modal, zero tweet text in the DOM, no __NEXT_DATA__, syndication
endpoint serves an HTML shell, all nitter mirrors dead, threadreader 404).
The SAME pattern that solved Reddit (REDDIT_SESSION_COOKIE env → cookie
header) solves X: set **X_AUTH_TOKEN** (auth_token) and **X_CT0** (ct0)
user-level env vars and this tier injects them as cookies — the timeline
then renders fully, exactly like a logged-in browser (VS Code's integrated
browser with your session would do the same).

Usage (CLI): python x_browser_fetch.py <acct>
Prints a JSON object: {"account", "tweets": [{id, text, date, url}...],
"gated": bool, "note": ...}. Exit 0 = tweets or clean gated report.
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import browser_head


def fetch_account(acct: str, poll_rounds: int = 25, scrolls: int = 6):
    from playwright.sync_api import sync_playwright
    url = f"https://x.com/{acct}"
    cookies = []
    if os.environ.get("X_AUTH_TOKEN"):
        cookies.append({"name": "auth_token", "value": os.environ["X_AUTH_TOKEN"],
                        "domain": ".x.com", "path": "/"})
    if os.environ.get("X_CT0"):
        cookies.append({"name": "ct0", "value": os.environ["X_CT0"],
                        "domain": ".x.com", "path": "/"})
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
    return parse_profile(html, acct)


def parse_profile(page_html: str, acct: str):
    """Parse tweet blocks from the profile DOM. Anonymous walled pages carry
    article shells but NO tweet text — detect that and report it as a login
    wall with the actionable fix (set X_AUTH_TOKEN / X_CT0)."""
    tweets, seen = [], set()
    # each <article> chunk: id from the tweetDate link, text from tweetText,
    # date from <time datetime=...>
    for chunk in re.split(r"<article\b", page_html)[1:]:
        mid = re.search(r'data-testid="tweetDate" href="/\w+/status/(\d+)"', chunk)
        if not mid:
            continue
        tid = mid.group(1)
        if tid in seen:
            continue
        seen.add(tid)
        mtext = re.search(r'data-testid="tweetText"[^>]*>(.*?)</div>', chunk, re.S)
        mtime = re.search(r"<time\b[^>]*datetime=\"([^\"]+)\"", chunk)
        text = re.sub(r"<[^>]+>", " ", mtext.group(1)) if mtext else ""
        text = re.sub(r"\s+", " ", text).strip()
        tweets.append({
            "id": tid,
            "text": _html_unescape(text)[:4000],
            "date": mtime.group(1) if mtime else "",
            "url": f"https://x.com/{acct}/status/{tid}",
        })
    has_tweet_text = 'data-testid="tweetText"' in page_html
    gated = not tweets and not has_tweet_text
    note = ""
    if gated:
        note = ("timeline did not render — anonymous X is login-gated (the profile "
                "page loads but tweets sit behind the login wall; verified 2026-10-27: "
                "syndication 429, mcp engine 429, all nitter mirrors dead, "
                "threadreader 404, browser head renders article shells without "
                "text). FIX (one-time, same pattern as REDDIT_SESSION_COOKIE): set "
                "user-level env X_AUTH_TOKEN (auth_token) + X_CT0 (ct0) — the "
                "browser tier then injects the session cookies and reads the full "
                "timeline.")
    elif not tweets:
        note = "page rendered but no tweet blocks found (DOM layout change?)"
    return {"account": acct, "tweets": tweets, "gated": gated, "note": note}


def _html_unescape(s):
    import html as _h
    return _h.unescape(s)


if __name__ == "__main__":
    acct = sys.argv[1] if len(sys.argv) > 1 else "BennyDaBall_OG"
    print(json.dumps(fetch_account(acct), ensure_ascii=False, indent=1))
