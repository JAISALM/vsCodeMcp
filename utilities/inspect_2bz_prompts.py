#!/usr/bin/env python
"""Inspect node 13 (MiniMaxH3ReferenceToVideo) + prompt-related widgets of the 2BZ workflow."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\2BZ_H3_character_sheet_2stage_v1_EN.json", encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}

n13 = nodes[13]
print("=== node 13", n13["type"], "===")
for i, w in enumerate(n13.get("widgets_values", [])):
    s = str(w)
    print(f"[{i}] ({len(s)} ch): {s[:600]}")
    print()

# also list all node types that carry long text widgets (prompt builders)
print("=== nodes with long text widgets ===")
for n in j["nodes"]:
    for w in n.get("widgets_values", []):
        if isinstance(w, str) and len(w) > 200:
            print(f"node {n['id']} {n['type']}: {w[:150].replace(chr(10), ' / ')!r}...")
            break
