# -*- coding: utf-8 -*-
"""
Build the Jaisal Kut INTRO B&W keyframe workflow.

Copies krea2_identity_edit.json -> krea2_intro_keyframes.json (so the title
workflow stays intact), stages a B&W version of the character reference, and
configures it for the Shot 1 keyframe (Jaisal seated, bare bulb, B&W cinematic).

Per D025 the identity edit inherits the reference's color tone, so the reference
is pre-converted to grayscale to force the B&W look (belt) + the instruction
also demands B&W (suspenders).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_intro_keyframes.py"
"""
import json
import shutil
from pathlib import Path
from PIL import Image

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
INPUT_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input")
CHAR_REF = Path(r"E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1\Image_00001_.png")

SRC = WF_DIR / "krea2_identity_edit.json"
DST = WF_DIR / "krea2_intro_keyframes.json"

# --- 1. Stage a B&W version of the character reference -----------------------
bw_ref_name = "intro_char_ref_bw.png"
im = Image.open(CHAR_REF).convert("L")  # grayscale
# keep it a 3-channel file (some loaders expect RGB) but B&W values
im_rgb = im.convert("RGB")
im_rgb.save(INPUT_DIR / bw_ref_name)
print(f"[stage] {CHAR_REF.name} -> input\\{bw_ref_name} (grayscale, {im.size})")

# --- 2. Copy the workflow ----------------------------------------------------
data = json.loads(SRC.read_text(encoding="utf-8"))

# --- 3. Configure nodes ------------------------------------------------------
SHOT1_POS = (
    "Black and white cinematic photograph, strictly monochrome, high contrast, "
    "fine film grain, no color at all. A dark empty room at night. A single bare "
    "bulb hangs from the ceiling on a thin cord, top-down at 45 degrees, the ONLY "
    "light source, casting one hard shadow, no fill light, deep black shadows. "
    "The same man (preserve his exact face and identity, dark wavy hair, dark "
    "shirt) sits at a simple wooden table, seated, calm and still, facing slightly "
    "toward the camera. Wide static framing, 35mm lens, eye level, deep focus. "
    "The room is sparse and empty - only the man, the table, and the swinging "
    "bulb. Black and white only, monochrome, moody, cinematic, dramatic hard "
    "shadow, fine grain."
)
SHOT1_NEG = (
    "color, colored, any color, warm tones, blue tones, multiple light sources, "
    "fill light, bright room, cluttered room, other people, extra characters, "
    "duplicates, text, watermark, logo, cartoon, 3d render, blurry, low quality"
)

for n in data["nodes"]:
    nid = n["id"]
    if nid == 72:  # LoadImage -> B&W character reference
        n["widgets_values"] = [bw_ref_name, "image"]
    elif nid == 84:  # positive instruction (widgets: [instruction, grounding_px, negative])
        n["widgets_values"] = [SHOT1_POS, 768, ""]
    elif nid == 85:  # negative (moot at cfg 1, but set it)
        n["widgets_values"] = [SHOT1_NEG, 768, ""]
    elif nid == 82:  # output size -> 1MP 16:9 (matches H3 native)
        n["widgets_values"] = [1344, 768, 1]
    elif nid == 29:  # save prefix
        n["widgets_values"] = ["jaisal_cut/intro_shot1"]

DST.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"[write] {DST.name}")
print("[done] validate + run krea2_intro_keyframes.json")
