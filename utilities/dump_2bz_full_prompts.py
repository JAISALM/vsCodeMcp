#!/usr/bin/env python
"""Dump full prompt texts of 2BZ nodes 13 (master prompt), 24, 49."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\2BZ_H3_character_sheet_2stage_v1_EN.json", encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}

for nid in (13, 24, 49):
    n = nodes[nid]
    print(f"########## NODE {nid} {n['type']} ##########")
    for i, w in enumerate(n.get("widgets_values", [])):
        if isinstance(w, str) and len(w) > 100:
            print(f"--- widget {i} ({len(w)} ch) ---")
            print(w)
            print()
    print()
