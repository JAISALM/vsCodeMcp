# P11 Batch — 3-project setup (heretic + Body Double + opencast-studio)

Opened 2026-11-01 ~21:00. User handed three GitHub projects "check it on loop"
while watching the match; wrap-up target 9:30 AM, zidhan v2 training ~10:30.
P9/P10 batches still have pending items (character LoRAs) — this batch is P11,
lower priority than those.

## Items

### P11-1 · heretic — enhance the DSH brain (IN PROGRESS)
- **What**: `p-e-w/heretic` v2.0 — training-free LLM modification (ARA steering).
  Goal = modify the DSH brain (Qwen3.8-27B) so it refuses less / is less
  sycophantic / less slop-prone. Cloned `D:\models\ai-movie\repos\heretic` @0db5c31.
- **Model reality**: user asked "is there a better Qwen 27B?" → **NO** (researched
  2026-11-01): Qwen3.8-27B (released 2026-08-14, Apache-2.0, 27.78B, 262K native
  context, vision+audio+video, MTP head built-in) is the newest Qwen-27B class;
  no Qwen4-27B released yet; our GGUF (NVFP4-MTP-LOW, 14.8 GB) + config
  (draft-mtp n-max 4, no p-min gate) already matches the community 5090 sweet spot
  (sudoingX/qwen38-mtp) — 80 tok/s is near the ceiling for this model on this card.
  → heretic goes straight on the current brain's HF original.
