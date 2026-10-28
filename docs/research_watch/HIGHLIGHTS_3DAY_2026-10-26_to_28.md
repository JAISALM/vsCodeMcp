# 3-Day Highlights — 2026-10-26 → 2026-10-28 (what RAG captured while we were away)

Compiled 2026-10-28 from `rag/news/` captures (Reddit via HTML tier, Civitai API,
HF trending). Only items that matter to **our** pipeline: H3 video / Krea2 sheets
/ charswapmask+SAM3 / audio (D041 no-music) / writer+agent LLMs / LoRA training /
ComfyUI adoption. Scores as captured on that day.

## Tier 1 — our pipeline directly (read first)

| # | Item (date, score) | Why it matters | URL |
|---|---|---|---|
| 1 | **"I 'hacked' Krea 2 to work with Pose Studio"** (10-27, 198u) | Krea2 + Pose Studio bridge for style diversity — exactly our reference-sheet chain (D021); the complaint is the same style-diversity problem we have | https://www.youtube.com/watch?v=6RQSVyMrRvs |
| 2 | **Gladas' Workflow for Krea 2 Turbo** (Civitai, 3,201 dl) | Ready-made Krea2 Turbo ComfyUI workflow — ADOPT candidate for reference-sheet speed | https://civitai.com/models/2807513 |
| 3 | **mini max character replace — with turbo LoRA, 4 steps** (Civitai, 2,577 dl) | H3 character-swap + 4-step turbo — our charswapmask pipeline + turbo speed | https://civitai.com/models/2843905 |
| 4 | **ReDetail 2.0: LTX-2.5 video refine + upscale to 4K (workflow + CLI)** (Civitai, 1,700 dl, u/bambushu) | LTX-2.5 refine/upscale — our VFX base model | https://civitai.com/models/2857731 |
| 5 | **MOSS-Image Vision Text Encode (ComfyUI node + workflow)** (10-27→28, 171u) | NEW ComfyUI node pack + workflow for MOSS's vision encoder — ADOPT candidate if we adopt MOSS | https://www.reddit.com/gallery/1xbjxcr |
| 6 | **My MOSS Character Lora Training Results** (10-27, 206u) + **"I finally nailed Moss char loras"** (140u) | Character-LoRA training recipes feeding tonight's LoRA plan | https://www.reddit.com/gallery/1xeunzs · https://www.reddit.com/r/StableDiffusion/comments/1xfu2d6/huge_shoutout_to_shootthesound_and_fizgig_i/ |
| 7 | **18-clip reel of my Minimax H3 LoRA on a 3090** (10-27, 137u) | H3 LoRA trained + used on a 24 GB card — proof of our LoRA plan at consumer scale | https://v.redd.it/oexsvwhx4cxh1 |
| 8 | **Flux 3 Klein in ComfyUI \| Generate, Edit & Combine** (10-27, 34u video) | Flux-3-Klein ComfyUI walkthrough — our Klein reference path | https://youtu.be/ntxxhO9H3bY |
| 9 | **Flux 3 Image is #1 model** (10-27, 177u) | Flux-3 adoption signal | https://www.reddit.com/r/StableDiffusion (search "Flux 3 Image is #1") |
| 10 | **Hy-Nomas (Tencent video world model) in ComfyUI on 12 GB** (10-27, 156u) | H3 alternative evaluation | https://v.redd.it/rlnpj9kgmaxh1 |

## Tier 2 — our infra (llama.cpp / GPU)

