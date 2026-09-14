# -*- coding: utf-8 -*-
"""
Crop the white pillarbox bars (left/right) that Krea2 sometimes adds, then pad
back to 2048x1152 (16:9) with BLACK (matches the void look). Deterministic post
fix - no re-rolling.

Usage:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\crop_white_bars.py"
"""
import sys
from pathlib import Path
from PIL import Image

SRC = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut")
DST = Path(r"D:\models\vsCodeMcp\Jaisal-intro\v5")
DST.mkdir(parents=True, exist_ok=True)

TARGET_W, TARGET_H = 2048, 1152
WHITE_THRESH = 245  # a column is a "white bar" if its mean brightness > this

FILES = [
    "kf2_seated_v5_00006_.png",
    "kf3a_headnormal_v5_00001_.png",
    "kf5_plants_grown_v5_00001_.png",
    "kf5a_stem_v5_00001_.png",
    "kf7a_page_v5_00001_.png",
    "kf3b_headtwisted_v5_00001_.png",
    "kf3c_head90_v5_00001_.png",
    "kf6_plants_dead_v5_00001_.png",
    "kf7b_page_mic_v5_00001_.png",
    "kf7c_cricket_v5_00001_.png",
]


def trim_white_bars(img):
    """Trim near-white columns from the left and right edges."""
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    # column means
    col_mean = [0] * w
    for x in range(w):
        s = 0
        for y in range(0, h, 4):  # sample every 4th row for speed
            s += px[x, y]
        col_mean[x] = s / (h // 4 + 1)
    left = 0
    while left < w and col_mean[left] > WHITE_THRESH:
        left += 1
    right = w - 1
    while right > left and col_mean[right] > WHITE_THRESH:
        right -= 1
    # safety: don't crop more than 40% off each side
    max_trim = int(w * 0.40)
    left = min(left, max_trim)
    right = max(right, w - 1 - max_trim)
    if left == 0 and right == w - 1:
        return img  # no white bars
    return img.crop((left, 0, right + 1, h))


def pad_to_16_9(img):
    """Center img on a 2048x1152 black canvas (scale to fit height)."""
    w, h = img.size
    # scale so height == TARGET_H
    scale = TARGET_H / h
    new_w = int(round(w * scale))
    new_h = TARGET_H
    img = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
    x = (TARGET_W - new_w) // 2
    canvas.paste(img, (x, 0))
    return canvas


for name in FILES:
    src = SRC / name
    if not src.exists():
        print(f"[MISSING] {name}")
        continue
    img = Image.open(src).convert("RGB")
    orig = img.size
    trimmed = trim_white_bars(img)
    tw = trimmed.size
    final = pad_to_16_9(trimmed)
    out = DST / name
    final.save(out)
    print(f"[ok] {name}: {orig} -> trimmed {tw} -> {final.size}  (bars removed: {tw[0] < orig[0]})")

print("\n[done] all saved to", DST)
