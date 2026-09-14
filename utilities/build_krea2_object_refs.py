r"""Build a Krea2 t2i workflow that generates the 3 Shot-7 object references:
soccer ball, cricket bat, paper-with-smiley. Each on a clean black background
so MiniMax H3 can extract them as clean object refs.

No identity LoRA (these are objects, not the character). Shared UNET/CLIP/VAE.
Native widgets_values shapes copied from krea2_identity_edit.json.

Usage:
    & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\build_krea2_object_refs.py"
"""
import json, os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

UNET = "krea2_turbo_bf16.safetensors"
CLIP = "qwen3vl_4b_fp8_scaled.safetensors"
VAE = "qwen_image_vae.safetensors"

# object prompts (clean black background, single top light, B&W)
PROMPTS = {
    "soccer_ball": (
        "A single round soccer ball, perfectly spherical, classic black and white "
        "pentagon pattern, resting on a flat surface. Pure black background, no other "
        "objects. Lit from directly above by a single UNSEEN light source - the light "
        "itself is NOT visible in the frame, only its light and hard shadow. "
        "Black and white, high contrast, clean smooth image, no grain. "
        "Centered, symmetric, eye level, static camera, 50mm lens."
    ),
    "cricket_bat": (
        "A single traditional wooden cricket bat, full-sized, flat broad blade and "
        "narrow handle, standing vertically upright. Pure black background, no other "
        "objects. Lit from directly above by a single UNSEEN light source - the light "
        "itself is NOT visible in the frame, only its light and hard shadow. "
        "Black and white, high contrast, clean smooth image, no grain. "
        "Centered, symmetric, eye level, static camera, 50mm lens."
    ),
    "paper_smiley": (
        "A single sheet of paper covered in dense handwriting, with a simple curved "
        "smile line drawn on it, lying flat. Pure black background, no other objects. "
        "Lit from directly above by a single UNSEEN light source - the light itself "
        "is NOT visible in the frame, only its light and hard shadow. "
        "Black and white, high contrast, clean smooth image, no grain. "
        "Centered, symmetric, top-down view, static camera, 50mm lens."
    ),
}

NEG = (
    "color, any color, warm tones, multiple light sources, bright background, "
    "other objects, multiple objects, person, human, face, text watermark, logo, "
    "blurry, low quality, noise, grain, speckles, american football, oval ball, "
    "light bulb, bare bulb, lamp, visible light source, ceiling, cord, wire, "
    "hanging bulb, bulb in frame"
)

