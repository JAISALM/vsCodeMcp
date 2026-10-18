# External Workflow Sources (user-collected, forum/internet)

Workflows the user downloaded from forums/internet, kept outside the ComfyUI
`user\default\workflows` folder. Logged 2026-10-18 so the locations survive
session loss.

## `E:\Flux_klein\` — FLUX.2 [klein] workflows (user-placed 2026-10-18)

| File | KB | Notes |
|---|---|---|
| **`1 Click Dataset (Klein 9b).json`** | 38 | **THE DATASET WORKFLOW (user-selected 2026-10-18).** 23 nodes. Ref-Latent-Controller by u/Capitan01R (Reddit r/StableDiffusion 1se5a5z), adjusted by u/9_…. **Models:** `flux-2-klein-9b.safetensors` (17.3 GB, `black-forest-labs/FLUX.2-klein-9B` — OPEN repo) + `qwen_3_8b_fp8mixed.safetensors` (8.3 GB, `Comfy-Org/vae-text-encorder-for-flux-klein-9b/split_files/text_encoders`) + `flux2-vae.safetensors` (320 MB, same repo `/split_files/vae/` — ALREADY DOWNLOADED). **Usage:** LoadImage node 76 = character's reference face (default `ref_woman.png` → replace with our HD face in `input/`); node 377 `CR Prompt List` = embedded dataset prompt set (frontal headshot 85mm f/2.8 etc.); `EmptyFlux2LatentImage` node 179 = 768×1120 (3:4); SaveImage node 280 prefix `Dataset\Test_woman\Image` → **rename per character** (`Dataset\Zidane\Image`, `Dataset\Jaisal\Image`). `Flux2KleinRefLatentController` node 359 = identity dial (widgets `[104.6, 0, 'none', 0.5, False]`); `Flux2KleinTextRefBalance` node 355 = `[0.995, False]`. |
| `FKlein9B_referenceLatent_4ImagesGrid_T2I_V3.json` | 152 | 4-image reference grid T2I (V3) |
| `Flux-2-klein-advanced-workfllow-Updated-new-realistic.json` | 81 | advanced realistic workflow (updated) |
| `Iden_feat_final_fixed_sigma.json` | 28 | identity-features variant, fixed sigma |
| `iden_wf (1).json` | 20 | identity workflow (dup copy, "(1)") |
| `KLEIN9B_Adonis_ColorMatchV2.json` | 39 | color-match V2 (adonis) |
| `objectSwappingFlux2_v10.json` | 42 | object swapping v10 |

**9B decision (user, 2026-10-18):** use the **9B dense** model — quality over speed.
Fits: 9B bf16 (~17.3 GB) in 32 GB VRAM, text encoder offloads to 64 GB RAM.

## `E:\minimax_workflow\` — MiniMax H3 workflows + kits (shared earlier, user-placed)

**Root — 21 H3 workflow JSONs:**
`2BZ_H3_character_sheet_2stage_v1_EN.json` (P3 char sheet) · `Dialogues.json` ·
`Ep29 MiniMaxH3_Continuation_Workflow.json` · `fl_minimax_h3_turbo_lora_example_workflow.json`
· `H3-Contest_BaseWorkflow.json` · `h3_refmod_cinematic.json` ·
`mini-max-refrance-to-video-1.json` · `Minimax H3 Workflow_ Magic Time Period Shift.json`
· `minimax-h3-guided-consistent-characters-via-reference-identity-face-body-cloths.inline-graph.json`
· `Minimax-H3_zuanfilm_res2s.json` · `minimaxH315SecondSeamlessMulti_v11.json` ·
`minimaxH3Camera_v10.json` · `minimaxH3Camera_v20.json` · `minimax_h3_character_swap_workflow.json`
· `MiniMax_H3_FL2VA_Fiirst-and-Last-Frame-Workflow.json` · `minimax_h3_sam_r2v_2char_cinematic.json`
· `minimax_h3_sam_r2v_cinematic.json` · `qwen_minimzed_h3.json` · `video_minimax_h3_r2v+turbo.json`
· `video_minimax_h3_r2v.json` · `WF-H3_zuanfilm-Face_Detailer.json` ·
`Workflow for Minimax H3 image editing w ComfyUI.json`

**Subfolders:**
- `blender+minimax\` — Blender→H3 R2V pipeline (guide PDF, blockout .blend, 5s square
  camref mp4, refs, 2 workflow JSONs) + `boar_grave\` kit (scene renders, camref,
  2 identity refs, `minimax_h3_boar_grave_talking_r2v.json` + `H3_FaceRefine_boar_grave.json`, README).
- `character_sheet\` — 4 sheet workflows: **`2BZ_H3_character_sheet_2stage_v1_EN.json`** (P3,
  = the P3 route), `LEEBLAAB-QwenImage21-Character-SHEET.json` (P5),
  `LocationOrbitSheetH3.json` (P2), `minimaxh sheet patreon.json`.
- `consistent_environment\` — env consistency experiment (refs + `MyRoom_Experiment_Refmod.safetensors`).
- `MiniMax-H3-NativeAudio-MusicVideo-Workflow\` — full pack: README +
  `run_nvidia_gpu_optimized.bat` + `custom_nodes\ComfyUI-Spectrum-MiniMax-H3` (Spectrum H3
  node pack source) + `workflows\` (native-audio music-video template, RIFE/WAN interpolation,
  8 chain variants incl. GGUF + AudioLock + RefImage).
- `production_experiments\` — `audio_splitter.json` (170 KB),
  `continuous_static_video_without_quality_loss.json` (243 KB),
  `foxydits_sucks_at_making_workflows_v7.2.json` (389 KB).

## Related project locations (not external, for reference)

- **Project workflows (ours, committed):** `D:\models\vsCodeMcp\challenge\consistent-short\workflows\`
  (01_character_sheet / 02_identity_refset / 03_hd_upscale) + `episode1\workflows\`.
- **ComfyUI UI workflows folder (200+ files, TRIAGE PENDING 2026-10-18):**
  `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\` —
  mark useful / archive the rest (see CURRENT_TASK).
- **Model dirs:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\` (active server).
