# MOVIE PRODUCTION PIPELINE

**Purpose:** the full character-to-movie pipeline for the Jaisal movie project — how any
character is introduced (face → refs → sheet → dataset → LoRA → movie), and WHERE every
workflow lives. This file is the map; `project-memory/` is the source of truth for decisions
(D-entries).

**Workflows folder (live):** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\`
**Mirror copy (sheets only):** `D:\models\vsCodeMcp\challenge\consistent-short\workflows\`
**Outputs:** `...\ComfyUI\output\` · **Inputs:** `...\ComfyUI\input\`
**Helper scripts:** `D:\models\vsCodeMcp\utilities\` (run with `E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe`)

---

## Stage map

```
CHARACTER BRIEF (hair / beard / clothing attributes)
   |
   v
STAGE 1  FACE REFERENCE ......... Krea2 t2i, FRONTAL, candid phone-snapshot (10a / krea2_t2i)
   |
STAGE 2  KIT + CREST REFS ....... kit flat-lay (07_kit_ref) + crest roundel (logo_fists_compare,
                                   logo_transparent for shirt-ready PNGs)
   |
STAGE 3  3-PANEL COMPOSITE ...... build_*_sheet_ref.py  (face LEFT | crest TOP-RIGHT | kit BOTTOM-RIGHT,
                                   2304x1536 = 3:2 = sheet aspect)
   |
STAGE 4  CHARACTER SHEET ........ Qwen Image 2.1 PE-architect (09j / 09k) — THE WINNING ROUTE (D154)
   |
STAGE 5  DATASET -> LoRA ........ sheet + t2i pics -> dataset workflow -> train character LoRA
   |                             (Klein-9B DENSE, D143)
   v
STAGE 6  MOVIE .................. MiniMax H3 R2V (story sheet refs) + Blender scenes + audio +
                                   upscale/interpolate
