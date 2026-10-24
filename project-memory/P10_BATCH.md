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
| 3 | **NVlabs Sana sol-engine** — faster MiniMax w/o quality loss (tricky to make work) | repo `github.com/NVlabs/Sana/tree/sol-engine` + `models/minimax_h3/Sol-H3-ComfyUI` · tweets `x.com/xieenze_jr/status/2111123049571324395` + `x.com/PixelAigc/status/2113186476322324913` | **DONE** (2026-10-24 21:00 — see WORKFLOW_HISTORY) |
| 4 | **NVIDIA VFX nodes** — video upscale for post | `github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes` · blog `blog.comfy.org/p/nvidia-vfx-nodes-for-video-upscaling` | **DONE** (2026-10-24 21:10 — see WORKFLOW_HISTORY) |
| 5 | **Motion2MixamoRig** — Blender helper: motion out of video (check thoroughly) | `github.com/MaxLiu22/Motion2MixamoRig` · tweet `x.com/MaxLiu09/status/2109530569566744620` | IN PROGRESS (install pwsh-392) |
| 6 | **Qwen3-TTS-12Hz-1.7B-CustomVoice** — audio pipeline; is it better than our Omnivoice? | HF `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | ANALYZED ✓ — verdict: **NO for the ML movie** (no Malayalam in its 10-language set; movie = user-dub + OpenVoice/RVC per D050). **YES as EN TTS option** (instruction-controlled emotion, 97 ms streaming, 1.7B = fits our GPU). "omnivoice" = **OpenVoice** (our timbre-swap). Weights queued (4.3 GB); `qwen-tts` venv install pending DNS recovery. |
| 7 | **MiniMax H3 person remover LoRA** — have we covered it? | reddit `r/StableDiffusion/comments/1x0kokb` | PENDING |
| 8 | **VNCCS PoseStudio QI2.1** — pose from given image (amazing per user) | reddit `r/StableDiffusion/comments/1wmg9e8` · HF `MIUProject/VNCCS_PoseStudio_QI2.1` | PENDING |
| 9 | **ComfyUI_ChatterBox_SRT_Voice** — audio pipeline; RANK vs our pipeline | `github.com/diodiogod/ComfyUI_ChatterBox_SRT_Voice` | PENDING |

## Download ledger (background jobs — resumable)

| File | Source | Job | Size target | Last seen | Status |
|---|---|---|---|---|---|
| `minimax_h3_fl2va_int8_convrot.safetensors` (diffusion_models) | Comfy-Org/MiniMax-H3 | pwsh-396 | **32,462 MB** (34,038,892,334 B — corrected from wrong ~19.5 GB estimate) | 0 (wb-reset by failed pwsh-274) | RUNNING (resume+retry) |
| `minimax_h3_ref2va_pruned_fp8_scaled.safetensors` (diffusion_models) | Comfy-Org/MiniMax-H3 | pwsh-396 | 19,987 MB (20,958,205,608 B) | 0 (wb-reset by failed pwsh-297) | RUNNING (resume+retry) |
| `minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors` | lightx2v | — | 1865 MB | — | DONE ✓ |
| `minimax_h3_ref2v_turbo_8step_v1.1_768p_comfyui_bf16.safetensors` | lightx2v | — | 1865 MB | — | DONE ✓ |
| `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` (loras) | lightx2v/Minimax-h3-Turbo | pwsh-396 | 1865 MB | 0 (DNS fail pwsh-274) | RUNNING (resume+retry) |
| `fasth3_omniref_qad_nvfp4_comfy.safetensors` (diffusion_models) | FastVideo/FastH3-OmniRef-NVFP4-QAD-Comfy | pwsh-396 | 13,135 MB (13,773,998,700 B) | ~1,911 MB partial (pwsh-343 reset) | RUNNING (resume from partial) |
| `fasth3_omniref_8step_pruned_int8_convrot.safetensors` (diffusion_models) | FastVideo/FastH3-Omni-Comfy | pwsh-396 | 22,213 MB (22,213,723,064 B) | 0 | QUEUED after QAD (same job) |
| `minimax_h3_character_swap_v1.1_ref2va_fro.safetensors` (loras) | Alissonerdx/Minimax-H3-ComfyUI | pwsh-353 | 76 MB | — | DONE ✓ (76 MB) |
| `minimax_h3_hyperflow_8step_v1.0.safetensors` (loras) | videorebirth/hyperflow | pwsh-396 | 2,665 MB (2,795,328,008 B) | partial (pwsh-360 reset) | RUNNING (resume) |
| `fasth3_4step_dense_datafree_adapter.safetensors` (`E:\minimax_workflow\sol_h3_weights`) | FastVideo/FastVideo-FastH3-4-step-Preview-v1-LoRA | pwsh-396 | 1,416 MB (1,485,626,152 B) | 0 | QUEUED (Sol/FastVideo runtime — PEFT adapter, not a ComfyUI LoRA) |
| `fast_h3_vae_noncausal_24l.safetensors` (vae — Sol-H3-VAE) | Efficient-Large-Model/Sol-H3-VAE | pwsh-396 | 6,171 MB (6,471,256,328 B) | 0 | QUEUED (optional fast decoder, ~10 s/clip saved) |
| **Qwen3-TTS-12Hz-1.7B-CustomVoice** (11 files, 4.3 GB → `D:\models\ai-movie\models\qwen3-tts\...`) | Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice | re-run script | 3,833 MB + 650 MB + small | 0 | QUEUED (P10 item 6 — append to `hf_resumable_download.py` ✓ done; re-run script) |
| `h3_character_swap_v1.5.safetensors` (148 MB) · `sam3.1_multiplex_fp16.safetensors` (1.7 GB) | akatz / Comfy-Org | — | — | already local ✓ | DONE |
| **m2mr venv** (`E:\minimax_workflow\Motion2MixamoRig\.venv`, uv Py3.12 + torch cu130) | MaxLiu22/Motion2MixamoRig | pwsh-392 | ~3 GB torch | blocked (DNS flake os error 11001) | RUNNING (uv auto-retry; chumpy needs `setuptools` in venv first — `uv pip install setuptools` then `--no-build-isolation chumpy==0.70`) |

**RESUME RECIPE (power-cut safe, single command):** `& "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "D:\models\vsCodeMcp\utilities\hf_resumable_download.py"`
— idempotent (skips complete files), Range-resumes partials, auto-retries with backoff (60 tries, 5→60 s), exact-byte targets verified against HF API.
2026-10-24 21:20 context: all 8 legacy downloads died on transient `WinError 10054` connection resets / DNS `os error 11001`
(flaky network window) → consolidated into the robust script above (pwsh-396 running; Qwen3-TTS appended = re-run when it finishes).

