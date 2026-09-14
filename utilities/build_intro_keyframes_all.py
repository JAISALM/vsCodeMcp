# -*- coding: utf-8 -*-
"""
Build the 7 Jaisal Kut INTRO B&W keyframe workflows (one per shot).

Each is a clean copy of krea2_identity_edit.json (native UI format, so it stays
openable + re-runnable in the ComfyUI UI later - NOT a one-off script run).
Per shot we only change: the positive instruction (node 84), the save prefix
(node 29), and bypass the rgthree Image Comparer (node 114). The grayscale
character reference (node 72) + B&W demand force the monochrome look (D025).

Outputs: krea2_intro_shot1.json ... krea2_intro_shot7.json
Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_intro_keyframes_all.py"
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
    "deformed face, wrong face, different person, extra head"
)

ROOM = (
    "Black and white cinematic photograph, strictly monochrome, high contrast, "
    "fine film grain, no color at all. A dark empty room at night. A single bare "
    "bulb hangs from the ceiling on a thin cord, the ONLY light source, casting "
    "one hard shadow, deep black shadows, no fill light. A simple wooden table. "
)
CHAR = (
    "The same man (preserve his exact face and identity, dark wavy hair, dark "
    "shirt) "
)

SHOTS = {
    1: ROOM + CHAR + "sits at the wooden table, seated, calm and still, facing "
        "slightly toward the camera. Wide static framing, 35mm lens, eye level, "
        "deep focus. The room is sparse and empty - only the man, the table, and "
        "the swinging bulb.",
    2: ROOM + CHAR + "sits at the wooden table, medium shot, 50mm lens, slightly "
        "low angle looking up at him, he looks calm and composed, one hand "
        "resting on the table, looking slightly off-camera toward an unseen "
        "interviewer. Medium framing, deep focus.",
    3: ROOM + CHAR + "extreme close-up of his face, 85mm lens, eye level, his "
        "face fills most of the frame, the bare bulb hangs directly above his "
        "head, his eyes shift subtly, a calm thoughtful expression, his body "
        "stays still, only his eyes and head move slightly. Tight close-up "
        "framing, shallow depth of field, the bulb glowing above.",
    4: ROOM + CHAR + "sits at the wooden table, medium shot from the opposite "
        "side (reverse angle), 50mm lens, he looks ordinary and relaxed, sitting "
        "normally, facing the camera, a calm neutral expression. Medium framing, "
        "eye level, deep focus.",
    5: ROOM + CHAR + "sits at the wooden table, medium shot, 50mm lens, small "
        "plants are growing on the surface of the wooden table - thin stems "
        "pushing through the wood, small leaves, one rose slowly opening, a few "
        "small plants populating the table, the man looks down at the growing "
        "plants with quiet curiosity. Medium framing, deep focus.",
    6: ROOM + CHAR + "close-up, 85mm lens, the man's face and the plants on the "
        "table, one leaf is falling, the plants are bending and wilting, the "
        "rose is closing, the room is emptying out, a slow melancholic mood, the "
        "man looks at the dying plants. Close-up framing, shallow depth of "
        "field.",
    7: ROOM + CHAR + "sits at the wooden table as if nothing is unusual, "
        "medium-wide shot, 35mm lens, on the table sits a strange assembled "
        "figure made of everyday objects - a cricket bat standing vertically as "
        "the body, two small stumps as the hands, the figure balancing on a "
        "football, a piece of paper with a smiley face as the head, a small "
        "microphone in front of it, a page of paper floating in the air, another "
        "microphone nearby, the objects assembled in the dark space, the man "
        "sits calmly. Medium-wide framing, deep focus.",
}

data = json.loads(SRC.read_text(encoding="utf-8"))

for shot, instr in SHOTS.items():
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
            n["widgets_values"] = [f"jaisal_cut/intro_shot{shot}"]
        elif nid == 114:
            n["mode"] = 4  # bypass the rgthree Image Comparer (crashes on stale temp)
    out = WF_DIR / f"krea2_intro_shot{shot}.json"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[write] {out.name}  (shot {shot})")

print("[done] validate + run krea2_intro_shot1..7.json")
