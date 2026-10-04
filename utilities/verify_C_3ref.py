# -*- coding: utf-8 -*-
import json
import os
WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
d = json.load(open(os.path.join(WFDIR, "jaisal_intro_C_headturn_3ref.json"), encoding="utf-8"))
r2v = [n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo"][0]
print("R2V length:", r2v["widgets_values"][3])
print("ref slots:")
for i in r2v["inputs"]:
    if i["name"].startswith("ref_images."):
        print("  ", i["name"], "link=", i.get("link"))
print("LoadImage nodes:")
for n in d["nodes"]:
    if n["type"] == "LoadImage":
        print("  node", n["id"], n["widgets_values"][0])
p = [n for n in d["nodes"] if n["type"] == "PrimitiveStringMultiline"][0]["widgets_values"][0]
print()
print("prompt checks:")
print("  3 refs (Picture 1/2/3):", all(t in p for t in ("<Picture 1>", "<Picture 2>", "<Picture 3>")))
print("  turn to the LEFT:", "to the LEFT" in p)
print("  NOT to the right:", "NOT to the right" in p)
print("  locked camera:", "LOCKED CLOSE UP" in p)
print("  dialogue at 5s mark:", "about the 5 second mark" in p)
print("  Malayalam dialogue:", "\u0d10\u0d28\u0d4d\u0d24\u0d3e" in p)
print("  negative: head turning right:", "head turning to the right" in p)
