#!/usr/bin/env python3
"""Build k2f_jaisal_movie_shot_16x9.json — the 'learned recipe' movie-shot still.

Source: k2f_jaisal_crookednose.json (proven identity-edit wiring, seed 90201).
Changes (all from the Krea2 Film Studio technique, 2026-10-24):
  1. UNET  krea2_turbo_fp8_scaled -> krea2_turbo_bf16 (fp8 = grain/black spots)
  2. VAE   qwen_image_vae -> krea2RealVae_v10 (Krea2-native VAE)
  3. Patch node: wire source_image from the ref LoadImage (pixel-fit path:
     center-crop ref to 16:9, resize to exact target grid, VAE-encode — no
     latent-space resize)
  4. KSampler -> ClownsharKSampler_Beta #1 (RES4LYF: multistep/res_2m +
     beta57, 10 steps, cfg 1.0, denoise 0.65) on a 1928x1088 16:9 canvas
     (EmptyLatentImage) instead of the 9:16 ref-size latent
  5. + ClownsharKSampler_Beta #2 = 3-step denoise 0.27 refine pass (the
     Film Studio refinement stage)
  6. VAEDecode now tiled-friendly (decode of the 16:9 latent, krea2RealVae_v10)
  7. Negative = empty-prompt grounded encode (training-unconditional recipe)
  8. POS prompt = S1 paddy-after-harvest scene
"""
import json
import copy

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2f_jaisal_crookednose.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\k2f_jaisal_movie_shot_16x9.json"

d = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

NEW_PROMPT = (
    "Keep the man's face, medium wavy black hair (falling to eyebrow length), his naturally "
    "CROOKED bent nose, identity, slim build, and plain black t-shirt EXACTLY the same as "
    "the reference image. Change ONLY the setting: place him in a flooded paddy field in "
    "Kerala after harvest - golden rice stubble, standing water, light rain falling, a "
    "farmer with a hat bending in the far distance. Dusk, overcast moody light, soft "
    "natural light on his face. Cinematic 35mm movie still, shallow depth of field, "
    "photorealistic, natural color grade, no text, no watermark."
)

# ---- 1. UNET model -> bf16
n55 = nodes[55]
n55["widgets_values"][0] = "krea2_turbo_bf16.safetensors"
for m in n55.get("properties", {}).get("models", []):
    m["name"] = "krea2_turbo_bf16.safetensors"

# ---- 2. VAE -> Krea2-native
n57 = nodes[57]
n57["widgets_values"][0] = "krea2RealVae_v10.safetensors"
for m in n57.get("properties", {}).get("models", []):
    m["name"] = "krea2RealVae_v10.safetensors"

# ---- 3. Patch node: source_image (slot 5) from LoadImage 72
n79 = nodes[79]
src_img_input = next(i for i in n79["inputs"] if i["name"] == "source_image")
assert src_img_input["link"] is None, f"source_image already linked: {src_img_input['link']}"
src_img_input["link"] = 103
n72 = nodes[72]
img_out = next(o for o in n72["outputs"] if o["name"] == "IMAGE")
if 103 not in (img_out.get("links") or []):
    img_out["links"] = (img_out.get("links") or []) + [103]

# ---- 7. prompts
n84 = nodes[84]
n84["widgets_values"][0] = NEW_PROMPT
n85 = nodes[85]
n85["widgets_values"][0] = ""  # empty-prompt grounded negative (training-unconditional)

