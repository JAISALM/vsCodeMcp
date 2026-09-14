# -*- coding: utf-8 -*-
"""
Build the Jaisal Cut INTRO B&W keyframe workflows — v4 (user feedback 2026-09-11).

ROOT CAUSE of the v3 drift (walls / extra chairs / shifting table / changing
plants): every shot was generated INDEPENDENTLY from the character ref only
(node 72). The identity-edit workflow has a SECOND reference slot (node 113,
the "_b" slot) that v3 left pointing at another character image, so the SCENE
(table / chair / bulb / room) was never anchored and re-invented every shot.

THE FIX (v4): use node 113 as a SCENE ANCHOR.
  - node 72 = character ref (intro_char_ref_bw.png)  -> locks the FACE
  - node 113 = scene anchor image                    -> locks the ENVIRONMENT
  - node 79 ref_boost=4 (face), ref_boost_a=3 (scene)

The v4 BASE (kf0_base_v4) was CONFIRMED by the user and staged as
input\\intro_scene_master.png - it is the SCENE ANCHOR for every shot (kf1_empty
= the base itself, no generation needed). This is a 4-pass pipeline (a shot can
only anchor to a previous stage once that stage is generated + staged):
  PASS 2  kf2 / kf3a / kf5 / kf5a / kf7a  -> all anchored to intro_scene_master.png
  PASS 3  kf3b / kf3c (from kf3a) / kf6 (from kf5) / kf7b (from kf7a)
            (stage the best kf3a/kf5/kf7a as input\\kf3a_v4.png / kf5_v4.png /
             kf7a_v4.png first)
  PASS 4  kf7c (from kf7b)  (stage the best kf7b as input\\kf7b_v4.png first)

SCENARIO ANCHORS (added 2026-09-11 to stop MiniMax H3 hallucinating the script):
  kf5a_stem    : "one tiny stem pushes through" - growth-not-fade-in (Shot 5)
  kf7a_page    : Shot 7 stage 1 - PAGE floats in on "കഥകൾ"
  kf7b_page_mic: Shot 7 stage 2 - MIC drops in on "രാഷ്ട്രീയം"
  kf7c_cricket : Shot 7 stage 3 - full cricket assembly on "കായികം"
  kf3c_head90  : mid-anchor for the SLOW 180deg head twist (Shot 3)

Per-shot fixes (user feedback 2026-09-11):
  kf1  chair CENTERED (was off to the right)
  kf2  ONLY ONE chair, NO wall (extra chair left + wall right in v3)
  kf3a keep (good) + no extra chairs / no wall
  kf3b head ALONE rotated 180deg (surreal), NOT a normal over-shoulder look
  kf5  ONLY ONE chair, plants LARGE (extra chairs both sides + plants too small)
  kf6  SAME scene as kf5, only plants DEAD + melancholy (was completely different)
  kf7  props SMALL + ON the table, ONE mic, NOT blocking the character

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_intro_keyframes_v4.py"
"""
import json
from pathlib import Path

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WF_DIR / "krea2_identity_edit.json"

CHAR_REF = "intro_char_ref_face.png"  # node 72 (FACE-ONLY crop, no t-shirt) - staged in input\
REALISM_LORA = "Krea2-realism-V1.safetensors"  # node 201 (natural look) - in E:\ComfyUI_windows_portable\ComfyUI\models\loras\
USE_REALISM_LORA = False  # 2026-09-12: DROPPED - the realism LoRA fills the void sides with white (studio backdrop). Keep identity LoRA only + cinematic B&W prompt.
SCENE_REF = "intro_scene_master.png" # node 113 (environment) = the CONFIRMED v4 base
KF3A_REF = "kf3a_v4.png"            # node 113 for kf3b/kf3c - stage after PASS 2
KF5_REF = "kf5_v4.png"              # node 113 for kf6 - stage after PASS 2
KF7A_REF = "kf7a_v4.png"            # node 113 for kf7b - stage after PASS 3
KF7B_REF = "kf7b_v4.png"            # node 113 for kf7c - stage after PASS 3

