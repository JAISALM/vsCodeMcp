# -*- coding: utf-8 -*-
"""
Build the Jaisal Kut INTRO B&W BASE (scene-master) workflow — v4 (user feedback 2026-09-11).

WHY v4:
  The v3 base image (kf1_scene_master_00001_.png) was REJECTED by the user:
  it was TILTED, a SIDE SHOT, with a WALL visible - "completely wrong".
  The base image is the ANCHOR for every other keyframe (they are identity-edits
  of it), so if the base is wrong, ALL downstream shots inherit the wrong
  setting. The user's rule: "build the base v4 first, if I confirm then we can
  go ahead - otherwise the setting itself will be different for each [image]".

  So this script builds ONLY the base image (kf0_base_v4). The user reviews it.
  Only after confirmation do we build the rest of the v4 set from this anchor.

v4 BASE PROMPT FIXES (vs v3):
  1. STRAIGHT-ON, perfectly centered, perfectly symmetric, eye level, static -
     NOT tilted, NOT a side shot, NOT a Dutch angle.
  2. NO walls / NO ceiling / NO pillars - pure black darkness outside the light
     pool (the light-pool-darkness rule).
  3. ONE chair, CENTERED directly behind the table (NOT to the left or right).
  4. Bulb at TOP CENTER, the only light source.
  5. Empty room (no person) - this is the scene master.

Node changes (clean copy of krea2_identity_edit.json, native UI format):
  node 72 (LoadImage)  = intro_char_ref_bw.png  (grayscale character ref -> B&W style, D025)
  node 84 (positive)   = v4 base instruction (grounding_px 768)
  node 85 (negative)   = v4 base negatives (tilt / side / wall / extra-chair exclusions)
  node 29 (SaveImage)  = jaisal_cut/kf0_base_v4
  node 114 (rgthree comparer) = bypass (mode 4)
  node 82 (EmptySD3LatentImage) = [2048, 1152, 1]  (2K 16:9, matches v3 output 1928x1088)

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_intro_base_v4.py"
"""
import json
from pathlib import Path

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WF_DIR / "krea2_identity_edit.json"

BW_REF = "blank_black.png"  # EMPTY base: no character ref (blank source, ref_boost 0)

# --- v4 BASE (scene master) --------------------------------------------------
# The anchor image: empty room, table + ONE centered chair, bulb top-center,
# straight-on / centered / symmetric / no wall / no tilt.
BASE_POS = (
    "Black and white cinematic photograph, strictly monochrome, high contrast, "
    "clean and sharp, no color at all, NO film grain, NO noise, NO speckles, "
    "clean deep blacks, crisp detail. "
    "A single bare bulb hangs from above on a thin cord at the TOP CENTER of "
    "the frame, the ONLY light source. "
    "A simple wooden table sits in the CENTER of the frame, and ONE simple "
    "wooden chair is placed directly BEHIND the table, perfectly centered "
    "(the chair is dead center behind the table, NOT to the left, NOT to the "
    "right). The scene is empty - no person, just the table, the single "
    "centered chair, and the hanging bulb. "
    "The table, chair and bulb are ISOLATED in a PURE BLACK VOID - there is "
    "NO back wall, NO side walls, NO ceiling, NO floor, NO ground, NO "
    "surface, NO horizon line, NO room, NO pillars, NO columns. The objects "
    "float in infinite pure black darkness. The bulb's light forms a small "
    "pool that illuminates ONLY the table, chair and bulb; everything "
    "OUTSIDE that small light pool is COMPLETE PURE BLACK - total darkness, "
    "nothing visible, no background at all. "
    "STRAIGHT-ON, perfectly centered, perfectly symmetric framing, eye level, "
    "static camera, the table is dead center in the frame, the camera is "
    "perfectly LEVEL (NOT tilted, NOT a side angle, NOT a Dutch angle, NOT "
    "canted). Wide static framing, 35mm lens."
)

BASE_NEG = (
    "color, colored, any color, warm tones, blue tones, multiple light "
    "sources, fill light, bright room, visible walls, back wall, side walls, "
    "background walls, ceiling, floor, ground, surface, horizon line, room, "
    "pillars, columns, concrete, other people, extra characters, duplicates, "
    "text, watermark, logo, cartoon, 3d render, blurry, low quality, "
    "extra chair, two chairs, multiple chairs, a second chair, chair on the "
    "left, chair on the right, off-center, asymmetric, tilted camera, tilted "
    "frame, tilted horizon, side angle, side shot, dutch angle, canted "
    "horizon, skewed perspective, diagonal view, diagonal angle, extreme "
    "close-up, face filling the frame"
)

data = json.loads(SRC.read_text(encoding="utf-8"))

for n in data["nodes"]:
    nid = n["id"]
    if nid == 72:
        n["widgets_values"] = [BW_REF, "image"]
    elif nid == 79:
        # empty base: no character identity to preserve -> ref_boost 0
        n["widgets_values"] = [0, 0, "fit"]
    elif nid == 84:
        n["widgets_values"] = [BASE_POS, 768, ""]
    elif nid == 85:
        n["widgets_values"] = [BASE_NEG, 768, ""]
    elif nid == 29:
        n["widgets_values"] = ["jaisal_cut/kf0_base_v4"]
    elif nid == 114:
        n["mode"] = 4  # bypass the rgthree Image Comparer

out = WF_DIR / "krea2_intro_kf0_base_v4.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"[write] {out.name}  -> jaisal_cut/kf0_base_v4")
print("[done] validate + run krea2_intro_kf0_base_v4.json, then the user reviews the base")
