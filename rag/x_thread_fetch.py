"""X THREAD (conversation) via BROWSER HEAD + X session cookies (tier 3.5 of the
X ladder). Navigates a status URL and extracts every rendered <article> — the
main tweet + the replies X renders in the conversation view. Reuses the exact
cookie-injection pattern of x_browser_fetch.py (auth_token + ct0 into BOTH
.x.com and .twitter.com, process env OR HKCU\\Environment fallback).

Usage: python x_thread_fetch.py <status_url> [more_urls...]
Prints one JSON object per URL: {"tweets": [{id, user, date, text, links}...],
"gated": bool, "note": ...}.
"""
import html as _h
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


def _user_env(name):
    v = os.environ.get(name, "")
    if v:
        return v
    if sys.platform == "win32":
        import winreg
        try:
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
            val, _t = winreg.QueryValueEx(k, name)
            winreg.CloseKey(k)
            return val or ""
        except Exception:
            return ""
    return ""


def fetch_thread(status_url, polls=20, scrolls=14):
    from playwright.sync_api import sync_playwright
    auth = _user_env("X_AUTH_TOKEN")
    ct0 = _user_env("X_CT0")
    cookies = []
    for d in (".x.com", ".twitter.com"):
        if auth:
            cookies.append({"name": "auth_token", "value": auth, "domain": d, "path": "/"})
        if ct0:
            cookies.append({"name": "ct0", "value": ct0, "domain": d, "path": "/"})
    with sync_playwright() as p:
        ctx = browser_head._launch(p, verbose=False)
        if cookies:
            try:
                ctx.add_cookies(cookies)
            except Exception:
                pass
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(status_url, wait_until="domcontentloaded", timeout=90 * 1000)
        except Exception:
            pass
        html = ""
        for _ in range(polls):
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
                page.wait_for_timeout(3000)
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
    return parse_thread(html)


def parse_thread(page_html):
    out, seen = [], set()
    # chunk on <article>; the main tweet on a status page is also an article,
    # but its header link may carry query params (?ref=...) — so the status-id
    # regex must NOT require the id to end right before the closing quote.
    for chunk in re.split(r"<article\b", page_html)[1:]:
        mid = re.search(r'href="(?:https?://[\w.]*\.)?(?:x\.com|twitter\.com|/)?/?(\w+)/status/(\d+)', chunk)
        if not mid:
            continue
        tid = mid.group(2)
        if tid in seen:
            continue
        seen.add(tid)
        muser = re.search(r'data-testid="username"[^>]*>\s*(?:<span[^>]*>)?\s*([^<]+)', chunk)
        mtext = re.search(r'data-testid="tweetText"[^>]*>(.*?)</div>', chunk, re.S)
        mtime = re.search(r"<time\b[^>]*datetime=\"([^\"]+)\"", chunk)
        text = re.sub(r"<[^>]+>", " ", mtext.group(1)) if mtext else ""
        text = re.sub(r"\s+", " ", _h.unescape(text)).strip()
        links = re.findall(r'href="(https?://(?!x\.com|twitter\.com)[^"]+)"', chunk)
        out.append({
            "id": tid,
            "user": muser.group(1).strip() if muser else "",
            "date": mtime.group(1) if mtime else "",
            "text": text[:3000],
            "links": links[:10],
        })
    # fallback: tweetText blocks not inside any captured article (DOM variant)
    for mtext in re.finditer(r'data-testid="tweetText"[^>]*>(.*?)</div>', page_html, re.S):
        text = re.sub(r"<[^>]+>", " ", mtext.group(1))
        text = re.sub(r"\s+", " ", _h.unescape(text)).strip()
        if not text or any(t["text"] == text for t in out):
            continue
        start = max(0, mtext.start() - 5000)
        ctx = page_html[start:mtext.end() + 3000]
        mid = re.search(r'href="(?:https?://[\w.]*\.)?(?:x\.com|twitter\.com|/)?/?(\w+)/status/(\d+)', ctx)
        tid = mid.group(2) if mid else ""
        if tid and tid in seen:
            continue
        seen.add(tid)
        mtime = re.search(r"<time\b[^>]*datetime=\"([^\"]+)\"", ctx)
        links = re.findall(r'href="(https?://(?!x\.com|twitter\.com)[^"]+)"', page_html[mtext.end():mtext.end() + 3000])
        out.append({
            "id": tid,
            "user": "",
            "date": mtime.group(1) if mtime else "",
            "text": text[:3000],
            "links": links[:10],
        })
    has_text = 'data-testid="tweetText"' in page_html
    note = ""
    if not out and not has_text:
        note = ("login wall or no render — if the X cookies (X_AUTH_TOKEN/X_CT0) are "
                "expired (they last ~30 days from the 2026-11-05 copy, exp 2026-11-27), "
                "re-copy from Brave DevTools; or restart Brave ONCE with "
                "--remote-debugging-port=9222 for the CDP tier (real_browser_fetch.py).")
    elif not out:
        note = "page rendered but no article blocks found (DOM layout change?)"
    return {"tweets": out, "gated": not out and not has_text, "note": note}


if __name__ == "__main__":
    for url in sys.argv[1:]:
        print(json.dumps(fetch_thread(url), ensure_ascii=False, indent=1))
