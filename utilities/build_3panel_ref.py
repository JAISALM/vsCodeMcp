#!/usr/bin/env python
"""Build the 3-panel sheet reference for 09j: face | crest(top-right) | kit(bottom-right).
2304x1536 (3:2, matches sheet output aspect -> i2i sees full composite, no crop).
PE image budget (549 widget[14]=4194304 px) >= 3.54MP composite -> architect sees full res."""
from PIL import Image
import os, shutil

IN = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
OUT1 = os.path.join(IN, "jaisal_sheet_ref_3panel.png")
OUT2 = r"D:\models\vsCodeMcp\data\refs\jaisal_sheet_ref_3panel.png"

face = Image.open(os.path.join(IN, "jaisal_portrait_HD.png")).convert("RGB")
crest = Image.open(os.path.join(IN, "jaisal_crest_ref.png")).convert("RGB")
kit = Image.open(os.path.join(IN, "jaisal_kit_ref.png")).convert("RGB")
print("face", face.size, "crest", crest.size, "kit", kit.size)

W, H = 2304, 1536
canvas = Image.new("RGB", (W, H), (255, 255, 255))

# face: scale to full height 1536
fw = round(face.width * H / face.height)          # 896/1120*1536 = 1229
face_r = face.resize((fw, H), Image.LANCZOS)
canvas.paste(face_r, (0, 0))

# right column: x = fw + 16, width = W - fw - 16
gap = 16
col_x = fw + gap
col_w = W - col_x                                  # 2304-1245 = 1059
sq = 760                                           # 760 + 16 + 760 = 1536 exact
cx_off = (col_w - sq) // 2                         # center square in column

crest_r = crest.resize((sq, sq), Image.LANCZOS)
kit_r = kit.resize((sq, sq), Image.LANCZOS)
canvas.paste(crest_r, (col_x + cx_off, 0))
canvas.paste(kit_r, (col_x + cx_off, sq + gap))

canvas.save(OUT1)
os.makedirs(os.path.dirname(OUT2), exist_ok=True)
shutil.copyfile(OUT1, OUT2)
print("saved", OUT1, canvas.size, os.path.getsize(OUT1))
print("copied", OUT2)
