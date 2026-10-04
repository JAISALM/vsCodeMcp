# -*- coding: utf-8 -*-
import json
import os
WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
for name in ("jaisal_intro_C1_headturn_90.json", "jaisal_intro_C2_headturn_180.json"):
    d = json.load(open(os.path.join(WFDIR, name), encoding="utf-8"))
    r2v = [n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo"][0]
    print("=== %s ===" % name)
    print("  length:", r2v["widgets_values"][3])
    for n in d["nodes"]:
        if n["type"] == "LoadImage":
            print("  ref:", n["widgets_values"][0])
    p = [n for n in d["nodes"] if n["type"] == "PrimitiveStringMultiline"][0]["widgets_values"][0]
    print("  has Malayalam dialogue:", "\u0d10\u0d28\u0d4d\u0d24\u0d3e" in p)
    print()
