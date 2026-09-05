import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
d = json.load(open(WF_DIR + r"\jaisal_single_shot.json"))
s = d["definitions"]["subgraphs"][0]

print("== subgraph links (model-relevant) ==")
for l in s.get("links", []):
    lid = l.get("id")
    src = l.get("origin_id") or l.get("from_node")
    dst = l.get("target_id") or l.get("to_node")
    src_slot = l.get("origin_slot") or l.get("from_slot")
    dst_slot = l.get("target_slot") or l.get("to_slot")
    if src in (6, 121, 122, 9, 16) or dst in (6, 121, 122, 9, 16):
        print(f"link {lid}: node {src} slot {src_slot} -> node {dst} slot {dst_slot}")

print("\n== sample subgraph link (full) ==")
print(json.dumps(s["links"][0], indent=1))

# max link id
all_ids = [l[0] for l in d["links"]]
all_ids += [l.get("id") for l in s.get("links", [])]
print("\nmax link id overall:", max(all_ids))

all_nids = [n["id"] for n in d["nodes"]]
all_nids += [n["id"] for n in s.get("nodes", [])]
print("max node id overall:", max(all_nids))
