#!/usr/bin/env python
"""Dump the AUTHOR's original H3 prompts: civitai-embedded (05d source) + patreon (05e source)."""
import json

j1 = json.load(open(r"D:\models\vsCodeMcp\data\civitai_embedded_workflow.json", encoding="utf-8"))
n28 = next(n for n in j1["nodes"] if n["id"] == 28)
print("=== CIVITAI (cgpixel23) node 28 ORIGINAL PROMPT ===")
print(n28["widgets_values"][0])
print("\n=== (widget tail)", n28["widgets_values"][1:], "===")

j2 = json.load(open(r"E:\minimax_workflow\character_sheet\minimaxh sheet patreon.json", encoding="utf-8"))
n28b = next(n for n in j2["nodes"] if n["id"] == 28)
print("\n=== PATREON node 28 ORIGINAL PROMPT ===")
print(n28b["widgets_values"][0])
print("\n=== (widget tail)", n28b["widgets_values"][1:], "===")