**Resume recipe (after power cut):** check each file size vs target (python os.path.getsize); re-run the same
download command — files are written in place; a complete file = size matches target (verify with HF API size).

## User post-restart checklist (growing — final version at loop end)

> User: "keep a file where i need to check/do after your loop is completed"

- [ ] **Restart ComfyUI once** — 18 packs load (10 previous + 7 item-6 + 1 item-4 VFX) + any new P10 packs (listed as they land).
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
- [ ] **P10-3 `H3_HyperFlow_Fast_LOCAL.json`** — standard H3 + HyperFlow 8-step LoRA (works TODAY, no engine).
      Requires `minimax_h3_hyperflow_8step_v1.0.safetensors` download complete (pwsh-360).
      Reference-only: `sol_h3_t2v.json` / `sol_h3_Sol-H3-Studio.json` (need `SolH3Generate` node = the Sol engine = WSL2 route).
- [ ] **P10-4 `RTX_Post_VFX_LOCAL.json`** — post pipeline (SR 2× → FrameGen ×2 → TrueHDR HLG). SR-only works pre-restart;
      full chain after restart. For grainy outputs: quality=DENOISE_ULTRA (same-res).
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
- 2026-10-24 21:00 — **item 3 DONE (analysis + usable part)**: Sana `sol-engine` branch cloned to `E:\minimax_workflow\NVlabs-Sana-sol-engine`.
      **5090 benchmarks (Sana README, 5 s @1344×768 w/ audio):** H3 50-step = 989 s → HyperFlow 8-step BF16 = 193.6 s →
      **Sol-H3 one-stage = 67.2 s → two-stage (H3 draft + LTX refine) = 35.5 s (27.9×)**; 480p one-stage = 22 s.
      **⚠ Full Sol engine = LINUX-only** (Py3.12 + PyTorch 2.12 CUDA13 + Triton 3.7 + FastVideo + SM120-built FlashAttn4/SageAttn2.2
      + **≥90 GB host RAM — we have 64 GB**) → on this Windows box = **WSL2 route** (author's own FastH3 tweet ran WSL2 on 5090).
      ComfyUI integration = `Sol-H3-ComfyUI` pack (symlink into custom_nodes) + **`SolH3Generate` single node** + separate worker process
      + "Sol-H3 Studio" UI overlay. Example workflows copied (`sol_h3_t2v.json`, `sol_h3_Sol-H3-Studio.json` — reference only).
      **USABLE TODAY:** HyperFlow 8-step LoRA in the standard H3 graph → `H3_HyperFlow_Fast_LOCAL.json` (pruned int8 convrot UNET +
      hyperflow @1.0, 8 steps) — validate: 1 expected error = hyperflow LoRA still downloading (pwsh-360: hyperflow 2.7 GB +
      fasth3 4-step PEFT adapter 1.4 GB + Sol-H3-VAE 6.2 GB). Tweets ✓ (xieenze_jr: 35.5 s 5090; PixelAigc zh: 11× / 1.65 s = 8-GPU B300 numbers).
- 2026-10-24 21:10 — **item 4 DONE**: `Comfy-Org/ComfyUI_Nvidia_VFX_Nodes` (formerly "Nvidia RTX Nodes") — 3 nodes:
      `RTXVideoSuperResolution` (image/upscaling: 1–4× or target dims up to 8192, 19 quality modes incl. same-res DENOISE_*/DEBLUR_*,
      10-bit RGB10A2 option), `RTXVideoFrameGeneration` (2×–16× multiplier or specific timestep, auto shot-change detection, LOW/MED/HIGH),
      `RTXTrueHDR` (SDR→BT.2020 HLG/PQ; contrast/saturation/middle_gray/luminance 400–2000 nits; DL-Debander on by default).
      **Torch 2.12.0+cu130 = exact requirement match ✓.** Binding = `nvidia-vfx` PyPI stub → real wheel from **pypi.nvidia.com**
      (`pip install nvidia-vfx --index-url https://pypi.nvidia.com` EXIT 0 ✓; **import name = `nvvfx`**, NOT `nvidia_vfx`).
      **GOTCHA:** superseded old pack `comfyui_nvidia_rtx_nodes` (SR-class-only) was ALREADY installed and loaded (that's why SR was
      live but FrameGen/TrueHDR missing) → renamed to `comfyui_nvidia_rtx_nodes.superseded_bak` (reversible). New pack cloned into
      custom_nodes (all 3 classes + example_workflows). `RTX_Post_VFX_LOCAL.json` built = VHS_LoadVideo → SR(2× ULTRA) →
      FrameGen(×2 MEDIUM, 24→48 fps slow-mo) → TrueHDR(HLG 1000 nits) → VHS_VideoCombine(48 fps) — **validate: 2 restart-gate
      errors** (FrameGen/TrueHDR not in live registry; SR already live → SR-only variant usable pre-restart).
      Blog extras: EXR 16/32-bit write (Save Advanced) + EXR load improvements. **Restart gate now = 18 packs.**
- 2026-10-24 21:15 — **item 5 (Motion2MixamoRig) thorough check**: repo cloned (`E:\minimax_workflow\Motion2MixamoRig`), v0.1.8.
      **Releases = macOS-only zips** (v0.1.6–0.1.8) → Windows = **CLI route**: uv Python 3.12 venv + numpy → chumpy (--no-build-isolation,
      needs setuptools in venv) → torch cu130 → `uv pip install -e .` (pwsh-392, blocked on DNS flake). **`m2mr doctor` = self-check.**
      Manual steps for user: (1) SMPL-X register (smpl-x.is.tue.mpg.de) → `SMPLX_NEUTRAL.npz` → `assets\body_models\smplx\`;
      (2) Mixamo character (mixamo.com, FBX Binary + T-pose); (3) optional MANO (`MANO_RIGHT.pkl` from mano.is.tue.mpg.de) for `--detect-hands`.
      First `m2mr run` auto-downloads GVHMR ~5 GB into `weights/` (+HaMeR ~2.7 GB optional). **Blender 5.2 on disk ✓** (ext needs 4.2+;
      ext zip mac-only → build from source if wanted; CLI is the primary path). Input rules: exactly ONE person head-to-toe in frame
      the whole clip, steady camera, 5–20 s clips first; output = animated `.glb` + preview, feet planted on floor + floor markers.
      **Movie relevance:** H3 clip / reference performance video → Jaisal/Zidhan 3D character animation (Blender/Unity).
- 2026-10-24 21:20 — **item 6 ANALYZED (Qwen3-TTS-12Hz-1.7B-CustomVoice vs "omnivoice" = OpenVoice):**
      Qwen3-TTS = 10 languages (zh/en/ja/ko/de/fr/ru/pt/es/it — **NO MALAYALAM**); CustomVoice variant = 9 premium stock timbres +
      natural-language style control (emotion/prosody/speed); arbitrary cloning = the **Base** variant (3 s rapid clone); 97 ms streaming
      latency; 1.7B params; `pip install qwen-tts` (Py3.12). **Verdict: NOT the movie path** (D050 = user-dub + OpenVoice timbre swap +
      RVC; Malayalam dub text can't go through Qwen3-TTS's 10-language set; IndicF5 stays ML-native TTS). **For EN content (future kids
      videos/narration): strong candidate** — instruction-controlled emotion beats Fish S2 Pro's tag approach; 1.7B fits the 5090.
      Weights queued in `hf_resumable_download.py` (11 files, 4.3 GB → `D:\models\ai-movie\models\qwen3-tts\`); venv install pending DNS.
- 2026-10-24 21:25 — **download consolidation**: all 8 legacy downloads died on transient `WinError 10054` resets + DNS `os error 11001`
      (flaky network window) → consolidated into **`D:\models\vsCodeMcp\utilities\hf_resumable_download.py`** (pwsh-396 running):
      Range-resume partials (qad_nvfp4 at ~1.9 GB kept), auto-retry with backoff (60 tries), exact-byte targets (HF API).
      **Power-cut recipe = re-run that one script** (idempotent). Corrected sizes: fl2va_int8 = 32,462 MB (NOT ~19.5 GB),
      ref2va_fp8 = 19,987 MB. Qwen3-TTS (11 files) appended = re-run script when pwsh-396 finishes.