nodes = [
    # shared loaders
    {"id": 1, "type": "UNETLoader", "pos": [40, 40], "size": [340, 100], "flags": {}, "order": 0, "mode": 0,
     "inputs": [
         {"localized_name": "unet_name", "name": "unet_name", "type": "COMBO", "widget": {"name": "unet_name"}, "link": None},
         {"localized_name": "weight_dtype", "name": "weight_dtype", "type": "COMBO", "widget": {"name": "weight_dtype"}, "link": None},
     ],
     "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [10, 11, 12]}],
     "properties": {"Node name for S&R": "UNETLoader"},
     "widgets_values": [UNET, "default"]},
    {"id": 2, "type": "CLIPLoader", "pos": [40, 180], "size": [340, 140], "flags": {}, "order": 1, "mode": 0,
     "inputs": [
         {"localized_name": "clip_name", "name": "clip_name", "type": "COMBO", "widget": {"name": "clip_name"}, "link": None},
         {"localized_name": "type", "name": "type", "type": "COMBO", "widget": {"name": "type"}, "link": None},
         {"localized_name": "device", "name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None},
     ],
     "outputs": [{"localized_name": "CLIP", "name": "CLIP", "type": "CLIP", "links": [13, 14, 15, 16, 17, 18]}],
     "properties": {"Node name for S&R": "CLIPLoader"},
     "widgets_values": [CLIP, "krea2", "default"]},
    {"id": 3, "type": "VAELoader", "pos": [40, 360], "size": [340, 80], "flags": {}, "order": 2, "mode": 0,
     "inputs": [
         {"localized_name": "vae_name", "name": "vae_name", "type": "COMBO", "widget": {"name": "vae_name"}, "link": None},
     ],
     "outputs": [{"localized_name": "VAE", "name": "VAE", "type": "VAE", "links": [19, 20, 21]}],
     "properties": {"Node name for S&R": "VAELoader"},
     "widgets_values": [VAE]},
]

# per-object branches
# slot layout: 0=model,1=positive,2=negative,3=latent (KSampler)
#              0=clip,1=text (CLIPTextEncode)
#              0=width,1=height,2=batch_size (EmptySD3LatentImage)
#              0=samples,1=vaE (VAEDecode)
#              0=images,1=filename_prefix (SaveImage)
branches = [
    ("soccer_ball", 100, 40),
    ("cricket_bat", 100, 460),
    ("paper_smiley", 100, 880),
]

link_id = 100
node_id = 10
for name, y, _ in branches:
    pos = [420, y]
    # positive
    nodes.append({"id": node_id, "type": "CLIPTextEncode", "pos": [420, y], "size": [400, 200], "flags": {}, "order": 3, "mode": 0,
        "inputs": [
            {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": link_id},
            {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": None},
        ],
        "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [link_id + 1]}],
        "properties": {"Node name for S&R": "CLIPTextEncode"},
        "widgets_values": [PROMPTS[name]]})
    pos_id, pos_link = node_id, link_id + 1
    node_id += 1; link_id += 2
    # negative
    nodes.append({"id": node_id, "type": "CLIPTextEncode", "pos": [420, y + 220], "size": [400, 160], "flags": {}, "order": 4, "mode": 0,
        "inputs": [
            {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": link_id},
            {"localized_name": "text", "name": "text", "type": "STRING", "widget": {"name": "text"}, "link": None},
        ],
        "outputs": [{"localized_name": "CONDITIONING", "name": "CONDITIONING", "type": "CONDITIONING", "links": [link_id + 1]}],
        "properties": {"Node name for S&R": "CLIPTextEncode"},
        "widgets_values": [NEG]})
    neg_id, neg_link = node_id, link_id + 1
    node_id += 1; link_id += 2
    # latent
    nodes.append({"id": node_id, "type": "EmptySD3LatentImage", "pos": [420, y + 400], "size": [320, 120], "flags": {}, "order": 5, "mode": 0,
        "inputs": [
            {"localized_name": "width", "name": "width", "type": "INT", "widget": {"name": "width"}, "link": None},
            {"localized_name": "height", "name": "height", "type": "INT", "widget": {"name": "height"}, "link": None},
            {"localized_name": "batch_size", "name": "batch_size", "type": "INT", "widget": {"name": "batch_size"}, "link": None},
        ],
        "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [link_id]}],
        "properties": {"Node name for S&R": "EmptySD3LatentImage"},
        "widgets_values": [1024, 1024, 1]})
    lat_id, lat_link = node_id, link_id
    node_id += 1; link_id += 1
    # sampler
    nodes.append({"id": node_id, "type": "KSampler", "pos": [860, y], "size": [320, 260], "flags": {}, "order": 6, "mode": 0,
        "inputs": [
            {"localized_name": "model", "name": "model", "type": "MODEL", "link": link_id},
            {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": pos_link},
            {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": neg_link},
            {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": lat_link},
            {"localized_name": "seed", "name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
            {"localized_name": "steps", "name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
            {"localized_name": "cfg", "name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
            {"localized_name": "sampler_name", "name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": None},
            {"localized_name": "scheduler", "name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": None},
            {"localized_name": "denoise", "name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None},
        ],
        "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [link_id + 1]}],
        "properties": {"Node name for S&R": "KSampler"},
        "widgets_values": [42, "randomize", 10, 1, "euler", "simple", 1]})
    samp_id, samp_link = node_id, link_id + 1
    node_id += 1; link_id += 2
    # decode
    nodes.append({"id": node_id, "type": "VAEDecode", "pos": [1220, y], "size": [220, 80], "flags": {}, "order": 7, "mode": 0,
        "inputs": [
            {"localized_name": "samples", "name": "samples", "type": "LATENT", "link": samp_link},
            {"localized_name": "vae", "name": "vae", "type": "VAE", "link": link_id},
        ],
        "outputs": [{"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [link_id + 1]}],
        "properties": {"Node name for S&R": "VAEDecode"},
        "widgets_values": []})
    dec_id, dec_link = node_id, link_id + 1
    node_id += 1; link_id += 2
    # save
    nodes.append({"id": node_id, "type": "SaveImage", "pos": [1480, y], "size": [340, 340], "flags": {}, "order": 8, "mode": 0,
        "inputs": [
            {"localized_name": "images", "name": "images", "type": "IMAGE", "link": dec_link},
            {"localized_name": "filename_prefix", "name": "filename_prefix", "type": "STRING", "widget": {"name": "filename_prefix"}, "link": None},
        ],
        "outputs": [],
        "properties": {"Node name for S&R": "SaveImage"},
        "widgets_values": ["jaisal_cut/obj_" + name]})
    node_id += 1

# wire shared loaders to branches: UNET->each sampler model, CLIP->each pos/neg, VAE->each decode
# (links already assigned above via link ids; ensure loader output link lists match)
# Rebuild loader output link lists to include all branch links
loader_links = {1: [], 2: [], 3: []}
for n in nodes:
    if n["type"] == "KSampler":
        loader_links[1].append(n["inputs"][0]["link"])
    if n["type"] == "CLIPTextEncode":
        loader_links[2].append(n["inputs"][0]["link"])
    if n["type"] == "VAEDecode":
        loader_links[3].append(n["inputs"][1]["link"])
for n in nodes:
    if n["id"] == 1:
        n["outputs"][0]["links"] = loader_links[1]
    if n["id"] == 2:
        n["outputs"][0]["links"] = loader_links[2]
    if n["id"] == 3:
        n["outputs"][0]["links"] = loader_links[3]

# build links array
links = []
for n in nodes:
    for i, inp in enumerate(n.get("inputs", [])):
        if inp.get("link") is not None:
            # find source node+slot
            for sn in nodes:
                for so, outp in enumerate(sn.get("outputs", [])):
                    if outp.get("links") and inp["link"] in outp["links"]:
                        links.append([inp["link"], sn["id"], so, n["id"], i, outp["name"]])
                        break
                else:
                    continue
                break

wf = {
    "id": "krea2-object-refs",
    "revision": 0,
    "last_node_id": node_id - 1,
    "last_link_id": max([l[0] for l in links], default=0),
    "nodes": nodes,
    "links": links,
    "groups": [],
    "config": {},
    "extra": {},
    "version": 0.4,
}

out_path = os.path.join(WF_DIR, "krea2_object_refs.json")
json.dump(wf, open(out_path, "w", encoding="utf-8"), indent=1)
print("WROTE", out_path)
print("objects:", list(PROMPTS.keys()))
print("UNET:", UNET, "| CLIP:", CLIP, "| VAE:", VAE)
