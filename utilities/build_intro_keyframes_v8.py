# -*- coding: utf-8 -*-
"""
Build the Jaisal Kut INTRO B&W keyframe workflows — v8 (2026-09-13).

Completes the 6 remaining keyframes from the 11-image reference plan
(docs/INTRO_KEYFRAME_PLAN.md):

  kf5a_stem        Shot 5 start  — ONE tiny stem on the table
  kf5_plants_grown Shot 5 end    — plants GROWN (flourish: rose + stems)
  kf6_plants_dead  Shot 6 end    — SAME plants as kf5, now DEAD / DULL
  kf7a_page        Shot 7 stage1 — a PAGE floats in
  kf7b_page_mic    Shot 7 stage2 — page + ONE mic drops in
  kf7c_cricket     Shot 7 stage3 — cricket assembly (bat + stumps + ball + page-head + mic)

USER DIRECTION (2026-09-13): "the one which is there with florish should be the
one which should go dull when he says the dialogue." So kf5 = plants with
flourish (alive), kf6 = the SAME plants but DULL / dead. kf5 and kf6 must be the
SAME composition (same plants, same positions, same pose, same ONE chair) — only
the plant STATE changes (alive -> dead).

DECISION (2026-09-12): ACCEPT A WALL — a DARK CHARCOAL wall (deep gray,
near-black at the edges), NOT a forced pure-black void (which kept coming out
cream/white).

CHARACTER CONSISTENCY (D058): node 72 = the grayscale character ref
(intro_char_ref_bw.png), NO scene anchor. This is the proven V7 setting that
gives the correct face. A scene anchor breaks the face — do NOT add one.

REFERENCE-IMAGE STRATEGY (one-by-one):
  All 6 are built with node 72 = character ref so they are IMMEDIATELY RUNNABLE.
  For the plant/prop sequences, the LATER keyframe should be re-anchored to the
  PREVIOUS good output for perfect consistency:
    kf5  -> anchor to kf5a   (after kf5a is confirmed)
    kf6  -> anchor to kf5    (after kf5 is confirmed)  [CRITICAL: same plants]
    kf7b -> anchor to kf7a   (after kf7a is confirmed)
    kf7c -> anchor to kf7b   (after kf7b is confirmed)
  To re-anchor: set node 72's widgets_values[0] to the previous output filename
  (staged in input\\) and re-run. See the printout at the bottom.

Each is a clean copy of krea2_identity_edit.json (native UI format, openable +
re-runnable in the ComfyUI UI). Per shot we change: node 84 (instruction),
node 85 (negative), node 29 (save prefix), node 72 (reference image), bypass
node 114 (rgthree comparer).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_intro_keyframes_v8.py"
"""
import json
from pathlib import Path

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WF_DIR / "krea2_identity_edit.json"

# Reference image for node 72. Default = the grayscale character ref (proven V7
# setting for the correct face). For the LATER keyframes (kf5, kf6, kf7b, kf7c)
# you may re-anchor to the previous good output for perfect consistency — see
# the REANCHOR map below and the printout at the bottom.
CHAR_REF = "intro_char_ref_bw.png"

# --- consistency lock (shared across ALL shots) -----------------------------
BW = ("Black and white cinematic photograph, strictly monochrome, high contrast, "
      "fine film grain, no color at all. ")
# DECISION 2026-09-12: ACCEPT A WALL — dark charcoal (deep gray, near-black at
# the edges), NOT a forced pure-black void (which kept coming out cream/white).
LIGHTING = ("A single bare bulb hangs from above on a thin cord, the ONLY light "
            "source. A dark charcoal wall behind the table (deep gray, near-black "
            "at the edges), the wall falls into shadow away from the bulb's light "
            "pool, only the area under the bulb is lit. Everything outside the "
            "light pool fades into darkness. ")
TABLE = ("A simple wooden table and ONE simple wooden chair (consistent size, "
         "color, and position). ONLY ONE chair in the frame, centered. ")
CHAR = ("The same young man (preserve his exact face and identity): dark wavy "
        "hair, dark complexion, wearing a black full-sleeve shirt that is "
        "unbuttoned halfway (open collar, the top buttons undone). ")
CAM = ("Straight-on, centered, symmetric framing, eye level, static camera, the "
       "subject is centered in the frame. ")

NEG = (
    "color, colored, any color, warm tones, blue tones, multiple light sources, "
    "fill light, bright room, bright wall, white wall, cream wall, light "
    "background, washed out, overexposed background, other people, extra "
    "characters, duplicates, extra chairs, multiple chairs, second chair, "
    "another chair, text, watermark, logo, cartoon, 3d render, blurry, low "
    "quality, deformed face, wrong face, different person, extra head, american "
    "football, oval ball, asymmetric, off-center, tilted camera, extreme "
    "close-up, face filling the frame"
)

