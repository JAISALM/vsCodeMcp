# -*- coding: utf-8 -*-
import json
d = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180_r2v.json", encoding="utf-8"))
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
p = [n for n in d["nodes"] if n["type"] == "PrimitiveStringMultiline"][0]["widgets_values"][0]
print()
print("prompt checks:")
print("  head rotates 180:", "rotate SLOWLY, deliberately, 180 degrees" in p)
print("  eyes shift first:", "EYES shift first" in p)
print("  body does NOT react:", "BODY does NOT react" in p)
print("  Malayalam dialogue:", "എന്താ പറയേണ്ടത് അറിയില്ല" in p)
print("  <d>[Malayalam]:", "<d>[Malayalam]" in p)
print("  NO music:", "NO music" in p)
