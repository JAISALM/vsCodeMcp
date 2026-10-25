#!/usr/bin/env python
"""zidane_crest_ref.png = the approved monochrome fist roundel on a DARK GREEN ground.
Recolors only the blue-ground pixels of jaisal_crest_ref.png (roundel pixels untouched);
the green is sampled from the actual zidane kit (zidane_kit_ref.png) so it matches the jersey.
"""
import numpy as np
from PIL import Image
import os, shutil

IN = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"

crest = np.array(Image.open(os.path.join(IN, "jaisal_crest_ref.png")).convert("RGB")).astype(np.int16)
kit = np.array(Image.open(os.path.join(IN, "zidane_kit_ref.png")).convert("RGB")).astype(np.int16)

# sample the dark green from the kit: green-dominant, mid-dark pixels
r, g, b = kit[:,:,0], kit[:,:,1], kit[:,:,2]
mask = (g > r + 8) & (g > b + 8) & (g < 150) & (g > 25)
sel = kit[mask]
assert len(sel) > 5000, f"too few green pixels: {len(sel)}"
green = np.median(sel, axis=0)
print("sampled kit green:", green, "from", len(sel), "px")

R, G, B = crest[:,:,0], crest[:,:,1], crest[:,:,2]
blue_score = B - np.maximum(R, G)   # >0 = bluer than the other channels
out = crest.copy()
# pure blue ground
pure = blue_score > 35
out[pure] = green
# anti-aliased edge: blend original -> green by how blue it is
edge = (blue_score > 10) & (blue_score <= 35)
t = np.clip((blue_score[edge] - 10) / 25.0, 0, 1)[:, None]
out[edge] = (crest[edge] * (1 - t) + green[None, :] * t)

res = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
out1 = os.path.join(IN, "zidane_crest_ref.png")
out2 = r"D:\models\vsCodeMcp\data\crests\zidane_crest_ref.png"
res.save(out1)
os.makedirs(os.path.dirname(out2), exist_ok=True)
shutil.copyfile(out1, out2)
print("saved", out1, res.size, os.path.getsize(out1))
print("copied", out2)
