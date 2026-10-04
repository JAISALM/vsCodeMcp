import json

path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-H3-Motion-Context\example_workflows\MiniMax H3 - fl2va - ref2va.json"
with open(path, "r", encoding="utf-8") as f:
    wf = json.load(f)

def dump(n):
    nid = n.get("id"); ntype = n.get("type")
    if "MotionContext" not in str(ntype):
        return
    print(f"\n[{nid}] {ntype}")
    print(f"  widgets_values = {n.get('widgets_values')}")
    print(f"  widgets_values_named = {n.get('widgets_values_named')}")
    for i in n.get("inputs", []):
        print(f"    in  {i.get('name'):26s} {i.get('type'):12s} link={i.get('link')}")
    for o in n.get("outputs", []):
        print(f"    out {o.get('name'):26s} {o.get('type'):12s} links={o.get('links')}")

# top-level
for n in wf.get("nodes", []):
    dump(n)

# subgraphs
for sg in (wf.get("definitions", {}).get("subgraphs") or []):
    for n in sg.get("nodes", []):
        dump(n)
