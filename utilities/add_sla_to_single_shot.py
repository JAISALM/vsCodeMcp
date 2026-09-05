import json

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
path = WF_DIR + r"\jaisal_single_shot.json"
d = json.load(open(path))
s = d["definitions"]["subgraphs"][0]

# --- 1. Build the SLA node (id 150, inside the subgraph) ---
sla_node = {
    "id": 150,
    "type": "H3SLAAttention",
    "pos": [0, 0],
    "size": [410, 414],
    "flags": {},
    "order": 99,
    "mode": 0,
    "inputs": [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 246},
        {"localized_name": "sparsity_ratio", "name": "sparsity_ratio", "type": "FLOAT", "widget": {"name": "sparsity_ratio"}, "link": None},
        {"localized_name": "block_size", "name": "block_size", "type": "COMBO", "widget": {"name": "block_size"}, "link": None},
        {"localized_name": "min_seq_len", "name": "min_seq_len", "shape": 7, "type": "INT", "widget": {"name": "min_seq_len"}, "link": None},
        {"localized_name": "dense_last_steps", "name": "dense_last_steps", "shape": 7, "type": "INT", "widget": {"name": "dense_last_steps"}, "link": None},
        {"localized_name": "protect_audio", "name": "protect_audio", "shape": 7, "type": "BOOLEAN", "widget": {"name": "protect_audio"}, "link": None},
        {"localized_name": "enabled", "name": "enabled", "shape": 7, "type": "BOOLEAN", "widget": {"name": "enabled"}, "link": None},
        {"localized_name": "dense_steps", "name": "dense_steps", "shape": 7, "type": "STRING", "widget": {"name": "dense_steps"}, "link": None},
        {"localized_name": "dense_backend", "name": "dense_backend", "type": "COMBO", "widget": {"name": "dense_backend"}, "link": None},
        {"localized_name": "disable_fp16_accum", "name": "disable_fp16_accum", "shape": 7, "type": "BOOLEAN", "widget": {"name": "disable_fp16_accum"}, "link": None},
        {"localized_name": "stabilize_motion", "name": "stabilize_motion", "shape": 7, "type": "BOOLEAN", "widget": {"name": "stabilize_motion"}, "link": None},
        {"localized_name": "reference_protection", "name": "reference_protection", "shape": 7, "type": "BOOLEAN", "widget": {"name": "reference_protection"}, "link": None},
    ],
    "outputs": [
        {"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [247, 248]},
    ],
    "properties": {"Node name for S&R": "H3SLAAttention"},
    "widgets_values": [0.9, "32", 8192, 1, True, True, "0", "comfy_kitchen", True, False, False],
}
s["nodes"].append(sla_node)
print("added SLA node 150 to subgraph")

# --- 2. Remove old links 234 (122→9) and 241 (122→16) ---
s["links"] = [l for l in s["links"] if l.get("id") not in (234, 241)]
print("removed old links 234, 241")

# --- 3. Add new links: 122→150 (246), 150→9 (247), 150→16 (248) ---
s["links"].append({"id": 246, "origin_id": 122, "origin_slot": 0, "target_id": 150, "target_slot": 0, "type": "MODEL"})
s["links"].append({"id": 247, "origin_id": 150, "origin_slot": 0, "target_id": 9, "target_slot": 0, "type": "MODEL"})
s["links"].append({"id": 248, "origin_id": 150, "origin_slot": 0, "target_id": 16, "target_slot": 0, "type": "MODEL"})
print("added new links 246 (122→150), 247 (150→9), 248 (150→16)")

json.dump(d, open(path, "w"), indent=1)
print("saved")
