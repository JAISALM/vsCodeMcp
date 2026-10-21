# MODEL INVENTORY — `E:\ComfyUI_windows_portable\ComfyUI\models`

Created 2026-10-21. Source of truth for what lives in the shared model library
(817.9 GB across 45 subfolders), what is used by which workflow, and what has
been archived.

**Method:** every model file cross-referenced against all 63 workflow JSONs in
both trees (`comfyUi_latest` + `ComfyUI_windows_portable`). Referenced = in use.

## UNTOUCHED — LTX family (all of it, ~131 GB)

User decision 2026-10-21: **untouchable for now** — Lightricks released VFX
LoRAs for LTX-2.5 that are powerful tools for the production movie workflow
("VFX week"):
- **`LTX-2.5-22b-IC-LoRA-Clean-Plate`** — background removal / clean plate
- **`LTX-2.5-22b-IC-LoRA-Day-To-Night`** — day→night + color changes
- **`LTX-2.5-22b-IC-LoRA-SDR-To-HDR`** — HDR
- background-text-addition + other VFX LoRAs (see
  https://docs.ltx.io/open-source-model/vfx-post-production/native-resolution and
  https://huggingface.co/Lightricks)

The LTX-2.5 base stack is ALREADY local: `ltx-2.5-22b-distilled-transformer`
(21.5 GB), `ltx-2.5-22b-ic-lora-sdr-to-hdr-1.0` + `ltx-2.5-22b-ic-lora-alpha-gen-0.9`
(1.31 GB each), `gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot` encoder (15.37 GB),
`ltx-2.5-video-vae` (1.47 GB) + audio VAE. Only the new VFX IC-LoRAs need fetching
when we test. Also referenced by 5 saved LTX workflows in the old tree
(`LTX-2 I2V WORKFLOW.json`, `LTX-2_I2V_Distilled_wLora.json`, `workflow LD.json`,
`video_ltx2_3_ia2v_Workflow.json`, `video_ltx2_3_t2v_workflow.json`).

## UNTOUCHED — H3 family + H3-adjacent (~145 GB)

Core H3 (referenced by our workflows — ref2va/fl2va/Singularity, turbo LoRAs,
video/audio VAEs, `qwen3vl_32b_minimax_h3_nvfp4_awq`) + everything H3-adjacent
left in place while the movie stage is active: `fastvideo_fasth3_8step_v2`
(22.13 GB), `minimax_h3_ref2va_viggle` (21.03 GB) + `viggle_animate_dmd_lora_r64`,
`minimax_h3_character_swap` ×2, `ig_tiktok_aesthetic_h3`, `dr0nesh0t_aerial`,
`h3-facial-realism-closeup`, `semantic_bridge`, `vdn-minimax-h3` (3.48 GB),
`Qwen3-VL-32B-Instruct-MiniMax-H3` GGUF pair (17.31 GB).

## KEPT — ditto (18.3 GB)

User decision: keep — the ditto workflow is useful for making different styles
(`ditto_global_comfy`, `ditto_global_style_comfy`, `ditto_sim2real_comfy`).

## KEPT — referenced by our workflows (~330 GB, do not move)

| Model | Referenced by |
|---|---|
| `Krea2Realism_V1` (13.14), `krea2_turbo_bf16` (26.28), `krea2_turbo_fp8_scaled` (13.14), `Krea2-realism-V2` (1.56), `krea2_identity_edit_v1_2` (1.83), `Krea2_Cinematic_Artstyle` (0.11), `krea2_turbo_lora_rank_64` (0.47), `krea2RealVae_v10` (0.51), `qwen3vl_4b_fp8_scaled` (5.24), `qwen_image_vae` (0.25) | 07/07c/08j/10a/1Click Krea2 chain, krea2T2iI2iInpaint2pass, krea2_2pass_bf16_turbo |
| `flux-2-klein-9b` (18.16) + `flux-2-klein-9b-kv-fp8` (9.82), `qwen_3_8b_fp8mixed` (8.66), `flux2-vae` (0.34) | `1 Click Dataset (Klein 9b)`, `image_flux2_klein_9b_kv_image_edit` |
| `qwen_image_2.1_bf16` (14.23), `qwen3vl_8b_fp8_scaled` (10.59), `qwen3vl_8b_int8_convrot` (9.35), `qwen_image_2.1_vae_bf16` (0.68) | 09j/09k character sheets, LEEBLAAB sheets, logo_fists_compare |
| H3 core: `minimax_h3_fl2va` / `ref2va` / `Singularity` (20.97 each), `qwen3vl_32b_minimax_h3_nvfp4_awq` (15.69), `minimax_h3_video_vae` ×2 (8.02), `minimax_h3_audio_vae` (0.61), `minimax_h3_ref2v_turbo` + `fl2v_turbo` (3.92) | 05d/05e charsheets, 2BZ, H3_FaceRefine, H3 R2V cinematic, boar_grave |
| `qwen_image_edit_2511_bf16` (40.86) + `Qwen-Image-Edit-2511-Lightning-4steps-bf16` (0.85) + `qwen-image-edit-2511-multiple-angles-lora` (0.30) + `qwen_2.5_vl_7b` (16.58) + `qwen_2.5_vl_7b_fp8_scaled` (9.38) | `QWEN_click_multiple_character_angles-v1.0` |
| `famegrid_spicy_3167060` (1.56), `Typnosis_Krea2` (0.46), `RawGirlV3` (0.40) | 10a_frontal_base, krea2_1click_dataset, krea2_t2i_char1, krea2_identity_edit |
| SEEDVR2 (16.98) | seedvr2_* upscale workflows |
| Florence-2 (3.29) | 05d/05e/07c charsheet workflows |
| `birefnet` (0.44) | logo_transparent |
| `sam3.1_multiplex_fp16` (1.75), `sam_vit_b` (0.38), `face_yolov8m` / `person_yolov8m-seg` (0.10) | H3 R2V + H3_FaceRefine + WF-H3_zuanfilm-Face_Detailer |
| `ae.safetensors` (0.34) | 05d/07c VAE slot |

## MOVED to `F:\models_bkp\<subfolder>\` (2026-10-21, structure preserved)

| Group | Files | Size |
|---|---|---|
| **Wan** (all) | `wan2.1_14B_SCAIL_2_fp16`, 4× `wan2.2` GGUF unets (i2v/t2v hi/lo), `wan2.2_vae`, `wan_2.1_vae`, `Wan2_1_VAE_bf16` ×2 (vae + vae\wan), 12 LoRAs (lightx2v T2V/I2V, WanAnimate_relight, wan2.2 i2v/t2v lightx2v ×4, SCAIL_2_DPO, ChronoEdit, CausVid ×3) | ~114.8 GB |
| **umt5 / FLUX.1 text encoders** | `umt5_xxl_fp16`, `umt5-xxl-enc-bf16`, `umt5-xxl-enc-bf16_mocha`, `umt5_xxl_fp8_e4m3fn_scaled`, `t5-base` — verified: zero workflow references; klein workflows use `qwen_3_8b_fp8mixed` (FLUX.2 arch uses Qwen3 CLIP, not umt5) | ~41.7 GB |
| **Qwen-Image 2511/2512 gen** (edit-2511 chain stays) | `qwen_image_2512_fp8_e4m3fn` (20.43), `Qwen-Image-Edit-2509-Q8_0.gguf` (21.76), 8 Lightning/Turbo/360 LoRAs (Qwen-Image-Lightning-4steps ×2, 8steps, 2512-Lightning-fp32, Wuli-2512-Turbo, qwen-360-2512, nicegirls_qwen2512, qwen-cinema), `qwen3.5_9b_qwen_image_2.1_pe_i2i` (9.47), `qwen_image_canny_diffsynth_controlnet` (2.27) | ~64.0 GB |
| **SDXL + orphaned controlnets** | `RealVisXL_V4.0` (6.94), `xinsircontrolnet-union-sdxl__model_promax` (2.51), `InstantXFLUX.1-dev-Controlnet-Union` (6.60 — no FLUX.1 model exists to use it) | ~16.05 GB |
| **Redundant encoders** (verified before moving) | `qwen3vl_4b_bf16` (8.88 — redundant with in-use `qwen3vl_4b_fp8_scaled`), `qwen_3_4b` (8.04 — zero workflow references; the 4B family is covered by the in-use fp8_scaled file) | ~16.9 GB |
| **Small unused misc** | `sdpose_wholebody_fp16` (1.92), `clip_vision_h` + `sigclip` (2.12), `wav2vec2_large_english_fp16` (0.63), `moge_2` (0.66), `inswapper_128.onnx` (0.55), liveportrait ×5 (0.51), `sam2` ×2 (0.48), `adonis_base/refine` (2.08), `Iyo-Sumiv_10`, `GrandlineLSIv1.0Krea`, `refcontrol_v2_poses`, `vh5tape-comfyui`, `flux-2-klein-9B-360-erp-outpaint-lora_V1`, `HighResolution9B`, `lenovo` (0.79), Z-Image Turbo LoRAs ×2 (0.43), `Z-Image-Turbo-Fun-Controlnet-Union` (3.10), `uso-flux1-projector-v1` (0.02), face/hand yolov8n/s (0.04), vae_approx taesd/taef1/taesd3/taesdxl ×8 (tiny) | ~14.3 GB |

Total ≈ **268 GB freed** (move = recoverable: copy the file back into the same
subfolder).

## DELIBERATELY NOT TOUCHED (this pass)

- **Junk**: `Unconfirmed 819787.crdownload` (1.63 GB, incomplete download) —
  left in place (user: don't delete junk while the Krea2 base download runs).
- **`ace_step_v1_3.5b`** (7.70 GB, audio) — not approved this pass.
- **Krea2/klein style LoRAs** not in any workflow (user's call): `krea2_darkbrush`
  (0.47), `krea2_lineart_v1_fp16` (0.06), `bfs_head_v1_flux-klein_9b` (0.66),
  `Flux2-Klein-9B-consistency-V2` (0.33).
- **H3 variants + H3-adjacent** (see UNTOUCHED-H3 above).
- **`Qwen3-VL-32B-Instruct-MiniMax-H3` GGUF pair** (17.31 GB) — H3-adjacent, kept.

## Pull-back procedure

`F:\models_bkp\<subfolder>\<file>` → copy back into
`E:\ComfyUI_windows_portable\ComfyUI\models\<subfolder>\`, then ComfyUI will see
it on next model-list refresh. Example (Qwen-Image 2512 when needed):

```powershell
Copy-Item "F:\models_bkp\diffusion_models\qwen_image_2512_fp8_e4m3fn.safetensors" `
          "E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\"
```

## Move log

- 2026-10-21: move executed (background job, E:→F: cross-volume). Pre/post
  verification: every file checked by name + byte size before and after.
  Result: pending.
