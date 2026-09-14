# -*- coding: utf-8 -*-
"""Dry-run: build the API prompt for a workflow and print the key nodes,
WITHOUT submitting. Verifies the native widget mapping is correct."""
import json
import sys
sys.path.insert(0, r"d:\models\vsCodeMcp\utilities")
from submit_krea2_workflow import build_prompt

wf_path = sys.argv[1]
wf = json.load(open(wf_path, encoding="utf-8"))
prompt = build_prompt(wf)

print("=== KEY NODES ===")
for nid, p in prompt.items():
    ct = p["class_type"]
    if ct in ("KSampler", "EmptySD3LatentImage", "Krea2EditModelPatch",
              "Krea2EditGroundedEncode", "LoadImage", "LoraLoaderModelOnly",
              "CLIPLoader", "UNETLoader", "VAELoader", "SaveImage",
              "ResolutionSelector"):
        print(f"\n[{nid}] {ct}:")
        for k, v in p["inputs"].items():
            if isinstance(v, str) and len(v) > 80:
                v = v[:80] + f"... ({len(v)} chars)"
            print(f"    {k} = {v!r}")