| # | Item (date, score) | Why it matters | URL |
|---|---|---|---|
| 11 | ⚠️ **PSA: llama.cpp CVE-2026-116096** (10-27, 127u) | OOB write in Pocket-TTS mmproj; fixed **b11796+** — our build **b11583** is below the line (low real risk: we don't use mmproj/Pocket-TTS). Update `D:\llama` at convenience | https://www.reddit.com/r/LocalLLaMA/comments/1xfizft/psa_llamacpp_cve2026116096/ |
| 12 | **GPU unlocks (FP32 accumulation): why Turing/Ampere/Ada but NOT Blackwell** (10-27→28, 240u) | Confirms our 5090 isn't in the unlockable set — closes the GPU-trick thread | https://www.reddit.com/r/LocalLLaMA/comments/1xgaapw/gpu_unlocks_fp32_accumulation_why_can_it_be/ |
| 13 | **Free 3090 speedup hack (15% PP / 5% TG)** (10-27, 236u) + **CMP170HX-inspired 2× prefill unlock** (178u) + power-limit notes (166u) | GPU speedup cluster — all pre-Blackwell; read once, then close | https://github.com/Zagitta/gpu-unlock · https://wccftech.com/nvidia-rtx-30-40-gpus-get-faster-in-ai-llms-with-new-unlock-tool-but-prices-surge-too/ |
| 14 | **Qwen3.8-27B SSD-streaming prefiller trick** (10-27, 199u) + **Lean-QwenFlash 125B on 16 GB via NVMe** (265u) | Our agent-model class (Qwen3.8-27B) — long-context on small VRAM | https://i.redd.it/soux8gtmjlwh1.png (reddit post) · https://v.redd.it/a5j13v147kxh1 |
| 15 | **Eagle-4 released** (10-27, 245u) | Speculative-decoding engine — writer/agent throughput option | https://github.com/eagle-hq/EAGLE-4 |
| 16 | **llama.cpp default server port 8080 → 9931** (10-26) | Check our writer/agent server configs for the port change | r/LocalLLaMA (10-26 capture) |

## Tier 3 — models to watch (writer/agent lineage + audio)

| # | Item (date, score) | Why it matters | URL |
|---|---|---|---|
| 17 | **Mysterious Qwen4 appearance by new GitHub accounts** (10-28, 223u) | Qwen4 signals intensifying — writer/agent lineage | https://www.reddit.com/r/LocalLLaMA/comments/1xdmt2o/mysterious_qwen4_appearance_by_new_github_accounts/ |
| 18 | **inclusionAI/Ling-3.1-flash-1019 (+ base weights)** (10-28, 219u) | Ant's fast-model family — writer-candidate | https://huggingface.co/inclusionAI/Ling-3.1-flash-1019 |
| 19 | **nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB** (10-27→28, 198u / HF 194) | 4 GB MoE — edge agent option | https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB |
| 20 | **ornith-ai/Ornith-1.5-122B (Qwen finetune)** (10-27, 222u) | New open 122B candidate | https://huggingface.co/ornith-ai/Ornith-1.5-122B |
| 21 | **IBM Granite Speech 5.0 2B** (10-27, 131u) | Small speech model → audio pipeline candidate (D041: verify speech-only, no music) | https://huggingface.co/ibm-granite/granite-speech-5.0-2b |
| 22 | **RecursiveSI/flint ("Recursive Flint" — the Qwen3.8-35B?)** (10-27, 241u) | New Qwen-class model | https://huggingface.co/RecursiveSI/flint |

## Tier 4 — ecosystem / security (quick notes)

| # | Item (date, score) | Note | URL |
|---|---|---|---|
| 23 | ⚠️ **PSA: fake GitHub projects — especially AI tools & ComfyUI custom nodes** (10-28, 148u) | Verify origins of node packs before `install_node` | r/LocalLLaMA (10-28 capture) |
| 24 | **NVIDIA/OpenShell — private runtime for autonomous AI agents** (10-28, 173u) | Agent-runtime context | https://github.com/NVIDIA/OpenShell |
| 25 | **35B MoE at 20.5 tok/s on an iPhone** (10-27, 176u) | Mobile-LLM context | https://v.redd.it/f1kj93lnktwh1 |
| 26 | **ZPix (local open-source app) adds lasso inpainting** (10-27, 153u) | Our charswapmask stays ComfyUI-native — note only | https://v.redd.it/kqrzsc0j4gxh1 |

## HF quick list (10-27 → 28 trending)

- **baidu/Unlimited-OCR-2** (256 likes) — https://huggingface.co/baidu/Unlimited-OCR-2
- **LiquidAI/LFM3-1.7B** (208 likes; + real-time video captioning w/ LFM3-VL-2B locally, 142u) — https://huggingface.co/LiquidAI/LFM3-1.7B
- **ccore/Qwen3.5-4B-3D-Coder** (181) — https://huggingface.co/ccore/Qwen3.5-4B-3D-Coder
- **KRAFTON/Raon-1-mini-preview** (218) — https://huggingface.co/KRAFTON/Raon-1-mini-preview
- **bones-studio/seed** dataset (350) — https://huggingface.co/bones-studio/seed

## Source status at compile time

- X: all 7 accounts login-walled (browser tier ran; **`X_AUTH_TOKEN`/`X_CT0` still
  not set — one-time env, same as `REDDIT_SESSION_COOKIE`**).
- r/comfyui_workflows: browser tier GATED 4 days running (no further tier exists
  for that sub).
- Reddit JSON API: 403 (IP wall) — HTML top-page tier carries 4/5 subs.
- Civitai: full, incl. author names (browser-tier resolved 48/48).
