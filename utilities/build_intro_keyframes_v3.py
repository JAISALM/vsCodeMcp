# -*- coding: utf-8 -*-
"""
Build the Jaisal Kut INTRO B&W keyframe workflows — v3 (user feedback 2026-09-11).

User feedback addressed:
  1. WALLS STILL VISIBLE -> the real fix is LIGHT-POOL DARKNESS: the bulb's light
     is a small pool; everything OUTSIDE that pool is pure black (no walls visible
     in the darkness). Baked into every prompt.
  2. NO extreme close-ups (shot 6 had face too big / plants too small / wrong
     lensing) -> all shots are MEDIUM, straight, centered, symmetric, static.
  3. Shot 3 (complete close-up) DROPPED -> replaced with a BACKSIDE view (back of
     chair + table + head twisted 180deg).
  4. TABLE kept, but CONSISTENT size/color/position (shared description block).
  5. CHARACTER: black full-sleeve shirt, UNBUTTONED HALFWAY (open collar).
  6. PLANTS/FLOWERS: consistent design across shots 5 & 6 (same stems + rose;
     only the STATE changes: alive vs dying).
  7. CAMERA: straight, centered, symmetric, eye-level, static (hard rule for
     emotional shots).
  8. EMOTION: each shot shows Jaisal's emotional state.

The 7 unique keyframes (motion anchors for MiniMax H3):
  kf1  empty room (table + chair, no person)          [shot 1 start]
  kf2  Jaisal seated, front, centered                 [shot 2 / 4 / 5-start / 7-start]
  kf3a backside, head NORMAL (twist start)            [shot 3 start]
  kf3b backside, head TWISTED 180deg (twist end)     [shot 3 end]
  kf5  plants GROWN + curiosity/dream emotion         [shot 5 end]
  kf6  plants DEAD + melancholy/limitation emotion    [shot 6 end]
  kf7  cricket ASSEMBLED + determination emotion      [shot 7 end]

Motion pairs for MiniMax (first -> last):
  shot 1 walk-in : kf1 -> kf2
  shot 3 twist   : kf3a -> kf3b
  shot 5 growth  : kf2 -> kf5
  shot 6 dying   : kf5 -> kf6
  shot 7 assembly: kf2 -> kf7
  shot 4 reverse : kf2 (reversed in post)

Each is a clean copy of krea2_identity_edit.json (native UI format, openable +
re-runnable in the ComfyUI UI). Per shot we change: node 84 (instruction),
node 29 (save prefix), bypass node 114 (rgthree comparer). Node 72 = grayscale
character ref (D025 forces the B&W look).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_intro_keyframes_v3.py"
"""
import json
from pathlib import Path

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WF_DIR / "krea2_identity_edit.json"

BW_REF = "intro_char_ref_bw.png"  # staged grayscale character ref (node 72)

# --- consistency lock (shared across ALL shots) -----------------------------
BW = ("Black and white cinematic photograph, strictly monochrome, high contrast, "
      "fine film grain, no color at all. ")
LIGHTING = ("A single bare bulb hangs from above on a thin cord, the ONLY light "
            "source. The bulb's light forms a small pool; everything OUTSIDE that "
            "light pool is pure black darkness - NO visible walls, NO ceiling, the "
            "room fades into complete blackness. ")
TABLE = ("A simple wooden table and a simple wooden chair (consistent size, color, "
         "and position). ")
CHAR = ("The same young man (preserve his exact face and identity): dark wavy hair, "
        "dark complexion, wearing a black full-sleeve shirt that is unbuttoned "
        "halfway (open collar, the top buttons undone). ")
CAM = ("Straight-on, centered, symmetric framing, eye level, static camera, the "
       "subject is centered in the frame. ")

NEG = (
    "color, colored, any color, warm tones, blue tones, multiple light sources, "
    "fill light, bright room, visible walls, ceiling, background walls, other "
    "people, extra characters, duplicates, text, watermark, logo, cartoon, 3d "
    "render, blurry, low quality, deformed face, wrong face, different person, "
    "extra head, american football, oval ball, asymmetric, off-center, tilted "
    "camera, extreme close-up, face filling the frame"
)

# --- the 7 unique keyframes -------------------------------------------------
KFS = {
    "kf1_empty":
        BW + LIGHTING + TABLE +
        "The room is empty - no person, just the table, the chair, and the "
        "swinging bulb. " + CAM + "Wide static framing, 35mm lens.",
    "kf2_seated":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, seated, calm and composed, "
        "facing the camera directly, centered in the frame. " + CAM +
        "Medium framing, 50mm lens.",
    "kf3a_headnormal":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair, seen from BEHIND (backside view) - we see the "
        "back of the chair and his back, the table in front of him, his head is "
        "normal (facing the table, away from the camera). " + CAM +
        "Medium framing, 50mm lens, the camera is positioned behind him.",
    "kf3b_headtwisted":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair, seen from BEHIND (backside view) - we see the "
        "back of the chair and his back, the table in front of him, but his head "
        "is TWISTED 180 degrees so his face is turned around to face the camera "
        "over his shoulder, an eerie detached expression. " + CAM +
        "Medium framing, 50mm lens, the camera is positioned behind him.",
    "kf5_plants_grown":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, looking down at the table with "
        "quiet curiosity and wonder, small plants are growing on the surface of "
        "the wooden table - thin green stems pushing through the wood, small "
        "leaves, one rose slowly opening, a few small plants populating the "
        "table. " + CAM + "Medium framing, 50mm lens.",
    "kf6_plants_dead":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table, looking at the plants with a "
        "melancholic, lonely expression, the plants on the table are dying - one "
        "leaf is falling, the stems are bending and wilting, the rose is closing, "
        "the plants are withering. " + CAM + "Medium framing, 50mm lens.",
    "kf7_cricket":
        BW + LIGHTING + TABLE + CHAR +
        "sits in the wooden chair at the table as if nothing is unusual, a calm "
        "determined expression. On the table sits a strange assembled figure made "
        "of everyday objects: a cricket bat standing vertically as the body, two "
        "small FULL cricket stumps as the hands (each a set of three thin wooden "
        "stumps with bails, each stump shaped like a stake - rounded on one end, "
        "tapered to a sharp point on the other), the figure balancing on a real "
        "SOCCER ball (a round black-and-white football, NOT an American "
        "football, NOT an oval ball), the head is a page of paper that has "
        "WRITING on it (lines of text) with a simple smiley face drawn ON that "
        "same written page, a small microphone in front of the figure, a page of "
        "paper floating in the air, another microphone nearby. " + CAM +
        "Medium-wide framing, 35mm lens.",
}

data = json.loads(SRC.read_text(encoding="utf-8"))

for name, instr in KFS.items():
    d = json.loads(json.dumps(data))  # deep copy
    for n in d["nodes"]:
        nid = n["id"]
        if nid == 72:
            n["widgets_values"] = [BW_REF, "image"]
        elif nid == 84:
            n["widgets_values"] = [instr, 768, ""]
        elif nid == 85:
            n["widgets_values"] = [NEG, 768, ""]
        elif nid == 29:
            n["widgets_values"] = [f"jaisal_cut/{name}"]
        elif nid == 114:
            n["mode"] = 4  # bypass the rgthree Image Comparer
    out = WF_DIR / f"krea2_intro_{name}.json"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[write] {out.name}  -> jaisal_cut/{name}")

print("[done] validate + run the krea2_intro_kf*.json workflows")
