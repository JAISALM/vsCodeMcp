#!/usr/bin/env python
"""Full node map of 02_identity_refset.json — what feeds the GroundedEncode, which refs exist."""
import json

j = json.load(open(r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json", encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
print("=== nodes ===")
for nid, n in sorted(nodes.items()):
    print(f"{nid} {n['type']}: {str(n.get('widgets_values'))[:100]}")
print("\n=== links (id, from, from_slot, to, to_slot, type) ===")
for l in j["links"]:
    print(l)
print("\n=== inputs of node 84 ===")
for i, inp in enumerate(nodes[84].get("inputs", [])):
    print(f"  in[{i}] {inp.get('name')} ({inp.get('type')}) link={inp.get('link')}")
