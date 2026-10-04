# -*- coding: utf-8 -*-
"""Compare R2V widget length vs the hidden math-node seconds across all 10 intro shots."""
import json, os, glob

wfdir = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
print("=== R2V widget length (index 3) vs hidden math-node seconds ===")
for fp in sorted(glob.glob(os.path.join(wfdir, "jaisal_intro_*.json"))):
    d = json.load(open(fp, encoding="utf-8"))
    nodes = {n["id"]: n for n in d["nodes"]}
    name = os.path.basename(fp)
    for n in d["nodes"]:
        if n["type"] == "MiniMaxH3ReferenceToVideo":
            wv = n.get("widgets_values", [])
            wl = wv[3] if len(wv) > 3 else "?"
            secs = None
            for m in d["nodes"]:
                if m["type"] == "ComfyMathExpression":
                    for i in m["inputs"]:
                        if i["name"] == "values.a" and i.get("link"):
                            for l in d["links"]:
                                if l[0] == i["link"] and nodes.get(l[1], {}).get("type") == "PrimitiveFloat":
                                    secs = nodes[l[1]].get("widgets_values", [None])[0]
            wls = round(wl / 24, 1) if isinstance(wl, int) else "?"
            print("  %-38s widget_len=%s (%ss)  BUT math-node secs=%s -> ACTUALLY RUNS %ss" % (name, wl, wls, secs, secs))
