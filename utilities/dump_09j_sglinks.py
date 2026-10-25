#!/usr/bin/env python
import json
p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\09j_QWEN21_JAISAL_sheet.json"
j = json.load(open(p, encoding="utf-8"))
for i, sg in enumerate(j["definitions"]["subgraphs"]):
    print(f"=== subgraph {i}: nodes={len(sg['nodes'])} links type={type(sg.get('links')).__name__}")
    for l in sg.get("links", []):
        print(" ", l)
    # node modes (bypassed?)
    for n in sg["nodes"]:
        if n["id"] in (478, 480, 481, 549, 551, 458, 557):
            print(f"  node {n['id']} {n['type']} mode={n.get('mode')}")
# main canvas modes for the architect chain
print("=== main canvas modes ===")
for n in j["nodes"]:
    if n["id"] in (478, 480, 481, 549, 551, 555, 557, 558, 484, 459, 74, 461, 569, 570):
        print(f"  {n['id']} {n['type']} mode={n.get('mode', 0)}")
