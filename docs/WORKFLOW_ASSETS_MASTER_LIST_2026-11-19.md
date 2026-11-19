# Workflow Assets — MASTER LIST (2026-11-19)

**Purpose:** single map of ALL workflow assets on the E: drive — so nothing is missed when the film work starts (author: "i dont want to miss out anything when we start working on the project").

**Three locations:**
1. **Canonical ComfyUI dir** `E:\comfyUi_latest\...\user\default\workflows\` — organized 2026-11-19: `movies/` (92 reusable, 8 stage folders) + `special/` (110 one-offs). Details: `WORKFLOW_TRIAGE_2026-11-19.md`.
2. **Staging** `E:\minimax_workflow\` — ~40 top-level loose files + 17 subfolders (downloads/experiments; some packs).
3. **Models** `E:\ComfyUI_windows_portable\ComfyUI\models` — all model files (UNet/LoRA/CLIP/VAE).

---

## ★ consistent_environment — THE FIND (author's idea: ball/referee POV + camera motions)

**Folder:** `E:\minimax_workflow\consistent_environment\` — 3 room photos + `MyRoom_Experiment_Refmod.safetensors` (467 KB) + `workflow.png` (the rig, as screenshot — **no JSON saved**).

**The rig (decoded from screenshot):** H3 R2V (8 refs) + **RefMod** (environment-consistency LoRA) + native audio + turbo/full-steps If/Else toggle:
```
4× room photos → Resize 2048 → MiniMax H3 Reference to Video (ref_image_0..8)
                 + Text(Multiline) = 6-section R2V prompt (the fly/bee POV chase)
