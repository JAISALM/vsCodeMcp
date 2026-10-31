# Daily RAG watch — rolling file (D201/D202)

One `## <date>` block appended per daily 09:00 IST run (reminder
`schedule-6479d179`). Format per block: **new relevant items** (what it is +
how it helps us) → **action items** → **source failures** (honest, one line
each). Mondays also get the full extended weekly report
(`docs/research_watch/<date>_weekly.md`).

**URL RULE (2026-10-30, user directive):** every relevant item line carries
its **source URL** (reddit / X / civitai / HF) — taken from the `url:`
frontmatter field of the `rag/news/<date>/<source>_*.md` files (100% present;
the X tier, when it works, stores tweet URLs the same way). Angle-bracket
form `<https://…>` so it survives markdown line-wrapping. Applies to all
future blocks (10-29 and 10-30 were retro-fitted 2026-10-30).

## 2026-10-31

**Sources:** Reddit ✅ HTML tier (LocalLLaMA 1 new/47, ComfyUI 0 new/25, artificial 0 new/50 —
all 403-JSON walled as usual; **comfyui_workflows GATED 7th day** — redlib.perennialte.ch
now also dead (410), catsarch parses no posts) · HF ✅ 12 trending + 1 downloads + 8
datasets · Civitai ✅ 85 items, **0 new** in all four categories (deduped vs store) · X ❌
login-walled (7 accounts, 429, browser tier ran, no `X_AUTH_TOKEN`/`X_CT0`).
**Pipeline note:** 08:00 schtask got KILLED at start (LastTaskResult 0xC000013A Ctrl-C;
log = header only) → 09:05 manual `daily.py --news-only` re-run completed idempotently:
1150 items, **100 newly indexed**, store 1318.

**New relevant items (vs 10-30 baseline):**
- **Pika-Labs published Pika-H3-Flex on HF (198 likes)** — the model our kitchen pipeline
  runs, now with the OFFICIAL package: **6-step generation**, FL2VA + Ref2VA adapters
  (FP32 LoRA rank/alpha 128 on MiniMax-H3 base), native 480p/768p all 11 aspect ratios,
  up to 12 ref files (9 img + 3 vid + 3 audio), 24 fps, 32 kHz stereo audio, 5–15 s;
  **ComfyUI supported — `comfy/loras/` ships BF16 LoRA weights + R2V/FL2VA/T2V workflows** —
  <https://huggingface.co/Pika-Labs/Pika-H3-Flex>
