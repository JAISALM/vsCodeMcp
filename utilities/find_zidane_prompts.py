#!/usr/bin/env python
import json, os, glob
from PIL import Image

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
print("== workflows containing 'zidane' (case-insensitive) ==")
for P in sorted(glob.glob(os.path.join(WF, "*.json"))):
    try:
        txt = open(P, encoding="utf-8").read()
    except Exception:
        continue
    low = txt.lower()
    if "zidane" in low:
        # find which nodes
        j = json.loads(txt)
        hits = []
        for n in j.get("nodes", []):
            wv = n.get("widgets_values")
            if wv and any(isinstance(w, str) and "zidane" in w.lower() for w in wv):
                hits.append((n["id"], n["type"]))
        # subgraphs too
        sg_hits = []
        for sg in j.get("definitions", {}).get("subgraphs", []):
            for n in sg.get("nodes", []):
                wv = n.get("widgets_values")
                if wv and any(isinstance(w, str) and "zidane" in w.lower() for w in wv):
                    sg_hits.append((n["id"], n["type"]))
        print(f"{os.path.basename(P):<55} main:{hits} subgraphs:{sg_hits}")

# downscale the big portrait
src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\refset_v7\zidane_portrait_HD_00001_.png"
im = Image.open(src)
print("\n== source", im.size)
im2 = im.copy()
im2.thumbnail((700, 1400))
out = r"D:\models\vsCodeMcp\data\zidane_portrait_HD_view.png"
im2.save(out)
print("saved view", out, im2.size)
