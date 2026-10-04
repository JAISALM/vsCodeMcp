import json, shutil, os

BAK_DIR = r"d:\models\vsCodeMcp\workflow_backups"
os.makedirs(BAK_DIR, exist_ok=True)
WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

def load(name):
    with open(os.path.join(WF_DIR, name), "r", encoding="utf-8") as f: return json.load(f)
def save(name, wf):
    with open(os.path.join(WF_DIR, name), "w", encoding="utf-8") as f: json.dump(wf, f, ensure_ascii=False)
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

def wire_continuity(name, load_clip, save_clip, backup_tag):
    """load_clip: clip_index for LoadLatent (0 = none). save_clip: clip_index for SaveLatent (0 = none)."""
    wf = load(name)
    shutil.copy(os.path.join(WF_DIR, name), os.path.join(BAK_DIR, name + "." + backup_tag + ".bak"))
    for nid in (125, 126, 136, 119, 122, 121, 130):
        find_node(wf, nid)
    changed = False

    # LoadLatent + MotionContext + Trim (if load_clip > 0)
    if load_clip > 0 and not has_node(wf, 162):
        wf["last_node_id"] = max(wf.get("last_node_id", 0), 163)
        wf["nodes"].append({
            "id": 161, "type": "MiniMaxH3MotionContextLoadLatent",
            "pos": [300, 5750], "size": [340, 80], "flags": {}, "order": 98, "mode": 0,
            "inputs": [],
            "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None}],
            "properties": {"Node name for S&R": "MiniMaxH3MotionContextLoadLatent"},
            "widgets_values": ["h3_context", load_clip]
        })
        wf["nodes"].append({
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
        wf["nodes"].append({
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
        # remove old direct links (136 positive->126, 122->130, 121->130)
        remove_link(wf, 270); remove_link(wf, 258); remove_link(wf, 259)
        lid = [max_link_id(wf)]
        def nl():
            lid[0] += 1
            return lid[0]
        add_link(wf, 136, 0, 162, 0, "CONDITIONING", nl())
        add_link(wf, 162, 0, 126, 1, "CONDITIONING", nl())
        add_link(wf, 136, 1, 162, 2, "LATENT", nl())
        add_link(wf, 119, 0, 162, 1, "VAE", nl())
        add_link(wf, 161, 0, 162, 4, "LATENT", nl())
        add_link(wf, 162, 1, 163, 2, "INT", nl())
        add_link(wf, 122, 0, 163, 0, "IMAGE", nl())
        add_link(wf, 121, 0, 163, 1, "AUDIO", nl())
        add_link(wf, 163, 0, 130, 0, "IMAGE", nl())
        add_link(wf, 163, 1, 130, 1, "AUDIO", nl())
        wf["last_link_id"] = lid[0]
        changed = True
        print("%s: added LoadLatent(clip %d) + MotionContext + Trim" % (name, load_clip))
    elif load_clip > 0:
        print("%s: continuity nodes already present" % name)

    # SaveLatent (if save_clip > 0)
    if save_clip > 0 and not has_node(wf, 164):
        wf["last_node_id"] = max(wf.get("last_node_id", 0), 164)
        wf["nodes"].append({
            "id": 164, "type": "MiniMaxH3MotionContextSaveLatent",
            "pos": [300, 5850], "size": [340, 100], "flags": {}, "order": 95, "mode": 0,
            "inputs": [{"localized_name": "latent", "name": "latent", "type": "LATENT", "link": None}],
            "outputs": [{"localized_name": "latent_path", "name": "latent_path", "type": "STRING", "links": None}],
            "properties": {"Node name for S&R": "MiniMaxH3MotionContextSaveLatent"},
            "widgets_values": ["h3_context/clip", save_clip]
        })
        lid = max_link_id(wf) + 1
        add_link(wf, 125, 0, 164, 0, "LATENT", lid)
        wf["last_link_id"] = lid
        changed = True
        print("%s: added SaveLatent(clip %d)" % (name, save_clip))
    elif save_clip > 0:
        print("%s: SaveLatent already present" % name)

    if changed:
        save(name, wf)
    return changed

# B: load clip 1 (A's latent), save clip 2
wire_continuity("jaisal_intro_B_setup.json", load_clip=1, save_clip=2, backup_tag="reapply_mc")
# C: load clip 2 (B's latent), save clip 3
wire_continuity("jaisal_intro_C_starting_2ref.json", load_clip=2, save_clip=3, backup_tag="reapply_mc")
print("DONE.")
