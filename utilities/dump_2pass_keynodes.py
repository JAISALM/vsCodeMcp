"""Dump the key nodes of krea2T2iI2iInpaint2pass_v15.json to plan the fix.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_2pass_keynodes.py"
"""
import json

WF = r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json"
wf = json.load(open(WF, encoding="utf-8"))

KEY_TYPES = {"LoadImage", "CLIPTextEncode", "Image Saver Simple", "UNETLoader",
             "VAELoader", "LoraLoaderModelOnly", "KSampler", "InpaintModelConditioning",
             "SolidMask", "ResolutionSelector", "ModelSamplingFlux", "CFGOverride",
             "ComfyUI-Krea2T-Enhancer", "ImageResizeKJv2", "EmptyLatentImage",
             "ConditioningZeroOut", "easy seed"}

for n in wf.get("nodes", []):
    t = n.get("type")
    if t in KEY_TYPES:
        print("=" * 70)
        print(f"node {n.get('id')}  type={t}  title={n.get('title')}")
        print("  widgets_values:", json.dumps(n.get("widgets_values"))[:600])
        if n.get("widgets_values_named"):
            print("  widgets_values_named:", json.dumps(n.get("widgets_values_named"))[:600])
        print("  inputs:", [(i.get("name"), i.get("link")) for i in n.get("inputs", [])])
        print("  outputs:", [(o.get("name"), o.get("links")) for o in n.get("outputs", [])])

# subgraph internals
for s in wf.get("definitions", {}).get("subgraphs", []):
    print("=" * 70)
    print("SUBGRAPH", s.get("name"), "id", s.get("id"))
    for n in s.get("nodes", []):
        print(f"  internal node {n.get('id')} type={n.get('type')} widgets={json.dumps(n.get('widgets_values'))[:300]}")
