# -*- coding: utf-8 -*-
"""
build_lora_training.py (2026-10-31)
Builds the character-LoRA training + test workflows (UI format, version 0.4):

  train_lora_jaisal.json / train_lora_zidhan.json
    LCOptimizer (Krea 2 Turbo, copied from v91 node 2888)
      -> LoadImageTextDataSetFromFolder (input\\lora_<char>)
      -> ShuffleImageTextDataset (seed 42)
      -> MakeTrainingDataset (vae, clip)
      -> TrainLoraNode (batch 1, grad_acc 1, steps 200 = 10 epochs on 20 imgs,
                        lr 1e-4, rank 16, AdamW, MSE, bf16/bf16, LoRA,
                        grad checkpointing, existing_lora [None])
      -> SaveLoRA (prefix loras/<trigger>_<char> -> output\\loras\\<...>_200_steps_00001_.safetensors)
      -> LossGraphNode (loss graph image -> output\\lora_trainloss_<char>_*)

  test_lora_<char>.json
    LCOptimizer -> LoraLoaderModelOnly (<trigger>_<char>, 1.0)
    + CLIPTextEncode (trigger prompt) + EmptyLatentImage 896x1152
    + KSampler (seed 13, 10 steps, cfg 1, euler/simple, denoise 1)
    + VAEDecode + SaveImage (lora_test_<char>)

NOTE (combo staleness): LoadImageTextDataSetFromFolder.folder and
LoraLoaderModelOnly.lora_name are dynamic combos computed at ComfyUI startup.
The validator will flag the NEW folder names / the NOT-YET-EXISTING lora file
until ComfyUI is restarted AFTER the dataset folders exist and the LoRA is
trained. That is expected — restart ComfyUI once, then queue.
"""
import json, copy, os, uuid

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
V91 = os.path.join(WF, "krea2_v91_dataset_jaisal.json")
TRAIN_PARAMS = [1, 1, 200, 0.0001, 16, "AdamW", "MSE", 42, "bf16", "bf16",
                False, "LoRA", True, 1, False, "[None]", False, False]
CHARS = [
    # char, dataset_folder, lora_name, test_prompt
    ("jaisal", "lora_jaisal", "jeskvman_jaisal",
     "jeskvman, young Keralite man, about 26, medium fair skin with soft natural tan, "
     "medium wavy black hair falling to eyebrow length, clean-shaven faint stubble, lean slim build, "
     "black t-shirt, standing near Kerala backwaters, soft natural light, photorealistic, 35mm"),
    ("zidhan", "lora_zidhan", "dlorman_zidhan",
     "dlorman, young Keralite man, about 26, medium fair skin with soft natural tan, "
     "short neat black hair, full short dense black beard, lean slim build, "
     "white t-shirt, standing in a Kerala coconut grove, soft natural light, photorealistic, 35mm"),
]

def widget_input(name, type_):
    return {"name": name, "type": type_, "widget": {"name": name}, "link": None}

def link_input(name, type_, link):
    return {"name": name, "type": type_, "link": link}

def out(name, type_, links):
    return {"name": name, "type": type_, "links": links}

def base_node(nid, ntype, pos, size, inputs, outputs, widgets):
    return {
        "id": nid, "type": ntype, "pos": pos, "size": size, "flags": {},
        "order": nid - 10, "mode": 0, "inputs": inputs, "outputs": outputs,
        "properties": {"Node name for S&R": ntype},
        "widgets_values": widgets,
    }

# LCOptimizer widget values (schema order: 12 required + spectrum optional).
# POSITIONAL list = v91's placeholder values — every entry is a VALID combo
# option, so the validator passes (real subfolder paths like
# 'Krea 2\\Your models\\...' are NOT in the cached combo options).
# The REAL resolved file paths live in widgets_values_named — the UI prefers
# the named dict (proven: the v91 canvas, carrying these same placeholders
# positionally, loaded Krealism_V3.1_int8_convrot.safetensors in every run).
# The MCP converter reads only widgets_values, so placeholder positionals are
# also the correct backend-safe choice (it never sees the named dict).
LCOPT_PLACEHOLDER = [
    "Krea 2 (Turbo)", "Optimal", "★ Recommended", "★ Recommended",
    "★ Recommended", "Auto", "auto", "auto", "auto", "off", "auto",
    "auto", "auto",
]

