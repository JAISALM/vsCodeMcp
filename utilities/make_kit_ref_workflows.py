#!/usr/bin/env python
"""Build the kit-reference (jersey flat-lay) t2i workflows from the 01 template.

01 node map (D142 recipe): 300 positive, 301 negative, 53 KSampler
[seed, fixed, 8, 1, euler, simple, 1], 82 EmptySD3LatentImage [w, h, 1],
29 SaveImage. Models untouched (Krea2Realism_V1 + V2 @1.0 + qwen3vl_4b + qwen_image_vae).

Output: 07_kit_ref_jaisal.json (blue kit) / 07_kit_ref_zidane.json (dark green kit).
"""
import json
import os

SRC = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\01_character_sheet.json"
OUT = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"

def kit_prompt(color, name):
    # D145 crest spec (user): fist roundel ONLY — NO PALESTINE RESISTANCE text.
    # Subtle solidarity symbol, not an obvious slogan.
    return (
        f"Product photograph of a men's soccer kit laid out flat on a clean light-grey studio background, "
        f"top-down flat-lay view: a {color} short-sleeve soccer jersey with a small, subtle white emblem on the left chest — "
        f"a simple clenched fist inside a thin circle, plain and minimal, no words, no letters, no text of any kind — "
        f"and matching {color} track pants with a single white stripe down each side, jersey neatly above the pants. "
        f"No person, no face, no other objects. Sharp even studio product lighting, crisp fabric detail, photoreal. kr2realism"
    )

VARIANTS = [
    ("jaisal", "royal blue", "JAISAL", "jaisal_kit_ref_00002", [13, "fixed", 8, 1, "euler", "simple", 1]),
    ("zidane", "dark green", "ZIDANE", "zidane_kit_ref_00002", [29, "fixed", 8, 1, "euler", "simple", 1]),
]

NEG = "person, face, head, blurry, low quality, watermark, text, words, letters, slogan, logo distortion"

j = json.load(open(SRC, encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}
assert nodes[300]["type"] == "CLIPTextEncode" and nodes[53]["type"] == "KSampler" and nodes[29]["type"] == "SaveImage"
print("source OK — 300/301/53/82/29 confirmed")

for char, color, name, prefix, sampler in VARIANTS:
    j2 = json.loads(json.dumps(j))
    n2 = {n["id"]: n for n in j2["nodes"]}
    n2[300]["widgets_values"] = [kit_prompt(color, name)]
    n2[301]["widgets_values"] = [NEG]
    n2[53]["widgets_values"] = sampler
    n2[82]["widgets_values"] = [1152, 1152, 1]
    n2[29]["widgets_values"] = [prefix]
    out = os.path.join(OUT, f"07_kit_ref_{char}.json")
    json.dump(j2, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"WROTE {out}")
    print(f"  kit: {color} | save: {prefix} | seed: {sampler[0]}")
