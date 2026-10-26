# LTX-2.5 VFX PIPELINE — post-production toolkit for the movie

Created 2026-10-21. Source of truth for the Lightricks LTX-2.5 IC-LoRA VFX
suite and how it plugs into our movie pipeline. **LTX is UNTOUCHABLE in the
model library** (user decision 2026-10-21 — see `MODEL_INVENTORY.md`).

## What this is

Lightricks shipped a rolling "VFX week" series of **IC-LoRAs** (image/
video-to-video adapters) for **LTX-2.5-22b**, each a ~306 MB LoRA that
re-renders a source video with a specific VFX transform **preserving
composition, framing, camera movement, and subject motion frame-for-frame**.
X account: **[@ltx_io](https://x.com/ltx_io)** (keep monitoring; X blocks
direct bot fetches — the HF org creation dates below are the reliable
timeline). Docs hub:
https://docs.ltx.io/open-source-model/vfx-post-production/overview

HF release timeline (verified via HF API, 2026-10-21):

| Date | LoRA | Version | What it does |
|---|---|---|---|
| 2026-09-08 | `LTX-2.5-22b-IC-LoRA-Day-To-Night` | 0.9 | re-renders a daytime video as the SAME shot at night (relighting) |
| 2026-09-09 | `LTX-2.5-22b-IC-LoRA-Water-Simulation` | 0.9 | water simulation |
| 2026-09-09 | `LTX-2.5-22b-IC-LoRA-Clean-Plate` | 1.0 | **removes the background** → clean plate for compositing |
| 2026-09-09 | `LTX-2.5-22b-IC-LoRA-Deblur` | 0.9 | deblur |
| 2026-09-10 | `LTX-2.5-22b-IC-LoRA-Colorization` | 0.9 | color changes / colorization |
| 2026-09-10 | `LTX-2.5-22b-IC-LoRA-Decompression` | 0.9 | compression-artifact removal |
| 2026-09-10 | `LTX-2.5-22b-IC-LoRA-Ingredients` | 0.9 | element add/remove (closest official match to the "background text addition" memory — no official "text" IC-LoRA exists in the org; possibly a community LoRA in the [LTX Community Library](https://ltx.io/ltx-community)) |
| 2026-09-10 | `LTX-2.5-22b-LoRA-Cinemagraph` | 0.9 | i2v: image + prompt → video with subtle **looping** motion (cinemagraph) — `ltx-2.5-22b-lora-cinemagraph-0.9.safetensors` (**201.5 MB**) |
| 2026-09-15 | `LTX-2.5-22b-LoRA-Slow-Motion-Control` | 1.0 | i2v: image + prompt → video with **controllable speed** (real-time → 40× slow-motion, single `--speed` param; repo ships a ComfyUI workflow) — `ltx-2.5-22b-lora-slow-motion-control-1.0.safetensors` (**654.5 MB**) |
| 2026-09-22 | `LTX-2.5-22b-IC-LoRA-Layout-To-Render` | 1.0 | clay viewport/blockout → finished shot (art-directed first frame) |
| 2026-09-27 | `LTX-2.5-22b-IC-LoRA-Refine-Details` | 1.0 | synthesized clarity/detail for low-quality footage |
| 2026-09-27 | `LTX-2.5-22b-IC-LoRA-Restore` | 1.0 | damaged/archival footage restoration (base tag LTX-2.3, runs on 2.5) |
| 2026-09-28 | `LTX-2.5-22b-IC-LoRA-SDR-To-HDR` | 1.0 + scene-emb | SDR video → gradeable HDR (EXR sequence, BT.2020/HLG master; ACEScct working rep) |
| 2026-09-28 | `LTX-2.5-22b-IC-LoRA-Alpha-Gen` | 0.9 | frame-aligned **alpha matte** (grayscale) from RGB video — white = keep, black = transparent, gray = partial |

Also (earlier, 2.5): `Pixel-Spatial-Upscaler-x2` (2026-08-11). Docs list six
post-production capabilities: **Native HDR, SDR→HDR, Alpha Gen (beta),
Layout-to-Render, Native Resolution (Tiled Fusion 4K/8K), Refine & Restore**.

## Our base stack — ALL LOCAL (untouched in the model library)

| Component | File (in `E:\ComfyUI_windows_portable\ComfyUI\models`) | Size |
|---|---|---|
| LTX-2.5-22b distilled DiT (int8) | `diffusion_models\ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors` | 21.5 GB |
| gemma4-12b text encoder (LTX-2.5 proj) | `text_encoders\gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors` | 15.37 GB |
| Video VAE | `vae\ltx-2.5-video-vae-bf16.safetensors` | 1.47 GB |
| Audio VAE | `vae\ltx-2.5-audio-vae-bf16.safetensors` | 0.36 GB |
| Latent spatial upscaler x2 (Native Resolution stage 2) | `latent_upscale_models\ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors` | 1.00 GB |
| SDR→HDR LoRA | `loras\ltx-2.5-22b-ic-lora-sdr-to-hdr-1.0.safetensors` | 1.31 GB |
| Alpha-Gen LoRA | `loras\ltx-2.5-22b-ic-lora-alpha-gen-0.9.safetensors` | 1.31 GB |

**Missing (the only downloads needed):**
1. `loras\ltx-2.5-22b-ic-lora-sdr-to-hdr-scene-emb.safetensors` — **12.6 MB
   companion to the HDR LoRA we already have** (without it the HDR pipeline is
   incomplete) — https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-SDR-To-HDR
2. `loras\ltx-2.5-22b-ic-lora-clean-plate-1.0.safetensors` — **306 MB** —
   https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Clean-Plate
3. `loras\ltx-2.5-22b-ic-lora-day-to-night-0.9.safetensors` — **306 MB** —
   https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Day-To-Night

Total missing for the core three: **~625 MB**. All three IC-LoRAs work on the
**distilled** checkpoint only (ours is the distilled int8 ✓).

## Movie-pipeline mapping (our film: 2 men, bridge/river, rain → moody night)

| Capability | Our use |
|---|---|
| **Clean-Plate** | strip backgrounds from bridge/river plates → composite new environments / CG elements |
| **Day-to-Night** | convert daytime bridge/river shots to the moody NIGHT look our climate continuity demands (D024) — same camera, same motion |
| **SDR→HDR** | gradeable HDR deliverables (EXR + HLG master) |
| **Alpha-Gen** | character alpha mattes from finished H3 shots → compositing (LoRA already local) |
| **Refine-Details** | detail pass on lower-quality H3 output |
| **Layout-to-Render** | storyboard/blockout → finished shot |
| **Water-Simulation** | river water effects |
| **Native Resolution** | 4K/8K output via Tiled Fusion (shared latent canvas, overlapping tiles, one noise field — not independent tile stitching) |
| **Slow-Motion-Control** (LoRA, added 2026-10-26) | slow-mo inserts for rain/action beats — real-time → 40× speed from image + prompt |
| **Cinemagraph** (LoRA, added 2026-10-26) | looping ambient backgrounds — title cards, ambient plates |

## ComfyUI gap — MUST FIX before any VFX workflow runs

**`ComfyUI-LTXVideo` (official Lightricks pack) is NOT in the running install**
(`E:\comfyUi_latest\...\custom_nodes`) — it exists only in the main tree
(`E:\ComfyUI_windows_portable\...\custom_nodes\ComfyUI-LTXVideo`). Install
`https://github.com/Lightricks/ComfyUI-LTXVideo` into the running install's
`custom_nodes`, restart, then pull the example workflows from
`example_workflows/2.5/` in that repo (e.g.
`LTX-2.5_V2V_TiledFusion_Native_4K_8K.json`). IC-LoRAs load through the pack's
IC-LoRA node on the distilled model.

## Download recommendations (2026-10-21)

**Download NOW (core, ~625 MB total):**
- [ ] `sdr-to-hdr-scene-emb` (12.6 MB) — completes the HDR pair we already half-have
- [ ] `clean-plate-1.0` (306 MB) — background removal
- [ ] `day-to-night-0.9` (306 MB) — day→night relight

**Download LATER (same ~306 MB class, when the need arises):**
- `Refine-Details-1.0`, `Water-Simulation-0.9`, `Layout-To-Render-1.0`,
  `Restore-1.0`, `Colorization-0.9`, `Deblur-0.9`, `Ingredients-0.9`,
  `Pixel-Spatial-Upscaler-x2-1.0`

**Weekly watch 2026-10-26 (new official LoRAs, not yet downloaded):**
- `ltx-2.5-22b-lora-slow-motion-control-1.0.safetensors` (654.5 MB) — slow-mo inserts
- `ltx-2.5-22b-lora-cinemagraph-0.9.safetensors` (201.5 MB) — looping ambient backgrounds

**Skip:** `Decompression` (we control our own quality), the LTX-2.3/19b-era
LoRAs (we're on the 2.5 stack).

## Notes / gotchas

- IC-LoRA = video-to-video adapter, NOT a style LoRA — attach it to a
  V2V workflow (source video in, transformed video out), frame-aligned.
- Native Resolution Tiled Fusion: single-GPU path, budget VRAM per canvas
  size; **test the target resolution on the 5090 (32 GB) before committing a
  full clip**; inspect tile boundaries across the whole clip.
- Native HDR / EXR workflows: frame sequences need explicit frame rate;
  EXR = scene-linear (ACEScg), never display-encoded HLG/PQ labeled as
  scene-linear.
- "The LTX-2.5 model card states a large majority of LTX-2.3 LoRAs/IC-LoRAs
  run unchanged on 2.5, with exceptions" — validate per-LoRA before relying on it.
- Example videos live in each HF repo's `examples/` folder (side-by-side mp4s)
  — watch one before wiring a workflow.
- **Audio rule (D041):** LTX V2V outputs are silent — all audio stays H3-native /
  ambient-only, no music.

## COMPLETE official IC-LoRA catalog (docs.ltx.io, fetched 2026-10-21)

**Runs with LTX-2.5:** Union Control (depth/canny/pose in one) · Motion Control
(spline trajectories, 2.3-trained) · **Ingredients** (characters/props/locations
consistent from a reference sheet — 2.5 adapter exists) · Pixel Spatial Upscaler
(2×) · In-Outpainting (canvas extend / masked fill, 2.3-trained) · Instant Shave
(2.3) · Water Simulation · Colorization · Decompression · Deblurring · Day to
Night · Clean Plate · SDR to HDR · Layout to Render · Refine Details · Restore.
**2.3-only:** Cross-Eyed · Dub-It (lip-sync speech re-gen) · **Relight (sun
direction)** — relights exterior video to a chosen sun direction + hardness
(`LTX-2.3-22b-IC-LoRA-Relight`, `ltx-2.3-22b-ic-lora-relight-1.0.safetensors` —
not local; useful for our bridge/river exteriors).

**"Background text addition" verdict (2026-10-21):** there is **NO standalone
"text" IC-LoRA** in the official org or catalog (verified: full org model list,
the official catalog above, Civitai search). The memory maps to:
(1) the **base model's text-rendering capability** — LTX-2.5 renders legible
in-scene text when prompted (the open-source item = the base model, which we
ALREADY have — no download needed), or (2) **Ingredients** (the official
element-consistency adapter — closest "add/manage elements" tool), or (3)
In-Outpainting (fill a masked region with generated content). If a specific
"background text" X post surfaces in the weekly watch, capture the exact repo
then. **Re-verified 2026-10-26 against the FULL LTX Community Library (45
curated entries fetched via browser) — still absent (3rd consecutive weekly
check). Verdict stands.**

**Download list for the user (browser, → `E:\ComfyUI_windows_portable\ComfyUI\models\loras\`),
given 2026-10-21:**
- [ ] `https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-SDR-To-HDR/resolve/main/ltx-2.5-22b-ic-lora-sdr-to-hdr-scene-emb.safetensors` (12.6 MB — completes the HDR pair)
- [ ] `https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Clean-Plate/resolve/main/ltx-2.5-22b-ic-lora-clean-plate-1.0.safetensors` (~306 MB)
- [ ] `https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Day-To-Night/resolve/main/ltx-2.5-22b-ic-lora-day-to-night-0.9.safetensors` (~306 MB)
- [ ] `https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Water-Simulation/resolve/main/ltx-2.5-22b-ic-lora-water-simulation-0.9.safetensors` (~306 MB — user-requested)
- [ ] optional `https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Ingredients/resolve/main/ltx-2.5-22b-ic-lora-ingredients-0.9.safetensors` (~306 MB — element consistency)
- [ ] future: `https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight/resolve/main/ltx-2.3-22b-ic-lora-relight-1.0.safetensors` (sun-direction relight), `.../LTX-2.3-22b-IC-LoRA-In-Outpainting/resolve/main/ltx-2.3-22b-ic-lora-in-outpainting-0.9.safetensors`

**Krea 2 RAW DiT STATUS (2026-10-21 11:00): DOWNLOADED by user →
`E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\krea2_raw_bf16.safetensors`
(24.5 GB) — all Fizgig Krea 2 training files are now local (VAE, CLIP, turbo LoRA
also in the shared library).**

## Monitoring (ongoing)

Weekly check (schedule set 2026-10-21): fetch
`https://huggingface.co/api/models?author=Lightricks&sort=createdAt&limit=40`,
diff new models against this doc's timeline, append new IC-LoRAs + note X
posts when discoverable (X blocks bots — search summaries as fallback).

Check log:
- **2026-10-21 (initial):** timeline above; no "text" LoRA in the org.
- **2026-10-26 (weekly #3):** HF org = **no new models since 09-28**
  (timeline current). Two official LoRAs previously untracked in this doc
  added to the timeline: Cinemagraph (09-10) + Slow-Motion-Control (09-15).
  X (@ltx_io): no new official VFX drop this week (latest recorded = Native
  Resolution + Refine + Restore); profile currently featuring community
  builds — @wildmindai "2D hand-drawn animation IC-LoRA" (live-action →
  hand-drawn 2D, plate/props left alone) and CQdesign "Video/Image Enhancer
  LoRA V2" (generative restore, no ghosting). Community library (full 45-entry
  list fetched via browser): **still NO "background text addition" LoRA**
  (3rd check). New community entries of note: **Foley IC-LoRA** (LTX team,
  2.3 — synchronized Foley SFX for silent video, suppresses music + speech →
  aligns with D041), **Obscura Remova** (WepeNerd, 2.3+**2.5** — removes
  foreground occlusions: curtains/plants/windows/haze), **Multiple Subject
  Reference** (LiconStudio, 2.3 — multi-ref identity), **IC-LoRA-Cameraman**
  (cseti, 2.3 — camera-motion transfer), **ID-LoRA** (AviadDahan, 2.3 —
  appearance + voice from image + audio).
