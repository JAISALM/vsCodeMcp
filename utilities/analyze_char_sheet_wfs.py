r"""Analyze the 4 local character-sheet workflows: node types, model names, structure.
Run: & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "D:\models\vsCodeMcp\utilities\analyze_char_sheet_wfs.py"
"""
import json, glob, os
from collections import Counter

for p in sorted(glob.glob(r"E:\minimax_workflow\character_sheet\*.json")):
    j = json.load(open(p, encoding="utf-8"))
    print("=" * 90)
    print(os.path.basename(p))
    nodes = j.get("nodes", [])
    c = Counter(str(n.get("type")) for n in nodes)
    for t, k in c.most_common():
        print(f"  {t}: {k}")
    print("  -- key nodes:")
    for n in nodes:
        t = str(n.get("type"))
        if any(x in t for x in ("Loader", "Sampler", "LoadImage", "SaveImage", "Generate",
                                "Reference", "H3", "Sheet", "Prompt", "Note", "Latent",
                                "Upscale", "Encode", "Decode", "MiniMax", "Text", "Video")):
            wv = json.dumps(n.get("widgets_values"), ensure_ascii=False)[:200]
            nid = n.get("id")
            print(f"    [{nid}] {t}: {wv}")
    subs = j.get("definitions", {}).get("subgraphs", [])
    for s in subs:
        print(f"  SUBGRAPH {s.get('id')} ({len(s.get('nodes', []))} nodes): "
              + ", ".join(str(x.get("type")) for x in s.get("nodes", [])[:12]))
    print()
