# -*- coding: utf-8 -*-
"""Diagnose the v4 keyframe workflows: what reference each one actually uses,
the KSampler settings, and the staged anchor files in input/."""
import json
from pathlib import Path

WF_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
INP = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input")

names = ["kf2_seated", "kf3a_headnormal", "kf3b_headtwisted", "kf3c_head90",
         "kf5_plants_grown", "kf5a_stem", "kf6_plants_dead",
         "kf7a_page", "kf7b_page_mic", "kf7c_cricket"]

print("=== PER-WORKFLOW REFERENCES + SAMPLER ===")
for name in names:
    p = WF_DIR / f"krea2_intro_{name}_v4.json"
    if not p.exists():
        print(f"  {name}: FILE MISSING")
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in d["nodes"]}
    n72 = nodes.get(72, {}).get("widgets_values", ["?"])[0]
    n113 = nodes.get(113, {}).get("widgets_values", ["?"])[0]
    n113_mode = nodes.get(113, {}).get("mode")
    n92_mode = nodes.get(92, {}).get("mode")
    n53 = nodes.get(53, {}).get("widgets_values", [])
    # KSampler: [seed, control, steps, cfg, sampler, scheduler, denoise]
    steps = n53[2] if len(n53) > 2 else "?"
    cfg = n53[3] if len(n53) > 3 else "?"
    denoise = n53[6] if len(n53) > 6 else "?"
    n84 = nodes.get(84, {}).get("widgets_values", [])
    grounding = n84[1] if len(n84) > 1 else "?"
    print(f"  {name}:")
    print(f"    char_ref(72)={n72}")
    print(f"    scene_ref(113)={n113}  [113.mode={n113_mode}, 92.mode={n92_mode}]")
    print(f"    KSampler: steps={steps} cfg={cfg} denoise={denoise}  grounding_px={grounding}")

print("\n=== STAGED ANCHOR FILES in input/ ===")
for f in ["intro_scene_master.png", "intro_char_ref_bw.png",
          "kf3a_v4.png", "kf5_v4.png", "kf7a_v4.png", "kf7b_v4.png"]:
    p = INP / f
    if p.exists():
        import os
        print(f"  {f}: {p.stat().st_size} bytes")
    else:
        print(f"  {f}: MISSING")