# --- the 6 remaining keyframes ---------------------------------------------
KFS = {
    # Shot 5 start — ONE tiny stem (the very first sign of growth)
    "kf5a_stem":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, looking down at the table with "
        "quiet anticipation. On the surface of the wooden table, ONE single tiny "
        "thin stem is just pushing through the wood - the very first sign of "
        "growth, nothing else growing yet, no leaves, no flowers, just one small "
        "thin stem. " + CAM + "Medium framing, 50mm lens.",
    # Shot 5 end — plants GROWN (flourish)
    "kf5_plants_grown":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, looking down at the table with "
        "quiet curiosity and wonder. Small plants are flourishing on the surface "
        "of the wooden table - thin stems pushing through the wood, small leaves, "
        "one rose slowly opening, a few small plants populating the table, alive "
        "and growing, lush and full. " + CAM + "Medium framing, 50mm lens.",
    # Shot 6 end — SAME plants as kf5, now DEAD / DULL
    "kf6_plants_dead":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, looking at the plants with a "
        "melancholic, lonely, downcast expression. The SAME plants on the table "
        "(the same thin stems, the same rose, the same positions as the grown "
        "version) are now DEAD and withered - the stems are bending and drooping, "
        "the rose is closed and dull, one leaf is falling, the plants are dead, "
        "lifeless, and dull. " + CAM + "Medium framing, 50mm lens.",
    # Shot 7 stage 1 — a PAGE floats in
    "kf7a_page":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, looking up with quiet attention. "
        "A single PAGE of paper (with lines of writing on it) is floating in the "
        "dark space above the table, hovering in the air, the only object in the "
        "frame besides the man and the table. " + CAM + "Medium framing, 50mm "
        "lens.",
    # Shot 7 stage 2 — page + ONE mic drops in
    "kf7b_page_mic":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, looking at the objects with calm "
        "attention. A single PAGE of paper (with lines of writing on it) is "
        "floating in the dark space above the table, and ONE small microphone is "
        "placed on the table in front of him. " + CAM + "Medium framing, 50mm "
        "lens.",
    # Shot 7 stage 3 — cricket assembly
    "kf7c_cricket":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table as if nothing is unusual, a calm "
        "determined expression. On the table sits a small assembled figure made "
        "of everyday objects: a cricket bat standing vertically as the body, two "
        "small cricket stumps as the hands, the figure balancing on a real "
        "SOCCER ball (a round black-and-white football, NOT an American "
        "football, NOT an oval ball), the head is a page of paper with a simple "
        "smiley face drawn on it, ONE small microphone in front of the figure. "
        "The figure is SMALL and sits ON the table, not blocking the character. "
        + CAM + "Medium-wide framing, 35mm lens.",
}

# Re-anchor map: for the LATER keyframes, the reference image should be the
# previous good output (staged in input\\) for perfect consistency. Apply this
# AFTER the previous keyframe is confirmed. Default (CHAR_REF) keeps all 6
# immediately runnable.
REANCHOR = {
    # "kf5_plants_grown": "kf5a_stem.png",
    # "kf6_plants_dead":  "kf5_plants_grown.png",
    # "kf7b_page_mic":    "kf7a_page.png",
    # "kf7c_cricket":     "kf7b_page_mic.png",
}

data = json.loads(SRC.read_text(encoding="utf-8"))

for name, instr in KFS.items():
    d = json.loads(json.dumps(data))  # deep copy
    ref = REANCHOR.get(name, CHAR_REF)
    for n in d["nodes"]:
        nid = n["id"]
        if nid == 72:
            n["widgets_values"] = [ref, "image"]
        elif nid == 84:
            n["widgets_values"] = [instr, 768, ""]
        elif nid == 85:
            n["widgets_values"] = [NEG, 768, ""]
        elif nid == 29:
            n["widgets_values"] = [f"jaisal_cut/{name}_v8"]
        elif nid == 114:
            n["mode"] = 4  # bypass the rgthree Image Comparer
    out = WF_DIR / f"krea2_intro_{name}_v8.json"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[write] {out.name}  -> jaisal_cut/{name}_v8   (ref={ref})")

print("\n[done] 6 workflows written. Validate + run one-by-one:")
print("  1. kf5a_stem        (ref=char)  -> confirm -> stage as kf5a_stem.png")
print("  2. kf5_plants_grown (ref=char)  -> confirm -> stage as kf5_plants_grown.png")
print("  3. kf6_plants_dead  (ref=char)  -> confirm; if plants != kf5, re-anchor node 72 to kf5_plants_grown.png + re-run")
print("  4. kf7a_page        (ref=char)  -> confirm -> stage as kf7a_page.png")
print("  5. kf7b_page_mic    (ref=char)  -> confirm; if props != kf7a, re-anchor node 72 to kf7a_page.png + re-run")
print("  6. kf7c_cricket     (ref=char)  -> confirm; if props != kf7b, re-anchor node 72 to kf7b_page_mic.png + re-run")
print("\n[re-anchor] to anchor a later keyframe to the previous output, set node 72")
print("  widgets_values[0] to the previous filename (staged in input\\) and re-run.")
