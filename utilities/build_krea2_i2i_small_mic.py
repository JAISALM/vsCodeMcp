"""Build a CLEAN Krea2 i2i workflow: base image (table empty.png) + good prompt -> small mic + papers.

This is "the same trick" as the refs: i2i with a good prompt + a better base image
(NOT t2i, NOT the inpaint workflow).

Chain:
  LoadImage (table empty.png) -> VAEEncode -> KSampler (denoise 0.6) -> VAEDecode -> SaveImage
  UNETLoader (krea2_turbo_bf16) -> KSampler.model
  CLIPLoader (qwen3vl_4b_fp8, krea2) -> CLIPTextEncode pos/neg -> KSampler
  VAELoader (qwen_image_vae) -> VAEEncode.vae + VAEDecode.vae

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_krea2_i2i_small_mic.py"
"""
import json, os

DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_i2i_small_mic.json"
BASE = "table empty.png"

PROMPT = (
    "A weathered wooden table with a single empty wooden chair behind it, a single bare bulb "
    "hanging from a thin wire above, pure black void background. On the table sits a SMALL "
    "compact studio microphone on a SHORT LOW stand, with a few loose sheets of paper with "
    "dense handwriting scattered on the table surface. Black and white, high contrast, clean "
    "smooth image, no grain, static camera, medium-wide."
)
NEGATIVE = (
    "color, any color, warm tones, multiple light sources, bright background, other objects, "
    "multiple objects, person, human, face, text watermark, logo, blurry, low quality, noise, "
    "grain, speckles, large microphone, tall stand, tall object, multiple microphones, "
    "broadcast mic, big mic"
)

def node(id, type, pos, size, widgets, inputs, outputs, title=None):
    n = {
        "id": id, "type": type, "pos": pos, "size": size, "flags": {},
        "order": id, "mode": 0, "inputs": inputs, "outputs": outputs,
        "properties": {"Node name for S&R": type}, "widgets_values": widgets,
    }
    if title:
        n["title"] = title
    return n

nodes = [
    node(1, "UNETLoader", [40, 40], [320, 60], ["krea2_turbo_bf16.safetensors", "default"],
         [], [{"name": "MODEL", "type": "MODEL", "links": [100]}], "UNet (bf16 krea)"),
    node(2, "CLIPLoader", [40, 140], [320, 100], ["qwen3vl_4b_fp8_scaled.safetensors", "krea2", "default"],
         [], [{"name": "CLIP", "type": "CLIP", "links": [101, 102]}], "CLIP (krea2)"),
    node(3, "VAELoader", [40, 280], [320, 60], ["qwen_image_vae.safetensors"],
         [], [{"name": "VAE", "type": "VAE", "links": [103, 104]}], "VAE"),
    node(4, "LoadImage", [40, 380], [320, 320], [BASE, "image"],
         [{"name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
          {"name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None}],
         [{"name": "IMAGE", "type": "IMAGE", "links": [105]},
          {"name": "MASK", "type": "MASK", "links": None}], "Base image"),
    node(5, "CLIPTextEncode", [420, 40], [400, 200], [PROMPT],
         [{"name": "clip", "type": "CLIP", "link": 101}],
         [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [106]}], "Positive (good prompt)"),
    node(6, "CLIPTextEncode", [420, 280], [400, 200], [NEGATIVE],
         [{"name": "clip", "type": "CLIP", "link": 102}],
         [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [107]}], "Negative"),
    node(7, "VAEEncode", [420, 520], [320, 80], [],
         [{"name": "pixels", "type": "IMAGE", "link": 105},
          {"name": "vae", "type": "VAE", "link": 103}],
         [{"name": "LATENT", "type": "LATENT", "links": [108]}], "Encode base"),
    node(8, "KSampler", [860, 40], [320, 160], [42, "randomize", 10, 1, "euler", "simple", 0.6],
         [{"name": "model", "type": "MODEL", "link": 100},
          {"name": "positive", "type": "CONDITIONING", "link": 106},
          {"name": "negative", "type": "CONDITIONING", "link": 107},
          {"name": "latent_image", "type": "LATENT", "link": 108}],
         [{"name": "LATENT", "type": "LATENT", "links": [109]}], "KSampler (denoise 0.6)"),
    node(9, "VAEDecode", [1220, 40], [320, 80], [],
         [{"name": "samples", "type": "LATENT", "link": 109},
          {"name": "vae", "type": "VAE", "link": 104}],
         [{"name": "IMAGE", "type": "IMAGE", "links": [110]}], "Decode"),
    node(10, "SaveImage", [1220, 160], [320, 120], ["jaisal_cut/mic_small_i2i"],
         [{"name": "images", "type": "IMAGE", "link": 110}],
         [], "Save (mic_small_i2i)"),
]

links = [
    [100, 1, 0, 8, 0, "MODEL"],
    [101, 2, 0, 5, 0, "CLIP"],
    [102, 2, 0, 6, 0, "CLIP"],
    [103, 3, 0, 7, 1, "VAE"],
    [104, 3, 0, 9, 1, "VAE"],
    [105, 4, 0, 7, 0, "IMAGE"],
    [106, 5, 0, 8, 1, "CONDITIONING"],
    [107, 6, 0, 8, 2, "CONDITIONING"],
    [108, 7, 0, 8, 3, "LATENT"],
    [109, 8, 0, 9, 0, "LATENT"],
    [110, 9, 0, 10, 0, "IMAGE"],
]

wf = {
    "id": "krea2_i2i_small_mic", "revision": 0, "last_node_id": 10, "last_link_id": 110,
    "nodes": nodes, "links": links, "groups": [], "definitions": {}, "config": {},
    "extra": {}, "version": 0.4,
}

os.makedirs(os.path.dirname(DST), exist_ok=True)
json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)
print("wrote:", DST)
print("base:", BASE)
print("denoise: 0.6, steps 10, cfg 1, euler/simple")
print("save: jaisal_cut/mic_small_i2i")
