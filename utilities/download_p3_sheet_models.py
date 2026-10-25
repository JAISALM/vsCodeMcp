#!/usr/bin/env python
"""Download ONLY the P3 sheet models (Klein 9B set already exists in main tree).

Targets the ACTIVE ComfyUI (comfyUi_latest) models dir — the sheet runs there.
Range-resumable.
"""
import concurrent.futures
import os
import urllib.request

MODELS = [
    (
        "https://huggingface.co/Mamad8/MiniMax-H3-Image-VAE/resolve/main/minimax_h3_t1_image_vae_step1597.safetensors",
        r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\vae\minimax_h3_t1_image_vae_step1597.safetensors",
    ),
    (
        "https://huggingface.co/Comfy-Org/Gemma4/resolve/main/text_encoders/gemma4_e4b_it_fp8_scaled.safetensors",
        r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\text_encoders\gemma4_e4b_it_fp8_scaled.safetensors",
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
        return (os.path.basename(dest), False, os.path.getsize(tmp) // 1024 // 1024 if os.path.exists(tmp) else 0, f"{e} (part kept)")


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        for name, ok, mb, note in ex.map(fetch, MODELS):
            if ok:
                print(f"OK   {name} {mb} MB {note}")
            else:
                print(f"FAIL {name} {mb} MB — {note}")


if __name__ == "__main__":
    main()