- **Open-H3-Regenerate-2K landed in ComfyUI** (yesterday's 168u NVIDIA announcement →
  today's ComfyUI port: refinement nodes + noise controls + comparisons) —
  <https://v.redd.it/li33sky01lyh1> (+ SD thread <https://www.reddit.com/r/StableDiffusion/comments/1xhwa8d/openh3regenerate2k/>)
- **Krea2 BBOX models finished training + released (239u)** — carried watch item RESOLVED
  — <https://www.reddit.com/gallery/1xh6gar>
- **LTX 2.5 open-source "film studio" on an 8 GB card** (#OpenSourceHiggsfield: cast,
  script, render seamless LTX 2.5 takes) — relevant to the pending LTX-2.5 A/B test —
  <https://v.redd.it/5y9xqdkjohyh1>
- **SameFace — new ComfyUI node pack (42u)** — "measures it and moves it back" = face
  consistency tooling — <https://v.redd.it/a2qrlrkjziyh1>
- **kaitchup Qwen3.8-27B-SLQ GGUF "statistically lossless" (192u)** — SLQ quants
  EAR98 Q5_K_S 18.5 GB / EAR98.5 Q5_K_M 20.3 GB / EAR99 Q6_K 23.3 GB (MTP tensors
  retained, MTP disabled in eval) — candidate A/B for our Qwen3.8-27B brain —
  <https://huggingface.co/kaitchup/Qwen3.8-27B-SLQ-GGUF>
- **PSA: llama.cpp CVE-2026-116096 (132u)** — we run b11960 → check affected component +
  patched build — <https://www.reddit.com/r/LocalLLaMA/comments/1xfizft/psa_llamacpp_cve2026116096/>
- **Kokoro voice clone in ~600 MB VRAM (234u)** — narration voice option for the film
  (audio stays ambient-only per D041; cloning ≠ music) — <https://v.redd.it/2yxkwfdpsfyh1>
- **Gemma-4-31B-Humanlike-Chat (266u)** — "2.0's improved human voice on official Gemma 4
  31B" — writer-model candidate (our writer is Gemma4-31B) —
  <https://www.reddit.com/gallery/1xjdjy0>
- **Krea2 1500+ style ComfyUI wildcard node (122u)** — <https://www.reddit.com/gallery/1xit315>
- **HF new:** **Clover-35B-A3B-Preview** (176 likes — 35B MoE, 3B active — 32 GB candidate
  note) <https://huggingface.co/Diffuspace/Clover-35B-A3B-Preview> · **LFM3-Audio-2B**
  (154 — audio variant of the tracked LFM3 family)
  <https://huggingface.co/LiquidAI/LFM3-Audio-2B> · **LFM3-1.7B** (487 likes)
  <https://huggingface.co/LiquidAI/LFM3-1.7B> · **Nemotron-3.5-Transcribe-30B-A4B**
  (417 — local transcription) <https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B>
  · **Ling-3.1-flash-1019** (inclusionAI) <https://huggingface.co/inclusionAI/Ling-3.1-flash-1019>
  · **baidu/Unlimited-OCR-2** (400) <https://huggingface.co/baidu/Unlimited-OCR-2>
- **DeepSeek-V4.1-Flash-1017 cluster** (carried candidate): **41 tok/s on one 3090** via
  musicurgy delta-inference-engine (170u) <https://github.com/musicurgy/delta-inference-engine>
  · Unsloth Dynamic v3.1 GGUF release (335u) <https://i.redd.it/v9q24jegzlyh1.png>
- **Qwen-family chatter:** Qwen4 expectations (163u)
  <https://www.reddit.com/r/LocalLLaMA/comments/1xfrti9/qwen4_expectations/> · Qwen4-27B
  "4-way HC shift" (156u) <https://www.reddit.com/r/LocalLLaMA/comments/1xftcj0/qwen427bs_4way_hc_shift/>
  · Qwen27b vs GPT 6 (196u) <https://i.redd.it/a3awgopisnyh1.png> · "Qwen 3.8 flash next
  rooted an LG TV of spyware/adware" (192u — our family)
  <https://www.reddit.com/r/LocalLLaMA/comments/1xhoeo3/used_qwen_38_flash_next_on_underspeced_pc_to_root/>
- **GPU-market cluster (5090 supply):** not accepting orders from board partners, backorders
  unavailable (192u)
  <https://videocardz.com/newz/nvidia-reportedly-not-accepting-rtx-5090-orders-from-board-partners-even-backorders-are-unavailable>
  · discontinued 5090s → Chinese-lab die-ripping (449u)
  <https://wccftech.com/the-discontinued-rtx-5090s-are-entering-chinese-labs-where-they-are-turned-into-ai-gpus/>
  · 5080 removed from marketplace (246u) <https://i.redd.it/34ods6vogkyh1.png> · CMP170HX
  unlock tool 30/40-series-only (N/A our 5090, 179u)
  <https://wccftech.com/nvidia-rtx-30-40-gpus-get-faster-in-ai-llms-with-new-unlock-tool-but-prices-surge-too/>
- **Civitai: 0 NEW** across hot/newest/comfyworkflows/newloras (store dedup) → **NO ADOPT**.
- **MOSS (user opted out of checking):** news round-up (31u) + Character & Style Catalog
  v0.1.2 34,251 samples (137u) <https://i.redd.it/csmdjery8lyh1.png> — noted, not chased.
- **Tool packs:** MarcoStudio 13 image/video tools MIT (24u) <https://v.redd.it/g0dkuxhk0myh1>
  — **no-adopt for now** (generic toolbox) · Motion Previs Studio 3D camera blocking +
  ComfyUI rendering (27u) <https://v.redd.it/u1jw4i5q2oyh1> — **no-adopt for now** (heavy;
  camera control already covered by H3 prompting) · **Primal VAE** (Ostris, 159u — "better
  than Flux.2 VAE") — we anchor on qwen_image_vae (Krea2) / H3 VAE — noted, no action —
  <https://i.redd.it/yns229gpioyh1.png>

**ACTION ITEMS (new today):**
1. **Pika-H3-Flex official package** — fetch `comfy/loras/` BF16 weights + the Comfy
   workflows; compare against the community int8 pruned weights our 66.86 s kitchen run
   used. TOP ADOPT candidate.
2. **Open-H3-Regenerate-2K ComfyUI nodes** — inspect the refinement nodes + noise controls
   for the H3 pipeline (follow-up on yesterday's 168u announcement).
3. **Krea2 BBOX released** — locate model + node (Civitai/HF) — carried item resolved;
   relevant to character-region editing.
4. **Qwen3.8-27B-SLQ EAR99 Q6_K (23.3 GB)** — A/B candidate in a SEPARATE slot (never
   replace the live brain without user OK).
5. **llama.cpp CVE-2026-116096** — read the PSA (b11960 running) + check patched build.
6. **LTX 2.5 8 GB film studio** — inspect for the pending LTX-2.5 A/B test.
7. **Kokoro 600 MB voice clone** — evaluate for narration (D041: ambient-only audio;
   narration voice ≠ music).
8. Carried: X cookies (`X_AUTH_TOKEN`/`X_CT0`) · H3 Relay Hires / Openjutsu / PixText
   reads · candidate models (DeepSeek-V4.1-Flash-1017 + delta-inference-engine,
   Gemma-4-31B-Humanlike-Chat writer test) · LFM3-Audio-2B / 1.7B optional local tests.

**SOURCE FAILURES (tier status per D203):** X — tier 3 login-walled (browser ran; no
cookies set). r/comfyui_workflows — browser tier GATED 7th day (redlib.perennialte.ch now
410; catsarch parses no posts). Reddit JSON 403 all subs (HTML tier carries 3/5 —
ComfyUI/artificial returned 0 new, so nothing lost). Civitai ✅ 0 new (store dedup, all
four categories).

## 2026-10-30

**Sources:** Reddit ✅ HTML tier (SD 1 new/25, artificial 25 new/25, LocalLLaMA +
ComfyUI 0 new — all 403-JSON walled as usual; **comfyui_workflows GATED 6th
day** — browser tier rendered no shreddit cards) · HF ✅ 16 items · Civitai ✅
85 items (author tier production: named authors throughout) · X ❌
login-walled (7 accounts, browser tier ran, no `X_AUTH_TOKEN`/`X_CT0`).
**Pipeline note:** 08:00 schtask fetched + indexed (199 items) then got
**TERMINATED ~08:06** (exit 267009 = SCHED_S_TASK_TERMINATED — likely machine
sleep; only the final log line was lost). 08:13 manual re-run confirmed
idempotent completion: 0 new items, 0 newly indexed, store 1,218.

**New relevant items (vs 10-29 baseline):**
- **445u "Qwen3.8-Flash-Next tried to send a diagnostic file to a remote
  location, while stating otherwise"** — privacy post about our Qwen family —
  <https://cohere.com/blog/concerning-behaviour-popular-open-weight-ai-model>
- **443u "I think local AI cost me a job"** — <https://www.reddit.com/r/LocalLLaMA/comments/1xils4t/i_think_local_ai_cost_me_a_job/>
- **434u "TokenGate (Stanford/Berkeley): token-gated attention for long-context
  prefill"** — prefill speed tech relevant to our 260K ctx —
  <https://www.marktechpost.com/2026-10-25/stanford-berkeley-tokengate-learned-token-pruning-llm-prefill/>
- **227u "New MiniMax H3 Finetune by Pika Labs"** — H3 pipeline ADOPT candidate —
  <https://i.redd.it/w5bcogm0zfyh1.png>
- **168u "NVIDIA's new Open-H3-Regenerate-2K"** — <https://v.redd.it/lw42y195m9yh1>
- **212u "Qwen Image 2.1 + TRELLIS.2 in Blender: prompt → textured rigged
  character → village"** — <https://v.redd.it/pbk62dlemfyh1>
- **184u "Flux 3 Image is #1 model"** — <https://i.redd.it/yv64a5398lxh1.jpeg>
- **197u "Interactive neuron steering playground for Qwen3.5-4B on WebGPU
  locally"** — <https://v.redd.it/o8dxp8s94wxh1>
- **290u/1228 mistralai/Mistral-Large-4-1T-A52B** — day's top HF model (1T
  MoE — far beyond 32 GB; noted) — <https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B>
- **GPU-unlock cluster** (30-series only → N/A for our 5090): 175u power-limit
  tip <https://i.redd.it/bit36iugnmxh1.png> · 143u which-cards info post
  <https://www.reddit.com/r/StableDiffusion/comments/1xdim6w/information_post_about_what_are_the_unlocks_for/> · 134u 59% throughput on 3090 Ti
  <https://www.reddit.com/r/StableDiffusion/comments/1xdoh8k/i_tested_the_rtx_30series_gpu_unlock_up_to_59/>
- **MOSS cluster** (user opted out of checking): 229u tips
  <https://www.reddit.com/r/StableDiffusion/comments/1xe1nmu/a_few_tips_for_moss/> · 226u char-LoRA results
  <https://www.reddit.com/gallery/1xeunzs> · 197u showcase
  <https://www.reddit.com/gallery/1xd9o13> · 166u variety tests
  <https://www.reddit.com/gallery/1xg29si> · 159u "nailed Moss char loras"
  <https://www.reddit.com/r/StableDiffusion/comments/1xfu2d6/huge_shoutout_to_shootthesound_and_fizgig_i/> · 152u hype-psyop debate
  <https://www.reddit.com/r/StableDiffusion/comments/1xdoqfm/was_the_moss_hype_a_psyop_or_am_i_missing/> · 144u MOSS-Image-Edit-HQ v3
  <https://www.reddit.com/gallery/1xdwo6o>
- **HF new:** LiquidAI **LFM3-Omni-2B (206)** <https://huggingface.co/LiquidAI/LFM3-Omni-2B> +
  **LFM3-VL-2B (167)** <https://huggingface.co/LiquidAI/LFM3-VL-2B> (b11960 runs LFM3
  natively → optional local tests) · nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D (30)
  <https://huggingface.co/nvidia/PhysicalAI-Autonomous-Vehicles-Foundation4D> · nvidia/Granary-v2 (25)
  <https://huggingface.co/nvidia/Granary-v2>
