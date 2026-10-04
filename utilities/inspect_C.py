# -*- coding: utf-8 -*-
import json
d = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json", encoding="utf-8"))
print("=== Shot C node types ===")
for n in d["nodes"]:
    t = n["type"]
    if t in ("H3LocalCameraEditor", "PrimitiveStringMultiline", "MiniMaxH3ReferenceToVideo", "LoadImage", "SaveVideo", "ComfyMathExpression", "PrimitiveFloat"):
        print("  node", n["id"], t, "widgets=", n.get("widgets_values"))
print()
print("=== R2V ref slots (if present) ===")
for n in d["nodes"]:
    if n["type"] == "MiniMaxH3ReferenceToVideo":
        for i in n["inputs"]:
            if i["name"].startswith("ref_images."):
                print("  ", i["name"], "link=", i.get("link"))
print()
print("=== subgraph? ===")
print("has definitions.subgraphs:", "definitions" in d and "subgraphs" in d.get("definitions", {}))
