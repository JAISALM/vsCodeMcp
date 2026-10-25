import json, io, copy

src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json"
arch = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows_archive\2026-10-18\krea2_t2i_character.json"
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_realism_2mp.json"

sw = json.load(open(src, encoding="utf-8"))
aw = json.load(open(arch, encoding="utf-8"))
snodes = {n["id"]: n for n in sw["nodes"]}
prompts = list(snodes[200]["widgets_values"])
assert len(prompts) == 6
neg = next(n for n in aw["nodes"] if n["type"] == "CLIPTextEncode" and n["widgets_values"][0].startswith("plastic"))["widgets_values"][0]

# keep shared nodes only
keep = [n for n in sw["nodes"] if n["id"] in (55, 56, 57, 96, 97, 82, 301)]
sn82 = next(n for n in keep if n["id"] == 82)
sn82["widgets_values"] = [1152, 2048, 1]
sn301 = next(n for n in keep if n["id"] == 301)
sn301["widgets_values"] = [neg]

enc_proto = snodes[301]
ks_proto = snodes[53]
vd_proto = snodes[54]
fin_proto = snodes[302]
sv_proto = snodes[29]

new = []
for i in range(6):
    y = 40 + i*190
    enc = copy.deepcopy(enc_proto); enc["id"] = 401+i; enc["type"] = "CLIPTextEncode"; enc["pos"] = [760, y]
    enc["widgets_values"] = [prompts[i]]
    ks = copy.deepcopy(ks_proto); ks["id"] = 407+i; ks["pos"] = [1120, y]
    ks["widgets_values"] = [42+i, "randomize", 10, 1, "euler", "simple", 1]
    vd = copy.deepcopy(vd_proto); vd["id"] = 413+i; vd["pos"] = [1480, y]
    fin = copy.deepcopy(fin_proto); fin["id"] = 419+i; fin["pos"] = [1480, y+140]; fin["widgets_values"] = [1.0, 0.6]
    sv = copy.deepcopy(sv_proto); sv["id"] = 425+i; sv["pos"] = [1700, y]
    sv["widgets_values"] = ["krea2_realism_2mp_%d" % (i+1)]
    for n in (enc, ks, vd, fin, sv):
        n["inputs"] = [{**x, "link": None} for x in n["inputs"]]
        n["outputs"] = [{**x, "links": None} for x in n["outputs"]]
    new.extend([enc, ks, vd, fin, sv])

allnodes = keep + new
nodeset = {n["id"]: n for n in allnodes}

links = []
lid = 500
def L(frm, fs, to, ts, t):
    global lid
    lid += 1
    links.append([lid, frm, fs, to, ts, t])

L(55, 0, 96, 0, "MODEL")
L(96, 0, 97, 0, "MODEL")
L(56, 0, 301, 0, "CLIP")
for i in range(6):
    e, k, v, f, s = 401+i, 407+i, 413+i, 419+i, 425+i
    L(56, 0, e, 0, "CLIP")
    L(97, 0, k, 0, "MODEL")
    L(e, 0, k, 1, "CONDITIONING")
    L(301, 0, k, 2, "CONDITIONING")
    L(82, 0, k, 3, "LATENT")
    L(k, 0, v, 0, "LATENT")
    L(57, 0, v, 1, "VAE")
    L(v, 0, f, 0, "IMAGE")
    L(f, 0, s, 0, "IMAGE")

# assign link fields by slot index, for every node
for n in allnodes:
    for j, inp in enumerate(n["inputs"]):
        inp["link"] = next((lk[0] for lk in links if lk[3] == n["id"] and lk[4] == j), None)
    for o in n["outputs"]:
        o["links"] = [lk[0] for lk in links if lk[1] == n["id"]] or None

w = copy.deepcopy(sw)
w["nodes"] = allnodes
w["links"] = links
w["last_node_id"] = 430
w["last_link_id"] = lid

with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out)
print("nodes:", len(allnodes), "links:", len(links))
for i in range(6):
    e = nodeset[401+i]
    print("branch%d: prompt=%s... ks=%d save=%s" % (i+1, e["widgets_values"][0][:40], 407+i, nodeset[425+i]["widgets_values"][0]))
