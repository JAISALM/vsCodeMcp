import json

DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_kf2_manual_inpaint.json'

def node(id, ntype, pos, size, inputs, outputs, widgets, title=None):
    n = {"id": id, "type": ntype, "pos": pos, "size": size, "flags": {}, "order": 0, "mode": 0,
         "inputs": inputs, "outputs": outputs, "properties": {"Node name for S&R": ntype},
         "widgets_values": widgets}
    if title:
        n["title"] = title
    return n

def link(id, origin, oslot, target, tslot, ltype):
    return [id, origin, oslot, target, tslot, ltype]

def loadimage(id, pos, filename, img_links, mask_links):
    return node(id, "LoadImage", pos, [320, 320],
        [
            {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
            {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
        ],
        [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": img_links},
            {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": mask_links},
        ],
        [filename, "image"])

nodes = []
# 200 LoadImage = the image to inpaint
nodes.append(loadimage(200, [0, 0], "kf2_seated_v7.png", [1, 2], None))
# 201 LoadImage = YOUR MASK (white = replace). Swap this file for your hand-drawn mask.
nodes.append(loadimage(201, [0, 400], "kf2_mask_combined.png", None, [3]))
# 202 GrowMaskWithBlur = expand + feather the mask edges
nodes.append(node(202, "GrowMaskWithBlur", [400, 400], [300, 200],
    [{"localized_name": "mask", "name": "mask", "type": "MASK", "link": 3}],
    [{"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": [4, 5, 16]}],
    [45, 0, True, False, 31, 1, 1, False], title="grow + feather mask"))
# 203 VAEEncode (image + mask -> latent)
nodes.append(node(203, "VAEEncode", [750, 0], [220, 100],
    [
        {"localized_name": "pixels", "name": "pixels", "type": "IMAGE", "link": 1},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 11},
        {"localized_name": "mask", "name": "mask", "type": "MASK", "link": 4},
    ],
    [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [6]}],
    []))
# 204 SetLatentNoiseMask
nodes.append(node(204, "SetLatentNoiseMask", [750, 150], [220, 80],
    [
        {"localized_name": "samples", "name": "samples", "type": "LATENT", "link": 6},
        {"localized_name": "mask", "name": "mask", "type": "MASK", "link": 5},
    ],
    [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [7]}],
    []))
# 205 UNETLoader
nodes.append(node(205, "UNETLoader", [750, 300], [360, 100],
    [
        {"localized_name": "unet_name", "name": "unet_name", "type": "COMBO", "widget": {"name": "unet_name"}, "link": None},
        {"localized_name": "weight_dtype", "name": "weight_dtype", "type": "COMBO", "widget": {"name": "weight_dtype"}, "link": None},
    ],
    [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [8]}],
    ["krea2_turbo_fp8_scaled.safetensors", "default"]))
# 206 CLIPLoader
nodes.append(node(206, "CLIPLoader", [750, 450], [360, 140],
    [
        {"localized_name": "clip_name", "name": "clip_name", "type": "COMBO", "widget": {"name": "clip_name"}, "link": None},
        {"localized_name": "type", "name": "type", "type": "COMBO", "widget": {"name": "type"}, "link": None},
        {"localized_name": "device", "name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None},
    ],
    [{"localized_name": "CLIP", "name": "CLIP", "type": "CLIP", "links": [9, 10]}],
    ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"]))
# 207 VAELoader
nodes.append(node(207, "VAELoader", [750, 650], [360, 80],
    [{"localized_name": "vae_name", "name": "vae_name", "type": "COMBO", "widget": {"name": "vae_name"}, "link": None}],
    [{"localized_name": "VAE", "name": "VAE", "type": "VAE", "links": [11]}],
    ["qwen_image_vae.safetensors"]))
# 208 positive
nodes.append(node(208, "CLIPTextEncode", [1200, 300], [400, 200],
    [{"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 9}],
    [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [12]}],
    ["pure black empty background, dark void, plain dark space, no objects, no furniture, no chair, no wall"]))
# 209 negative
nodes.append(node(209, "CLIPTextEncode", [1200, 550], [400, 200],
    [{"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 10}],
    [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [13]}],
    ["chair, table, wall, objects, person, bright, white, light, furniture"]))
# 210 KSampler (Krea2 turbo: 10 steps, cfg 1, euler, simple, denoise 1)
nodes.append(node(210, "KSampler", [1650, 300], [320, 260],
    [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 8},
        {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": 12},
        {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": 13},
        {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": 7},
    ],
    [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [14]}],
    [123456789, "randomize", 10, 1, "euler", "simple", 1]))
# 211 VAEDecode
nodes.append(node(211, "VAEDecode", [2050, 300], [220, 80],
    [
        {"localized_name": "samples", "name": "samples", "type": "LATENT", "link": 14},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 11},
    ],
    [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [15]}],
    []))
# 212 ImageCompositeMasked (original + inpainted + mask -> final)
nodes.append(node(212, "ImageCompositeMasked", [2350, 300], [260, 120],
    [
        {"localized_name": "destination", "name": "destination", "type": "IMAGE", "link": 2},
        {"localized_name": "source", "name": "source", "type": "IMAGE", "link": 15},
        {"localized_name": "mask", "name": "mask", "type": "MASK", "link": 16},
    ],
    [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [17]}],
    [0, 0, False], title="composite back onto original"))
# 213 SaveImage
nodes.append(node(213, "SaveImage", [2700, 300], [300, 200],
    [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": 17}],
    [],
    ["jaisal_kf2_manual_inpaint"]))

links = [
    link(1, 200, 0, 203, 0, "IMAGE"),
    link(2, 200, 0, 212, 0, "IMAGE"),
    link(3, 201, 1, 202, 0, "MASK"),
    link(4, 202, 0, 203, 1, "MASK"),
    link(5, 202, 0, 204, 1, "MASK"),
    link(6, 203, 0, 204, 0, "LATENT"),
    link(7, 204, 0, 210, 3, "LATENT"),
    link(8, 205, 0, 210, 0, "MODEL"),
    link(9, 206, 0, 208, 0, "CLIP"),
    link(10, 206, 0, 209, 0, "CLIP"),
    link(11, 207, 0, 211, 1, "VAE"),
    link(12, 208, 0, 210, 1, "CONDITIONING"),
    link(13, 209, 0, 210, 2, "CONDITIONING"),
    link(14, 210, 0, 211, 0, "LATENT"),
    link(15, 211, 0, 212, 1, "IMAGE"),
    link(16, 202, 0, 212, 2, "MASK"),
    link(17, 212, 0, 213, 0, "IMAGE"),
]

d = {
    "id": "kf2-manual-inpaint", "revision": 0, "last_node_id": 213, "last_link_id": 17,
    "nodes": nodes, "links": links, "groups": [], "config": {}, "extra": {}, "version": 0.4
}
json.dump(d, open(DST, 'w', encoding='utf-8'), ensure_ascii=False)
print("WROTE", DST)
