"""Build `seedvr2_lastframe_2k.json` — video -> LAST FRAME -> 2K image, in one go.

Pipeline (single run):
  LoadVideo -> GetVideoComponents -> GetImageRangeFromBatch[-1,1]
            -> SeedVR2VideoUpscaler (1080 shortest-edge, batch=1) -> SaveImage

Purpose: take the LAST frame of a generated (or already-upscaled) shot video,
upscale it to 2K (1920x1080), and save it as a PNG. That PNG becomes the
ref_image_0 (start anchor) of the NEXT shot's H3 R2V workflow -> seamless
stitch, no glitch.

Native widget shapes cloned from the proven `seedvr2_video_upscale.json`
(official SeedVR2 example) so the UI renders + validates clean.

Usage:
  python build_seedvr2_lastframe_2k.py [default_video.mp4] [save_prefix]
  (defaults: jaisal_intro_C_starting_2ref_00006_.mp4, lastframe_2k)
"""
import json
import sys
import os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
OUT = os.path.join(WF_DIR, "seedvr2_lastframe_2k.json")

default_video = sys.argv[1] if len(sys.argv) > 1 else "jaisal_intro_C_starting_2ref_00006_.mp4"
save_prefix = sys.argv[2] if len(sys.argv) > 2 else "lastframe_2k"


def node(id, ntype, pos, size, order, mode, inputs, outputs, props, widgets, **extra):
    d = {
        "id": id,
        "type": ntype,
        "pos": pos,
        "size": size,
        "flags": {},
        "order": order,
        "mode": mode,
        "inputs": inputs,
        "outputs": outputs,
        "properties": props,
        "widgets_values": widgets,
    }
    d.update(extra)
    return d


def link_input(localized, name, ltype, widget_name=None, link=None):
    d = {"localized_name": localized, "name": name, "type": ltype, "link": link}
    if widget_name:
        d["widget"] = {"name": widget_name}
    return d


def link_output(localized, name, ltype, links):
    return {"localized_name": localized, "name": name, "type": ltype, "links": links}


# ---- Node 21: LoadVideo (default = the shot video to extract the last frame from)
n21 = node(
    21, "LoadVideo", [-201.66, -266.87], [274.08, 228.17], 2, 0,
    inputs=[
        link_input("file", "file", "COMBO", "file", None),
        link_input("choose file to upload", "upload", "IMAGEUPLOAD", "upload", None),
    ],
    outputs=[link_output("VIDEO", "VIDEO", "VIDEO", [20])],
    props={"cnr_id": "comfy-core", "ver": "0.3.68", "Node name for S&R": "LoadVideo"},
    widgets=[default_video, "image"],
)

# ---- Node 22: GetVideoComponents (VIDEO -> IMAGE batch)
n22 = node(
    22, "GetVideoComponents", [149.29, -267.41], [185.18, 66], 6, 0,
    inputs=[link_input("video", "video", "VIDEO", None, 20)],
    outputs=[
        link_output("images", "images", "IMAGE", [21]),
        link_output("audio", "audio", "AUDIO", []),
    ],
    props={"cnr_id": "comfy-core", "ver": "0.3.68", "Node name for S&R": "GetVideoComponents"},
    widgets=[],
)

# ---- Node 30: GetImageRangeFromBatch (start_index=-1 -> LAST frame, num_frames=1)
n30 = node(
    30, "GetImageRangeFromBatch", [400.0, -267.41], [240.0, 80.0], 7, 0,
    inputs=[
        link_input("images", "images", "IMAGE", None, 21),
        link_input("masks", "masks", "MASK", None, None),
    ],
    outputs=[
        link_output("IMAGE", "IMAGE", "IMAGE", [26]),
        link_output("MASK", "MASK", "MASK", []),
    ],
    props={"Node name for S&R": "GetImageRangeFromBatch"},
    widgets=[-1, 1],
)

