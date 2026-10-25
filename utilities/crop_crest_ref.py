#!/usr/bin/env python
"""Tight crop of ONLY the fist roundel from jaisal_kit_ref.png -> 512x512 crest ref."""
from PIL import Image
import os

inp = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
im = Image.open(os.path.join(inp, "jaisal_kit_ref.png")).convert("RGB")
# Emblem circle in the 1152x1152 source: center ~(700, 328), circle radius ~55px.
# Tight square with ~35% margin.
cx, cy, half = 700, 328, 75
box = (cx-half, cy-half, cx+half, cy+half)
crop = im.crop(box).resize((512, 512), Image.LANCZOS)
out = os.path.join(inp, "jaisal_crest_ref.png")
crop.save(out)
print("saved:", out, os.path.getsize(out), "bytes")
