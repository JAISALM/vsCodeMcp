#!/usr/bin/env python
"""logo_to_transparent.py — deterministic blue-chroma color key (no ML, ring-safe).

Usage:
  python logo_to_transparent.py <input.png> <out_white.png> [out_black.png]

Background = royal-blue gradient (B - max(R,G) ~ 75-140). Logo = white fill (d~0)
+ black lines (d~5). Alpha ramp: d <= 30 -> opaque, d >= 70 -> transparent,
linear between (anti-aliased edges). Black variant = same alpha, RGB = inverted
luminance (white fill -> black, black lines -> white) for white shirts.
"""
import sys
import numpy as np
from PIL import Image

IN = sys.argv[1]
OUT_WHITE = sys.argv[2]
OUT_BLACK = sys.argv[3] if len(sys.argv) > 3 else None

D_LO = 30.0   # below this blue-chroma -> fully opaque
D_HI = 70.0   # above this -> fully transparent

arr = np.asarray(Image.open(IN).convert("RGB"), dtype=np.float32)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
d = b - np.maximum(r, g)

alpha = np.clip((D_HI - d) / (D_HI - D_LO), 0.0, 1.0) * 255.0
alpha = alpha.astype(np.uint8)

white = np.dstack([arr.astype(np.uint8), alpha])
Image.fromarray(white, "RGBA").save(OUT_WHITE)
print("saved", OUT_WHITE)

if OUT_BLACK:
    lum = arr.mean(axis=2)
    v = (255.0 - lum).clip(0, 255).astype(np.uint8)
    black = np.stack([v, v, v, alpha], axis=2)
    Image.fromarray(black, "RGBA").save(OUT_BLACK)
    print("saved", OUT_BLACK)