# --- consistency lock (shared across ALL shots) -----------------------------
BW = ("Black and white cinematic photograph, strictly monochrome, high contrast, "
      "clean and sharp, no color at all, NO film grain, NO noise, NO speckles, "
      "clean deep blacks, crisp detail. ")
LIGHTING = ("A single bare bulb hangs from above on a thin cord, the ONLY light "
            "source, centered. The bulb's light forms a small pool; everything "
            "OUTSIDE that light pool is pure black darkness - NO visible walls, "
            "NO ceiling, NO pillars, the room fades into complete blackness on "
            "ALL sides. ")
CHAR = ("A single bare bulb hangs from above on a thin cord, the ONLY light "
        "source, centered; its light forms a small pool and everything OUTSIDE "
        "that pool is pure black darkness - NO visible walls, NO ceiling, NO "
        "pillars, NO columns, the room fades into complete blackness on ALL "
        "sides. The same young man (preserve his exact face and identity): dark "
        "wavy hair, dark complexion, wearing a PLAIN CASUAL BLACK SHIRT - a "
        "single black shirt, NO inner t-shirt, NO undershirt, NO white shirt "
        "underneath, NO second shirt, just one plain black shirt. ")
CAM = ("Straight-on, centered, symmetric framing, eye level, static camera, the "
       "subject is centered in the frame. ")
ONE_CHAIR = ("ONLY ONE chair in the frame (the one at the table), NO extra "
             "chairs, NO second chair, NO additional chairs, NO visible walls, "
             "NO pillars, NO columns. ")

NEG = (
    "color, colored, any color, warm tones, blue tones, multiple light sources, "
    "fill light, bright room, visible walls, ceiling, background walls, pillar, "
    "column, concrete wall, textured wall, other people, extra characters, "
    "duplicates, extra chair, multiple chairs, second chair, additional chair, "
    "text, watermark, logo, cartoon, 3d render, blurry, low quality, deformed "
    "face, wrong face, different person, extra head, american football, oval "
    "ball, asymmetric, off-center, tilted camera, extreme close-up, face "
    "filling the frame, props blocking the character, props covering the face, "
    "huge props, oversized objects, inner t-shirt, undershirt, white shirt, "
    "second shirt, two shirts, floor, ground, surface, horizon line, room, "
    "back wall, side walls, ceiling, white bars, white borders, white "
    "background, white edges, pillarbox, letterbox, white frame, white "
    "margins, white sides, studio backdrop, white studio background"
)

