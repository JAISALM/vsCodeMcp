import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
d = json.load(open(WF_DIR + r"\jaisal_single_shot.json"))

# Collect all internal node IDs
internal_ids = set()
for s in d.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        internal_ids.add(n["id"])
print("internal node ids:", sorted(internal_ids))

# Top-level links referencing internal nodes
print("\n== top-level links touching internal nodes ==")
for l in d["links"]:
    lid, src, src_slot, dst, dst_slot, *rest = l
    if src in internal_ids or dst in internal_ids:
        print(f"link {lid}: node {src} slot {src_slot} -> node {dst} slot {dst_slot}")

# Where does 121's MODEL output (link 233) go?
print("\n== link 233 (121 MODEL out) ==")
for l in d["links"]:
    if l[0] == 233:
        print(l)

# Full internal node list with inputs/outputs
print("\n== all internal nodes ==")
for s in d.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        ins = [(i["name"], i.get("link")) for i in n.get("inputs", [])]
        outs = [(o["name"], o.get("links")) for o in n.get("outputs", [])]
        print(f"{n['id']} {n['type']}: in={ins} out={outs}")
