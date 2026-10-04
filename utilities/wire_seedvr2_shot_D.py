#!/usr/bin/env python
r"""Wire the SeedVR2 pipeline for shot D take 00006 (2026-09-20).

1. Stage output\jaisal_intro_D_reverse_00006_.mp4 -> input\
2. seedvr2_video_upscale.json:
   - LoadVideo (node 21) -> jaisal_intro_D_reverse_00006_.mp4
   - SaveVideo (node 23) prefix -> intor_selected_Upscale/upscaled_D
     (deterministic output: output\intor_selected_Upscale\upscaled_D_00001_.mp4)
3. seedvr2_lastframe_2k.json:
   - LoadVideo (node 21) -> jaisal_intro_D_reverse_00006_.mp4 (the ORIGINAL take)
     (the workflow's internal SeedVR2 upscaler re-upscales the last frame to 2K,
      so no manual copy of the upscaled video is needed)
   - SaveImage (node 31) prefix stays lastframe_2k -> output\lastframe_2k_00001_.png
4. Verify the SeedVR2 model files exist.
"""
import json, io, shutil, os

COMFY = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"
WF_DIR = os.path.join(COMFY, "user", "default", "workflows")
INPUT = os.path.join(COMFY, "input")
OUTPUT = os.path.join(COMFY, "output")
MODELS = r"E:\ComfyUI_windows_portable\ComfyUI\models"

D_TAKE = "jaisal_intro_D_reverse_00006_.mp4"

def set_widget(path, node_id, idx, value):
    with io.open(path, "r", encoding="utf-8") as f:
        wf = json.load(f)
    node = next(n for n in wf["nodes"] if n["id"] == node_id)
    old = node["widgets_values"][idx]
    node["widgets_values"][idx] = value
    if "widgets_values_named" in node and node["widgets_values_named"]:
        # keep named in sync by position is not reliable; only update if key count matches
        pass
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)
    return old

def main():
    # 1. stage the take into input\
    src = os.path.join(OUTPUT, D_TAKE)
    dst = os.path.join(INPUT, D_TAKE)
    if not os.path.exists(src):
        raise SystemExit(f"source not found: {src}")
    shutil.copy2(src, dst)
    print(f"staged: {dst} ({os.path.getsize(dst)} bytes)")

    # 2. video upscale workflow
    p = os.path.join(WF_DIR, "seedvr2_video_upscale.json")
    old = set_widget(p, 21, 0, D_TAKE)
    print(f"video_upscale LoadVideo: {old!r} -> {D_TAKE!r}")
    old = set_widget(p, 23, 0, "intor_selected_Upscale/upscaled_D")
    print(f"video_upscale SaveVideo prefix: {old!r} -> 'intor_selected_Upscale/upscaled_D'")

    # 3. lastframe workflow (point at the ORIGINAL take - the internal upscaler
    #    re-upscales the last frame to 2K, so no manual copy is needed)
    p = os.path.join(WF_DIR, "seedvr2_lastframe_2k.json")
    old = set_widget(p, 21, 0, D_TAKE)
    print(f"lastframe LoadVideo: {old!r} -> {D_TAKE!r}")

    # 4. verify SeedVR2 models
    for m in ("seedvr2_ema_7b_sharp_fp16.safetensors", "ema_vae_fp16.safetensors"):
        for base in (os.path.join(MODELS, "SEEDVR2"), MODELS):
            fp = os.path.join(base, m)
            if os.path.exists(fp):
                print(f"model OK: {fp} ({os.path.getsize(fp)/1e9:.2f} GB)")
                break
        else:
            print(f"MODEL MISSING: {m}")

if __name__ == "__main__":
    main()
