#!/usr/bin/env python3
"""
reddit_fetch.py — fetch Reddit threads/searches using the stored session cookie.

Reads the reddit_session cookie from the user env var REDDIT_SESSION_COOKIE
(set locally on this machine). Reddit's edge presents a JS work-challenge
(jsc_token + solution=input+input) to curl clients — this helper solves it
automatically and persists the resulting cookies in
C:\\Users\\user\\.dsh\\fetch_creds\\reddit_cookies.txt (Netscape format),
so the challenge is only re-solved when Reddit re-issues it.

IMPORTANT: HTTP goes through curl.exe (Python's own TLS fingerprint is
flat-blocked at Reddit's edge — measured 2026-10-11).

Usage:
  python reddit_fetch.py "https://www.reddit.com/r/LocalLLaMA/comments/1wcwa7i/.json?limit=5"
  python reddit_fetch.py --search "gemma 4 31b qat writing" --limit 5
  python reddit_fetch.py --user spanielrassler --limit 10   (a user's posts)

Output: raw JSON on stdout. Exit 0 = OK, non-zero = blocked/failed.

Run with: "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe"
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
CRED_DIR = os.path.expanduser(r"~\.dsh\fetch_creds")
JAR_FILE = os.path.join(CRED_DIR, "reddit_cookies.txt")


def curl_get(url, cookie_header):
    """One GET via curl with cookie jar. Returns (body, http_code)."""
    os.makedirs(CRED_DIR, exist_ok=True)
    if not os.path.exists(JAR_FILE):
        open(JAR_FILE, "w").close()  # curl -b needs an existing file
    hdrs = [
        f"User-Agent: {UA}",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language: en-US,en;q=0.9",
    ]
    if cookie_header:
        hdrs.append(cookie_header)
    cmd = ["curl.exe", "-s", "-m", "45"]
    for h in hdrs:
        cmd += ["-H", h]
    cmd += ["-b", JAR_FILE, "-c", JAR_FILE,
            "-w", "\n===HTTP:%{http_code}", url]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=90)
        out = r.stdout.decode("utf-8", "replace")
    except Exception as e:
        return f"curl error: {e}", 0
    m = re.search(r"===HTTP:(\d+)\s*$", out)
    code = int(m.group(1)) if m else 0
    body = re.sub(r"\n===HTTP:\d+\s*$", "", out)
    return body, code


def solve_challenge(body, cookie_header):
    """If body is a jsc work-challenge page, solve it (solution = input+input).
    Returns (new_body, code) or None when body has no challenge."""
    m = re.search(r'name="jsc_token" value="([0-9a-f]+)"', body)
    w = re.search(r'await\((async e=>[^)]+)\)\("([^"]+)"\)', body)
    if not (m and w):
        return None
    solution = w.group(2) + w.group(2)
    url = ("https://www.reddit.com/?solution=" + urllib.parse.quote(solution)
           + "&js_challenge=1&jsc_token=" + m.group(1))
    return curl_get(url, cookie_header)


def warm_up(cookie_header, attempts=3):
    """The challenge is served on the HOME page. Solve it so cookies
    (csrf_token, session_tracker, ...) land in the jar."""
    import time
    for i in range(attempts):
        body, code = curl_get("https://www.reddit.com/", cookie_header)
        if "jsc_token" not in body:
            return code == 200
        solved = solve_challenge(body, cookie_header)
        if solved and "jsc_token" not in solved[0]:
            return True
        time.sleep(4)
    return False


def fetch(url, cookie_header, attempts=3):
    import time
    last = None
    for i in range(attempts):
        warm_up(cookie_header)
        body, code = curl_get(url, cookie_header)
        last = f"HTTP {code}"
        if code == 200 and (body.lstrip().startswith("[") or body.lstrip().startswith("{")):
            return body
        if "jsc_token" in body:
            continue
        time.sleep(5)
    print(f"blocked after {attempts} attempts (last={last})", file=sys.stderr)
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    session_cookie = os.environ.get("REDDIT_SESSION_COOKIE", "")
    if not session_cookie:
        print("ERROR: REDDIT_SESSION_COOKIE env var not set (user level).", file=sys.stderr)
        sys.exit(2)
    cookie_header = f"Cookie: reddit_session={session_cookie}"

    args = sys.argv[1:]
    limit = 10
    if "--limit" in args:
        i = args.index("--limit")
        limit = int(args[i + 1])
        del args[i:i + 2]

    if args[0] == "--search":
        q = args[1]
        url = "https://www.reddit.com/search.json?limit=%d&q=%s" % (limit, urllib.parse.quote(q))
    elif args[0] == "--user":
        user = args[1]
        url = ("https://www.reddit.com/user/%s/submitted.json?limit=%d"
               % (urllib.parse.quote(user), limit))
    else:
        url = args[0]
        if ".json" not in url:
            url = url.rstrip("/") + "/.json?limit=5"

    result = fetch(url, cookie_header)
    if result is None:
        sys.exit(3)
    sys.stdout.write(result)


if __name__ == "__main__":
    main()
