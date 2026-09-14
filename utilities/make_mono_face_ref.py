"""
Create a monochrome face-only close-up reference for the kf3b 180-degree head shot.

CORRECT SOURCE (user-confirmed 2026-09-13): the REAL character reference set
  E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1\
Image_00001_.png = a clean FRONTAL face close-up of the character (dark wavy
hair, black shirt, white background). This is the identity we copy the face
from - NOT the Krea2 render (jaisal_face_v4_A.png was the WRONG character).

Output: jaisal_face_mono_closeup.png - face-dominant square crop, converted to
        grayscale (monochrome) so it matches the B&W horror scene.

This file is loaded into node 113 (the SECOND reference / identity slot) of
krea2_identity_edit.json, so the model copies the ACTUAL face instead of
hallucinating one when it rotates the head fully around.
"""
from PIL import Image, ImageOps
import os

SRC = r"E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1\Image_00001_.png"
OUT = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\jaisal_face_mono_closeup.png"

im = Image.open(SRC).convert("RGB")
W, H = im.size
print(f"source: {W}x{H}")

# Face-dominant square crop. In the 1136x912 source the head is centered
# horizontally and sits in the upper-middle. Crop a square that keeps the
# whole head + a little neck/shoulder context.
cx = int(W * 0.50)   # face is centered
cy = int(H * 0.42)   # head sits in the upper-middle
side = int(H * 0.78)  # ~711 px square, face-dominant

left = max(0, cx - side // 2)
top = max(0, cy - side // 2)
right = min(W, left + side)
bottom = min(H, top + side)
# keep it square
side = min(right - left, bottom - top)
crop = im.crop((left, top, left + side, top + side))
print(f"crop box: ({left},{top}) -> ({left+side},{top+side})  = {side}x{side}")

# Convert to monochrome (grayscale).
mono = ImageOps.grayscale(crop)

# Optional: slight contrast boost so the face reads clearly in B&W.
mono = ImageOps.autocontrast(mono, cutoff=1)

mono.save(OUT)
print(f"saved: {OUT}  ({mono.size[0]}x{mono.size[1]}, mode={mono.mode})")
print(f"exists: {os.path.exists(OUT)}")
