#!/usr/bin/env python
"""Open a Reddit thread in headless Chromium, click each post image to open the
full-res lightbox, capture the full-size image URL it loads, and download it.

Usage:
    python expand_reddit_images.py <thread_url> <dom.html> <outdir> [--limit N] [--headed]

The DOM is only used to find the thread's post-media image ids (to know which
images belong to the thread vs. comment/aside thumbnails).
"""
import os
import re
import sys
import time


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--") and sys.argv.index(a) > 0]
    argv = sys.argv[1:]
    if len(argv) < 3:
        print(__doc__)
        return
    thread_url, dom, outdir = argv[0], argv[1], argv[2]
    limit = 8
    if "--limit" in argv:
        i = argv.index("--limit")
        limit = int(argv[i + 1])

    h = open(dom, encoding="utf-8", errors="ignore").read()
    ids = []
    seen = set()
    for m in re.findall(r"https://preview\.redd\.it/([a-z0-9]{12,}\.[a-z]{2,4})", h):
        if m not in seen:
            seen.add(m)
            ids.append(m)
    print(f"thread images in DOM: {len(ids)}")

    os.makedirs(outdir, exist_ok=True)
    from playwright.sync_api import sync_playwright

    tag = os.path.basename(dom).split("_")[0]
    profile = r"C:\Users\user\.dsh\fetch_creds\browser_profile"
    saved = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            profile, headless=("--headed" not in argv),
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            viewport={"width": 1400, "height": 900},
        )
        page = ctx.new_page()
        try:
            page.goto(thread_url, timeout=90000, wait_until="domcontentloaded")
            time.sleep(5)
        except Exception as e:
            print("goto failed:", e)
        # find post-media image elements (shreddit-image or media imgs)
        for i, imgid in enumerate(ids[:limit], 1):
            try:
                # locate the thumbnail element by src fragment
                el = page.locator(f"img[src*='{imgid}']").first
                if el.count() == 0:
                    print(f"{tag} {i:02d} not found in page: {imgid}")
                    continue
                el.scroll_into_view_if_needed()
                time.sleep(1)
                el.click()
                time.sleep(3)
                # find the largest image now on the page (lightbox)
                src = page.evaluate(
                    """() => {
                        let best = null, bestArea = 0;
                        for (const im of document.querySelectorAll('img')) {
                            const a = (im.naturalWidth || 0) * (im.naturalHeight || 0);
                            if (a > bestArea) { bestArea = a; best = im; }
                        }
                        return best ? {src: best.src, w: best.naturalWidth, h: best.naturalHeight} : null;
                    }"""
                )
                if not src:
                    print(f"{tag} {i:02d} no lightbox img")
                    page.keyboard.press("Escape")
                    continue
                print(f"{tag} {i:02d} lightbox {src['w']}x{src['h']} {src['src'][:120]}")
                out = os.path.join(outdir, f"{tag}_{i:02d}_{imgid.split('.', 1)[0]}.{imgid.rsplit('.', 1)[-1]}")
                resp = ctx.request.get(src["src"], timeout=90000)
                data = resp.body()
                if resp.status == 200 and len(data) > 2000:
                    open(out, "wb").write(data)
                    saved.append((i, src["w"], src["h"], len(data)))
                    print(f"{tag} {i:02d} SAVED {len(data)//1024} KB")
                else:
                    print(f"{tag} {i:02d} HTTP {resp.status}")
                page.keyboard.press("Escape")
                time.sleep(1.5)
            except Exception as e:
                print(f"{tag} {i:02d} FAIL {e}")
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
        ctx.close()
    print(f"saved {len(saved)}/{min(limit, len(ids))}")
    for i, w, hh, b in saved:
        print(f"  {tag} {i:02d} {w}x{hh} {b//1024} KB")


if __name__ == "__main__":
    main()
