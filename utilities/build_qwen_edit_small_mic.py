import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\qwen_edit_small_mic.json'

EDIT_PROMPT = (
    "Make the microphone SMALL and COMPACT, on a SHORT LOW stand, sitting low on the table "
    "among the papers. The microphone head should be small (like a compact studio mic), "
    "NOT a large broadcast mic. Keep EVERYTHING ELSE exactly the same: the loose sheets of "
    "paper floating in the air, the wooden table, the empty wooden chair, the single bare "
    "bulb hanging above, the pure black void background, and the black-and-white high-contrast "
    "cinematic style with fine film grain. Only the microphone changes - smaller and lower."
)
NEG_PROMPT = (
    "large microphone, big microphone, tall microphone stand, broadcast microphone, "
    "color, any color, people, a person, a boy, extra objects, text, watermark, "
    "glowing effects, holograms, fire, smoke"
)

nodes = [
    {"id": 1, "type": "LoadImage", "pos": [40, 200], "size": [300, 320], "flags": {}, "order": 0, "mode": 0,
     "inputs": [
        {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
        {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
     ],
     "outputs": [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [101, 113, 114]},
        {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
     ],
     "properties": {"Node name for S&R": "LoadImage"},
     "widgets_values": ["mic+paper.png", "image"]},
    {"id": 2, "type": "UnetLoaderGGUF", "pos": [40, 600], "size": [320, 60], "flags": {}, "order": 1, "mode": 0,
     "inputs": [],
     "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [104]}],
     "properties": {"Node name for S&R": "UnetLoaderGGUF"},
     "widgets_values": ["Qwen-Image-Edit-2509-Q8_0.gguf"]},
    {"id": 3, "type": "CLIPLoader", "pos": [40, 700], "size": [320, 100], "flags": {}, "order": 2, "mode": 0,
     "inputs": [],
     "outputs": [{"localized_name": "CLIP", "name": "CLIP", "type": "CLIP", "links": [102, 111]}],
     "properties": {"Node name for S&R": "CLIPLoader"},
     "widgets_values": ["qwen_2.5_vl_7b_fp8_scaled.safetensors", "qwen_image", "default"]},
    {"id": 4, "type": "VAELoader", "pos": [40, 820], "size": [320, 60], "flags": {}, "order": 3, "mode": 0,
     "inputs": [],
     "outputs": [{"localized_name": "VAE", "name": "VAE", "type": "VAE", "links": [103, 109, 112, 115]}],
     "properties": {"Node name for S&R": "VAELoader"},
     "widgets_values": ["qwen_image_vae.safetensors"]},
    {"id": 5, "type": "TextEncodeQwenImageEdit", "pos": [420, 200], "size": [400, 260], "flags": {}, "order": 4, "mode": 0,
     "inputs": [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 102},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 103},
        {"localized_name": "image", "name": "image", "type": "IMAGE", "link": 101},
        {"localized_name": "prompt", "name": "prompt", "type": "STRING", "widget": {"name": "prompt"}, "link": None},
     ],
     "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [105]}],
     "properties": {"Node name for S&R": "TextEncodeQwenImageEdit"},
     "widgets_values": [EDIT_PROMPT]},
    {"id": 10, "type": "TextEncodeQwenImageEdit", "pos": [420, 520], "size": [400, 200], "flags": {}, "order": 5, "mode": 0,
     "inputs": [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 111},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 112},
        {"localized_name": "image", "name": "image", "type": "IMAGE", "link": 113},
        {"localized_name": "prompt", "name": "prompt", "type": "STRING", "widget": {"name": "prompt"}, "link": None},
     ],
     "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [106]}],
     "properties": {"Node name for S&R": "TextEncodeQwenImageEdit"},
     "widgets_values": [NEG_PROMPT]},
    {"id": 6, "type": "VAEEncode", "pos": [420, 520], "size": [340, 100], "flags": {}, "order": 5, "mode": 0,
     "inputs": [
        {"localized_name": "pixels", "name": "pixels", "type": "IMAGE", "link": 114},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 115},
     ],
     "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [107]}],
     "properties": {"Node name for S&R": "VAEEncode"},
     "widgets_values": []},
    {"id": 7, "type": "KSampler", "pos": [860, 400], "size": [320, 260], "flags": {}, "order": 6, "mode": 0,
     "inputs": [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 104},
        {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": 105},
        {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": 106},
        {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": 107},
        {"localized_name": "seed", "name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
        {"localized_name": "steps", "name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
        {"localized_name": "cfg", "name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
        {"localized_name": "sampler_name", "name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": None},
        {"localized_name": "scheduler", "name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": None},
        {"localized_name": "denoise", "name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None},
     ],
     "outputs": [
        {"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None},
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None},
     ],
     "properties": {"Node name for S&R": "KSampler"},
     "widgets_values": [123456789, "randomize", 20, 1.0, "euler", "simple", 1.0]},
    {"id": 8, "type": "VAEDecode", "pos": [1220, 400], "size": [220, 60], "flags": {}, "order": 7, "mode": 0,
     "inputs": [
        {"localized_name": "samples", "name": "samples", "type": "LATENT", "link": 108},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 109},
     ],
     "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [110]}],
     "properties": {"Node name for S&R": "VAEDecode"},
     "widgets_values": []},
    {"id": 9, "type": "SaveImage", "pos": [1460, 400], "size": [320, 240], "flags": {}, "order": 8, "mode": 0,
     "inputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": 110}],
     "outputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "links": None}],
     "properties": {"Node name for S&R": "SaveImage"},
     "widgets_values": ["jaisal_cut/mic_small"]},
]

links = [
    [101, 1, 0, 5, 2, "IMAGE"],
    [102, 3, 0, 5, 0, "CLIP"],
    [103, 4, 0, 5, 1, "VAE"],
    [104, 2, 0, 7, 0, "MODEL"],
    [105, 5, 0, 7, 1, "CONDITIONING"],
    [106, 10, 0, 7, 2, "CONDITIONING"],
    [107, 6, 0, 7, 3, "LATENT"],
    [108, 7, 0, 8, 0, "LATENT"],
    [109, 4, 0, 8, 1, "VAE"],
    [110, 8, 0, 9, 0, "IMAGE"],
    [111, 3, 0, 10, 0, "CLIP"],
    [112, 4, 0, 10, 1, "VAE"],
    [113, 1, 0, 10, 2, "IMAGE"],
    [114, 1, 0, 6, 0, "IMAGE"],
    [115, 4, 0, 6, 1, "VAE"],
]

wf = {"id": "qwen-edit-small-mic", "version": 0.4, "last_node_id": 10, "last_link_id": 115,
      "nodes": nodes, "links": links,
      "groups": [], "extra": {"ds": {"scale": 1, "offset": [0, 0]}},
      "config": {}}

json.dump(wf, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written:', WF)

# Also point G's ref_image_1 (node 139) at the new small-mic file
G = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json'
g = json.load(open(G, encoding='utf-8'))
for n in g['nodes']:
    if n['id'] == 139:
        n['widgets_values'] = ['mic+paper_small.png', 'image']
        print('G node 139 -> mic+paper_small.png')
json.dump(g, open(G, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('G updated')