```

**Why 09j wins (D154):** it separates SPEC (text, written by a PE architect that SEES the face)
from IDENTITY (image, i2i conditioning). H3 routes (05d/05e) = video frame-anchors (soft
identity, layout from the model's prior). Krea2 (08j) = strong identity, "photograph" layout
prior. A prompt can steer within a model's prior — it can't add an artifact class the model
never learned.

---

## STAGE 1 — Face reference (Krea2 realistic images)

| Workflow | Purpose | Details |
|---|---|---|
| `10a_frontal_base_jaisal.json` | Jaisal FRONTAL face | Krea2 t2i, 3 seed branches (42/43/44 → `FACEFRONTAL_JAISAL_a/b/c`), 896×1120, 10 steps euler/simple cfg 1, `krea2_turbo_fp8_scaled` + `Krea2-realism-V2`@1.0 + `famegrid_spicy_3167060`@0.7, `qwen3vl_4b_fp8_scaled` (krea2 type), `qwen_image_vae`, `FameGridColorFinish` 1.0/0.6. Prompt = D142 candid phone-snapshot recipe, face COMPLETELY FRONTAL (no profile/3-quarter). |
| `10a_frontal_base_zidane.json` | Zidane FRONTAL face | Clone of 10a with ZIDANE's canonical attributes (short black hair w/ faded sides, short full dark beard, white tee — from `zidane_portrait_00001`), 3 branches `FACEFRONTAL_ZIDANE_a/b/c`. **VALIDATES 0/0.** |
| `krea2_t2i_char1.json` / `krea2_t2i_char2.json` | Base t2i (any scene) | Krea2 t2i, D142 recipe (8 steps, clean bg). |
| `krea2_t2i_char1_pe3.json` / `krea2_t2i_char2_pe3.json` | PE3-variant t2i | Same chain + prompt expansion. |
| `krea2_2pass_bf16_turbo.json` | 2-pass t2i | bf16 + turbo second pass. |
| `krea2_identity_edit.json` | Identity-edit scene | Krea2 Identity Edit v1.2: ref image + instruction → scene with same face. `ref_boost` 2.5–4.0 (D023/D025 recipe; D141: dropped for char-refs, kept for explicit scene edits). |
| `krea2T2iI2iInpaint2pass_v15_fixed.json` | t2i / i2i / inpaint 2-pass | General-purpose 2-pass. |

**Face-ref naming:** `input\{char}_portrait_front.png` (frontal, 896×1120). Jaisal's sheet
uses `jaisal_portrait_HD.png` (the frontal face); Zidane's sheet will use
`zidane_portrait_front.png` (staged by `build_zidane_sheet_ref.py`).

## STAGE 2 — Kit + crest references

| Workflow | Purpose | Details |
|---|---|---|
| `07_kit_ref_jaisal.json` | Royal-blue kit flat-lay | Krea2 t2i, 8 steps → `jaisal_kit_ref.png` (1152²). Jersey + track pants (white side stripe) + white boots. |
| `07_kit_ref_zidane.json` | Dark-green kit flat-lay | Same → `zidane_kit_ref.png` (1152²). D144: same team, different years/colors. |
| `logo_fists_compare.json` | Crest DESIGN (4 branches) | H3 ref-based (902/903 on the poster ref) + Qwen 2.1 i2i (956/957); 3-fist + 1-fist variants; save prefixes `LOGO_FISTS_{H3,QWEN}_{3fist,1fist}`. **v2 MONOCHROME spec (D145):** solid white fill + black outline + thin black separator lines, NO colors. Approved: `LOGO_FISTS_H3_1fist_00002` → `input\jaisal_crest_ref.png` (blue ground). |
| `logo_transparent.json` | Background removal (shirt-ready logo) | LoadImage → **PixaromaRemoveBackground** (BiRefNet `birefnet.safetensors`) → RGBA PNG. **Rule: thin-line logos → deterministic color-key instead** (`logo_to_transparent.py`): `data\crests\logo_1fist_{white,black}_transparent.png`. |
| `build_zidane_crest.py` (script) | Crest on kit-matched ground | Recolors only the blue ground of `jaisal_crest_ref.png` → dark green sampled from `zidane_kit_ref.png` (38,73,63) → `input\zidane_crest_ref.png`. Roundel pixels untouched. |

**Crest refs:** `input\jaisal_crest_ref.png` (blue ground) / `input\zidane_crest_ref.png`
(green ground) — the approved monochrome 1-fist roundel (D145). Team crest is SHARED
(same team); only the ground color changes with the kit.

## STAGE 3 — 3-panel combiner (the "feed the images" fix)

| Script | Purpose | Details |
|---|---|---|
| `build_3panel_ref.py` | Jaisal composite | `input\jaisal_sheet_ref_3panel.png` (2304×1536, 3:2): LEFT = face 896×1120 scaled to full height (DOMINANT — sole identity source), TOP-RIGHT = crest 760², BOTTOM-RIGHT = kit 760², 16px white gaps. |
| `build_zidane_sheet_ref.py` | Zidane composite (post-face-run) | Stages newest `output\FACEFRONTAL_ZIDANE\_00001_.png` → `input\zidane_portrait_front.png` (or pass `a`/`b`/`c`), then builds `input\zidane_sheet_ref_3panel.png` (same layout, zidane refs). |

**Why this exact layout (D154):** 2304×1536 = the sheet's 3:2 output aspect → the i2i
generator sees the WHOLE composite (no crop); the PE's image budget (4MP) ≥ 3.54MP → the
architect sees it at full resolution. Face panel dominant → identity; crest panel = a COPY
target ("copy it EXACTLY — do not redesign" — the model copies pixels instead of inventing);
kit panel = color/fabric/texture source.

## STAGE 4 — Character sheet (Qwen Image 2.1 PE-architect — THE ROUTE)

| Workflow | Purpose | Details |
|---|---|---|
| `09j_QWEN21_JAISAL_sheet.json` | Jaisal sheet — **WINNER** (D154) | Chain: `470` LoadImage (3-panel ref) → PE subgraph `555` (ThinkingLLM `Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf`, Qwen3VL, sees the ref + writes a 10-section production spec) → `558` → `459` generator subgraph (bc1c967a: `qwen_image_2.1_bf16` UNET / `qwen3vl_8b_fp8_scaled` CLIP / `qwen_image_2.1_vae_bf16` VAE — D152/D153) with i2i `images.image_1` = the SAME composite → `461` SaveImageAdvanced `charsheet/QWEN21_JAISAL`. `13` ResolutionSelector **3:2 (Photo) @ 3.4MP** (6.0 = best quality). `481` "JAISAL" feeds `{{name}}`. `485` VSR node BYPASSED (orphaned — it soft-upscaled the face; half the old blur). `569` ImageStitch = face-vs-result diagnostic only. |
| `09k_QWEN21_ZIDANE_sheet.json` | Zidane sheet | Clone of 09j: `470`→`zidane_sheet_ref_3panel.png`, `481`→`ZIDANE`, `461`→`charsheet/QWEN21_ZIDANE`, `478`+`555[0]` spec → dark-green kit + green-ground crest. **VALIDATES 0/0 (both copies).** |
| `LEEBLAAB-QwenImage21-Character-SHEET - jaisal.json` / `- zidane.json` | FLAT Qwen sheet (no PE) | Author's original: single face ref → VSR → generator with a raw 10-section prompt (no architect). 16:9 @ 6MP. Kept for comparison only. |
| `05d_charsheet_H3_wide_{jaisal,zidane}.json` | H3-wide sheet (archived route) | MiniMax H3 ref-based sheet. A/B verdict (D154): good face+layout, small crest. |
| `05e_charsheet_H3_fizgig_{jaisal,zidane}.json` | H3-fizgig sheet (archived route) | A/B verdict: **identity drift** (different man) + duplicated back view. |
| `08j_KREA2_JAISAL_sheet.json` | Krea2 sheet (archived route) | Good face + good crest, loose layout. |
| `07c_krea2_3view_sheet_{jaisal,zidane}.json` | Krea2 3-view strip | Early A/B/C test route (reliable, ~30 s). |
| `2BZ_H3_character_sheet_2stage - {jaisal,zidane}.json` | H3 2-stage sheet | Early A/B/C test route. |
| `character sheet\` folder | Author originals | `LEEBLAAB-QwenImage21-Character-SHEET.json`, `minimaxh sheet patreon.json`, `minimax_h3_character_sheet_1wxixua.json`. |

**⚠ THE LIVE SPEC LAYER (D154 — critical):** the PE LLM receives ONLY subgraph node `478`
(the ~11k-char architect spec). Instance node `555` widget[0] is a **DEAD FIELD** (absent
from the LLM input — proven by the node's debug "Final prompt"). The Jaisal emblem-invention
bug (D154) was exactly this: the monochrome spec had been placed in the dead field while
478 carried the old spec. **Rule: edit `478` (internal subgraph node), mirror to `555[0]`
for consistency; never rely on `555[0]` alone.** `481` supplies `{{name}}` (replaced by `480`
StringReplace in the `# USER` line); the KIT SPEC name inside 478 is hardcoded — update it
when flipping characters.

