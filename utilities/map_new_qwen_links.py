#!/usr/bin/env python
"""Dump the new Qwen workflow: links, subgraph internals (list format), instance inputs."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\Qwen Image 2.1 Character Design Sheet.json", encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

print("=== LINKS ===")
for l in j["links"]:
    lid, oid, oslot, tid, tslot, ltype = l
    print(f"link {lid}: {oid} -> {tid} slot {tslot} ({ltype})")

print("\n=== instance inputs ===")
for nid in (459, 555, 569, 485, 459):
    n = nodes[nid]
    print(f"\nnode {nid} ({n['type']}):")
    for i, inp in enumerate(n.get("inputs", [])):
        print(f"  slot {i}: {inp['name']} ({inp['type']}) link={inp.get('link')}")

subs = j.get("definitions", {}).get("subgraphs", [])
print(f"\n=== {len(subs)} subgraphs ===")
for sg in subs:
    print(f"\n-- subgraph key={sg.get('key')}: {len(sg.get('nodes', []))} nodes")
    for n in sg.get("nodes", []):
        w = n.get("widgets_values") or []
        ws = " | ".join(str(x)[:110] for x in w[:6])
        print(f"  id={n['id']:>4} {n['type']:<42} widgets=[{ws}]")
