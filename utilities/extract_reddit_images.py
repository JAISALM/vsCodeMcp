#!/usr/bin/env python
"""Extract image URLs (and comment snippets) from a saved Reddit DOM (browser-rendered HTML).

Usage:
    python extract_reddit_images.py <dom.html> [--out <urls.txt>] [--comments]

Prints unique i.reddit.com / preview.redd.it / redditstatic image URLs.
With --comments, also prints comment bodies (first 400 chars each).
"""
import re
import sys


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args:
        print(__doc__)
        return
    src = args[0]
    h = open(src, encoding="utf-8", errors="ignore").read()

    urls = []
    seen = set()
    pats = [
        r"https://i\.reddit\.com/[^\"'\s<>\\]+?\.(?:png|jpe?g|webp)(?:\?[^\"'\s<>\\]*)?",
        r"https://preview\.redd\.it/[^\"'\s<>\\]+?\.(?:png|jpe?g|webp)(?:\?[^\"'\s<>\\]*)?",
        r"https://www\.redditstatic\.com/[^\"'\s<>\\]+?\.(?:png|jpe?g|webp)(?:\?[^\"'\s<>\\]*)?",
        r"https://external-preview\.reddit\.com/[^\"'\s<>\\]+?\.(?:png|jpe?g|webp)(?:\?[^\"'\s<>\\]*)?",
    ]
    for pat in pats:
        for m in re.findall(pat, h):
            u = m.rstrip('"\\')
            if u not in seen:
                seen.add(u)
                urls.append(u)
    print(f"=== {len(urls)} unique images")
    for u in urls:
        print(u)

    if "--out" in flags:
        i = flags.index("--out")
        out = args[i + 1]
        open(out, "w", encoding="utf-8").write("\n".join(urls))
        print(f"saved -> {out}")

    if "--comments" in flags:
        # shreddit-comment bodies
        bodies = re.findall(r'shreddit-comment[^>]*>.*?<div class="md[^"]*">(.*?)</div>', h, re.S)
        if not bodies:
            bodies = re.findall(r'"body"\s*:\s*"((?:[^"\\]|\\.)*)"', h)
        print(f"=== {len(bodies)} comment bodies")
        for b in bodies[:30]:
            b = re.sub(r"<[^>]+>", " ", b)
            b = b.encode("utf-8", "ignore").decode("unicode_escape", errors="ignore") if "\\" in b else b
            b = re.sub(r"\s+", " ", b).strip()
            print("-", b[:400])


if __name__ == "__main__":
    main()
