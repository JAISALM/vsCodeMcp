# Workflow Triage — 2026-11-19

**User directive:** "there are lots of other workflows which is reusable and production pipeline… dont limit only for krea2. check for other models, experiments… i dont want the workflows folder to pile up, lets check and keep the reusable ones, and the special ones, redundant once we can remove."

**Result:** the flat 207-file workflows dir is now organized into a **stage-based pipeline** (`movies/<stage>/` = 92 reusable, all models) + a **`special/`** folder (110 char-specific / test / training / intro-era one-offs). Top level = `.index.json` only. **11 redundant `.bak` files deleted + 1 verified-exact duplicate removed** (identity-edit, SHA256-identical).

## New structure (canonical: `E:\comfyUi_latest\...\user\default\workflows\`)

| Folder | Files | Contents (models) |
|---|---|---|
| `movies/sheets/` | 30 | Krea2 t2i/3-view/kit/frontal + batch (PixaromaPromptEach) + PE3 expansion · H3 wide/fizgig/patreon/2-stage (Gemma4 TextGenerate) · Qwen-Image-2.1 (PE-I2I GGUF composite, multi-angles, face i2i) · VNCCS PoseStudio (pose-anchored) |
| `movies/identity/` | 5 | Krea2 identity-edit v1.2 (ref_boost 4.0) + batch rig · H3 FaceRefine auto/manual (face_yolov8m auto-detect) · WF-H3_zuanfilm face detailer (H3FaceStitch) |
| `movies/motion/` | 21 | H3 R2V + turbo · FastH3 omni ref2va · H3 HyperFlow 8-step · seamless 15s multi / 30s image · BG swap (fused refdelta + latent upscaler) · camera v20 (H3LocalCameraEditor) · sam 2-char cinematic · recast (person YOLO) · char-swap v1.1 FRO + v1.5 mask · pika H3 flex (t2v/ref2va/fl2va + kitchen ×2) · viggle remake edit/swap (UI) |
| `movies/image/` | 17 | H3 image t2i-cine / 20MP / pose-ref (simple+cine) · Krea2 duo 2-char (composer/2pass/inpaint/cine) · Krea2 quad 4-char (base + inpaint ×4) · raw-bf16 recipe · 2-pass i2i/inpaint (v15 fixed + bf16 turbo) |
| `movies/grade/` | 9 | **Zuanfilm Retrolab** (B&W emulsion + grain + halation + vignette = the 1950 grade; ektachrome = 2026 filmic texture) · seedVR2 batch/image/lastframe-2k/video upscale (P6 2K master) · H3 person removal (local + Relay-V2) · RTX Post VFX (TrueHDR) · RIFE frame interpolation |
| `movies/world/` | 2 | `world_pano_angles` (LC 360 View — geometry layer from 2:1 ERP pano) · `h3image_world_shot` (appearance layer) |
| `movies/audio/` | 3 | TTS_Suite: TTS-SRT / ASR-SRT-builder / OmniVoice (all D041-compliant — no music) |
| `movies/utility/` | 5 | sheet composite (ImageCompositeMasked) · SDPose ood image/video + multi-person-video pose · logo transparent (birefnet bg-removal) |
| `special/` | 110 | char-specific one-offs (k2f S1–S6 oneclick sets ×2, k2f scene sets, movie-shot 16x9 recipes, duo/cine char-LoRA scenes, film tests, boar-grave, opencast, logo fists) · test matrices (ABCD ×8, krea2_ab ×4, fair ×2, charlora ×2, mu/control/raw_qtest, face_lock ×7, v91 datasets ×4, lora stack, vdn benchmark, sol_h3 ×2 [needs sol weights], Viggle API-format ×2, 1-Click-Klein9b, H3-Contest base, Fizgig template, NativeAudio-MusicVideo [D041 — other content only]) · LoRA training pipeline (dataset ×2 + v91 + prograde, train_lora ×2, test_lora ×4, 1click dataset) · intro-video era (clussy_origin_story, you_do_not_know_what_kind_of_man_i_am [ChatterBox voice]) |

**Deleted (redundant):** 11 `.bak` files (`.ABCD.bak` ×2, `.preposeref.bak`, `.prefullmodel.bak`, `.pre_realism.bak` ×2, `.pre_t2i.bak` ×2, `.preint8.bak` ×2, `.bak_audiofix_20261025`) — every one a pre-change backup of a file whose current version is alive. + `krea2_identity_edit.json` top-level (SHA256-identical duplicate of `movies/identity/` copy).

## Classification rules used
- **REUSABLE → `movies/<stage>/`:** char-agnostic rig OR canonical route for a model (prompt/prefix/size swap = new use). All models: Krea2 (t2i/i2i/duo/quad), H3 (image/video/refine/swap/recast/camera), Qwen-Image-2.1, seedVR2, TTS, SDPose, panorama.
- **SPECIAL → `special/`:** char-specific content (jaisal/zidane/k2f/boar-grave/logo), test matrices, LoRA training pipelines, intro-video-era one-offs, D041-excluded (music) templates, benchmark/sol-weights-dependent files.
- **REdundant → deleted:** `.bak` files + hash-verified exact duplicates only. Version-drift "duplicates" (same name, different size/date in `E:\minimax_workflow` staging) were NOT deleted — the staging folder is the user's download area and was left untouched.

## Repo mirror
- `workflows/movies/<stage>/` = mirror of the 92 reusable files (resync: `workflows/resync_workflows.ps1`, now directory-based `robocopy /MIR`).
- `special/` = NOT mirrored (repo rule: one-shot tests never committed).
- Old flat 52-file mirror list retired (files now live in stage folders).

## Open items
1. **`ZuanfilmRetroLab` pack — INSTALLED 2026-11-19 (D259):** `zuanfilm/Zuanfilm-Retrolab` (Apache-2.0) cloned to `custom_nodes\Zuanfilm-Retrolab` (author-approved; zero extra pip deps; `NODE_CLASS_MAPPINGS` exact match; tests included). **One ComfyUI restart to load it** (user's call — open canvases lost on restart). After restart `movies/grade/Zuanfilm_Retrolab.json` is fully runnable.
2. `E:\minimax_workflow` staging dir untouched (download area; `consistent_environment` / `sol_h3_weights` / `NVlabs-Sana` = out of scope until 11-24 per user — download-dependent).
3. `special/` is recoverable from git? No — it's local-only. If a special file proves reusable later, promote: move to `movies/<stage>/` + it enters the mirror on next resync.
