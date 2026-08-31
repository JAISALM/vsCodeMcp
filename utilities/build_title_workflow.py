import json

OUT = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_title.json'

POSITIVE = ("An angular, 3d art style, with brush stroke color texture. A FULLY UNDERWATER shot in a wide open "
            "natural Kerala river, the ENTIRE frame is underwater, no waterline, no half-water-half-bridge split, "
            "the camera positioned low in the water looking STRAIGHT UP, directly vertical, no tilt, no diagonal, "
            "the long stone bridge with its arches and the dark moody sky seen THROUGH the rippling water surface "
            "from below, refracted and distorted by the water, integrated into the water, rising bubbles, the water "
            "is open and unbounded on ALL sides with NO visible river bed, NO sand, NO pebbles, NO bottom in view, "
            "the water fades into dark open depth below, the title text 'The Jaisal Cut' rendered in elegant bold "
            "typography in the generous negative space of the open water, the title clearly readable and centered, "
            "NO person, NO boy, NO character, the water is dark and moody matching the rain, the sky seen through "
            "the water is DARK and moody, heavy overcast post-rain clouds, dim grey light filtering down through "
            "the water, highly detailed, 16:9 widescreen\n")

NEGATIVE = ("person, boy, character, figure, human, kid, face, body, multiple characters, more than one kid, "
            "duplicate character, blurry, low quality, deformed, watermark, logo, cartoon, flat vector, "
            "photorealistic, photo, bright sky, blue sky, sunny sky, clear sky, visible river bed, sandy river bed, "
            "pebble river bed, river bottom, sand, pebbles, concrete walls, canal, bund, garbled text, misspelled "
            "text, unreadable text, distorted letters\n")

def node(id, type, pos, size, inputs, outputs, widgets_values, props=None):
    n = {"id": id, "type": type, "pos": pos, "size": size, "flags": {}, "order": 0, "mode": 0,
         "inputs": inputs, "outputs": outputs, "widgets_values": widgets_values}
    if props:
        n["properties"] = props
    return n

