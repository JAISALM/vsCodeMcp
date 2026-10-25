#!/usr/bin/env python
"""Check availability for the patreon Fizgig workflow: nodes + model files."""
import json, os, urllib.request

raw = urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60).read().decode("utf-8", "replace")
print("=== NODES ===")
for name in ["CLIPLoaderGGUF", "H3SLAAttention", "MiniMaxChunkFeedForward", "MiniMaxLowVRAMAttention",
             "MiniMaxH3SigmaShift", "ImageScaleToTotalPixels", "easy cleanGpuUsed",
             "FizgigH3StillDecode", "FizgigH3StillLatent", "MiniMaxH3ReferenceToVideo",
             "PrimitiveInt", "LoadImageListFromDir //Inspire"]:
    print(("OK  " if raw.find('"' + name + '"') >= 0 else "MISS"), name)

base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models"
print("\n=== MODEL FILES ===")
cands = {
    "UNET patreon": os.path.join(base, "diffusion_models", "minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors"),
    "VAE video int8": os.path.join(base, "vae", "minimax_h3_video_vae_int8_convrot.safetensors"),
    "GGUF CLIP": os.path.join(base, "gguf", "minimax", "qwen3vl-32B-MiniMax-H3-Q2_K.gguf"),
}
for label, p in cands.items():
    print(("EXISTS " if os.path.exists(p) else "MISSING"), f"{label}: {p}")

# search for any gguf files + patreon unet anywhere in models/
print("\n=== SEARCH ===")
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".gguf") or "fused_refdelta" in f or "mystic" in f:
            print(os.path.join(root, f))
