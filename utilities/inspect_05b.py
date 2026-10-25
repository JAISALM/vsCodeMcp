#!/usr/bin/env python
"""Inspect 05b (Qwen 2.1 t2i sheet) — full structure for cloning into a logo t2i workflow."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\05b_charsheet_QWEN_jaisal.json"
j = json.load(open(p, encoding="utf-8"))
print("last_node_id:", j.get("last_node_id"), "last_link_id:", j.get("last_link_id"))
for n in j["nodes"]:
    w = n.get("widgets_values")
    ws = str(w)[:300] if w is not None else None
    print(f"--- {n['id']} {n['type']} mode={n.get('mode',0)} widgets={ws}")
    for i, inp in enumerate(n.get("inputs", [])):
        if inp.get("link") is not None:
            print(f"    in[{i}] {inp.get('name')} ({inp.get('type')}) link={inp.get('link')}")
    for o, out in enumerate(n.get("outputs", [])):
        if out.get("links"):
            print(f"    out[{o}] {out.get('name')} -> {out.get('links')}")
print("=== subgraphs ===")
for i, sg in enumerate(j.get("definitions", {}).get("subgraphs") or []):
    print(f"sg{i}: {[ (n['id'], n['type']) for n in sg['nodes'] ]}")
    for n in sg["nodes"]:
        w = n.get("widgets_values")
        print(f"  {n['id']} {n['type']} mode={n.get('mode',0)} widgets={str(w)[:300]}")
