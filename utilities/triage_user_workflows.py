#!/usr/bin/env python
"""Triage the ComfyUI user-workflows folder (2026-10-18).

Moves non-essential workflows to workflows_archive\\2026-10-18\\ (reversible),
keeps the current-project + tooling set, writes a manifest of archived files.
"""
import os
import shutil

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
ARCH = os.path.join(WF, "..", "workflows_archive", "2026-10-18")

KEEP = {
    # UI index (required)
    ".index.json",
    # character pipeline (current)
    "1 Click Dataset (Klein 9b).json",
    "2BZ_H3_character_sheet_2stage_v1_EN.json",
    "krea2_1click_dataset.json",
    "krea2_dataset_char1.json",
    "krea2_dataset_char2.json",
    "krea2_identity_edit.json",
    "krea2_t2i_char1.json",
    "krea2_t2i_char2.json",
    "krea2_t2i_char1_pe3.json",
    "krea2_t2i_char2_pe3.json",
    "krea2_2pass_bf16_turbo.json",
    "krea2T2iI2iInpaint2pass_v15_fixed.json",
    "QWEN_click_multiple_character_angles-v1.0.json",
    # H3 project / production
    "minimax_h3_boar_grave_talking_r2v.json",
    "minimax_h3_sam_r2v_2char_cinematic.json",
    "minimax_h3_sam_r2v_cinematic.json",
    "H3_Face_Refine_Auto_Select.json",
    "H3_Face_Refine_Manual_Select.json",
    "H3_FaceRefine_boar_grave.json",
    "H3-Contest_BaseWorkflow.json",
    "MiniMaxH3_NativeAudio_MusicVideo_TEMPLATE.json",
    "RIFE_WAN_Method_Interpolation_TEMPLATE.json",
    "video_minimax_h3_r2v.json",
    "video_minimax_h3_r2v+turbo.json",
    "minimaxH3Camera_v20.json",
    "minimaxH315SecondSeamlessMulti_v11.json",
    "minimaxH330SecondSeamlessImage_v13.json",
    # tools
    "WF-H3_zuanfilm-Face_Detailer.json",
    "vdn_h3_t2v_benchmark.json",
    "seedvr2_batch_upscale.json",
    "seedvr2_image_upscale.json",
    "seedvr2_lastframe_2k.json",
    "seedvr2_video_upscale.json",
}

os.makedirs(ARCH, exist_ok=True)
moved, kept = [], []
for name in os.listdir(WF):
    full = os.path.join(WF, name)
    if os.path.isdir(full):
        continue
    if name in KEEP:
        kept.append(name)
        continue
    dest = os.path.join(ARCH, name)
    shutil.move(full, dest)
    moved.append(name)

with open(os.path.join(ARCH, "MANIFEST.txt"), "w", encoding="utf-8") as f:
    f.write(f"Archived {len(moved)} files on 2026-10-18 (reversible: move them back to {WF})\n")
    for m in sorted(moved):
        f.write(m + "\n")

print(f"KEPT: {len(kept)}")
for k in sorted(kept):
    print("  keep:", k)
print(f"ARCHIVED: {len(moved)} -> {ARCH}")
