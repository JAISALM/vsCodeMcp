import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
path = WF_DIR + r"\jaisal_single_shot.json"
d = json.load(open(path))
s = d["definitions"]["subgraphs"][0]
nodes = {n["id"]: n for n in s["nodes"]}

# Show current node-level link fields before fixing
for nid in (122, 9, 16, 150):
    n = nodes[nid]
    print(f"BEFORE {nid} {n['type']}: inputs[0].link={n['inputs'][0].get('link')} outputs[0].links={n['outputs'][0].get('links')}")

# Fix node-level link references to match the links array:
# 122 (switch) -> 150 (SLA) via link 246
# 150 (SLA) -> 9 (scheduler) via link 247
# 150 (SLA) -> 16 (guider) via link 248
nodes[122]["outputs"][0]["links"] = [246]
nodes[9]["inputs"][0]["link"] = 247
nodes[16]["inputs"][0]["link"] = 248
nodes[150]["inputs"][0]["link"] = 246
nodes[150]["outputs"][0]["links"] = [247, 248]

# Ensure the links array has exactly these three (remove stale 234/241 if present)
s["links"] = [l for l in s["links"] if l.get("id") not in (234, 241)]
existing = {l.get("id") for l in s["links"]}
for lid, src, dst in ((246, 122, 150), (247, 150, 9), (248, 150, 16)):
    if lid not in existing:
        s["links"].append({"id": lid, "origin_id": src, "origin_slot": 0, "target_id": dst, "target_slot": 0, "type": "MODEL"})

for nid in (122, 9, 16, 150):
    n = nodes[nid]
    print(f"AFTER  {nid} {n['type']}: inputs[0].link={n['inputs'][0].get('link')} outputs[0].links={n['outputs'][0].get('links')}")

json.dump(d, open(path, "w"), indent=1)
print("saved")
