import os
from PIL import Image, ImageDraw, ImageFilter

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\mic+paper.png'
OUT = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\mic_mask.png'

img = Image.open(SRC)
W, H = img.size
print('image size:', W, H)

# Mask: WHITE = region to INPAINT (the mic), BLACK = keep.
# The big broadcast mic is centered: head ~y400-580, stand down to table base ~y950.
mask = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(mask)

# Head (ellipse) + stand (rectangle) + base (ellipse), generous coverage.
cx = int(W * 0.50)
d.ellipse([cx-110, 380, cx+110, 600], fill=255)          # mic head
d.rectangle([cx-45, 560, cx+45, 930], fill=255)          # stand
d.ellipse([cx-90, 890, cx+90, 970], fill=255)            # base on table

# Feather the edges so the inpaint blends.
mask = mask.filter(ImageFilter.GaussianBlur(12))

mask.save(OUT)
print('mask saved:', OUT)
