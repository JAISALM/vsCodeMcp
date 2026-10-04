import json, shutil, os

D_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json"
BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_intro_D_reverse.json.pre_motion_context.bak"

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)
def save(p, wf):
    with open(p, "w", encoding="utf-8") as f: json.dump(wf, f, ensure_ascii=False)
def find_node(wf, nid):
    for n in wf["nodes"]:
        if n["id"] == nid: return n
    raise KeyError("node %s not found" % nid)
def max_link_id(wf):
    m = 0
    for l in wf.get("links", []):
        if isinstance(l, list) and l and isinstance(l[0], int):
            m = max(m, l[0])
    return m
def set_out_link(wf, node_id, slot, lid):
    node = find_node(wf, node_id)
    links = node["outputs"][slot]["links"]
    if links is None: node["outputs"][slot]["links"] = links = []
    if lid not in links: links.append(lid)
def set_in_link(wf, node_id, slot, lid):
    find_node(wf, node_id)["inputs"][slot]["link"] = lid
def remove_link(wf, lid):
    wf["links"] = [l for l in wf["links"] if not (isinstance(l, list) and l and l[0] == lid)]
    for n in wf["nodes"]:
        for o in n["outputs"]:
            if lid in (o["links"] or []): o["links"].remove(lid)
        for i in n["inputs"]:
            if i.get("link") == lid: i["link"] = None
def add_link(wf, fn, fs, tn, ts, ltype, lid):
    wf["links"].append([lid, fn, fs, tn, ts, ltype])
    set_out_link(wf, fn, fs, lid); set_in_link(wf, tn, ts, lid)
def has_node(wf, nid):
    return any(n["id"] == nid for n in wf["nodes"])

D = load(D_PATH)
shutil.copy(D_PATH, BAK)
for nid in (125, 126, 136, 119, 122, 121, 130):
    find_node(D, nid)

if not has_node(D, 162):
    D["last_node_id"] = max(D.get("last_node_id", 0), 164)
    D["nodes"].append({
        "id": 161, "type": "MiniMaxH3MotionContextLoadLatent",
        "pos": [300, 5750], "size": [340, 80], "flags": {}, "order": 98, "mode": 0,
        "inputs": [],
        "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None}],
        "properties": {"Node name for S&R": "MiniMaxH3MotionContextLoadLatent"},
        "widgets_values": ["h3_context", 3]
    })
    D["nodes"].append({
        "id": 162, "type": "MiniMaxH3MotionContext",
        "pos": [650, 5700], "size": [360, 220], "flags": {}, "order": 97, "mode": 0,
        "inputs": [
            {"localized_name": "conditioning", "name": "conditioning", "type": "CONDITIONING", "link": None},
            {"localized_name": "vae", "name": "vae", "type": "VAE", "link": None},
            {"localized_name": "latent", "name": "latent", "type": "LATENT", "link": None},
            {"localized_name": "context_frames", "name": "context_frames", "type": "IMAGE", "link": None},
            {"localized_name": "context_latent", "name": "context_latent", "type": "LATENT", "link": None},
            {"localized_name": "audio_vae", "name": "audio_vae", "type": "VAE", "link": None},
            {"localized_name": "context_audio", "name": "context_audio", "type": "AUDIO", "link": None},
        ],
        "outputs": [
            {"localized_name": "conditioning", "name": "conditioning", "type": "CONDITIONING", "links": None},
            {"localized_name": "trim_frames", "name": "trim_frames", "type": "INT", "links": None},
        ],
        "properties": {"Node name for S&R": "MiniMaxH3MotionContext"},
        "widgets_values": ["22", 24]
    })
    D["nodes"].append({
        "id": 163, "type": "MiniMaxH3MotionContextTrim",
        "pos": [1050, 5700], "size": [340, 140], "flags": {}, "order": 96, "mode": 0,
        "inputs": [
            {"localized_name": "images", "name": "images", "type": "IMAGE", "link": None},
            {"localized_name": "audio", "name": "audio", "type": "AUDIO", "link": None},
            {"localized_name": "trim_frames", "name": "trim_frames", "type": "INT", "link": None},
        ],
        "outputs": [
            {"localized_name": "images", "name": "images", "type": "IMAGE", "links": None},
            {"localized_name": "audio", "name": "audio", "type": "AUDIO", "links": None},
        ],
        "properties": {"Node name for S&R": "MiniMaxH3MotionContextTrim"},
        "widgets_values": [0, 24, True]
    })
    D["nodes"].append({
        "id": 164, "type": "MiniMaxH3MotionContextSaveLatent",
        "pos": [300, 5850], "size": [340, 100], "flags": {}, "order": 95, "mode": 0,
        "inputs": [{"localized_name": "latent", "name": "latent", "type": "LATENT", "link": None}],
        "outputs": [{"localized_name": "latent_path", "name": "latent_path", "type": "STRING", "links": None}],
        "properties": {"Node name for S&R": "MiniMaxH3MotionContextSaveLatent"},
        "widgets_values": ["h3_context/clip", 4]
    })
    remove_link(D, 270); remove_link(D, 258); remove_link(D, 259)
    lid = [max_link_id(D)]
    def nl():
        lid[0] += 1
        return lid[0]
    add_link(D, 136, 0, 162, 0, "CONDITIONING", nl())
    add_link(D, 162, 0, 126, 1, "CONDITIONING", nl())
    add_link(D, 136, 1, 162, 2, "LATENT", nl())
    add_link(D, 119, 0, 162, 1, "VAE", nl())
    add_link(D, 161, 0, 162, 4, "LATENT", nl())
    add_link(D, 162, 1, 163, 2, "INT", nl())
    add_link(D, 122, 0, 163, 0, "IMAGE", nl())
    add_link(D, 121, 0, 163, 1, "AUDIO", nl())
    add_link(D, 163, 0, 130, 0, "IMAGE", nl())
    add_link(D, 163, 1, 130, 1, "AUDIO", nl())
    add_link(D, 125, 0, 164, 0, "LATENT", nl())
    D["last_link_id"] = lid[0]
    save(D_PATH, D)
    print("D: wired LoadLatent(clip 3) + MotionContext + Trim + SaveLatent(clip 4), links up to %d" % lid[0])
else:
    print("D: continuity nodes already present")
