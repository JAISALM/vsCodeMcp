import json, shutil, os

A_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
B_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_B_setup.json"
BAK_DIR = r"d:\models\vsCodeMcp\workflow_backups"
os.makedirs(BAK_DIR, exist_ok=True)

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)
def save(p, wf):
    with open(p, "w", encoding="utf-8") as f: json.dump(wf, f, ensure_ascii=False)
def find_node(wf, nid):
    for n in wf["nodes"]:
        if n["id"] == nid: return n
    raise KeyError("node %s not found" % nid)
def next_link_id(wf):
    return wf.get("last_link_id", 0) + 1
def set_out_link(wf, node_id, slot, lid):
    node = find_node(wf, node_id)
    links = node["outputs"][slot]["links"]
    if links is None: node["outputs"][slot]["links"] = links = []
    if lid not in links: links.append(lid)
def set_in_link(wf, node_id, slot, lid):
    find_node(wf, node_id)["inputs"][slot]["link"] = lid
def remove_link(wf, lid):
    wf["links"] = [l for l in wf["links"] if l[0] != lid]
    for n in wf["nodes"]:
        for o in n["outputs"]:
            if lid in (o["links"] or []): o["links"].remove(lid)
        for i in n["inputs"]:
            if i.get("link") == lid: i["link"] = None
def add_link(wf, fn, fs, tn, ts, ltype):
    lid = next_link_id(wf); wf["last_link_id"] = lid
    wf["links"].append([lid, fn, fs, tn, ts, ltype])
    set_out_link(wf, fn, fs, lid); set_in_link(wf, tn, ts, lid)
    return lid
def has_node(wf, nid):
    return any(n["id"] == nid for n in wf["nodes"])

# ---------------- A: add SaveLatent (saves A's AV latent -> clip_00001.safetensors) ----------------
A = load(A_PATH)
shutil.copy(A_PATH, os.path.join(BAK_DIR, "jaisal_intro_A_walkin.json.pre_motion_context.bak"))
if not has_node(A, 160):
    A["last_node_id"] = max(A.get("last_node_id", 0), 163)
    A["nodes"].append({
        "id": 160, "type": "MiniMaxH3MotionContextSaveLatent",
        "pos": [300, 5650], "size": [340, 100], "flags": {}, "order": 99, "mode": 0,
        "inputs": [{"localized_name": "latent", "name": "latent", "type": "LATENT", "link": None}],
        "outputs": [{"localized_name": "latent_path", "name": "latent_path", "type": "STRING", "links": None}],
        "properties": {"Node name for S&R": "MiniMaxH3MotionContextSaveLatent"},
        "widgets_values": ["h3_context/clip", 1]
    })
    add_link(A, 125, 0, 160, 0, "LATENT")   # A sampler output -> SaveLatent
    print("A: added SaveLatent node 160 (clip_index=1) wired to sampler 125")
else:
    print("A: SaveLatent 160 already present, skipping")
save(A_PATH, A)

# ---------------- B: add LoadLatent + MotionContext + Trim ----------------
B = load(B_PATH)
shutil.copy(B_PATH, os.path.join(BAK_DIR, "jaisal_intro_B_setup.json.pre_motion_context.bak"))
for nid in (125, 126, 136, 119, 122, 121, 130):
    find_node(B, nid)  # assert present

if not has_node(B, 161):
    B["last_node_id"] = max(B.get("last_node_id", 0), 163)
    # 161 LoadLatent (loads A's latent, clip_index=1)
    B["nodes"].append({
        "id": 161, "type": "MiniMaxH3MotionContextLoadLatent",
        "pos": [300, 5750], "size": [340, 80], "flags": {}, "order": 98, "mode": 0,
        "inputs": [],
        "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None}],
        "properties": {"Node name for S&R": "MiniMaxH3MotionContextLoadLatent"},
        "widgets_values": ["h3_context", 1]
    })
    # 162 MotionContext (pins A's tail into B's conditioning)
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
    # 163 Trim (removes the pinned head from B's decoded clip)
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
    # --- rewiring: remove old direct links first ---
    remove_link(B, 270)   # 136 positive -> 126 conditioning  (now via 162)
    remove_link(B, 258)   # 122 IMAGE -> 130 images           (now via 163)
    remove_link(B, 259)   # 121 AUDIO -> 130 audio           (now via 163)
    # --- new links ---
    add_link(B, 136, 0, 162, 0, "CONDITIONING")  # ref2va positive -> MC conditioning
    add_link(B, 162, 0, 126, 1, "CONDITIONING")  # MC conditioning -> BasicGuider
    add_link(B, 136, 1, 162, 2, "LATENT")       # ref2va target latent -> MC latent
    add_link(B, 119, 0, 162, 1, "VAE")          # video VAE -> MC vae
    add_link(B, 161, 0, 162, 4, "LATENT")       # LoadLatent -> MC context_latent
    add_link(B, 162, 1, 163, 2, "INT")         # MC trim_frames -> Trim
    add_link(B, 122, 0, 163, 0, "IMAGE")       # VAEDecode IMAGE -> Trim images
    add_link(B, 121, 0, 163, 1, "AUDIO")       # VAEDecodeAudio AUDIO -> Trim audio
    add_link(B, 163, 0, 130, 0, "IMAGE")       # Trim images -> CreateVideo
    add_link(B, 163, 1, 130, 1, "AUDIO")       # Trim audio -> CreateVideo
    print("B: added LoadLatent 161 + MotionContext 162 + Trim 163, rewired")
else:
    print("B: continuity nodes already present, skipping")
save(B_PATH, B)

print("DONE. Backups in", BAK_DIR)
