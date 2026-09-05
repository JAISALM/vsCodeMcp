import json

path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
d = json.load(open(path))

def show(nodes, prefix=""):
    for n in nodes:
        wv = n.get("widgets_values")
        if isinstance(wv, list):
            wv = wv[:4]
        print(prefix, n["id"], n["type"], wv)

print("== top-level nodes ==")
show(d["nodes"])

subs = d.get("definitions", {}).get("subgraphs", [])
for i, s in enumerate(subs):
    print(f"== subgraph {i} nodes ==")
    show(s.get("nodes", []), "  ")
