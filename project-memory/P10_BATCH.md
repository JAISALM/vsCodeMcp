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
| 5 | **Motion2MixamoRig** — Blender helper: motion out of video (check thoroughly) | `github.com/MaxLiu22/Motion2MixamoRig` · tweet `x.com/MaxLiu09/status/2109530569566744620` | **DONE (2026-10-24 22:40)** — venv `E:\minimax_workflow\Motion2MixamoRig\.venv` (uv Py3.12) fully installed: torch **2.14.1+cu130 (cuda True)** + gvhmr[rtmpose] + `motion2mixamorig==0.1.8` editable. **`m2mr doctor` GREEN on all code paths** (numpy/cv2/torch/gvhmr/ffmpeg ok; only the 3 USER assets missing = expected). **MSVC workaround:** `cython-bbox` (gvhmr[preproc]) needs a C++ compiler (absent; sdist-only) → installed `gvhmr[rtmpose]` **without the preproc extra** + `--no-deps` editable install — doctor confirms nothing else is missing. User manual steps (all recorded): SMPLX_NEUTRAL.npz + Mixamo FBX + input video/still. |
| 6 | **Qwen3-TTS-12Hz-1.7B-CustomVoice** — audio pipeline; is it better than our Omnivoice? | HF `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | ANALYZED ✓ — **Qwen3-TTS** = 10 languages (zh/en/ja/ko/de/fr/ru/pt/es/it — **NO Malayalam**); CustomVoice = 9 premium stock timbres + NL style control; Base = 3 s rapid clone. **NOT the movie path** (D050 = user-dub + OpenVoice/RVC; IndicF5 stays ML-native). **RIVAL TO OMNIVOICE** = `OmniVoice` engine (600+ languages) inside TTS-Audio-Suite (already installed — see item 9). Weights queued (4.3 GB); `qwen-tts` venv install pending DNS. |
| 7 | **MiniMax H3 person remover LoRA** — have we covered it? | reddit `r/StableDiffusion/comments/1x0kokb` | **DONE (2026-10-24 21:30)** — **NOT covered before** (we had Akatz's swap v1.5, not the remover). `H3-Person-Remover-V1.safetensors` (147 MB) **downloaded ✓**; `h3-relay` pack **cloned ✓** (8 `H3Relay*` classes); `H3-Person-Removal_LOCAL.json` **built + validated** (only 8 H3Relay restart-gate errors remain; all 7 models local; `gpu:0`→`default` fixed). |
| 8 | **VNCCS PoseStudio QI2.1** — pose from given image (amazing per user) | reddit `r/StableDiffusion/comments/1wmg9e8` · HF `MIUProject/VNCCS_PoseStudio_QI2.1` | **DONE (2026-10-24 21:35)** — pack `AHEKOT/ComfyUI_VNCCS_Utils` v0.7.0 **cloned ✓** (`VNCCS_PoseStudio` = interactive 3D posing/lighting/camera node); 3 LoRAs (152 MB each) + QI2.1 base models (UNET 6.9 GB + CLIP 8.9 GB) **queued in resumable downloader**; reference workflow saved (`VNCCS_PoseStudio_QI2.1_REFERENCE.json` — graph = QI2.1 UNET + Qwen3-VL-8B CLIP + LoRA + PoseStudio node; 4 classes live ✓, only `VNCCS_PoseStudio` restart-gated). **Movie use: Jaisal/Zidhan character + pose image → posed Krea2-style reference frames.** |
| 9 | **ComfyUI_ChatterBox_SRT_Voice** — audio pipeline; RANK vs our pipeline | `github.com/diodiogod/ComfyUI_ChatterBox_SRT_Voice` | **DONE (2026-10-24 21:40) — RANKED** — v3.4.4 evolved into **TTS-Audio-Suite v5.9.2** (1,241 stars, active) = **ALREADY INSTALLED** in custom_nodes (16+ engines: **OmniVoice (600+ langs)**, **Qwen3-TTS**, RVC, F5-TTS, Higgs v3 (100+ langs), Fish S2 Pro, VibeVoice, IndexTTS2, CosyVoice3, DramaBox (SRT-aware durations), Step Audio EditX (14 emotions/32 styles), Granite ASR (diarization + word timestamps)). **Rank for our pipeline: #1 audio orchestration layer** — SRT-timing TTS node (line-accurate dubs, `smart_natural`, Adjusted_SRT output, segment caching) = the movie dubbing pipeline; character/narrator switching + language brackets + pause tags. See WORKFLOW_HISTORY item-9 section. |

## Download ledger (background jobs — resumable)

| File | Source | Job | Size target | Last seen | Status |
|---|---|---|---|---|---|
| `minimax_h3_fl2va_int8_convrot.safetensors` (diffusion_models) | Comfy-Org/MiniMax-H3 | pwsh-396 | **32,462 MB** (34,038,892,334 B — corrected from wrong ~19.5 GB estimate) | 9,090 MB stale partial | QUEUED (script resumes from partial) |
| `minimax_h3_ref2va_pruned_fp8_scaled.safetensors` (diffusion_models) | Comfy-Org/MiniMax-H3 | pwsh-396 | 19,987 MB (20,958,205,608 B) | **DONE ✓ (2026-10-25 01:0x)** (size 19,987 MB + header 1,082 tensors verified) | DONE |
| `minimax_h3_ref2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors` | lightx2v | — | 1865 MB | — | DONE ✓ |
| `minimax_h3_ref2v_turbo_8step_v1.1_768p_comfyui_bf16.safetensors` | lightx2v | — | 1865 MB | — | DONE ✓ |
| `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` (loras) | lightx2v/Minimax-h3-Turbo | pwsh-396 | 1865 MB | — | **DONE ✓ (2026-10-24 23:0x)** |
| `fasth3_omniref_qad_nvfp4_comfy.safetensors` (diffusion_models) | FastVideo/FastH3-OmniRef-NVFP4-QAD-Comfy | pwsh-396 | 13,135 MB (13,773,998,700 B) | **DONE ✓ (2026-10-24 22:54)** → P10-1 fully runnable | DONE |
| `fasth3_omniref_8step_pruned_int8_convrot.safetensors` (diffusion_models) | FastVideo/FastH3-Omni-Comfy | pwsh-396 | 22,213 MB (22,213,723,064 B) | **DONE ✓ (2026-10-25 00:25)** (reset at 79% → auto-resume) | DONE |
| `minimax_h3_character_swap_v1.1_ref2va_fro.safetensors` (loras) | Alissonerdx/Minimax-H3-ComfyUI | pwsh-353 | 76 MB | — | DONE ✓ (76 MB) |
| `minimax_h3_hyperflow_8step_v1.0.safetensors` (loras) | videorebirth/hyperflow | pwsh-396 | 2,665 MB (2,795,328,008 B) | — | DONE ✓ (2665 MB on disk) → **`H3_HyperFlow_Fast_LOCAL.json` RE-VALIDATED = 0 errors, runnable pre-restart** |
| `fasth3_4step_dense_datafree_adapter.safetensors` (`E:\minimax_workflow\sol_h3_weights`) | FastVideo/FastVideo-FastH3-4-step-Preview-v1-LoRA | pwsh-396 | 1,416 MB (1,485,626,152 B) | **DONE ✓ (2026-10-24 23:0x)** | DONE |
| `fast_h3_vae_noncausal_24l.safetensors` (vae — Sol-H3-VAE) | Efficient-Large-Model/Sol-H3-VAE | pwsh-396 | 6,171 MB (6,471,256,328 B) | **DONE ✓ (2026-10-24 23:0x)** | DONE |
| **Qwen3-TTS-12Hz-1.7B-CustomVoice** (11 files, 4.3 GB → `D:\models\ai-movie\models\qwen3-tts\...`) | Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice | re-run script | 3,833 MB + 650 MB + small | 0 | QUEUED (P10 item 6 — append to `hf_resumable_download.py` ✓ done; re-run script) |
| `h3_character_swap_v1.5.safetensors` (148 MB) · `sam3.1_multiplex_fp16.safetensors` (1.7 GB) | akatz / Comfy-Org | — | — | already local ✓ | DONE |
| **m2mr venv** (`E:\minimax_workflow\Motion2MixamoRig\.venv`, uv Py3.12 + torch cu130) | MaxLiu22/Motion2MixamoRig | pwsh-426/430 | ~3 GB torch | **DONE ✓** torch 2.14.1+cu130 (cuda True) + gvhmr[rtmpose] + editable 0.1.8; `m2mr doctor` green (code) — 3 user assets pending (SMPLX npz / Mixamo FBX / input) |
| `H3-Person-Remover-V1.safetensors` (loras, item 7) | akatz-ai/MiniMax-H3-Person-Remover-LoRA | — | 147 MB | — | DONE ✓ (147 MB on disk) |
| **VNCCS_QI2_PoseStudio V1 / V1.1 / V2** (loras `QI2.1\VNCCS\`, item 8) | MIUProject/VNCCS_PoseStudio_QI2.1 | pwsh-396 | 159,436,408 B × 2 + 159,436,400 B | 0 | QUEUED in `hf_resumable_download.py` |
| `qwen_image_2.1_int8_convrot.safetensors` (unet, item 8) | Comfy-Org/Qwen-Image-2.1 | pwsh-396 | 7,256,783,064 B | 0 | QUEUED |
| `qwen3vl_8b_int8_convrot.safetensors` (clip, item 8) | Comfy-Org/Qwen-Image-2.1 | pwsh-396 | 9,350,798,360 B | 0 | QUEUED |

**RESUME RECIPE (power-cut safe, single command):** `& "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "D:\models\vsCodeMcp\utilities\hf_resumable_download.py"`
— idempotent (skips complete files), Range-resumes partials, auto-retries with backoff (60 tries, 5→60 s), exact-byte targets verified against HF API.
2026-10-24 21:20 context: all 8 legacy downloads died on transient `WinError 10054` connection resets / DNS `os error 11001`
(flaky network window) → consolidated into the robust script above (pwsh-396 running; Qwen3-TTS appended = re-run when it finishes).