- **Civitai: no new ADOPT candidates** — same top 10 (all author-named):
  Gladas Krea 2 Turbo 3,250 dl <https://civitai.com/models/2807513> · kimimorgam
  char-replace 2,604 <https://civitai.com/models/2843905> · Dasiwa Xtra 2,141
  <https://civitai.com/models/2861921> · LTX 2.3 Director 2,053
  <https://civitai.com/models/2677668> · H3+Ultimate Upscale 1,769
  <https://civitai.com/models/2901854> · ReDetail 2.0 1,715
  <https://civitai.com/models/2857731> · H3 Infinite Iteration 1,497
  <https://civitai.com/models/2895239> · Krea 2 Workflows 1,455
  <https://civitai.com/models/2896885> · H3 Looping 1,301
  <https://civitai.com/models/2873520> · Gladas Anima 1,233
  <https://civitai.com/models/2814428>. newloras = same legacy set → **NO ADOPT**.

**ACTION ITEMS (new today):**
1. **Pika Labs H3 finetune** (227u) + **NVIDIA Open-H3-Regenerate-2K** (168u)
   — inspect for the H3 pipeline.
2. **TokenGate** (434u) — read for long-context prefill implications (260K ctx).
3. **Qwen3.8-Flash-Next diagnostic-file post** (445u) — quick read (Qwen
   family, local-trust angle).
