#!/usr/bin/env python
"""1) Summarize the new Qwen 2.1 Character Design Sheet workflow.
2) Extract the ComfyUI workflow embedded in the civitai PNG (tEXt chunks)."""
import json, base64, io
from PIL import Image

print("=" * 70)
print("NEW QWEN WORKFLOW")
print("=" * 70)
p = r"E:\minimax_workflow\character_sheet\Qwen Image 2.1 Character Design Sheet.json"
raw = open(p, "rb").read()
j = json.loads(raw.decode("utf-8", errors="ignore"))
if isinstance(j, dict) and "nodes" in j:
    nodes = j["nodes"]
    print(f"UI format, {len(nodes)} root nodes")
    for n in nodes:
        w = n.get("widgets_values", [])
        wstr = [str(x)[:60] for x in w]
        print(f"  [{n['id']}] {n['type']}: {wstr[:6]}")
    if "definitions" in j and j["definitions"]:
        for i, sg in enumerate(j["definitions"].get("subgraphs", [])):
            print(f"  subgraph[{i}]: {len(sg['nodes'])} internal nodes")
            for n in sg["nodes"]:
                w = n.get("widgets_values", [])
                wstr = [str(x)[:60] for x in w]
                print(f"    [{n['id']}] {n['type']}: {wstr[:6]}")
else:
    print("API format:", list(j.keys())[:10])

print()
print("=" * 70)
print("CIVITAI PNG EMBEDDED WORKFLOW")
print("=" * 70)
img = Image.open(r"E:\minimax_workflow\character_sheet\1CJX8DERQKDMG6Z2C5QC4D6HW0.png")
print("size:", img.size, "format:", img.format)
info = img.info
print("info keys:", list(info.keys()))
for k in ("workflow", "prompt", "parameters", "description"):
    v = info.get(k)
    if v is None:
        continue
    if isinstance(v, bytes):
        v = v.decode("utf-8", errors="ignore")
    print(f"\n--- {k}: {len(v)} chars ---")
    # try to decode base64 (ComfyUI embeds base64)
    data = None
    try:
        data = base64.b64decode(v, validate=True)
        data = data.decode("utf-8", errors="ignore")
        print("(base64 decoded) first 500:", data[:500])
        data = json.loads(data)
        if isinstance(data, dict) and "nodes" in data:
            print(f"UI format: {len(data['nodes'])} nodes")
            for n in data["nodes"][:40]:
                w = n.get("widgets_values", [])
                print(f"  [{n['id']}] {n['type']}: {[str(x)[:50] for x in w[:5]]}")
            if data.get("definitions"):
                for i, sg in enumerate(data["definitions"].get("subgraphs", [])):
                    print(f"  subgraph[{i}]: {len(sg['nodes'])} internal nodes")
        else:
            print("first 800:", json.dumps(data)[:800])
    except Exception as e:
        print(f"(not base64 JSON: {e}) first 500: {v[:500]}")
    out = r"D:\models\vsCodeMcp\data\civitai_embedded_%s.json" % k
    with open(out, "w", encoding="utf-8") as f:
        f.write(v if isinstance(v, str) else v.decode("utf-8", errors="ignore"))
    print(f"saved raw -> {out}")
