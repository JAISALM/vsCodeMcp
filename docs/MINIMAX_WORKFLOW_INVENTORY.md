# E:\minimax_workflow — Inventory & Audit (P8, completed 2026-10-24)

Audit method: every top-level JSON parsed (UI vs API format), every node class
cross-checked against the LIVE `/object_info` catalog (read-only HTTP, no GPU).
Embedded subgraphs (`definitions.subgraphs`) audited by their INTERNAL classes.
UUID-typed instance nodes (e.g. `4c314f31-...`) are NOT missing classes — they are
subgraph instances whose definitions are embedded in the file.

## Top-level workflows (24 JSONs)

### Fully resolvable as-is (all classes in live install — runnable today)

| File | Classes | Notes |
|---|---|---|
| `H3-Contest_BaseWorkflow.json` | 19 | H3 base/contest workflow |
| `Workflow for Minimax H3 image editing w ComfyUI.json` | 17 | H3 image editing |
| `video_minimax_h3_r2v+turbo.json` | 19 | **H3 R2V + turbo LoRA — the P4 movie tool** |
| `Minimax H3 Workflow_ Magic Time Period Shift.json` | 18 + embedded subgraph (15, all resolve) | time-period shift |
| `minimaxH315SecondSeamlessMulti_v11.json` | 23 + embedded subgraph (17, all resolve) | 15 s seamless multi |
| `qwen_minimzed_h3.json` | 18 + embedded subgraph (14, all resolve) | Qwen-optimized H3 |
| `2BZ_H3_character_sheet_2stage_v1_EN.json` | 33 + embedded subgraph (12, all resolve — incl. `ToobusyMiniMaxH3ImageLatent`) | 2-stage character sheet |
| `Dialogues.json` | 26 + embedded subgraph (3, all resolve) | dialogue pipeline |

### Effectively runnable (missing only decorative/utility nodes)

| File | Missing | Effect |
|---|---|---|
| `video_minimax_h3_r2v.json` | `MarkdownNote` (pack's own note node — loads with FilmStudio restart) | cosmetic |
| `mini-max-refrance-to-video-1.json` | `Note` | cosmetic |
| `WF-H3_zuanfilm-Face_Detailer.json` | `Note` | cosmetic |
| `MiniMax_H3_FL2VA_Fiirst-and-Last-Frame-Workflow.json` | rgthree `Fast Groups Bypasser` + notes | needs rgthree (or node removal) — FL2VA = first/last-frame-to-video, our long-shot anchor tool |
| `minimax_h3_sam_r2v_cinematic.json` | rgthree `GetNode`/`SetNode` + `Note` | needs rgthree |
| `minimax_h3_sam_r2v_2char_cinematic.json` | same as above (2-char cinematic!) | needs rgthree — **directly relevant to our 2-man movie** |
| `fl_minimax_h3_turbo_lora_example_workflow.json` | EastMoe `SolAttnPatch` + `MarkdownNote` | needs EastMoe |

### Need pack installs (real missing capability)

| File | Missing packs/nodes |
|---|---|
| `minimaxH3Camera_v10.json` / `_v20.json` | EastMoe `EastMoeSolAttn` |
| `h3_refmod_cinematic.json` | `MiniMaxH3RefMod*` (comfyui-minimax-h3-refmod) |
| `minimax_h3_character_swap_workflow.json` | `BFSShot*` (shot planner) + `BiRefNetRMBG` (BiRefNet) + EastMoe |
| `Ep29 MiniMaxH3_Continuation_Workflow.json` | JW `JWFloatToInteger` + `MiniMaxH3DualClockSamplerT8` + EastMoe + `RAMCleanup` + rgthree |
| `Minimax-H3_zuanfilm_res2s.json` | `ApplyMiniMaxH3FirstBlockCache` (zuanfilm) + `RAMCleanup` |
| `minimax-h3-guided-consistent-characters-via-reference-identity-face-body-cloths.inline-graph.json` | NOT a runnable UI file — platform export format (`target` UUID, `version: 2`, keys app/graph/params/prompt) — re-export/conversion needed |

### Pack gap list (install these to unlock the "need pack installs" tier)

1. **EastMoe** (`SolAttnPatch`, `EastMoeSolAttn`) — camera + turbo-LoRA examples
2. **rgthree** (GetNode/SetNode/muters/Label) — 5 files
3. **JW nodes** (`JWFloatToInteger`) — Ep29 continuation
4. **RAMCleanup** — Ep29 + zuanfilm res2s
5. **BiRefNet** (`BiRefNetRMBG`) + **BFSShot** pack — character-swap workflow
6. **comfyui-minimax-h3-refmod** — refmod cinematic
7. **zuanfilm** FirstBlockCache — res2s

## Subfolders

| Folder | Contents | Relevance |
|---|---|---|
| `H3-LongTakeNoCuts/` | v01 + v02 example workflows + `character.png` | **P7 suite — matches the installed LongTakeNoCuts pack** |
| `Herrgotts-H3-Infinite-Continuation-Suite/` | v1.4 samples 01–04 + `README.md` + example mp4 | **P7 suite — matches the installed Herrgotts pack** (validation after restart) |
| `MiniMax-H3-NativeAudio-MusicVideo-Workflow/` | FULL git repo (custom_nodes + workflows + `run_nvidia_gpu_optimized.bat`) | NativeAudio MusicVideo — **music-oriented → low value under D041 (no music)**; audio/SFX parts worth a look later |
| `blender+minimax/` | `camera_reference_5s_square.blend` + `.mp4`, guide PDF, character/environment refs, `blender_camera_motion_prompt.txt`, `video_minimax_h3_r2v-workflow.json` | **P2 (Blender → H3) assets** |
| `character_sheet/` | 5 sheet workflows (2BZ 2-stage H3, Qwen-Image-2.1 sheet, `LocationOrbitSheetH3`, patreon sheet) + images | character-sheet generation options |
| `consistent_environment/` | `MyRoom_Experiment_Refmod.safetensors` + 3 room photos + workflow.png | refmod environment-consistency experiment |
| `production_experiments/` | `audio_splitter.json`, `continuous_static_video_without_quality_loss.json`, `foxydits...v7.2.json`, `LocationOrbitSheetH3.json`, `VRGDG_MiniMaxH3_2Pass_MusicVideo_Shareable.json` | misc experiments (2-pass music video → D041-restricted) |

## Bottom line

- **8 files runnable today, no installs** (incl. the P4 tool `video_minimax_h3_r2v+turbo`).
- **7 more runnable with cosmetic gaps** (notes) or one small pack (rgthree).
- **7 need real pack installs** (EastMoe / JW / RAMCleanup / BiRefNet / BFSShot / refmod / zuanfilm) — list above.
- **1 is a platform export** (inline-graph v2) — not directly loadable.
- P7 suites (LongTakeNoCuts v01/v02, Herrgotts v1.4 01–04) are here for post-restart validation.