4. **LFM3-Omni-2B / VL-2B** — small, native on b11960 — optional test.
5. Carried: X cookies (`X_AUTH_TOKEN`/`X_CT0`) · H3 Relay Hires / Openjutsu /
   Krea2 BBOX / PixText reads · candidate-model tests (DeepSeek-V4.1-Flash /
   flint) · 3 Civitai adopt-tests.

**SOURCE FAILURES (tier status per D203):** X — tier 3 login-walled (browser
ran; no cookies set). r/comfyui_workflows — browser tier GATED 6th day. Reddit
JSON 403 all subs (HTML tier carries 4/5). redlib mirrors dead (410). Civitai
author tier ✅ production (all top-10 author-named).

## 2026-10-29

**Sources:** Reddit ✅ HTML tier (SD 49 + LocalLLaMA 47 + ComfyUI 25 +
artificial 25; comfyui_workflows GATED — 5th day) · HF ✅ 11 items · Civitai
✅ 85 items — **author tier production-verified: 83 named / 2 uid** · X ❌
login-walled (cookies not set). **08:00 schtask ran cleanly for the first
time in 3 days (machine awake) — 96 new items, no manual fetch needed.**
96 Reddit posts at 50+ (top: 1275u BF16-unlock).

**New relevant items (vs 10-28 baseline):**
- **1275u "RTX 3000 series can run BF16 almost 2× faster — NVIDIA locked it
  via kernel, not a hardware limit"** — day's top post; GPU-unlock cluster
  continues (Blackwell still excluded → N/A for our 5090) —
  <https://i.redd.it/9ew6udlf83xh1.png>
- **993u "Krea 2 king of styles!"** — adoption signal for our Krea2 base —
  <https://www.reddit.com/gallery/1xfeonr>
- **511u "Openjutsu — one-click character swap (ComfyUI Higgsfield
  challenge)"** — character-swap node pack → ADOPT candidate for our
  charswapmask chain — <https://v.redd.it/1p0n1b05l0yh1>
