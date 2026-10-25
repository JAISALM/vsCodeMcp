import json

BASE = {
    "id": "test-108", "revision": 0, "last_node_id": 108, "last_link_id": 0,
    "links": [],
}

def node_with_inputs(named):
    n = {
        "id": 108, "type": "UNETLoader", "pos": [0, 0], "size": [330, 60],
        "flags": {}, "order": 0, "mode": 0,
        "inputs": [
            {"localized_name": "unet_name", "name": "unet_name", "type": "COMBO", "widget": {"name": "unet_name"}, "link": None},
            {"localized_name": "weight_dtype", "name": "weight_dtype", "type": "COMBO", "widget": {"name": "weight_dtype"}, "link": None},
        ],
        "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": None}],
        "properties": {"Node name for S&R": "UnetLoaderGGUF"},
        "widgets_values": ["minimax_h3_fl2va_pruned_int8_convrot.safetensors", "default"],
    }
    if named:
        n["widgets_values_named"] = {"unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "weight_dtype": "default"}
    return n

# B: positional only (no named dict)
b = dict(BASE)
b["nodes"] = [node_with_inputs(False)]
json.dump(b, open(r"D:\models\vsCodeMcp\data\test_108_B.json", "w", encoding="utf-8"))

# C: positional only + S&R property = UNETLoader
c = dict(BASE)
nc = node_with_inputs(False)
nc["properties"] = {"Node name for S&R": "UNETLoader"}
c["nodes"] = [nc]
json.dump(c, open(r"D:\models\vsCodeMcp\data\test_108_C.json", "w", encoding="utf-8"))

# D: no inputs array at all + no named (original template shape)
d = dict(BASE)
nd = {
    "id": 108, "type": "UNETLoader", "pos": [0, 0], "size": [330, 60],
    "flags": {}, "order": 0, "mode": 0,
    "inputs": [],
    "outputs": [{"name": "MODEL", "type": "MODEL", "links": None}],
    "widgets_values": ["minimax_h3_fl2va_pruned_int8_convrot.safetensors", "default"],
}
d["nodes"] = [nd]
json.dump(d, open(r"D:\models\vsCodeMcp\data\test_108_D.json", "w", encoding="utf-8"))
print("wrote B, C, D")
