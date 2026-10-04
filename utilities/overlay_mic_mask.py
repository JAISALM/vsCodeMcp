"""Overlay the mask's regenerate-region (transparent) in RED on the base image
so the user can confirm it's over the correct (black) mic."""
import os
import numpy as np
from PIL import Image

IN = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
OUT = r"d:\models\vsCodeMcp\Jaisal-intro\kf2_headset"
os.makedirs(OUT, exist_ok=True)

base = Image.open(os.path.join(IN, "mic_small_id_00001_.png")).convert("RGB")
mask = np.array(Image.open(os.path.join(IN, "remove_mic_mask.png")).convert("RGBA"))[:, :, 3]

# regenerate region = transparent (alpha < 255)
reg = mask < 255
overlay = np.array(base)
overlay[reg] = [255, 0, 0]  # red = will be regenerated
Image.fromarray(overlay).save(os.path.join(OUT, "remove_mic_mask_overlay.png"))

# bounding box of the regenerate region
ys, xs = np.where(reg)
print("regenerate region bbox: x", xs.min(), "-", xs.max(),
      "y", ys.min(), "-", ys.max(), "of", base.size)
print("saved overlay ->", os.path.join(OUT, "remove_mic_mask_overlay.png"))