- **406u "Character Reference for Anima is released!"** — Anima ecosystem
  (our Gladas Anima candidate workflow) — <https://www.reddit.com/gallery/1xhfyso>
- **296u "H3 Relay Hires node: 0.5 → 2 MP upscaler, ~4× faster than native"**
  — H3 pipeline **ADOPT candidate** — <https://v.redd.it/kccwx11iu4yh1>
- **297u "PixText: small fast model for fixing text in generated images"** —
  text-fix tool for our title compositing — <https://www.reddit.com/gallery/1xd9186>
- **225u "Krea2 BBOX models have finished training and been released"** —
  Krea2 ecosystem expansion (bounding-box conditioning) —
  <https://www.reddit.com/gallery/1xh6gar>
- **252u "testing minimax h3 ref2va with my ps2 style lora"** — validates our
  ref2va + style-LoRA technique — <https://v.redd.it/fp7snoz784xh1> · 271u H3
  SLA + 8-step-LoRA lighting/physics tests — <https://v.redd.it/fki8d6xp6gxh1>
- **306u "PSA: 10Eros-Max Beta 7 is out"** — new SD-family checkpoint —
  <https://huggingface.co/TenStrip/10Eros-Max>
- **MOSS cluster** (user opted out of MOSS-image checking): 346u
  sft-normal-people <https://i.redd.it/npmhi04nt8xh1.png> · 253u MOSS-Image-Edit LoRA
  <https://i.redd.it/aonldybzc1xh1.png> · 228u tips
  <https://www.reddit.com/r/StableDiffusion/comments/1xe1nmu/a_few_tips_for_moss/>
- **HF new:** tencent/Hy-SimulMT-30B-A3B-FP8 (380)
  <https://huggingface.co/tencent/Hy-SimulMT-30B-A3B-FP8> · openbmb/MiniCPM-OCR-1.0
  (278) <https://huggingface.co/openbmb/MiniCPM-OCR-1.0> ·
  NVIDIA-Nemotron-3.5-Transcribe-30B-A4B (205 — speech-to-text, D041-safe
  input-side) <https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B> ·
  secemp9/arxiv-complete dataset (744) <https://huggingface.co/secemp9/arxiv-complete>
- **Civitai: no new ADOPT candidates** (same top 10, downloads rising, authors
  now show real names): Gladas Krea 2 Turbo 3,225
  <https://civitai.com/models/2807513> · kimimorgam char-replace turbo 2,588
  <https://civitai.com/models/2843905> · ReDetail 2.0 1,713
  <https://civitai.com/models/2857731> · Dasiwa Xtra 2,136
  <https://civitai.com/models/2861921> · LTX 2.3 Director 2,051
  <https://civitai.com/models/2677668>. newloras still the legacy
  SD1.5/SDXL/Pony set → **NO ADOPT**.

**ACTION ITEMS (new today):**
1. **H3 Relay Hires node** (296u) — inspect pack/workflow (0.5→2 MP upscaler
   for our H3 route).
2. **Openjutsu character swap** (511u) — inspect for the charswapmask chain.
3. **Krea2 BBOX models** (225u) — quick read: what does BBOX conditioning
   give us for reference-sheet work?
4. **PixText** (297u) — text-fix option for title compositing.
5. Carried: X cookies (`X_AUTH_TOKEN`/`X_CT0`) · candidate-model tests now
   possible on b11960 (DeepSeek-V4.1-Flash / RecursiveSI-flint) · 3 Civitai
   workflow adopt-tests · Krea2+PoseStudio read.

**SOURCE FAILURES (tier status per D203):** X — tier 3 login-walled (browser
ran, no `X_AUTH_TOKEN`/`X_CT0` set). r/comfyui_workflows — browser tier
GATED 5th day (no further tier exists for that sub). Reddit JSON 403 all
subs (tier 3 HTML carries 4/5). redlib mirrors dead. Civitai author tier ✅
production (83 named / 2 uid — tier ran inside the venv subprocess fix).

## 2026-10-28

**Sources:** Reddit ✅ HTML tier (SD 25 + LocalLLaMA 48 + ComfyUI 25 +
artificial 25; comfyui_workflows gated again — 4th day) · HF ✅ 9 items ·
Civitai ✅ 85 items — **author resolution now live: all 48 unique authors
resolved via browser tier (0 unresolved); files patched with real names** ·
X ❌ all 7 login-walled (tier 3 browser ran; cookies still not set).
08:00 schtask missed again (machine asleep) — manual fetch run, 302 newly
indexed. **73 Reddit posts at 50+** (top 340u "everything will be local
eventually").

**New relevant items (vs 10-27 baseline):**
- **223u "Mysterious Qwen4 Appearance by New GitHub Accounts"** — Qwen4
  signals intensify (writer/agent lineage watch).
- **GPU-unlock cluster (new theme today):** 240u "GPU unlocks (FP32
  accumulation): why Turing/Ampere/Ada but not Blackwell" · 236u "free 3090
  speedup hack, verified 15% PP / 5% TG" · 179u "CMP170HX-inspired unlocks
  30x/40x, up to 2× prefill speedup" · 168u "lower power limit when
  unlocking" → GPU/VRAM-trick reading for our 5090 (Blackwell is NOT in the
  unlockable set — consistent with our 5090 being locked).
