import json, sys

path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_B_setup.json"
with open(path, "r", encoding="utf-8") as f:
    wf = json.load(f)

print("=== NODES ===")
for n in wf["nodes"]:
    nid = n.get("id")
    ntype = n.get("type")
    wv = n.get("widgets_values")
    # shorten widgets_values for display
    wvs = wv
    if isinstance(wv, list) and len(str(wv)) > 120:
        wvs = str(wv)[:120] + "..."
    print(f"\n[{nid}] {ntype}  widgets={wvs}")
    for i in n.get("inputs", []):
        lnk = i.get("link")
        print(f"    in  {i.get('name'):24s} {i.get('type'):14s} link={lnk}")
    for o in n.get("outputs", []):
        print(f"    out {o.get('name'):24s} {o.get('type'):14s} links={o.get('links')}")

print("\n=== LINKS ===")
for l in wf.get("links", []):
    # link = [id, from_node, from_slot, to_node, to_slot, type]
    if isinstance(l, list) and len(l) >= 6:
        print(f"  link {l[0]}: node {l[1]} slot {l[2]} -> node {l[3]} slot {l[4]} ({l[5]})")
