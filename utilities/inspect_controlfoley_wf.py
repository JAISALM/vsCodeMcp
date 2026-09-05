"""Inspect the ControlFoley workflow structure (links, node inputs, widgets)."""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_sketch_title_audio.json"

wf = json.load(open(WF, encoding="utf-8"))
print("=== LINKS ===")
for l in wf["links"]:
    print(f"  link {l[0]}: node {l[1]} slot {l[2]} -> node {l[3]} slot {l[4]} ({l[5]})")

for nid in (2, 3, 4, 5):
    n = next(x for x in wf["nodes"] if x["id"] == nid)
    print(f"=== NODE {nid} [{n['type']}] ===")
    print("  inputs:")
    for i in n.get("inputs", []):
        print(f"    {i['name']} ({i['type']}) link={i.get('link')}")
    print("  outputs:")
    for o in n.get("outputs", []):
        print(f"    {o['name']} ({o['type']}) links={o.get('links')}")
    print(f"  widgets_values: {n.get('widgets_values')}")