- **219u "Ling-3.1-flash-1019 weights out + base model released"** (Ant) —
  fast-model writer-candidate family; +190u Ling-3.0-flash-Sante (124B /
  5.1B active) from yesterday.
- **217u "My MOSS Character Lora Training Results" + 172u "MOSS-Image Vision
  Text Encode (ComfyUI node + workflow)"** — MOSS char-LoRA cluster continues;
  the **ComfyUI node + workflow for MOSS's vision text encoder is NEW** →
  ADOPT candidate if we adopt MOSS for image work.
- **198u + HF 194-likes "NVIDIA Nemotron-3.5-Bolt-E4B-4GB"** — 4 GB MoE that
  runs anywhere (edge agent option; not a writer/agent replacement for us).
- **148u "⚠️ PSA: Fake GitHub projects — especially AI tools & ComfyUI custom
  nodes"** — supply-chain security → verify origins of the node packs we
  install via ComfyUI-Manager (esp. new packs before `install_node`).
- **180u "neuron-steering playground for Qwen3.5-4B in-browser WebGPU"** ·
  **177u "35B MoE at 20.5 tok/s on an iPhone"** · 173u "NVIDIA/OpenShell
  private runtime for autonomous AI agents" (context) · 161u "ZPix local
  open-source app adds lasso inpainting" (our charswapmask is ComfyUI-native —
  note only).
- **HF new:** baidu/Unlimited-OCR-2 (256 likes — OCR) · LiquidAI/LFM3-1.7B
  (208) · ccore/Qwen3.5-4B-3D-Coder (181) · bones-studio/seed dataset (350
  likes) · nvidia/simready-central-library (51) · Rapidata text-to-3d-with-
  llm-code (42).
- **Civitai workflows — NO new adopt candidates today:** top 10 = same as
  10-27 (downloads rising): Gladas Krea 2 Turbo (3,201) · mini-max char
  replace turbo 4-step (2,577) · H3 Dasiwa Xtra (2,122) · LTX 2.3 + Director
  (2,048) · H3 + Ultimate Upscale 8 GB (1,713) · ReDetail 2.0 LTX-2.5 4K
  (1,700) · H3 Infinite Iteration (1,472) · Krea 2 Workflows (1,414) · H3
  Looping/Morphing (1,274) · Gladas Anima (1,205).
- **Civitai new LoRAs — still NO ADOPT:** same legacy SD1.5/SDXL/Pony
  detail/style set (Not Artists 665 k, Detail Tweaker 583 k/461 k/410 k,
  Hands XL 311 k, blindbox 307 k, MoXin 288 k, Velvet Mythic Fantasy 246 k
  — the only Krea2-tagged one, style LoRA, D021 candidate — unchanged),
  Cute_girl_mix4 231 k, Disney Princess XL 208 k.

**ACTION ITEMS (new today):**
1. GPU-unlock reading (240u/236u/179u/168u) — confirm none applies to our
   5090 (Blackwell excluded per 240u) — 10-min read, close the thread.
2. MOSS-Image Vision Text Encode ComfyUI node/workflow (172u) — inspect the
   pack + workflow before any MOSS adoption.
3. Fake-GitHub PSA (148u) — quick check that our installed node packs match
   their registry origins.
4. Carried (10-27): llama.cpp b11583 CVE-2026-116096 update at convenience ·
   Krea2+PoseStudio hack read · adopt-test the 3 Civitai workflows · X
   cookies (`X_AUTH_TOKEN`/`X_CT0`) — the X tier is wired and waiting.

**SOURCE FAILURES (tier status per D203):** X — tiers 1+2 429 all 7; tier 3
browser head ran per account: pages render but timeline is login-walled
(article shells, zero tweet text) → **still awaiting `X_AUTH_TOKEN`/`X_CT0`
from user** (one-time). r/comfyui_workflows — browser tier GATED 4th day
(3 attempts, fresh-profile fallback). Reddit JSON 403 all subs (tier 3 HTML
carries 4/5). redlib mirrors dead. Civitai `/users/{id}` 401 → **resolved via
browser tier today (48/48 authors, 0 unresolved)** — the uid placeholders are
gone.