# --- the keyframes ----------------------------------------------------------
# Each entry: (save_name, char_ref(node72), scene_ref(node113), ref_boost,
#              ref_boost_a, instruction)
KFS = {
    # PASS 2 - character shots anchored to the CONFIRMED v4 base (scene master)
    "kf2_seated": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair at the table, centered. BOTH of "
        "his hands are placed flat on the table surface in front of him, "
        "resting on the table. He is looking at the chair - his gaze is "
        "directed toward the chair, a calm composed expression. " + ONE_CHAIR +
        " " + CAM + "Medium framing, 50mm lens."
    ),
    "kf3a_headnormal": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair, seen from BEHIND (backside "
        "view) - we see the back of the chair and his back, the table in front "
        "of him, his head is normal (facing the table, away from the camera). "
        + ONE_CHAIR + " " + CAM + "Medium framing, 50mm lens, the camera is "
        "positioned behind him."
    ),
    "kf5_plants_grown": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair at the table, looking down at "
        "the table with quiet curiosity and wonder. On the table, SEVERAL "
        "LARGE plants are growing - tall green stems with big leaves, one "
        "large rose fully open, the plants are PROMINENT and take up a good "
        "portion of the table surface. " + ONE_CHAIR + " " + CAM +
        "Medium framing, 50mm lens."
    ),
    "kf5a_stem": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair at the table, looking down at "
        "the table with quiet curiosity. ONE tiny thin stem is just pushing "
        "through the surface of the wooden table (a single small stem, barely "
        "visible, the very first sign of growth, nothing else). " + ONE_CHAIR +
        " " + CAM + "Medium framing, 50mm lens."
    ),
    "kf7a_page": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair at the table, a calm determined "
        "expression. A single page of paper with writing on it (lines of text) "
        "is floating in the dark space above the table, gently hovering. "
        + ONE_CHAIR + " " + CAM + "Medium framing, 50mm lens."
    ),
    # PASS 3 - stage-based shots anchored to the previous stage
    "kf3b_headtwisted": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair, FRONT view - we see his FACE "
        "directly. His HEAD is TWISTED sharply to his left side, turned almost "
        "fully around over his shoulder (a surreal, impossible neck twist), so "
        "his face is angled back toward the camera. His BODY and SHOULDERS face "
        "the camera normally (this is NOT a back view, NOT a reverse view - we "
        "see his chest and face). The twisted head is the surreal focus, an "
        "eerie detached expression. " + ONE_CHAIR + " " + CAM +
        "Medium framing, 50mm lens."
    ),
    "kf3c_head90": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair, seen from BEHIND (backside "
        "view) - we see the back of the chair and his back, the table in front "
        "of him. His head is rotated 90 degrees to the side (a profile view, "
        "the nose points sideways, halfway through the twist), the body and "
        "shoulders stay facing away. " + ONE_CHAIR + " " + CAM +
        "Medium framing, 50mm lens, the camera is positioned behind him."
    ),
    "kf6_plants_dead": (
        CHAR_REF, KF5_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair at the table, looking at the "
        "table with a MELANCHOLIC, LONELY expression - a sad, downcast look. "
        "The SAME plants as the reference image, now DYING and WITHERED - the "
        "same stems and leaves, now bent and wilting, the leaves drooping and "
        "withered and brown, the rose closed and drooping, one leaf falling. "
        "The plants are dead, not alive. Keep the SAME table, chair, bulb, "
        "character and framing as the reference - ONLY the plants change to "
        "dead. " + ONE_CHAIR + " " + CAM + "Medium framing, 50mm lens."
    ),
    "kf7b_page_mic": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair at the table, a calm determined "
        "expression. A single page of paper with writing on it (lines of text) "
        "is floating in the dark space above the table, and ONE microphone is "
        "sitting on the table in front of the character (ONE microphone, a "
        "clearly visible standard handheld microphone, NOT tiny, sitting on "
        "the table surface). " + ONE_CHAIR + " " + CAM +
        "Medium framing, 50mm lens."
    ),
    # PASS 4 - the full cricket assembly, anchored to kf7b
    "kf7c_cricket": (
        CHAR_REF, SCENE_REF, 4, 3,
        BW + CHAR + "sits in the wooden chair at the table as if nothing is "
        "unusual, a calm determined expression. On the table, SMALL and "
        "COMPACT, sits a strange assembled figure made of everyday objects: a "
        "small cricket bat standing vertically as the body, two small cricket "
        "stumps as the hands, the figure balancing on a small round SOCCER "
        "ball, the head is a small page of paper with writing and a simple "
        "smiley face, ONE small microphone in front of the figure. ALL props "
        "are SMALL and COMPACT, sitting ON the table surface, NOT blocking or "
        "covering the character's face or body - the character is the clear "
        "focus. " + ONE_CHAIR + " " + CAM + "Medium-wide framing, 35mm lens."
    ),
}

data = json.loads(SRC.read_text(encoding="utf-8"))

# --- check the realism LoRA is present (user downloads it to models\loras\) ---
import os
_lora_path = os.path.join(r"E:\ComfyUI_windows_portable\ComfyUI\models\loras", REALISM_LORA)
if not os.path.exists(_lora_path):
    print(f"[WARN] realism LoRA NOT FOUND: {_lora_path}")
    print("       Download it (Civitai, account required) and save it there, then re-run this script.")
    print("       The workflows will FAIL validation until the file exists.")