def lcopt_node(nid, outputs_links, v91_nodes):
    # copy the proven LCOptimizer node from v91 (shape + REAL named values),
    # rewire outputs, force placeholder positionals
    src = next(n for n in v91_nodes if n["id"] == 2888)
    n = copy.deepcopy(src)
    n["id"] = nid
    n["widgets_values"] = list(LCOPT_PLACEHOLDER)
    # deep-copied widgets_values_named already carries the real file paths
    # (model_file / text_encoder / vae) — the UI's runtime source of truth.
    for i, o in enumerate(n["outputs"]):
        o["links"] = [outputs_links[i]] if outputs_links[i] else None
    n["properties"] = {"Node name for S&R": "LCOptimizer"}
    n["pos"] = [-3740, -3040]
    return n

def mklinks(*tuples):
    # native format: 6-element LISTS — the converter's _build_link_map skips
    # dict-form links entirely (isinstance(link, (list, tuple)) check).
    return [[lid, f, fs, t, ts, ty] for (lid, f, fs, t, ts, ty) in tuples]

def header(last_node, last_link):
    return {
        "id": str(uuid.uuid4()), "version": 0.4, "config": {}, "extra": {},
        "revision": 0, "last_node_id": last_node, "last_link_id": last_link,
    }

def save(fname, header_data, nodes, links):
    d = dict(header_data)
    d["nodes"] = nodes
    d["links"] = links
    d["groups"] = []
    p = os.path.join(WF, fname)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("saved", p)

v91 = json.load(open(V91, encoding="utf-8"))

# ---------------- TRAIN FILE ----------------
for char, ds, lora_name, test_prompt in CHARS:
    train_params = list(TRAIN_PARAMS)
    nodes = []
    links = []

    nodes.append(lcopt_node(10, [1, 6, 5, None], v91["nodes"]))  # 10 LCOptimizer

    nodes.append(base_node(11, "LoadImageTextDataSetFromFolder", [-3260, -3040], [320, 120],
        [widget_input("folder", "COMBO")],
        [out("images", "IMAGE", [2]), out("texts", "STRING", [3])],
        [ds]))

    nodes.append(base_node(12, "ShuffleImageTextDataset", [-2900, -3040], [320, 140],
        [link_input("images", "IMAGE", 2),
         link_input("texts", "STRING", 3),
         widget_input("seed", "INT")],
        [out("images", "IMAGE", [4]), out("texts", "STRING", [7])],
        [42]))

    nodes.append(base_node(13, "MakeTrainingDataset", [-2540, -3040], [320, 180],
        [link_input("images", "IMAGE", 4),
         link_input("vae", "VAE", 5),
         link_input("clip", "CLIP", 6),
         link_input("texts", "STRING", 7)],
        [out("latents", "LATENT", [8]), out("conditioning", "CONDITIONING", [9])],
        []))

    train_inputs = [
        link_input("model", "MODEL", 1),
        link_input("latents", "LATENT", 8),
        link_input("positive", "CONDITIONING", 9),
        widget_input("batch_size", "INT"),
        widget_input("grad_accumulation_steps", "INT"),
        widget_input("steps", "INT"),
        widget_input("learning_rate", "FLOAT"),
        widget_input("rank", "INT"),
        widget_input("optimizer", "COMBO"),
        widget_input("loss_function", "COMBO"),
        widget_input("seed", "INT"),
        widget_input("training_dtype", "COMBO"),
        widget_input("lora_dtype", "COMBO"),
        widget_input("quantized_backward", "BOOLEAN"),
        widget_input("algorithm", "COMBO"),
        widget_input("gradient_checkpointing", "BOOLEAN"),
        widget_input("checkpoint_depth", "INT"),
        widget_input("offloading", "BOOLEAN"),
        widget_input("existing_lora", "COMBO"),
        widget_input("bucket_mode", "BOOLEAN"),
        widget_input("bypass_mode", "BOOLEAN"),
    ]
    nodes.append(base_node(14, "TrainLoraNode", [-2180, -3040], [360, 460],
        train_inputs,
        [out("lora", "LORA_MODEL", [10]),
         out("loss_map", "LOSS_MAP", [11]),
         out("steps", "INT", [])],
        train_params))

    nodes.append(base_node(15, "SaveLoRA", [-1780, -3040], [340, 140],
        [link_input("lora", "LORA_MODEL", 10),
         widget_input("prefix", "STRING")],
        [],
        ["loras/" + lora_name]))

    nodes.append(base_node(16, "LossGraphNode", [-1780, -2840], [340, 120],
        [link_input("loss", "LOSS_MAP", 11),
         widget_input("filename_prefix", "STRING")],
        [],
        ["lora_trainloss_" + char]))

    links = mklinks(
        (1,  10, 0, 14, 0, "MODEL"),
        (2,  11, 0, 12, 0, "IMAGE"),
        (3,  11, 1, 12, 1, "STRING"),
        (4,  12, 0, 13, 0, "IMAGE"),
        (5,  10, 2, 13, 1, "VAE"),
        (6,  10, 1, 13, 2, "CLIP"),
        (7,  12, 1, 13, 3, "STRING"),
        (8,  13, 0, 14, 1, "LATENT"),
        (9,  13, 1, 14, 2, "CONDITIONING"),
        (10, 14, 0, 15, 0, "LORA_MODEL"),
        (11, 14, 1, 16, 0, "LOSS_MAP"),
    )
    save("train_lora_%s.json" % char, header(16, 11), nodes, links)

