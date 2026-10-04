import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_small_mic_end.json'

POS = (
    "A SINGLE small compact studio microphone on a SHORT LOW stand, sitting low on a "
    "weathered wooden table, its top well below the height of a tall broadcast mic. "
    "ONLY ONE microphone in the entire image. Several loose sheets of paper with dense "
    "handwriting float in the air around it, multiple sheets drifting. A single bare "
    "bulb hangs from a thin wire above, the only light source. Pure black void "
    "background. Black-and-white high-contrast cinematic style, fine film grain, sharp "
    "focus, high detail, clean smooth image, static camera, medium-wide shot, eye level."
)
NEG = (
    "two microphones, multiple microphones, duplicate mic, extra mic, second mic, "
    "large microphone, big microphone, tall microphone stand, broadcast microphone, "
    "tall object, color, any color, people, a person, a boy, a chair, no papers, "
    "empty scene, text watermark, logo, blurry, low quality, out of focus, "
    "glowing effects, holograms, fire, smoke"
)

nodes = [
    {"id": 1, "type": "UNETLoader", "pos": [40, 200], "size": [320, 80], "flags": {}, "order": 0, "mode": 0,
     "inputs": [
        {"localized_name": "unet_name", "name": "unet_name", "type": "COMBO", "widget": {"name": "unet_name"}, "link": None},
        {"localized_name": "weight_dtype", "name": "weight_dtype", "type": "COMBO", "widget": {"name": "weight_dtype"}, "link": None},
     ],
     "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [101]}],
     "properties": {"Node name for S&R": "UNETLoader"},
     "widgets_values": ["krea2_turbo_bf16.safetensors", "default"]},
    {"id": 2, "type": "CLIPLoader", "pos": [40, 320], "size": [320, 100], "flags": {}, "order": 1, "mode": 0,
     "inputs": [
        {"localized_name": "clip_name", "name": "clip_name", "type": "COMBO", "widget": {"name": "clip_name"}, "link": None},
        {"localized_name": "type", "name": "type", "type": "COMBO", "widget": {"name": "type"}, "link": None},
        {"localized_name": "device", "name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None},
     ],
     "outputs": [{"localized_name": "CLIP", "name": "CLIP", "type": "CLIP", "links": [102, 103]}],
     "properties": {"Node name for S&R": "CLIPLoader"},
     "widgets_values": ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"]},
    {"id": 3, "type": "VAELoader", "pos": [40, 460], "size": [320, 60], "flags": {}, "order": 2, "mode": 0,
     "inputs": [
        {"localized_name": "vae_name", "name": "vae_name", "type": "COMBO", "widget": {"name": "vae_name"}, "link": None},
     ],
     "outputs": [{"localized_name": "VAE", "name": "VAE", "type": "VAE", "links": [104]}],
     "properties": {"Node name for S&R": "VAELoader"},
     "widgets_values": ["qwen_image_vae.safetensors"]},
    {"id": 10, "type": "CLIPTextEncode", "pos": [420, 200], "size": [400, 220], "flags": {}, "order": 3, "mode": 0,
     "inputs": [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 102},
        {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": None},
     ],
     "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [106]}],
     "properties": {"Node name for S&R": "CLIPTextEncode"},
     "widgets_values": [POS]},
    {"id": 11, "type": "CLIPTextEncode", "pos": [420, 480], "size": [400, 220], "flags": {}, "order": 4, "mode": 0,
     "inputs": [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 103},
        {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": None},
     ],
     "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [107]}],
     "properties": {"Node name for S&R": "CLIPTextEncode"},
     "widgets_values": [NEG]},
    {"id": 12, "type": "EmptySD3LatentImage", "pos": [420, 760], "size": [340, 100], "flags": {}, "order": 5, "mode": 0,
     "inputs": [
        {"localized_name": "width", "name": "width", "type": "INT", "widget": {"name": "width"}, "link": None},
        {"localized_name": "height", "name": "height", "type": "INT", "widget": {"name": "height"}, "link": None},
        {"localized_name": "batch_size", "name": "batch_size", "type": "INT", "widget": {"name": "batch_size"}, "link": None},
     ],
     "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [108]}],
     "properties": {"Node name for S&R": "EmptySD3LatentImage"},
     "widgets_values": [1920, 1088, 1]},
    {"id": 13, "type": "KSampler", "pos": [860, 400], "size": [320, 260], "flags": {}, "order": 6, "mode": 0,
     "inputs": [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 101},
        {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": 106},
        {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": 107},
        {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": 108},
        {"localized_name": "seed", "name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
        {"localized_name": "steps", "name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
        {"localized_name": "cfg", "name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
        {"localized_name": "sampler_name", "name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": None},
        {"localized_name": "scheduler", "name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": None},
        {"localized_name": "denoise", "name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None},
     ],
     "outputs": [
        {"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [109]},
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": None},
     ],
     "properties": {"Node name for S&R": "KSampler"},
     "widgets_values": [42, "randomize", 15, 1.0, "euler", "simple", 1.0]},
    {"id": 14, "type": "VAEDecode", "pos": [1220, 400], "size": [220, 60], "flags": {}, "order": 7, "mode": 0,
     "inputs": [
        {"localized_name": "samples", "name": "samples", "type": "LATENT", "link": 109},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 104},
     ],
     "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [110]}],
     "properties": {"Node name for S&R": "VAEDecode"},
     "widgets_values": []},
    {"id": 15, "type": "SaveImage", "pos": [1460, 400], "size": [320, 240], "flags": {}, "order": 8, "mode": 0,
     "inputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": 110}],
     "outputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "links": None}],
     "properties": {"Node name for S&R": "SaveImage"},
     "widgets_values": ["jaisal_cut/mic_small_end"]},
]

links = [
    [101, 1, 0, 13, 0, "MODEL"],
    [102, 2, 0, 10, 0, "CLIP"],
    [103, 2, 0, 11, 0, "CLIP"],
    [104, 3, 0, 14, 1, "VAE"],
    [106, 10, 0, 13, 1, "CONDITIONING"],
    [107, 11, 0, 13, 2, "CONDITIONING"],
    [108, 12, 0, 13, 3, "LATENT"],
    [109, 13, 0, 14, 0, "LATENT"],
    [110, 14, 0, 15, 0, "IMAGE"],
]

wf = {"id": "krea2-t2i-small-mic-end", "version": 0.4, "last_node_id": 15, "last_link_id": 110,
      "nodes": nodes, "links": links,
      "groups": [], "extra": {"ds": {"scale": 1, "offset": [0, 0]}},
      "config": {}}

json.dump(wf, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written:', WF)
