#!/usr/bin/env python3
"""Fetch ONE X status page and print its text (browser tier, cookies from
X_AUTH_TOKEN/X_CT0 user env when set). Usage:
    python fetch_x_status.py <status_id_or_url> [<more> ...]
Public status pages need no login; the cookies make replies/media render too."""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rag"))
import browser_head as bh  # noqa: E402


def norm_url(a: str) -> str:
    a = a.strip()
    if a.startswith("http"):
        return a
    return f"https://x.com/i/status/{a}"


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    results = []
    for arg in sys.argv[1:]:
        url = norm_url(arg)
        html = bh.fetch_html(
            url,
            until=lambda h: 'data-testid="tweetText"' in h,
            scrolls=3,
            scroll_sleep_s=2.0,
            verbose=False,
        )
        m = re.search(r'data-testid="tweetText"[^>]*>(.*?)</div>', html, re.S)
        text = ""
        if m:
            raw = m.group(1)
            raw = raw.replace("Show more", "")
            text = re.sub(r"<[^>]+>", "", raw)
            text = re.sub(r"&amp;", "&", text)
            text = re.sub(r"&quot;", '"', text)
            text = re.sub(r"&#39;", "'", text)
            text = re.sub(r"\s+", " ", text).strip()
        dm = re.search(r'datetime="([^"]+)"', html)
        results.append({"url": url, "text": text, "date": dm.group(1) if dm else "",
                        "rendered": bool(m)})
    print(json.dumps(results, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