# ---- 4. KSampler 53 -> ClownsharKSampler_Beta #1
n53 = nodes[53]
n53["type"] = "ClownsharKSampler_Beta"
n53["size"] = [340, 600]
n53["inputs"] = [
    {"localized_name": "model", "name": "model", "type": "MODEL", "link": 3},
    {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": 20},
    {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": 21},
    {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": 100},
    {"localized_name": "eta", "name": "eta", "type": "FLOAT", "widget": {"name": "eta"}, "link": None},
    {"localized_name": "sampler_name", "name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": None},
    {"localized_name": "scheduler", "name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": None},
    {"localized_name": "steps", "name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
    {"localized_name": "steps_to_run", "name": "steps_to_run", "type": "INT", "widget": {"name": "steps_to_run"}, "link": None},
    {"localized_name": "denoise", "name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None},
    {"localized_name": "cfg", "name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
    {"localized_name": "seed", "name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
    {"localized_name": "sampler_mode", "name": "sampler_mode", "type": "COMBO", "widget": {"name": "sampler_mode"}, "link": None},
    {"localized_name": "bongmath", "name": "bongmath", "type": "BOOLEAN", "widget": {"name": "bongmath"}, "link": None},
]
n53["widgets_values"] = [0.5, "multistep/res_2m", "beta57", 10, -1, 0.65, 1.0, 90201, "standard", True]
n53["outputs"] = [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [101]}]
n53["widgets_values_named"] = None
n53["properties"] = {"Node name for S&R": "ClownsharKSampler_Beta", "cnr_id": "RES4LYF"}

# ---- 5. + refine stage node 61
n61 = {
    "id": 61, "type": "ClownsharKSampler_Beta", "pos": [3520, -170], "size": [340, 600],
    "flags": {}, "order": 30, "mode": 0,
    "inputs": [
        {"localized_name": "model", "name": "model", "type": "MODEL", "link": 3},
        {"localized_name": "positive", "name": "positive", "type": "CONDITIONING", "link": 20},
        {"localized_name": "negative", "name": "negative", "type": "CONDITIONING", "link": 21},
        {"localized_name": "latent_image", "name": "latent_image", "type": "LATENT", "link": 101},
        {"localized_name": "eta", "name": "eta", "type": "FLOAT", "widget": {"name": "eta"}, "link": None},
        {"localized_name": "sampler_name", "name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": None},
        {"localized_name": "scheduler", "name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": None},
        {"localized_name": "steps", "name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": None},
        {"localized_name": "steps_to_run", "name": "steps_to_run", "type": "INT", "widget": {"name": "steps_to_run"}, "link": None},
        {"localized_name": "denoise", "name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": None},
        {"localized_name": "cfg", "name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": None},
        {"localized_name": "seed", "name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
        {"localized_name": "sampler_mode", "name": "sampler_mode", "type": "COMBO", "widget": {"name": "sampler_mode"}, "link": None},
        {"localized_name": "bongmath", "name": "bongmath", "type": "BOOLEAN", "widget": {"name": "bongmath"}, "link": None},
    ],
    "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [102]}],
    "widgets_values": [0.5, "multistep/res_2m", "beta57", 3, -1, 0.27, 1.0, 90201, "standard", True],
    "widgets_values_named": None,
    "properties": {"Node name for S&R": "ClownsharKSampler_Beta", "cnr_id": "RES4LYF",
                   "note": "refine pass: 3 steps denoise 0.27 (Film Studio refinement stage)"},
}
d["nodes"].append(n61)

# ---- 4b. EmptyLatentImage 60 = 1928x1088 16:9 movie canvas
n60 = {
    "id": 60, "type": "EmptyLatentImage", "pos": [3520, -830], "size": [340, 160],
    "flags": {}, "order": 31, "mode": 0,
    "inputs": [
        {"localized_name": "width", "name": "width", "type": "INT", "widget": {"name": "width"}, "link": None},
        {"localized_name": "height", "name": "height", "type": "INT", "widget": {"name": "height"}, "link": None},
        {"localized_name": "batch_size", "name": "batch_size", "type": "INT", "widget": {"name": "batch_size"}, "link": None},
    ],
    "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [100]}],
    "widgets_values": [1928, 1088, 1],
    "widgets_values_named": None,
    "properties": {"Node name for S&R": "EmptyLatentImage", "cnr_id": "comfy-core"},
}
d["nodes"].append(n60)

# ---- 6. VAEDecode samples <- refine node
n54 = nodes[54]
smp = next(i for i in n54["inputs"] if i["name"] == "samples")
assert smp["link"] == 23
smp["link"] = 102

# ---- wire up links: drop stale 22/23, add 100-103 (links = list of [id, from_node, from_slot, to_node, to_slot, type])
def _find_link(lid):
    for l in d["links"]:
        if l[0] == lid:
            return l
    return None

for lid in (22, 23):
    l = _find_link(lid)
    if l is not None:
        d["links"].remove(l)
# node 73 (VAEEncode ref A) LATENT output: drop link 22, keep 16
n73 = nodes[73]
lat_out = next(o for o in n73["outputs"] if o["name"] == "LATENT")
lat_out["links"] = [l for l in (lat_out.get("links") or []) if l != 22]
d["links"].append([100, 60, 0, 53, 3, "LATENT"])
d["links"].append([101, 53, 0, 61, 3, "LATENT"])
d["links"].append([102, 61, 0, 54, 0, "LATENT"])
d["links"].append([103, 72, 0, 79, 5, "IMAGE"])

# ---- 8. save prefix
n29 = nodes[29]
n29["widgets_values"][0] = "k2f_jaisal_movie_shot_16x9"

json.dump(d, open(DST, "w", encoding="utf-8"), indent=1)
print("WROTE", DST)
print("nodes:", len(d["nodes"]), "links:", len(d["links"]))
