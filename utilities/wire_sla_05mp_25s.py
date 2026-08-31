import json, shutil, os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json"
BAK = WF + ".pre_sla.bak"

# Backup
if not os.path.exists(BAK):
    shutil.copy(WF, BAK)
    print("backup ->", BAK)

d = json.load(open(WF, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

# 1) ResolutionSelector (115) -> 0.5 MP
n115 = nodes[115]
n115["widgets_values"] = ["16:9 (Widescreen)", 0.5, 32]
if "widgets_values_named" in n115:
    n115["widgets_values_named"]["megapixels"] = 0.5
print("115 ->", n115["widgets_values"])

# 2) length (132) -> 25s
n132 = nodes[132]
n132["widgets_values"] = [25]
if "widgets_values_named" in n132:
    n132["widgets_values_named"]["value"] = 25
print("132 ->", n132["widgets_values"])

# 3) Insert H3 SLA node (150) between LoRA(146) and BasicGuider(126)
SLA_ID = 150
if SLA_ID in nodes:
    print("SLA node already present, skipping insert")
else:
    sla = {
        "id": SLA_ID,
        "type": "H3SLAAttention",
        "pos": [-946.0, 5100.0],
        "size": [410, 202],
        "flags": {},
        "order": 16,
        "mode": 0,
        "inputs": [
            {"name": "model", "type": "MODEL", "link": 288}
        ],
        "outputs": [
            {"name": "model", "type": "MODEL", "links": [305]}
        ],
        "properties": {"Node name for S&R": "H3SLAAttention"},
        "widgets_values": [0.90, "32", 8192, 1, True, True, "0", "comfy_kitchen", True, False, False],
        "widgets_values_named": {
            "sparsity_ratio": 0.90,
            "block_size": "32",
            "min_seq_len": 8192,
            "dense_last_steps": 1,
            "protect_audio": True,
            "enabled": True,
            "dense_steps": "0",
            "dense_backend": "comfy_kitchen",
            "disable_fp16_accum": True,
            "stabilize_motion": False,
            "reference_protection": False
        }
    }
    d["nodes"].append(sla)
    print("added SLA node 150")

# 4) Rewire: link 288 (was 146->126) becomes 146->150; add link 305 (150->126)
links = d["links"]
# find link 288
for i, l in enumerate(links):
    if l[0] == 288:
        links[i] = [288, 146, 0, SLA_ID, 0, "MODEL"]
        print("rewired 288 -> 146->150")
        break
# add link 305 if not present
if not any(l[0] == 305 for l in links):
    links.append([305, SLA_ID, 0, 126, 0, "MODEL"])
    print("added link 305 -> 150->126")

# 5) Update BasicGuider(126) input slot 0 link: 288 -> 305
n126 = nodes[126]
for inp in n126.get("inputs", []):
    if inp.get("link") == 288:
        inp["link"] = 305
        print("126 input link 288 -> 305")

json.dump(d, open(WF, "w", encoding="utf-8"), indent=4)
print("saved", WF)
print("total nodes:", len(d["nodes"]), "total links:", len(links))