# ---------------- TEST FILE ----------------
for char, ds, lora_name, test_prompt in CHARS:
    nodes = []
    links = []

    nodes.append(lcopt_node(10, [1, 2, 8, None], v91["nodes"]))  # model->11, clip->12, vae->15

    nodes.append(base_node(11, "LoraLoaderModelOnly", [-3260, -3040], [320, 140],
        [link_input("model", "MODEL", 1),
         widget_input("lora_name", "COMBO"),
         widget_input("strength_model", "FLOAT")],
        [out("model", "MODEL", [3])],
        [lora_name, 1.0]))

    nodes.append(base_node(12, "CLIPTextEncode", [-3260, -2840], [400, 200],
        [link_input("clip", "CLIP", 2),
         widget_input("text", "STRING")],
        [out("CONDITIONING", "CONDITIONING", [4, 5])],
        [test_prompt]))

    nodes.append(base_node(13, "EmptyLatentImage", [-2800, -3040], [300, 140],
        [],
        [out("LATENT", "LATENT", [6])],
        [896, 1152, 1]))

    # Native KSampler widgets_values = [seed, control_after_generate, steps, cfg,
    # sampler_name, scheduler, denoise] — the control slot MUST be one of
    # fixed/increment/decrement/randomize or the converter shifts every later
    # widget. "fixed" = the seed stays fixed (determinism, matches v91 intent).
    # The object_info input name is 'latent_image' (not 'latent').
    nodes.append(base_node(14, "KSampler", [-2460, -2840], [320, 260],
        [link_input("model", "MODEL", 3),
         widget_input("seed", "INT"),
         widget_input("steps", "INT"),
         widget_input("cfg", "FLOAT"),
         widget_input("sampler_name", "COMBO"),
         widget_input("scheduler", "COMBO"),
         widget_input("denoise", "FLOAT"),
         link_input("positive", "CONDITIONING", 4),
         link_input("negative", "CONDITIONING", 5),
         link_input("latent_image", "LATENT", 6)],
        [out("LATENT", "LATENT", [7])],
        [13, "fixed", 10, 1.0, "euler", "simple", 1.0]))

    nodes.append(base_node(15, "VAEDecode", [-2100, -2840], [300, 100],
        [link_input("samples", "LATENT", 7),
         link_input("vae", "VAE", 8)],
        [out("IMAGE", "IMAGE", [9])],
        []))

    nodes.append(base_node(16, "SaveImage", [-1760, -2840], [320, 120],
        [link_input("images", "IMAGE", 9),
         widget_input("filename_prefix", "STRING")],
        [],
        ["lora_test_" + char]))

    links = mklinks(
        (1, 10, 0, 11, 0, "MODEL"),
        (2, 10, 1, 12, 0, "CLIP"),
        (3, 11, 0, 14, 0, "MODEL"),
        (4, 12, 0, 14, 8, "CONDITIONING"),
        (5, 12, 0, 14, 9, "CONDITIONING"),
        (6, 13, 0, 14, 10, "LATENT"),
        (7, 14, 0, 15, 0, "LATENT"),
        (8, 10, 2, 15, 1, "VAE"),
        (9, 15, 0, 16, 0, "IMAGE"),
    )
    save("test_lora_%s.json" % char, header(16, 9), nodes, links)

print("done")
