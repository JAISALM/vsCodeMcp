#!/usr/bin/env python
"""Summarize the LEEBLAAB Qwen Image 2.1 character sheet workflow."""
import json

path = r"E:\minimax_workflow\character_sheet\LEEBLAAB-QwenImage21-Character-SHEET.json"
try:
    j = json.load(open(path, encoding="utf-8", errors="ignore"))
except Exception as e:
    print("parse fail:", e)
    raise SystemExit
nodes = j.get("nodes", [])
print(f"file: {path}")
print(f"nodes: {len(nodes)} | links: {len(j.get('links', []))}")
print("-" * 100)
for n in nodes:
    t = n.get("type", "?")
    wv = n.get("widgets_values", [])
    keep = any(k in t for k in (
        "Loader", "Lora", "LoadImage", "SaveImage", "KSampler", "Empty",
        "TextGenerate", "Note", "Switch", "If", "Qwen", "Note", "Prompt",
        "VAE", "CLIP", "UNET", "Generate", "Text", "Image", "Combine", "Grid"))
    if keep:
        s = str(wv)[:170].replace("\n", " / ")
        print(f"{n.get('id', '?'):>4} {t:<28} {s}")
