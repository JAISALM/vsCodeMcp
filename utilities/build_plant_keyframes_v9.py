# -*- coding: utf-8 -*-
"""
Build the Jaisal Kut INTRO plant keyframes — v9 (2026-09-13).

USER DIRECTION (2026-09-13): the BASE image from now on is `kf2_hands_table.png`
(character, hands on table, facing camera) — the consistency anchor. The plant
keyframes are identity-edits of this base so the character/pose/table stay locked.

TWO PLANT KEYFRAMES:
  kf5_plants_alive  — base = kf2_hands_table, plants FLOURISHING on the table.
  kf6_plants_dead   — base = kf2_hands_table + SECONDARY ref = kf5_plants_alive,
                      the SAME plants now DEAD/withered (2-ref to lock plant
                      positions and minimize drift).

2-REFERENCE WIRING (krea2_identity_edit.json):
  node 72  = LoadImage PRIMARY ref  (character base, always enabled)
  node 113 = LoadImage SECONDARY ref (plants-alive for kf6; BYPASSED for kf5)
  node 92  = VAEEncode for the secondary ref (enabled for kf6; BYPASSED for kf5)
  node 79  = Krea2EditModelPatch [ref_boost_primary, ref_boost_secondary, fit_mode]
  node 84  = positive instruction
  node 85  = negative instruction
  node 29  = SaveImage prefix
  node 114 = rgthree Image Comparer (BYPASSED)

RUN ORDER (one-by-one):
  1. kf5_plants_alive  -> review -> stage as input\\kf5_plants_alive.png
  2. kf6_plants_dead   (needs kf5_plants_alive.png staged as the secondary ref)

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_plant_keyframes_v9.py"
"""
import json
from pathlib import Path

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC = WF_DIR / "krea2_identity_edit.json"

BASE_REF = "kf2_hands_table.png"      # primary ref (node 72) — the consistency anchor
PLANTS_ALIVE_REF = "kf5_plants_alive.png"  # secondary ref (node 113) for kf6

# --- consistency lock (shared across ALL shots) -----------------------------
BW = ("Black and white cinematic photograph, strictly monochrome, high contrast, "
      "clean smooth image, NO grain, NO noise, NO speckles, NO texture, no color "
      "at all. ")
LIGHTING = ("A single bare bulb hangs from above on a thin cord, the ONLY light "
            "source. The background is SMOOTH and fades into COMPLETE BLACK "
            "DARKNESS - no visible wall, no wall texture, no grain, no speckles, "
            "just clean smooth blackness around the lit area. The bulb's light "
            "forms a small pool on the man and the table. ")
TABLE = ("A simple wooden table and ONE simple wooden chair (consistent size, "
         "color, and position). ONLY ONE chair in the frame, centered. ")
CHAR = ("The same young man (preserve his exact face and identity): dark wavy "
        "hair, dark complexion, wearing a black full-sleeve shirt that is "
        "unbuttoned halfway (open collar, the top buttons undone). ")
HANDS = ("both hands resting naturally ON the table surface, visible above the "
         "table edge, relaxed natural hand position, hands NOT under the table. ")
CAM = ("Straight-on, centered, symmetric framing, eye level, static camera, the "
       "subject is centered in the frame. ")

NEG = (
    "color, colored, any color, warm tones, blue tones, multiple light sources, "
    "fill light, bright room, bright wall, white wall, cream wall, light "
    "background, washed out, overexposed background, other people, extra "
    "characters, duplicates, extra chairs, multiple chairs, second chair, "
    "another chair, empty chair, spare chair, chair in the background, hands "
    "under the table, hidden hands, arms under the table, missing hands, "
    "distorted eyes, wrong eyes, deformed eyes, shifted facial features, text, "
    "watermark, logo, cartoon, 3d render, blurry, low quality, deformed face, "
    "wrong face, different person, extra head, american football, oval ball, "
    "asymmetric, off-center, tilted camera, extreme close-up, face filling the "
    "frame, noise speckles, excessive grain, film grain, noisy background, "
    "textured background, wall texture, visible wall, jpeg artifacts, compression "
    "artifacts, speckled background"
)

