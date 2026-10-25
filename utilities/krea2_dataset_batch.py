#!/usr/bin/env python
"""Krea 2 '1 Click Dataset' batch generator.

Mirrors the tested krea2_identity_edit.json chain:
  UNETLoader -> LoraLoaderModelOnly(identity) -> LoraLoaderModelOnly(RawGirl)
             -> Krea2EditModelPatch -> KSampler -> VAEDecode -> SaveImage
with a Krea2EditGroundedEncode (positive) + Krea2EditGroundedEncode (negative)
grounded on the reference image.

Loops 20 scene prompts (same character, varied scene/camera/lighting),
each with a distinct seed, submitting to the running ComfyUI REST API and
polling until done. Outputs land in the ComfyUI output dir under a
filename_prefix; we then copy them into a dataset folder.

Usage:
  python krea2_dataset_batch.py
"""
import json
import time
import shutil
import urllib.request
import urllib.error
import random
import os
import sys

BASE = "http://127.0.0.1:8188"
OUT_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"
DATASET_DIR = r"E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\krea2_character_2"

# Reference image (already in the running server's input dir)
REF_IMAGE = "krea2_test_ref.png"

# LoRA chain (matches tested workflow)
IDENTITY_LORA = "krea2_identity_edit_v1_2.safetensors"
RAWGIRL_LORA = "RawGirlV3.safetensors"
RAWGIRL_STRENGTH = 1.2

# Krea 2 turbo sampler settings (matches tested workflow)
STEPS = 10
CFG = 1.0
SAMPLER = "euler"
SCHEDULER = "simple"
DENOISE = 1.0
WIDTH = 2048
HEIGHT = 1152
GROUNDING_PX = 768

# Character identity (kept constant across all 20)
CHAR = ("the SAME boy from the reference: short dark hair, rose-pink collared "
        "shirt, black full-length trousers, black school bag")

# Shared realism tail (natural photo, no plastic)
REALISM = ("ONLY ONE character, no other people, no duplicates. Natural unposed "
           "look, real skin texture with pores and imperfections, natural "
           "lighting, slight motion blur, deep depth of field, sharp background, "
           "no fake bokeh, no editorial polish, looks like a real photo someone "
           "already took.")

NEG = ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI, "
       "3d render, stick figure, duplicate character, multiple people, "
       "watermark, logo")

# 20 scene prompts: same character, varied scene/camera/lighting
SCENES = [
    "A frontal headshot of {c}, neutral expression, head tilted slightly to the right. Close-up, 85mm lens f/2.8, sharp focus on the eyes. Soft overcast daylight, plain muted background. {r}",
    "{c} walking down a wet city street in the afternoon, head turned slightly toward the camera, candid expression. Medium shot, 35mm f/4.0, urban background. Natural overcast light. {r}",
    "A wide shot of {c} standing on the stone bridge over the river, looking directly at the camera. Full-body, 50mm f/8.0, head to toe. Moody overcast light, open river behind. {r}",
    "{c} standing in a dark alleyway, head in sharp profile toward a light source. Medium shot, 35mm f/1.8, high-contrast moody atmosphere, dim ambient light. {r}",
    "{c} standing in a dimly lit indoor corridor, head angled three-quarters away from the camera. Full-body, 24mm, natural light streaks from a high window, deep shadows. {r}",
    "A true profile view of {c}, chin tilted slightly upward. Close-up, 105mm telephoto, compressed background. Soft golden-hour light from behind. {r}",
    "{c} sitting on a simple wooden stool, head tilted slightly downward, eyes looking up at the camera. Medium shot, 85mm f/4.0, soft even light, neutral grey background. {r}",
    "{c} standing on a rooftop at dusk, body facing away, head turned back over the shoulder toward the camera. Half-body, 35mm f/2.0, moody sky. {r}",
    "{c} riding a train, head bowed slightly as if in thought. Medium shot, 50mm f/2.8, soft window light, blurred interior. {r}",
    "{c} standing in a foggy forest at dusk, head tilted back looking up into a beam of light. Medium shot, 50mm f/1.4, a single bright shaft through the mist. {r}",
    "A close-up of {c} in a messy artist's studio, head tilted slightly to the left, curious expression. Close-up, 85mm prime f/2.8, warm practical light. {r}",
    "{c} sitting on a concrete ramp at a sun-bleached skatepark, head turned away from the sun toward the horizon. Medium shot, 35mm f/4.0, bright daylight. {r}",
    "A wide shot of {c} standing with arms crossed against a plain wall, looking directly at the camera with a slight chin tuck. Full-body, 50mm f/8.0, even soft light. {r}",
    "A low-angle shot looking up at {c}, head tilted down toward the lens with a confident gaze. Medium shot, 24mm wide-angle, overcast sky behind. {r}",
    "{c} walking through a lush green park, head turned in a three-quarter view as if looking at something in the distance. Full-body, 35mm f/4.0, dappled daylight. {r}",
    "{c} face illuminated solely by the glow of a computer screen in a pitch-black room, head angled slightly upward. Blue light reflects off the face. Close-up, 85mm f/2.0. {r}",
    "{c} standing in a cozy, cluttered record store, viewed from a profile angle as they look at a shelf. Medium shot, 35mm f/2.0, warm ambient light. {r}",
    "{c} standing under a single flickering street lamp in the rain, head bowed slightly so the face is partially in shadow. Half-body, 50mm f/2.8, wet pavement reflections. {r}",
    "{c} standing on a wooden beach pier during sunset, head tilted back slightly with eyes closed, enjoying the breeze. Medium shot, 85mm f/2.8, warm low sun. {r}",
    "A relaxed, three-quarter view of {c} standing against a plain muted background, head turned slightly off-camera. Medium shot, 50mm f/4.0, soft even light. {r}",
]