**Resume recipe (after power cut):** check each file size vs target (python os.path.getsize); re-run the same
download command — files are written in place; a complete file = size matches target (verify with HF API size).

## User post-restart checklist (growing — final version at loop end)

> User: "keep a file where i need to check/do after your loop is completed"

- [ ] **Restart ComfyUI once** — **20 packs** load (18 previous + `h3-relay` + `ComfyUI_VNCCS_Utils` from P10 items 7/8; `TTS-Audio-Suite` v5.9.2 was already installed).
- [ ] Run `k2f_*_oneclick.json` × 8 (Krea2 cinematic images — the 6-scene set).
- [ ] Run item-2 `minimaxH3BackgroundSwap_v21a_LOCAL.json` (all models local).
- [ ] Run item-3 `VRGDG_MiniMaxH3_2Pass_MusicVideo_LOCAL.json` (**D041 — your other content only**).
- [ ] Run item-4 `H3_Recast_LOCAL.json` (inputs pre-copied to `input\`).
- [ ] Run item-5 `MiniMax-H3-Character-Swap-Mask_LOCAL.json` (char1_sheet.png / char2_sheet.png).
- [ ] Run item-6 `withers_has_big_nattys_LOCAL.json` (audio branches OFF = D041-safe).
- [ ] **P10-1 `FastH3_Omni_R2V_LOCAL.json`** — fast omni R2V (8 steps, cfg 1, shifts 12/3). **UNET `fasth3_omniref_qad_nvfp4_comfy` COMPLETE (13,135 MB, 2026-10-24 22:54) — FULLY RUNNABLE.**
      5090 benchmark: 5 s @832×480 ≈ 10 s, 10 s @1344×768 ≈ 69 s.
- [ ] **P10-2 `CharSwap_v1.1_fro_LOCAL.json`** — Alissonerdx's new swap LoRA (v1.1 fro, improved likeness). Run the SAME
      clip as `MiniMax-H3-Character-Swap-Mask_LOCAL.json` (v1.5 Akatz) and compare likeness.
- [ ] **P10-3 `H3_HyperFlow_Fast_LOCAL.json`** — standard H3 + HyperFlow 8-step LoRA (works TODAY, no engine).
      **ALL MODELS NOW LOCAL — validated 0 errors, runnable pre-restart** (hyperflow LoRA landed 21:50).
      Reference-only: `sol_h3_t2v.json` / `sol_h3_Sol-H3-Studio.json` (need `SolH3Generate` node = the Sol engine = WSL2 route).
- [ ] **P10-4 `RTX_Post_VFX_LOCAL.json`** — post pipeline (SR 2× → FrameGen ×2 → TrueHDR HLG). SR-only works pre-restart;
      full chain after restart. For grainy outputs: quality=DENOISE_ULTRA (same-res).
- [ ] vLo: `D:\models\ai-movie\repos\vlo` → `run.bat` → `http://127.0.0.1:6332` (SAM-Audio feature blocked —
      Python 3.11 needed; retry command shown in-app).
