# -*- coding: utf-8 -*-
"""Diagnose node 79 (Krea2EditModelPatch) wiring in the native identity workflow."""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json"
d = json.load(open(WF, encoding="utf-8"))
links = {l[0]: l for l in d["links"]}
nodes = {n["id"]: n for n in d["nodes"]}

def src(lid):
    l = links.get(lid)
    if not l:
        return "NONE"
    return f"node {l[1]} ({nodes[l[1]]['type']})"

for nid in (92, 73, 113, 72):
    n = nodes[nid]
    print(f"=== node {nid} ({n['type']}) mode={n.get('mode')} widgets={n.get('widgets_values')}")
    for i in n.get("inputs", []):
        print(f"    {i['name']} [{i['type']}] link={i.get('link')} <- {src(i.get('link'))}")
