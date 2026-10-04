# -*- coding: utf-8 -*-
"""
Build the COMPARISON workflow: a copy of jaisal_intro_A_walkin.json with the
standard CLIPLoader (node 128) swapped for CLIPLoaderGGUF (the Nif00 fork)
loading the pruned Qwen3-VL-32B MiniMax H3 GGUF. Everything else identical, so
the only variable is the text encoder.

Output: jaisal_intro_A_walkin_gguf.json
"""
import json, os

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin_gguf.json"
GGUF = "Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf"

d = json.load(open(SRC, encoding="utf-8"))

# Find the CLIPLoader node and swap it for CLIPLoaderGGUF.
swapped = False
for n in d["nodes"]:
    if n["type"] == "CLIPLoader":
        n["type"] = "CLIPLoaderGGUF"
        # CLIPLoaderGGUF widgets: [clip_name, type] (no device).
        n["widgets_values"] = [GGUF, "minimax"]
        # Update the S&R property so the UI shows the right name.
        if "properties" in n:
            n["properties"]["Node name for S&R"] = "CLIPLoaderGGUF"
        swapped = True
        print("swapped node %d -> CLIPLoaderGGUF, widgets=%s" % (n["id"], n["widgets_values"]))
        break

if not swapped:
    raise SystemExit("CLIPLoader node not found in source workflow")

# Rename the SaveVideo prefix so the output is distinguishable.
for n in d["nodes"]:
    if n["type"] == "SaveVideo":
        n["widgets_values"][0] = "jaisal_intro_A_walkin_gguf"
        print("SaveVideo prefix -> %s" % n["widgets_values"][0])

json.dump(d, open(DST, "w", encoding="utf-8"), ensure_ascii=False)
print("wrote %s" % DST)