def build_graph(prompt, seed):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "krea2_turbo_fp8_scaled.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_4b_fp8_scaled.safetensors", "type": "krea2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": IDENTITY_LORA, "strength_model": 1.0}},
        "5": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["4", 0], "lora_name": RAWGIRL_LORA, "strength_model": RAWGIRL_STRENGTH}},
        "6": {"class_type": "LoadImage", "inputs": {"image": REF_IMAGE}},
        "7": {"class_type": "VAEEncode", "inputs": {"pixels": ["6", 0], "vae": ["3", 0]}},
        "8": {"class_type": "EmptySD3LatentImage", "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1}},
        "9": {"class_type": "Krea2EditModelPatch", "inputs": {"model": ["5", 0], "source_latent": ["7", 0], "ref_boost": 4.0, "fit_mode": "fit", "source_image": ["6", 0], "vae": ["3", 0]}},
        "10": {"class_type": "Krea2EditGroundedEncode", "inputs": {"clip": ["2", 0], "prompt": prompt, "image": ["6", 0], "grounding_px": GROUNDING_PX}},
        "11": {"class_type": "Krea2EditGroundedEncode", "inputs": {"clip": ["2", 0], "prompt": NEG, "image": ["6", 0], "grounding_px": GROUNDING_PX}},
        "12": {"class_type": "KSampler", "inputs": {"model": ["9", 0], "seed": seed, "steps": STEPS, "cfg": CFG, "sampler_name": SAMPLER, "scheduler": SCHEDULER, "positive": ["10", 0], "negative": ["11", 0], "latent_image": ["8", 0], "denoise": DENOISE}},
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["3", 0]}},
        "14": {"class_type": "SaveImage", "inputs": {"images": ["13", 0], "filename_prefix": "krea2_ds"}},
    }


def post_json(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def get_json(path):
    with urllib.request.urlopen(BASE + path, timeout=60) as r:
        return json.load(r)


def run_one(prompt, seed, idx):
    graph = build_graph(prompt, seed)
    res = post_json("/prompt", {"prompt": graph, "client_id": "krea2-ds-batch"})
    pid = res.get("prompt_id")
    if not pid:
        raise RuntimeError(f"no prompt_id: {res}")
    # poll
    deadline = time.time() + 600
    while time.time() < deadline:
        hist = get_json(f"/history/{pid}")
        if pid in hist:
            status = hist[pid].get("status", {})
            if status.get("status_str") == "success":
                outputs = hist[pid].get("outputs", {})
                files = []
                for nid, out in outputs.items():
                    for f in out.get("images", []):
                        if f.get("type") == "output":
                            files.append(f["filename"])
                return pid, files
            if status.get("status_str") == "error":
                raise RuntimeError(f"error on {pid}: {status.get('message')}")
        time.sleep(2)
    raise TimeoutError(f"timeout waiting for {pid}")


def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    random.seed(20261008)
    seeds = [random.randint(1, 2**31 - 1) for _ in range(len(SCENES))]
    results = []
    for i, scene in enumerate(SCENES):
        prompt = scene.format(c=CHAR, r=REALISM)
        seed = seeds[i]
        print(f"[{i+1:02d}/{len(SCENES)}] seed={seed} submitting...", flush=True)
        try:
            pid, files = run_one(prompt, seed, i)
            print(f"    done -> {files}", flush=True)
            # copy outputs into dataset dir with ordered names
            for j, fn in enumerate(files):
                src = os.path.join(OUT_DIR, fn)
                if os.path.exists(src):
                    dst = os.path.join(DATASET_DIR, f"Image_{i+1:05d}_{j+1}.png")
                    shutil.copy2(src, dst)
                    print(f"    saved -> {dst}", flush=True)
            results.append((i + 1, seed, files))
        except Exception as e:
            print(f"    FAILED: {e}", flush=True)
            results.append((i + 1, seed, f"ERROR: {e}"))
    print("\n=== SUMMARY ===")
    for r in results:
        print(r)
    print(f"\nDataset dir: {DATASET_DIR}")


if __name__ == "__main__":
    main()