## 2026-10-27

**Sources:** Reddit ✅ HTML tier (SD 25 + LocalLLaMA 50 + ComfyUI 25 +
artificial 25; comfyui_workflows gated again) · HF ✅ 5 trending + 2
datasets · Civitai ✅ 85 items (hot/newest/ComfyWorkflows/new LoRAs, now
enriched with downloads via detail endpoint) · X ❌ 429 all 7.
**Reddit 50+ today: 73** (top = LocalLLaMA 311u "8 GB GPU, 262K context, 3.5
BPW Qwen-Flash-Next Coder at 70 T/s using llama.cpp").

**New relevant items (vs 10-26 baseline):**
- **198u "I 'hacked' Krea 2 to work with Pose Studio"** (r/StableDiffusion,
  u/foxdit) — Krea2 + Pose Studio bridge for style diversity (complaint:
  Qwen/Klein style diversity). → our Krea2 reference-sheet chain (D021) —
  read the thread for the technique.
- **Civitai "Gladas' Workflow for Krea 2 Turbo"** (3,175 dl, top new workflow)
  — Krea2 Turbo ComfyUI workflow → **ADOPT candidate** for reference-sheet
  speed.
- **Civitai "mini max character replace — with turbo lora 4 steps"** (2,565 dl)
  — H3 character-swap + 4-step turbo → **ADOPT candidate** for our
  charswapmask pipeline + turbo speed.
- **Civitai "ReDetail 2.0: LTX-2.5 video refine + upscale to 4K (workflow +
  CLI)"** (1,688 dl) — LTX-2.5 refine/upscale → **ADOPT candidate** for our
  VFX pipeline (our base model).
- **Civitai "Easy Workflow — MiniMax H3 + Ultimate Upscale for TURBO Hybrid —
  8GB"** (1,689 dl) — H3 upscale chain (we have 32 GB — no constraint issue) —
  review.
- **137u "18 clip reel of my Minimax H3 LoRA on a 3090"** — H3 LoRA trained +
  used on a 24 GB card → input for tonight's LoRA training plan.
- **140u "I finally nailed Moss char loras"** + 157u MOSS-Image-Base LoRA
  (Smartphone Snapshot Photo Reality v14) — MOSS character-LoRA results →
  tonight's training inputs.
- **177u "Flux 3 Image is #1 model"** — Flux-3 adoption signal (our Flux-3-
  Klein reference path).
- **149u "Qwen4-27B's 4-way HC shift?"** + 139u "Qwen4 expectations" — Qwen4
  27B signals continue (writer/agent lineage).
- **131u IBM Granite Speech 5.0 2B** — another small speech model → audio
  pipeline candidate (D041 check: speech is fine, verify no music output).
- **222u ornith-ai/Ornith-1.5-122B** (Qwen finetune; HF 190 likes, 60 k dl) —
  new open 122B candidate.
- **Civitai new LoRAs feed** (top: Not Artists 665 k dl, Detail Tweaker 583 k,
  Hands XL 311 k, blindbox/MoXin/Cute_girl_mix4) — all SD1.5/SDXL/Pony
  detail+style LoRAs → **NO ADOPT** (not our Krea2/H3/MOSS model family).

**ACTION ITEMS (new today):**
1. ⚠️ **llama.cpp CVE-2026-116096** (127u PSA, verified): OOB write in
   Pocket-TTS `pockettts-gen.cpp` on malformed mmproj files; fixed in
   **b11796+** (current b11871); medium. **Our build = b11583** (2026-10-13)
   → below fix line. Real risk ≈ 0 (we never load mmproj / run Pocket-TTS) —
   **update `D:\llama` build at next convenience**, not urgent.
2. Krea2 + Pose Studio hack (198u) — read thread, evaluate for reference-set
   style diversity.
3. Adopt-test: Gladas Krea 2 Turbo workflow + mini-max character replace
   turbo workflow + ReDetail 2.0 (LTX-2.5 4K refine).
4. Tonight's LoRA training — inputs gathered: H3 LoRA 3090 reel (137u), MOSS
   char LoRAs (140u/157u).

