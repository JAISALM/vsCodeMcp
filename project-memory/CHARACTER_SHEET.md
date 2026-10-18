# Character Sheet — sources, workflows & analysis (created 2026-10-18)

**Purpose:** the single reference for everything related to character-sheet generation in this
project. Reconstructed 2026-10-18 — user had shared these before but the details were lost from
memory. Anything future related to character sheets starts here.

**Standing rule (user directive 2026-10-18): no ComfyUI workflow runs without explicit user
confirmation.** The ComfyUI server is currently DOWN (crashed ~17:12 during a Qwen-2.1 sheet
test) — bring-up also needs the user's go-ahead.

## Sources (user-shared, 2026-10-18)

| # | Source | Link | Working title |
|---|--------|------|---------------|
| P1 | reddit r/comfyui `1wxixua` | https://www.reddit.com/r/comfyui/comments/1wxixua/minimax_h3_image_generation_create_consistent/ | MiniMax H3 image gen — create consistent [character] |
| P2 | reddit r/StableDiffusion `1vov6jb` | https://www.reddit.com/r/StableDiffusion/comments/1vov6jb/create_full_character_location_sheets_in_seconds/ | Full character + location sheets in seconds |
| P3 | reddit r/StableDiffusion `1w2dujd` | https://www.reddit.com/r/StableDiffusion/comments/1w2dujd/i_turned_that_h3_as_an_image_editor_post_into_a/ | "H3 as an image editor" turned into a [workflow] |
| P4 | reddit r/StableDiffusion `1wsb4h3` | https://www.reddit.com/r/StableDiffusion/comments/1wsb4h3/minimax_h3_ref_fizgig_nodes_as_sota_ref2img/ | MiniMax H3 REF + Fizgig nodes as SOTA ref2img |
| P5 | reddit r/comfyui `1wsee1y` | https://www.reddit.com/r/comfyui/comments/1wsee1y/character_sheet_workflow_qwen21/ | Character sheet workflow — Qwen 2.1 |
| HF | HuggingFace `PoopMan333/H3_Character_Sheet_Generator` | https://huggingface.co/PoopMan333/H3_Character_Sheet_Generator/tree/main | H3 character sheet generator (repo) |
| LOCAL | `E:\minimax_workflow\character_sheet\` | (local disk, 4 files, user-placed 2026-10-18) | user-saved workflows — cross-check vs posts |

Local files: `2BZ_H3_character_sheet_2stage_v1_EN.json` (150 KB),
`LEEBLAAB-QwenImage21-Character-SHEET.json` (67 KB), `LocationOrbitSheetH3.json` (26 KB),
`minimaxh sheet patreon.json` (43 KB).
(Also present in `user\default\workflows\character sheet\`: the same 4 + a
`minimax_h3_character_sheet_1wxixua.json` copy.)

**Cross-references (existing memory):** `PRODUCTION_CONSISTENCY.md` "Sources (2026-10-08)" already
listed P4 (`1wsb4h3`), P5 (`1wsee1y` — "workflow already saved"), and P1 (`1wxixua`, "MiniMax H3
consistent character").

## Fetch status (2026-10-18)
- [x] Local workflow inventory + node-level analysis (all 4 files).
- [x] HF repo tree + full README (complete).
- [x] Model + node-pack availability gap check.
- [ ] P1–P5 post bodies — **ALL routes blocked** (table below). Retry windows noted.

## Reddit fetch routes — tested 2026-10-18 (all blocked)

| Route | Result |
|---|---|
| MCP `get-single-web-page-content` → reddit.com | 403 "Prove your humanity" (JS challenge) |
| harness `web_fetch` → reddit `.json` | 403 |
| `utilities\reddit_fetch.py` (session-cookie helper) | 403 ×3 — the `REDDIT_SESSION_COOKIE` env (from 2026-10-11) is stale |
| `red.artemislena.eu` mirror | Anubis proof-of-work gate (needs browser JS) |
| `rl.bloat.cat` mirror | dead (ECONNRESET) |
| `r.jina.ai` reader proxy | anonymous reddit access blocked until **13:04 UTC (18:34 IST) 2026-10-18** — retryable after that |
| websearch MCP / built-in search | 0 indexed results; built-in web_search has no API key configured |

**Clean fix (one-time user action):** refresh `REDDIT_SESSION_COOKIE` — open reddit.com in the
browser, F12 → Application → Cookies → www.reddit.com → copy the `reddit_session` value and
share it. The helper auto-solves the JS challenge and persists the new cookie
(`C:\Users\user\.dsh\fetch_creds\reddit_cookies.txt`). This route is proven (worked 2026-10-11).

## Per-post explanations (inferred from matching local workflow + README + titles — post bodies pending)

### P1 — "MiniMax H3 image generation: create consistent character" (r/comfyui 1wxixua)
- Memory (10-08): "MiniMax H3 consistent character: r/comfyui 1wxixua" — using H3's
  multi-reference capability (up to 9 refs) for character consistency.
- **Best match: the PoopMan333 HF repo** (README describes exactly this post's concept).
- **How it works:** feed up to 9 rough refs (face from here, armor from there — H3 holds them
  together) → A-Prompt (user: one line per reference — what to take and what to **ignore**) +
  B-Prompt (handles the spin/pose/lighting; since 10 Sept a "general purpose" A prompt makes it
  near-effortless) → H3 generates a **slow 360° orbit video** (character stands still, no hard
  cuts) → grab **6 frames** (4 in the faster version) → stitch into a sheet to reuse forever.
  Rationale: six frames from ONE video pass can't drift (jaw/jacket/colour drift between separate
  generations is the problem). Optional outputs: the 360 spin video + every individual frame.
- **Files:** `H3_CharSheetMaker_6_Panel.json` (front, both sides, back + two face shots),
  `H3_CharSheetMaker_4_Panel_(Faster).json` (~40% fewer frames),
  `H3_ExpressionsSheetMaker_6_Panel.json` (experimental, 22 Sept — close-up face-deformation
  sheet to reinforce the face; "the model typically does not need this"),
  `B prompts/Anime2Real - 6 panel.txt`, `early_version/`, `old/`, `examples/SHEET_00393_*`.
- **Update log:** 10 Sept — general-purpose A prompt + turbo LoRA switched to
  `minimax_h3_turbo_v4_step600_ema` ("slightly better results"); 29 Aug — 4-panel fixed to 73
  frames (was 124), speed-up nodes, **use 8 steps instead of 25 when using speed-ups**;
  22 Sept — experimental expressions sheet.
- **Models:** `minimax_h3_ref2va_pruned_int8_convrot.safetensors` (diffusion_models/),
  `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` (text_encoders/),
  `minimax_h3_video_vae_int8_convrot.safetensors` + `minimax_h3_audio_vae_fp32.safetensors`
  (vae/), optional turbo LoRA `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors`
  (loras/). INT8 low-VRAM builds; higher precision (esp. the text encoder — "that's where prompt
  adherence lives") gives better detail.
- **Custom nodes:** near-vanilla; only third-party in the optional Speed Ups group:
  **KJNodes + rgthree** (toggle panel). Delete that group to go vanilla.
- License: minimax-h3-community-license.

### P2 — "Create full character + location sheets in seconds" (r/StableDiffusion 1vov6jb)
- **Local match: `LocationOrbitSheetH3.json`** — two chains:
  (a) **Krea2 t2i** location image (`Krea2_Turbo_convrot_int8mixed` UNET + `qwen3vl_4b_fp8_scaled`
  CLIP krea2 + `qwen_image_vae`, 1920×1080) →
  (b) **H3 image-to-video orbit** of that location (`minimax_h3_fl2va_pruned_int8_convrot` UNET +
  `qwen3vl_32b_minimax_h3_nvfp4_awq` CLIP minimax + `minimax_h3_video_vae_fp16`, LoRAs
  `minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy` @1.0 + `minimax_h3_ref_lora_rank_256_bf16`
  @1.0, 1216×672 @ 124 frames, 8 steps euler/simple, MiniMaxH3SigmaShift 12.0/3.0).
- Frame handling: **OrbitSheetsFrameSelect** (6 frames, selector = **`vision_llm`** — content-based
  frame picking), **OrbitSheetsContactSheet** (2×2), `CreateVideo`/`SaveVideo` (24 fps).
- Custom pack: **OrbitSheets** (`OrbitSheetsLocationPrompt` — "interior / cut views / auto",
  `OrbitSheetsAttentionBackend` = "comfy kitchen (int8)") — **pack NOT installed here**.
- README cross-ref: PoopMan333's README points to **ethanfel's `H3_Cinematic_Multishot_Coverage`**
  (HF) for the same orbit logic applied to a room/background — this file is likely that workflow
  or a close derivative.

### P3 — "I turned that 'H3 as an image editor' post into a..." (r/StableDiffusion 1w2dujd)
- **Local match: `2BZ_H3_character_sheet_2stage_v1_EN.json`** — by **Too Busy Grasshopper (2BZ)**,
  YouTube @toobusyAI; the file's own "Inspiration & Original Post" note (node 69) links the
  original post (expected to be this P3).
- **Structure:** Stage 1 = H3 orbit front/side/back sheet of **Picture 1 = face/identity** +
  **Picture 2 = outfit only**; Stage 2 (optional, default OFF) = 1–4 **action panels** entered
  as plain-English "Panel N: ..." requests ("jump while aiming the water gun") + a final
  horizontal 16:9 composite — i.e. H3 used as an IMAGE EDITOR over the sheet.
- **Reference semantics (the clever part):** 6 LoadImage slots — face/identity, outfit, optional
  prop/weapon, optional environment, optional extra accessory, Stage-2 pose. Three
  `ToobusyMiniMaxH3SemanticReference` nodes assign explicit `<Picture N>` jobs
  ("Picture 3 = environment — use only its location/surfaces/atmosphere/lighting; do not copy
  people or text"). Four `TextGenerate` nodes run a LOCAL LLM (CLIP `gemma4_e4b_it_fp8_scaled`,
  type krea2) to analyze the optional refs → "VISUAL_REFERENCE: YES/NO" lines + a
  "POSE TRANSFER:" block.
- **Models:** UNET `minimax_h3_ref2va_pruned_int8_convrot` ✓, CLIP
  `qwen3vl_32b_minimax_h3_nvfp4_awq` (type minimax) ✓, image VAE
  `minimax_h3_t1_image_vae_step1597` ✗, audio VAE `minimax_h3_audio_vae_fp32` ✓, turbo LoRA
  `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16` @0.75 ✓; sampling chain KSamplerSelect
  `er_sde` + BasicScheduler + SamplerCustomAdvanced + RandomNoise + BasicGuider;
  `ToobusyMiniMaxH3ImageLatent` 1344×768; save prefix `charsheet/H3_2STAGE_STAGE1_3VIEW`.
- **Packs:** **toobusy** (publisher `neobabae`, ≥ v0.4.9) ✗ NOT installed, **pysssss**
  (MathExpression, ImageConcanate) ✗ NOT installed, KJNodes ✓, rgthree ✓,
  ModelAttentionBackend (comfy kitchen) ✓, subgraph 40bb7e22 (14 nodes: 2nd orbit pass,
  ImageCrop, ImageConcanate, SaveImage).

### P4 — "MiniMax H3 REF + Fizgig nodes as SOTA ref2img" (r/StableDiffusion 1wsb4h3)
- Memory (10-08): already listed.
- **Local match: `minimaxh sheet patreon.json`** — a **sprite-sheet-style single-frame sheet**:
  **FizgigH3StillLatent (4096×1536) + FizgigH3StillDecode** — TRUE single-frame stills from H3
  (crisp, no banding; pack `ComfyUI-Fizgig-H3-Still` INSTALLED ✓) — plus
  `MiniMaxH3ReferenceToVideo` (prompt: "[reference generation] static image of sprite sheet..."),
  `LoadImageListFromDir //Inspire` feeding a WHOLE FOLDER of refs (`D:\character sheet`),
  `easy cleanGpuUsed` ×3 (Easy-Use ✓), `ImageScaleToTotalPixels`, and a custom H3-attention
  subgraph (`H3SLAAttention`, `MiniMaxChunkFeedForward`, `MiniMaxLowVRAMAttention`,
  `MiniMaxH3SigmaShift` — served by installed H3-Optimizations / Spectrum / chunk-star7 packs).