# --- the 2 plant keyframes --------------------------------------------------
KFS = {
    # Shot 5 end — plants FLOURISHING (alive)
    "kf5_plants_alive": {
        "secondary": None,  # no secondary ref (node 113 bypassed)
        "boost": [4, 1, "fit"],
        "instr": (
            "The man has a NEUTRAL, calm expression (the facial emotion is "
            "handled later in the video, keep the face natural and relaxed). "
            "Small plants are flourishing on the surface of the wooden table - "
            "thin stems WITH SMALL LEAVES pushing through the wood, leafy plants "
            "with several small leaves on each stem, one rose slowly opening, a "
            "few small leafy plants populating the table, alive and growing, lush "
            "and full, the plants have visible LEAVES not just flowers. " + CAM +
            "Medium framing, 50mm lens."
        ),
    },
    # Shot 6 end — the SAME plants now DEAD / DULL (2-ref: base + plants-alive)
    "kf6_plants_dead": {
        "secondary": PLANTS_ALIVE_REF,  # node 113 = the plants-alive image
        "boost": [4, 2, "fit"],
        "instr": (
            "The man has a NEUTRAL, calm expression (the facial emotion is "
            "handled later in the video, keep the face natural and relaxed). "
            "The SAME plants on the table are now DEAD and withered - the rose "
            "is fully closed and drooping, the stems are bent and drooping, the "
            "leaves are curled and falling, the plants look lifeless, dry, and "
            "dull. " + CAM + "Medium framing, 50mm lens."
        ),
    },
}

data = json.loads(SRC.read_text(encoding="utf-8"))

# Use the bf16 krea2 model (already installed) for higher native detail.
# The FP8 turbo (krea2_turbo_fp8_scaled) was the quality ceiling.
UNET_BF16 = "krea2_turbo_bf16.safetensors"

for name, cfg in KFS.items():
    d = json.loads(json.dumps(data))  # deep copy
    for n in d["nodes"]:
        nid = n["id"]
        if nid == 55:
            n["widgets_values"] = [UNET_BF16, "default"]
        elif nid == 72:
            n["widgets_values"] = [BASE_REF, "image"]
            n["mode"] = 0
        elif nid == 113:
            if cfg["secondary"]:
                n["widgets_values"] = [cfg["secondary"], "image"]
                n["mode"] = 0  # enable the secondary ref
            else:
                n["mode"] = 4  # bypass the secondary ref
        elif nid == 92:
            n["mode"] = 0 if cfg["secondary"] else 4  # VAEEncode for secondary
        elif nid == 79:
            n["widgets_values"] = cfg["boost"]
        elif nid == 84:
            n["widgets_values"] = [cfg["instr"], 768, ""]
        elif nid == 85:
            n["widgets_values"] = [NEG, 768, ""]
        elif nid == 29:
            n["widgets_values"] = [f"jaisal_cut/{name}_v9"]
        elif nid == 114:
            n["mode"] = 4  # bypass the rgthree Image Comparer
    out = WF_DIR / f"krea2_intro_{name}_v9.json"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    sec = cfg["secondary"] or "BYPASSED"
    print(f"[write] {out.name}  -> jaisal_cut/{name}_v9   (primary={BASE_REF}, secondary={sec}, boost={cfg['boost']})")

print("\n[done] 2 plant workflows written. RUN ORDER (one-by-one):")
print("  1. krea2_intro_kf5_plants_alive_v9.json  (primary=kf2_hands_table, secondary=BYPASSED)")
print("     -> review -> stage the good output as input\\kf5_plants_alive.png")
print("  2. krea2_intro_kf6_plants_dead_v9.json   (primary=kf2_hands_table, secondary=kf5_plants_alive)")
print("     -> needs kf5_plants_alive.png staged first (the secondary ref)")
