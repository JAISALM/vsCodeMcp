"""Build seedvr2_batch_upscale.json — ComfyUI workflow to upscale ONE video at a
time (preview / tweak). For the full batch of 8 clips, use
`batch_upscale_seedvr2.py` (CLI directory mode, model loaded once).

Chain:
  VHS_LoadVideoPath (video path) -> SeedVR2VideoUpscaler -> VHS_VideoCombine
  + SeedVR2LoadDiTModel (7B sharp fp16) + SeedVR2LoadVAEModel (ema_vae_fp16)

Widget shapes from object_info + verified memory note (seedvr2-image-upscale):
  - VHS_LoadVideoPath: [video, force_rate, custom_width, custom_height,
    frame_load_cap, skip_first_frames, select_every_nth, format]
  - SeedVR2LoadDiTModel: [model, device, offload_blocks, offload_device,
    attention_mode, compile, ...] (verified shape)
  - SeedVR2LoadVAEModel: [model, device, tiled, tile_h, tile_w, ...] (verified)
  - SeedVR2VideoUpscaler: [seed, randomize, resolution, max_resolution,
    batch_size, uniform_batch_size, color_correction, temporal_overlap,
    prepend_frames, input_noise_scale, latent_noise_scale, offload_device,
    enable_debug] (13 values)
  - VHS_VideoCombine: [frame_rate, loop_count, filename_prefix, format,
    pingpong, save_output]

To upscale a different clip: change the VHS_LoadVideoPath `video` widget to the
clip's filename (or full path). To change resolution: edit the
SeedVR2VideoUpscaler `resolution`/`max_resolution` widgets (1080/1920 = HD,
1440/2560 = 2K).
"""
import json, os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
DST = os.path.join(WF_DIR, "seedvr2_batch_upscale.json")

