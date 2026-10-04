import json, shutil, os

A_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
B_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_B_setup.json"
B_BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_intro_B_setup.json.pre_motion_context.bak"

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

# ---------- A: just fix the stale last_link_id (link 303 already added, valid) ----------
A = load(A_PATH)
a_max = max_link_id(A)
A["last_link_id"] = a_max
save(A_PATH, A)
print("A: last_link_id set to", a_max)

# ---------- B: restore from backup, re-wire with correct link ids ----------
shutil.copy(B_BAK, B_PATH)
B = load(B_PATH)
for nid in (125, 126, 136, 119, 122, 121, 130):
    find_node(B, nid)

B["last_node_id"] = max(B.get("last_node_id", 0), 163)
B["nodes"].append({
    "id": 161, "type": "MiniMaxH3MotionContextLoadLatent",
    "pos": [300, 5750], "size": [340, 80], "flags": {}, "order": 98, "mode": 0,
    "inputs": [],
    "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None}],
    "properties": {"Node name for S&R": "MiniMaxH3MotionContextLoadLatent"},
    "widgets_values": ["h3_context", 1]
})
B["nodes"].append({
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
B["nodes"].append({
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

# remove old direct links
remove_link(B, 270)   # 136 positive -> 126 conditioning (now via 162)
remove_link(B, 258)   # 122 IMAGE -> 130 images (now via 163)
remove_link(B, 259)   # 121 AUDIO -> 130 audio (now via 163)

# new links: ids start ABOVE the real max (305 = 150->126 MODEL, must stay intact)
lid = max_link_id(B)  # 305
def nl():
    global lid
    lid += 1
    return lid

add_link(B, 136, 0, 162, 0, "CONDITIONING", nl())  # ref2va positive -> MC conditioning
add_link(B, 162, 0, 126, 1, "CONDITIONING", nl())  # MC conditioning -> BasicGuider
add_link(B, 136, 1, 162, 2, "LATENT", nl())       # ref2va target latent -> MC latent
add_link(B, 119, 0, 162, 1, "VAE", nl())          # video VAE -> MC vae
add_link(B, 161, 0, 162, 4, "LATENT", nl())       # LoadLatent -> MC context_latent
add_link(B, 162, 1, 163, 2, "INT", nl())         # MC trim_frames -> Trim
add_link(B, 122, 0, 163, 0, "IMAGE", nl())       # VAEDecode IMAGE -> Trim images
add_link(B, 121, 0, 163, 1, "AUDIO", nl())       # VAEDecodeAudio AUDIO -> Trim audio
add_link(B, 163, 0, 130, 0, "IMAGE", nl())       # Trim images -> CreateVideo
add_link(B, 163, 1, 130, 1, "AUDIO", nl())       # Trim audio -> CreateVideo

B["last_link_id"] = lid
save(B_PATH, B)
print("B: restored + rewired, links 306..%d, last_link_id=%d" % (lid, lid))