- **Hero model:** `minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors`
  (weight dtype `fp8_e4m3fn`) — a **fused ref-delta turbo-8** single model (reference
  conditioning baked in — the "REF" of the title) ✗ MISSING.
- **CLIP:** GGUF `minimax\qwen3vl-32B-MiniMax-H3-Q2_K.gguf` via `CLIPLoaderGGUF`
  (ComfyUI-GGUF ✓) ✗ GGUF file MISSING.
- VAE `minimax_h3_video_vae_int8_convrot` ✓. Timing table in the file: 8 steps 4.4 min / 10 → 6 /
  16 → 7 / 25 → 12 (megapixel table).

### P5 — "Character sheet workflow Qwen 2.1" (r/comfyui 1wsee1y)
- Memory (10-08): "workflow already saved".
- **Local match: `LEEBLAAB-QwenImage21-Character-SHEET.json`** (author LEEBLAAB) — a SUBGRAPH
  pipeline: UNET `qwen_image_2.1_bf16` (or the author's `qwen_image_2.1_int8_convrot` variant) +
  CLIP `qwen3vl_8b_int8_convrot` + VAE `qwen_image_2.1_vae_bf16` →
  `TextEncodeQwenImage21` (sheet prompt + reference image = i2i) → `QwenImage21Cache` →
  KSampler (25 steps euler/simple, seed, schedulers "res_2m"/"beta") → VAEDecode →
  **VAEDeGrid 4× zoom** → `ImageStitch` → `ImageResizeKJv2` (nvidia_rtx_vsr → 1536) →
  `SaveImageAdvanced`.
- A MarkdownNote carries the **"Character Sheet Prompt Architect"** system prompt: input ONE
  reference image + entity name → output a 10-section sheet prompt (layout zones A–F, hero pose,
  turnaround, expression row, wardrobe, metadata column, style, lighting/palette, quality
  contract; every rendered string in English double quotes).
- Resolution presets: **1.0 MP fast / 3.4 MP balanced / 6.0 MP best** (default 6 MP, 16:9).
- **Models:** `qwen_image_2.1_bf16.safetensors` ✓ (13.3 GB), `qwen3vl_8b_int8_convrot` ✓
  (8.7 GB), `qwen_image_2.1_vae_bf16` ✓ (0.6 GB). The author's `qwen_image_2.1_int8_convrot`
  UNET variant ✗ missing → bf16 must be used.
- **CAUTION (tested 2026-10-18 ~17:12):** a headless run of this workflow with the bf16 UNET
  **crashed the ComfyUI server** (probably VRAM: 13.3 GB UNET + 8.7 GB CLIP + 1536 px + 4× zoom
  decode on the 32 GB 5090). If retried: lower the resolution (1–3.4 MP), free VRAM first, or
  obtain the int8_convrot variant. Also: the multi-angle turnaround format of this sheet was
  **rejected by the user** ("not the correct one") — do not run it without explicit confirmation.
- **Packs:** QwenImage21Cache / TextEncodeQwenImage21 / ModelAttentionBackend ✓, KJNodes
  (ImageResizeKJv2, SaveImageAdvanced, ResolutionSelector) ✓, DeGrid (VAEDeGrid) ✓.

## Local workflow ↔ post mapping

| Local file | Post | Route | Ready on this machine? |
|---|---|---|---|
| `2BZ_H3_character_sheet_2stage_v1_EN.json` | P3 | H3 orbit 2-stage (ref2va) + LLM-analyzed refs + action panels | Models 4/6 ✓; **toobusy ✗, pysssss ✗ packs missing** |
| `LocationOrbitSheetH3.json` | P2 | Krea2 t2i → H3 fl2va location orbit → contact sheet | 3 models ✗ (Krea2_Turbo_convrot_int8mixed, lightx2v turbo, ref_lora_rank_256); **OrbitSheets pack ✗**; needs a vision LLM for frame select |
| `minimaxh sheet patreon.json` | P4 | H3 Fizgig-still sprite sheet, fused ref-delta turbo8, folder of refs | 2 models ✗ (fused_refdelta, Q2_K GGUF CLIP); Fizgig + Easy-Use ✓ |
| `LEEBLAAB-QwenImage21-Character-SHEET.json` | P5 | Qwen 2.1 i2i design sheet (multi-angle) | All 3 models ✓; int8_convrot UNET variant ✗; **OOM risk on bf16** (crashed server); format rejected by user |
| (not local — HF download candidate) | P1 | H3 360° orbit sheet (PoopMan333) | ref2va ✓, video VAE int8 ✓, audio VAE ✓, turbo4step ✓; int8_convrot 32B CLIP ✗ (have nvfp4_awq equivalent — likely swappable); v4 turbo LoRA ✗; KJNodes + rgthree ✓ |

## What we HAVE (models, main tree `E:\ComfyUI_windows_portable\ComfyUI\models`)
- `minimax_h3_ref2va_pruned_int8_convrot.safetensors` (diffusion_models)
- `minimax_h3_fl2va_pruned_int8_convrot.safetensors` (diffusion_models)
- `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` (text_encoders)
- `minimax_h3_video_vae_fp16` + `minimax_h3_video_vae_int8_convrot` + `minimax_h3_audio_vae_fp32` (vae)
- `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` (loras)
- `qwen_image_2.1_bf16.safetensors` (13.3 GB, diffusion_models), `qwen3vl_8b_int8_convrot`
  (text_encoders), `qwen_image_2.1_vae_bf16` (vae)
- Krea2 line: `Krea2Realism_V1`, Krea2 V2 LoRA, `krea2_identity_edit` LoRA, `qwen3vl_4b_fp8_scaled`,
  `qwen_image_vae`
- Packs: KJNodes, rgthree-comfy, ComfyUI-Easy-Use, ComfyUI-GGUF, ComfyUI-Fizgig-H3-Still,
  ComfyUI-DeGrid, ComfyUI-H3-FaceRefine, H3-Optimizations, ComfyUI-Spectrum-MiniMax-H3,
  minimax-h3-chunk-star7, Minimax-H3-Latent-Continuation, ComfyUI-MiniMax-H3-Turbo,
  minimax-h3-semantic-bridge, ComfyUI-H3-Multishot, ComfyUI-H3-Project-Suite, …

## What is MISSING (with likely source)
| Item | Needed by | Likely source |
|---|---|---|
| `minimax_h3_t1_image_vae_step1597.safetensors` | P3/2BZ | author's repo / 2BZ's share |
| `gemma4_e4b_it_fp8_scaled.safetensors` (TextGenerate CLIP) | P3/2BZ | author's conversion (or swap in an installed local LLM route) |
| `Krea2_Turbo_convrot_int8mixed.safetensors` | P2 | author's Krea2 conversion |
| `minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy.safetensors` | P2 | HF (lightx2v lineage) |
| `minimax_h3_ref_lora_rank_256_bf16.safetensors` | P2 | author's ref LoRA |
| `minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors` | P4 | author's fused model (may be patreon-gated) |
| `minimax\qwen3vl-32B-MiniMax-H3-Q2_K.gguf` | P4 | author's GGUF conversion |
| `minimax_h3_turbo_v4_step600_ema.safetensors` | P1 (recommended turbo) | HF PoopMan333 repo / MiniMax |
| `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` | P1 (CLIP; nvfp4_awq equivalent exists — verify swap) | HF (convrot conversions) |
| `qwen_image_2.1_int8_convrot.safetensors` | P5 (author variant; bf16 works but OOM-risky) | author's conversion |
| Pack **toobusy** (neobabae ≥0.4.9) | P3/2BZ | ComfyUI Manager |
| Pack **pysssss** (ComfyUI-SSS-Nodes) | P3/2BZ | ComfyUI Manager |
| Pack **OrbitSheets** | P2 | author's repo (from the P2 post) |
| Pack **Inspire** (`LoadImageListFromDir //Inspire`) | P4 | ComfyUI Manager |

## Next steps (AWAITING USER CALL — nothing runs without confirmation)
1. **Refresh `REDDIT_SESSION_COOKIE`** (one-time) → fetch all 5 post bodies via
   `utilities\reddit_fetch.py` → fill in the actual post bodies + author model download links.
   (Alternative: retry `r.jina.ai` after **13:04 UTC / 18:34 IST** 2026-10-18.)
2. Pick the sheet route: P1 (PoopMan333 orbit — best model match, 2 small gaps), P4 (fused
   ref-delta + Fizgig still — 2 model downloads, single-frame sprite sheet, no orbit), P3
   (2-stage editor — 2 packs + 2 models), P2 (location orbit — 3 models + 1 pack), P5
   (Qwen 2.1 — models present but OOM risk + multi-angle format rejected by user).
3. Download missing models/packs, wire the LOCKED v6 sheets (`input\char1_sheet.png` /
   `char2_sheet.png`) as references, then run — with explicit user confirmation.
4. Bring the ComfyUI server back up (currently down) — also needs the user's go-ahead.
