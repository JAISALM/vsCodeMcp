# P10 BATCH — 9 items (2026-10-24, user directive)

**Process (user, verbatim intent):** thoroughly one-by-one loop engineering; each point verified thoroughly;
record changes/benefits/details + downloadable models; background downloads = MY responsibility (track + report
progress — resumable after power cut); **log what to do BEFORE acting, verify each, mark DONE only on verified
completion**; always set up ComfyUI workflows; ALL URLs/repos from chat → memory + md files.
**User has NOT restarted ComfyUI yet** — after my loop the user restarts (17 packs) + runs everything.

**Hard rules in force:** D192 (no agent-run ComfyUI — build/validate only) · D041 (NO music in OUR content) ·
D193 (item-7 style: film language only when user says so) · shared restart = the gate for new packs.

## Items

| # | Item | Source (ALL links from user) | Status |
|---|---|---|---|
| 1 | **FastH3-Omni** — new faster H3 for t2v + ref2v | HF `FastVideo/FastH3-Omni-Comfy` · tweet `x.com/BennyDaBall_OG/status/2113323686250106978` | **DONE** (2026-10-24 20:45 — see WORKFLOW_HISTORY) |
| 2 | **Character swap (Alissonerdx)** — COMPARE vs our existing swap workflows (items 4/5) | tweet `x.com/Alissonerdx/status/2111649216653148305` | **DONE** (2026-10-24 20:52 — see WORKFLOW_HISTORY) |
| 3 | **NVlabs Sana sol-engine** — faster MiniMax w/o quality loss (tricky to make work) | repo `github.com/NVlabs/Sana/tree/sol-engine` + `models/minimax_h3/Sol-H3-ComfyUI` · tweets `x.com/xieenze_jr/status/2111123049571324395` + `x.com/PixelAigc/status/2113186476322324913` | PENDING |
| 4 | **NVIDIA VFX nodes** — video upscale for post | `github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes` · blog `blog.comfy.org/p/nvidia-vfx-nodes-for-video-upscaling` | PENDING |
| 5 | **Motion2MixamoRig** — Blender helper: motion out of video (check thoroughly) | `github.com/MaxLiu22/Motion2MixamoRig` · tweet `x.com/MaxLiu09/status/2109530569566744620` | PENDING |
| 6 | **Qwen3-TTS-12Hz-1.7B-CustomVoice** — audio pipeline; is it better than our Omnivoice? | HF `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | PENDING |
| 7 | **MiniMax H3 person remover LoRA** — have we covered it? | reddit `r/StableDiffusion/comments/1x0kokb` | PENDING |
| 8 | **VNCCS PoseStudio QI2.1** — pose from given image (amazing per user) | reddit `r/StableDiffusion/comments/1wmg9e8` · HF `MIUProject/VNCCS_PoseStudio_QI2.1` | PENDING |
| 9 | **ComfyUI_ChatterBox_SRT_Voice** — audio pipeline; RANK vs our pipeline | `github.com/diodiogod/ComfyUI_ChatterBox_SRT_Voice` | PENDING |

## Download ledger (background jobs — resumable)

| File | Source | Job | Size target | Last seen | Status |
|---|---|---|---|---|---|
| `minimax_h3_fl2va_int8_convrot.safetensors` (diffusion_models) | Comfy-Org/MiniMax-H3 | pwsh-274 | ~19.5 GB | 4.2 GB (20:12) | RUNNING |
| `minimax_h3_ref2va_pruned_fp8_scaled.safetensors` (diffusion_models) | Comfy-Org/MiniMax-H3 | pwsh-297 | ~19.5 GB? | 1.9 GB (20:05) | RUNNING |
| `minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors` | lightx2v | pwsh-311 | 1865 MB | DONE ✓ 1865 MB | DONE |
| `minimax_h3_ref2v_turbo_8step_v1.1_768p_comfyui_bf16.safetensors` | lightx2v | pwsh-293 | 1865 MB | DONE ✓ | DONE |
| `fasth3_omniref_qad_nvfp4_comfy.safetensors` (diffusion_models) | FastVideo/FastH3-OmniRef-NVFP4-QAD-Comfy | pwsh-343 | 13135 MB | RUNNING (item-1 primary — 5090-optimal NVFP4 QAD) | RUNNING |
| `fasth3_omniref_8step_pruned_int8_convrot.safetensors` (diffusion_models) | FastVideo/FastH3-Omni-Comfy | pwsh-343 (after QAD) | 21184 MB | QUEUED (item-1 fallback) | QUEUED |
| `minimax_h3_character_swap_v1.1_ref2va_fro.safetensors` (loras) | Alissonerdx/Minimax-H3-ComfyUI | pwsh-353 | 76 MB | — | DONE ✓ (76 MB) |
| `h3_character_swap_v1.5.safetensors` (148 MB) · `sam3.1_multiplex_fp16.safetensors` (1.7 GB) | akatz / Comfy-Org | pwsh-293 | — | already local ✓ | DONE |

**Resume recipe (after power cut):** check each file size vs target (python os.path.getsize); re-run the same
download command — files are written in place; a complete file = size matches target (verify with HF API size).

## User post-restart checklist (growing — final version at loop end)

> User: "keep a file where i need to check/do after your loop is completed"

- [ ] **Restart ComfyUI once** — 17 packs load (10 previous + 7 from item-6: h3_clown_anchoring,
      comfyui-load-audio-batch-from-dir, ComfyUI-TranscriptionTools, ComfyUI_Fill-ChatterBox, comfy-image-saver,
      ComfyUI-Animation_Nodes_and_Workflows, ComfyUI-JNodes) + any new P10 packs (listed as they land).
- [ ] Run `k2f_*_oneclick.json` × 8 (Krea2 cinematic images — the 6-scene set).
- [ ] Run item-2 `minimaxH3BackgroundSwap_v21a_LOCAL.json` (all models local).
- [ ] Run item-3 `VRGDG_MiniMaxH3_2Pass_MusicVideo_LOCAL.json` (**D041 — your other content only**).
- [ ] Run item-4 `H3_Recast_LOCAL.json` (inputs pre-copied to `input\`).
- [ ] Run item-5 `MiniMax-H3-Character-Swap-Mask_LOCAL.json` (char1_sheet.png / char2_sheet.png).
- [ ] Run item-6 `withers_has_big_nattys_LOCAL.json` (audio branches OFF = D041-safe).
- [ ] **P10-1 `FastH3_Omni_R2V_LOCAL.json`** — fast omni R2V (8 steps, cfg 1, shifts 12/3); UNET `fasth3_omniref_qad_nvfp4_comfy`
      must be fully downloaded first (pwsh-343). 5090 benchmark: 5 s @832×480 ≈ 10 s, 10 s @1344×768 ≈ 69 s.
- [ ] **P10-2 `CharSwap_v1.1_fro_LOCAL.json`** — Alissonerdx's new swap LoRA (v1.1 fro, improved likeness). Run the SAME
      clip as `MiniMax-H3-Character-Swap-Mask_LOCAL.json` (v1.5 Akatz) and compare likeness.
- [ ] vLo: `D:\models\ai-movie\repos\vlo` → `run.bat` → `http://127.0.0.1:6332` (SAM-Audio feature blocked —
      Python 3.11 needed; retry command shown in-app).
