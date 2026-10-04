"""Convert the user's MaskEditor paint layer into a proper ComfyUI mask.

ComfyUI LoadImage MASK = 1 - alpha:
  transparent (alpha=0)  -> mask=1 (regenerate)
  opaque (alpha=255)     -> mask=0 (keep)

The paint layer (clipspace-paint-*.png) has the mic region OPAQUE (alpha=255)
on a transparent background. We INVERT the alpha so the mic region becomes
transparent (regenerate) and the rest becomes opaque (keep).

Also applies a Gaussian feather to the edges for a smooth transition.
"""
import os
import numpy as np
from PIL import Image, ImageFilter

IN = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
PAINT = os.path.join(IN, "clipspace-paint-1790600217258.png")
OUT = os.path.join(IN, "remove_mic_mask.png")

# Load the paint layer (RGBA: mic region opaque, rest transparent)
paint = Image.open(PAINT).convert("RGBA")
alpha = np.array(paint)[:, :, 3]  # 255 = painted (mic), 0 = unpainted

# Invert: painted region -> transparent (0), rest -> opaque (255)
new_alpha = 255 - alpha

# Feather the edges (Gaussian blur on the alpha for a smooth transition)
alpha_img = Image.fromarray(new_alpha, mode="L")
alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(radius=8))
new_alpha = np.array(alpha_img)

# Build the RGBA mask: transparent where we want to regenerate, opaque elsewhere
# The RGB channels don't matter for the MASK output (only alpha is read),
# but we fill them with a neutral gray so the file is viewable.
rgb = np.zeros((*new_alpha.shape, 3), dtype=np.uint8)
rgb[:, :, 0] = 128  # gray
rgb[:, :, 1] = 128
rgb[:, :, 2] = 128
rgba = np.dstack([rgb, new_alpha])
mask = Image.fromarray(rgba, mode="RGBA")
mask.save(OUT)

# Verify
verify = np.array(Image.open(OUT).convert("RGBA"))[:, :, 3]
print(f"Saved {OUT}")
print(f"  size: {mask.size}")
print(f"  transparent (regenerate) px: {int((verify == 0).sum())}")
print(f"  opaque (keep) px: {int((verify == 255).sum())}")
print(f"  feathered (partial) px: {int(((verify > 0) & (verify < 255)).sum())}")
print(f"  LoadImage MASK will be: 1 where transparent (regenerate), 0 where opaque (keep)")
