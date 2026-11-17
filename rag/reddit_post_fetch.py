#!/usr/bin/env python3
"""Reddit per-post page fetch via the PERSISTENT BROWSER HEAD (depth tier).

WHY THIS EXISTS (verified 2026-11-17):
  The .json endpoints are IP-rate-limited from this machine EVEN WITH A VALID
  SESSION COOKIE (HTTP 403 with/without cookie; browser with cookie gets the
  "whoa there, pardner" page; JWT checked 2026-11-17: cookie valid to
  2027-04-04 — the wall is the egress IP on the JSON API, not the cookie).
  The HTML pages, however, render in the SAME persistent profile the top-page
  card tier uses (D202) — so the depth tier for full content (post body + top
  comments) is a per-post PAGE fetch, not a JSON call.

PACING (hard-won 2026-11-17): a burst of ~6 requests in 20 min (incl. .json
endpoints) tripped a whole-IP "Blocked" cooldown. So: ONE browser session,
at most a handful of posts, 10 s between posts, and on the first
"Blocked"/"whoa"/gate the batch STOPS (remaining posts enrich next run).
The list (top-page) tier keeps working on its own schedule — the depth tier
is additive and best-effort.

USAGE:
  python reddit_post_fetch.py <post_url> [more_urls...] [--top 5]
Prints a JSON object: {"results": [{url, title, body, comments:[{author,
score, text}], note}], "note"}. Exit 0 = at least one post rendered.
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

CHROME = r"C:\Users\user\AppData\Local\ms-playwright\chromium-1234\chrome-win64\chrome.exe"
PROFILE = os.path.expanduser(r"~\.dsh\fetch_creds\browser_profile")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
PACING_S = 10


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
    results = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, executable_path=CHROME, headless=True,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent=UA, viewport={"width": 1366, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
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
                # whole-IP cooldown — stop the batch, retry next run
                results.append({"url": url, "title": "", "body": "",
                                "comments": [], "note": f"STOP: {block} "
                                "(remaining posts deferred to next run)"})
                break
            # one gentle scroll to hydrate a few more comments
            try:
                page.mouse.wheel(0, 6000)
                page.wait_for_timeout(2500)
                html = page.content()
            except Exception:
                pass
            title, body, comments = _extract(html, url, top)
            note = ""
            if not body and not comments:
                note = ("page rendered but no body/comments extracted "
                        "(DOM layout change? link-only post?)")
            results.append({"url": url, "title": title, "body": body,
                            "comments": comments, "note": note})
        try:
            ctx.close()
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