# ---- Node 14: SeedVR2LoadDiTModel (7B Sharp FP16 = max quality)
n14 = node(
    14, "SeedVR2LoadDiTModel", [-369.51, 315.09], [307.67, 178], 0, 0,
    inputs=[],
    outputs=[link_output("DIT", "DIT", "SEEDVR2_DIT", [27])],
    props={"aux_id": "ainvfx/ComfyUI-SeedVR2_VideoUpscaler", "Node name for S&R": "SeedVR2LoadDiTModel"},
    widgets=["seedvr2_ema_7b_sharp_fp16.safetensors", "cuda:0", 0, False, "cpu", False, "sdpa"],
)

# ---- Node 13: SeedVR2LoadVAEModel (ema_vae_fp16, tiled)
n13 = node(
    13, "SeedVR2LoadVAEModel", [-369.51, 550.0], [307.67, 220], 1, 0,
    inputs=[],
    outputs=[link_output("VAE", "VAE", "SEEDVR2_VAE", [28])],
    props={"aux_id": "ainvfx/ComfyUI-SeedVR2_VideoUpscaler", "Node name for S&R": "SeedVR2LoadVAEModel"},
    widgets=["ema_vae_fp16.safetensors", "cuda:0", True, 1024, 128, True, 768, 128, "false", "cpu", False],
)

# ---- Node 10: SeedVR2VideoUpscaler (1080 shortest-edge -> 1920x1080, batch=1)
n10 = node(
    10, "SeedVR2VideoUpscaler", [650.0, -267.41], [320.0, 260], 8, 0,
    inputs=[
        link_input("image", "image", "IMAGE", None, 26),
        link_input("dit", "dit", "SEEDVR2_DIT", None, 27),
        link_input("vae", "vae", "SEEDVR2_VAE", None, 28),
    ],
    outputs=[link_output("IMAGE", "IMAGE", "IMAGE", [29])],
    props={"aux_id": "ainvfx/ComfyUI-SeedVR2_VideoUpscaler", "Node name for S&R": "SeedVR2VideoUpscaler"},
    # [seed, control_after_generate, resolution, max_resolution, batch_size,
    #  use_alpha, color_correction, ?, ?, ?, ?, offload_device, ?]
    # batch_size=1 (single last-frame image), resolution=1080 (shortest edge)
    widgets=[42, "fixed", 1080, 0, 1, True, "lab", 3, 0, 0, 0, "cpu", False],
)

# ---- Node 31: SaveImage (the 2K last frame)
n31 = node(
    31, "SaveImage", [950.0, -267.41], [270.0, 249.88], 9, 0,
    inputs=[
        link_input("images", "images", "IMAGE", None, 29),
        link_input("filename_prefix", "filename_prefix", "STRING", "filename_prefix", None),
    ],
    outputs=[],
    props={"cnr_id": "comfy-core", "ver": "0.3.68", "Node name for S&R": "SaveImage"},
    widgets=[save_prefix],
)

# ---- Note
n_note = node(
    32, "Note", [400.0, -120.0], [300.0, 120], 0, 0,
    inputs=[], outputs=[], props={},
    widgets=["LAST FRAME -> 2K\n\n1. Set LoadVideo to the shot video (original OR already-upscaled).\n"
             "2. GetImageRangeFromBatch start_index=-1 grabs the LAST frame.\n"
             "3. Upscaler 1080 shortest-edge -> 1920x1080 (2K), batch=1.\n"
             "4. SaveImage writes the 2K last frame -> use as next shot's ref_image_0."],
    color="#432", bgcolor="#653",
)

# Native UI link format: [id, from_node, from_slot, to_node, to_slot, type]
links = [
    [20, 21, 0, 22, 0, "VIDEO"],
    [21, 22, 0, 30, 0, "IMAGE"],
    [26, 30, 0, 10, 0, "IMAGE"],
    [27, 14, 0, 10, 1, "SEEDVR2_DIT"],
    [28, 13, 0, 10, 2, "SEEDVR2_VAE"],
    [29, 10, 0, 31, 0, "IMAGE"],
]

wf = {
    "id": "lastframe-2k-0001",
    "revision": 0,
    "last_node_id": 32,
    "last_link_id": 29,
    "nodes": [n21, n22, n30, n14, n13, n10, n31, n_note],
    "links": links,
    "version": 4,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=1)

print("WROTE", OUT)
print("default_video =", default_video)
print("save_prefix   =", save_prefix)
