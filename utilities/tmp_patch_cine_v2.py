import json, io, copy

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
for fname in ("krea2_cine_v2.json", "krea2_cine_v2_4mp.json"):
    p = W + "\\" + fname
    w = json.load(open(p, encoding="utf-8"))
    nodes = w["nodes"]
    by_id = {n["id"]: n for n in nodes}
    # add empty negative encode -> zero out
    neg85 = copy.deepcopy(by_id[840])
    neg85["id"] = 85
    neg85["pos"] = [700, 200]
    neg85["widgets_values"] = [""]
    for inp in neg85.get("inputs", []):
        inp["link"] = None
    for o in neg85.get("outputs", []):
        o["links"] = None
    nodes.append(neg85)
    lid = w["last_link_id"]
    def L(frm, fs, to, ts, t):
        global lid
        lid += 1
        w["links"].append([lid, frm, fs, to, ts, t])
    for i in range(3 if fname == "krea2_cine_v2.json" else 1):
        L(56, 0, 840+i, 0, "CLIP")
    L(56, 0, 85, 0, "CLIP")
    L(85, 0, 90, 0, "CONDITIONING")
    for n in nodes:
        for j, inp in enumerate(n.get("inputs", [])):
            inp["link"] = next((lk[0] for lk in w["links"] if lk[3] == n["id"] and lk[4] == j), None)
        for o in n.get("outputs", []):
            o["links"] = [lk[0] for lk in w["links"] if lk[1] == n["id"]] or None
    w["last_link_id"] = lid
    w["last_node_id"] = max(w["last_node_id"], 843)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(w, indent=1))
    print("patched", fname, "nodes:", len(nodes), "links:", len(w["links"]))
