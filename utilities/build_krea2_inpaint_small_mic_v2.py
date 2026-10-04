import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_inpaint_small_mic.json'

POS = ("A small compact studio microphone on a short low stand, sitting low on the "
       "wooden table. The microphone head is small (like a compact studio mic), NOT a "
       "large broadcast mic. Black-and-white high-contrast cinematic style, fine film "
       "grain, matching the surrounding scene exactly.")
NEG = ("large microphone, big microphone, tall microphone stand, broadcast microphone, "
       "color, any color, people, a person, a boy, extra objects, text, watermark, "
       "glowing effects, holograms, fire, smoke")

nodes = [
    {"id": 1, "type": "LoadImage", "pos": [40, 200], "size": [300, 320], "flags": {}, "order": 0, "mode": 0,
     "inputs": [
        {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
        {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
     ],
     "outputs": [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [101]},
        {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
     ],
     "properties": {"Node name for S&R": "LoadImage"},
     "widgets_values": ["mic+paper.png", "image"]},
    {"id": 2, "type": "LoadImage", "pos": [40, 560], "size": [300, 320], "flags": {}, "order": 1, "mode": 0,
     "inputs": [
        {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
        {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
     ],
     "outputs": [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None},
        {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": [102]},
     ],
     "properties": {"Node name for S&R": "LoadImage"},
     "widgets_values": ["mic_mask.png", "image"]},
    {"id": 3, "type": "UNETLoader", "pos": [40, 920], "size": [320, 80], "flags": {}, "order": 2, "mode": 0,
     "inputs": [
        {"localized_name": "unet_name", "name": "unet_name", "type": "COMBO", "widget": {"name": "unet_name"}, "link": None},
        {"localized_name": "weight_dtype", "name": "weight_dtype", "type": "COMBO", "widget": {"name": "weight_dtype"}, "link": None},
     ],
     "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [103]}],
     "properties": {"Node name for S&R": "UNETLoader"},
     "widgets_values": ["krea2_turbo_bf16.safetensors", "default"]},
    {"id": 4, "type": "CLIPLoader", "pos": [40, 1040], "size": [320, 100], "flags": {}, "order": 3, "mode": 0,
     "inputs": [
        {"localized_name": "clip_name", "name": "clip_name", "type": "COMBO", "widget": {"name": "clip_name"}, "link": None},
        {"localized_name": "type", "name": "type", "type": "COMBO", "widget": {"name": "type"}, "link": None},
        {"localized_name": "device", "name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None},
     ],
     "outputs": [{"localized_name": "CLIP", "name": "CLIP", "type": "CLIP", "links": [104, 105]}],
     "properties": {"Node name for S&R": "CLIPLoader"},
     "widgets_values": ["qwen3vl_4b_bf16.safetensors", "krea2", "default"]},
    {"id": 5, "type": "VAELoader", "pos": [40, 1180], "size": [320, 60], "flags": {}, "order": 4, "mode": 0,
     "inputs": [
        {"localized_name": "vae_name", "name": "vae_name", "type": "COMBO", "widget": {"name": "vae_name"}, "link": None},
     ],
     "outputs": [{"localized_name": "VAE", "name": "VAE", "type": "VAE", "links": [106, 107]}],
     "properties": {"Node name for S&R": "VAELoader"},
     "widgets_values": ["qwen_image_vae.safetensors"]},
    {"id": 6, "type": "CLIPTextEncode", "pos": [420, 200], "size": [400, 200], "flags": {}, "order": 5, "mode": 0,
     "inputs": [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 104},
        {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": None},
     ],
     "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [108]}],
     "properties": {"Node name for S&R": "CLIPTextEncode"},
     "widgets_values": [POS]},
    {"id": 7, "type": "CLIPTextEncode", "pos": [420, 460], "size": [400, 200], "flags": {}, "order": 6, "mode": 0,
     "inputs": [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 105},
        {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": None},
     ],
     "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [109]}],
     "properties": {"Node name for S&R": "CLIPTextEncode"},
     "widgets_values": [NEG]},
    {"id": 8, "type": "VAEEncodeForInpaint", "pos": [420, 720], "size": [340, 120], "flags": {}, "order": 7, "mode": 0,
     "inputs": [
        {"localized_name": "pixels", "name": "pixels", "type": "IMAGE", "link": 101},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 106},
        {"localized_name": "mask", "name": "mask", "type": "MASK", "link": 102},
     ],
     "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [110]}],
     "properties": {"Node name for S&R": "VAEEncodeForInpaint"},
     "widgets_values": []},
    {"id": 9, "type": "KSampler", "pos": [860, 400], "size": [320, 260], "flags": {}, "order": 8, "mode": 0,
     "inputs": [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 103},
        {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": 108},
        {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": 109},
        {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": 110},
        {"localized_name": "seed", "name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
        {"localized_name": "steps", "name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
        {"localized_name": "cfg", "name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
        {"localized_name": "sampler_name", "name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": None},
        {"localized_name": "scheduler", "name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": None},
        {"localized_name": "denoise", "name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None},
     ],
     "outputs": [
        {"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [111]},
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None},
     ],
     "properties": {"Node name for S&R": "KSampler"},
     "widgets_values": [123456789, "randomize", 8, 1.0, "euler", "simple", 1.0]},
    {"id": 10, "type": "VAEDecode", "pos": [1220, 400], "size": [220, 60], "flags": {}, "order": 9, "mode": 0,
     "inputs": [
        {"localized_name": "samples", "name": "samples", "type": "LATENT", "link": 111},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 107},
     ],
     "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [112]}],
     "properties": {"Node name for S&R": "VAEDecode"},
     "widgets_values": []},
    {"id": 11, "type": "SaveImage", "pos": [1460, 400], "size": [320, 240], "flags": {}, "order": 10, "mode": 0,
     "inputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": 112}],
     "outputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "links": None}],
     "properties": {"Node name for S&R": "SaveImage"},
     "widgets_values": ["jaisal_cut/mic_small"]},
]

links = [
    [101, 1, 0, 8, 0, "IMAGE"],
    [102, 2, 1, 8, 2, "MASK"],
    [103, 3, 0, 9, 0, "MODEL"],
    [104, 4, 0, 6, 0, "CLIP"],
    [105, 4, 0, 7, 0, "CLIP"],
    [106, 5, 0, 8, 1, "VAE"],
    [107, 5, 0, 10, 1, "VAE"],
    [108, 6, 0, 9, 1, "CONDITIONING"],
    [109, 7, 0, 9, 2, "CONDITIONING"],
    [110, 8, 0, 9, 3, "LATENT"],
    [111, 9, 0, 10, 0, "LATENT"],
    [112, 10, 0, 11, 0, "IMAGE"],
]

wf = {"id": "krea2-inpaint-small-mic", "version": 0.4, "last_node_id": 11, "last_link_id": 112,
      "nodes": nodes, "links": links,
      "groups": [], "extra": {"ds": {"scale": 1, "offset": [0, 0]}},
      "config": {}}

json.dump(wf, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written:', WF)
