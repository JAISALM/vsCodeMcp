"""Inspect the user's painted mask files + build a proper mask for the
remove-mic inpaint workflow.

ComfyUI's LoadImage MASK output = 1 - alpha (verified in nodes.py):
  - transparent pixels (alpha=0) -> mask=1 (regenerate)
  - opaque pixels (alpha=255)   -> mask=0 (keep)
So the mask file must be RGBA with TRANSPARENT = the region to remove.
The MaskEditor's clipspace-mask files are exactly that format.
"""
import os
import numpy as np
from PIL import Image

IN = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"

for f in ["clipspace-mask-1790600217258.png",
          "clipspace-paint-1790600217258.png",
          "remove_mic_mask.png"]:
    p = os.path.join(IN, f)
    if not os.path.exists(p):
        print("MISSING", f)
        continue
    im = Image.open(p)
    print("===", f, "mode", im.mode, "size", im.size)
    rgba = im.convert("RGBA")
    al = np.array(rgba)[:, :, 3]
    g = np.array(im.convert("L"))
    print("  alpha: min", al.min(), "max", al.max(),
          "transparent(=0) px", int((al == 0).sum()),
          "of", al.size)
    print("  gray:  min", g.min(), "max", g.max(),
          "white(>=128) px", int((g >= 128).sum()))
