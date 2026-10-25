#!/usr/bin/env python
"""Dump the FULL 459 instance prompt widget (LEEBLAAB sheet prompt template)."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\LEEBLAAB-QwenImage21-Character-SHEET.json", encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}
n459 = nodes[459]
print("widgets:", len(n459["widgets_values"]))
for i, w in enumerate(n459["widgets_values"]):
    print(f"--- widget {i} ({len(str(w))} ch) ---")
    print(str(w))
    print()
