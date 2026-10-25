#!/usr/bin/env python
"""Run AFTER 10a_frontal_base_zidane: stages the best FACEFRONTAL_ZIDANE output into
input\\zidane_portrait_front.png, then builds the zidane 3-panel sheet reference
(input\\zidane_sheet_ref_3panel.png, 2304x1536 3:2): LEFT = face (dominant),
TOP-RIGHT = zidane crest (dark green ground), BOTTOM-RIGHT = zidane kit flat-lay.
Usage:  python build_zidane_sheet_ref.py [a|b|c]   (branch to stage; default = newest)
"""
import glob, os, re, shutil, sys
from PIL import Image

IN = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
OUTDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"

# SaveImage prefix without a slash -> file lands at the OUTPUT ROOT
# (output\FACEFRONTAL2_ZIDANE_a_00001_.png), not in a subfolder.
# The counter increments per run (v4b run took _00001_, v5b run -> _00002_), so
# match ANY zero-padded counter, then pick by mtime (newest = the run you just did).
branch = sys.argv[1] if len(sys.argv) > 1 else None
pats = [
    rf"^FACEFRONTAL3_ZIDANE_[0-9]{4,6}_.png$",  # D163 i2i face lock (newest = the one you just ran)
    rf"^FACEFRONTAL2_ZIDANE_{re.escape(branch) if branch else '[abc]'}_[0-9]{4,6}_.png$",
    r"^FACEFRONTAL_I2I_ZIDANE_[0-9]{4,6}_.png$",
    rf"^FACEFRONTAL_ZIDANE_{re.escape(branch) if branch else '[abc]'}_[0-9]{4,6}_.png$",
]
cands = []
for fn in os.listdir(OUTDIR):
    if any(re.match(pat, fn) for pat in pats):
        cands.append(os.path.join(OUTDIR, fn))
cands = sorted(cands, key=os.path.getmtime)
assert cands, "no FACEFRONTAL_ZIDANE output yet — run 10a_frontal_base_zidane first"
src = cands[-1]
face = Image.open(src).convert("RGB")
print("staging", os.path.basename(src), face.size)
face_path = os.path.join(IN, "zidane_portrait_front.png")
face.save(face_path)

crest = Image.open(os.path.join(IN, "zidane_crest_ref.png")).convert("RGB")
kit = Image.open(os.path.join(IN, "zidane_kit_ref.png")).convert("RGB")
print("crest", crest.size, "kit", kit.size)

W, H = 2304, 1536
canvas = Image.new("RGB", (W, H), (255, 255, 255))
fw = round(face.width * H / face.height)
face_r = face.resize((fw, H), Image.LANCZOS)
canvas.paste(face_r, (0, 0))
gap = 16
col_x = fw + gap
col_w = W - col_x
sq = 760
cx_off = (col_w - sq) // 2
canvas.paste(crest.resize((sq, sq), Image.LANCZOS), (col_x + cx_off, 0))
canvas.paste(kit.resize((sq, sq), Image.LANCZOS), (col_x + cx_off, sq + gap))
out = os.path.join(IN, "zidane_sheet_ref_3panel.png")
canvas.save(out)
print("saved", out, canvas.size, os.path.getsize(out))
