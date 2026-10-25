#!/usr/bin/env python
"""Map the two unmapped H3 workflows in the user's character_sheet folder:
find which one is the 'MiniMax H3 Fizgig' one (FizgigH3StillDecode / toobusy H3 node)."""
import json, os

folder = r"E:\minimax_workflow\character_sheet"
for name in ["LocationOrbitSheetH3.json", "minimaxh sheet patreon.json"]:
    path = os.path.join(folder, name)
    try:
        j = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"\n### {name}: LOAD FAIL {e}")
        continue
    nodes = j.get("nodes", [])
    types = {}
    for n in nodes:
        t = n.get("type", "?")
        types[t] = types.get(t, 0) + 1
    print(f"\n### {name}: {len(nodes)} nodes, {len(j.get('links', []))} links")
    print("  types:", types)
    if "definitions" in j:
        for sg in j["definitions"].get("subgraphs", []):
            for n in sg.get("nodes", []):
                print(f"  subgraph node {n['id']}: {n['type']}")
    # key nodes: H3 + Fizgig + refs
    for n in nodes:
        t = n.get("type", "")
        if any(k in t for k in ("Fizgig", "H3", "Reference", "LoadImage")):
            w = n.get("widgets_values") or []
            print(f"  id={n['id']:>4} {t:<36} widgets={[str(x)[:70] for x in w[:6]]}")