## STAGE 5 — Dataset → LoRA

| Workflow | Purpose | Details |
|---|---|---|
| `krea2_dataset_char1.json` / `krea2_dataset_char2.json` | Character dataset builders | Consistent-image sets for LoRA training. |
| `krea2_1click_dataset.json` | 1-click dataset | One-shot dataset generation. |
| `1 Click Dataset (Klein 9b).json` | Klein-9B dataset | **D143: train the character LoRA with Klein-9B DENSE** (not quantized). |

Dataset = the character's sheet (multiple views) + t2i scene pics. The LoRA becomes the
face-lock for all future refs/sheets/frames (D141 pipeline pivot — no identity-edit
machinery).

## STAGE 6 — Movie (MiniMax H3 + Blender + audio)

| Workflow | Purpose | Details |
|---|---|---|
| `video_minimax_h3_r2v.json` / `video_minimax_h3_r2v+turbo.json` | H3 reference-to-video | 6-section R2V prompt style (D017), 2–3 refs max as frame anchors (D020). |
| `minimaxH315SecondSeamlessMulti_v11.json` | 15 s seamless multi-ref | The "Jaisal Cut" 15 s shot pipeline. |
| `minimaxH330SecondSeamlessImage_v13.json` | 30 s seamless | Longer takes. |
| `minimaxH3Camera_v20.json` | Camera-controlled H3 | Camera moves. |
| `minimax_h3_sam_r2v_cinematic.json` / `minimax_h3_sam_r2v_2char_cinematic.json` | Cinematic / 2-character | Two characters in one shot. |
| `MiniMax H3 Fizgig.json` / `H3-Contest_BaseWorkflow.json` / `vdn_h3_t2v_benchmark.json` | H3 variants/benchmarks | Fizgig = the 05e sheet's H3 variant. |
| `H3_Face_Refine_Auto_Select.json` / `H3_Face_Refine_Manual_Select.json` / `WF-H3_zuanfilm-Face_Detailer.json` | Face refinement/detailer | Post-H3 face touch-ups. |
| `MiniMaxH3_NativeAudio_MusicVideo_TEMPLATE.json` | H3 audio | **D041 HARD RULE: NO music** — natural ambient sounds only. |
| `RIFE_WAN_Method_Interpolation_TEMPLATE.json` | Frame interpolation | Smooth slow-mo. |
| `seedvr2_image_upscale.json` / `seedvr2_video_upscale.json` / `seedvr2_batch_upscale.json` / `seedvr2_lastframe_2k.json` | SEEDVR2 upscaling | HD pass (image/video/batch/last-frame). |
| `QWEN_click_multiple_character_angles-v1.0.json` | Qwen multi-angles | Character angle set. |
| **Blender:** `data\boar_grave_scene.blend` (+ `data\blender_mcp_test.blend`) | Scene construction | Boar-grave scene built in Blender (MCP), paired with `minimax_h3_boar_grave_talking_r2v.json`. |

