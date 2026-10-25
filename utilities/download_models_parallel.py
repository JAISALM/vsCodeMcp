#!/usr/bin/env python
"""Parallel HuggingFace model downloader (browser UA, threaded, Range-resumable).

Downloads the character-pipeline models in parallel and reports per-file status.
Resumes existing .part files via HTTP Range.
"""
import concurrent.futures
import os
import urllib.request

MODELS = [
    # P3 H3 character sheet
    (
        "https://huggingface.co/Mamad8/MiniMax-H3-Image-VAE/resolve/main/minimax_h3_t1_image_vae_step1597.safetensors",
        r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\vae\minimax_h3_t1_image_vae_step1597.safetensors",
    ),
    (
        "https://huggingface.co/Comfy-Org/Gemma4/resolve/main/text_encoders/gemma4_e4b_it_fp8_scaled.safetensors",
        r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\text_encoders\gemma4_e4b_it_fp8_scaled.safetensors",
    ),
    # FLUX.2 KLEIN 9B dataset workflow (1 Click Dataset)
    (
        "https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-9b/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors",
        r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\text_encoders\qwen_3_8b_fp8mixed.safetensors",
    ),
    (
        "https://huggingface.co/black-forest-labs/FLUX.2-klein-9B/resolve/main/flux-2-klein-9b.safetensors",
        r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\flux-2-klein-9b.safetensors",
    ),
]

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def fetch(item):
    url, dest = item
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    start = os.path.getsize(tmp) if os.path.exists(tmp) else 0
    headers = dict(UA)
    if start > 0:
        headers["Range"] = f"bytes={start}-"
    req = urllib.request.Request(url, headers=headers)
    mode = "ab" if start > 0 else "wb"
    try:
        with urllib.request.urlopen(req, timeout=900) as r, open(tmp, mode) as f:
            got = start
            while True:
                chunk = r.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                got += len(chunk)
                if got % (1024 * 1024 * 512) < 1024 * 1024:
                    print(f"  {os.path.basename(dest)}: {got//1024//1024} MB", flush=True)
        os.replace(tmp, dest)
        return (os.path.basename(dest), True, os.path.getsize(dest) // 1024 // 1024, f"resumed from {start//1024//1024} MB" if start else "")
    except Exception as e:
        return (os.path.basename(dest), False, os.path.getsize(tmp) // 1024 // 1024 if os.path.exists(tmp) else 0, f"{e} (part kept for resume)")


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for name, ok, mb, note in ex.map(fetch, MODELS):
            if ok:
                print(f"OK   {name} {mb} MB {note}")
            else:
                print(f"FAIL {name} {mb} MB — {note}")


if __name__ == "__main__":
    main()
