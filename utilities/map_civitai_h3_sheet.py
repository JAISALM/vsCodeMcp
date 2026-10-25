#!/usr/bin/env python
"""Map the civitai-embedded H3 sheet workflow (70 nodes)."""
import json

j = json.load(open(r"D:\models\vsCodeMcp\data\civitai_embedded_workflow.json", encoding="utf-8"))
nodes = j["nodes"]
links = j["links"]
print(f"{len(nodes)} nodes, {len(links)} links")
print()
for n in sorted(nodes, key=lambda x: x["id"]):
    w = n.get("widgets_values", [])
    wstr = [str(x)[:55] for x in w[:6]]
    ins = [f"{i['name']}({i['type']})" for i in n.get("inputs", []) if i.get("link")]
    print(f"[{n['id']:>3}] {n['type']:<38} w={wstr} in={ins}")

# link map
print("\n=== links ===")
for l in links:
    lid, oid, oslot, tid, tslot, ltype = l
    print(f"link {lid}: {oid} -> {tid} slot {tslot} ({ltype})")
