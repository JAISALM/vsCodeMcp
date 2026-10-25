#!/usr/bin/env python
"""Dump full crest-related prompt text from the 4 sheet workflows (main copies)."""
import json, re

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
files = ["05d_charsheet_H3_wide_jaisal.json", "05e_charsheet_H3_fizgig_jaisal.json",
         "08j_KREA2_JAISAL_sheet.json", "09j_QWEN21_JAISAL_sheet.json"]

for f in files:
    j = json.load(open(f"{BASE}\\{f}", encoding="utf-8"))
    print("=" * 30, f)
    # find all nodes carrying long text prompts (main canvas)
    for n in j["nodes"]:
        wv = n.get("widgets_values") or []
        for i, w in enumerate(wv):
            if isinstance(w, str) and len(w) > 300 and ("crest" in w or "emblem" in w or "fist" in w):
                print(f"--- node {n['id']} ({n['type']}) widget[{i}] len={len(w)}")
                # print only crest/emblem/fist sentences
                for sent in re.split(r"(\n|;)", w):
                    if re.search(r"crest|emblem|fist|roundel", sent, re.I):
                        print("   |", sent[:400])
    # subgraph definitions
    for sg in (j.get("definitions", {}).get("subgraphs") or []):
        for n in sg.get("nodes", []):
            wv = n.get("widgets_values") or []
            for i, w in enumerate(wv):
                if isinstance(w, str) and len(w) > 300 and ("crest" in w or "emblem" in w or "fist" in w):
                    print(f"--- [subgraph] node {n['id']} ({n['type']}) widget[{i}] len={len(w)}")
                    for sent in re.split(r"(\n|;)", w):
                        if re.search(r"crest|emblem|fist|roundel", sent, re.I):
                            print("   |", sent[:400])
