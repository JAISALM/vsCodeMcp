import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# --- production1: how is H3SLAAttention (150) wired? ---
d = json.load(open(WF_DIR + r"\jaisalproduction1.json"))
nodes = {n["id"]: n for n in d["nodes"]}
sla = nodes[150]
print("== production1 H3SLAAttention (150) ==")
print("type:", sla["type"])
print("widgets:", sla["widgets_values"])
print("inputs:", [(i["name"], i.get("link")) for i in sla["inputs"]])
print("outputs:", [(o["name"], o.get("links")) for o in sla["outputs"]])
print()
for l in d["links"]:
    lid, src, src_slot, dst, dst_slot, *rest = l
    if src == 150 or dst == 150:
        print(f"link {lid}: node {src} slot {src_slot} -> node {dst} slot {dst_slot}")
print()
# what feeds the model input of 136 (MiniMaxH3ReferenceToVideo)?
mm = nodes[136]
for i in mm["inputs"][:6]:
    print("136 input:", i["name"], "link:", i.get("link"))
# lora node 146 outputs
print("146 outputs:", [(o["name"], o.get("links")) for o in nodes[146]["outputs"]])

# --- single_shot: model chain inside subgraph ---
print()
print("== single_shot subgraph model chain ==")
d2 = json.load(open(WF_DIR + r"\jaisal_single_shot.json"))
for s in d2.get("definitions", {}).get("subgraphs", []):
    snodes = {n["id"]: n for n in s.get("nodes", [])}
    for nid in (6, 121, 104):
        n = snodes.get(nid)
        if n:
            print(f"internal {nid} ({n['type']}):")
            print("  inputs:", [(i["name"], i.get("link")) for i in n["inputs"]])
            print("  outputs:", [(o["name"], o.get("links")) for o in n["outputs"]])
    # links inside subgraph
    print("subgraph links:")
    for l in s.get("links", []):
        lid, src, src_slot, dst, dst_slot, *rest = l
        if src in (6, 121) or dst in (6, 121, 104):
            print(f"  link {lid}: node {src} slot {src_slot} -> node {dst} slot {dst_slot}")
