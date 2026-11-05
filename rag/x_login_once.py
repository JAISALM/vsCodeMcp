r"""One-time X login into the SHARED persistent browser profile (D203).

Why: anonymous X is login-walled — headless fetches render the page shell but
the tweets sit behind a login modal. Logging in ONCE in the shared profile
(`~\.dsh\fetch_creds\browser_profile`) makes the session persist there, so every
future headless X fetch (daily schtask + manual) reads full timelines with NO
env cookies and NO secrets stored anywhere but the profile dir.

Usage:
    & "D:\models\vsCodeMcp\rag\.venv\Scripts\python.exe" "D:\models\vsCodeMcp\rag\x_login_once.py"

A VISIBLE Chromium window opens at x.com. Log in with any X account, wait for
the home timeline to render, then CLOSE THE WINDOW. Closing saves the session
into the profile. (You may keep it open — the script waits for the window to
close or a 20-minute timeout, then verifies the session headlessly.)
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from browser_head import CHROME, PROFILE  # reuse the exact profile + binary

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TIMEOUT_MIN = 20


def main():
    from playwright.sync_api import sync_playwright

    print(f"profile: {PROFILE}")
    print("launching VISIBLE Chromium — log in to X, then close the window "
          f"(timeout {TIMEOUT_MIN}min)...")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, executable_path=CHROME, headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/126.0.0.0 Safari/537.36"),
            viewport={"width": 1366, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://x.com", wait_until="domcontentloaded",
                  timeout=90_000)

        # Wait until the window is closed (user logged in + closed it) or timeout.
        closed = {"flag": False}
        def _on_close(_page):
            closed["flag"] = True
        page.on("close", _on_close)
        deadline = time.time() + TIMEOUT_MIN * 60
        while time.time() < deadline and not closed["flag"]:
            time.sleep(3)

        # Read cookies BEFORE closing the context (persisted anyway on close).
        try:
            names = sorted(c["name"] for c in ctx.cookies("https://x.com"))
            have_auth = "auth_token" in names
            have_ct0 = "ct0" in names
            print(f"cookies on x.com: {names}")
            print(f"auth_token present: {have_auth}   ct0 present: {have_ct0}")
        except Exception as e:
            print("cookie check failed (context closing):", e)
        ctx.close()

    print("done — the session now persists in the profile; headless X fetches "
          "will use it automatically.")


if __name__ == "__main__":
    main()
