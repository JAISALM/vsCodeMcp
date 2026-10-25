import json, io, copy

# base: old recipe file (complete chain with prompts)
src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json"
# negative from the archived 2MP file (the one that made the good attached images)
arch = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows_archive\2026-10-18\krea2_t2i_character.json"
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_realism_2mp.json"

w = json.load(open(src, encoding="utf-8"))
aw = json.load(open(arch, encoding="utf-8"))

nodes = {n["id"]: n for n in w["nodes"]}
anodes = {n["id"]: n for n in aw["nodes"]}
prompts = list(nodes[200]["widgets_values"])
assert len(prompts) == 6
neg = anodes[301]["widgets_values"][0]
print("negative:", neg[:80])

# remove old single-branch nodes
for nid in (200, 300, 53, 54, 302, 29):
    del nodes[nid]
w["nodes"] = list(nodes.values())

# change resolution 896x1120 -> 1152x2048
nodes[82]["widgets_values"] = [1152, 2048, 1]
# shared negative encode keeps its text from the archived 2MP run
nodes[301]["widgets_values"] = [neg]

tmpl = {
    "enc": nodes[301],        # CLIPTextEncode shape
    "ks": json.load(open(src, encoding="utf-8"))["nodes"],
}
ks_proto = next(n for n in json.load(open(src, encoding="utf-8"))["nodes"] if n["type"] == "KSampler")
vdec_proto = next(n for n in json.load(open(src, encoding="utf-8"))["nodes"] if n["type"] == "VAEDecode")
fin_proto = next(n for n in json.load(open(src, encoding="utf-8"))["nodes"] if n["type"] == "FameGridColorFinish")
save_proto = next(n for n in json.load(open(src, encoding="utf-8"))["nodes"] if n["type"] == "SaveImage")

new_nodes = []
links = []
lid = 500
def add_link(frm, fs, to, ts, t):
    global lid
    lid += 1
    links.append([lid, frm, fs, to, ts, t])
    return lid

for i in range(6):
    enc_id, ks_id, vd_id, fin_id, sv_id = 401+i, 407+i, 413+i, 419+i, 425+i
    y = 40 + i*190

    enc = copy.deepcopy(ks_proto)
    enc.update({"id": enc_id, "type": "CLIPTextEncode", "pos": [760, y],
                "inputs": copy.deepcopy(nodes[301]["inputs"]),
                "outputs": copy.deepcopy(nodes[301]["outputs"]),
                "widgets_values": [prompts[i]]})
    # clear link fields, assign after
    enc["inputs"] = [{**x, "link": None} for x in enc["inputs"]]
    enc["outputs"] = [{**x, "links": None} for x in enc["outputs"]]
    new_nodes.append(enc)

    ks = copy.deepcopy(ks_proto)
    ks.update({"id": ks_id, "pos": [1120, y], "widgets_values": [42+i, "randomize", 10, 1, "euler", "simple", 1]})
    ks["inputs"] = [{**x, "link": None} for x in ks["inputs"]]
    ks["outputs"] = [{**x, "links": None} for x in ks["outputs"]]
    new_nodes.append(ks)

    vd = copy.deepcopy(vdec_proto)
    vd.update({"id": vd_id, "pos": [1480, y]})
    vd["inputs"] = [{**x, "link": None} for x in vd["inputs"]]
    vd["outputs"] = [{**x, "links": None} for x in vd["outputs"]]
    new_nodes.append(vd)

    fin = copy.deepcopy(fin_proto)
    fin.update({"id": fin_id, "pos": [1480, y+140], "widgets_values": [1.0, 0.6]})
    fin["inputs"] = [{**x, "link": None} for x in fin["inputs"]]
    fin["outputs"] = [{**x, "links": None} for x in fin["outputs"]]
    new_nodes.append(fin)

    sv = copy.deepcopy(save_proto)
    sv.update({"id": sv_id, "pos": [1700, y], "widgets_values": ["krea2_realism_2mp_%d" % (i+1)]})
    sv["inputs"] = [{**x, "link": None} for x in sv["inputs"]]
    sv["outputs"] = [{**x, "links": None} for x in sv["outputs"]]
    new_nodes.append(sv)

    l1 = add_link(56, 0, enc_id, 0, "CLIP")
    l2 = add_link(97, 0, ks_id, 0, "MODEL")
    l3 = add_link(enc_id, 0, ks_id, 1, "CONDITIONING")
    l4 = add_link(301, 0, ks_id, 2, "CONDITIONING")
    l5 = add_link(82, 0, ks_id, 3, "LATENT")
    l6 = add_link(ks_id, 0, vd_id, 0, "LATENT")
    l7 = add_link(57, 0, vd_id, 1, "VAE")
    l8 = add_link(vd_id, 0, fin_id, 0, "IMAGE")
    l9 = add_link(fin_id, 0, sv_id, 0, "IMAGE")

# shared chain links (55->96->97 already in old links? rebuild everything)
links = []
lid = 500
def add_link(frm, fs, to, ts, t):
    global lid
    lid += 1
    links.append([lid, frm, fs, to, ts, t])
    return lid

add_link(55, 0, 96, 0, "MODEL")
add_link(96, 0, 97, 0, "MODEL")
add_link(56, 0, 301, 0, "CLIP")
for i in range(6):
    enc_id, ks_id, vd_id, fin_id, sv_id = 401+i, 407+i, 413+i, 419+i, 425+i
    lmap = {
        enc_id: {0: add_link(56, 0, enc_id, 0, "CLIP")},
        ks_id: {0: add_link(97, 0, ks_id, 0, "MODEL"),
                1: add_link(enc_id, 0, ks_id, 1, "CONDITIONING"),
                2: add_link(301, 0, ks_id, 2, "CONDITIONING"),
                3: add_link(82, 0, ks_id, 3, "LATENT")},
        vd_id: {0: add_link(ks_id, 0, vd_id, 0, "LATENT"),
                1: add_link(57, 0, vd_id, 1, "VAE")},
        fin_id: {0: add_link(vd_id, 0, fin_id, 0, "IMAGE")},
        sv_id: {0: add_link(fin_id, 0, sv_id, 0, "IMAGE")},
    }
    for n in w["nodes"]:
        if n["id"] in lmap:
            for j, inp in enumerate(n["inputs"]):
                inp["link"] = lmap[n["id"]].get(j)
            if n["type"] != "SaveImage":
                n["outputs"][0]["links"] = [l for l in links if l[1] == n["id"]]
    # saveimage outputs: none linked
# reset all link fields on shared nodes then assign
shared_links = {}
for L in links:
    shared_links.setdefault(L[3], {})[L[4]] = L[0]
for n in w["nodes"]:
    if n["id"] in (55, 56, 57, 82, 301, 96, 97):
        for j, inp in enumerate(n["inputs"]):
            inp["link"] = shared_links.get(n["id"], {}).get(j)
        for o in n["outputs"]:
            o["links"] = [L[0] for L in links if L[1] == n["id"]]

# fix output links for new nodes
for n in w["nodes"]:
    if n["id"] >= 401:
        for o in n["outputs"]:
            o["links"] = [L[0] for L in links if L[1] == n["id"]]

w["links"] = links
w["last_node_id"] = 430
w["last_link_id"] = lid

with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out)
print("nodes:", len(w["nodes"]), "links:", len(links))
print("prompt in branch1:", w["nodes"][list(nodes.keys()).index(82)+1]["widgets_values"][0][:60] if False else new_nodes[0]["widgets_values"][0][:60])
