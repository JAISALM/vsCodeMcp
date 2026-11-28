# COMMUNITY WORKFLOW LIBRARY — ARSENAL INDEX (2026-11-28)

Source: **`E:\minimax_workflow\`** (author-saved community workflows/packs). Triage done
2026-11-28 against the Dec 6 teaser plan. **Rule: every community workflow gets
`validate_workflow` + a paid-node audit BEFORE first run (D192 — author queues).**
Model root = `E:\ComfyUI_windows_portable\ComfyUI\models` (the :8188 install reads it).

## DEC-6 CRITICAL PATH (use these first)

| Item | What it does | Needs (live? on :8188) | Maps to |
|---|---|---|---|
| **`H3-LongTakeNoCuts`** (v01/v02) — the Reddit "2-min selfie continuous take" post (author item 1) | ONE continuous take, no cuts: per-shot prompt switching (`SetNode`/`GetNode` shot_index + `easy textIndexSwitch`), **MotionContext chain** (pin previous clip's frames as never-denoised rows), **`H3BlendLatentsByFrames`** frame-blend map, VRAM-friendly attention (`MiniMaxLowVRAMAttention`/`MiniMaxChunkFeedForward`/`MiniMaxH3MotionContext*` all LIVE ✓), `VAEDecodeAudio` LIVE ✓, H3 length grid = **17n+5 frames** (124 = 7×17+5 ✓) | models: fl2va ✓ + ref2va ✓ (19.5 GB, both roots) + qwen3vl ✓ + taeh3 ✓. **GAP: `MiniMaxH3HybridLoader` NOT live** (closest = `H3RelayInternalHybridLoader`) → swap the loader node or update the H3 pack before running | teaser assembly: 60–90 s continuous-feel sequence across the 3 beats; 15 s+ shots |
| **`character_sheet\`** — `minimaxH3CharacterSheet_v10.json` · `2BZ_H3_character_sheet_2stage_v1_EN.json` · `LEEBLAAB-QwenImage21-Character-SHEET.json` + `Qwen Image 2.1 Character Design Sheet.json` · `LocationOrbitSheetH3.json` · `minimaxh sheet patreon.json` | H3-native character sheets (two-stage), Qwen-image sheets (our local Qwen :8100 can drive), location ORBIT sheets | validate on first use | **CHARACTER IMAGE LAYER** (supersedes Krea2-identity-edit × 2 as primary; Krea2 stays as face-lock fallback) |
| **`consistent_environment\`** — `MyRoom_Experiment_Refmod.safetensors` + ref photos · `workflow.png` | Refmod-based ENVIRONMENT consistency | Refmod mechanism | ENVIRONMENT LAYER — pairs with the 35 Krea2 plates (plates = the set; Refmod = the consistency across shots) |
| **`minimax_h3_sam_r2v_2char_cinematic.json`** (101 KB) + `minimax_h3_sam_r2v_cinematic.json` · `minimax-h3-guided-consistent-characters-via-reference-identity-face-body-cloths.inline-graph.json` | SAM-assisted **multi-character** cinematic; guided consistency via identity/face/body/cloths refs | SAM3 live ✓ (models present) | **THREE-CHARACTER GATE** (Sc 6 ground: adapt 2char → 3 ref slots + rule-5 layout per `14_PROMPT_CRAFT.md`) |
| **`Minimax H3 Workflow_ Magic Time Period Shift.json`** | period shift | validate | **2026 ↔ 1950 dual-timeline** (Sc 22–23) |
| **`LBH_latent_upscaler_{i2v,r2v}_example.json`** — author item 3 (AIWarper upscaler post) | latent upscaling for H3 i2v/r2v | **`PainterMinimaxH3LatentUpscaler` + `MinimaxH3LatentUpscalerNode2D` LIVE ✓** (+ `SEGSUpscaler`, `Pixel*` ups calers) | **UPSCALE STAGE** — before the 1080p post-fix chain (D275); the X post body was NOT retrievable (timeline stale — top items Oct 2026) but the mechanism is saved + runnable either way |
| **`Library_VFX_Lip Sync and Localization_MiniMax H3 - Translate and Lip Sync.json`** — author item 2 | video-in → translated dub out: ElevenLabs isolation/clone/STT → LLM translate → TTS → **LOCAL core = MediaPipe mouth mask (`mediapipe_face_fp32`) → `SetLatentNoiseMask` → H3 regenerates MOUTH ONLY to fit the dub → composite onto untouched frames** | MediaPipe nodes LIVE ✓ · ElevenLabs + OpenRouter nodes LIVE ✓ (keys needed = the paid part) · **`mediapipe_face_fp32.safetensors` MISSING in `models\detection`** (only hard blocker) · ref2va ✓ | **P1 Malayalam dub route (D050)** — replace the ElevenLabs/OpenRouter block with our own audio: author's headset dub → RVC (D050) → feed `new_audio`; keep the mouth-mask chain. LatentSync local build = SUPERSEDED by this H3-native mouth-mask route (not cloned, not needed) |
| **`MiniMax_H3_FL2VA_Fiirst-and-Last-Frame-Workflow.json`** | first/last-frame anchoring | validate | shot-to-shot stitching |
| **Continuation/seam family** — `minimaxH315SecondSeamlessMulti_v11.json` · `seamless_video_combiner\clussy_origin_story.json` · `Seamless_vlog_workflow` · `Herrgotts-H3-Infinite-Continuation-Suite` · `Ep29 MiniMaxH3_Continuation_Workflow.json` · `minimax_continuous_audio_splitter` · `Bruxosdovfx-SyncTile-MiniMax-H3-v5.4` (pack) · `Minimax-H3-Latent-Continuation` (pack) | 15 s+ seamless multi-shot, infinite continuation, audio splitting | **SyncTile H3 nodes LIVE ✓** (`SyncTileGuiderH3`, `SyncTileRef2VAConditioningH3`, `SyncTileI2VConditioningH3`, `SyncTileStreamDecodeVideoH3`) · `MiniMaxH3NativeLatentContinuationConcatT8Advanced` LIVE ✓ | long-shot bridges (Maracana A0→A3), clip stitching |
| **`minimaxH3Camera_v10/v20`** · **`krea2POSESTUDIOPoseYour_v10.json`** | camera control · pose control | validate | craft rule ① camera lines (`14_PROMPT_CRAFT.md`) |
| **`Zuanfilm_Retrolab.json`** + `WF-H3_zuanfilm-Face_Detailer.json` | retro grade · face detailer | validate | **1950 B&W grade** (Sc 22–23) + FaceRefine pass |
| **`h3-recast\`** (repo + `H3_Recast.json` + example inputs) · `MiniMax-H3-Character-Swap-Mask.json` · `miniMaxCharacterReplace_v11.json` · `minimax_h3_character_swap_workflow.json` | character recast / swap with masks | validate | character replacement across episodes |
| **`Motion2MixamoRig\`** (full repo + venv) · **`blender+minimax\`** (camera-ref pipeline + boar_grave demo) | mocap → Mixamo retarget · Blender camera reference → H3 | author's pending queue | mocap + camera-ref shots (author queue, D192) |
| **`sol_h3_weights\fasth3_4step_dense_datafree_adapter.safetensors`** (1.45 GB) + **`NVlabs-Sana-sol-engine\`** | SANA SOL 4-step data-free distillation engine | future speed path | faster H3 shots once the teaser is proven |
| **`qwen_minimzed_h3.json`** · **`h3_refmod_cinematic.json`** · **`fl_minimax_h3_turbo_lora_example_workflow.json`** · **`video_minimax_h3_r2v(+turbo).json`** · **`H3-Contest_BaseWorkflow.json`** | memory-minimized H3 · refmod cinematic · turbo-lora example · base R2V variants | validate | base rigs |
| **`MiniMax-H3-NativeAudio-MusicVideo-Workflow`** (VRGDG) + `comfyui-vrgamedevgirl\` (framework) + `Dialogues.json` | native-audio music video · dialogue workflow | **D041: music N/A for us** — native-AUDIO mechanism + dialogue flow are reusable | dub pipeline support |
| **`ideogramV4Workflow_v30.json`** | Ideogram v4 (API model — NOT local) | API | title cards / graphics only |
| **`foxydits_sucks_at_making_workflows_v7.2.json`** (389 KB) · `audio_splitter.json` · `redetail20LTX25VideoRefine_v20_3277022.json` | VFX-library demo · audio splitter · LTX-2.5 video refine (redetail20) | validate | the VFX library the lip-sync workflow comes from |

## PAID-NODE AUDIT (which community files contain paid/API nodes)

- `Library_VFX_Lip Sync…` = **ElevenLabs ×4 + OpenRouterLLM (claude-opus-5)** — nodes live,
  keys absent. Integration = swap that block with local RVC + local Qwen (:8100).
- `ideogramV4Workflow_v30` = Ideogram API (not local at all).
- `261116/261127_MICKMUMPITZ_*` + `character_sheet\minimaxh sheet patreon.json` =
  mickmumpitz's free + Patreon content (author item 4 — site page `mickmumpitz.ai/posts/new-video-free-i-176532821`
  **redirects to Patreon** = paywall confirmed; his free series is already saved here, and his
  2025 core = the multi-character-consistency tutorial + free workflows
  (`youtu.be/PZVs4lqG6LA`), which is exactly what the `minimax_h3_sam_r2v_2char` +
  guided-consistency files in this library implement).
- `VRGDG_MiniMaxH3_2Pass_MusicVideo_Shareable.json` — audit on first use (framework-driven).
- **Everything else in the library is local H3/Krea2 mechanisms — free.**

## MICKMUMPITZ H3-VFX SUITE (author-downloaded 11-28 12:18 — the "new-video-free" series, 4 files in `production_experiments\`)

| File | What it does |
|---|---|
| **`261116_MICKMUMPITZ_H3-IMAGE_1-2.json`** | **IMAGE**: refs (optional) + plain-words instruction → image out: **reference/character sheets + start frames** for the VFX workflow. H3 ref2va @ up to 2016×1152 (1.5×), **TURBO? switch = 8 fast steps** vs official 50. |
| **`261127_MICKMUMPITZ_H3-VFX_1-3.json`** | **VFX**: filmed **plate + "what should change" → the edited shot, frame-for-frame on the plate** (fun-controlnet-union model-patch + DA3 depth + control checkpoint). QUALITY Draft/Full/**Final = H3's own 50 steps**; MAX-FRAMES switch. |
| **`261127_MICKMUMPITZ_H3-VFX-PREPROCESS_1-3.json`** | **PREPROCESS**: plate → the VFX helper videos: edges, pose (SDPose), depth (DA3), tracking dots (CoTracker), subject mask (SAM3.1), person-on-flat-colour, combined-control video (8 SaveVideo outputs, switched individually). |
| **`H3-VFX_AGENT_INSTALL.md`** | **install+operate doc WRITTEN FOR AI AGENTS** (CHECK-gated; license note = EU/UK/KR/USA only — India = Community License, N/A). |

**Local readiness audit (11-28, verified on disk):** ComfyUI **0.45.2 ✓** (≥0.44) · packs **KJNodes ✓ · ComfyUI-Mickmumpitz-Nodes ✓ · rgthree ✓** (missing: CoTracker = PREPROCESS TRACK-DOTS? switch only · MMH3-UltimateUpscale = H3-IMAGE UPSCALE? advanced only — both optional/ASK) · models: ref2va ✓ qwen3vl ✓ video VAE ✓ audio VAE ✓ **fun-controlnet-union 2.14 GB ✓** **SAM3.1 ✓** · **MISSING (3 core, ≈3.9 GB total):** `loras\minimax_h3_turbo_v4_step600_ema_pruned_comfyui.safetensors` (620 MB, drbaph HF) · `checkpoints\sdpose_wholebody_fp16.safetensors` (1.9 GB) · `geometry_estimation\depth_anything_3_mono_large.safetensors` (1.3 GB) · optional: `upscale_models\RealESRGAN_x2.pth` (67 MB). **Consequence: H3-IMAGE (character sheets) is ONE 620 MB download from runnable — unblocks the character-image layer for 11-29; H3-VFX + PREPROCESS need all three.**
**Plan mapping:** H3-IMAGE = CHARACTER IMAGE LAYER (supersedes Krea2-×2 as primary — H3-native, fast turbo 8-step) · H3-VFX = **SHOT-EDITING TOOL** (plate + change-prompt → frame-accurate edit — the Maracana RAIN VFX pass, environment anchoring on plates, per-frame consistency) · PREPROCESS = control-signal factory.

## STATUS OF THE 11-28 AUTHOR ITEMS

1. **Reddit LongTakeNoCuts post** → workflow saved by author (`H3-LongTakeNoCuts\` v01/v02),
   node audit done above, models present. IN ARSENAL (this doc). Only gap = the
   `MiniMaxH3HybridLoader` swap. The post body itself: Reddit IP-walled today (engine =
   "Prove your humanity" challenge; CDP tier down — Brave not running with the 9222 flag);
   the workflow details came from the saved JSON instead — same content.
2. **Lip-sync workflow (shared 11-26, "one paid node")** → **NOT integrated** (verdict only:
   "let's integrate"). On-disk 11-28: no LatentSync repo, no `mediapipe_face_fp32`, no
   wiring. New plan (D277): the H3 mouth-mask route from the saved VFX-library workflow +
   our RVC dubs — one model download away (`mediapipe_face_fp32.safetensors` →
   `models\detection`).
3. **AIWarper upscaler post** → body not retrievable (timeline fetch returned stale Oct-2026
   items); the mechanism (LBH latent upscaler) is saved + the pack is live. IN ARSENAL.
4. **mickmumpitz** → site = **Patreon redirect (paywall confirmed)**; his free recent series = the **H3-VFX SUITE (4 files, author-downloaded 11-28 12:18)** — see the suite section above: full local readiness audit done (≈3.9 GB of models missing, all packs present, ComfyUI 0.45.2 ✓). His 2025 core = the multi-character-consistency tutorial (`youtu.be/PZVs4lqG6LA`) — what `minimax_h3_sam_r2v_2char` + guided-consistency implement.
