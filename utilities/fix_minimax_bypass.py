import json

path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\mini-max-jaisal-test.json"
wf = json.load(open(path, encoding="utf-8"))
n = {x["id"]: x for x in wf["nodes"]}

# --- Rewire links 67 and 68 to come from node 1 (raw UNET) instead of node 49 ---
for l in wf["links"]:
    if l[0] == 67:
        l[1] = 1   # from node 1
        l[2] = 0
    if l[0] == 68:
        l[1] = 1
        l[2] = 0

# --- Remove the now-unused optimization-chain links 56, 65, 66 ---
wf["links"] = [l for l in wf["links"] if l[0] not in (56, 65, 66)]

# --- Node 1 output links: now feeds 21 and 23 directly ---
n[1]["outputs"][0]["links"] = [67, 68]

# --- Bypass the optimization chain nodes 45, 47, 49 and disconnect them ---
for nid in (45, 47, 49):
    n[nid]["mode"] = 4
    # clear model input link
    for inp in n[nid]["inputs"]:
        if inp["name"] == "model":
            inp["link"] = None
    # clear output links
    for o in n[nid]["outputs"]:
        o["links"] = []

json.dump(wf, open(path, "w", encoding="utf-8"), indent=1)
print("rewired. node1 outputs:", n[1]["outputs"][0]["links"])
print("node45 mode:", n[45]["mode"], "node47 mode:", n[47]["mode"], "node49 mode:", n[49]["mode"])
print("link67:", [l for l in wf["links"] if l[0] == 67])
print("link68:", [l for l in wf["links"] if l[0] == 68])
print("node21 model link:", [i for i in n[21]["inputs"] if i["name"] == "model"][0]["link"])
print("node23 model link:", [i for i in n[23]["inputs"] if i["name"] == "model"][0]["link"])
