#!/usr/bin/env python
"""Audit all long-text widgets (prompts + notes) in the 4 sheet workflows for leftover
CHARACTER ATTRIBUTE descriptions (identity must come ONLY from the ref image).
Allowed: clothing/kit, mood/lighting, composition, crest spec, name JAISAL.
Flagged: age, ethnicity, hair style, beard, build, skin tone, face shape, height, body.
"""
import json, re

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
FILES = ["05d_charsheet_H3_wide_jaisal.json", "05e_charsheet_H3_fizgig_jaisal.json",
         "08j_KREA2_JAISAL_sheet.json", "09j_QWEN21_JAISAL_sheet.json"]

# attribute words/phrases (identity) — case-insensitive
ATTR = [
    r"\bindian\b", r"\b26[- ]?year", r"\b~?26\b", r"\bwavy\b", r"\bblack hair\b",
    r"\bhair\b(?! ?color)", r"\bbeard\b", r"\bslim\b", r"\bbuild\b",
    r"\bskin\b", r"\bbrown\b", r"\byouthful\b", r"\bround face\b", r"\bface shape\b",
    r"\bmalayal", r"\bheight\b", r"\btall\b", r"\bathletic\b", r"\bmuscular\b",
    r"\bethnicity\b", r"\bethnic\b", r"\bmen ?s\b", r"\bman\b", r"\bmen\b",
    r"\bshort beard\b", r"\bpatchy\b", r"\bmedium[- ]?length\b",
]
# "hair color" detail circle is allowed (it's a detail tile, not identity) — exclude those sentences

def scan_text(fname, where, text):
    hits = []
    for pat in ATTR:
        for m in re.finditer(pat, text, re.I):
            s = max(0, m.start() - 90); e = min(len(text), m.end() + 90)
            hits.append((pat, text[s:e].replace("\n", " ⏎ ")))
    if hits:
        print(f"[{fname} | {where}]")
        seen = set()
        for pat, ctx in hits:
            key = ctx[:60]
            if key in seen:
                continue
            seen.add(key)
            print(f"    <{pat}> …{ctx}…")
        print()

for f in FILES:
    j = json.load(open(f"{BASE}\\{f}", encoding="utf-8"))
    for n in j["nodes"]:
        for i, w in enumerate(n.get("widgets_values") or []):
            if isinstance(w, str) and len(w) > 100:
                scan_text(f, f"node {n['id']} ({n['type']}) widget[{i}]", w)
    for sg in (j.get("definitions", {}).get("subgraphs") or []):
        for n in sg.get("nodes", []):
            for i, w in enumerate(n.get("widgets_values") or []):
                if isinstance(w, str) and len(w) > 100:
                    scan_text(f, f"[subgraph] node {n['id']} ({n['type']}) widget[{i}]", w)
print("audit done")
