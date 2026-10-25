import json, io

base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_cine_test.json"
out  = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_mu_test.json"

w = json.load(open(base, encoding="utf-8"))

# 1. find the existing link feeding KSampler(53) model input (slot 0)
ks_model_link = None
for i, L in enumerate(w["links"]):
    if L[3] == 53 and L[4] == 0:
        ks_model_link = i
        break
assert ks_model_link is not None, "KSampler model link not found"
old_link = w["links"][ks_model_link]
from_node = old_link[1]          # last LoRA node (303)
print("KSampler model link", old_link, "from node", from_node)

# 2. remove that link; node 53 model input -> new link 16; node 303 output links update
w["links"].pop(ks_model_link)
for n in w["nodes"]:
    if n["id"] == 53:
        for inp in n["inputs"]:
            if inp["name"] == "model":
                inp["link"] = 16
    if n["id"] == from_node:
        for o in n["outputs"]:
            if o["links"]:
                o["links"] = [15 if x == old_link[0] else x for x in o["links"]]

# 3. add ModelSamplingFlux node 58 (shift 1.15)
lora_node = [n for n in w["nodes"] if n["id"] == from_node][0]
px, py = lora_node["pos"]
new_node = {
    "id": 58, "type": "ModelSamplingFlux",
    "pos": [px, py - 120], "size": [270, 46],
    "flags": {}, "order": 30, "mode": 0,
    "inputs": [{"name": "model", "type": "MODEL", "link": 15}],
    "outputs": [{"name": "MODEL", "type": "MODEL", "links": [16]}],
    "properties": {"Node name for S&R": "ModelSamplingFlux"},
    "widgets_values": [1.15],
}
w["nodes"].append(new_node)
w["links"].append([15, from_node, 0, 58, 0, "MODEL"])
w["links"].append([16, 58, 0, 53, 0, "MODEL"])

# 4. official turbo settings: 8 steps, cfg 0
for n in w["nodes"]:
    if n["id"] == 53:
        n["widgets_values"] = [42, "randomize", 8, 0, "euler", "simple", 1]
    if n["id"] == 29:
        n["widgets_values"] = ["krea2_mu_test"]

with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out, "nodes:", len(w["nodes"]), "links:", len(w["links"]))
