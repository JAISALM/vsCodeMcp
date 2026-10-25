#!/usr/bin/env python
"""Find the Qwen 2.1 loader nodes in 09j (subgraph) — confirm ids + current widget values."""
import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json"
j = json.load(open(p, encoding="utf-8"))
for sg in j["definitions"]["subgraphs"]:
    for n in sg["nodes"]:
        if n["type"] in ("UNETLoader", "CLIPLoader", "VAELoader"):
            print(f"subgraph node {n['id']} ({n['type']}): widgets={n.get('widgets_values')}")
