import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
d = json.load(open(WF_DIR + r"\jaisal_single_shot.json"))

s = d["definitions"]["subgraphs"][0]
print("subgraph keys:", list(s.keys()))
print("num subgraph links:", len(s.get("links", [])))
print("\n== subgraph links (model-relevant) ==")
for l in s.get("links", []):
    lid, src, src_slot, dst, dst_slot, *rest = l
    if src in (6, 121, 122, 9, 16) or dst in (6, 121, 122, 9, 16):
        print(f"link {lid}: node {src} slot {src_slot} -> node {dst} slot {dst_slot}")

# max link id across whole file (top-level + subgraph)
all_ids = [l[0] for l in d["links"]]
all_ids += [l[0] for l in s.get("links", [])]
print("\nmax link id overall:", max(all_ids))

# max node id
all_nids = [n["id"] for n in d["nodes"]]
all_nids += [n["id"] for n in s.get("nodes", [])]
print("max node id overall:", max(all_nids))

# Show a sample subgraph link full structure
print("\nsample subgraph link[0]:", s["links"][0])
