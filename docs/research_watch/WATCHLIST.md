# Research WATCHLIST — canonical source of truth (created 2026-11-17)

**Why this file exists:** the lab-org list previously lived only in weekly-report
headers + agent process memory. Orgs that became relevant OFF that list
silently never got watched — proven gap 2026-11-17: `meituan-longcat`
(30 models incl. LongCat-Video-Avatar-1.6, an audio-driven avatar-video model
directly relevant to our dialogue-shot route) was never on any weekly list.
**Rule: the weekly run MUST read this file first — never re-derive the list
from memory. Any org that produces an ADOPT candidate, or that the user
mentions, is added here IN THE SAME TURN (D131 commit).**

## HF lab orgs (weekly diff via `api/models?author=<org>&sort=lastModified`, web_fetch tier)

| Org | Relevance to our project | Added |
|---|---|---|
| `Qwen` | brain family (D225: dense 27B-class = the correct upgrade) + `Qwen-Image-2.1` = Krea2 base + PAN2's qwen3.5_9b encoder | original |
| `MiniMaxAI` | H3 image/video stack (our video runtime) | original |
| `Krea` / `KreaAI` | Krea2 image stack (both names probed — orgs return zero public HF models; Krea2 lives under Qwen) | original |
| `black-forest-labs` | FLUX3 gate (user: HF token + Agree at `flux-3-image-klein-comfy`) | original |
| `meta-llama` | Llama brain family | original |
| `stabilityai` | image/video pool | original |
| `mistralai` | brain pool | original |
| `deepseek-ai` | brain family (V4.1-Flash vs Qwen FN threads) | original |
| `facebook` | meta-encoder etc. (RAG-tier candidates) | original |
| `fishaudio` | D041 drama-3 output-class check (audio tier) | original |
| `Comfy-Org` | single-file ports (MiniMax-H3 33.3M dl, H3-Image, PAN2, MOSS-Image) — our runtime ports land here | original |
| `Lightricks` | LTX-2 family — `VFX_PIPELINE_LTX25.md` timeline diff (base checkpoint still not dropped as of 11-17) | original (LTX scope) |
| **`meituan-longcat`** | **LongCat ecosystem: `LongCat-Video` (T2V/I2V base, arXiv 2510.22200), `LongCat-Video-Avatar` 1.5/1.6 (audio-driven avatar video — DIALOGUE-SHOT candidate, D041-safe: narration-driven not music-driven), `LongCat-Image`/`-Edit`/`-Edit-Turbo` (image pool), `LongCat-2.5` (MoE LLM 11-04, trending), AudioDiT (audio tier). All MIT.** | **2026-11-17 (user flag: "why are u missing these things")** |
| **`Wan-AI`** | Wan2.2 family — PAN2 (11-15, pool note) uses the Wan2.2 VAE; major open video org | 2026-11-17 |
| **`google`** | Gemma-4 family — `gemma4-12b` = our LTX text-encoder family; tokenizer-fix thread 11-17 (t3_1xxxs0a) | 2026-11-17 |
| **`tencent`** | Hy4-Flash (11-17 top post t3_1xxlgpb — brain-pool candidate; official page WAF-blocked from our IP) | 2026-11-17 (carry from 11-17 daily) |
| **`nvidia`** | Granite brain + ModelOpt NVFP4 quants (the NVFP4 class of our D207 brain) | 2026-11-17 |

## Community tiers (daily watch — `fetch_news.py` + agent tiers)

- **Reddit:** r/LocalLLaMA (top week), r/ComfyUI (top week — GATED 4+ days as of 11-17 → manual Brave tier), r/artificial (top week)
- **X:** `PixelAigc`, `BennyDaBall_OG` (cookie tier — user-level env, expiry 2026-11-27 → re-copy from Brave DevTools)
  - **2026-11-17 added:** `ai_hakase_` (JP ComfyUI/GenAI aggregator — posts blockout→H3 route content), `aichof21` (JP — "image-gen only" practitioner who ran the blockout→H3 route end-to-end; self-described no-Blender user)
- **Civitai:** boards (H3/Krea2 image + workflow boards; author via browser tier)
- **HF trending/datasets:** brain + world/dataset signals (USDCraft-10K class = geometry layer)

## LTX scope (weekly)

`VFX_PIPELINE_LTX25.md` timeline — diff the Lightricks org + community LTX
mentions (t3_1xuk5dd timeline editor = ready test rig carry).

## ADOPT-candidate standing notes (watch for ComfyUI ports / runnable quants)

- **`meituan-longcat/LongCat-Video-Avatar-1.6`** (11-13, MIT, 130 likes):
  audio-text→video + audio-image→video + audio-driven continuation; = LoRA
  A/B on `LongCat-Video` base + whisper-large-v3 + vocal-separator ONNX
  (Kim_Vocal_2); base_model (BF16 6-shard) + `base_model_int8` (4-shard) +
  77.6 GB total; spaces: `victor/LongCat-Video-Avatar-1.6`,
  `akhaliq/LongCat-Avatar-Studio`. **VERDICT: ADOPT candidate for the
  dialogue-shot route** (narration audio → synced character mouth = the
  piece our H3 R2V reference route lacks; D041-safe). int8 base ≈ 40 GB =
  borderline on 32 GB VRAM → eval when a ComfyUI port lands (no Comfy-Org
  port yet) or via the int8 + CPU-offload diffusers route.
- **`Comfy-Org/PAN2`** (11-15): T2V pool candidate (Wan2.2 VAE, qwen3.5_9b
  encoder, Apache-2.0) — pool note only.
- **MOSS-Image** (11-17, 6.6M dl): image pool watch alongside H3-Image.
- **Abiray H3-Image-GGUF** (rising: 288 likes / 155.5k dl): watch.
- **Qwen4-27B dense** (D225): the correct brain upgrade — auto-covered by the
  `Qwen` org row; flag on sight.
- **FLUX3** (black-forest-labs): gated on the user (HF token + Agree).
- **t3_1xvpmt8** (10-min wordless H3 film): read carry.
- **civitai 2889463**: ADOPT side route carry.

## Route-validation watch (blockout → H3 R2V, our P2)

- **Community proof the 3D-previs → H3 route works with NO Blender
  (2026-11-15/16, X):** `aichof21` (self-described "image-gen only, no
  Blender") + `ai_hakase_` ran it: **Claude Code (Opus 5.5) builds a 3D
  previs video in Three.js** → pass the previs video + character sheet to
  **MiniMax H3** → 10 s 8:9 output. Demo video saved
  `data\x_aichof_previs_h3_1080p.mp4` (1080×1214). **Implication:** our
  S1-S6 Blender blockouts are the same previs step — the route is validated
  by a third party who did NOT use Blender; our editable `.blend` + 5 stills
  per scene are directly convertible to the H3 camref (5 s square) → R2V.
  Two independent community validations now (this X + the 11-14 Blender one).