- **HF original**: `Qwen/Qwen3.8-27B` — PUBLIC (no token), bf16, 18 shards,
  55.6 GB, arch `Qwen3_5ForConditionalGeneration` (model_type qwen3_5 — VLM).
  Downloading → `D:\models\qwen\hf_original\Qwen3.8-27B\` (job pwsh-21; script
  `session_tmp\download_qwen38_27b.py`, resume-safe).
- **Tooling**: venv `D:\models\ai-movie\repos\heretic\.venv` (uv, py3.12,
  heretic-llm 1.4.0, bitsandbytes 0.50.2 ✓ Windows wheels exist). torch needs
  CUDA wheels (default PyPI gave 2.14.1+cpu) — force-reinstall cu130 running
  (job pwsh-20). On the 5090, run with `quantization = bnb_4bit` (bf16 = 56 GB
  won't fit; 4-bit ≈ 15-16 GB).
- **VRAM rule (user-confirmed)**: brain (llama-server, ~17-20 GB) and heretic
  never run together — user stops the brain for the heretic run (D192: user runs
  the GPU job). Brain stop = close its window / taskkill llama-server.exe;
  DSH chat dies while stopped (documented, expected).
- **HOW TO SWAP THE BRAIN (user asked "can we just change the model in dsh like
  other models?" → YES, exactly like the others):**
  1. heretic output = HF safetensors dir (bf16, same size as input) — NOT GGUF.
  2. Convert: llama.cpp `convert_hf_to_gguf.py` (D:\llama toolchain) →
     `llama-quantize` with the SAME recipe family as today's
     `Qwen3.8-27B-NVFP4-MTP-LOW.gguf` (NVFP4 + MTP head must survive, or fall
     back to Q4_K_M/Q5_K_M and drop the `--spec-type draft-mtp` flags).
  3. Put the GGUF in `D:\models\qwen\`, edit the MODEL line in
     `start_qwen_8100.bat` (and `Qwen3.827BMTP.bat`), double-click the bat.
     DSH keeps talking to :8100 — session continues (memory files carry context).
     If llama-swap cutover (D207) is done first, edit `D:\tools\llama-swap\config.yaml`
     model entry instead. `mmproj-BF16.gguf` (vision, 888 MB) stays unchanged —
     heretic only touches language-model matrices.
  4. Rollback = old GGUF filename + re-run the same bat (or
     `rollback_qwen_direct.bat` for the swap-tool layer).
- **Run (USER, when back)**: from a GPU-free state (brain stopped, ComfyUI
  models freed), e.g. `heretic Qwen3.8-27B-heretic-bf16dir config.default.toml`
  (censorship removal) — README: 30-40 min class on 3090 for a 4B; 27B will be
  longer (est 1-2 h). Configs available: default (censorship), noslop, nosyco,
  nohumor, emotions. Recommended brain stack: default + noslop.
- **Open**: (a) torch cu130 verify (pwsh-20); (b) confirm heretic 2.0 supports
  the `qwen3_5` hybrid arch (test = the run itself — user's); (c) GGUF re-quant
  recipe (NVFP4-MTP-LOW reproduction) — check `D:\llama` for the converter used
  originally.

### P11-2 · Body Double — video character recasting (SET UP, TEST DEFERRED)
- **What**: `lucataco/open-source-higgsfield` = "Body Double": same take, new
  cast, on STOCK ComfyUI (core nodes only). SAM 3.1 track + follow-cam crops +
  FLUX 3 Klein anchor + per-81-frame SCAIL-2 (WanSCAILToVideo) replacement +
  paste-back. Cloned `D:\models\ai-movie\repos\open-source-higgsfield` @864c8de.
- **Done**: repo clone ✓ · runner venv `.venv` (uv py3.12, comfy-sdk 0.5.0,
  comfy-api-proxy, av) — `import bodydouble` OK ✓ · `WanSCAILToVideo` +
  WanVideoWrapper SCAIL embeds confirmed REGISTERED on running :8188 instance ✓.
  Already on our server: `sam3.1_multiplex_fp16` (checkpoints) ✓,
  `wan_2.1_vae.pth` ✓, `flux2-vae` ✓.
- **DEFERRED (user: "let's defer the download… tomorrow after seeing which
  models we are actively using")**: `scripts/models.tsv` = 12 files ~41 GB.
  ~30 GB non-gated (SCAIL-2 int8 16.7 GB, 2 SCAIL LoRAs, 2 lightx2v distill
  LoRAs, umt5_xxl_fp8 6.7 GB, clip_vision_h 1.3 GB, wan vae .safetensors 254 MB)
  → `D:\models\bodydouble\{ComfyUI-folder}\` via
  `session_tmp\download_bodydouble_models.py` (resume-safe; killed mid-run at
  user request — partial .part files resume on rerun). Then register
  `D:\models\bodydouble\*` in `extra_model_paths.yaml` + ComfyUI restart.
- **GATED** (needs user): `flux3-image-klein-int8-convrot.safetensors` (5.8 GB) +
  `qwen3vl_4b_int8_convrot.safetensors` (4.9 GB) from
  `black-forest-labs/flux-3-image-klein-comfy` — **URL for the user to accept
  the FLUX Kommunity license: https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy
  (click "Agree")** — then an HF token is still needed for gated downloads
  (acceptance alone doesn't unlock anonymous pulls).
- **VRAM caveat**: README ~50 GB VRAM per segment @1280×704 vs our 32 GB 5090 →
  low-res attempt (960×540 / 720×408) when testing. Test deferred by user.
- **Runner**: `bodydouble/runner.py` queues via comfy-sdk to a ComfyUI URL —
  USER runs it (D192).

### P11-3 · opencast-studio — character sheets / Krea2 OpenCast style (DONE — value extracted)
- **What**: `akatz-labs/opencast-studio` — React UI + Node API + GPU executor.
  Cloned `D:\models\ai-movie\repos\opencast-studio` @7fe6397. `npm ci` ✓,
  `npm run doctor` ✓ (node 25.6.1, ffmpeg/ffprobe/uv/git OK, RTX 5090 seen).
- **Windows limitation (verified by its own doctor)**: `automaticGpuSetup: false`
  on win32 — generation needs a LINUX x64 NVIDIA worker (local or SSH); UI/API
  run fine on Windows. User chose: **LoRA + workflow is enough — skip the app.**
- **Done (ready to use in normal ComfyUI)**:
  - `krea2_opencast_v1.safetensors` (228.6 MB, sha256 98f8b6d4…) →
    `E:\ComfyUI_windows_portable\ComfyUI\models\loras\` ✓ (auto-listed by server).
  - Author's canvas workflow → `user\default\workflows\opencast_portrait_krea2.json`
    (UI format v0.4, 15 nodes, core classes only) — **validate_workflow 0/0,
    converted 11, no partner nodes** — runs as-is: Krea2 Turbo (
    `krea2_turbo_fp8_scaled`) + `krea2_opencast_v1` @1.0 + 1024×1536, 8 steps,
    cfg 1, euler/simple, denoise 1, `ConditioningZeroOut` negative, no trigger
    word, no custom packs.
  - **USE FOR**: stylized character-design portraits for Jaisal/Zidhan
    (exaggerated-face OpenCast look) — feeds the movie character sheets.
- App UI (optional, skipped): `npm run build && npm start` → :8389.
  Its 3 FLUX3 files share the same gated BFL repo as P11-2.

## Deferred until tomorrow (user's words)
- Body Double model downloads (~30 GB) + extra_model_paths registration + restart.
- opencast FLUX3 files (with the P11-2 gated pair).
- "once the comfyui higgsfield challenge ends, we may get more useful workflow
  items" — re-evaluate Body Double scope then.

## Status board
| item | state |
|---|---|
| P11-1 heretic brain | venv done (CUDA torch installed) · **heretic 2.0 from repo installing** (PyPI only has 1.4.0 = old config style; repo configs are 2.0-style with ARA plugin) · 55.6 GB original downloading · **conversion path refined**: D:\llama = b11960 (current) but NO NVFP4 in its quantizer → heretic output → `llama.cpp-src/convert_hf_to_gguf.py` (source clone, running) → F16 → `llama-quantize.exe Q4_K_M/Q5_K_M` (MTP head: verify converter support, else drop spec flags) · RUN = user (brain stopped, bnb_4bit) |
| P11-2 Body Double | setup done · downloads DEFERRED · gated files need license+token · low-res test later |
| P11-3 opencast | DONE (LoRA + validated canvas workflow) · app skipped |

## 2026-11-01 ~21:55 (conversion CLI PRE-VALIDATED — run_brain.bat footer corrected)
`convert_hf_to_gguf.py --help` (current llama.cpp source): outtype choices are lowercase
`{f32,f16,bf16,q8_0,tq1_0,tq2_0,auto}` (no `-m`/single-file flag exists — splitting is
controlled by `--split-max-tensors/--split-max-size`). **`--mtp` flag present** (exports
the MTP/NextN head — REQUIRED so the brain's `--spec-type draft-mtp` survives; `--no-nextn`
disables it). Corrected recipe (also in run_brain.bat footer):
```
1. D:\models\ai-movie\repos\heretic\.venv\Scripts\python D:\llama\llama.cpp-src\convert_hf_to_gguf.py "D:\models\qwen\heretic_out\qwen38-27B-brain" --outtype bf16 --mtp
2. D:\llama\llama-quantize.exe <bf16.gguf> D:\models\qwen\Qwen3.8-27B-heretic-Q4_K_M.gguf Q4_K_M
```
Plus `--dry-run` exists — ONCE the Qwen download completes, run
`... --dry-run --outtype bf16 --mtp <dir>` to confirm the qwen3_5 arch + MTP export
plans cleanly BEFORE the real 55 GB conversion. mmproj stays the existing
`mmproj-BF16.gguf` (language-model-only modification; no `--mmproj` re-export needed).

## 2026-11-01 ~21:50 status (user back at 9:30 PM — tonight = ZIDHAN V2 TRAINING)
User corrected the timeline: 9:30 was PM, not AM. **Tonight's priority = zidhan v2 LoRA
training (launch verified ready — see CURRENT_TASK.md top entry).** This batch's GPU
work (heretic run) waits for a free-GPU window (after zidhan scan, ~morning/afternoon).
Only background activity left: Qwen 55.6 GB download (disk-only), heretic-2.0 repo
install, llama.cpp source clone. FLUX3: user to click Agree on
https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy then provide a token.
