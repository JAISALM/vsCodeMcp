#!/usr/bin/env python
"""Dump civitai node 28 (H3 R2V) full inputs/widgets + the links touching it,
plus nodes 7/8/9/64/65/12/6 (sampler chain) for the wide-sheet builder."""
import json

j = json.load(open(r"D:\models\vsCodeMcp\data\civitai_embedded_workflow.json", encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

n28 = nodes[28]
print("=== node 28 inputs (slot index -> name/type) ===")
for i, inp in enumerate(n28["inputs"]):
    print(f"  slot {i}: {inp['name']} ({inp['type']}) link={inp.get('link')}")
print("widgets:", n28["widgets_values"][:6])

for nid in (7, 8, 9, 64, 65, 12, 6, 66, 67):
    n = nodes[nid]
    print(f"\n=== node {nid} ({n['type']}) widgets={n['widgets_values'][:6]}")
    for i, inp in enumerate(n["inputs"]):
        print(f"  slot {i}: {inp['name']} ({inp['type']}) link={inp.get('link')}")

print("\n=== all links ===")
for l in j["links"]:
    print(l)