nodes = [
    {
        "id": 1, "type": "VHS_LoadVideoPath",
        "pos": [40, 200], "size": [340, 260], "flags": {}, "order": 0, "mode": 0,
        "inputs": [
            {"localized_name": "meta_batch", "name": "meta_batch", "type": "VHS_BatchManager", "widget": {"name": "meta_batch"}, "link": None},
            {"localized_name": "vae", "name": "vae", "type": "VAE", "widget": {"name": "vae"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [10]},
            {"localized_name": "frame_count", "name": "frame_count", "type": "INT", "links": None},
            {"localized_name": "audio", "name": "audio", "type": "AUDIO", "links": None},
            {"localized_name": "video_info", "name": "video_info", "type": "VHS_VIDEOINFO", "links": None},
            {"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": None},
        ],
        "properties": {"Node name for S&R": "VHS_LoadVideoPath"},
        "widgets_values": ["", 0.0, 0, 0, 0, 0, 1, "None"],
    },
    {
        "id": 2, "type": "SeedVR2LoadDiTModel",
        "pos": [40, 520], "size": [340, 220], "flags": {}, "order": 1, "mode": 0,
        "inputs": [],
        "outputs": [
            {"localized_name": "SEEDVR2_DIT", "name": "SEEDVR2_DIT", "type": "SEEDVR2_DIT", "links": [11]},
        ],
        "properties": {"Node name for S&R": "SeedVR2LoadDiTModel"},
        "widgets_values": ["seedvr2_ema_7b_sharp_fp16.safetensors", "cuda:0", 0, False, "none", False, "sdpa"],
    },
    {
        "id": 3, "type": "SeedVR2LoadVAEModel",
        "pos": [40, 780], "size": [340, 260], "flags": {}, "order": 2, "mode": 0,
        "inputs": [],
        "outputs": [
            {"localized_name": "SEEDVR2_VAE", "name": "SEEDVR2_VAE", "type": "SEEDVR2_VAE", "links": [12]},
        ],
        "properties": {"Node name for S&R": "SeedVR2LoadVAEModel"},
        "widgets_values": ["ema_vae_fp16.safetensors", "cuda:0", False, 1024, 128, False, 1024, 128, "false", "none", False],
    },
    {
        "id": 4, "type": "SeedVR2VideoUpscaler",
        "pos": [440, 300], "size": [340, 340], "flags": {}, "order": 3, "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "IMAGE", "widget": {"name": "image"}, "link": 10},
            {"localized_name": "dit", "name": "dit", "type": "SEEDVR2_DIT", "widget": {"name": "dit"}, "link": 11},
            {"localized_name": "vae", "name": "vae", "type": "SEEDVR2_VAE", "widget": {"name": "vae"}, "link": 12},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [13]},
        ],
        "properties": {"Node name for S&R": "SeedVR2VideoUpscaler"},
        # [seed, randomize, resolution, max_resolution, batch_size, uniform_batch_size,
        #  color_correction, temporal_overlap, prepend_frames, input_noise_scale,
        #  latent_noise_scale, offload_device, enable_debug]
        "widgets_values": [42, "randomize", 1080, 1920, 1, False, "lab", 0, 0, 0.0, 0.0, "cpu", False],
    },
    {
        "id": 5, "type": "VHS_VideoCombine",
        "pos": [840, 300], "size": [340, 300], "flags": {}, "order": 4, "mode": 0,
        "inputs": [
            {"localized_name": "images", "name": "images", "type": "IMAGE", "widget": {"name": "images"}, "link": 13},
            {"localized_name": "audio", "name": "audio", "type": "AUDIO", "widget": {"name": "audio"}, "link": None},
            {"localized_name": "meta_batch", "name": "meta_batch", "type": "VHS_BatchManager", "widget": {"name": "meta_batch"}, "link": None},
            {"localized_name": "vae", "name": "vae", "type": "VAE", "widget": {"name": "vae"}, "link": None},
        ],
        "outputs": [],
        "properties": {"Node name for S&R": "VHS_VideoCombine"},
        # [frame_rate, loop_count, filename_prefix, format, pingpong, save_output]
        "widgets_values": [24.0, 1, "jaisal_cut/upscaled", "video/h264-mp4", False, True],
    },
    {
        "id": 6, "type": "Note",
        "pos": [440, 40], "size": [740, 220], "flags": {}, "order": 5, "mode": 0,
        "inputs": [], "outputs": [],
        "properties": {},
        "widgets_values": [
            "SEEDVR2 BATCH UPSCALE (one clip at a time — for the full batch of 8, run\n"
            "utilities\\batch_upscale_seedvr2.py which uses CLI directory mode).\n\n"
            "1. Set the VHS_LoadVideoPath `video` widget to the clip filename (or full path).\n"
            "2. Resolution: SeedVR2VideoUpscaler widgets — 1080/1920 = HD, 1440/2560 = 2K.\n"
            "3. Queue Prompt -> output\\jaisal_cut\\upscaled\\<name>.mp4\n\n"
            "Model: seedvr2_ema_7b_sharp_fp16 (max quality). batch_size 1 (VRAM-safe).\n"
            "Source fps is preserved (24fps clips stay 24fps). NO audio in output —\n"
            "audio is added in post (DaVinci) with the dub."
        ],
    },
]

links = [
    [10, 1, 0, 4, 0, "IMAGE"],
    [11, 2, 0, 4, 1, "SEEDVR2_DIT"],
    [12, 3, 0, 4, 2, "SEEDVR2_VAE"],
    [13, 4, 0, 5, 0, "IMAGE"],
]

d = {"id": "seedvr2_batch_upscale", "version": 0.4, "last_node_id": 6,
     "last_link_id": 13, "nodes": nodes, "links": links,
     "groups": [], "extra": {}, "config": {}, "workflow": {}, "version": 0.4}
# dedupe version key
d = {"id": "seedvr2_batch_upscale", "version": 0.4, "last_node_id": 6,
     "last_link_id": 13, "nodes": nodes, "links": links,
     "groups": [], "extra": {}, "config": {}, "workflow": {}}

json.dump(d, open(DST, "w", encoding="utf-8"), indent=1)
print("WROTE", DST)
print("nodes:", len(nodes), "links:", len(links))
