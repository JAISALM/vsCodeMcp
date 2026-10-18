# User-Workflows Folder Triage (2026-10-18)

**Trigger:** user — the `user\default\workflows` folder had **245 files** ("not good"); mark the
useful ones, remove the rest.

**Location triaged:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\`

## Result

- **34 files KEPT** in the folder (root) — the list below.
- **211 files MOVED** (not deleted — reversible) to
  `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows_archive\2026-10-18\`
  (212 files incl. `MANIFEST.txt` listing every archived name).
- **`character sheet\` subfolder kept as-is** (3 P1/P5 sheet variants: LEEBLAAB, patreon, 1wxixua).
- `.index.json` kept (UI index — do not touch).
- Restore anything: move the file back from the archive folder (names unchanged).
- Script: `utilities\triage_user_workflows.py` (idempotent keep-list; re-runnable).

## The 34 kept (marked useful)

**Character pipeline (current):**
`1 Click Dataset (Klein 9b).json` (THE dataset workflow) · `2BZ_H3_character_sheet_2stage_v1_EN.json`
(P3 sheet) · `krea2_1click_dataset.json` · `krea2_dataset_char1.json` · `krea2_dataset_char2.json`
· `krea2_identity_edit.json` (face-lock core) · `krea2_t2i_char1.json` · `krea2_t2i_char2.json`
· `krea2_t2i_char1_pe3.json` · `krea2_t2i_char2_pe3.json` (pe/pe2 superseded → archived)
· `krea2_2pass_bf16_turbo.json` · `krea2T2iI2iInpaint2pass_v15_fixed.json`
· `QWEN_click_multiple_character_angles-v1.0.json`

**H3 project / production:**
`minimax_h3_boar_grave_talking_r2v.json` · `minimax_h3_sam_r2v_2char_cinematic.json` ·
`minimax_h3_sam_r2v_cinematic.json` · `H3_Face_Refine_Auto_Select.json` ·
`H3_Face_Refine_Manual_Select.json` · `H3_FaceRefine_boar_grave.json` ·
`H3-Contest_BaseWorkflow.json` · `MiniMaxH3_NativeAudio_MusicVideo_TEMPLATE.json` ·
`RIFE_WAN_Method_Interpolation_TEMPLATE.json` · `video_minimax_h3_r2v.json` ·
`video_minimax_h3_r2v+turbo.json` · `minimaxH3Camera_v20.json` (v10 → archived)
· `minimaxH315SecondSeamlessMulti_v11.json` · `minimaxH330SecondSeamlessImage_v13.json`

**Tools:**
`WF-H3_zuanfilm-Face_Detailer.json` · `vdn_h3_t2v_benchmark.json` ·
`seedvr2_batch_upscale.json` · `seedvr2_image_upscale.json` · `seedvr2_lastframe_2k.json`
· `seedvr2_video_upscale.json`

## What was archived (211)

- **~120 Episode-1 / old-schoolboy-era files** — all `jaisal_*` (intro A–J shots, keyframes,
  shots 1-3, sketch, production 1/2, lowangle, single_shot), all `krea2_intro_*` /
  `krea2_jaisal_*` / `krea2_kf*` / `krea2_small_mic_*` / `krea2_inpaint_*` / `krea2_object_refs`,
  `kerala_kid_2d_ref`, `mini-max-jaisal-test`, `t2v_beach_sprint_test`, `beach_sprint_test` —
  superseded by the D137 character re-scope (old schoolboy char deprecated).
- **~25 backups** — every `*.bak` / `*.pre_*.bak` / `*.api.bak` file.
- **8 native-audio chain copies** (`05_Chained` … `08_GGUF_Chained_AudioLock`) — originals live
  in `E:\minimax_workflow\MiniMax-H3-NativeAudio-MusicVideo-Workflow\workflows\chain\`.
- **Stale one-offs:** `plaguekindMinimaxH3SparseAttention_h3V31`, `oneNode-Flux.json`,
  `qwen_edit_small_mic/remove_mic`, `krea2_t2i_character`, `_ref_krea2_t2i_int8`, `jaisal_2mp_test`,
  `krea2_t2i_small_mic_end`, `krea2_intro_keyframes`, `vdn_h3_t2v_benchmark.json.bak`, etc.

**NOTE for future:** `episode1\workflows\` contains only a README — no committed copies of the
Episode-1 workflows exist yet. The archive folder is their only backup (they were moved, not
deleted).
