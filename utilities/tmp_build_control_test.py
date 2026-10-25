import json, io

base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_mu_test.json"
out  = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_control_test.json"

w = json.load(open(base, encoding="utf-8"))
nodes = {n["id"]: n for n in w["nodes"]}

POS_A = ("candid close-up photograph of a 26-year-old young Malayali man, warm medium-brown natural skin "
"with visible pores, round youthful face, medium-length wavy dark hair worn down, short patchy beard, "
"plain dark t-shirt. Soft window light. 35mm film photograph, natural skin texture, muted color grade.")
POS_B = "jeskvman, " + POS_A
NEG = "cartoon, illustration, painting, 3d render, cgi, deformed face, bad eyes, extra fingers, watermark, text"

keep_ids = {55, 56, 57, 82, 58, 53, 54, 29, 300, 301, 303}
w["nodes"] = [n for n in w["nodes"] if n["id"] in keep_ids]

import copy
def clone(src_id, new_id, dy, dx):
    n = copy.deepcopy(nodes[src_id])
    n["id"] = new_id
    n["pos"] = [n["pos"][0] + dx, n["pos"][1] + dy]
    for i in n.get("inputs", []): i["link"] = None
    for o in n.get("outputs", []): o["links"] = []
    w["nodes"].append(n)

clone(58, 59, 180, 600)
clone(53, 63, 180, 600)
clone(54, 64, 180, 600)
clone(29, 65, 180, 600)
clone(300, 304, 180, 600)
clone(301, 305, 180, 600)
clone(82, 83, 180, 600)

by_id = {n["id"]: n for n in w["nodes"]}
by_id[53]["widgets_values"] = [42, "fixed", 8, 0, "euler", "simple", 1]
by_id[63]["widgets_values"] = [42, "fixed", 8, 0, "euler", "simple", 1]
by_id[29]["widgets_values"] = ["krea2_bare_A"]
by_id[65]["widgets_values"] = ["krea2_lora_B"]
by_id[300]["widgets_values"] = [POS_A]
by_id[301]["widgets_values"] = [NEG]
by_id[304]["widgets_values"] = [POS_B]
by_id[305]["widgets_values"] = [NEG]
by_id[83]["widgets_values"] = [1920, 1080, 1]

links = [
    [1, 55, 0, 58, 0, "MODEL"],
    [2, 58, 0, 53, 0, "MODEL"],
    [3, 56, 0, 300, 0, "CLIP"],
    [4, 56, 0, 301, 0, "CLIP"],
    [5, 300, 0, 53, 1, "CONDITIONING"],
    [6, 301, 0, 53, 2, "CONDITIONING"],
    [7, 82, 0, 53, 3, "LATENT"],
    [8, 53, 0, 54, 0, "LATENT"],
    [9, 57, 0, 54, 1, "VAE"],
    [10, 54, 0, 29, 0, "IMAGE"],
    [11, 55, 0, 303, 0, "MODEL"],
    [12, 303, 0, 59, 0, "MODEL"],
    [13, 59, 0, 63, 0, "MODEL"],
    [14, 56, 0, 304, 0, "CLIP"],
    [15, 56, 0, 305, 0, "CLIP"],
    [16, 304, 0, 63, 1, "CONDITIONING"],
    [17, 305, 0, 63, 2, "CONDITIONING"],
    [18, 83, 0, 63, 3, "LATENT"],
    [19, 63, 0, 64, 0, "LATENT"],
    [20, 57, 0, 64, 1, "VAE"],
    [21, 64, 0, 65, 0, "IMAGE"],
]
w["links"] = links

# reset then assign by SLOT INDEX (the native rule)
for n in w["nodes"]:
    for i in n.get("inputs", []): i["link"] = None
    for o in n.get("outputs", []): o["links"] = []
for L in links:
    lid, fn, fs, tn, ts, _ = L
    for n in w["nodes"]:
        if n["id"] == fn and len(n["outputs"]) > fs:
            o = n["outputs"][fs]
            if not o["links"]: o["links"] = []
            if lid not in o["links"]: o["links"].append(lid)
        if n["id"] == tn and len(n["inputs"]) > ts:
            n["inputs"][ts]["link"] = lid

# sanity: print input link fields for the critical nodes
for nid in (53, 54, 63, 64, 300, 301):
    n = by_id[nid]
    print(nid, n["type"], [ (i["name"], i["link"]) for i in n.get("inputs", []) ])

with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out)
