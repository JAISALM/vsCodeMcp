#!/usr/bin/env python
"""Create Jaisal/Zidane variants of the 1 Click Dataset (Klein 9b) workflow.

Loads E:\Flux_klein\1 Click Dataset (Klein 9b).json, swaps the reference face
(LoadImage node 76) and the output prefix (SaveImage node 280), writes the
two variants next to the original.
"""
import json
import os

SRC = r"E:\Flux_klein\1 Click Dataset (Klein 9b).json"

VARIANTS = [
    ("jaisal_portrait_HD.png", r"Dataset\Jaisal\Image"),
    ("zidane_portrait_HD.png", r"Dataset\Zidane\Image"),
]

j = json.load(open(SRC, encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}

# sanity-check the two nodes we touch
print("before 76:", nodes[76]["widgets_values"])
print("before 280:", nodes[280]["widgets_values"])
assert nodes[76]["type"] == "LoadImage"
assert nodes[280]["type"] == "SaveImage"

for face, prefix in VARIANTS:
    j2 = json.loads(json.dumps(j))  # deep copy
    n76 = next(n for n in j2["nodes"] if n["id"] == 76)
    n280 = next(n for n in j2["nodes"] if n["id"] == 280)
    n76["widgets_values"] = [face, "image"]
    n280["widgets_values"] = [prefix]
    name = face.split("_")[0]
    out = os.path.join(os.path.dirname(SRC), f"1 Click Dataset (Klein 9b) - {name}.json")
    json.dump(j2, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE:", out)
    print("  76 ->", n76["widgets_values"], "| 280 ->", n280["widgets_values"])