---

## HOW WE ADD MORE DETAILS (methodology — user question, D154)

**Two channels, each with a job:**

1. **IMAGE channel (copy targets)** — for anything with exact pixels: emblems, kit, props.
   Make a reference image (Krea2 t2i / logo workflow) → add it as a PANEL in the 3-panel
   composite → add ONE spec line to `478`: "…copied EXACTLY from the TOP-RIGHT panel — do not
   redesign it, do not invent a new emblem." The model copies pixels instead of inventing.
   (This is what fixed the crest: text-only "white fist in a circle" → the model invented a
   crown; crest image + copy instruction → the actual roundel.)
2. **TEXT channel (construction spec)** — for anything without pixels: layout, typography,
   zones, captions. Add a line to `478`'s spec (the LIVE layer — see the warning above).

**Identity is ALWAYS image-only (D151):** the LEFT panel is the SOLE identity source — no
attribute re-descriptions in text (no age/hair/beard/build lines in sheet prompts). Fair A/B,
no text-vs-image identity fight.

**Kit color:** text (in 478 + `555[0]`) AND the kit panel. Crest ground color = kit color
(sampled from the kit ref — `build_zidine_crest.py` style recolor, never a new design).

**New character checklist (introduce as many as we want):**
1. Character brief (hair / beard / clothing) — 2–3 lines.
2. Clone `10a_frontal_base_*.json` → edit the 3 positive prompts + negatives + save prefixes
   (`FACEFRONTAL_{char}_{a,b,c}`) → RUN (fresh tab) → pick the best branch.
3. `07_kit_ref_{char}.json` → kit flat-lay → `input\{char}_kit_ref.png`.
4. Crest: reuse the team roundel on the kit's ground color (recolor script) →
   `input\{char}_crest_ref.png`.
5. Clone `build_*_sheet_ref.py` → stage the chosen face → `input\{char}_sheet_ref_3panel.png`.
6. Clone `09j` → `09?_{CHAR}_sheet.json` with the 5 swaps: `470` file, `481` name, `461`
   prefix, `478` spec (name + kit color + crest ground), `555[0]` mirror → validate 0/0 →
   RUN (fresh tab).
7. Sheet + t2i pics → dataset workflow → **Klein-9B DENSE LoRA** (D143) → LoRA = the face-lock.
8. Movie: H3 R2V with the character's refs + story sheet (stage 6).

**Hard rules that bit us (keep them):**
- **D150:** agent never runs GPU jobs without explicit instruction; NEVER run qwen
  llama-server (8100) + ComfyUI (H3) in parallel (VRAM). User manages servers.
- **D154:** the PE live spec layer = subgraph `478`, not `555[0]` (dead field). Verify with
  the node's debug "Final prompt" when in doubt.
- **No VSR upscale on the face** (485 bypassed in 09j/09k) — softens identity conditioning.
- **Composite = 2304×1536 (3:2)** = sheet aspect → no i2i crop; ≤4MP → PE sees full res.
- **Open fresh tabs** for freshly-built workflows (stale `#converted-` views corrupt
  widgets_values on re-save).
- **D152/D153:** Qwen layers = `qwen_image_2.1_bf16` / `qwen3vl_8b_fp8_scaled` /
  `qwen_image_2.1_vae_bf16`; when localizing any author template, sync ALL FOUR model-widget
  layers to on-disk names (`sync_model_layers.py`).
- **D041:** no music anywhere — natural sounds only.
- If the hero is soft: bump `13` ResolutionSelector 3.4→6.0MP, or crop hero +
  `seedvr2_image_upscale` for dataset use.
