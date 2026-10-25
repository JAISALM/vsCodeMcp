#!/usr/bin/env python
"""Scan 09j for ALL model-file references (safetensors/gguf/ckpt/pt) in every widget
(main canvas + subgraphs) and check existence in both model trees."""
import json, os, re

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json"
TREES = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models",
    r"E:\ComfyUI_windows_portable\ComfyUI\models",
]
j = json.load(open(P, encoding="utf-8"))

found = []

def scan(n, where):
    for i, w in enumerate(n.get("widgets_values") or []):
        if isinstance(w, str) and re.search(r"\.(safetensors|gguf|ckpt|pt|pth|bin)$", w):
            found.append((where, n["id"], n["type"], i, w))
    for k, v in (n.get("widgets_values_named") or {}).items():
        if isinstance(v, str) and re.search(r"\.(safetensors|gguf|ckpt|pt|pth|bin)$", v):
            found.append((where, n["id"], n["type"], f"named:{k}", v))

for n in j["nodes"]:
    scan(n, "main")
for sg in (j.get("definitions", {}).get("subgraphs") or []):
    for n in sg.get("nodes", []):
        scan(n, "subgraph")

# existence check
def exists(fname):
    for tree in TREES:
        for root, _, files in os.walk(tree):
            if fname in files:
                return f"{root}"
    return None

print(f"{'WHERE':<10} {'NODE':<6} {'TYPE':<28} {'IDX':<14} FILE")
for where, nid, ntype, idx, fname in sorted(found, key=lambda x: (x[0], str(x[1]))):
    loc = exists(fname)
    print(f"{where:<10} {nid:<6} {ntype:<28} {str(idx):<14} {fname}")
    print(f"{'':<52} -> {loc if loc else '!!! NOT FOUND ON DISK !!!'}")
print()
print("total model refs:", len(found))
