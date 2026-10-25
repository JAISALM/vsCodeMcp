#!/usr/bin/env python
"""Extract the subgraph internals of the LEEBLAAB workflow (model loaders etc.)."""
import json

j = json.load(open(r"E:\minimax_workflow\character_sheet\LEEBLAAB-QwenImage21-Character-SHEET.json", encoding="utf-8", errors="ignore"))
defs = j.get("definitions", {})
sigs = defs.get("subgraphs", [])
print(f"subgraphs: {len(sigs)}")
for sg in sigs:
    nodes = sg.get("nodes", [])
    print(f"subgraph {sg.get('id')} — nodes: {len(nodes)}")
    for n in nodes:
        t = n.get("type", "?")
        wv = n.get("widgets_values", [])
        s = str(wv)[:200].replace("\n", " / ")
        print(f"  {n.get('id','?'):>4} {t:<30} {s}")