**SOURCE FAILURES (tier status per D203 — browser head is now the standing
last tier):**
- **X:** tiers 1+2 (syndication, mcp engine) 429 all 7 → **new tier 3 browser
  head ran today: profile pages render but the timeline sits behind the LOGIN
  wall (article shells, zero tweet text; nitter mirrors dead, threadreader
  404 — all verified live).** Unlocked by one-time env `X_AUTH_TOKEN`
  (auth_token) + `X_CT0` (ct0) — same pattern as `REDDIT_SESSION_COOKIE`;
  tier injects the cookies and reads the full timeline. **AWAITING USER COOKIES.**
- **r/comfyui_workflows:** browser tier GATED (3 attempts, fresh-profile
  fallback, no cards — 3rd day). Next tier: none known for this sub (small,
  intermittently challenge-gated) — retry daily.
- **Reddit JSON 403** all subs (tier 1 dormant — IP wall, proven cookie
  doesn't beat it) → HTML top-page tier (tier 3) carries 4/5 subs.
- **redlib mirrors:** both dead (catsarch engine error; perennialte HTTP 410).
- **Civitai `/users/{id}` 401** no-auth → **browser tier wired today**: model
  pages SSR `href="/user/<name>"` (verified: ReDetail 2.0 author = u/bambushu);
  `fetch_civitai` now resolves unresolved authors via ONE browser session +
  cache (`news/state/civitai_users.json`). Today's 85 files stay `uid:<n>`
  until the next run's cache fills.

## 2026-10-26 (baseline — first extended watch, D201/D202)

**Source status:** Reddit ✅ via new HTML top-page tier (`rag/reddit_html_top.py`
— JSON API is IP-walled, HTML page is not); r/comfyui_workflows intermittently
gated; HF ✅ 66 items; X ❌ 429 all 7 accounts; "ComfyUI channel" (Discord)
❌ not directly accessible — awaiting a feed URL from the user; LTX org ✅ no new
models since 09-28.

**Reddit 50+ (last 2 days, pulled live):**
- r/StableDiffusion — 25/25 posts at 50+: H3 ref2va + PS2 style LoRA (231u) ·
  Krea2 Turbo @4-step LoRA (190u) · Hy-Nomas (Tencent video model) native in
  ComfyUI on 12 GB (150u) · FLUX.3 Klein 12-task editing comparison (158u) ·
  MOSS character-LoRA training results (194u) · Fibo2.0 character LoRA same-day
  (149u).
- r/LocalLLaMA — 50/50 posts at 50+: llama.cpp server default port **8080→9931**
  (135u) · Qwen3.8-27B low-quant SSD-streaming prefiller trick (199u) · all
  Qwen-3.8-FN engines benchmarked on a single 5090+128 GB (129u) · Eagle-4
  engine (242u) · Qwen3.8-Flash-Next 125B on 16 GB via NVMe offload (239u) ·
  ISTA GSQ-RCO GGUFs for DeepSeek-V4.1-Flash (203u) · Phonon 31M/40M edge TTS
  (193u).
- r/ComfyUI — 49 posts, none at 50+ this week (top ≈ 43u: selflift-Fish longer
  H3 clips on 16 GB; first H3 scene on a 3090; 2x2 storyboard grid R2V; H3 on
  Apple Silicon).
- r/artificial — 25 posts, none at 50+.

**HF trending relevance (10-25 capture):** sam3 (masks → charswapmask chain) ·
fishaudio/drama-3 (audio — D041 output-class check first) ·
MiniMax-M3.1-Flash (H3 team's LLM) · LTX-2.5 trending (adoption signal) ·
Flux-3-Image-Klein +comfy · DeepSeek-V4.1-Flash (+FP8/GGUF) · Qwen3.8-27B +
distills · Krea2 base (Qwen-Image-2.1) trending · bge-m3/bge-reranker (RAG
upgrade path over MiniLM-384d).

**X:** @ltx_io no new official drop (profile now features community work:
@wildmindai 2D hand-drawn IC-LoRA, CQdesign Enhancer V2).

**ACTION ITEMS (carried from 2026-10-26):**
1. ⚠️ llama.cpp default port 8080→9931 — check our writer/agent server configs.
2. Qwen3.8-27B SSD-streaming prefiller trick — our agent model class.
3. Krea2 4-step turbo LoRA — reference-sheet speed-up candidate.
4. H3 ref2va + style LoRA technique — our video pipeline.
5. Tencent Hy-Nomas (12 GB) — evaluate as H3 alternative.
6. Phonon 31M/40M TTS — D041-safe only if speech/ambient (verify output class).
7. "Background text addition" community LoRA — still absent (3rd check).
8. ComfyUI-LTXVideo pack missing from running install — fix before VFX workflows.
9. User to provide a "ComfyUI channel" (Discord) feed URL to wire into the RAG.
