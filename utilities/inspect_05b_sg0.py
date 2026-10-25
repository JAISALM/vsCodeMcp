#!/usr/bin/env python
"""Dump 05b subgraph-0 internal node input/output shapes (exact UI shape for flat cloning)."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\05b_charsheet_QWEN_jaisal.json"
j = json.load(open(p, encoding="utf-8"))
sg = j["definitions"]["subgraphs"][0]
for n in sg["nodes"]:
    print(f"=== {n['id']} {n['type']}")
    for i, inp in enumerate(n.get("inputs", [])):
        print(f"  in[{i}] {inp.get('name')} type={inp.get('type')} link={inp.get('link')} widget={inp.get('widget')}")
    for o, out in enumerate(n.get("outputs", [])):
        print(f"  out[{o}] {out.get('name')} type={out.get('type')} links={out.get('links')}")
    print(f"  widgets={n.get('widgets_values')}")
