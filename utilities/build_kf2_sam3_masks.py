import json

DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_kf2_sam3_masks.json'

def node(id, ntype, pos, size, inputs, outputs, widgets, title=None):
    n = {"id": id, "type": ntype, "pos": pos, "size": size, "flags": {}, "order": 0, "mode": 0,
         "inputs": inputs, "outputs": outputs, "properties": {"Node name for S&R": ntype},
         "widgets_values": widgets}
    if title:
        n["title"] = title
    return n

def link(id, origin, oslot, target, tslot, ltype):
    return [id, origin, oslot, target, tslot, ltype]

nodes = []
links = []

# 100 LoadImage (original kf2, chair still present)
nodes.append(node(100, "LoadImage", [0, 0], [320, 320],
    [
        {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
        {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
    ],
    [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [1, 2]},
        {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
    ],
    ["kf2_seated_v7.png", "image"]))

# 101 CheckpointLoaderSimple -> SAM3 model
nodes.append(node(101, "CheckpointLoaderSimple", [0, 400], [360, 100],
    [
        {"localized_name": "ckpt_name", "name": "ckpt_name", "type": "COMBO", "widget": {"name": "ckpt_name"}, "link": None},
    ],
    [
        {"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [3, 4]},
        {"localized_name": "CLIP", "name": "CLIP", "type": "CLIP", "links": [5, 6]},
        {"localized_name": "VAE", "name": "VAE", "type": "VAE", "links": None},
    ],
    ["sam3.1_multiplex_fp16.safetensors"]))

# 110 CLIPTextEncode "wooden chair"
nodes.append(node(110, "CLIPTextEncode", [400, 0], [400, 200],
    [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 5},
    ],
    [
        {"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [7]},
    ],
    ["wooden chair"]))

# 111 CLIPTextEncode "wall"
nodes.append(node(111, "CLIPTextEncode", [400, 250], [400, 200],
    [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 6},
    ],
    [
        {"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [8]},
    ],
    ["wall"]))

# 102 SAM3_Detect chair
nodes.append(node(102, "SAM3_Detect", [850, 0], [320, 220],
    [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 3},
        {"localized_name": "image", "name": "image", "type": "IMAGE", "link": 1},
        {"localized_name": "threshold", "name": "threshold", "type": "FLOAT", "widget": {"name": "threshold"}, "link": None},
        {"localized_name": "refine_iterations", "name": "refine_iterations", "type": "INT", "widget": {"name": "refine_iterations"}, "link": None},
        {"localized_name": "individual_masks", "name": "individual_masks", "type": "BOOLEAN", "widget": {"name": "individual_masks"}, "link": None},
        {"localized_name": "conditioning", "name": "conditioning", "type": "CONDITIONING", "link": 7},
    ],
    [
        {"localized_name": "masks", "name": "masks", "type": "MASK", "links": [9]},
        {"localized_name": "bboxes", "name": "bboxes", "type": "BOUNDING_BOX", "links": None},
    ],
    [0.5, 2, False], title="SAM3 chair"))

# 103 SAM3_Detect wall
nodes.append(node(103, "SAM3_Detect", [850, 250], [320, 220],
    [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 4},
        {"localized_name": "image", "name": "image", "type": "IMAGE", "link": 2},
        {"localized_name": "threshold", "name": "threshold", "type": "FLOAT", "widget": {"name": "threshold"}, "link": None},
        {"localized_name": "refine_iterations", "name": "refine_iterations", "type": "INT", "widget": {"name": "refine_iterations"}, "link": None},
        {"localized_name": "individual_masks", "name": "individual_masks", "type": "BOOLEAN", "widget": {"name": "individual_masks"}, "link": None},
        {"localized_name": "conditioning", "name": "conditioning", "type": "CONDITIONING", "link": 8},
    ],
    [
        {"localized_name": "masks", "name": "masks", "type": "MASK", "links": [10]},
        {"localized_name": "bboxes", "name": "bboxes", "type": "BOUNDING_BOX", "links": None},
    ],
    [0.5, 2, False], title="SAM3 wall"))

# 104 MaskToImage (chair)
nodes.append(node(104, "MaskToImage", [1250, 0], [200, 60],
    [
        {"localized_name": "mask", "name": "mask", "type": "MASK", "link": 9},
    ],
    [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [11]},
    ],
    []))

# 106 MaskToImage (wall)
nodes.append(node(106, "MaskToImage", [1250, 250], [200, 60],
    [
        {"localized_name": "mask", "name": "mask", "type": "MASK", "link": 10},
    ],
    [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [12]},
    ],
    []))

# 105 SaveImage chair mask
nodes.append(node(105, "SaveImage", [1500, 0], [300, 200],
    [
        {"localized_name": "images", "name": "images", "type": "IMAGE", "link": 11},
    ],
    [],
    ["jaisal_kf2_mask_chair"]))

# 107 SaveImage wall mask
nodes.append(node(107, "SaveImage", [1500, 250], [300, 200],
    [
        {"localized_name": "images", "name": "images", "type": "IMAGE", "link": 12},
    ],
    [],
    ["jaisal_kf2_mask_wall"]))

links = [
    link(1, 100, 0, 102, 1, "IMAGE"),
    link(2, 100, 0, 103, 1, "IMAGE"),
    link(3, 101, 0, 102, 0, "MODEL"),
    link(4, 101, 0, 103, 0, "MODEL"),
    link(5, 101, 1, 110, 0, "CLIP"),
    link(6, 101, 1, 111, 0, "CLIP"),
    link(7, 110, 0, 102, 5, "CONDITIONING"),
    link(8, 111, 0, 103, 5, "CONDITIONING"),
    link(9, 102, 0, 104, 0, "MASK"),
    link(10, 103, 0, 106, 0, "MASK"),
    link(11, 104, 0, 105, 0, "IMAGE"),
    link(12, 106, 0, 107, 0, "IMAGE"),
]

d = {
    "id": "kf2-sam3-masks", "revision": 0, "last_node_id": 111, "last_link_id": 12,
    "nodes": nodes, "links": links, "groups": [], "config": {}, "extra": {}, "version": 0.4
}
json.dump(d, open(DST, 'w', encoding='utf-8'), ensure_ascii=False)
print("WROTE", DST)
print("nodes:", [n['id'] for n in nodes])
