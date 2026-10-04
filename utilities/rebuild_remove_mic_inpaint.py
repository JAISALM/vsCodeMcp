"""Rebuild krea2_inpaint_remove_mic.json by CLONING the proven
krea2_kf2_manual_inpaint.json (exact structure that worked for the kf2 chair):
  LoadImage(base) -> VAEEncodeForInpaint -> SetLatentNoiseMask -> KSampler
  -> VAEDecode -> ImageCompositeMasked -> SaveImage
The SAME LoadImage node provides both the image AND the mask — the user paints
directly on the base image in the Mask Editor (right-click -> Open in Mask
Editor). No separate mask file.
Only swaps: base image filename, prompts, save prefix.
"""
import json
import os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = os.path.join(WF, "krea2_kf2_manual_inpaint.json")
DST = os.path.join(WF, "krea2_inpaint_remove_mic.json")

POS = ("empty weathered wooden table surface, matching the surrounding wood grain "
       "and lighting exactly, plain table, seamless continuation of the table")
NEG = ("microphone, mic, mic stand, black microphone, two microphones, objects, "
       "person, chair, color, text, watermark")

d = json.load(open(SRC, encoding="utf-8"))

for n in d["nodes"]:
    if n["id"] == 200:  # base image (user paints mask on THIS image)
        n["widgets_values"][0] = "mic_small_id_00001_.png"
        n["title"] = "paint the black mic here (right-click -> Open in Mask Editor)"
    elif n["id"] == 208:  # positive
        n["widgets_values"][0] = POS
    elif n["id"] == 209:  # negative
        n["widgets_values"][0] = NEG
    elif n["id"] == 213:  # save prefix
        n["widgets_values"][0] = "jaisal_cut/mic_single"

json.dump(d, open(DST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("WROTE", DST)
print("nodes:", len(d["nodes"]), "links:", len(d["links"]))
