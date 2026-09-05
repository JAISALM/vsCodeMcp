import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
d = json.load(open(WF_DIR + r"\jaisal_single_shot.json"))
s = d["definitions"]["subgraphs"][0]

print("== full link objects (model chain) ==")
for l in s.get("links", []):
    if l.get("id") in (234, 241, 233, 232, 229):
        print(json.dumps(l))

# production1 node 150 full structure
d1 = json.load(open(WF_DIR + r"\jaisalproduction1.json"))
for n in d1["nodes"]:
    if n["id"] == 150:
        print("\n== production1 node 150 (H3SLAAttention) full ==")
        print(json.dumps(n, indent=1))