- [ ] P10 items land here as built.

## Status log

- 2026-10-24 20:34 — P10 batch received (9 items); tracker created; goal armed (goal-0e826188).
- 2026-10-24 20:45 — **item 1 DONE**: FastH3-Omni analyzed (README + variant repos + 5090 benchmark tweet);
      NVFP4 QAD (13 GB, 5090-optimal) + int8 fallback (21 GB) downloading (pwsh-343, resumable Range);
      `FastH3_Omni_R2V_LOCAL.json` built from validated item-5 graph (swap LoRA + SAM3 removed; chain
      UNET→SigmaShift[12,3]→Attention→Guider/Scheduler; omni prompt w/ D041 ambient-only audio) — **validate CLEAN** ✓.
- 2026-10-24 20:52 — **item 2 DONE**: Alissonerdx tweet 2111649216653148305 = char-swap LoRA **v1.0 → v1.1 update**
      ("improve likeness … almost v2.0, but for that I'd want multiple characters"). Release = `minimax_h3_character_swap_v1.1_ref2va_fro`
      (76 MB, `Alissonerdx/Minimax-H3-ComfyUI/loras`, repo updated same day 2026-10-18). **Downloaded ✓.**
      `CharSwap_v1.1_fro_LOCAL.json` built from item-5 graph (only swap LoRA slot 1 changed; turbo @0.85 kept;
      SAM3 mask chain intact) — **validate CLEAN** ✓. Swap-LoRA comparison table recorded (v1.1_fro vs Akatz v1.5 vs v1.0 r64_gl).
