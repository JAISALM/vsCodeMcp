#!/usr/bin/env python
"""Check ResolutionSelector aspect/size options + node 83/29 widgets in 02_identity_refset.json."""
import json, urllib.request

# ResolutionSelector options from live object_info
try:
    d = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info/ResolutionSelector", timeout=30))
    req = d["ResolutionSelector"]["input"]["required"]
    for k in ("aspect_ratio", "megapixels", "resolution", "width", "height"):
        if k in req:
            spec = req[k]
            if isinstance(spec, list) and isinstance(spec[0], list):
                print(f"{k}: {spec[0]}")
            else:
                print(f"{k}: default={spec[1].get('default') if isinstance(spec[1], dict) else spec}")
except Exception as e:
    print("ResolutionSelector lookup failed:", e)

j = json.load(open(r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json", encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
for nid in (83, 29, 79, 84, 53):
    n = nodes.get(nid)
    if n:
        print(f"\nnode {nid} ({n['type']}): widgets={n.get('widgets_values')}")
