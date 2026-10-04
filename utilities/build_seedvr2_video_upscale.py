# -*- coding: utf-8 -*-
"""
Build seedvr2_video_upscale.json - SeedVR2 2K video upscaler for the intro shots.

Clones the OFFICIAL example (custom_nodes/seedvr2_videoupscaler/example_workflows/
SeedVR2_HD_video_upscale.json) so all native widget shapes are preserved, then:
  - LoadVideo -> jaisal_intro_A_walkin_00005_.mp4 (swap per video)
  - DiT model -> seedvr2_ema_7b_sharp_fp16.safetensors (max quality, 32GB VRAM)
  - resolution 1080 (shortest edge) -> 1376x768 becomes 1920x1080
  - SaveVideo prefix -> intor_selected_Upscale/upscaled

The 3 selected videos (all 1376x768 @ 24fps):
  jaisal_intro_A_walkin_00005_.mp4      (124f, 5.2s)
  jaisal_intro_B_setup_00003_.mp4       (73f, 3.0s)
  jaisal_intro_C_starting_2ref_00006_.mp4 (243f, 10.1s)

Run the workflow 3x, swapping the LoadVideo filename each time.
Outputs land in output/intor_selected_Upscale/upscaled_*.mp4.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\build_seedvr2_video_upscale.py"
"""
import json
import shutil
import os

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\seedvr2_videoupscaler\example_workflows\SeedVR2_HD_video_upscale.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\seedvr2_video_upscale.json"

VIDEO = "jaisal_intro_A_walkin_00005_.mp4"   # swap per run (B, C)
SAVE_PREFIX = "intor_selected_Upscale/upscaled"
DIT_MODEL = "seedvr2_ema_7b_sharp_fp16.safetensors"


def main():
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)

    nodes = {n["id"]: n for n in d["nodes"]}

    # LoadVideo (node 21): widgets [filename, "image"]
    lv = nodes[21]
    lv["widgets_values"] = [VIDEO, "image"]
    print("LoadVideo ->", VIDEO)

    # DiT (node 14): widgets [model, device, blocks_to_swap, swap_io, offload, cache, attention]
    dit = nodes[14]
    dit["widgets_values"] = [DIT_MODEL, "cuda:0", 0, False, "cpu", False, "sdpa"]
    print("DiT ->", DIT_MODEL)

    # SaveVideo (node 23): widgets [filename_prefix, format, codec]
    sv = nodes[23]
    sv["widgets_values"] = [SAVE_PREFIX, "auto", "auto"]
    print("SaveVideo ->", SAVE_PREFIX)

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("saved", DST)


if __name__ == "__main__":
    main()
