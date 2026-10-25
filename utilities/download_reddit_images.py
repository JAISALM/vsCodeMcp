#!/usr/bin/env python
"""Download full-size images from a saved Reddit DOM via Playwright's request context.

Direct urllib/requests downloads of preview.redd.it return 403 (bot-blocked);
a request through the browser's context carries proper headers and works.

Usage:
    python download_reddit_images.py <dom.html> <outdir> [--limit N] [--headed]

Reads the unique content images (preview.redd.it, no query params) from the DOM,
opens the thread page once to warm the session, then fetches each full-size image.
"""
import os
import re
import sys


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return
    dom, outdir = args[0], args[1]
    limit = 10
    if "--limit" in sys.argv:
        i = sys.argv.index("--limit")
        limit = int(sys.argv[i + 1])

    h = open(dom, encoding="utf-8", errors="ignore").read()
    thread_url = None
    m = re.search(r"<link rel=\"canonical\" href=\"(https://www\.reddit\.com/[^\"]+)\"", h)
    if m:
        thread_url = m.group(1)

    urls, seen = [], set()
    for x in re.findall(r"https://preview\.redd\.it/([a-z0-9]{12,}\.[a-z]{2,4})", h):
        u = f"https://preview.redd.it/{x}"
        if u not in seen:
            seen.add(u)
            urls.append(u)
    urls = urls[:limit]
    print(f"{len(urls)} images to fetch; thread={thread_url}")

    os.makedirs(outdir, exist_ok=True)
    from playwright.sync_api import sync_playwright

    tag = os.path.basename(dom).split("_")[0]
    profile = r"C:\Users\user\.dsh\fetch_creds\browser_profile"
    ok = 0
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            profile, headless=("--headed" not in flags),
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        )
        if thread_url:
            try:
                ctx.new_page().goto(thread_url, timeout=60000, wait_until="domcontentloaded")
                import time
                time.sleep(3)
            except Exception as e:
                print("page warm-up failed (continuing):", e)
        for i, u in enumerate(urls, 1):
            ext = u.rsplit(".", 1)[-1]
            out = os.path.join(outdir, f"{tag}_{i:02d}_{u.rsplit('/', 1)[-1]}")
            try:
                resp = ctx.request.get(u, timeout=60000)
                data = resp.body()
                if resp.status == 200 and len(data) > 1000:
                    open(out, "wb").write(data)
                    ok += 1
                    print(f"{tag} {i:02d} OK {len(data)//1024} KB {u}")
                else:
                    print(f"{tag} {i:02d} HTTP {resp.status} {u}")
            except Exception as e:
                print(f"{tag} {i:02d} FAIL {e} {u}")
        ctx.close()
    print(f"{ok}/{len(urls)} downloaded -> {outdir}")


if __name__ == "__main__":
    main()
