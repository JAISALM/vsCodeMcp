import json, shutil, os

C_PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_starting_2ref.json"
BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_intro_C_starting_2ref.json.pre_save_latent3.bak"

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

C = load(C_PATH)
shutil.copy(C_PATH, BAK)
if any(n["id"] == 164 for n in C["nodes"]):
    print("C: SaveLatent 164 already present, skipping")
else:
    C["last_node_id"] = max(C.get("last_node_id", 0), 164)
    C["nodes"].append({
        "id": 164, "type": "MiniMaxH3MotionContextSaveLatent",
        "pos": [300, 5850], "size": [340, 100], "flags": {}, "order": 95, "mode": 0,
        "inputs": [{"localized_name": "latent", "name": "latent", "type": "LATENT", "link": None}],
        "outputs": [{"localized_name": "latent_path", "name": "latent_path", "type": "STRING", "links": None}],
        "properties": {"Node name for S&R": "MiniMaxH3MotionContextSaveLatent"},
        "widgets_values": ["h3_context/clip", 3]
    })
    lid = max_link_id(C) + 1
    C["links"].append([lid, 125, 0, 164, 0, "LATENT"])
    set_out_link(C, 125, 0, lid)
    set_in_link(C, 164, 0, lid)
    C["last_link_id"] = lid
    save(C_PATH, C)
    print("C: added SaveLatent node 164 (clip_index=3), link %d" % lid)
