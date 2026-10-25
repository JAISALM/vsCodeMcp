#!/usr/bin/env python
"""Summarize a ComfyUI UI-format workflow: node types + key widget values."""
import json
import sys

path = sys.argv[1]
j = json.load(open(path, encoding="utf-8", errors="ignore"))
nodes = j.get("nodes", [])
print(f"file: {path}")
print(f"nodes: {len(nodes)} | links: {len(j.get('links', []))} | title: {j.get('title','')}")
print("-" * 100)
for n in nodes:
    t = n.get("type", "?")
    wv = n.get("widgets_values", [])
    keep = any(k in t for k in (
        "Loader", "Lora", "LoadImage", "SaveImage", "KSampler", "Empty",
        "TextGenerate", "Note", "Switch", "If", "Dataset", "Klein", "Grid",
        "Prompt", "VAE", "CLIP", "UNET"))
    if keep:
        s = str(wv)[:170].replace("\n", " / ")
        print(f"{n.get('id','?'):>4} {t:<28} {s}")
