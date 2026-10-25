#!/usr/bin/env python
"""Stage 2BZ sheet inputs in the latest-tree ComfyUI:

1. create neutral_placeholder.png (white 1024x1024) in input/
2. copy the two HD character faces into input/
"""
import os
from PIL import Image

IN = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
OUT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\refset_v7"

ph = os.path.join(IN, "neutral_placeholder.png")
if not os.path.exists(ph):
    Image.new("RGB", (1024, 1024), (255, 255, 255)).save(ph)
    print("created neutral_placeholder.png (white 1024x1024)")
else:
    print("neutral_placeholder.png exists")

import shutil
for name in ("zidane", "jaisal"):
    src = os.path.join(OUT, f"{name}_portrait_HD_00001_.png")
    dst = os.path.join(IN, f"{name}_portrait_HD.png")
    shutil.copy2(src, dst)
    print(f"copied {name}_portrait_HD.png ({os.path.getsize(dst)//1024//1024} MB)")
