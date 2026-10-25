#!/usr/bin/env python
"""Build 05e_charsheet_H3_fizgig_jaisal.json — the user's patreon 'MiniMax H3 Fizgig' sheet
workflow (E:\minimax_workflow\character_sheet\minimaxh sheet patreon.json) set up for Jaisal.

Author's design (kept):
- single character ref (node 25 LoadImage -> ImageScaleToTotalPixels 47 -> H3 ref_image_0)
- H3 node 28 [prompt, 4096, 1536, 5, 'max'], width/height driven by primitives 364/365
- vanilla sampler chain: BasicScheduler 7 (beta, 25 steps) + er_sde (6) + RandomNoise 12
- attention subgraph 356 (H3SLAAttention + MiniMaxChunkFeedForward + kitchen attention +
  MiniMaxLowVRAMAttention + MiniMaxH3SigmaShift) — the author's stack, untouched
- FizgigH3StillLatent 65 (4096x1536x1) -> SamplerCustomAdvanced 8 -> FizgigH3StillDecode 64
- VAE 73 = the author's minimax_h3_video_vae_int8_convrot (available via extra_model_paths)

Adaptations for Jaisal / on-disk models:
- 25 LoadImage -> jaisal_portrait_HD.png (identity ref; kit is TEXT-specified in the prompt)
- 28 prompt -> single-ref R2V 6-section 3-view sheet (new crest spec: fist roundel, no text)
- 71 UNET -> minimax_h3_ref2va_pruned_int8_convrot.safetensors (the author's
  minimax_h3_fused_refdelta_r1024_turbo8_mystic07 is NOT on disk)
- 72 CLIPLoaderGGUF (author's qwen3vl-32B-MiniMax-H3-Q2_K.gguf NOT on disk) ->
  CLIPLoader + qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (proven in 05d)
- 68 SaveImage -> charsheet/H3FIZ_JAISAL
- 358 LoadImageListFromDir DELETED (orphaned — no links — and its node class is not installed)
"""
import json, os

SRC = r"E:\minimax_workflow\character_sheet\minimaxh sheet patreon.json"
OUT_UI = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\05e_charsheet_H3_fizgig_jaisal.json"
OUT_PRJ = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\05e_charsheet_H3_fizgig_jaisal.json"

# AUTHORS' prompting technique (patreon sprite-sheet template, copied verbatim structure):
# left portrait closeup + center 3-angle full-body + right 6 round detail images.
# Single-ref workflow: the author's empty 'META for composition:' field is filled with
# our kit + crest spec (text-specified — this workflow has only the face ref).
PROMPT = (
    "iintegrated_multimodal_description:\n\n"
    "subject_definitions:\n"
    "<CHARACTER> character from <Picture 1> — a ~26-year-old Indian man, wavy medium-length black hair, "
    "a small patchy short beard, slim build, medium-brown Indian skin. META for composition: <CHARACTER> "
    "wears the complete team kit — a royal blue short-sleeve soccer jersey with a small subtle white emblem "
    "on the left chest (a clenched fist inside a thin circle, no words, no letters), matching royal blue "
    "track pants with a single white stripe down each side, clean white football boots, and the white name "
    "JAISAL centered on the upper back of the jersey.\n"
    "<Picture 1> is the identity source portrait of <CHARACTER>.\n\n"
    "summary:\n"
    "[reference generation] static image of sprite sheet, keep the exactly same art style of <Picture 1>.\n\n"
    "retention_analysis:\n"
    "<CHARACTER>: fully_preserved — face, hair, beard, skin tone and body build come only from <Picture 1>.\n\n"
    "detailed_description:\n"
    "The target image is a static image of sprite sheet showing <CHARACTER> from different angles, each "
    "element is separated and not overlap on each other, on a clean white studio background.\n\n"
    "[Shot 1] static image.\n\n"
    "<CHARACTER> on white background, sprite sheet showing <CHARACTER> composition adapted following all "
    "possible variants and angles:\n"
    "1. <CHARACTER> On the left portrait (head and chest) closeup composition on white background.\n"
    "2. <CHARACTER> In the center full body view from 3 different angles: straight from front, straight from "
    "side, straight from back — all wearing the complete team kit.\n"
    "3. <CHARACTER> On the right 6 round images (same size 2x3 vertical narrow row) with <CHARACTER>'s "
    "highlight details: single eye, lips, single ear (in circle), hair color, detailed skin texture color, "
    "outfit texture color (the royal blue jersey fabric and the small white clenched-fist roundel emblem).\n\n"
    "overall_soundscape: N/A\n\n"
    "non_diegetic_music: N/A"
)

j = json.load(open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
assert nodes[25]["type"] == "LoadImage", nodes[25]["type"]
assert nodes[28]["type"] == "MiniMaxH3ReferenceToVideo"
assert nodes[71]["type"] == "UNETLoader"
assert nodes[72]["type"] == "CLIPLoaderGGUF"
assert nodes[73]["type"] == "VAELoader"
assert nodes[68]["type"] == "SaveImage"
assert nodes[358]["type"] == "LoadImageListFromDir //Inspire"
print("source structure confirmed")

# --- Jaisal ref + prompt
nodes[25]["widgets_values"] = ["jaisal_portrait_HD.png", "image"]
nodes[28]["widgets_values"] = [PROMPT, 4096, 1536, 5, "max"]

# --- on-disk UNET (author's patreon UNET not on disk)
nodes[71]["widgets_values"] = ["minimax_h3_ref2va_pruned_int8_convrot.safetensors", "fp8_e4m3fn"]

# --- CLIP: author's GGUF not on disk -> proven CLIPLoader + nvfp4_awq (same as 05d)
nodes[72]["type"] = "CLIPLoader"
nodes[72]["widgets_values"] = ["qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "minimax", "default"]
# sync the widget-input list for the new node type (CLIPLoader = clip_name/type/device)
if "inputs" in nodes[72]:
    nodes[72]["inputs"] = [
        {"localized_name": "clip_name", "name": "clip_name", "type": "COMBO", "widget": {"name": "clip_name"}, "link": None},
        {"localized_name": "type", "name": "type", "type": "COMBO", "widget": {"name": "type"}, "link": None},
        {"localized_name": "device", "name": "device", "type": "COMBO", "widget": {"name": "device"}, "link": None},
    ]

# --- save prefix
nodes[68]["widgets_values"] = ["charsheet/H3FIZ_JAISAL"]

# --- drop the orphaned dir-loader (class not installed + no links)
j["nodes"] = [n for n in j["nodes"] if n["id"] != 358]
j["links"] = [l for l in j["links"] if l[1] != 358 and l[3] != 358]

for path in (OUT_UI, OUT_PRJ):
    json.dump(j, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("WROTE", path)
