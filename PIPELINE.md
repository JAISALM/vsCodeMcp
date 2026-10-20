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
| `10a_frontal_base_zidane.json` | Zidane FRONTAL face — **v7 = D164 ROOT-CAUSE FIX** (v6 FAILED: fixed ADJACENT seeds 76/77/78 = micro-variants; Jaisal-templated prompt = Jaisal's face) | Clone of `01_character_sheet.json` (8 steps, 1152×2048) + **GENUINELY NEW description** (face-shape-first: round/full-cheeked, halal, full beard, lean, white tee — Jaisal template retired) + **DISTANT seeds 250/777/4242 fixed** → 3 genuinely different men. Saves `FACEFRONTAL2_ZIDANE_{a,b,c}` (root, next `_00007_`). **VALIDATES 0/0 (16 nodes).** |
| ~~`10a_frontal3_zidane_i2i.json`~~ | REJECTED (D164 — user: i2i drifts quality) — **DO NOT RUN** | Built (i2i from the approved face, denoise 0.55, 1152×2048); file stays on disk as reference only. |
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

## PROMPTS — LIVE, VERBATIM (what each character workflow actually uses)

**Rule (D159):** every character workflow's live prompts are copied here VERBATIM so the
user can see exactly what's running and ask for changes per character. When a prompt
changes in a workflow, update this section in the same turn.

### `01_character_sheet.json` — Jaisal portrait (the "01 t2i", seed 42, 8 steps, 1152×2048, 01 chain)
**Positive (node 300):**
> kr2realism. Candid medium close-up photograph of a slim 26-year-old Indian man, head and upper chest in frame. Medium-length wavy black hair, and a small patchy short beard. He wears a plain black t-shirt, fully clothed. Warm natural skin with visible pores and a healthy flush, soft even daylight from the side. Clean simple neutral light background, plain uncluttered backdrop. He looks just off camera with a relaxed expression and a small easy half-smile. Shot on a 50mm lens, sharp focus on the face, shallow depth of field, looks like a real unposed photograph.

**Negative (node 301):**
> duplicate character, multiple people, watermark, logo, deformed face, bad eyes, extra fingers

### `10a_frontal_base_jaisal.json` — Jaisal FRONTAL face (3 branches, seeds 42/43/44, 10 steps, 896×1120, turbo+spicy chain)
**Positive (nodes 300/313/318, identical):**
> A candid phone snapshot of a 26-year-old young Malayali man from Kerala, India, South Indian facial features, warm medium-brown natural skin, a young MAN (male only), with a ROUND youthful face, softer rounded features and a masculine jaw, MEDIUM-LENGTH WAVY dark hair worn DOWN and loose around his neck and ears (wavy, natural, slightly messy, hair is NOT tied up, NOT in a bun, NOT a topknot, NOT a short haircut), a sparse short BEARD on his chin and jaw (sparse uneven dark patches you can see on his face, more than stubble, NOT clean-shaven, NOT a dense full beard), a lean and fit young man, NOT bulky, NOT muscular, wearing a plain dark t-shirt, his face completely frontal. He is standing alone, facing the camera directly, dead-center, head and shoulders framing, both eyes fully open and symmetric, looking straight into the lens, calm neutral relaxed expression, face completely frontal, NO side angle, NO profile, NO three-quarter view. His wavy hair is down and loose, the sparse beard visible on his chin and jaw. Sharp focus on the man's face, his face is the main subject, in focus, crisp facial detail, detailed iris and eye texture. He looks like a real young man in his mid-20s: youthful fresh face, natural young skin, no wrinkles, no aging, no grey hair. Candid unposed snapshot caught in a real moment, natural ambient light, looks like a real photo someone took on their phone, slight natural imperfections, a real ordinary person, ONLY ONE character, no other people, NOT a studio portrait, NOT a headshot, NOT a stock photo, NOT a professional photo.

**Negative (node 301):**
> studio portrait, studio lighting, posed portrait, headshot, professional photoshoot, fashion photography, model, celebrity, stock photo, beauty campaign, perfect skin, airbrushed skin, plastic skin, waxy skin, artificial skin, generic AI face, western facial features, northern Indian appearance, older man, mature man, 30s, 40s, 50s, aged face, wrinkles, grey hair, bald, short haircut, bulky body, muscular body, bodybuilder, clean-shaven, no beard, missing beard, full long beard, perfectly groomed beard, duplicate character, multiple people, crowd, woman, women, girl, female, second person, extra person, person in background, text, words, letters, subtitles, captions, dialogue, speech bubble, readable sign, logo, watermark, label, social media overlay, screenshot, UI, deformed face, bad eyes, crossed eyes, extra fingers, malformed hands, distorted anatomy, oversaturated skin, over-processed image, excessive bokeh, artificial cinematic poster, professional camera look, fake environment, saree, sari, traditional dress, nose ring, feminine features, anime, cartoon, illustration, painting, drawing, sketch, stylized, 3d render, cgi, mixed art styles

### `10a_frontal_base_zidane.json` — ZIDANE FRONTAL face — **v6 = ZIDANE'S HOME CHAIN (01 chain) + lean/round prompt**
**DIAGNOSIS (D162 — user: "images look exactly same as jaisals image without hair ... think outside the box"):** the seed is NOT the cause (file ran randomize; 4 runs, same face). **Krea2 anchors the FACE to the model chain + resolution + prompt family — the prompt only swaps attributes (hair/tee/beard) on top of it.** v5/v5b ran on Jaisal's turbo chain (`krea2_turbo_fp8_scaled`, 896×1120) → **Jaisal's face wearing Zidane's hair and white tee** (verified side-by-side: same face, different hair/tee). Zidane's approved face lives on the **01 chain** (`Krea2Realism_V1` + `Krea2-realism-V2`@1.0, `qwen3vl_4b` (krea2), `qwen_image_vae`, **1152×2048**) — the user's 18:19/18:24 runs there came out with ZIDANE's face ("first 3 is good"), only the build was fat.
**v6 = clone of `01_character_sheet.json`** (his home chain, 8 steps euler/simple cfg 1) + v4b's prompt family (the one that produced his face there) with ONLY the build line fixed (lean and fit + distinctly ROUND face — no fat). 3 branches: seeds **77/76/78 FIXED** (77 = his approved face seed = the lock), 1152×2048, saves `FACEFRONTAL2_ZIDANE_{a,b,c}` (root, next counter `_00006_`). i2i dropped (0.4 came out = input).
**Positive (node 300, shared by all 3 branches — v4b family, build line fixed):**
> kr2realism. A candid phone snapshot of a 26-year-old young Malayali man from Kerala, India, with South Indian facial features and warm medium-brown natural skin. He is a lean and fit young man — a slim athletic build — with a distinctly ROUND face, wider and rounder than a long oval face, soft cheeks and a short strong jaw — and he has a short black halal cut with very short faded sides and a short neat crop on top, no waves, and a full short dark beard, neatly trimmed and shaped, dense and clearly visible on his chin, jaw and upper lip. He wears a plain white t-shirt. His face is completely frontal, dead center, head straight, both eyes fully open, looking straight into the camera with a relaxed easy half-smile. Soft even natural daylight, a clean plain off-white wall behind him, sharp focus on his face, realistic skin with visible pores and a healthy flush, looks like a real unposed photo someone took on their phone, a real ordinary young man, only one character, no other people.

**Negative (node 301, shared by all 3 branches — clean D142 + pose/hair lock):**
> duplicate character, multiple people, watermark, logo, deformed face, bad eyes, extra fingers, profile view, three-quarter view, head turned to the side, head tilted, looking away from camera, long hair, wavy hair, man-bun, topknot, ponytail, clean-shaven, no beard, missing beard
**CANONICAL ZIDANE (final, 2026-10-20):** LEAN and fit (the "slightly bulky/fat" instruction was a MISGUIDANCE — retracted by the user); **ROUND face** (wider/rounder than a long oval face — deliberately different from Jaisal's long/oval face); short black halal cut (short faded sides, no waves, no bun); FULL short dark beard, neatly trimmed, dense; white tee; warm medium-brown skin; mid-20s; relaxed half-smile.
**Prompt history:** v1 (10a-jaisal clone, jaisal's prompt kept) → jaisal-like face, no hair. v3 (01 chain, weak beard clause) → patchy beard. v4 (01 chain, beefed-up prompt + i2i) → beard landed, quality dropped (prompt bloat); i2i denoise 0.4 came out = the input. v4b (01 chain, D142-style, "slightly stocky") → **ZIDANE's face correct, build came out fat** (user: "first 3 is good ... like a fat boy"). v5/v5b (Jaisal's turbo chain 896×1120) → **JAISAL'S FACE** wearing zidane's hair/tee — the face is anchored to the chain+resolution (D162), not the prompt. **v6 (CURRENT) = back to the 01 chain (his home chain) + v4b prompt family with ONLY the build line fixed (lean and fit + ROUND face); seeds 77/76/78 fixed (77 = his approved face seed).**
**v6 VERDICT (D163→D164 — user: "the face is still somehow long ... the facial structure is still of jaisals ... idealy it should create a different man altogether"):** v6 output (seeds 77/76/78 fixed) = long face + stubble, a/b/c near-identical to the v4b runs. **ROOT CAUSE (D164):** (1) v6 used `fixed` ADJACENT seeds 76/77/78 — 77 = the exact v4b seed, so 00006 ≈ 00002 (the user's "same seed?" suspicion was correct); (2) every zidane prompt so far was Jaisal's template with attributes swapped — the prompt description anchors the face.
**v7 (CURRENT — D164 root-cause fix):** 01 home chain (8 steps, 1152×2048) + **GENUINELY NEW description** (face-shape-first — Jaisal's template retired, kr2realism trigger kept) + **DISTANT seeds 250/777/4242 fixed** → three genuinely different men to pick from. Saves `FACEFRONTAL2_ZIDANE_{a,b,c}` (root, next counter `_00007_`). Validate 0/0.
**v7 prompt (node 300, shared by all 3 branches):**
> kr2realism. Close-up photo of a young South Indian man facing the camera dead-on, his face filling most of the frame. His face is round and full-cheeked — wide, soft, with a short strong jaw — warm medium-brown skin with natural pores and a healthy flush. His hair is a short black halal haircut: very short faded sides and back, a short neat crop on top, no waves, no bun. A full short dark beard, neatly trimmed and shaped, dense on the chin, jawline and upper lip. He is lean and slim, wearing a plain white t-shirt. He looks straight into the camera with a relaxed half-smile. Natural even daylight, a plain off-white wall behind him, sharp focus on the face, looks like a real unposed phone photo, one person only, no other people.

**Pick-set rule (D164):** never use adjacent seeds for a pick-set (hundreds apart); never clone a sibling's prompt template — write the description from scratch, target face shape FIRST.

### ~~`10a_frontal3_zidane_i2i.json`~~ — REJECTED (D164 — user: "we cannot go with i2i for images because it will drift the quality"): **DO NOT RUN**
Built (validate 0/0, 11 nodes) but rejected: i2i drifts image quality. The lock is v7 (t2i, distant seeds). File stays on disk as a reference.
Chain: 01 home chain (`Krea2Realism_V1` + `Krea2-realism-V2`@1.0, `qwen3vl_4b` (krea2), `qwen_image_vae`, 8 steps euler/simple cfg 1) + **LoadImage `zidane_portrait_00001_.png`** (input dir — the approved 3/4 face, 1152×2048) → VAEEncode → KSampler **[77, fixed, 8, 1, euler, simple, denoise 0.55]** → VAEDecode → SaveImage `FACEFRONTAL3_ZIDANE` (root). Denoise **0.55** because v4's 0.4 came out = the input (too weak for a head rotation). His pixels anchor the face; the model only rotates the head. Validate 0/0 (11 nodes).
**Positive (node 300 — identity anchor FIRST, then target pose, then attributes):**
> kr2realism. The exact same man as the reference image — the SAME face, SAME facial structure, same skin — now completely frontal: dead center, head straight, both eyes fully open, looking straight into the camera with a relaxed easy half-smile. His hair is a short black halal cut with very short faded sides and a short neat crop on top, no waves. He has a full short dark beard, neatly trimmed and shaped, dense and clearly visible on his chin, jaw and upper lip. He wears a plain white t-shirt. Soft even natural daylight, a clean plain off-white wall behind him, sharp focus on his face, realistic skin with visible pores and a healthy flush, looks like a real unposed photo someone took on their phone, only one character, no other people.

**Negative (node 301):**
> different person, different face, duplicate character, multiple people, watermark, logo, deformed face, bad eyes, extra fingers, profile view, three-quarter view, head turned to the side, head tilted, looking away from camera, long hair, wavy hair, man-bun, topknot, ponytail, clean-shaven, no beard, missing beard

### `07_kit_ref_jaisal.json` — Jaisal kit ref (seed 13, 8 steps, 1152×1152, 01 chain)
**Positive (node 300):**
> Product photograph of a men's soccer kit laid out flat on a clean light-grey studio background, top-down flat-lay view: a royal blue short-sleeve soccer jersey with a small, subtle white emblem on the left chest — a simple clenched fist inside a thin circle, plain and minimal, no words, no letters, no text of any kind — and matching royal blue track pants with a single white stripe down each side, jersey neatly above the pants. No person, no face, no other objects. Sharp even studio product lighting, crisp fabric detail, photoreal. kr2realism

**Negative (node 301):**
> person, face, head, blurry, low quality, watermark, text, words, letters, slogan, logo distortion

### `07_kit_ref_zidane.json` — Zidane kit ref (seed 29, 8 steps, 1152×1152, 01 chain)
**Positive (node 300):**
> Product photograph of a men's soccer kit laid out flat on a clean light-grey studio background, top-down flat-lay view: a dark green short-sleeve soccer jersey with a small, subtle white emblem on the left chest — a simple clenched fist inside a thin circle, plain and minimal, no words, no letters, no text of any kind — and matching dark green track pants with a single white stripe down each side, jersey neatly above the pants. No person, no face, no other objects. Sharp even studio product lighting, crisp fabric detail, photoreal. kr2realism

**Negative (node 301):**
> person, face, head, blurry, low quality, watermark, text, words, letters, slogan, logo distortion

### Sheet specs (09j/09k)
The sheet "prompt" is not a t2i prompt — it's the **478 live spec** (~11.3k chars, the
character spec the PE architect works from) + the 3-panel image feed. Jaisal spec in
`09j_QWEN21_JAISAL_sheet.json`, ZIDANE spec in `09k_QWEN21_ZIDANE_sheet.json` (dark
green kit, green-ground crest). Change a detail = change a line in 478 (+ a panel in the
composite for image details).

### Stale / superseded (for reference only)
`krea2_t2i_char2.json` node 200 = 6 STALE man-bun-era zidane prompts ("long dark hair
tied up in a loose man-bun") + JAISAL negative — NOT what produced the approved face;
do not use.

---

## OUTPUT REGISTRY (workflow → image → what it is) — the reuse map

**Rule (D157):** whenever a workflow produces an approved output, record it here —
workflow, settings, output path, what it is, status. Output paths are relative to
`...\ComfyUI\output\` unless prefixed `input:`. **SaveImage convention:** prefix with a
slash (`charsheet/QWEN21_JAISAL`) → subfolder; without a slash (`FACEFRONTAL2_ZIDANE`) →
file at the output ROOT.

### Character faces — Jaisal (char1)

| Image | Source workflow | Settings | What it is / status |
|---|---|---|---|
| `refset_v7\jaisal_t2i_base_00001_.png` | `01_character_sheet` (01 t2i) | seed 42, 8 steps, D142, 2MP 16:9 | t2i base scene — wavy hair ✓, thin patchy beard ✓, black tee + dark trousers, slim, clean cream backdrop, half-smile |
| `refset_v7\jaisal_portrait_00001_.png` | `01_character_sheet` | seed 42, 8 steps, **1152×2048 portrait** | portrait close-up (3/4 view), head + shoulders |
| `refset_v7\jaisal_portrait_HD_00001_.png` | `03_hd_upscale` | Real-ESRGAN x4plus, 4× | 4608×8192 HD of the portrait — **APPROVED canonical (3/4 view)** |
| `FACEFRONTAL_JAISAL_a/b/c_00001_.png` | `10a_frontal_base_jaisal` | Krea2 turbo + V2@1.0 + spicy@0.7, 10 steps, seeds 42/43/44, 896×1120 | FRONTAL faces, 3 branches — **b = APPROVED straight-up** |
| `krea2_char1_face_{,a_,b_,c_}00001…00007` | `krea2_t2i_char1` | 2026-10-08 | early canonical face set: a = misty forest profile, b = wooden boat golden hour, c = rainy street frontal |
| `char_v4\jaisal_00001_.png` / `char_v6\jaisal_v2lora_00001_.png` | 01 t2i | v4: 2MP/10s · v6: V2 LoRA @1.0, 8 steps, 1152×2048 | t2i test faces (wavy ✓, thin beard visible ✓) |
| `input: jaisal_portrait_HD.png` | staged from 10a | 896×1120 | the FRONTAL face staged for the sheet (09j ref) |
| `input: jaisal_portrait_HD_34view.png` | staged | — | 3/4 view variant |
| `input: jaisal_ref.png / jaisal_base.png / jaisal_base_final.png / jaisal_krea2_base_v1-4.png` | various | — | earlier base faces (pre-refset_v7) |

### Character faces — Zidane (char2)

| Image | Source workflow | Settings | What it is / status |
|---|---|---|---|
| `refset_v7\zidane_t2i_base_00001_.png` | `01_character_sheet` (live-typed zidane prompt) | seed 77, 8 steps, D142, 2MP | t2i base — halal short cut ✓ (old spec: thin patchy beard), white tee + dark trousers, athletic build |
| `refset_v7\zidane_portrait_00001_.png` | `01_character_sheet` | seed 77, 8 steps, **1152×2048** | portrait close-up — **3/4 view** (the "sideways" one) |
| `refset_v7\zidane_portrait_HD_00001_.png` | `03_hd_upscale` | 4× | 4608×8192 HD of the portrait — **APPROVED canonical (3/4 view)** |
| `refset_v7\zidane_clean8_00001_.png` | 01 t2i (Z-B) | seed 77, natural-language + D142 clean negative, 8 steps | **WINNER of the grain A/B** — natural warm skin, no grain |
| `refset_v7\zidane_clean16_00001_.png` | 01 t2i (Z-C) | same, 16 steps | also clean skin but 16 steps regenerates MORE → different face (clarity answer: NO — grain was the negative) |
| `FACEFRONTAL_ZIDANE_a/b/c_00001_.png` | 10a v1 (FAILED) | 10a-jaisal clone, tag-stack | **FAILED — jaisal-like face, no hair** (shared opening tokens → face convergence; tag-stack = D142 failure mode) |
| `FACEFRONTAL2_ZIDANE_{a,b,c}_00006_.png` (root — counters _00001_–_00005_ taken by earlier versions) | `10a_frontal_base_zidane` **v6** | ZIDANE'S HOME CHAIN: `Krea2Realism_V1` + V2@1.0, 8 steps, 1152×2048, seeds **77/76/78 fixed**, v4b prompt family with build fixed (lean + ROUND face, halal cut, full beard, white tee) | **FAILED (D163)** — long face + stubble, NOT the approved face; a/b/c near-identical. t2i re-rolling is a dead end (original prompt never saved) |
| ~~`FACEFRONTAL3_ZIDANE_00001_.png`~~ (root) | `10a_frontal3_zidane_i2i` **REJECTED (D164)** | i2i from the approved face, denoise 0.55 | **DO NOT RUN — user rejected i2i (quality drift)** |
| `FACEFRONTAL2_ZIDANE_{a,b,c}_00007_.png` (root) | `10a_frontal_base_zidane` **v7 — D164 ROOT-CAUSE FIX** | 01 home chain (8 steps, 1152×2048) + GENUINELY NEW description (face-shape-first, Jaisal template retired) + **DISTANT seeds 250/777/4242** | 3 genuinely different men → pick best (round face, halal, full beard, lean, white tee) → becomes the sheet face — **PENDING RUN** |
| `krea2_char2_face_{,a_,b_,c_}00001…00008` | `krea2_t2i_char2` | 2026-10-08 | early face set — **STALE man-bun era** (file still holds those prompts) |
| `char_v4\zidane_00001_.png` / `char_v6\zidane_v2lora_00001_.png` | 01 t2i | v4: 2MP/10s · v6: V2 @1.0, 8 steps, 1152×2048 | t2i test faces (halal cut ✓, half-smile ✓) |
| `input: zidane_portrait_HD.png` (4608×8192) / `zidane_portrait_00001_.png` (1152×2048) / `zidane_ref.png` | copies of the approved face | — | 3/4 view — NOT for the sheet (needs the frontal one) |

### Kit references

| Image | Source workflow | Settings | What it is / status |
|---|---|---|---|
| `input: jaisal_kit_ref.png` (1152²) | `07_kit_ref_jaisal` | Krea2 t2i, 8 steps, seed 13 | royal blue jersey + track pants (white side stripe) + white boots flat-lay |
| `input: zidane_kit_ref.png` (1152²) | `07_kit_ref_zidane` | 8 steps, seed 29 | dark green kit flat-lay (D144: same team, different years) |
| `output\zidane_kit_ref_0000{1,2}_00001_.png` | 07 rebuild | fist-only prompt, seeds 13/29 | kit refs with the fist-only crest (first-try both ✓) |

### Crest references

| Image | Source workflow | Settings | What it is / status |
|---|---|---|---|
| `LOGO_FISTS_H3_1fist_00002_.png` | `logo_fists_compare` | H3 ref-based branch | **APPROVED monochrome 1-fist roundel** (D145) → staged to `input: jaisal_crest_ref.png` (blue ground) |
| `LOGO_FISTS_{H3,QWEN}_{3fist,1fist}_0000{1,2}.png` | `logo_fists_compare` | H3 + Qwen branches | all crest design variants |
| `input: logo_1fist_mono.png` | staged | — | monochrome master |
| `data\crests\logo_1fist_{white,black}_transparent.png` | `logo_to_transparent.py` (chroma key — BiRefNet too destructive for thin lines) | — | shirt-ready transparent logos (D145) |
| `input: zidane_crest_ref.png` | `build_zidane_crest.py` | roundel pixels untouched; blue ground → dark green sampled from `zidane_kit_ref.png` (38,73,63) | crest on the kit-matched green ground |
| `input: jaisal_crest_ref_v1_colored.png` | logo v1 | — | colored v1 — SUPERSEDED by D145 monochrome |

### 3-panel composites (the "feed the images" refs)

| Image | Source | Layout | Status |
|---|---|---|---|
| `input: jaisal_sheet_ref_3panel.png` (2304×1536) | `build_3panel_ref.py` | LEFT face (full height, dominant) · TOP-RIGHT crest 760² · BOTTOM-RIGHT kit 760² · 16px gaps, white bg | **IN USE by 09j** (3:2 = sheet aspect; ≤4MP = PE sees full res) |
| `input: zidane_sheet_ref_3panel.png` | `build_zidane_sheet_ref.py` (run AFTER the face run) | same layout, zidane refs | **PENDING face** |

### Character sheets (the A/B verdict, D154)

| Image | Source workflow | Verdict |
|---|---|---|
| `charsheet\QWEN21_JAISAL_0000{1,2,3}.png` | `09j` (PE architect + 3-panel feed) | **00002 = WINNER** — face ✓, crest = actual roundel ✓ (after 3-panel fix), texture ✓ |
| `charsheet\QWEN_JAISAL_00001.png` / `QWEN_ZIDANE_00001.png` | `LEEBLAAB-QwenImage21-Character-SHEET - {jaisal,zidane}` (flat, no PE) | comparison route — raw 10-section prompt straight into generator |
| `charsheet\H3WIDE_JAISAL_0000{1..5}.png` / `H3WIDE_ZIDANE_00001_.png` | `05d_charsheet_H3_wide_*` | good face + layout, small crest |
| `charsheet\H3FIZ_JAISAL_0000{1..4}.png` | `05e_charsheet_H3_fizgig_*` | **identity drift** (different man) + duplicated back view |
| `charsheet\KREA2_JAISAL_{,ID_}0000{1..4}.png` | `08j_KREA2_JAISAL_sheet` | good face + crest, loose layout |
| `charsheet\KREA2_ZIDANE_0000{1,2}.png` | Krea2 zidane sheet | zidane comparison |
| `charsheet\H3_{JAISAL,ZIDANE}_3VIEW_0000{1,2}.png` | `07c_krea2_3view_sheet_*` | early 3-view strip route |
| `refset_v7\jaisal_sheet_00001_.png` | 01-based sheet | early sheet attempt |

### Upscaling

| Workflow | What | Details |
|---|---|---|
| `03_hd_upscale.json` (challenge) | portrait → 4K+ face HD | LoadImage → `UpscaleModelLoader` (Real-ESRGAN_x4plus) → `ImageUpscaleWithModel` → SaveImage. This is how `zidane_portrait_HD` / `jaisal_portrait_HD` were made (4608×8192 from 1152×2048). |
| `seedvr2_{image,video,batch,lastframe_2k}_upscale.json` | SEEDVR2 HD pass | image / video / batch / last-frame-2K |

### Movie assets (input refs for H3)

`jaisal_1_longshot…jaisal_7_title.png` (story-shot refs), `jaisal_sketch_shot{1,2,3}.png`
(sketch refs), `storysheet_05_rain_closeup_gust_v4` / `storysheet_09_cut_title_scene`
(story sheets), `boar_char1_identity.png` / `boar_char2_identity.png` (boar-grave
characters), `char1_sheet.png` / `char2_sheet.png` (sheet inputs for identity-edit),
`intro_*` / `title_*` / `kf*_*.png` (intro, title, keyframe assets), `jaisal_head_180_dergree.png`
/ `jaisal_head_left_back_side.png` (angle refs).

### Datasets → LoRA

`prompts\char_dataset_gpt_package.txt` + `prompts\KREA2_character_dataset_rewritten_2026-10-08.md`
(dataset prompt packages), `krea2_dataset_char{1,2}.json` / `krea2_1click_dataset.json` /
`1 Click Dataset (Klein 9b).json` (builders). **D143: train character LoRA with
Klein-9B DENSE.**

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
2. Clone the **face-t2i workflow** (Zidane: `10a_frontal_base_zidane` v3 = clone of
   `01_character_sheet` — `Krea2Realism_V1` + V2@1.0, 8 steps, 1152×2048; Jaisal frontal:
   `10a_frontal_base_jaisal`) → edit the prompt (D142 natural-language, char's canonical
   attrs + FRONTAL emphasis) + negative (D142 clean + pose/hair lock) + seed + save
   prefix (`FACEFRONTAL{N}_{CHAR}`, no slash = output root) → RUN (fresh tab).
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