for name, (char_ref, scene_ref, ref_boost, ref_boost_a, instr) in KFS.items():
    save_name = f"{name}_v5"
    d = json.loads(json.dumps(data))  # deep copy
    for n in d["nodes"]:
        nid = n["id"]
        if nid == 72:
            n["widgets_values"] = [char_ref, "image"]
        elif nid == 113:
            n["widgets_values"] = [scene_ref, "image"]
            n["mode"] = 0  # ENABLE the scene anchor (native ships it bypassed mode=4)
        elif nid == 92:
            n["mode"] = 0  # ENABLE the scene VAEEncode (113 -> 92 -> 79.source_latent_b)
        elif nid == 79:
            n["widgets_values"] = [ref_boost, ref_boost_a, "fit"]
        elif nid == 84:
            n["widgets_values"] = [instr, 768, ""]
        elif nid == 85:
            n["widgets_values"] = [NEG, 768, ""]
        elif nid == 29:
            n["widgets_values"] = [f"jaisal_cut/{save_name}"]
        elif nid == 114:
            n["mode"] = 4  # bypass the rgthree Image Comparer
    # --- Krea2 REALISM LoRA (node 201) - OPTIONAL, currently DROPPED ---
    # When USE_REALISM_LORA=True: chain 55 UNETLoader -> 71 identity LoRA -> 201 realism LoRA -> 79 patch.
    # When False (current): the original chain 71 identity LoRA -> 79 patch is left untouched.
    if USE_REALISM_LORA:
        n71 = next(n for n in d["nodes"] if n["id"] == 71)
        n79 = next(n for n in d["nodes"] if n["id"] == 79)
        for l in d["links"]:
            if l[0] == 41:
                l[3] = 201  # to_node = 201
        d["links"].append([42, 201, 0, 79, 0, "MODEL"])
        for o in n71.get("outputs", []):
            if o.get("links"):
                o["links"] = [41]
        for i in n79["inputs"]:
            if i["name"] == "model":
                i["link"] = 42
        d["nodes"].append({
            "id": 201, "type": "LoraLoaderModelOnly",
            "pos": [60, 520], "size": [480, 120], "flags": {}, "order": 1, "mode": 0,
            "inputs": [
                {"localized_name": "lora_name", "name": "lora_name", "type": "COMBO", "widget": {"name": "lora_name"}, "link": None},
                {"localized_name": "strength", "name": "strength", "type": "FLOAT", "widget": {"name": "strength"}, "link": None},
                {"localized_name": "model", "name": "model", "type": "MODEL", "link": 41}
            ],
            "outputs": [
                {"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [42]}
            ],
            "properties": {"Node name for S&R": "LoraLoaderModelOnly"},
            "widgets_values": [REALISM_LORA, 0.3]
        })
    out = WF_DIR / f"krea2_intro_{name}_v5.json"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[write] {out.name}  -> jaisal_cut/{save_name}  "
          f"(node72={char_ref}, node113={scene_ref}, boost={ref_boost}/{ref_boost_a})")

print("\n[done] 4-pass pipeline (the v4 base is already confirmed = intro_scene_master.png):")
print("  NOTE: kf1_empty = the confirmed v4 base itself (intro_scene_master.png) - no generation needed")
print("  PASS 2: run krea2_intro_kf2_seated_v4 / kf3a_headnormal_v4 / kf5_plants_grown_v4 / kf5a_stem_v4 / kf7a_page_v4")
print("         -> stage the best kf3a/kf5/kf7a into input\\ (kf3a_v4.png, kf5_v4.png, kf7a_v4.png)")
print("  PASS 3: run krea2_intro_kf3b_headtwisted_v4 / kf3c_head90_v4 / kf6_plants_dead_v4 / kf7b_page_mic_v4")
print("         -> stage the best kf7b into input\\ (kf7b_v4.png)")
print("  PASS 4: run krea2_intro_kf7c_cricket_v4")
