#!/usr/bin/env python
"""Full dump of 'minimaxh sheet patreon.json' (the Fizgig H3 sheet workflow)."""
import json

path = r"E:\minimax_workflow\character_sheet\minimaxh sheet patreon.json"
j = json.load(open(path, encoding="utf-8"))
print("top keys:", list(j.keys()))
print(f"last_node_id={j.get('last_node_id')} last_link_id={j.get('last_link_id')}\n")

for n in j["nodes"]:
    w = n.get("widgets_values") or []
    ws = " | ".join(str(x)[:90] for x in w[:10])
    print(f"id={n['id']:>4} {n['type']:<34} widgets=[{ws}]")
    for i, inp in enumerate(n.get("inputs", [])):
        print(f"      in[{i}] {inp.get('name')} ({inp.get('type')}) link={inp.get('link')}")

print("\n=== LINKS ===")
for l in j["links"]:
    print(f"link {l[0]}: {l[1]} -> {l[3]} slot {l[4]} ({l[5]})")

print("\n=== SUBGRAPH ===")
for sg in j.get("definitions", {}).get("subgraphs", []):
    for n in sg.get("nodes", []):
        w = n.get("widgets_values") or []
        ws = " | ".join(str(x)[:90] for x in w[:10])
        print(f"  id={n['id']:>4} {n['type']:<34} widgets=[{ws}]")
