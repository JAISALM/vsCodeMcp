#!/usr/bin/env python
"""1) subgraph links in the author's Qwen file (what links into 549?)
   2) node 549's inputs[] with link fields
   3) how the pack resolves model_name ([local] prefix) + where it scans for GGUFs"""
import json, re

p = r"E:\minimax_workflow\character_sheet\Qwen Image 2.1 Character Design Sheet.json"
j = json.load(open(p, encoding="utf-8"))
print("=== top-level links touching 555 ===")
for l in j["links"]:
    if l[1] == 555 or l[3] == 555:
        print(l)
subs = j["definitions"]["subgraphs"]
for si, sg in enumerate(subs):
    print(f"\n=== subgraph {si} links ===")
    for l in sg.get("links", []):
        print(l)
    n549 = next((n for n in sg["nodes"] if n["id"] == 549), None)
    if n549:
        print("\n=== node 549 inputs ===")
        for i, inp in enumerate(n549.get("inputs", [])):
            print(f"  in[{i}] {inp.get('name')} ({inp.get('type')}) link={inp.get('link')}")
        print("node 549 widgets_values:", n549.get("widgets_values"))

print("\n\n=== PACK SOURCE: model_name resolution ===")
src = open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-ThinkingLLM\AILab_QwenVL_GGUF.py", encoding="utf-8").read()
print("lines:", len(src.splitlines()))
for m in re.finditer(r".*(\[local\]|base_dir|GGUF_DIR|glob|listdir|scandir).*", src):
    line = m.group(0).strip()
    if line and not line.startswith("#"):
        print(line[:160])
