# -*- coding: utf-8 -*-
import json
d = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_B_setup.json", encoding="utf-8"))
r2v = [n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo"][0]
print("R2V widgets (width,height,length,ref_image_size):", r2v["widgets_values"])
print("ref slots:")
for i in r2v["inputs"]:
    if i["name"].startswith("ref_images."):
        print("  ", i["name"], "link=", i.get("link"))
print("LoadImage nodes:")
for n in d["nodes"]:
    if n["type"] == "LoadImage":
        print("  node", n["id"], n["widgets_values"][0])
print("SaveVideo:")
for n in d["nodes"]:
    if n["type"] == "SaveVideo":
        print("  ", n["widgets_values"])
# confirm the micro-expression is in the prompt
for n in d["nodes"]:
    if n["type"] == "PrimitiveStringMultiline":
        p = n["widgets_values"][0]
        print("prompt has 'settling smile':", "settling smile" in p)
        print("prompt has 'slight, calm nod':", "calm nod" in p)
