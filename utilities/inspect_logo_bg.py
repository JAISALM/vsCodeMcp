#!/usr/bin/env python
"""Inspect background colors of logo_1fist_mono.png (corners, edges, top band) to tune the color key."""
import sys
from PIL import Image
from collections import Counter

im = Image.open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\logo_1fist_mono.png").convert("RGB")
W, H = im.size
print("size", im.size)
px = im.load()

def sample(name, x, y):
    print(f"{name} ({x},{y}) = {px[x, y]}")

sample("TL", 2, 2)
sample("TR", W - 3, 2)
sample("BL", 2, H - 3)
sample("BR", W - 3, H - 3)
sample("top-center", W // 2, 2)
sample("top-band y=10", W // 2, 10)
sample("top-band y=30", W // 2, 30)
sample("mid-left", 2, H // 2)
sample("bottom-center", W // 2, H - 3)

# top 40 rows: color distribution (is there a gray band?)
c = Counter()
for y in range(0, 40):
    for x in range(0, W, 16):
        c[px[x, y]] += 1
print("top 40 rows top colors:", c.most_common(6))

# corner regions: distribution (background uniformity)
cc = Counter()
for (x0, y0) in [(0, 0), (W - 60, 0), (0, H - 60), (W - 60, H - 60)]:
    for y in range(y0, min(y0 + 60, H), 4):
        for x in range(x0, min(x0 + 60, W), 4):
            cc[px[x, y]] += 1
print("corner regions top colors:", cc.most_common(6))

# min/max blue channel spread across all edge pixels
edges = []
for x in range(0, W, 8):
    edges.append(px[x, 0]); edges.append(px[x, H - 1])
for y in range(0, H, 8):
    edges.append(px[0, y]); edges.append(px[W - 1, y])
rmin = min(p[0] for p in edges); rmax = max(p[0] for p in edges)
gmin = min(p[1] for p in edges); gmax = max(p[1] for p in edges)
bmin = min(p[2] for p in edges); bmax = max(p[2] for p in edges)
print(f"edge pixel spread: R {rmin}-{rmax}, G {gmin}-{gmax}, B {bmin}-{bmax}")
