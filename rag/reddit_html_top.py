"""Reddit top-of-week via BROWSER-RENDERED HTML (the route that works when the
JSON API is IP-walled — verified 2026-10-26: www.reddit.com top page renders
shreddit-post cards with title/score/author/timestamp attributes after the JS
challenge auto-solves in the persistent profile).

Usage (CLI): python reddit_html_top.py <sub> [period]
  period: week (default) | day
Prints a JSON array of posts to stdout. Exit 3 = still gated.
"""
import html as _html
import json
import os
import re
import sys
import time

# Windows console is cp1252 — force UTF-8 so titles with ×/—/… don't crash print.
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


def _attr(tag: str, name: str):
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return _html.unescape(m.group(1)) if m else None


def parse_posts(page_html: str):
    """shreddit-post cards carry every field as attributes (verified 2026-10-26):
    post-title, score, author, created-timestamp, content-href/permalink,
    comment-count, upvote-ratio, id (t3_...). Dedup by id."""
    posts, seen = [], set()
    for tag in re.findall(r"<shreddit-post\b[^>]*>", page_html):
        pid = _attr(tag, "id") or _attr(tag, "post-id")
        title = _attr(tag, "post-title")
        if not title:
            continue
        if pid and pid in seen:
            continue
        seen.add(pid)
        score = _attr(tag, "score")
        posts.append({
            "id": pid or re.sub(r"[^a-z0-9]", "", (title or ""))[:30],
            "title": title,
            "score": int(score) if score and score.lstrip("-").isdigit() else 0,
            "author": _attr(tag, "author") or _attr(tag, "author-name"),
            "created": _attr(tag, "created-timestamp"),
            "url": _attr(tag, "content-href") or _attr(tag, "permalink"),
            "comments": _attr(tag, "comment-count"),
            "flair": _attr(tag, "post-language"),
        })
    return posts


def _launch(p, verbose=False):
    """Launch the persistent-profile context. The shared profile can be mid-close
    from the previous sub in a batched run, so a ProcessSingleton / access-denied
    lock error is TRANSIENT. Retry with backoff; as a last resort use a fresh
    temp profile (the challenge is arithmetic and auto-solves in a clean profile)."""
    def _launch_with(profile, fresh=False):
        return p.chromium.launch_persistent_context(
            profile, executable_path=CHROME, headless=True,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent=UA, viewport={"width": 1366, "height": 900})
    last_err = None
    for attempt in range(3):
        try:
            return _launch_with(PROFILE)
        except Exception as e:
            last_err = e
            msg = str(e)
            transient = any(s in msg for s in (
                "ProcessSingleton", "Access is denied", "already in use",
                "Lock file", "SingletonLock"))
            if not transient:
                raise
            if verbose:
                print(f"lock collision attempt {attempt+1}: {msg.splitlines()[0]}",
                      file=sys.stderr)
            time.sleep(4 * (attempt + 1))
    # fallback: fresh temp profile
    import tempfile
    tmp_profile = os.path.join(tempfile.gettempdir(), "reddit_html_fresh_profile")
    os.makedirs(tmp_profile, exist_ok=True)
    if verbose:
        print(f"shared profile locked after retries ({last_err}) -> fresh temp profile",
              file=sys.stderr)
    return _launch_with(tmp_profile)


def fetch_sub(sub: str, period: str = "week", timeout: int = 60):
    """Browser-render the top page and parse posts. Returns list (empty if gated)."""
    from playwright.sync_api import sync_playwright
    url = f"https://www.reddit.com/r/{sub}/top/?t={period}"
    with sync_playwright() as p:
        ctx = _launch(p, verbose=True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90 * 1000)
        except Exception:
            pass  # challenge redirect / slow network — the poll loop below recovers
        html = ""
        for _ in range(30):  # let the JS challenge run + redirect
            try:
                html = page.content()
            except Exception:
                time.sleep(2)
                continue
            head = html[:30000].lower()
            if "prove your humanity" not in head or "shreddit-post" in html:
                break
            time.sleep(2)
        for _ in range(5):  # lazy-load the feed (a challenge redirect mid-scroll
                            # destroys the execution context — swallow it)
            try:
                page.mouse.wheel(0, 6000)
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
    return parse_posts(html)


if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else "ComfyUI"
    period = sys.argv[2] if len(sys.argv) > 2 else "week"
    posts = fetch_sub(sub, period)
    if not posts:
        print("GATED (no shreddit-post cards rendered)", file=sys.stderr)
        sys.exit(3)
    print(json.dumps(posts, ensure_ascii=False, indent=1))
