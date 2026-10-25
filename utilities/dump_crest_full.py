#!/usr/bin/env python
"""Dump FULL prompt texts of the crest-carrying nodes (untruncated)."""
import json

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

targets = [
    ("05d_charsheet_H3_wide_jaisal.json", 28, None),
    ("05e_charsheet_H3_fizgig_jaisal.json", 28, None),
    ("08j_KREA2_JAISAL_sheet.json", 84, None),
    ("08j_KREA2_JAISAL_sheet.json", 85, None),
    ("09j_QWEN21_JAISAL_sheet.json", 555, None),
    ("09j_QWEN21_JAISAL_sheet.json", 478, "subgraph"),
]

for f, nid, mode in targets:
    j = json.load(open(f"{BASE}\\{f}", encoding="utf-8"))
    if mode == "subgraph":
        for sg in j["definitions"]["subgraphs"]:
            for n in sg["nodes"]:
                if n["id"] == nid:
                    print("=" * 25, f, f"[subgraph] node {nid} ({n['type']})")
                    print(n["widgets_values"][0])
    else:
        for n in j["nodes"]:
            if n["id"] == nid:
                print("=" * 25, f, f"node {nid} ({n['type']})")
                print(n["widgets_values"][0])
    print()
