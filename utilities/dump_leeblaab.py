#!/usr/bin/env python
"""Full dump of the LEEBLAAB Qwen 2.1 sheet workflow (all nodes + links)."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\LEEBLAAB-QwenImage21-Character-SHEET.json", encoding="utf-8", errors="ignore"))
for n in j["nodes"]:
    wv = n.get("widgets_values", [])
    s = str(wv)[:500].replace("\n", " / ")
    print(f"== {n['id']} {n['type']} ==")
    print(s)
    print()
print("=== LINKS (id, origin, oslot, target, tslot, type) ===")
for l in j["links"]:
    print(l[:6])