- [ ] **P10-5 Motion2MixamoRig** — install DONE (venv + doctor green). YOUR STEPS: (1) register smpl-x.is.tue.mpg.de →
      `E:\minimax_workflow\Motion2MixamoRig\assets\body_models\smplx\SMPLX_NEUTRAL.npz`; (2) mixamo.com character (FBX Binary, T-pose,
      e.g. Y Bot) → `assets\mixamo\<Name>.fbx`; (3) one-person 5–20 s clip → `assets\video\`; then
      `E:\minimax_workflow\Motion2MixamoRig\.venv\Scripts\python.exe -m motion2mixamorig.cli doctor` → `... run --rig assets\mixamo\Y_Bot.fbx`
      (first run auto-downloads GVHMR ~5 GB). Output = `outputs\<stamp>\<source>\mixamo_character.glb` → Blender File→Import glTF 2.0
      (hide Icosphere + armature). **Movie use:** Jaisal/Zidhan performance video → 3D character animation.
- [ ] **P10-7 `H3-Person-Removal_LOCAL.json`** — Akatz's person remover: 24 fps source video (W/H divisible by 32, ~5 s shot)
      + **clean first frame** (person removed, same framing) into the green LoadImage + person description in the green CLIP text
      node ("man in gray shirt"). Needs `h3-relay` pack loaded (post-restart). All 7 models local.
      **Movie use:** clean Krea2 duplicate-character references (the duplication quirk) + remove extras from plates.
- [ ] **P10-8 VNCCS PoseStudio** — needs 3 LoRAs + QI2.1 UNET/CLIP (queued in `hf_resumable_download.py` — re-run when done)
      + `ComfyUI_VNCCS_Utils` loaded (post-restart). Reference: `VNCCS_PoseStudio_QI2.1_REFERENCE.json`.
      **Movie use:** char1/char2 sheet + pose image → posed reference frames for R2V anchors.
- [ ] **P10-9 TTS-Audio-Suite v5.9.2** (already installed — loads post-restart) — audio orchestration:
      SRT-timing TTS node (line-accurate dubs), OmniVoice (600+ langs — Malayalam candidate to A/B vs IndicF5),
      Qwen3-TTS engine (item 6 lands here), RVC, Higgs v3, Fish S2 Pro. Engines download weights on first use.
      **Reference workflows saved:** `TTS_Suite_TTS_SRT_REFERENCE.json` (SRT-timed TTS) · `TTS_Suite_ASR_SRT_Builder_REFERENCE.json`
      (dub audio → ASR → SRT builder = the movie dubbing pipeline) · `TTS_Suite_OmniVoice_REFERENCE.json`.
      **Qwen3-TTS engine path:** suite auto-downloads from HF into its preferred TTS path (extra_model_paths YAML) OR takes a
      `local:<ModelName>` prefix — our queued weights (`D:\models\ai-movie\models\qwen3-tts\Qwen3-TTS-12Hz-1.7B-CustomVoice`,
      11 files 4.3 GB in `hf_resumable_download.py`) can be pointed to via that YAML to skip the re-download.
- [ ] P10 items land here as built.

## Status log

- 2026-10-25 00:3x — **Downloads:** qad UNET DONE (22:54) → pruned_int8 UNET DONE (21,184 MB; 1 reset at 79% → auto-resume) →
      ref2va_fp8 DONE (19,987 MB, header 1,082 tensors verified) — P10-1 (FastH3 Omni) + item-7 remover chain fully local.
      fl2va_int8 resuming (9,090/32,462 MB). Then 16 queued files (VNCCS×3, QI2.1 UNET/CLIP, Qwen3-TTS×11).
- 2026-10-25 00:3x — **RAG (D194) built + verified + scheduled** (user directive): `rag/` package (chunk→MiniLM-CPU→FAISS→query),
      seed = 1,248 project chunks + 65 news items, task `VsCodeMcp-RagDaily` 08:00. ChromaDB→FAISS (bindings broken here),
      Ollama absent→sentence-transformers CPU.
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
- 2026-10-24 21:30 — **item 7 DONE (person remover)**: reddit 1x0kokb (r/StableDiffusion, 16d ago) = Akatz (the char-swap author)
      dropped `akatz-ai/MiniMax-H3-Person-Remover-LoRA` (2026-10-08, 2276 downloads). **NOT covered before** (we had his swap v1.5 only).
      `H3-Person-Remover-V1.safetensors` (147 MB) downloaded ✓; example workflow `H3-Person-Removal-Relay-V2.json` (114 KB) saved as
      `_REFERENCE`; **`h3-relay` pack cloned ✓** (github.com/akatz-ai/h3-relay — "steerable, resumable, bounded-memory H3 workflows";
      provides the 8 `H3Relay*` classes in `h3_relay/{toolkit,text_memory,window_review}.py`).
      **`H3-Person-Removal_LOCAL.json` built + validated** — all 7 model refs LOCAL (ref2va_pruned_int8_convrot UNET ✓,
      qwen3vl_32b_nvfp4_awq CLIP ✓ in text_encoders/, video+audio VAE ✓, SAM3.1 ✓, remover LoRA ✓); only 8 H3Relay restart-gate
      errors remain; `SelectCLIPDevice` `gpu:0`→`default` fixed (single-GPU box).
      **Usage:** 24 fps video (W/H %32, ~5 s shot) + clean first frame + person description → SAM3.1 green-mask relay windows.
      **Movie use:** remove Krea2-duplicated characters from references; clean background plates.
- 2026-10-24 21:35 — **item 8 DONE (VNCCS PoseStudio)**: HF `MIUProject/VNCCS_PoseStudio_QI2.1` (2026-09-21, 62 likes) = 3 LoRAs
      (152 MB each: V1/V1.1/V2) + workflow JSON `VNCCS_PoseStudio_QI2.1.json` (saved as `_REFERENCE`). Graph = **Qwen-Image-2.1 stack**
      (UNet `qwen_image_2.1_int8_convrot` 6.9 GB + CLIP `qwen3vl_8b_int8_convrot` 8.9 GB — both queued; VAE `qwen_image_2.1_vae_bf16`
      LOCAL ✓) + `LoraLoaderModelOnly QI2.1\VNCCS\...@1.0` + `VNCCS_PoseStudio` node (interactive 3D posing/body-shaping/camera/
      lighting/pose-library) + `QwenImage21Cache` + `TextEncodeQwenImage21` (prompt: "replace the pose of \<image 2\> with the pose of
      \<image 1\>…") + rgthree Image Comparer. **Live classes:** QwenImage21Cache ✓, TextEncodeQwenImage21 ✓, Image Comparer (rgthree) ✓,
      GetImageSize ✓ — only `VNCCS_PoseStudio` restart-gated → pack **`AHEKOT/ComfyUI_VNCCS_Utils` v0.7.0 cloned ✓** (10 nodes:
      Pose Studio + UniCanvas + 3D Factory; MIT). **Movie use:** char1/char2 sheet + pose image → posed Krea2-style reference frames.
      LoRAs + base models queued in `hf_resumable_download.py` (exact-byte targets).
- 2026-10-24 21:40 — **item 9 DONE (RANKED, ChatterBox SRT Voice)**: repo v3.4.4 (83 stars) **evolved into TTS-Audio-Suite v5.9.2**
      (`diodiogod/TTS-Audio-Suite`, 1,241 stars, pushed 2026-10-24) — **ALREADY INSTALLED** in custom_nodes (engines dir: omnivoice,
      qwen3_tts, rvc, f5tts, higgs_audio_v3, fish_audio_s2, index_tts, cosyvoice, dots_tts, dramabox, granite_asr, qwen3_asr,
      moss_tts, step_audio_editx, vibevoice_engine, video…). **RANK for our audio pipeline: #1 orchestration layer** —
      (1) **SRT-timing TTS node** (line-accurate dubs, `smart_natural`, `Adjusted_SRT` output, segment-level caching) = the movie
      dubbing→TTS→timing sync we lack; (2) **OmniVoice engine = 600+ languages** (user's "omnivoice" — NOT installed locally =
      engine weights download on first use; Malayalam candidate to A/B vs IndicF5); (3) **Qwen3-TTS engine = item 6 lands here**
      (no separate venv needed); (4) character/narrator switching, language brackets, pause tags, iterative VC, Audio Analyzer;
      (5) DramaBox = SRT-aware duration targeting; Step Audio EditX = 14-emotion/32-style second-pass; Granite ASR = diarization +
      word timestamps. **vs our stack:** complements (not replaces) OpenVoice (timbre swap audio→audio) + RVC (D050 movie VC) +
      IndicF5 (ML-native TTS). Installs via `install.py` (ComfyUI Manager runs it on restart — venv python 3.10.6 caveat: some engines
      may need the uv 3.12 venv route).
- 2026-10-24 22:40 — **item 5 DONE (Motion2MixamoRig install)**: clean re-run (pwsh-426/430) after killing the DNS-stuck pwsh-392:
      `uv pip install pip setuptools` into the uv venv → numpy → `chumpy==0.70 --no-build-isolation` ✓ → **torch 2.14.1+cu130
      (cuda True)** ✓ → `gvhmr[rtmpose]` + smplx/einops/timm/opencv/scikit-image ✓ → editable `--no-deps` (`motion2mixamorig==0.1.8`) ✓.
      **MSVC WORKAROUND:** first `uv pip install -e .` FAILED — `cython-bbox` (pulled by `gvhmr[preproc]`) is sdist-only + needs
      Microsoft C++ Build Tools (absent on this box; no wheels on PyPI) → skipped the `preproc` extra (`gvhmr[rtmpose]` + `--no-deps`
      editable). **`m2mr doctor` GREEN on all code paths** (numpy/cv2/torch/gvhmr/ffmpeg ok) — the preproc extra is NOT required by
      doctor or the run path. Doctor's 3 `[missing]` = the user's manual assets (SMPLX_NEUTRAL.npz · Mixamo FBX · input video/still) —
      expected. First `m2mr run` auto-downloads GVHMR ~5 GB into `weights/`.
      **Repo AGENTS.md fully read (thorough):** asset table (`assets\body_models\smplx\` · `assets\mixamo\` FBX Binary T-pose ·
      `assets\video\` ONE person · `assets\image\` optional · optional MANO), commands (`run --video/--image/--rig/--skeleton/
      --detect-hands --hand-smooth 0.08/--no-foot-lock` · `diagnose [--visualize] [--threshold-cm]`), outputs per run
      (`mixamo_character.glb` glTF 2.0 · `skeleton_motion.npz` 24 SMPL joints Y-up m + foot_contact · `mixamo_rotations.npz` quat wxyz ·
      `diagnostics.json` self-intersections + `.html` · 4 comparison videos), foot-lock default on + ground y=0, review pass
      (`m2mr-review-v1` amber lane → `<stem>_review.json` → new GLB in a new dir), Blender ext = thin UI launching EXTERNAL python
      (our venv = Advanced mode; panel = 3D Viewport N sidebar; hide Icosphere+armature after import; Floor Markers mesh; FPS match),
      C4D FBX rigs supported. REPOS.md row updated.
