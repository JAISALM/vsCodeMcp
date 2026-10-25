#!/usr/bin/env python
"""All-layers model-reference check for all 4 sheet workflows: positional widgets,
named widgets, instance nodes — flag any file not on disk."""
import json, os, re

BASES = [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows",
         r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"]
FILES = ["05d_charsheet_H3_wide_jaisal.json", "05e_charsheet_H3_fizgig_jaisal.json",
         "08j_KREA2_JAISAL_sheet.json", "09j_QWEN21_JAISAL_sheet.json"]
TREES = [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models",
         r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\LLM",
         r"E:\ComfyUI_windows_portable\ComfyUI\models"]

disk = set()
for tree in TREES:
    for root, _, files in os.walk(tree):
        disk.update(files)

def check(fname, where, label, val):
    bare = val.lstrip("[]local] ").strip()
    if re.search(r"\.(safetensors|gguf|ckpt|pt|pth|bin)$", val) and val not in disk:
        print(f"  {where} {label}: {val}  !!! NOT ON DISK")

for base in BASES:
    for f in FILES:
        j = json.load(open(f"{base}\\{f}", encoding="utf-8"))
        print(f"== {f} ({'UI' if 'comfyUi_latest' in base else 'project'})")
        for n in j["nodes"]:
            wv = n.get("widgets_values") or []
            for i, w in enumerate(wv):
                if isinstance(w, str):
                    check(f, f"node {n['id']} ({n['type']})", f"widgets[{i}]", w)
            for k, v in (n.get("widgets_values_named") or {}).items():
                if isinstance(v, str):
                    check(f, f"node {n['id']} ({n['type']})", f"named:{k}", v)
        for sg in (j.get("definitions", {}).get("subgraphs") or []):
            for n in sg.get("nodes", []):
                wv = n.get("widgets_values") or []
                for i, w in enumerate(wv):
                    if isinstance(w, str):
                        check(f, f"[sub] node {n['id']} ({n['type']})", f"widgets[{i}]", w)
                for k, v in (n.get("widgets_values_named") or {}).items():
                    if isinstance(v, str):
                        check(f, f"[sub] node {n['id']} ({n['type']})", f"named:{k}", v)
print("check done")
