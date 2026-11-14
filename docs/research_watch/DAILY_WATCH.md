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

## 2026-11-14

**Sources:** Reddit ✅ 68 posts at 50+ (JSON 403 all subs as usual → HTML top-page tier; r/comfyui_workflows GATED 2nd straight day) · HF ✅ 39 trending + 6 top-downloads + 24 datasets · Civitai ✅ 4 items, 2 new · X ✅ all 7 accounts via browser-head, 40 tweets with full bodies (session healthy — no rotation). **Pipeline note:** 08:00 schtask catch-up died at launch (no log, stale code) → manual re-run hung ~12 min on a transient x.com stall (established conn, server sending nothing — same class as the user's Brave x.com hang this morning) → killed + re-run clean in 8 min (2696 items, 220 newly indexed, store 2864). All X tiers carry hard timeouts (30/90/300s) so no indefinite hang possible.

**New relevant items (vs 11-13 baseline):**

**H3-Image / H3 video (our A/B core):**
- **BennyDaBall_OG (A/B ground truth) validated OUR planned combo** — HyperFlow's Flash INT8 + PrunaAI P-H3 image LoRA → H3 images on a single 5090: 3872×2176 (8 MP) 8.7 s @ 6 steps vs 14.1 s stock H3 INT8; under 1 s at small sizes (512×288: 0.86 s); seed-only change 1344×768 in 0.86 s. Caveat: Flash 6-step "moves compositions vs stock" (his fisherman grew a hood); P-H3's own 8-step schedule stays closer (+1.7 s). All local ComfyUI. <https://x.com/BennyDaBall_OG/status/2120949801621807429>
- **Benny 16 MP benchmark table** (stock ComfyUI 0.45.0, 6 steps, 5090): 2048² BF16 8.24 s / W4A8 3.68 s / NVFP4 3.07 s; 4096² BF16 27.40 s / W4A8 14.52 s / NVFP4 12.93 s; sizes 40.23/12.55/12.54 GB — reference parity numbers for our 16 MP leg. <https://x.com/BennyDaBall_OG/status/2121291541683577120>
- **Benny Qwen Image 2.1 Turbo NVFP4 v2** — rebuilt with next solver, calibrated on image EDITING (not just t2i): LPIPS 0.166→0.136, PSNR 20.5→21.3 dB, edits 25% lower error per step; same 5.69 GB/speed; drop-in stock ComfyUI. Relevant to our identity-edit leg. <https://x.com/BennyDaBall_OG/status/2121074516382162996>
- **MiniMaxAI/MiniMax-H3-Image** — official H3-Image model on HF (trending #1, 949 score, 437k dl; t2i/i2i/image-editing). <https://huggingface.co/MiniMaxAI/MiniMax-H3-Image>
- **Comfy-Org/MiniMax-H3-Image** — official ComfyUI port (trending 318, 1.25M dl). <https://huggingface.co/Comfy-Org/MiniMax-H3-Image>
- **Viggle/Viggle-Remake** — MiniMax-H3-based **character-replacement video-editing LoRA** (v2v, GGUF, 183k dl) — the video-side counterpart of our image char-swap. <https://huggingface.co/Viggle/Viggle-Remake>
- **VideoRebirthAI/hyperflow-h3-flash** — H3 video (audio-video, t2v/i2v) in GGUF/safetensors (389k dl) — the model Benny's hybrid uses; local H3-video candidate. <https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash>

**Pose pipeline (our pending build):**
- **facebook/sam-3d-body-dinov3** — 3D human mesh recovery + human pose estimation (Meta, 1141 likes) — pose-reference asset candidate alongside the nvidia PhysicalAI-Human dataset. <https://huggingface.co/facebook/sam-3d-body-dinov3>

**Civitai (first new items since 11-12):**
- **2877939 "LTX 2.5 — Pure 2K/3K Ultra-Low VRAM (Universal Workflow)"** (NeronLTXEngine, LTXV 2.5, 8 reviews) — **config-only upload** (18.5 KB); checkpoint comes separately — watch for it (next-gen LTX for our labs route). <https://civitai.com/models/2877939>
- **112902 DreamShaper XL Turbo-Lightning** — 2024 classic back on hot (641k dl) — no-adopt (SDXL base; we're on Krea2/H3/LTX). <https://civitai.com/models/112902>

**Training tools / quant (next character training + brain A/B):**
- **Fizgig v9.7.0** released (supersedes the v9.6.0 update plan from 11-13). <https://github.com/shootthesound/Fizgig/releases/tag/v9.7.0>
- **unsloth/Qwen3.8-Flash-Next-GGUF** (2.3M dl) + **huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF** (4M dl) + **tencent/Qwen3.8-27B-DSpine-b16** (speculative-decoding draft model, sglang — caveat: our brain runs llama.cpp, DSpine is sglang-native) — brain A/B pool keeps expanding. <https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF> <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF> <https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16>
- **xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic** — top trending (3657) — 9B heretic merge, agent-fast context only. <https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic>
- Reddit: "train your own LLMs with less memory" (151 up) <https://www.reddit.com/gallery/1xtgnh9> · "macaq beats unsloth GGUFs" (135 up) <https://www.reddit.com/gallery/1xto0fa> · llama.cpp PR 28392 (139 up) <https://www.reddit.com/gallery/1xt9o3t>

**Audio (D041 — TTS/narration only, no music):**
- **Zyphra/ZONOS3-Mini** — multilingual TTS + voice cloning, GGUF (13k dl) — OmniVoice territory candidate. <https://huggingface.co/Zyphra/ZONOS3-Mini>
- **ConwayResearch/Underdog-Woof** — on-device CPU-only TTS (numpy) — zero-GPU narration fallback. <https://huggingface.co/ConwayResearch/Underdog-Woof>
- OmniVoice community thread #2 (125 up) — the 11-13 confirmation keeps rippling. <https://www.reddit.com/gallery/1xs46nh>

**GPU/hardware context (no action):**
- Alleged **96 GB RTX 5090** listed in China (254 up) <https://videocardz.com/newz/alleged-geforce-rtx-5090-with-96gb-listed-for-sale-in-china> · CMP 170HX voltage-glitch → A100 viral (244 up) <https://www.reddit.com/gallery/1xu1dkz>
- **speridlabs/idol** — Gaussian-splatting image-to-3D (Apache-2.0, 2.3k likes) — 3D context, no adopt. <https://huggingface.co/speridlabs/idol>

**X account activity (40 new, full bodies saved):** BennyDaBall_OG 5 (3 relevant above) · MaxLiu09 7 <https://x.com/MaxLiu09/status/2121199711055172041> · akatz_ai 7 <https://x.com/akatz_ai/status/2112625528805208257> · Alissonerdx 5 <https://x.com/Alissonerdx/status/2108452516556829295> · PixelAigc 5 <https://x.com/PixelAigc/status/2116445686577265633> · xieenze_jr 6 <https://x.com/xieenze_jr/status/2109484157952999505> · diodiogod 5 <https://x.com/diodiogod/status/620828381482191488>

**ACTION ITEMS:**
1. **Nov 16 pi-H3 (PrunaAI/P-H3-Image-Comfy) arrival → test Benny's hybrid leg** (HyperFlow-Flash INT8 @ 6 steps + P-H3 LoRA) as the fast H3-Image leg — his 5090 numbers: 8.7 s @ 8 MP, <1 s drafts; watch composition drift at 6 steps vs stock (his caveat).
2. **Post-A/B: bench our 16 MP leg against Benny's table** (NVFP4 4096² = 12.93 s @ 6 steps stock ComfyUI) — target parity, then the 4704×7040 step.
3. **User (browser, no GPU):** pull Benny's **Qwen Image 2.1 Turbo NVFP4 v2** (drop-in, edit-calibrated) — strengthens the identity-edit leg.
4. **Evaluate sam-3d-body-dinov3** for the pose-reference gallery (CPU inference — zero GPU conflict; pairs with the nvidia PhysicalAI-Human dataset).
5. **Fizgig v9.7.0** replaces the v9.6.0 update plan — update `D:\tools\Fizgig` before next character training.
6. **Watch for the LTX-2.5 checkpoint** behind civitai 2877939's low-VRAM 2K/3K universal workflow — evaluate vs our LTX labs route when it drops.
7. **Brain A/B pool (post-writer A/B):** rank Flash-Next-GGUF + huihui abliterated + unsloth quants vs our NVFP4-MTP-LOW; DSpine draft = sglang-only, likely not portable to our llama.cpp brain.
8. **Post-A/B:** Viggle-Remake as the character-consistency-in-video candidate (H3 v2v char replacement).

**Source failures (honest):**
- Reddit JSON tier: 403 all subs (standing; mirrors dead — redlib.catsarch.com browser-failed, perennialte.ch 410) → HTML top-page tier worked (SD 22 / LocalLLaMA 24 / ComfyUI 50 / artificial 25 posts, 0 new each).
- **r/comfyui_workflows HTML tier GATED 2nd straight day** (rc=3, no shreddit-post cards even in fresh temp profile) — retrying next run; if it persists 3 days, try the browser-tier retry from a warm profile.
- X syndication: 429 (standing) → all 7 accounts via browser-head tier ✓ (40 tweets, full bodies).
- Civitai boards healthy (hot 30 / newest 25 / comfyworkflows 15 / newloras 15) — 2 new items.

**Post-hoc items (user-flagged 15:46, fetched via browser tier):**
- **Nekodificador — H3 control thread + speech rhythm/intonation question** <https://x.com/Nekodificador/status/2120985455164305451> (11-12): "Would it be possible to control the rhythm and intonation of speech with something similar?" — in a thread about the new **H3 control** feature (11-13 replies: @AstrablueAI "H3 control — this is Magic", @seanward "ubiquitous feature in future AI video generators"). **Relevance: fine-grained H3-video control is landing, and the next frontier being discussed is speech rhythm/intonation control — directly adjacent to our narration domain (D041) and H3 r2v/ref2va routes.** When the H3-control release is official → test on our 2char-SAM + char-swap workflows. (Honest note: parent post itself did not render in browser-head — recorded from reply context.)
- **ComfyUI — Blender + video model** <https://x.com/ComfyUI/status/2121308924800647349> (11-13): agent-driven 3D — "made 7 felt puppets in my own 3D tool… they dance to a 138 BPM track and their jaws move on the beat. An AI agent did the heavy lifting, I directed it." **Relevance: 3D character/scene route for our movie pipeline (we hold the Blender MCP) + audio-reactive jaw/motion-sync technique (for us = narration-emphasis sync, D041 no-music).** When the feature/repo lands → evaluate as a third leg alongside 2D image→video and H3 r2v.

## 2026-11-13

**Sources:** Reddit ✅ 69 posts at 50+ (JSON 403 all subs as usual; HTML top-page tier) · HF ✅ 19 trending + 3 top-downloads + 12 datasets · Civitai ✅ hot + ComfyWorkflows (both items = 11-12 knowns → 0 new) · X ✅ 40 IDs (saved bodies EMPTY — 7 key new statuses fetched individually, worked). **Pipeline note:** 08:00 schtask FAILED (machine asleep — LastTaskResult 2147946720, last run 11-12 11:29; same mode as 11-09..11-12) → manual `daily.py --news-only` re-run → clean (2476 items, 191 newly indexed, store 2644); **r/comfyui_workflows HTML tier GATED this run** (rc=3, no shreddit cards → fresh-profile retry next run).

**New relevant items (vs 11-12 baseline):**

*Our exact brain + writer (user's A/B days = today/tomorrow):*
- **unsloth/Qwen3.8-27B-GGUF trending #1 (5756 likes, 5.9M dl)** — unsloth's official GGUF quants of our EXACT brain model = quant-alternative pool to the running NVFP4-MTP-LOW brain <https://huggingface.co/unsloth/Qwen3.8-27B-GGUF>
- **t3_1xpicjz (115u) — "qwen38_27b hitting 6645 toks on prefill and 316"** — community perf numbers on our brain family = throughput reference <https://www.reddit.com/r/LocalLLaMA/comments/1xpicjz/qwen38_27b_hitting_6645_toks_on_prefill_and_316/>
- **t3_1xto0fa (111u) — "opensource method macq beats unsloth ggufs"** — MacQ = new open quant method claimed to beat unsloth GGUFs — watch for future brain/writer quants <https://www.reddit.com/r/LocalLLaMA/comments/1xto0fa/opensource_method_macaq_beats_unsloth_ggufs/>
- **mradermacher/gemma-4-31B-it-ARA-heretic-GGUF (224 likes, 78K dl)** — new heretic GGUF quant of our WRITER family (gemma-4-31B) — optional add to today's writer A/B pool <https://huggingface.co/mradermacher/gemma-4-31B-it-ARA-heretic-GGUF>
- **t3_1xruzry (154u) — "Drummers Orion 26B-A4B v1 and v1.1 plus a new"** — new small-MoE brain-pool candidate <https://www.reddit.com/r/LocalLLaMA/comments/1xruzry/drummers_orion_26b_a4b_v1_and_v11_plus_a_new/>
- **t3_1xq4yju (143u) — "obsessive17b: a 11 GB websearch subagent"** + **xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic (4136 likes)** — small agentic-LLM candidates for the agent tier <https://www.reddit.com/r/LocalLLaMA/comments/1xq4yju/obsessive17b_a_11_gb_websearch_subagent/>

*H3-Image / our A/B legs:*
- **akatz_ai X (11-12) — "Generate at 33 megapixels (4704×7040) in ComfyUI with H3 Image"** — 33 MP = the H3-Image ceiling vs our 16 MP leg — post-A/B resolution step for final outputs <https://x.com/akatz_ai/status/2118403164374552897>
- **VideoRebirthAI/hyperflow-h3-flash (216 likes, 242K dl)** — new fast H3 video variant — video-route context <https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash>
- **BennyDaBall_OG X (11-11) — LFM3-1.7B NVFP4 quants updated with a new solver: "4–7% closer to BF16, stock llama.cpp, no patches, free re-download"** — quant-tuning craft from our ground-truth reviewer; technique transfers to small-model quants <https://x.com/BennyDaBall_OG/status/2120575920503222778>
- **t3_1xpz5ti (126u) — "Rebuilt Higgsfield's 'Miracle' demo edit by edit with Viggle-Remake — no private beta, run it locally"** — practical confirmation of the local char-animation route (Viggle-Remake = 11-12 context item) <https://www.reddit.com/r/StableDiffusion/comments/1xpz5ti/rebuilt_higgsfields_miracle_demo_edit_by_edit/>
- **t3_1xtpc2v (196u) — "LucidML world model: images → interactive real-time video, runs on RTX 3060+"** — new open interactive-video route (lucidml/gta on HF) — context only, H3-first <https://www.reddit.com/comments/1xtpc2v>
- **MaxLiu09 X (11-11) — pose retargeting into physics sim = "local optima based on physics, aesthetics, semiotics"** — pose-pipeline research context for our pose-reference work <https://x.com/MaxLiu09/status/2120560878919778535>

*Audio (D041 route):*
- **t3_1xs46nh (118u) — "omni_voice is the fastest and best voice clone"** — community confirmation of our OmniVoice TTS app <https://www.reddit.com/r/LocalLLaMA/comments/1xs46nh/omni_voice_is_the_fastest_and_best_voice_clone/>

*Training / tools:*
- **t3_1xqzu2f (165u) + t3_1xtkg94 (160u) — Fizgig v9.6.0 release** — our LoRA training tool shipped a major release (our checkout = 10-20 vintage) — update before next character training <https://github.com/shootthesound/Fizgig/releases/tag/v9.6.0>
- **t3_1xtgnh9 (133u) — "you can now train your own llms with less memory"** — low-memory LLM training (LoRA context) <https://www.reddit.com/r/LocalLLaMA/comments/1xtgnh9/you_can_now_train_your_own_llms_with_less_memory/>

*Datasets:*
- **nvidia/PhysicalAI-Human-1M-100K** — 1M human-motion samples (100K subset) — pose-reference pipeline asset (pose gallery sourcing) <https://huggingface.co/nvidia/PhysicalAI-Human-1M-100K>

*Context / no-adopt:* Muse Ember open-source drama t3_1xs0qmx (248u) <https://www.reddit.com/gallery/1xs0qmx> · moonshotai/Kimi-K3.1-Pro (1944 likes) <https://huggingface.co/moonshotai/Kimi-K3.1-Pro> · ricursiveAI/Ripple-65B-Preview (518) <https://huggingface.co/ricursiveAI/Ripple-65B-Preview> · webAI-Official/TwIL-8B (314) <https://huggingface.co/webAI-Official/TwIL-8B> · 3D datasets (sand3d-objaverse / tencent/TailorRig / pixel-art-atlas) — no-adopt (no 3D in our pipeline) · Civitai 0 new (112902 DreamShaper + 2877939 LTX-2.5-low-VRAM = both 11-12 knowns).

**ACTION ITEMS:**
1. **Writer A/B (USER, today/tomorrow):** optional new candidate = `gemma-4-31B-it-ARA-heretic-GGUF` alongside the existing pool (QAT-31B / Ortenzya / gemma-4-31B-it / 26B-A4B).
2. **Brain A/B (post-writer):** add `unsloth/Qwen3.8-27B-GGUF` quants to the brain pool vs current NVFP4-MTP-LOW (t3_1xpicjz = throughput reference).
3. **A/B legs:** after the 16 MP verdict, try the winning leg at 4704×7040 (33 MP, akatz_ai's setup) for final outputs.
4. **Fizgig:** update the `D:\tools\Fizgig` checkout (10-20) to v9.6.0 before next character training.
5. **Pose-reference pipeline:** `nvidia/PhysicalAI-Human-1M-100K` = candidate pose-gallery source.

**Source failures (honest):**
- 08:00 schtask missed (machine asleep — same mode as 11-09..11-12). Manual `daily.py --news-only` re-run clean.
- Reddit JSON API 403 all subs (as usual); redlib mirrors dead (catsarch + perennialte 410); HTML top-page tier carried (SD 20/24, LocalLLaMA 5/23, ComfyUI 25/25, artificial 25/25); **r/comfyui_workflows GATED this run** (fresh-profile retry next run).
- X tier: saved bodies EMPTY again (article-shell DOM) — 7 key new statuses individually fetched via `fetch_x_status.py` (cookies valid, worked). GOTCHA: parallel browser-tier jobs on the shared profile lock-collide (both first attempts failed) — run them SEQUENTIALLY.
- Civitai: 0 new items.

## 2026-11-12

**Sources:** Reddit ✅ 113 posts at 50+ (JSON 403 all subs as usual; HTML tier clean) · HF ✅ 36 trending + 6 top-downloads + 24 datasets · Civitai ✅ hot + ComfyWorkflows (newest/newloras 0 new) · X ⚠️ all 7 accounts via browser-head (IDs pulled, saved bodies EMPTY — 6 key statuses fetched individually, worked). **Pipeline note:** 08:00 schtask FAILED (LastTaskResult 2147946720 — machine asleep) → manual `daily.py --news-only` 09:51 stuck 92 min on a profile lock held by 3 ORPHAN headless_shell procs (from ~06:46, zero net connections) → killed strays + re-run 11:24 → clean in 27 min (2285 items, 195 newly indexed, store 2453). **GAP NOTE:** last block was 11-05 (7-day gap; 11-06/11-07/11-09/11-10 have no store data) — 11-08 store scanned for gap fill (2 items below).

**New relevant items (vs 11-05 baseline):**

*H3-Image (OUR A/B legs — the big cluster today):*
- **t3_1xsj747 (199u) — "H3 Editor: a timeline video editor for MiniMax H3 inside ComfyUI… (open source, GPL-3.0)"** — the H3 Editor we adopted (D220) is now trending community-wide — validation of the assembly-layer choice <https://www.reddit.com/r/StableDiffusion/comments/1xsj747/h3_editor_a_timeline_video_editor_for_minimax/>
- **t3_1xsrphc (184u) — "MiniMax H3 Image is natively supported in ComfyUI on day-0"** — native H3-Image support = our v0.45.2 + native nodes path confirmed by the community <https://v.redd.it/o37u7zutct0i1>
- **t3_1xtoutk (155u) — "According to Ostris, H3 Image has a VAE issue"** + **xieenze_jr X: "the main reason H3 Image struggles on detail is that it has a highly compressed latent space… H3 Image VAE scores worse on every metric, even worse than the SD 1.5 VAE"** — root cause for detail loss = the VAE, not the UNET → try alternate VAEs in the A/B leg <https://www.reddit.com/r/StableDiffusion/comments/1xtoutk/according_to_ostris_h3_image_has_a_vae_issue/> · <https://x.com/xieenze_jr/status/2119663862274503050>
- **t3_1xszz5f (159u) — "300 random prompts across styles on MiniMax H3" (h3-image-bench)** — 300-prompt H3-Image benchmark = A/B judging reference <https://jo-nike.github.io/h3-image-bench/>
- **t3_1xt9ocv (155u) — "MiniMax H3 Image 20MP Workflow"** — the 20MP workflow we already adapted (`h3image_20mp_cine.json`) is the community thread to watch for VAE fixes <https://www.reddit.com/gallery/1xt9ocv>
- **t3_1xt9yzt (163u) — "H3 Image is wildly creative"** + **t3_1xsp3xt (183u) — official MiniMaxAI/MiniMax-H3-Image repo trending** — quality sentiment + official repo (we run the Comfy-Org port) <https://www.reddit.com/gallery/1xt9yzt> · <https://huggingface.co/MiniMaxAI/MiniMax-H3-Image>
- **BennyDaBall_OG X (11-10) — full H3-Image review: 25 s/image (17-18 s seed-only) on 5090, 5472×3648 native, 6 steps no upscaler/LoRA, "very literal… small faces far from the camera smear… great for keyframes in video production using H3 video"** — our carried "Benny 25 s" baseline in full = the A/B ground-truth expectation <https://x.com/BennyDaBall_OG/status/2120251186574168146>

*Krea2 (identity leg):*
- **t3_1xohwh5 (150u) — "Krea 2 Turbo — 4 Step LoRA comeback (trained to 133K checkpoint, ~55K more than the 'final' 78K in Sep)"** — the Krea2 Turbo LoRA we run in the identity leg got a bigger checkpoint — candidate upgrade <https://www.reddit.com/gallery/1xohwh5>
- **t3_1xs9wrj (161u) — "Krea2 is King #2"** — stack sentiment <https://www.reddit.com/gallery/1xs9wrj>

*H3 video route:*
- **t3_1xp9nbb (172u) — "Super Huge Update for Minimax H3 Temporal Spatial Node"** — our H3 video node got a major update — check changelog before the next shoot <https://i.redd.it/75z8gwfuzyzh1.png>
- **PixelAigc X — MiniMax-H3-I2V-Anime-Motion-LoRA** (anime-motion LoRA for H3 I2V) — anime-only; we are photoreal → no-adopt, context <https://x.com/PixelAigc/status/2120758059815629100>
- **t3_1xtyxzo (154u) — ComfyUI blog: "Doubling LLM token rates in ComfyUI" / "LLMs just got twice as fast in ComfyUI 🚀"** — PE/TextGenerate perf doubling — relevant to our PE-gated 20MP leg <https://blog.comfy.org/p/doubling-llm-token-rates-in-comfyui>

*Brain/writer/agent pool:*
- **t3_1xs7ffm (203u) — "Same prompt, DeepSeek V4.1 Flash vs Qwen 3.8 FN: 94 tok/s vs 350 tok/s"** — OUR brain family beats DeepSeek V4.1 Flash 3.7× on speed — brain A/B data point <https://www.reddit.com/r/LocalLLaMA/comments/1xs7ffm/same_prompt_deepseek_v41_flash_vs_qwen_38_fn_94/>
- **t3_1xr2aaa (288u) — tencent/Qwen3.8-27B-DSpine-b16** — a DSpine quant of OUR exact brain — A/B candidate <https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16>
- **t3_1xted8w (268u) — "Ernie 5.5 Flash will be released in two weeks"** + **baidu/ERNIE-5.5-Flash-Base trending** — brain-pool release date ~Nov 26 <https://www.reddit.com/gallery/1xted8w> · <https://huggingface.co/baidu/ERNIE-5.5-Flash-Base>
- **t3_1xqacka (239u) — llama.cpp PR #30966 "llama_moe_cache: run missed experts on CPU"** — MoE feature for our brain/agent toolchain (pairs with carried gemma4 PR #31356) <https://github.com/ggml-org/llama.cpp/pull/30966>
- **t3_1xpvfx8 (256u) — "Harness Leaderboard — Kimi Code, Hermes, Pi, Claude Code, Codex… on Terminal Bench 2.1 & Deep SWE 1.1"** — agent-harness benchmarking (our agent class) <https://huggingface.co/spaces/joelniklaus/harness-leaderboard>
- **t3_1xrkomn (294u) — "L11 N8147 is a neuron that makes Qwen-3.5-4B get things confidently wrong… but writes interesting poetry"** — neuron-level quirk of OUR 4B agent family (qwen35_4b_q6 server) <https://www.reddit.com/gallery/1xrkomn>
- **t3_1xp32od (204u) — "Introducing Inkling 2 Small" (Thinking Machines)** + **t3_1xt82mz (205u) — MSR backdoored an AI agent by editing <10 dormant neurons** — brain-pool release + agent-safety research <https://thinkingmachines.ai/news/inkling-2-small/> · <https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/>
- **t3_1xqafp1 (185u) — "testing Qoduck (maybe qwen4) on Qoder"** — Qwen4 rumor — brain/writer pool watch <https://i.redd.it/v7ug4550w70i1.png>
- **t3_1xpm8mw (279u) — "Mirage: a 22 MB visual-language model" (scene desc + detection + OCR + segmentation, single pass)** — tiny VLM for the agent pool <https://www.reddit.com/gallery/1xpm8mw>
- **t3_1xpdk0i (219u) — "A 0.1B model just killed 8B embedding models"** — context (we do no embeddings) <https://www.reddit.com/gallery/1xpdk0i>

*Image/3D pool + hardware:*
- **t3_1xqeznz (154u) — "[Papers] WeLM-Image MoE 31.7B-5.4B: Unified Image Generation Model"** — new unified image MoE — image-pool context <https://www.reddit.com/gallery/1xqeznz>
- **t3_1xtl83k (150u) — "I can't stop making cheap flash photos with MOSS-Image-Base"** — new image model in active use — image-pool context <https://www.reddit.com/gallery/1xtl83k>
- **t3_1xozbe6 (188u) — "CCORE GLB-3D-Coder dataset: 3,918 examples across 40 domains" + t3_1xt6rc7 (203u) — 1.7B GLB-3D-Coder for Godot** — 3D-coding route; not our 2D→video pipeline → no-adopt, context <https://i.redd.it/ulne0ine2wzh1.jpeg> · <https://v.redd.it/gizdfgcmdw0i1>
- **t3_1xtdwps (209u) — "NVIDIA reportedly cancels RTX 5080 24GB launch, brings back 16GB over GDDR7 costs"** + **t3_1xojryw (277u) — "RTX PRO 5500 Blackwell appears at $17,999"** — GPU-market context (we have the 5090) <https://videocardz.com/newz/nvidia-reportedly-cancels-geforce-rtx-5080-24gb-launch-brings-back-16gb-model-over-gddr7-costs> · <https://videocardz.com/newz/nvidia-rtx-pro-5500-blackwell-appears-at-17999-msrp-higher-than-rtx-pro-6000>
- **t3_1xr78s5 (180u) — "Intel Arc Pro B70 32GB ($1,299) vs RTX 5090 on Qwen3.8-27B: ~1/2 speed (1/3 prefill) at 1/5 price"** — cheaper-brain alternative benchmark (context only) <https://www.reddit.com/gallery/1xr78s5>
- **HF: Viggle/Viggle-Remake (136k downloads, trending)** — character animation/remake model — character-route context (we do H3 video) <https://huggingface.co/Viggle/Viggle-Remake> · **NousResearch/Arete-27B (418 likes, Qwen finetune)** — brain-pool context <https://huggingface.co/NousResearch/Arete-27B> · **PrunaAI/P-H3-Image-Comfy (899k downloads)** — pi-H3, release Nov 16 (carried) <https://huggingface.co/PrunaAI/P-H3-Image-Comfy>

*Civitai:*
- **(hot) 112902 — DreamShaper XL (Lykon, 641k downloads)** — known SDXL checkpoint — NO-ADOPT (not our stack) <https://civitai.com/models/112902>
- **(comfyworkflows) 2877939 — "LTX 2.5 — Pure 2K/3K Ultra-Low VRAM (Universal Workflow)"** — LTX 2.5 low-VRAM video workflow — alternative video route; we are H3-centric → CONTEXT (fits the weekly labs+LTX thread; revisit if H3 video ever underperforms) <https://civitai.com/models/2877939>

*Gap fill (11-08 store, vs 11-05 baseline):*
- **t3_1xp9jt1 (431u, 11-08) — "Latest Open-Source Labs are gutting away cybersecurity and reverse-engineering"** — open-source models in the security field — brain-pool context <https://www.reddit.com/gallery/1xp9jt1>
- **t3_1xobe4h (361u, 11-08) — "CCORE GLB-3D-Coder 4B final model and full weights are out"** — 4B 3D-coder final (pairs with the 11-12 dataset post) <https://www.reddit.com/gallery/1xobe4h>

**ACTION ITEMS:**
1. **VAE experiment in the H3-Image A/B** (from ostris + xieenze_jr above): if leg B shows detail loss, swap the H3 VAE for a better round-trip VAE (xieenze's comparison names the winners; SD1.5-class VAE as the floor) — a one-line UNET/VAE-loader change in `h3image_t2i_cine.json`.
2. **Krea2 Turbo 133K checkpoint** (t3_1xohwh5): pull the extended LoRA → A/B vs our current identity-leg checkpoint at the same strength.
3. **Use Benny's review as A/B ground truth** (25 s/image, very literal, distant small faces smear, "great for keyframes") — the A/B judging criteria are now externalized.
4. **Watch t3_1xt9ocv (20MP workflow thread)** for community VAE fixes before running the 20MP leg.
5. **H3 Temporal Spatial Node "super huge update"** — check the changelog for compatibility with our H3 video workflow before the next shoot.
6. **ERNIE 5.5 Flash (~Nov 26)** — add to the brain-pool A/B list when it lands. pi-H3 remains Nov 16.

**Source failures (honest):**
- Reddit JSON API 403 all subs (as usual) — HTML tier clean (113 posts at 50+). redlib.perennialte.ch mirror 410 (r/artificial) — HTML top-page tier fallback OK (25/25).
- X tier: all 7 accounts fetched via browser-head but SAVED BODIES WERE EMPTY (article-shell-without-text, the known DOM-change symptom recurring) — 6 key statuses fetched individually via `fetch_x_status.py` (cookies valid, worked). diodiogod "new" items = 2021-era stale-tweet artifact (ignore).
- 08:00 schtask: LastTaskResult 2147946720 (machine asleep at 08:00). Manual re-run stuck 92 min on a profile lock held by 3 ORPHAN headless_shell procs (from ~06:46, zero network connections — killed before the 11:24 re-run, which completed clean in 27 min). LESSON: check for orphan browser procs before diagnosing a "slow" browser-tier run.

## 2026-11-05

**Sources:** Reddit ✅ HTML tier (SD 7 new / LocalLLaMA 10 new / ComfyUI 7 new / artificial 36 new; 70 posts at 50+; JSON 403 all subs as usual) · HF ✅ 22 trending models + 14 datasets (top-downloads 0 rows — 4th day) · Civitai ⚠️ hot only (DreamShaper XL, known — no-adopt) · X ⚠️ PixelAigc backfill only (50 files = 24 unique ×2; other 6 accounts login-walled). **Pipeline note:** 08:00 schtask did NOT run today (no log, no news dir — machine asleep?) — manual 09:51 re-run (`--news-only`): **completed clean in ~15min — no X-tier hang today** (1717 items, 274 newly indexed, store 1885).

**New relevant items (vs 11-04 baseline):**
- **t3_1xnhzbz (378u) — "Introducing Hy4 (open weights soon)"** — Tencent's Hy4 — open weights coming soon — model landscape (brain/agent pool when the weights drop) <https://hy.tencent.ai/research/hy4?langVersion=en>
- **t3_1xnuva2 (225u) — "Unsloth Qwen3.8-Flash-Next GGUFs V3.1 Update (November 4th 2026)"** — unsloth refreshed the GGUFs for OUR exact brain family — A/B candidate for the brain (carried Flash-Next recipe) <https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF>
- **t3_1xnrt67 (170u) — "Better Image-Edit workflow for MiniMax H3"** — H3 image-edit workflow — candidate for the movie H3 chain <https://v.redd.it/z20dzydo9mzh1>
- **t3_1xn6mm0 (161u) — "gemma4: graph optimizations (massive gains on pp for E2B and E4B)" — llama.cpp PR #31356** — our brain's toolchain (pairs with the carried "can only run gemma 4" thread) <https://github.com/ggml-org/llama.cpp/pull/31356>
- **t3_1xms6eq (144u) — "Is Qwen 3.8 27B still the king"** — community sentiment on OUR exact model (brain + agent) — READ <https://www.reddit.com/r/LocalLLaMA/comments/1xms6eq/is_qwen_38_27b_still_the_king/>
- **t3_1xn81vh (141u) — "Krea 3 Technical Report"** — Krea 3! our stack is Krea2 — next-gen architecture/quality context for the image pipeline (character LoRAs likely won't transfer — note for the movie) <https://www.reddit.com/gallery/1xn81vh>
- **t3_1xncdmm (124u) — "No more paywalls for Flux 2 Klein checkpoints on Civitai"** — Flux 2 Klein checkpoints now freely downloadable on Civitai — image-model pool <https://i.redd.it/obsllzhw9izh1.jpeg>
- **t3_1xmuowj (112u) — "Reshoot 4D: Reshoot Anyone in 4D"** — character-reshoot tooling (4D) — character-work context <https://v.redd.it/pjlfkrzwsezh1>
- **t3_1xngaid (103u) — "ComfyUI v0.44.0 released"** — check node changes affecting our workflows (we run a recent version) <https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.44.0>
- **t3_1xnqxlq (411u) — "I am big enough to admit that this is me"** — day's top post (self-deprecating image post; context only) <https://i.redd.it/lqr4hd2s4mzh1.jpeg>
- **t3_1xnx3cs (264u) — ricursiveAI/Ripple-65B-Preview** + **t3_1xnjiu4 (260u) — Axion1-0/Axion-1.0-35B** — new open-model releases (brain-pool context) <https://huggingface.co/ricursiveAI/Ripple-65B-Preview> · <https://huggingface.co/Axion1-0/Axion-1.0-35B>
- **t3_1xlusil (138u) — "Proposal: A community revolution for private quality benchmarks (and why endless chasing tok/s is rotting our brains)"** — community quality-vs-speed debate <https://www.reddit.com/r/LocalLLaMA/comments/1xlusil/proposal_a_community_revolution_for_private/>
- **t3_1xn5cfw (143u, up from 102u 11-04) — "Electricity per AI image on RTX 5090-class: about 3 to 10 cents per 1,000 images (FLUX.2 klein, 1024×1024)"** — cost data for our 5090 generation runs <https://www.reddit.com/r/StableDiffusion/comments/1xn5cfw/electricity_per_ai_image_on_an_rtx_pro_6000_rtx/>
- **HF NEW:** moonshotai/Kimi-K3.1-Pro (574 likes) — Moonshot's new Pro model (brain/agent pool) <https://huggingface.co/moonshotai/Kimi-K3.1-Pro> · unsloth/DeepSeek-V4.1-Flash-1017-GGUF (345 / 690k dl) — unsloth's cut of the carried 1017 build <https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF>
- **Carried + RISING (not new):** Qwen-Image-2.1-Turbo-Quantized (5652) · idol (632) · Sulphur-3 (364) · numbat (343 — still DO NOT DOWNLOAD) · Audio8-TTS (296) · OBLITERATUS (250) · SenseNova-Loop (235) · Open-H3-Regenerate-2K (201) · weight-space cluster (434/378/437 — still top)
- **Civitai:** DreamShaper XL (u/Lykon, 640k dl) hot — known, NO-ADOPT (SDXL-era generalist checkpoint; not in our Krea2/H3 stack) <https://civitai.com/models/112902>
- **X:** 50 files = PixelAigc timeline backfill (24 unique, listed twice) — no new signal; other 6 accounts login-walled (9th day).

**ACTION ITEMS (new today):**
1. **Unsloth Qwen3.8-Flash-Next GGUFs V3.1 (t3_1xnuva2)** — A/B the refreshed GGUFs against the brain's current recipe (carried Flash-Next A/B; V3.1 may improve speed/quality).
2. **Krea 3 Technical Report (t3_1xn81vh)** — READ; assess impact on our Krea2 pipeline (character LoRAs likely won't transfer).
3. **"Better Image-Edit workflow for MiniMax H3" (t3_1xnrt67)** — READ + adopt candidate for the H3 sheet/edit chain.
4. **gemma4 graph-optimizations llama.cpp PR #31356 (t3_1xn6mm0)** — check applicability to the brain (carried gemma4 thread).
5. **Hy4 (Tencent) open-weights announcement** — watch; brain/agent pool when weights drop.
6. Carried (11-04): H3 tiny sliders A/B · Krea2/H3 text encoder comparison · Strata 20× patch · P-H3-Image-Comfy · X-tier timeout fix.

**SOURCE FAILURES (tier status per D203):** 08:00 schtask did NOT run today (no log entry, no news dir — machine asleep?) — manual 09:51 re-run covered it (clean ~15min, no X hang today; store 1885, 274 newly indexed) · X — 6/7 accounts login-walled (9th consecutive day; tier-4 fix = one-time `X_AUTH_TOKEN`+`X_CT0` env — not set, deprioritized) · Civitai — hot only (DreamShaper XL, known); newest/ComfyWorkflows/new-LoRAs returned 0 new (partial, NOT verified-zero) · HF top-downloads 0 rows (API quirk, 4th day) · Reddit JSON 403 all subs (HTML tier carried — 70 at 50+) · r/comfyui_workflows HTML tier GATED (10th consecutive day).

## 2026-11-04

**Sources:** Reddit ✅ HTML tier (126 items, 92 posts at 50+; JSON 403 all subs as usual) · HF ✅ 19 trending models + 11 datasets (top-downloads 0 rows — 3rd day) · Civitai ⚠️ hot only (DreamShaper XL, known — no-adopt) · X ⚠️ PARTIAL — PixelAigc timeline backfill only (25 files, mostly old 2024-25 posts + 1 recent); other 6 accounts still login-walled. **Pipeline note:** 08:00 schtask CRASHED today (Result 3221225786, log header only, no "done") — manual 09:50 re-run (`--news-only`) hung in the X tier ~3.7h after the PixelAigc backfill (idle python, no browser process, no profile lock) — killed at 13:50; the watch ran on the 169 captured files.

**11-03 "unidentified" posts now TITLED (gap resolved):**
- **t3_1xljdnj (437u) — "Sorry Sam, my 'quite terrible' home DRAM is at 100%: patched Strata to make DeepSeek V4.1 agent sessions start 20× faster on a good old standard gaming GPU"** — the 11-03 day-top image post — local agent sessions on a gaming GPU = OUR exact class (brain on 5090) — READ the patch approach <https://i.redd.it/dwgmz70zi3zh1.png>
- **t3_1xlys6k (366u) — "[Release] ISTA DeepSeek-V4.1-Flash-1017 GSQ-RCO Coder: a 763B model at 1 bit per parameter"** — 763B @ ~1bpp won't fit our 64GB RAM, but the GSQ-RCO 1-bit quant technique is the interesting part for llama.cpp quants <https://www.reddit.com/gallery/1xlys6k>
- **t3_1xlwpqv (339u) — "Not another tok/s post: local quants vs Claude on 9 real bugs"** — real-task quality data for local-brain choices <https://i.redd.it/ufmzse0g77zh1.png>
- **t3_1xkibxw (220u) — "CrowdGPT v2.6 - The collaborative LLM"** — context <https://i.redd.it/4zhosp53cuyh1.png>

**New relevant items (vs 11-03 baseline):**
- **t3_1xhdmlk (470u) — "Artificial Analysis Intelligence Index v5 (major update)"** — day's top post; LLM landscape/benchmark context <https://www.reddit.com/gallery/1xhdmlk>
- **t3_1xl4ckr (432u) — "Don't people pay attention anymore when buying hardware for AI?"** — hardware-market cluster (pairs with the PCB-shortage posts) <https://www.reddit.com/r/LocalLLaMA/comments/1xl4ckr/dont_people_pay_attention_anymore_when_buying/>
- **t3_1xmbj0v (313u) — "New sparse attention method for ultra-long context"** — long-context technique for the brain <https://x.com/jcrwhittington/status/2117317159777177602>
- **t3_1xm33gr (255u) — "yet another reason to self-host anthropic has"** — self-hosting sentiment <https://www.reddit.com/r/LocalLLaMA/comments/1xm33gr/yet_another_reason_to_self_host_anthropic_has/>
- **t3_1xn2jyz (203u) — "what do people with normal hardware (32GB RAM, 16GB VRAM) use"** — our hardware class discussion <https://www.reddit.com/r/LocalLLaMA/comments/1xn2jyz/what_do_people_with_normal_hardware_32gb_ram_16gb/>
- **t3_1xn1gs9 (195u) — "I tried MIT's weightspace programming on my own"** — community reproduction of the 11-03 TOP cluster (weight-space editing) — READ for the LoRA-training implications (in-place edits vs low-rank deltas for character LoRAs) <https://www.reddit.com/r/LocalLLaMA/comments/1xn1gs9/i_tried_mits_weightspace_programming_on_my_own/>
- **t3_1xmmadn (172u) — "DeepSeek V5 is planned to be pre-trained on Huawei Ascend chips"** — model-landscape context <https://www.reddit.com/r/LocalLLaMA/comments/1xmmadn/deepseek_v5_is_planned_to_be_pretrained_on_huawei/>
- **Hardware supply cluster: t3_1xj4qi0 (170u) — "Guys I think I found our GPUs" (Business Insider: AI boom → "heaps" of a new phenomenon) + t3_1xk17m0 (330u) — "AI boom triggers massive PCB shortage, orders booked until 2030"** — GPU/PCB market: do NOT plan hardware purchases now (prices rising) <https://www.linkedin.com/posts/businessinsider_the-ai-boom-is-facing-a-new-phenomenon-heaps-activity-7521314592090705920-K6m8> · <https://wccftech.com/ai-boom-triggers-massive-pcb-shortage-with-orders-booked-until-2030/>
- **t3_1xjvasi (167u) — "I made tiny sliders for MiniMax H3 that control motion, emotion, and more without training a LoRA [ComfyUI]"** — the 11-03 carried "tiny sliders" item as a ComfyUI post — motion/emotion control without LoRA = DIRECT fit for the movie R2V shots — READ + install candidate <https://v.redd.it/6snf3fm9zoyh1>
- **t3_1xkzony (165u) — "A tiny 109M-parameter model outperforms models up to 72B at image-text alignment, using 42× less training data"** — VLM alignment research <https://x.com/askalphaxiv/status/2116779287390896418>
- **t3_1xn7rfh (162u) — "[llama.cpp fork]: QFN + [specific quant] + [ultra specific hardware config] = [incredible and irreproducible pp and tg]"** — our brain's toolchain — check what the fork does <https://www.reddit.com/r/LocalLLaMA/comments/1xn7rfh/llamacpp_fork_qfn_specific_quant_ultra_specific/>
- **t3_1xkb7ay (160u) — "ostris is training MOSS image to use Primal VAE"** + **t3_1xjmxyo (141u) — "Examples of two stage MOSS-Image-Base + 8-steps-dmd2 at 6mp"** — MOSS VAE work + quality examples (noted; user opted out of MOSS chasing) <https://www.reddit.com/r/StableDiffusion/comments/1xkb7ay/ostris_is_training_moss_image_to_use_primal_vae/> · <https://www.reddit.com/gallery/1xjmxyo>
- **V4.1-Flash-1017 quant cluster (new 1017 build):** t3_1xm0uy0 (149u) — AtomicChat GSQ-RCO GGUF <https://huggingface.co/AtomicChat/DeepSeek-V4.1-Flash-1017-Uncensored-GSQ-RCO-GGUF> · t3_1xjkjla (138u) — "ISTA DeepSeekV4.1Flash1017 GSQRCO quants comparison" <https://www.reddit.com/r/LocalLLaMA/comments/1xjkjla/ista_deepseekv41flash1017_gsqrco_quants_comparison/> — noted (won't fit our RAM)
- **t3_1xjkajg (137u) — "im just laughing at fal"** — fal cloud-image-API pricing complaints (cloud context) <https://www.reddit.com/r/StableDiffusion/comments/1xjkajg/im_just_laughing_at_fal/>
- **t3_1xicnjs (113u) — "Krea 2 and MiniMax H3 text encoder comparison"** — DIRECTLY relevant (our exact stack: Krea2 + H3) — READ to sanity-check our qwen3vl_4b CLIP choice for Krea2 <https://www.reddit.com/r/StableDiffusion/comments/1xicnjs/krea_2_and_minimax_h3_text_encoder_comparison/>
- **t3_1xn1mep (111u) — PrunaAI/P-H3-Image-Comfy** — H3 image generation in ComfyUI (Pruna) — candidate alternative/complement for our Krea2 stills chain <https://huggingface.co/PrunaAI/P-H3-Image-Comfy>
- **t3_1xmal1l (145u) — "Open-H3-Regenerate-2K to preserve draft pass details"** — H3 regenerate-2K usage (pairs with HF `Efficient-Large-Model/Open-H3-Regenerate-2K`, 413k dl) — H3 route <https://v.redd.it/wecv2asir9zh1>
- **t3_1xms9ii (144u) — "What Qwen is thinking when it gets stuck saying 'Wait'"** — brain-behavior context (fun read) <https://i.redd.it/9xp6rgam8ezh1.png>
- **HF NEW:** abenzerps/Qwen-Image-2.1-Turbo-Quantized (5625 likes / 2.5M dl — top trending) — Qwen-Image turbo quant pool <https://huggingface.co/abenzerps/Qwen-Image-2.1-Turbo-Quantized> · Efficient-Large-Model/Open-H3-Regenerate-2K (201 likes / 413k dl) <https://huggingface.co/Efficient-Large-Model/Open-H3-Regenerate-2K> · xiaomi-research/Xiaomi-OCR-0 (262) — OCR tooling <https://huggingface.co/xiaomi-research/Xiaomi-OCR-0> · AtomicChat/LFM3-1.7B-Uncensored-GGUF (239) — small uncensored GGUF (brain pool) <https://huggingface.co/AtomicChat/LFM3-1.7B-Uncensored-GGUF>
- **Carried + RISING (not new):** Sulphur-3 (272→334 likes) · numbat (299→323 — still DO NOT DOWNLOAD, hoax flag) · Audio8-TTS-Realistic-Air (251→276) · OBLITERATUS Flash-1017 (222→235) · SenseNova-Loop-9B (190→213) · Betelgeuse IQ4_XS (162→166) · Mage-VL-Cowork (145→146) · DFlash2 GGUF (139→140) · Qwen 3.8 27B sentiment (211→466)
- **Civitai:** DreamShaper XL (u/Lykon, 639k dl) hot — known, NO-ADOPT (SDXL-era generalist checkpoint; not in our Krea2/H3 stack) <https://civitai.com/models/112902>
- **X:** 25 files = PixelAigc timeline backfill (mostly 2024-25-era posts, 1 recent: 2116511077202833801) — no new signal; other 6 accounts login-walled (8th day).

**ACTION ITEMS (new today):**
1. **H3 tiny sliders (t3_1xjvasi, 167u)** — READ the post; if it's an installable ComfyUI pack → A/B one R2V shot (motion/emotion control without a LoRA = direct fit for the movie shots).
2. **Krea2 vs H3 text encoder comparison (t3_1xicnjs)** — READ; sanity-check our qwen3vl_4b CLIP choice for Krea2.
3. **Strata 20× gaming-GPU patch (t3_1xljdnj)** — READ; check applicability to our llama.cpp brain config (5090).
4. **P-H3-Image-Comfy (Pruna, t3_1xn1mep)** — inspect the repo; H3-image-in-ComfyUI (candidate for the Krea2 stills chain).
5. **X-tier hang FIX** — add a per-account timeout to the X tier in `fetch_news.py` (hung ~3.7h after the PixelAigc backfill: idle python, no browser process, no profile lock — a bare network wait with no timeout); or skip the X tier when no cookie is set.
6. Carried (11-03): weight-space blog READ (now with the 195u community-repro thread) · Sulphur-3 card · DFlash2 A/B · Audio8-TTS eval · FastH3 darkening check.

**SOURCE FAILURES (tier status per D203):** 08:00 schtask CRASHED (Result 3221225786; log header only, no "done") — manual 09:50 re-run covered the fetch · **X tier HUNG ~3.7h** after the PixelAigc backfill (idle python, no browser process, no profile lock — killed at 13:50; the watch ran on the 169 captured files) · X — 6/7 accounts login-walled (8th consecutive day; tier-4 fix = one-time `X_AUTH_TOKEN`+`X_CT0` env — not set, deprioritized) · Civitai — hot only (DreamShaper XL, known); newest/ComfyWorkflows/new-LoRAs returned nothing new (partial, NOT verified-zero) · HF top-downloads 0 rows (API quirk, 3rd day) · Reddit JSON 403 all subs (HTML tier carried — 92 at 50+) · r/comfyui_workflows HTML tier GATED (9th consecutive day).

## 2026-11-03

**Sources:** Reddit ✅ HTML tier (91 new: SD 17 / LocalLLaMA 22 / ComfyUI 38 / artificial 14; 56 posts at 50+; JSON 403 all subs as usual) · HF ✅ 12 trending models + 9 datasets (top-downloads 0 rows again) · Civitai ⚠️ hot 1 new (DreamShaper XL re-identified, 639k dl — known); newest/ComfyWorkflows/new-LoRAs = 0 new (quiet day, not verified-zero) · X ❌ all 7 accounts login-walled (429 engine-blocked + login-gated browser tier — the one-time tier-4 fix remains `X_AUTH_TOKEN`+`X_CT0` env, deprioritized). **Pipeline note:** 08:00 schtask did NOT run today (last run 11-02 08:00, machine asleep?) — daily re-run at 09:50 IST (`--news-only`, idempotent, exit 0): 105 newly indexed items.

**New relevant items (vs 11-02 baseline):**
- **Weight-space programming cluster (378u + 347u) — MIT CSAIL: "GPT-6 Astra edits Qwen3.5 0.8B weights in-place, math 7.9→48.1"** — the day's top-relevance pair: direct weight-space editing as a training alternative/complement — exactly our LoRA-training territory (in-place weight edits vs low-rank deltas for character LoRAs) — READ the blog <https://rikiyat.github.io/blog/weight-space-programming/> · <https://explainx.ai/blog/weight-space-programming-gpt-6-astra-edits-qwen3-5-0-8b-weights-math-7-9-to-48-1-mit-csail-2026>
- **Sulphur-3 is ON HF now — FusionCow/Sulphur-3 (272 likes, 195 dl)** — the 11-02 "coming soon" teaser materialized on HF — Krea2-alternative pool candidate; check the model card/architecture before any sheet test <https://huggingface.co/FusionCow/Sulphur-3>
- **nazeshinjite/Qwen3.8-Flash-Next-DFlash2-GGUF (139u thread)** — fresh DFlash2 GGUF for OUR exact model family — A/B candidate for the brain (carried 11-02 action item) <https://huggingface.co/nazeshinjite/Qwen3.8-Flash-Next-DFlash2-GGUF/>
- **"Betelgeuse running Qwen 3.8 Flash Next IQ4_XS" (162u)** — new speed data point for the carried Flash-Next recipe A/B <https://www.reddit.com/r/LocalLLaMA/comments/1xkh2ns/betelgeuse_running_qwen_38_flash_next_iq4_xs_at/>
- **"qwen 3.8 27b is sometimes so smart it scares me" (211u)** — community sentiment on the model family we run locally (brain + agent) — context only <https://www.reddit.com/r/LocalLLaMA/comments/1xmbym0/qwen_38_27b_is_sometimes_so_smart_it_scares_me/>
- **microsoft/Mage-VL-Cowork (145u + HF trending)** — new Microsoft VL agent model — writer/agent pipeline context <https://huggingface.co/microsoft/Mage-VL-Cowork>
- **Edge0/Audio8-TTS-Realistic-Air (HF trending, 251 likes / 7.2k dl)** — new realistic-voice TTS variant in the Audio8 family — D041 narration pool (voice ≠ music — allowed) — evaluate for movie narration <https://huggingface.co/Edge0/Audio8-TTS-Realistic-Air>
- **OBLITERATUS/DeepSeek-V4.1-Flash-1017-obliterated (222 likes / 1.1k dl)** — abliterated Flash variant (TE-ablation context carried 11-02) <https://huggingface.co/OBLITERATUS/DeepSeek-V4.1-Flash-1017-obliterated>
- **sensenova/SenseNova-Loop-9B-Preview (190 likes / 1.5k dl)** — new SenseTime family preview (carried SenseNova 6.8 Code2Video thread) — watch <https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview>
- **burner22/numbat RE-SURFACED on trending (299 likes / 7.1k dl, up from 204/5.8k 11-01)** — the recorded RNG-tensor HOAX — still DO NOT DOWNLOAD; warn if user asks <https://huggingface.co/burner22/numbat>
- **AMD "another Radeon GPU + GDDR6 price increase in November" (156u)** + "spent a lot on my rig but I can only run gemma 4" (182u) — hardware cluster (no action for our 5090) <https://videocardz.com/newz/amd-reportedly-plans-another-radeon-gpu-and-gddr6-price-increase-in-november>
- **ComfyUI-sub signals under 50u (relevant):** MOSS image DAILY roundups now running (31 Oct / 1 Nov / 2 Nov — fast-moving; user opted out of MOSS chasing, noted only) <https://www.reddit.com/r/ComfyUI/comments/1xm72g8/a_quick_mossimage_news_roundup_2nd_november_2026/> · **"fizgig H3 still images — latent runs in any workflow" (14u)** — H3 still-image latent injection — candidate for our H3 sheet chain <https://www.reddit.com/r/comfyui/comments/1xhtrxj/fizgig_h3_still_images_latent_runs_in_any_workflow/> · **"FastH3 videos getting darker and darker" (16u)** — FastH3 exposure issue — check vs our FastH3 sheet workflow (carried) <https://www.reddit.com/r/comfyui/comments/1xka09k/fasth3_videos_getting_darker_and_darker/> · **"why LTX 2.5 is being ignored" (11u)** <https://www.reddit.com/r/comfyui/comments/1xgyt9z/why_ltx25_is_being_ignored/> · **"STEM Studio — my submission for open-source Higgsfield" (14u)** — open-source Higgsfield context (our pending setup) <https://www.reddit.com/r/comfyui/comments/1xjoztu/stem_studio_my_submission_for_opensourcehiggsfield/> · koboldcpp v1.124 release <https://github.com/LostRuins/koboldcpp/releases/tag/v1.124>
- **Unidentified top media posts (no titles captured in the HTML tier — honest gap):** t3_1xljdnj (421u — day's top post, image) <https://i.redd.it/dwgmz70zi3zh1.png> · t3_1xlys6k (336u) <https://www.reddit.com/gallery/1xlys6k> · t3_1xlwpqv (316u) <https://i.redd.it/ufmzse0g77zh1.png> · t3_1xkibxw (217u) <https://i.redd.it/4zhosp53cuyh1.png>

**ACTION ITEMS (new today):**
1. **Weight-space programming (MIT CSAIL, 378u/347u)** — READ the rikiyat blog; assess in-place weight editing vs our LoRA-delta character training (tonight's V3 train is the testbed).
2. **Sulphur-3 HF card (FusionCow)** — check architecture/model card; if Krea-family DiT → sheet-test candidate.
3. **DFlash2 GGUF (nazeshinjite)** — A/B against the brain (carried 11-02).
4. **Audio8-TTS-Realistic-Air** — evaluate for D041 movie narration (voice-only, no music).
5. **FastH3 darkening issue** — check our FastH3 sheet workflow for the same exposure drift (carried).
6. **burner22/numbat re-surfaced** — keep the hoax flag current; DO NOT DOWNLOAD.
7. Carried (11-02): SenseNova 6.8 Code2Video evaluation · ZenTrainer inspection · KreaMossMix sheet-chain inspection · DeepSeek super-agent architecture read · H3 "tiny sliders" workflow · Betelgeuse bit-exact Flash-Next A/B · LayerShop Regions · Pika H3-Flex ADOPT · llama.cpp CVE-2026-116096.

**SOURCE FAILURES (tier status per D203):** Reddit JSON 403 all subs (HTML tier carried — 91 new items) · r/comfyui_workflows HTML tier GATED (8th consecutive day) · X — all 7 accounts: engine 429 + browser tier login-gated (anonymous X walled; tier-4 fix = one-time `X_AUTH_TOKEN`+`X_CT0` env — not set, deprioritized) · Civitai — hot only had 1 new (DreamShaper XL, known); newest/ComfyWorkflows/new-LoRAs returned 0 new (quiet day — treat as partial, NOT verified-zero) · HF top-downloads 0 rows (API quirk, carried) · 08:00 schtask missed today (machine asleep) — manual 09:50 re-run covered it.

## 2026-11-02

**Sources:** Reddit ✅ HTML tier (33 posts 50+: LocalLLaMA 5 / StableDiffusion 10 /
ComfyUI 0 / artificial 0 — JSON 403 on all subs as usual; ComfyUI top ≈ 29u) ·
HF ✅ 6 trending models + 4 datasets (top-downloads 0) · Civitai ⚠️ PARTIAL — hot only
(DreamShaper XL 112902, 639k dl — re-identified via browser head this run); no
ComfyWorkflow/new-LoRA captures · X ✅ tier-3 browser (4 of 7 accounts: MaxLiu09,
PixelAigc, xieenze_jr; no capture BennyDaBall_OG / Alissonerdx / diodiogod) — 99
items, again mostly 2024–25 timeline backfill (ID range 1823…–1901… ≈ 2024–25;
only the 2109…/2116… 2026-10/11 posts are new-era, already flagged 11-01).
**Pipeline note:** 08:00 schtask clean — LastTaskResult 0, log `fetch: 9 new
items` + `done` — no re-run needed.

**New relevant items (vs 11-01 baseline):**
- **SenseTime open-sourced SenseNova 6.8 Code2Video — "video creation through
  code, with natural-language editing" (99u)** — new code-driven video route
  (code + NL editing, vs our prompt-driven H3 route) — watch; potential
  deterministic-composition complement <https://www.reddit.com/r/StableDiffusion/comments/1xguh4z/>
- **ZenTrainer — open-source LoRA trainer INSIDE ComfyUI (image + video, live
  previews, NVIDIA/AMD) (134u)** — in-ComfyUI LoRA training; complements our
  AI-Toolkit krea2 recipe (live preview is the useful part) — evaluate, NOT a
  recipe replacement <https://www.reddit.com/r/StableDiffusion/comments/1xjjst7/i_made_zentrainer_an_open_source_lora_trainer_that_runs_inside_comfyui_image_video_models_live_previews_nvidia_or_amd/>
- **KreaMossMix Workflow — "one model composes, the other finishes it" (100u)**
  — Krea + MOSS compose/finish chain — candidate for our Krea2 reference-sheet
  pipeline <https://www.reddit.com/gallery/1xj1xxe>
- **"Sulphur-3 is coming soon!" (155u)** — new image-model family teaser —
  watch for the release; candidate in the Krea2-alternative pool
  <https://www.reddit.com/r/StableDiffusion/comments/1xl6amz/sulphur3_is_coming_soon/>
- **burner22/numbat — HF trending (204 likes, 5.8k dl) = ALLEGED Anthropic
  "Mythos-class" checkpoint leak (claims ~14T params)** — 11-01 community
  audit: 43 tensors rebuild exactly from their own names via a seeded RNG =
  random-number tensors → **treat as hoax/unverified — DO NOT DOWNLOAD**
  <https://huggingface.co/burner22/numbat>
- **Comfy-Org/Idol (released 11-01, HF API)** — ComfyUI single-file
  image-to-3D port of `speridlabs/idol` (resolves 11-01's "unverified" flag) —
  **NO ADOPT** (no 3D in our pipeline); note for future 3D/turnaround-table
  work <https://huggingface.co/Comfy-Org/Idol>
- **AtomicChat/LFM3-1.7B-Uncensored-GGUF (178 likes, 46k dl)** — small
  uncensored agent-LLM GGUF — utility-tier option only (marginal)
  <https://huggingface.co/AtomicChat/LFM3-1.7B-Uncensored-GGUF>
- **DeepSeek open-sourced a super-agent coding prototype: "one Router, many
  Workers, minimal human attention" (7u, r/artificial)** — agent architecture
  (router/worker) — read for our DSH/writer pipeline context
  <https://www.reddit.com/r/artificial/comments/1xlc9ye/>
- **Open Jutsu Studio — put your characters into real footage, keep going (23u,
  ComfyUI sub)** — character-into-live-footage compositing — adjacent to
  charswapmask/SAM3 region work <https://www.reddit.com/r/ComfyUI/comments/1xjette/>
- **Higgsfield chatter: "why am I seeing so many Higgsfield" (29u)** +
  "Updated Minimax Music Video Workflow" (122u) — Body Double context (our
  open-source-higgsfield setup pending) · D041 note: music-video workflow
  pattern ≠ our no-music rule — watch only
  <https://www.reddit.com/r/ComfyUI/comments/1xjmrh4/>
- **Hardware cluster continues (no action for our 5090):** "Don't people pay
  attention anymore when buying hardware for AI?" (311u)
  <https://www.reddit.com/r/LocalLLaMA/comments/1xl4ckr/dont_people_pay_attention_anymore_when_buying/>
  · "Coding is solved* (exclusions apply)" (316u)
  <https://www.reddit.com/r/LocalLLaMA/comments/1xl90rr/coding_is_solved_exclusions_apply/>
  · "I'm just laughing at Fal" (137u — fal.ai pricing)
  <https://www.reddit.com/r/StableDiffusion/comments/1xjkajg/im_just_laughing_at_fal/>
  · PCB shortage (302u — carried 11-01)
  <https://wccftech.com/ai-boom-triggers-massive-pcb-shortage-with-orders-booked-until-2030/>
- **Krea 2 vs MiniMax H3 text-encoder comparison — "what impact do abliterated
  text encoders really have?" (112u)** — TE ablation data for our exact rig
  (Krea2 + H3) — read for prompt-expansion quality trade-offs
  <https://www.reddit.com/r/StableDiffusion/comments/1xicnjs/krea_2_and_minimax_h3_text_encoder_comparison/>
- **MOSS (user opted out of checking — noted, not chased):** "Moss image edit
  vs Fibo-2.0-edit" (114u) <https://www.reddit.com/gallery/1xg526w>
- **Unidentified media posts (no titles captured in today's HTML tier —
  honest gap):** t3_1xklq96 (316u) <https://www.reddit.com/gallery/1xklq96> ·
  t3_1xk5m1s "Try this workflow, too." (88u)
  <https://v.redd.it/vfmusamesryh1>

**ACTION ITEMS (new today):**
1. **SenseNova 6.8 Code2Video (99u)** — evaluate as an alternative/complement
   video route (code-driven + NL editing) — H3 video routes.
2. **ZenTrainer (134u)** — inspect for future character-LoRA runs (live
   previews); keep AI-Toolkit krea2 recipe as primary.
3. **KreaMossMix workflow (100u)** — inspect for the Krea2 sheet chain.
4. **Sulphur-3** — watch for the release (Krea2-alternative pool).
5. **burner22/numbat — DO NOT DOWNLOAD** (RNG-tensor audit) — record as hoax
   signal; warn user if it re-surfaces.
6. **DeepSeek super-agent prototype (7u)** — read for router/worker agent
   architecture (DSH/writer context).
7. Carried (11-01): H3 "tiny sliders" workflow test · Betelgeuse bit-exact
   Flash-Next recipe A/B · DFlash2 GGUF A/B · FastH3 sheet workflow ·
   LayerShop Regions · Pika H3-Flex ADOPT · Audio8-TTS-0.6b narration
   evaluation (D041) · llama.cpp CVE-2026-116096 · X cookies deprioritized.

**SOURCE FAILURES (tier status per D203):** Reddit JSON 403 all subs (HTML tier
carried — 33 items 50+ today) · ComfyUI sub: 0 posts at 50+ (top ≈ 29u — not a
failure, genuinely quiet) · Civitai PARTIAL — hot category only;
ComfyWorkflow/new-LoRA categories returned nothing (treat as partial, NOT
verified-zero) · X — 3 of 7 accounts captured nothing this run (same 3 as
11-01); backfill-dominated capture = low-signal day, not a fetch failure ·
HF ✅ (6 trending models + 4 datasets; top-downloads returned 0 rows).

## 2026-11-01

**Sources:** Reddit ✅ HTML tier (32 new items — artificial 11 / LocalLLaMA 8 / StableDiffusion 7 /
ComfyUI 6; JSON 403 on all subs as usual) · HF ✅ 5 trending models + 3 datasets + 1 top-download ·
Civitai ⚠️ PARTIAL — only 1 item captured today (hot: DreamShaper XL re-trending); no ComfyWorkflow /
new-LoRA captures · X ✅ **tier-3 browser RECOVERED** (anonymous profile pages rendered with full
metadata — `X_AUTH_TOKEN`/`X_CT0` still NOT set) — 99 items from 4 of 7 tracked accounts (MaxLiu09,
PixelAigc, akatz_ai, xieenze_jr; no capture for BennyDaBall_OG / Alissonerdx / diodiogod); 96 of 99
are 2024–25 timeline backfill, only 3 posts dated 2026-10.
**Pipeline note:** 08:00 schtask clean — log `fetch: 104 new items` + `done`, LastTaskResult 0 — no
re-run needed.

**New relevant items (vs 10-31 baseline):**
- **Betelgeuse: Qwen 3.8 Flash Next @ 22 tok/s sustained (spiking 48) on RTX 3060 12 GB + 16 GB
  DDR4, "100% bit-exact" (413u)** — new memory/offload recipe for our Qwen 3.8 family (agent/writer
  LLMs) — GPU+VRAM-tricks candidate, bit-exact claim is checkable
  <https://v.redd.it/lnqnbp15nsyh1>
- **Tiny sliders for MiniMax H3 — control motion/emotion "without training a LoRA" [ComfyUI] (137u)**
  — no-LoRA H3 control layer; complements our Krea2 char-LoRA + sheet pipeline (H3 video routes)
  <https://v.redd.it/6snf3fm9zoyh1>
- **FastH3 + ComfyUI: short anime scene from character sheets (45u)** — sheet → H3 scene, exactly
  our Krea2 reference-sheet → H3 pattern (Krea2 reference sheets / H3 video routes)
  <https://v.redd.it/4ysutygq1qyh1>
- **LayerShop update: now with Regions (50u)** — region-scoped layer editing — candidate for
  charswapmask/SAM3 character-region edits <https://v.redd.it/g62bzjf6vtyh1>
- **MINIMAX H3 4K (180u)** — H3 4K output route — follow-up on the carried H3-Hires item
  <https://v.redd.it/o8io2bvvtqyh1>
- **Blender previsualization with MiniMax H3 (38u)** — Blender camera-blocking → H3 render (H3 video
  routes / previz) <https://v.redd.it/akqdv3440wyh1>
- **H3 Morphing (23u)** — H3 morphing feature (H3 video routes) <https://v.redd.it/8h3phdx23myh1>
- **PSA: DFlash2 GGUF for Qwen 3.8 Flash Next, +17% avg (131u)** — quant upgrade for our LLM family
  (writer+agent LLMs + llama.cpp) <https://huggingface.co/nazeshinjite/Qwen3.8-Flash-Next-DFlash2-GGUF/>
- **Pika H3 "Flexing its muscles" (24u)** — community demo of Pika-H3-Flex (10-31's TOP ADOPT
  candidate — compare against our kitchen run) <https://v.redd.it/b02yf82u5qyh1>
- **vLLM PLE disk offload on nightly (167u)** — disk-offload path for large models (GPU+VRAM
  tricks; we run llama.cpp — informational) <https://github.com/vllm-project/vllm/pull/59958>
- **Edge0/Audio8-TTS-Realistic-0.6b — HF trending (163 likes, 2.7k dl)** — small realistic TTS,
  runs locally — narration-voice option (D041: audio stays ambient-only for music; a narration
  voice ≠ music) <https://huggingface.co/Edge0/Audio8-TTS-Realistic-0.6b>
- **speridlabs/idol — HF trending (214 likes, 2.4k dl)** — no description in capture — unverified,
  low priority <https://huggingface.co/speridlabs/idol>
- **X — @PixelAigc (195 likes, 10-31): how super-long AI videos (1300 s / 640 s / 500 s / 1010 s)
  get made — multi-minute generation method** — long-form video route (H3 video routes)
  <https://x.com/PixelAigc/status/2116511077202833801>
- **X — @MaxLiu09 (4994 likes, 10-12): "made an open-source one that does the same thing" +
  Blender extension** — capture carries only t.co short links — verify what it is before acting
  <https://x.com/MaxLiu09/status/2109530569566744620> · **@MaxLiu09 (10-12): Motion2MixamoRig
  passes 200 GitHub stars** — motion → Mixamo rigging — marginal for our H3-video pipeline —
  **NO ADOPT** <https://x.com/MaxLiu09/status/2109689869312377094>
- **Civitai — DreamShaper XL re-trending (hot, 639k dl)** — old SDXL checkpoint — **NO ADOPT**
  (we anchor on Krea2 / H3 / Qwen Image, not SDXL) <https://civitai.com/models/112902> · no new
  ComfyWorkflow/LoRA captures today (partial fetch — see Sources).
- **GPU/hardware cluster (market):** PCB shortage, orders booked until 2030 (262u)
  <https://wccftech.com/ai-boom-triggers-massive-pcb-shortage-with-orders-booked-until-2030/> ·
  AMD November Radeon GPU + GDDR6 price increase (141u)
  <https://videocardz.com/newz/amd-reportedly-plans-another-radeon-gpu-and-gddr6-price-increase-in-november>
  · "Guys I think I found our GPUs" (Business Insider, 138u)
  <https://www.linkedin.com/posts/businessinsider_the-ai-boom-is-facing-a-new-phenomenon-heaps-activity-7521314592090705920-K6m8>
  — continuation of the 10-31 5090 supply cluster; no action for our 5090.
- **LLM chatter:** "spent a lot on my rig but I can only run Gemma 4" (138u — our writer-model
  family) <https://www.reddit.com/r/LocalLLaMA/comments/1xkcyn6/spent_a_lot_on_my_rig_but_i_can_only_run_gemma_4/>
  · **Koboldcpp v1.124 released** (llama.cpp fork; we run llama.cpp directly — informational)
  <https://github.com/LostRuins/koboldcpp/releases/tag/v1.124> · "What happens once China stops
  providing free, OSS models?" (172u) <https://i.redd.it/npcf6t3r3vyh1.png> · one-person studio
  ships a 12-chapter FPS coded by AI agents in 20 days (26u — agent-LLM capability context)
  <https://www.reddit.com/r/artificial/comments/1xikfco/a_oneperson_studio_shipped_a_steam_demo_of_a/>
  · **Qwen Image 2.1** anime-cosplay gallery (132u — new Qwen-image version; we anchor
  qwen_image VAE / Krea2 — informational) <https://www.reddit.com/gallery/1xj4hfm>
- **MOSS (user opted out of checking):** MOSS-Image-Base + 8-steps-dmd2 6mp examples (122u)
  <https://www.reddit.com/gallery/1xjmxyo> · Ostris training MOSS Image on Primal VAE — "4K images
  at 1080p compute cost" (123u — follow-up on the 10-31 Primal VAE note)
  <https://www.reddit.com/r/StableDiffusion/comments/1xkb7ay/ostris_is_training_moss_image_to_use_primal_vae/>
  — noted, not chased.
- **HF datasets (marginal):** ccore/ThreeJS-3D-Scenes (4,146 3D scenes + prompts + thinking
  traces) <https://huggingface.co/ccore/ThreeJS-3D-Scenes> · codepawl/simready-glb (2,595 CC-BY
  GLB models) <https://huggingface.co/codepawl/simready-glb> — 3D asset/scene data for previz —
  no action for now.

**ACTION ITEMS (new today):**
1. **H3 "tiny sliders" (no-LoRA motion/emotion control)** — find the workflow/nodes; test with our
   Krea2 character sheets (H3 video routes). TOP new H3 item.
2. **Betelgeuse bit-exact Flash Next recipe (413u)** — read the post, identify the quant/offload
   method; A/B in a SEPARATE slot (never replace the live brain without user OK).
3. **DFlash2 GGUF (nazeshinjite, +17% avg)** — A/B candidate for our Qwen 3.8 Flash Next setup.
4. **FastH3 character-sheet workflow (45u)** — inspect for our sheet → H3 scene pipeline.
5. **LayerShop "Regions" update** — check the node for charswapmask/SAM3 region edits.
6. **Pika H3 community demo (24u)** — compare against our 66.86 s kitchen run; continue 10-31 TOP
   ADOPT (official `comfy/loras/` BF16 weights + workflows).
7. **Edge0/Audio8-TTS-Realistic-0.6b** — evaluate local narration (D041: ambient-only music rule;
   narration voice is OK).
8. Carried: X cookies (`X_AUTH_TOKEN`/`X_CT0`) — tier worked anonymously today, so deprioritized
   · H3 4K / Relay Hires reads · LTX-2.5 A/B · Gemma-4-31B-Humanlike-Chat writer test · llama.cpp
   CVE-2026-116096.

**SOURCE FAILURES (tier status per D203):** X — tier-3 browser **recovered** today (anonymous
profile pages rendered with full metadata; `X_AUTH_TOKEN`/`X_CT0` still unset — cookies now a
nice-to-have, not required); 3 of 7 tracked accounts (BennyDaBall_OG, Alissonerdx, diodiogod)
captured nothing this run. Reddit JSON 403 on all subs (HTML tier carried — 32 new items today).
Civitai — PARTIAL: only 1 item captured today (hot DreamShaper XL); ComfyWorkflow/new-LoRA
categories returned nothing — treat as partial fetch, NOT a verified zero-new day. HF ✅ (5
trending models + 3 datasets + 1 top-download).

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

## 2026-11-11

**Sources (3-day catch-up — PC off/asleep 11-09/11-10 + 11-11 08:00 miss; manual run 11-11 ~17:25 IST):** `daily.py --news-only` clean (exit 0). Reddit ✅ HTML tier (SD 23 / LocalLLaMA 21 / ComfyUI 25 / artificial 25; JSON 403 all subs as usual) · HF ✅ 17 trending + 12 datasets + 3 downloads · Civitai: hot 1 + ComfyWorkflows 1 + newest/new-LoRAs 0 · X ✅ **6 of 7 accounts via browser-head tier — 55 posts, ZERO walls** (Alissonerdx absent; MaxLiu09 backfill-dominated, old 2024 IDs). Store 2258 items, 183 newly indexed.

**New relevant items (vs 11-08 baseline):**

*H3 / movie pipeline (the big ones):*
- **t3_1xsj747 (199u, 11-10) — "H3 Editor: a timeline video editor for MiniMax H3 inside ComfyUI — you write shots instead of wiring graphs" (open source, GPL-3.0)** — shot-based H3 timeline = a movie-assembly layer above our R2V workflows — TOP ADOPT candidate <https://www.reddit.com/r/stablediffusion/comments/1xsj747/h3_editor_a_timeline_video_editor_for_minimax_h3/>
- **MiniMax H3-Image open weights + native ComfyUI day-0 support (11-10 cluster)** — "H3-Image is now available with open weights!" <https://i.redd.it/u421wox54t0i1.jpeg> · "MiniMax-H3-Image in ComfyUI!" <https://i.redd.it/qde2u57mjt0i1.png> · "natively supported in ComfyUI on day-0" <https://v.redd.it/o37u7zutct0i1> · "H3 Image 20MP Workflow" <https://www.reddit.com/gallery/1xt9ocv> · "300 random prompts across styles" bench <https://jo-nike.github.io/h3-image-bench/> — HF: `MiniMaxAI/MiniMax-H3-Image` (11-03, 143K dl) + `MiniMaxAI/MiniMax-H3-Image-PE` (11-08) + `Comfy-Org/MiniMax-H3-Image` (352K dl) — the official H3 IMAGE model + PE variant — ADOPT candidate (H3 image chain / Krea2 alternative pool) <https://huggingface.co/MiniMaxAI/MiniMax-H3-Image>
- **"pi-H3: 2–4 Steps Without a VAE Decoder — will be released Nov 16" (11-11, 103u)** — the carried 11-05 P-H3-Image-Comfy item now has a release date; HF `PrunaAI/P-H3-Image-Comfy` trending — WATCH (Nov 16) <https://hanshengchen.com/blog/pi-h3/>
- **"ReCaVSR — one-step streaming video super-resolution built on Wan2.2" (11-10, 19u)** — upscaling cluster (alongside SeedVR2/FlashVSR/RelayVSR) <https://v.redd.it/xb5gv8b01t0i1>
- **"Fixing MiniMax H3 Video Upscaling details loss with RelayVSR & DLSS5 Nodes with only 6 GB VRAM" (11-10, 21u)** — H3-output upscaling on low VRAM; HF `Comfy-Org/RelayVSR` (11-05, 91K dl) <https://v.redd.it/qlsbz3oi6s0i1>
- **"Super Huge Update for Minimax H3 Temporal Spatial Node" (11-06, 172u)** — H3 temporal-spatial node update <https://i.redd.it/75z8gwfuzyzh1.png>
- **t3_1xq3fiz (11-07, 14u) — "MiniMax H3 running locally on an RTX 5060 Ti 16GB"** — low-VRAM H3 recipe (backup path for our 32 GB 5090) <https://www.reddit.com/r/comfyui/comments/1xq3fiz/minimax_h3_running_locally_on_an_rtx_5060_ti_16gb/>
- **"MOSS-Image-SFT control LoRAs — pose, depth, canny and the rest" (11-10, 196u)** + MOSS roundups 6th/7th/10th Nov <https://www.reddit.com/r/comfyui/comments/1xp4q0c/a_quick_mossimage_news_roundup_6th_november_2026/> · <https://www.reddit.com/r/comfyui/comments/1xq7gbc/a_quick_mossimage_news_roundup_7th_november_2026/> · <https://www.reddit.com/r/comfyui/comments/1xsmt6h/a_quick_mossimage_news_roundup_10th_november_2026/> + "Moss SFT INT8-convrot is just fine" (11-07, 112u) + "Moss training speed boost in Fizgig" (11-08, 163u) — MOSS control-LoRA cluster (pose/depth/canny = character-sheet control) <https://www.reddit.com/gallery/1xsh4xq>
- **"Kandinsky S2V 1.0 — 2B and 21B models" (11-04, 100u)** — new open video model (t2v pool alongside H3/LTX) <https://v.redd.it/6160glrp1nzh1>
- **"[Model Release] Qwen-Image-2.1 Uncensored Omni — ~1M images, 9 local formats" (11-05, 165u)** — our Krea2 base family (Qwen-Image-2.1) <https://www.reddit.com/gallery/1xotduk>
- **t3_1xsysy3 (11-10, 31u) — "Open Source Higgsfield results are out"** + HF `Viggle/Viggle-Remake` trending — the Higgsfield "Miracle" remake model open-sourced (character motion/remake) <https://www.reddit.com/r/comfyui/comments/1xsysy3/open_source_higgsfield_results_are_out_congrats/>
- **"[Papers] LTX-Video: Realtime Video Latent Diffusion" (11-09, 97u)** — LTX cluster (VFX pipeline org) <https://www.reddit.com/gallery/1xs5io9>
- **"Hybrid Pipeline Test: audio from MiniMax H3 + visuals from Nano Banana 2, edited in DaVinci Resolve" (11-10, 4u)** — external validation of OUR exact pipeline shape (H3 audio + stills + Resolve assembly, no music — D041) <https://v.redd.it/hctc3bst5v0i1>
- **"SolordZ_Realism_Moss_Base — realism-focused version" (11-10, 119u)** — MOSS realism base <https://www.reddit.com/gallery/1xsqrzv>
- **HF trending (new):** `VideoRebirthAI/hyperflow-h3-flash` (H3 flash variant — H3 cluster) · `mradermacher/gemma-4-31B-it-ARA-heretic-GGUF` (writer pool — our writer is Gemma4-31B) · `mradermacher` + `xtools-at` DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic GGUFs (brain/agent merges) · `baidu/ERNIE-5.5-Flash-Base` + `moonshotai/Kimi-K3.1-Pro` (brain pool) <https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash>

*Brain / hardware:*
- **t3_1xs7ffm (11-09, 200u) — "Same prompt, DeepSeek V4.1 Flash vs Qwen 3.8 FN: 94 tok/s vs 350 tok/s"** — our brain family's speed context <https://www.reddit.com/r/LocalLLaMA/comments/1xs7ffm/same_prompt_deepseek_v41_flash_vs_qwen_38_fn_94/>
- **`tencent/Qwen3.8-27B-DSpine-b16` (11-08, 287u)** — Qwen3.8-27B DSpine (sparse) variant — brain cluster <https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16>
- **"NVIDIA reportedly cancels GeForce RTX 5080 24GB launch, brings back 16GB over GDDR7 costs" (11-11, 209u)** — hardware news — don't buy now (we have the 5090) <https://videocardz.com/newz/nvidia-reportedly-cancels-geforce-rtx-5080-24gb-launch-brings-back-16gb-model-over-gddr7-costs>
- **"Intel Arc Pro B70 32GB ($1,299) vs RTX 5090 ($6,500+) on Qwen3.8-27B: about 1/2 speed gen" (11-08, 179u)** — cheaper-alternative context <https://www.reddit.com/gallery/1xr78s5>
- **"Microsoft patent: paying you to train AI on your idle GPU" (11-10, 8u)** + **"US takes Nvidia CEO affair public" (11-10, 267u)** — context only <https://www.techspot.com/news/114499-microsoft-patent-describes-paying-you-train-ai-idle.html> · <https://www.reddit.com/r/LocalLLaMA/comments/1xsljn6/nobody_wondering_why_the_us_takes_nvidia_ceo/>

*Civitai:*
- LTX 2.5 low-VRAM 2K/3K workflow (2877939) reappears, 1,176 dl (up from 1,136) — carried ADOPT-candidate (eval) <https://civitai.com/models/2877939> · DreamShaper XL hot — known NO-ADOPT <https://civitai.com/models/112902>

*X:* 6 of 7 accounts readable (BennyDaBall_OG 6, xieenze_jr 6, PixelAigc 6, diodiogod 5, akatz_ai 7, MaxLiu09 25 — backfill-dominated old 2024 IDs; Alissonerdx absent) — 55 posts, ZERO walls; all image-only (no text bodies captured this run) — consistent with the 11-08 art-account pattern.

**ACTION ITEMS (new):**
1. t3_1xsj747 — H3 Editor (shot-based H3 timeline editor, GPL-3.0) — inspect for movie assembly (TOP item)
2. MiniMax H3-Image open weights + native ComfyUI day-0 — ADOPT candidate (H3 image chain / Krea2 alternative pool)
3. pi-H3 (release Nov 16) — calendar it; inspect `PrunaAI/P-H3-Image-Comfy` at release (carried 11-05)
4. ReCaVSR + RelayVSR/DLSS5 — H3-output upscaling options (alongside carried SeedVR2/FlashVSR)
5. MOSS-Image control LoRAs (pose/depth/canny) — character-sheet control route
6. Kandinsky S2V 1.0 (2B/21B) — t2v pool eval
7. Viggle-Remake open weights — character motion/remake
8. t3_1xs7ffm — DeepSeek V4.1 Flash vs Qwen 3.8 FN speed read (brain)
9. Hardware (5080 24GB cancelled / Arc Pro B70 $1,299) — don't buy now
10. Carried from 11-08: KV-cache quant Qwen3.8 27B READ · TurboH3 FL2VA i2va ADOPT-candidate · Krea2 Turbo 133K check · H3 KSampler speedup A/B · LTX 2.5 low-VRAM inspect · Fizgig v9.0.4 · 0.1B embeddings (RAG) · MoE CPU-offload PR · unsloth Flash-Next V3.1 A/B · Krea 3 tech report · H3 image-edit workflow · gemma4 PR #31356 · Hy4 · H3 tiny sliders A/B · Strata 20× patch

**SOURCE FAILURES:** 08:00 schtask missed on 11-09/11-10/11-11 (PC off/asleep — LastRunTime still 11-08 08:52, Result 2147946720) → manual `daily.py --news-only` clean (store 2258, 183 newly indexed) · Reddit JSON 403 all subs (expected tier-1 noise — HTML tier carried 94 posts) · r/comfyui_workflows HTML tier GATED (day 17) · X — NO walls (6 of 7 accounts via browser-head; Alissonerdx absent; all image-only) · Civitai newest/new-LoRAs = 0 (partial — NOT verified-zero).

## 2026-11-08

**Sources (3-day catch-up — machine down 11-06/11-07/11-08, power outage):** 08:00 schtask
fired at 08:52 post-boot but FAILED (Result 2147946720, no log) → manual re-run, clean.
Reddit ✅ HTML tier (SD 21 new / LocalLLaMA 28 / ComfyUI 21 / artificial 50; 49 posts at
50+; JSON 403 all subs as usual) · HF ✅ 14 trending + **3 top-downloads (API quirk
RESOLVED after ~4 days of 0 rows)** + 10 datasets · Civitai: hot 1 (DreamShaper XL,
known) + ComfyWorkflows 1 (LTX 2.5 low-VRAM) + newest/LoRAs 0 · X ✅ **ALL 7 ACCOUNTS
via browser-head tier — 41 posts, ZERO walls** (first full X run since the 11-05 cookie
unlock; latest posts mostly image-only art; text parsing verified live 11/11 with-text).
Store 2075 items, 190 newly indexed.

**New relevant items (vs 11-05 baseline):**

*Brain / agent toolchain (our exact model family):*
- **t3_1xqbesv (135u) — "Effects of KV Cache Quantization on Qwen3.8 27B"** — KV-cache
  quant for OUR exact brain model — READ for brain speed/VRAM tuning <https://www.reddit.com/r/LocalLLaMA/comments/1xqbesv/effects_of_kv_cache_quantization_on_qwen38_27b/>
- **t3_1xqacka (195u) — llama.cpp PR #30966 "llama_moe_cache: run missed experts on CPU + tuning script"** —
  MoE CPU offload in our toolchain (carried brain-toolchain cluster) <https://github.com/ggml-org/llama.cpp/pull/30966>
- **t3_1xo3ikc (161u) — "What are you looking forward to in Qwen 4?"** — next-gen expectations
  for our brain family <https://www.reddit.com/r/LocalLLaMA/comments/1xo3ikc/what_are_you_looking_forward_to_in_qwen_4/>
- **t3_1xp9jt1 (431u) — "Latest Open-Source Labs are gutting away cybersecurity and reverse-engineering
  capabilities"** — day's top post (context) <https://i.redd.it/e9368ci3yyzh1.png>
- **award_wow_2 (268u) — NousResearch/Arete-27B (Qwen finetune)** — new 27B brain-pool candidate
  <https://huggingface.co/NousResearch/Arete-27B>
- **t3_1xnu6y1 (121u) — "Kimi K3.1 is probably benchmaxxed (with some evidence)"** — context for the
  carried Kimi-K3.1-Pro <https://i.redd.it/24084yfbrmzh1.png>
- **t3_1xpvfx8 (230u) — "Harness Leaderboard — Kimi Code, Hermes, Pi, Claude Code, Codex vs Terminal
  Bench 2.1"** — agent-harness class (= our DSH) <https://huggingface.co/spaces/joelniklaus/harness-leaderboard>
- **t3_1xpm8mw (237u) — "Mirage: a 22 MB VLM (scene descriptions + detection + OCR + segmentation +
  spatial relations, single pass)"** — tiny VLM (RAG/VLM context) <https://www.reddit.com/gallery/1xpm8mw>
- **t3_1xpdk0i (180u) — "A 0.1B model just killed 8B embedding models… I tried it out"** — tiny
  embeddings — RAG upgrade path over our MiniLM-384d <https://www.reddit.com/gallery/1xpdk0i>
- **t3_1xntou1 (163u) — "LFM3-Omni-2B fully offline on iPhone 18 Pro Max at ~80 tok/s (WebGPU)"** —
  edge-LLM context <https://v.redd.it/vrc0vshunmzh1>
- **t3_1xobe4h (361u) — "CCORE GLB-3D-Coder 4B final model + full weights"** (+ **t3_1xozbe6 (177u)** —
  3,918-example dataset) — 3D codegen (not our niche; pool context) <https://v.redd.it/5ya4a2v5fqzh1> · <https://i.redd.it/ulne0ine2wzh1.jpeg>
- **t3_1xp32od (196u) — "Introducing Inkling 2 Small" (Thinking Machines)** — model-pool context
  <https://thinkingmachines.ai/news/inkling-2-small/>
- **t3_1xqd058 (277u) — "Use your phone to monitor anything with local models — 100% local agent
  (iOS/Android)"** — local-agent context <https://v.redd.it/g80qnydhc80i1>

*Krea2 / H3 (movie pipeline):*
- **t3_1xo3pjo (91u) — Kijai MiniMax-H3_comfy: new TurboH3 FL2VA pruned INT8 ConvRot (i2va)** —
  H3 image-to-VIDEO for our movie i2v chain (pairs with carried H3 tiny sliders) — ADOPT candidate
  <https://huggingface.co/Kijai/MiniMax-H3_comfy/blob/main/diffusion_models/minimax_h3_fl2va_turboh3_i2va_pruned_int8_convrot.safetensors>
- **t3_1xmuea8 (90u) — "SPEEDing up more than just MiniMax-H3 without retraining — drop-in KSampler
  replacement for image, edit, and video"** — H3 speed-up, drop-in — A/B candidate
  <https://www.reddit.com/r/StableDiffusion/comments/1xmuea8/speeding_up_more_than_just_minimaxh3_without/>
- **t3_1xohwh5 (142u) — "Krea 2 Turbo — 4 Step LoRA comeback (trained to 133K checkpoint, ~55K more
  than the 'final' 78K in Sep)"** — the 10-26 carried turbo-LoRA item, retrained further —
  reference-sheet speed-up candidate <https://www.reddit.com/gallery/1xohwh5>
- **t3_1xllwpg (84u) — "Easier Poses Ref2V MM-H3 — Semi-Transparent Canny"** — pose control for
  character shots <https://v.redd.it/167z4b5544zh1>
- **t3_1xqfcjs (87u) — "Ultima Online (6 min) made with MiniMax H3 in ComfyUI on a single 24 GB GPU"** —
  H3 long-form on 24 GB <https://v.redd.it/uj6rbctsw80i1>
- **t3_1xpz5ti (107u) — "Rebuilt Higgsfield's 'Miracle' demo edit-by-edit with Viggle-remake"** —
  video-editing context <https://v.redd.it/7aztbitmr40i1>
- **t3_1xo18u8 (91u) — Fizgig v9.0.4: Fibo 2.0 training, Z-Image Base, masks from SAM 3.1, Detail
  crops** — our LoRA-training GUI update; SAM 3.1 masks = charswapmask chain
  <https://github.com/shootthesound/Fizgig/releases/tag/v9.0.4>
- **ComfyUI sub (sub-50):** t3_1xlbcpn (17u) — "ComfyUI-skkut-utils: 1400+ Visual Krea 2 Style
  Selector" — Krea2 style picker for our pipeline <https://www.reddit.com/gallery/1xlbcpn> ·
  t3_1xlu284 (15u) — "SeedVR2 vs Open-H3 vs FlashVSR+ Turbo 4K upscale — actual tests on RTX 5090" —
  our upscaling route <https://www.youtube.com/watch?v=27kdYJlOONA> · t3_1xoc3tv (20u) — "H3
  Singularity V2 on 12 GB 3060, 4-step up to 2336×1312" — H3 low-VRAM <https://v.redd.it/s82p1ykxrqzh1>
  · t3_1xqasyo (14u) — FilmDateStamp: optical burn-in + emulsion halation node — film look for the
  movie <https://www.reddit.com/gallery/1xqasyo> · t3_1xmukz1 (18u) — prompt enhancer running a small
  local LLM without permanent VRAM <https://i.redd.it/pqqnho27sezh1.png> · t3_1xodw5i (14u) — low-VRAM
  upscaler <https://www.reddit.com/gallery/1xodw5i>

*Hardware (continues the 11-04 PCB-shortage cluster — DON'T BUY NOW):*
- **t3_1xojryw (268u) — "NVIDIA RTX PRO 5500 Blackwell appears at $17,999 MSRP (higher than RTX PRO
  6000's $16,000)"** <https://videocardz.com/newz/nvidia-rtx-pro-5500-blackwell-appears-at-17999-msrp-higher-than-rtx-pro-6000>
- **t3_1xmgmd8 (129u) — "RTX 8000 48GB prices decreased over last 2 years, while 3090 prices doubled"**
  <https://www.reddit.com/r/LocalLLaMA/comments/1xmgmd8/rtx_8000_48gb_prices_have_decreased_over_the_last/>
- **t3_1xn40w7 (154u) — "World's biggest PCIe GPU — 4-GPU AMD prototype pictured"**
  <https://videocardz.com/newz/worlds-biggest-pcie-graphics-card-discovered-prototype-amd-radeon-rx-470-board-with-four-gpus-has-been-pictured>

*Civitai:*
- **(comfyworkflows) "LTX 2.5 — Pure 2K/3K Ultra-Low VRAM (Universal Workflow)"** (1,136 dl) — low-VRAM
  LTX 2.5 route — ADOPT-CANDIDATE (eval): LTX = our weekly-watch org; universal 2K/3K low-VRAM
  workflow = alternative video route alongside H3 <https://civitai.com/models/2877939>
- **(hot) DreamShaper XL** (Lykon, 640k dl) — known NO-ADOPT <https://civitai.com/models/112902>

*HF:*
- **Top-downloads BACK (3 rows after ~4 days of 0):** microsoft/Florence-2-base (10.09M dl) ·
  Comfy-Org/Wan-2.2 (9.90M) · Comfy-Org/Z-Image-Turbo (9.69M) — API quirk resolved
  <https://huggingface.co/microsoft/Florence-2-base>
- **NEW trending:** NousResearch/Arete-27B (220) · webAI-Official/TwIL-8B (215) ·
  ccore/Qwen3.5-4B-GLB-3D-Coder (260) · xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic (528)
  · openvivo/BluePixel-Turbo (native 4K instruction-based edit, 4 steps) <https://huggingface.co/openvivo/BluePixel-Turbo>
- **Carried + RISING:** Qwen-Image-2.1-Turbo-Quantized 5713 · Kimi-K3.1-Pro 1643 (up from 574) ·
  unsloth Flash-Next 1.42M dl · idol 1139 · Sulphur-3 405 · numbat 381 (DO-NOT-DOWNLOAD) · AtomicChat
  1017 117k dl · Ripple-65B 376 · OBLITERATUS 275 · P-H3-Image-Comfy 233
- **Datasets:** ccore/ThreeJS-3D-Scenes + codepawl GLB-3D sets (abo/scanned-objects/simready) — 3D
  asset cluster · tencent/TailorRig · NousResearch arete-data-pairs / Propaganda_Eval

*X:* all 7 accounts readable (41 posts) — first full X tier since the 11-05 cookie unlock; latest
posts mostly image-only (art accounts); text parsing verified (11/11 with-text on the older
timeline). No new relevant TEXT posts in this window.

**ACTION ITEMS (new):**
1. t3_1xqbesv — KV-cache quant for Qwen3.8 27B — READ (our exact brain model)
2. t3_1xo3pjo — TurboH3 FL2VA i2va pruned INT8 ConvRot — ADOPT candidate (movie i2v chain)
3. t3_1xohwh5 — Krea2 Turbo 4-step LoRA retrained to 133K — check the new checkpoint (carried 10-26)
4. t3_1xmuea8 — drop-in KSampler H3 speed-up — A/B candidate
5. Civitai LTX 2.5 ultra-low-VRAM 2K/3K workflow — inspect (alternative video route)
6. t3_1xo18u8 — Fizgig v9.0.4 (SAM 3.1 masks + Fibo 2.0 training) — LoRA-training GUI update
7. t3_1xpdk0i — 0.1B embedding model — RAG upgrade path over MiniLM-384d
8. t3_1xqacka — llama.cpp MoE CPU-offload PR #30966 — brain toolchain
9. Hardware cluster (RTX PRO 5500 at $17,999) — don't buy now
10. Carried: unsloth Flash-Next V3.1 A/B (brain) · Krea 3 tech report · H3 image-edit workflow · gemma4
    PR #31356 · Hy4 watch · H3 tiny sliders A/B · Krea2/H3 text-encoder comparison · Strata 20× patch
    · P-H3-Image-Comfy

**SOURCE FAILURES:** 08:00 schtask fired 08:52 (post-boot) but FAILED (Result 2147946720; no 11-08
log) → manual re-run clean (~45min; 3-day catch-up; store 2075) · Reddit JSON 403 all subs (expected
tier-1 noise — HTML tier carried 49 at 50+) · r/comfyui_workflows HTML tier GATED (day 13) · X — NO
failures (all 7 accounts via browser-head tier — login wall down since 11-05) · Civitai newest/new
LoRAs = 0 new (partial — NOT verified-zero) · HF top-downloads RESOLVED (3 rows).
