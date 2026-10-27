"""SHARED BROWSER-HEAD TIER — the proven fallback for any source our plain-HTTP
tiers fail on (403/429/JS-gated/challenge-walled).

PROOF (2026-10-26, user directive — "VS Code is able to do this, why is DSH
struggling?"): our own Playwright Chromium head is the SAME engine class as VS
Code's integrated browser. Reddit JSON is IP-walled (403 even with a valid
session cookie) but the BROWSER-RENDERED top page is not — `shreddit-post`
cards carry every field as attributes. This module generalizes that mechanism:

    from browser_head import fetch_html
    html = fetch_html("https://example.com/x",
                      until=lambda h: 'data-testid="tweetText"' in h)

Rules (D203):
- Persistent profile `~\.dsh\fetch_creds\browser_profile` (challenge state
  persists across runs — same profile the VS Code-proof used).
- Profile-lock collisions (ProcessSingleton / access-denied from a previous
  run's mid-close) are TRANSIENT: retry with backoff, then a fresh temp
  profile (challenges auto-solve in a clean profile).
- A source is only "failed" after the browser tier has ALSO failed. Never
  report a source as walled when a real browser could render it.
"""
import html as _html
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
FRESH_PROFILE = os.path.join(
    os.environ.get("TEMP", os.environ.get("TMP", r"D:\models\vsCodeMcp\rag\temp")),
    "browser_head_fresh_profile")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

_TRANSIENT_MARKERS = ("ProcessSingleton", "Access is denied", "already in use",
                      "Lock file", "SingletonLock")


def _launch(p, verbose=False):
    def _launch_with(profile):
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
            if not any(s in msg for s in _TRANSIENT_MARKERS):
                raise
            if verbose:
                print(f"browser_head: profile lock attempt {attempt+1}: "
                      f"{msg.splitlines()[0]}", file=sys.stderr)
            time.sleep(4 * (attempt + 1))
    os.makedirs(FRESH_PROFILE, exist_ok=True)
    if verbose:
        print(f"browser_head: shared profile locked after retries -> fresh temp profile",
              file=sys.stderr)
    return _launch_with(FRESH_PROFILE)


def fetch_html(url, until=None, goto_timeout_ms=90_000, poll_rounds=30,
               poll_sleep_s=2.0, scrolls=5, scroll_px=6000, scroll_sleep_s=2.0,
               verbose=False):
    """Browser-render `url`, wait until `until(html)` is True (challenge
    auto-solves in the persistent profile), optionally lazy-load by scrolling.
    Returns the final page HTML ('' if everything failed)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx = _launch(p, verbose=verbose)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=goto_timeout_ms)
        except Exception:
            pass  # challenge redirect / slow network — the poll loop recovers
        html = ""
        for _ in range(poll_rounds):
            try:
                html = page.content()
            except Exception:
                time.sleep(poll_sleep_s)
                continue
            if until is None or until(html):
                break
            time.sleep(poll_sleep_s)
        for _ in range(scrolls):
            try:
                page.mouse.wheel(0, scroll_px)
                page.wait_for_timeout(int(scroll_sleep_s * 1000))
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
    return html


def attr(tag: str, name: str):
    """Read attribute `name` from a tag string (unescape entities)."""
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return _html.unescape(m.group(1)) if m else None