Models: minimax_h3_82va_pruned_int8_convert · turbo3_step_lora rank35 · qwen3vl_32b fp4 · video_vae int8 · audio_vae fp32
Consistency: Load H3 RefMods (MyRoom_Experiment_Refmod, components 1.00) → Apply H3 RefMod (mode override, curve constant)
Sample: RandomNoise 49 · Basic Guider · KSamplerSelect euler · BasicScheduler simple · SamplerCustomAdvanced (steps 100 / turbo via If/Else 20|16)
Decode: VAE Decode + VAE Decode Audio → Create Video (fps 24, sRGB) → Save Video
Duration: Float(9.0 s) · Math Expression (frame calc) · Resolution Selector (2048, 3:4)
```
**How it works:** a **RefMod** = a tiny (~467 KB) per-environment appearance module. `Apply H3 RefMod` (mode override) forces every generated frame to carry the same room appearance → **any camera path (fly/bee POV, orbit, dolly) renders the SAME room**. The author's community test: "a guy asked for a bee/fly view of the room he has" — output came out well.

**Film mapping (author's idea — confirmed feasible):**
- **Ball POV:** RefMod of the pitch + prompt = ground-level camera rolling with the ball → consistent pitch under the ball.
- **Referee POV:** same RefMod + "referee's view scanning the field, high angle".
- **Camera motions (author: "with little tweaks we can use this for camera motions"):** exactly right — the rig is **environment-locked camera work**: change the prompt's camera choreography (dolly/pan/orbit/POV), the RefMod holds the environment. This is the **missing CAMERA stage** of our pipeline — bridges `world/` (appearance/geometry) and `motion/` (H3 R2V). Complements `minimaxH3Camera_v20` (camera control, env-unlocked).
- **Per-environment RefMods for the film:** extract from our own reference images with the pack's **RefMod training workflow** (`refmodtrain.json`: `MiniMaxH3RefModExtract` + VAELoader + `VRGDG_RefModDescribe` + `VRGDG_RefModImagePicker`) → one RefMod per environment (pitch / 1950s village / 2026 stadium / school).

**Model audit (main models path):**
| Rig needs | We have | Action |
|---|---|---|
| `minimax_h3_82va_pruned_int8_convert` | `minimax_h3_ref2va_pruned_int8_convrot` (21 GB) + `Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8` (21 GB) | swap-in (same family) |
| `minimax_h3_turbo3_step_lora_avg_rank_35_t50` | turbo 4-step/8-step LoRAs (ref2v/fl2v, v0.1–v1.1) | swap-in |
| `qwen3vl_32b.minimax_h3_mr_fp4` | `Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49` GGUF Q4_K_M (14.9 GB) + mmproj | swap-in (GGUF loader path) |
| `minimax_h3_video_vae_int8_convert` | `minimax_h3_video_vae_int8_convrot` (2.8 GB) — same model, different name | swap-in |
| `minimax_h3_audio_vae_fp32` | ✓ HAVE | — |
| `MyRoom_Experiment_Refmod` | in staging folder | **copy to models** (e.g. `models/refmods/`) |

**To make it runnable:** ① install the **`comfyui-vrgamedevgirl`** pack (already in staging — provides `MiniMaxH3RefMod{Extract,Inspect,Loader}` + `VRGDG_RefMod{Describe,ImagePicker}` + MatchGrain + memory utils) into `custom_nodes` + restart ② copy the refmod to models ③ reconstruct the workflow JSON (from screenshot, or start from the pack's own `minimax_h3_2pass_refmod_test_api.json` — the CE rig in API format, 35 nodes, all local models).

---

## E:\minimax_workflow — top-level loose files (~40)

| File | What | Status |
|---|---|---|
| `2BZ_H3_character_sheet_2stage_v1_EN.json` (145 KB, 09-06) | H3 2-stage sheet template (Gemma4 + ref2v turbo) | **in movies/sheets** (canonical copy) |
| `Dialogues.json` | H3 dialogue (VBVR + dmd_ref2va_8step + flf2v_lora) | special (dialogue test) |
| `Ep29 MiniMaxH3_Continuation_Workflow.json` | H3 continuation (Singularity pruned + tail slicer) | special (old-era) |
| `fl_minimax_h3_turbo_lora_example_workflow.json` | turbo LoRA example (fl2va pruned + turbo_v4_step600_ema) | reference example |
| `H3-Contest_BaseWorkflow.json` | old contest base (h3-realism-people LoRA) | **in special/** |
| `h3_refmod_cinematic.json` | H3 + refmod cinematic (MysticXXX MMH3-V4 + fl2v turbo 8step) | **RefMod cinematic variant — see CE** |
| `ideogramV4Workflow_v30.json` | Ideogram v4 + LTX-2.3 22B + FLUX2 (10-24) | out of scope (LTX/FLUX2 downloads) |
| `LBH_latent_upscaler_{i2v,r2v}_example.json` | **latent upscaler examples** (lightx2v turbo + `minimax_h3_latent_upscaler_3d_fp16`) | **quality-pass candidates** (needs the latent-upscaler model) |
| `mini-max-refrance-to-video-1.json` | H3 ref2va base (pruned int8 + qwen3vl_32b) | superseded by canonical r2v |
| `Minimax H3 Workflow_ Magic Time Period Shift.json` | time-period shift subgraph (fl2va pruned) | special (time-shift gimmick) |
| `MiniMax-H3-Character-Swap-Mask.json` | char-swap v1.5 mask | **in movies/motion** |
| `minimax-h3-guided-consistent-characters-via-reference-identity...inline-graph.json` | inline graph (not UI format) | reference |
| `Minimax-H3_zuanfilm_res2s.json` | H3 + Zuanfilm res2s (VRAMCleanup + first-block-cache + Clownshark) | special (zuanfilm H3 variant) |
| `minimaxH3Camera_v10/v20.json` | camera control (v20 = canonical) | **v20 in movies/motion**; v10 = superseded |
| `minimax_h3_sam_r2v_*` | sam 2-char/cinematic | **in movies/motion** |
| `h3_refmod_cinematic` — see above. |
| `Ep29 continuation` / `Dialogues` — see above. |
| `krea2POSESTUDIOPoseYour_v10.json` (production_experiments) | Krea2 pose-studio (pose-anchored) | special (pose) |
| `LocationOrbitSheetH3.json` (production_experiments) | **location orbit sheet** (H3 orbit around a location) | **world/ candidate — see camera idea** |
| `MiniMax-H3-Character-Sheets.json` / `MiniMax-H3-Character-Swap-Mask.json` / `miniMaxCharacterReplace_v11.json` (production_experiments) | sheet/swap/replace variants | superseded (canonical versions in movies/) |
| `redetail20LTX25VideoRefine_v20.json` | LTX-2.5 redetail (LTX-dependent) | out of scope |
| `VRGDG_MiniMaxH3_2Pass_MusicVideo_Shareable.json` (production_experiments) | 2-pass music video (D041) | special (D041) |
| `audio_splitter.json` / `continuous_static_video_without_quality_loss.json` / `foxydits_sucks_at_making_workflows_v7.2.json` (production_experiments) | audio splitter (ChatterBox) · static-video quality hold · foxydits test | special (audio-splitter = also in `minimax_continuous_audio_splitter/`) |
| `Zuanfilm_Retrolab.json` (production_experiments, 11-19) | the grade workflow | **in movies/grade** |
| `krea2POSESTUDIO` — see above. |

## E:\minimax_workflow — subfolders

| Folder | Contents | Purpose · Status |
|---|---|---|
| **`consistent_environment`** | room photos + room RefMod + workflow screenshot | ★ **the find** — see deep-dive above. PROMOTION CANDIDATE (camera/world stage). |
| **`comfyui-vrgamedevgirl`** (THE PACK) | **RefMod suite** (`MiniMaxH3RefMod{Extract,Inspect,Loader}`, `VRGDG_RefMod{Describe,ImagePicker}`, `refmodtrain.json`, `refmodinfo.json`, `refmod_scene_cases.json`) · **MatchGrain** (image + video — grain-matching to a reference = film-grade utility) · **Two-Stage-Sampling-v2** (4 workflows: FastH3 two-model refinement test · H3 I2V 2-stage 77n · **H3 R2V 2-stage 109n** · 2-pass shareable [D041] — draft-turbo → full-refine = the quality stage) · **masked_continuation_test** (2 scenes · masked seam predecessor/continued — cross-scene continuation via masking) · **masked_seam_test** (Scene08→09 masked seam ×2 — same) · **audio-driven H3 builders** (7: audio-driven · audio-driven 2-pass latent-upscale · normal 2-pass · built-in-audio · i2v-audio-driven · ref2video 2-pass · **ref2video 3-pass** — dialogue-driven video, D041-safe) · **`minimax_h3_2pass_refmod_test_api`** (the CE rig in API format, all local models) · MatchGrain image/video · **fluxKleinSubjectLocation + fluxKleinMultiImage** (subject placement for multi-char layouts — flux-2-klein-4b) · Krea2 API family (t2i/2-pass/train-sample — all Krea2 models we have) · LTX2.3 family (7 — out of scope) · image_ernie (ernie-image-turbo — missing) · **memory utils** (`RAMCleanup`, `VRAMCleanup`, `VRGDG_UnloadGemmaModels`, `ClearMemory_API`) | **THE PACK TO INSTALL** — RefMod + MatchGrain + 2-stage + masked-seam + audio-driven + memory utils. Install = copy folder to `custom_nodes` + restart. |
| **`H3-LongTakeNoCuts`** | `LongTakeNoCuts_example_workflow__v01/v02` | **long-take H3** (fl2va pruned + ref2va pruned + video_vae — ALL LOCAL ✓) — the long-take stage. CORRECTION: previously guessed out-of-scope — it is fully local. |
| **`Herrgotts-H3-Infinite-Continuation-Suite`** | `Herrgotts_H3_Infinite_v1.4`: 01_Start · 02_Continue · 03_3Clip_Showcase_AutoStitch · 04_Stitch_Saved_Chain (nodes `H3Continuous{AnalyzeHandoverV14,SaveLatent,StitchOutput,StitchSavedChainV14}`) | **infinite continuation suite** — chain N clips with handover analysis + auto-stitch (all local models ✓). Complements our seamless 15s/30s. Needs the Herrgotts pack installed. |
| **`MiniMax-H3-NativeAudio-MusicVideo-Workflow`** | MusicVideo template (D041) + RIFE interpolation (in movies/grade) + **`chain/` (8 files: 05/06/07/08 Chained + GGUF variants, with AudioLock + RefImage)** — `H3MultishotSampler` + `H3ModelLoaderAny` + `MiniMaxH3SigmaShift` = **multi-shot chaining with audio lock + reference image** | The **multi-shot stage** (several shots in one generation without regeneration). Non-GGUF chain variants use models we have. GGUF variants need `minimaxH3GGUF_fl2va.gguf` + `qwen3vl_32b_nvfp4_awq` (missing). MusicVideo template = D041-excluded. |
| **`h3-recast`** | `H3_Recast.json` | duplicate of canonical (in movies/motion) |
| **`h3_clown_anchoring`** | clown-anchoring H3 experiments | special (test) |
| **`character_sheet`** | sheet variants | superseded (movies/sheets has the routes) |
| **`h3-recast` / `blender+minimax`** | Blender + H3 character pipeline (Motion2MixamoRig integration) | the Blender rigging bridge |
| **`minimax_continuous_audio_splitter`** | audio splitter (ChatterBox) ×2 | in special/ (audio tool) |
| **`Motion2MixamoRig`** | Python tool `motion2mixamorig-0.1.8` (video → Mixamo rig) + venv (most of the 363-row count = venv site-packages noise, not workflows) | **motion-capture bridge**: video → Mixamo rig → Blender character pipeline. Tool, not workflows. |
| **`NVlabs-Sana-sol-engine`** | engine + evals/benchmarks (data JSON) | out-of-scope testbed (Sana/sol weights = downloads) |
| **`seamless_video_combiner`** | `clussy_origin_story.json` (VHS combiner) | in special/ (intro era) |
| **`Seamless_vlog_workflow`** | `withers_has_big_nattys.json` (motion-context vlog) | in special/ |
| **`sol_h3_weights`** | sol_h3 weight files | out of scope (weights = download-dependent until 11-24) |
| **`Bruxosdovfx-SyncTile-MiniMax-H3-v5.4`** | SyncTile pack (scene sync tiling) | pack — for tiled large-frame consistency |
| **`comfyui-load-audio-batch-from-dir`** | batch audio load pack | pack — batch audio for the audio-driven builders |
| **`production_experiments`** (11 files) | see top-level section above | mixed (some promoted, some special, 2 out-of-scope) |

## Canonical dir (organized 11-19) — summary

`movies/` = 92 reusable across 8 stages (sheets 30 · identity 5 · motion 21 · image 17 · grade 9 · world 2 · audio 3 · utility 5) + `special/` = 110. Full mapping: `WORKFLOW_TRIAGE_2026-11-19.md`.

## Model availability (H3 family, main models path)

**HAVE:** UNets — `Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8` · `minimax_h3_{ref2va,fl2va,image}_pruned_int8_convrot` · `ref2va_pruned_fp8_scaled` · `fl2va_int8_convrot` · `fasth3_omniref_{8step_pruned_int8_convrot,qad_nvfp4_comfy}` · `fastvideo_fasth3_8step_v2_pruned_int8_convrot` · LoRAs — turbo 4/8-step (ref2v/fl2v v0.1–v1.1 768p) · hyperflow_8step · character_swap v1.0/v1.1/v1.5/pro4500 · facial-realism-closeup · H3-Person-Remover · **dr0nesh0t_aerial_flyover** (aerial LoRA!) · tiktok_aesthetic · CLIP — Qwen3-VL-32B GGUF Q4_K_M + mmproj · qwen3vl_8b_int8 · VAEs — video_vae fp16/int8_convrot · audio_vae_fp32 · image_vae_fp16 · taeh3 · fast_h3_vae_noncausal_24l.

**MISSING but swappable:** `82va_pruned_int8_convert` (= ref2va_pruned_int8_convrot) · `turbo3_step_lora` (= our 4/8-step turbo) · `qwen3vl_32b_mr_fp4` (= our GGUF) · `video_vae_int8_convert` (= our int8_convrot).

**Actually missing (download-dependent → 11-24+):** `minimax_h3_latent_upscaler_3d_{bf16,conv_v1_b}` (latent-upscale stage) · `minimax_h3_turbo_v4_step600_ema` · `fl2v_lightx2v_turbo_4step...rank21_bf16` · `minimaxH3GGUF_fl2va.gguf` + `qwen3vl_32b_nvfp4_awq` (GGUF chain variants) · flux-2-klein family · all LTX-2.3/2.5 · ernie-image-turbo · ControlFoley TC-V2A audio encoder (verified empty 11-18).

## Action board (film-relevant)

1. **`consistent_environment` → runnable:** install `comfyui-vrgamedevgirl` pack + copy `MyRoom_Experiment_Refmod.safetensors` to models + rebuild the rig JSON (from screenshot or `minimax_h3_2pass_refmod_test_api.json`). Then: **train per-environment RefMods** (pitch / 1950s village / 2026 stadium / school) → ball-POV, referee-POV, and **environment-locked camera motions** (dolly/pan/orbit/POV) for the film.
2. **Promote (local, ready):** `H3-LongTakeNoCuts` ×2 → `movies/motion/` · `masked_seam_test` ×2 → `movies/motion/` (needs VRGDG pack) · `LocationOrbitSheetH3` → `movies/world/` · `h3_refmod_cinematic` → `movies/motion/` (needs VRGDG pack).
3. **Pack installs (copy from staging + restart):** `comfyui-vrgamedevgirl` (RefMod/MatchGrain/2-stage/masked-seam/audio-driven/memory) · `Herrgotts` continuation suite (if the pack ships with it — verify) · `Bruxosdovfx-SyncTile` (tiled consistency).
4. **Out of scope until 11-24 (downloads):** LTX family · sol_h3 weights · latent-upscaler models · ControlFoley · klein flux-2 family.
5. **D041-excluded:** all MusicVideo templates (kept in `special/`, other-content-only).
6. **Archive candidates (superseded, already in `special/`):** v10 camera · old-era continuation · intro-era combiners.
