r"""Build a SeedVR2 single-IMAGE upscale workflow (UI format).

Uses the numz ComfyUI-SeedVR2_VideoUpscaler nodes (image-capable, batch_size=1).
Native widgets_values shapes copied from the official example workflow so the
server maps values correctly (the upscaler has a hidden 'randomize' widget after
seed, same pattern as KSampler).

Usage:
    & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\build_seedvr2_image_wf.py" <input_filename.png> [out_prefix]

Example:
    ... build_seedvr2_image_wf.py kf5_plants_alive_v9_00004_.png seedvr2_2k_kf5

Writes to the ComfyUI workflows folder and validates via MCP is done separately.
"""
import json, sys, os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# --- parameters (override via argv) ---
INPUT_IMG = sys.argv[1] if len(sys.argv) > 1 else "kf5_plants_alive_v9_00004_.png"
OUT_PREFIX = sys.argv[2] if len(sys.argv) > 2 else "seedvr2_2k"

DIT_MODEL = "seedvr2_ema_7b_sharp_fp16.safetensors"   # max quality, already local
VAE_MODEL = "ema_vae_fp16.safetensors"
RESOLUTION = 1440        # target shortest edge -> ~2K
MAX_RESOLUTION = 2560    # cap longest edge
BATCH_SIZE = 1           # single image (4n+1; 1 = single image per docs)
COLOR_CORR = "lab"       # perceptual, recommended
ATTENTION = "sdpa"       # stable, always available

