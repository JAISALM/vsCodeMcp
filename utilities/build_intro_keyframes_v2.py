# -*- coding: utf-8 -*-
"""
Build the Jaisal Kut INTRO B&W keyframe workflows — v2 (user feedback 2026-09-11).

Changes from v1 (per user):
  1. NO VISIBLE WALLS — the background is a dark void; the empty room fades into
     pure darkness (no walls, no ceiling). This keeps the space behind the
     character clear so the 180-degree head-twist (shot 3) has no blocker.
  2. Shot 7 — real SOCCER ball (not American football) under the cricket bat.
  3. Shot 7 — small but FULL cricket stumps (three stumps + bails), each shaped
     like a stake (rounded one end, sharp point the other, so it can be stuck
     into the ground).
  4. Shot 7 — the smiley face is drawn ON the paper page that has WRITING on it
     (not on plain paper).
  5. NO-TABLE variants of shots 1 & 2 (for comparison — the table is a nice
     touch but the user wants to see it without the table).

Each is a clean copy of krea2_identity_edit.json (native UI format, openable +
re-runnable in the ComfyUI UI). Per shot we change: node 84 (instruction),
node 29 (save prefix), bypass node 114 (rgthree comparer). Node 72 = grayscale
character ref (D025 forces the B&W look).

Outputs:
  krea2_intro_shot1_v2.json ... krea2_intro_shot7_v2.json
  krea2_intro_shot1_notable.json, krea2_intro_shot2_notable.json

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_intro_keyframes_v2.py"
"""
import json
from pathlib import Path

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WF_DIR / "krea2_identity_edit.json"

BW_REF = "intro_char_ref_bw.png"  # staged grayscale character ref (node 72)

NEG = (
    "color, colored, any color, warm tones, blue tones, multiple light sources, "
    "fill light, bright room, cluttered room, other people, extra characters, "
    "duplicates, text, watermark, logo, cartoon, 3d render, blurry, low quality, "
    "deformed face, wrong face, different person, extra head, visible walls, "
    "ceiling, background walls, american football, oval ball"
)

# --- shared building blocks --------------------------------------------------
BW = ("Black and white cinematic photograph, strictly monochrome, high contrast, "
      "fine film grain, no color at all. ")
VOID = ("The background is a dark void - NO visible walls, NO ceiling, the empty "
        "room fades into pure darkness, the space behind the character is clear "
        "and unobstructed. ")
BULB = ("A single bare bulb hangs from above on a thin cord, the ONLY light "
        "source, casting one hard shadow, deep black shadows, no fill light. ")
CHAR = ("The same man (preserve his exact face and identity, dark wavy hair, "
        "dark shirt) ")
TABLE = "A simple wooden table. "

# --- the 7 main shots (no walls) --------------------------------------------
SHOTS = {
    1: BW + VOID + BULB + TABLE + CHAR +
       "sits at the wooden table, seated, calm and still, facing slightly toward "
       "the camera. Wide static framing, 35mm lens, eye level, deep focus. Only "
       "the man, the table, and the swinging bulb.",
    2: BW + VOID + BULB + TABLE + CHAR +
       "sits at the wooden table, medium shot, 50mm lens, slightly low angle "
       "looking up at him, he looks calm and composed, one hand resting on the "
       "table, looking slightly off-camera toward an unseen interviewer. Medium "
       "framing, deep focus.",
    3: BW +
       "The background is a pure dark void - NO visible walls, NO obstructions, "
       "the space behind the character is empty darkness so the head can rotate "
       "freely. A single bare bulb hangs directly above his head, the ONLY light "
       "source. Extreme close-up of " + CHAR +
       "face, 85mm lens, eye level, his face fills most of the frame, his eyes "
       "shift subtly, a calm thoughtful expression, his body stays still, only "
       "his eyes and head move slightly. Tight close-up framing, shallow depth "
       "of field, the bulb glowing above.",
    4: BW + VOID + BULB + TABLE + CHAR +
       "sits at the wooden table, medium shot from the opposite side (reverse "
       "angle), 50mm lens, he looks ordinary and relaxed, sitting normally, "
       "facing the camera, a calm neutral expression. Medium framing, eye level, "
       "deep focus.",
    5: BW + VOID + BULB + TABLE + CHAR +
       "sits at the wooden table, medium shot, 50mm lens, small plants are "
       "growing on the surface of the wooden table - thin stems pushing through "
       "the wood, small leaves, one rose slowly opening, a few small plants "
       "populating the table, the man looks down at the growing plants with "
       "quiet curiosity. Medium framing, deep focus.",
    6: BW + VOID + BULB + TABLE + CHAR +
       "close-up, 85mm lens, the man's face and the plants on the table, one "
       "leaf is falling, the plants are bending and wilting, the rose is "
       "closing, the room is emptying out, a slow melancholic mood, the man "
       "looks at the dying plants. Close-up framing, shallow depth of field.",
    7: BW + VOID + BULB + TABLE + CHAR +
       "sits at the wooden table as if nothing is unusual, medium-wide shot, "
       "35mm lens. On the table sits a strange assembled figure made of "
       "everyday objects: a cricket bat standing vertically as the body, two "
       "small FULL cricket stumps as the hands - each hand is a set of three "
       "thin wooden stumps with bails on top, each stump shaped like a stake, "
       "rounded on one end and tapered to a sharp point on the other end (so it "
       "can be stuck into the ground), the figure balancing on a real SOCCER "
       "ball (a round black-and-white football, NOT an American football, NOT "
       "an oval ball), the head is a page of paper that has WRITING on it (lines "
       "of text) with a simple smiley face drawn ON that same written page, a "
       "small microphone in front of the figure, a page of paper floating in the "
       "air, another microphone nearby, the objects assembled in the dark space, "
       "the man sits calmly. Medium-wide framing, deep focus.",
}

# --- no-table variants (shots 1 & 2, for comparison) -------------------------
NOTABLE = {
    1: BW + VOID + BULB + "NO table. " + CHAR +
       "sits on a simple wooden chair, seated, calm and still, facing slightly "
       "toward the camera. Wide static framing, 35mm lens, eye level, deep "
       "focus. Only the man, the chair, and the swinging bulb.",
    2: BW + VOID + BULB + "NO table. " + CHAR +
       "sits on a simple wooden chair, medium shot, 50mm lens, slightly low "
       "angle looking up at him, he looks calm and composed, looking slightly "
       "off-camera toward an unseen interviewer. Medium framing, deep focus.",
}

data = json.loads(SRC.read_text(encoding="utf-8"))

def build(instr, save_prefix, out_name):
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
            n["widgets_values"] = [save_prefix]
        elif nid == 114:
            n["mode"] = 4  # bypass the rgthree Image Comparer
    out = WF_DIR / out_name
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[write] {out.name}  -> {save_prefix}")

for shot, instr in SHOTS.items():
    build(instr, f"jaisal_cut/intro_shot{shot}_v2", f"krea2_intro_shot{shot}_v2.json")

for shot, instr in NOTABLE.items():
    build(instr, f"jaisal_cut/intro_shot{shot}_notable", f"krea2_intro_shot{shot}_notable.json")

print("[done] validate + run the _v2 and _notable workflows")