nodes = [
    node(10, "UNETLoader", [40, 40], [480, 120],
         [{"name": "unet_name", "type": "COMBO", "widget": {"name": "unet_name"}, "link": None},
          {"name": "weight_dtype", "type": "COMBO", "widget": {"name": "weight_dtype"}, "link": None}],
         [{"name": "MODEL", "type": "MODEL", "links": [100]}],
         ["krea2_turbo_fp8_scaled.safetensors", "default"],
         {"Node name for S&R": "UNETLoader"}),
    node(11, "CLIPLoader", [40, 180], [480, 120],
         [{"name": "clip_name", "type": "COMBO", "widget": {"name": "clip_name"}, "link": None},
          {"name": "type", "type": "COMBO", "widget": {"name": "type"}, "link": None},
          {"name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None}],
         [{"name": "CLIP", "type": "CLIP", "links": [101, 102]}],
         ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"],
         {"Node name for S&R": "CLIPLoader"}),
    node(12, "VAELoader", [40, 320], [480, 90],
         [{"name": "vae_name", "type": "COMBO", "widget": {"name": "vae_name"}, "link": None}],
         [{"name": "VAE", "type": "VAE", "links": [103, 104]}],
         ["qwen_image_vae.safetensors"],
         {"Node name for S&R": "VAELoader"}),
    node(15, "LoraLoaderModelOnly", [560, 40], [480, 120],
         [{"name": "model", "type": "MODEL", "link": 100},
          {"name": "lora_name", "type": "COMBO", "widget": {"name": "lora_name"}, "link": None},
          {"name": "strength_model", "type": "FLOAT", "widget": {"name": "strength_model"}, "link": None}],
         [{"name": "MODEL", "type": "MODEL", "links": [105]}],
         ["Krea2_Cinematic_Artstyle.safetensors", 1.0],
         {"Node name for S&R": "LoraLoaderModelOnly"}),
    node(32, "LoraLoaderModelOnly", [560, 180], [480, 120],
         [{"name": "model", "type": "MODEL", "link": 105},
          {"name": "lora_name", "type": "COMBO", "widget": {"name": "lora_name"}, "link": None},
          {"name": "strength_model", "type": "FLOAT", "widget": {"name": "strength_model"}, "link": None}],
         [{"name": "MODEL", "type": "MODEL", "links": [106]}],
         ["Typnosis_Krea2.safetensors", 1.0],
         {"Node name for S&R": "LoraLoaderModelOnly"}),
    node(30, "LoadImage", [560, 320], [480, 320],
         [{"name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
          {"name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None}],
         [{"name": "IMAGE", "type": "IMAGE", "links": [107]},
          {"name": "MASK", "type": "MASK", "links": None}],
         ["refs_water.png", "image"],
         {"Node name for S&R": "LoadImage"}),
    node(31, "VAEEncode", [1080, 320], [480, 90],
         [{"name": "pixels", "type": "IMAGE", "link": 107},
          {"name": "vae", "type": "VAE", "link": 103}],
         [{"name": "LATENT", "type": "LATENT", "links": [108]}],
         [],
         {"Node name for S&R": "VAEEncode"}),
    node(6, "CLIPTextEncode", [1080, 40], [480, 200],
         [{"name": "clip", "type": "CLIP", "link": 101}],
         [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [109]}],
         [POSITIVE],
         {"Node name for S&R": "CLIPTextEncode"}),
    node(13, "CLIPTextEncode", [1080, 260], [480, 200],
         [{"name": "clip", "type": "CLIP", "link": 102}],
         [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [110]}],
         [NEGATIVE],
         {"Node name for S&R": "CLIPTextEncode"}),
    node(3, "KSampler", [1600, 40], [480, 260],
         [{"name": "model", "type": "MODEL", "link": 106},
          {"name": "positive", "type": "CONDITIONING", "link": 109},
          {"name": "negative", "type": "CONDITIONING", "link": 110},
          {"name": "latent_image", "type": "LATENT", "link": 108},
          {"name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
          {"name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
          {"name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
          {"name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": None},
          {"name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": None},
          {"name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None}],
         [{"name": "LATENT", "type": "LATENT", "links": [111]}],
         [123456789, "randomize", 8, 1.0, "euler", "simple", 0.55],
         {"Node name for S&R": "KSampler"}),
    node(8, "VAEDecode", [2120, 40], [480, 90],
         [{"name": "samples", "type": "LATENT", "link": 111},
          {"name": "vae", "type": "VAE", "link": 104}],
         [{"name": "IMAGE", "type": "IMAGE", "links": [112]}],
         [],
         {"Node name for S&R": "VAEDecode"}),
    node(29, "SaveImage", [2640, 40], [480, 260],
         [{"name": "images", "type": "IMAGE", "link": 112}],
         [],
         ["jaisal_cut/title"],
         {"Node name for S&R": "SaveImage"}),
]

links = [
    [100, 10, 0, 15, 0, "MODEL"],
    [101, 11, 0, 6, 0, "CLIP"],
    [102, 11, 0, 13, 0, "CLIP"],
    [103, 12, 0, 31, 1, "VAE"],
    [104, 12, 0, 8, 1, "VAE"],
    [105, 15, 0, 32, 0, "MODEL"],
    [106, 32, 0, 3, 0, "MODEL"],
    [107, 30, 0, 31, 0, "IMAGE"],
    [108, 31, 0, 3, 3, "LATENT"],
    [109, 6, 0, 3, 1, "CONDITIONING"],
    [110, 13, 0, 3, 2, "CONDITIONING"],
    [111, 3, 0, 8, 0, "LATENT"],
    [112, 8, 0, 29, 0, "IMAGE"],
]

d = {"id": "jaisal-title-card", "version": 0.4, "revision": 0, "last_node_id": 32,
     "last_link_id": 112, "nodes": nodes, "links": links,
     "groups": [], "extra": {}, "config": {}, "workflow": {}, "version": 0.4}
json.dump(d, open(OUT, "w", encoding="utf-8"), indent=1)
print("Wrote", OUT)
print("Chain: UNET(10) -> Cinematic LoRA(15) -> Typnosis LoRA(32) -> KSampler(3)")
print("i2i: LoadImage(30) -> VAEEncode(31) -> KSampler latent; denoise 0.55")
print("Save prefix: jaisal_cut/title")