nodes = [
    {
        "id": 1, "type": "LoadImage",
        "pos": [40, 200], "size": [320, 340], "flags": {}, "order": 0, "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
            {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [10]},
            {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
        ],
        "properties": {"Node name for S&R": "LoadImage"},
        "widgets_values": [INPUT_IMG, "image"],
    },
    {
        "id": 2, "type": "SeedVR2LoadDiTModel",
        "pos": [40, 600], "size": [340, 300], "flags": {}, "order": 1, "mode": 0,
        "inputs": [
            {"localized_name": "model", "name": "model", "type": "COMBO", "widget": {"name": "model"}, "link": None},
            {"localized_name": "device", "name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None},
            {"localized_name": "blocks_to_swap", "name": "blocks_to_swap", "type": "INT", "widget": {"name": "blocks_to_swap"}, "link": None},
            {"localized_name": "swap_io_components", "name": "swap_io_components", "type": "BOOLEAN", "widget": {"name": "swap_io_components"}, "link": None},
            {"localized_name": "offload_device", "name": "offload_device", "type": "COMBO", "widget": {"name": "offload_device"}, "link": None},
            {"localized_name": "cache_model", "name": "cache_model", "type": "BOOLEAN", "widget": {"name": "cache_model"}, "link": None},
            {"localized_name": "attention_mode", "name": "attention_mode", "type": "COMBO", "widget": {"name": "attention_mode"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "SEEDVR2_DIT", "name": "SEEDVR2_DIT", "type": "SEEDVR2_DIT", "links": [11]},
        ],
        "properties": {"Node name for S&R": "SeedVR2LoadDiTModel"},
        "widgets_values": [DIT_MODEL, "cuda:0", 0, False, "none", False, ATTENTION],
    },
    {
        "id": 3, "type": "SeedVR2LoadVAEModel",
        "pos": [40, 950], "size": [340, 360], "flags": {}, "order": 2, "mode": 0,
        "inputs": [
            {"localized_name": "model", "name": "model", "type": "COMBO", "widget": {"name": "model"}, "link": None},
            {"localized_name": "device", "name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None},
            {"localized_name": "encode_tiled", "name": "encode_tiled", "type": "BOOLEAN", "widget": {"name": "encode_tiled"}, "link": None},
            {"localized_name": "encode_tile_size", "name": "encode_tile_size", "type": "INT", "widget": {"name": "encode_tile_size"}, "link": None},
            {"localized_name": "encode_tile_overlap", "name": "encode_tile_overlap", "type": "INT", "widget": {"name": "encode_tile_overlap"}, "link": None},
            {"localized_name": "decode_tiled", "name": "decode_tiled", "type": "BOOLEAN", "widget": {"name": "decode_tiled"}, "link": None},
            {"localized_name": "decode_tile_size", "name": "decode_tile_size", "type": "INT", "widget": {"name": "decode_tile_size"}, "link": None},
            {"localized_name": "decode_tile_overlap", "name": "decode_tile_overlap", "type": "INT", "widget": {"name": "decode_tile_overlap"}, "link": None},
            {"localized_name": "tile_debug", "name": "tile_debug", "type": "COMBO", "widget": {"name": "tile_debug"}, "link": None},
            {"localized_name": "offload_device", "name": "offload_device", "type": "COMBO", "widget": {"name": "offload_device"}, "link": None},
            {"localized_name": "cache_model", "name": "cache_model", "type": "BOOLEAN", "widget": {"name": "cache_model"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "SEEDVR2_VAE", "name": "SEEDVR2_VAE", "type": "SEEDVR2_VAE", "links": [12]},
        ],
        "properties": {"Node name for S&R": "SeedVR2LoadVAEModel"},
        "widgets_values": [VAE_MODEL, "cuda:0", False, 1024, 128, False, 1024, 128, "false", "none", False],
    },
    {
        "id": 4, "type": "SeedVR2VideoUpscaler",
        "pos": [440, 500], "size": [360, 420], "flags": {}, "order": 3, "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "IMAGE", "link": 10},
            {"localized_name": "dit", "name": "dit", "type": "SEEDVR2_DIT", "link": 11},
            {"localized_name": "vae", "name": "vae", "type": "SEEDVR2_VAE", "link": 12},
            {"localized_name": "seed", "name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": None},
            {"localized_name": "resolution", "name": "resolution", "type": "INT", "widget": {"name": "resolution"}, "link": None},
            {"localized_name": "max_resolution", "name": "max_resolution", "type": "INT", "widget": {"name": "max_resolution"}, "link": None},
            {"localized_name": "batch_size", "name": "batch_size", "type": "INT", "widget": {"name": "batch_size"}, "link": None},
            {"localized_name": "uniform_batch_size", "name": "uniform_batch_size", "type": "BOOLEAN", "widget": {"name": "uniform_batch_size"}, "link": None},
            {"localized_name": "color_correction", "name": "color_correction", "type": "COMBO", "widget": {"name": "color_correction"}, "link": None},
            {"localized_name": "temporal_overlap", "name": "temporal_overlap", "type": "INT", "widget": {"name": "temporal_overlap"}, "link": None},
            {"localized_name": "prepend_frames", "name": "prepend_frames", "type": "INT", "widget": {"name": "prepend_frames"}, "link": None},
            {"localized_name": "input_noise_scale", "name": "input_noise_scale", "type": "FLOAT", "widget": {"name": "input_noise_scale"}, "link": None},
            {"localized_name": "latent_noise_scale", "name": "latent_noise_scale", "type": "FLOAT", "widget": {"name": "latent_noise_scale"}, "link": None},
            {"localized_name": "offload_device", "name": "offload_device", "type": "COMBO", "widget": {"name": "offload_device"}, "link": None},
            {"localized_name": "enable_debug", "name": "enable_debug", "type": "BOOLEAN", "widget": {"name": "enable_debug"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [13]},
        ],
        "properties": {"Node name for S&R": "SeedVR2VideoUpscaler"},
        # native order: seed, [hidden randomize], resolution, max_resolution,
        # batch_size, uniform_batch_size, color_correction, temporal_overlap,
        # prepend_frames, input_noise_scale, latent_noise_scale, offload_device, enable_debug
        "widgets_values": [42, "randomize", RESOLUTION, MAX_RESOLUTION, BATCH_SIZE, False, COLOR_CORR, 0, 0, 0, 0, "cpu", False],
    },
    {
        "id": 5, "type": "SaveImage",
        "pos": [860, 500], "size": [340, 340], "flags": {}, "order": 4, "mode": 0,
        "inputs": [
            {"localized_name": "images", "name": "images", "type": "IMAGE", "link": 13},
            {"localized_name": "filename_prefix", "name": "filename_prefix", "type": "STRING", "widget": {"name": "filename_prefix"}, "link": None},
        ],
        "outputs": [],
        "properties": {"Node name for S&R": "SaveImage"},
        "widgets_values": [OUT_PREFIX],
    },
]

links = [
    [10, 1, 0, 4, 0, "IMAGE"],   # LoadImage.IMAGE -> Upscaler.image
    [11, 2, 0, 4, 1, "SEEDVR2_DIT"],  # DiT -> Upscaler.dit
    [12, 3, 0, 4, 2, "SEEDVR2_VAE"],  # VAE -> Upscaler.vae
    [13, 4, 0, 5, 0, "IMAGE"],   # Upscaler.IMAGE -> SaveImage.images
]

wf = {
    "id": "seedvr2-image-upscale",
    "revision": 0,
    "last_node_id": 5,
    "last_link_id": 13,
    "nodes": nodes,
    "links": links,
    "groups": [],
    "config": {},
    "extra": {},
    "version": 0.4,
}

out_path = os.path.join(WF_DIR, "seedvr2_image_upscale.json")
json.dump(wf, open(out_path, "w", encoding="utf-8"), indent=1)
print("WROTE", out_path)
print("input:", INPUT_IMG, "| prefix:", OUT_PREFIX)
print("model:", DIT_MODEL, "| res:", RESOLUTION, "max:", MAX_RESOLUTION, "| batch:", BATCH_SIZE)
