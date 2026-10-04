# -*- coding: utf-8 -*-
import json
d = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin_v2.json", encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}
r2v = next(n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo")
print("=== R2V ref slots ===")
for i in r2v["inputs"]:
    if i["name"].startswith("ref_images.ref_image_"):
        print("  ", i["name"], "link=", i.get("link"))
print()
print("=== LoadImage nodes ===")
for n in d["nodes"]:
    if n["type"] == "LoadImage":
        print("  node", n["id"], n["widgets_values"][0])
print()
print("=== prompt (subject_definitions + retention) ===")
for n in d["nodes"]:
    if n["type"] == "PrimitiveStringMultiline":
        p = n["widgets_values"][0]
        # print up to detailed_description
        end = p.find("detailed_description:")
        print(p[:end] if end != -1 else p[:900])
