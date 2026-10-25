import json, io
p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_cine_max.json"
w = json.load(open(p, encoding="utf-8"))
w["nodes"] = [n for n in w["nodes"] if n["id"] not in (54, 83)]
for n in w["nodes"]:
    if n["id"] == 98:
        n["type"] = "Krea2T-Enhancer-Advanced"

ksel = {"id": 100, "type": "KSamplerSelect", "pos": [2560, 1120],
        "inputs": [],
        "outputs": [{"name": "SAMPLER", "localized_name": "SAMPLER", "type": "SAMPLER", "links": None}],
        "widgets_values": ["euler"]}
w["nodes"].append(ksel)
w["last_node_id"] = max(w["last_node_id"], 843)

# drop stale links (to removed nodes)
w["links"] = [L for L in w["links"] if L[3] not in (54, 83) and L[1] not in (54, 83)]
lid = max(L[0] for L in w["links"])
def L(frm, fs, to, ts, t):
    global lid
    lid += 1
    w["links"].append([lid, frm, fs, to, ts, t])

for i in range(3):
    sm = 530+i
    L(79, 0, sm, 0, "MODEL")
    L(100, 0, sm, 3, "SAMPLER")

# reassign link fields
for n in w["nodes"]:
    for j, inp in enumerate(n["inputs"]):
        inp["link"] = next((lk[0] for lk in w["links"] if lk[3] == n["id"] and lk[4] == j), None)
    for o in n["outputs"]:
        o["links"] = [lk[0] for lk in w["links"] if lk[1] == n["id"]] or None
w["last_link_id"] = lid

with io.open(p, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("patched: nodes", len(w["nodes"]), "links", len(w["links"]))
