#!/usr/bin/env python
"""Full 05d structure dump — node types, widgets, inputs/outputs, ALL links — for H3 logo clone."""
import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\05d_charsheet_H3_wide_jaisal.json"
j = json.load(open(p, encoding="utf-8"))
print("last_node_id:", j.get("last_node_id"), "last_link_id:", j.get("last_link_id"))
for n in j["nodes"]:
    w = n.get("widgets_values")
    ws = str(w)[:220] if w is not None else None
    print(f"--- {n['id']} {n['type']} mode={n.get('mode',0)} widgets={ws}")
    for i, inp in enumerate(n.get("inputs", [])):
        if inp.get("link") is not None:
            print(f"    in[{i}] {inp.get('name')} ({inp.get('type')}) link={inp.get('link')}")
    for o, out in enumerate(n.get("outputs", [])):
        if out.get("links"):
            print(f"    out[{o}] {out.get('name')} -> {out.get('links')}")
print("=== ALL LINKS ===")
for l in sorted(j["links"], key=lambda x: x[0]):
    print(l)
