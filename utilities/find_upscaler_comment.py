#!/usr/bin/env python
"""Find the latent-upscaler comment in the saved plastic-look post DOM."""
import re, html, sys

p = r"D:\models\vsCodeMcp\data\h3_plastic_look"
raw = open(p, encoding="utf-8", errors="ignore").read()
# strip tags per comment-ish chunk: find text around keywords
keywords = ["upscale", "Upscaler", "latent", "github", "LBH", "fake", "plastic", "real"]
# extract all visible text
text = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S)
text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S)
text = re.sub(r"<[^>]+>", " ", text)
text = html.unescape(text)
text = re.sub(r"\s+", " ", text)

hits = []
for kw in ["latent", "upscale", "Upscaler", "LBH", "github.com"]:
    for m in re.finditer(re.escape(kw), text, flags=re.I):
        s = max(0, m.start() - 400)
        e = min(len(text), m.end() + 400)
        hits.append(text[s:e])

seen = set()
out = []
for h in hits:
    key = h[:80]
    if key in seen:
        continue
    seen.add(key)
    out.append(h)

print(f"{len(out)} unique hit contexts\n")
for i, h in enumerate(out[:12]):
    print(f"--- hit {i} ---")
    print(h)
    print()
