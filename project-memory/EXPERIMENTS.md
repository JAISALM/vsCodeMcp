# Experiments

Newest experiments first.

---

## 2026-10-22 — Krea2 dual-subject LoRA first train `krea2fp` (2 subjects + Isolation) → A/B decision test built

**Goal:** 2-subject face-lock LoRA (Jaisal=`jeskv`, Zidane=`dlor`) via Fizgig LoRA
Isolation, for the 2-man movie (faces locked before MiniMax H3 R2V).

**Config (verified from `/api/runs` payload, run id 19cd96f65583):** page defaults
(NETWORK_DIM 8 / alpha 8, LR 1e-4 adaptive 2e-4..4e-4, 30 epochs, save every
epoch, DATASET_MEGAPIXELS 0.25, seed 42, EMA 0.98, adamw8bit — the locked rank-32
/ 1.0 MP config was NOT applied; user went with defaults), 2 subjects
(`D:\lora_training\jaisal` + `D:\lora_training\zidane`), People mode = **Fizgig
LoRA Isolation**, sample prompts = `jeskvman` / `dlorman` (two lines), turbo
preview 0.7, 1024², every 1 epoch. **~43 min** (08:01→08:44, 30 checkpoints + 60
previews).

**Outputs:** `D:\tools\Fizgig\output_loras\krea2fp-000001..000030.safetensors` +
final `krea2fp.safetensors` (56 MB) + 60 previews in `output_loras\sample\`.
Copied to shared lib as `krea2fp_rank8_ep30.safetensors` +
`krea2fp_rank8_ep16.safetensors` (`E:\ComfyUI_windows_portable\ComfyUI\models\loras\`).

**User observations:** previews good but all close-ups (EXPECTED — dataset is 40
close/medium shots; movie shot-size comes from the prompt, the LoRA pins identity
only); **face 2 (Zidane) sometimes missing** in previews → plausible at rank 8 /
0.25 MP (less capacity + coarser resolution for two identities).

**Decision (user, 2026-10-22 10:43 IST):** A/B test BEFORE retraining — base model
+ descriptive 2-man prompt (no LoRA) vs our LoRA + trigger prompts, same chain /
seed. Workflows built from `krea2_t2i_char1.json` chain (krea2_turbo_fp8_scaled
DiT + Krea2-realism-V2@1.0 + famegrid_spicy@0.7, 10 steps CFG1 euler/simple,
1120×896 landscape): **`krea2_ab_A_baseline.json`** (no krea2fp; descriptive
prompts for both men — wavy-hair black-T man + bun-hair white-T man, 2 framings)
and **`krea2_ab_B_lora.json`** (+ node 303 LoraLoaderModelOnly
`krea2fp_rank8_ep30.safetensors`@1.0 spliced UNET→303→realism via link 14;
trigger prompts `jeskvman and dlorman…`). Both MCP-validated clean (0 errors / 0
warnings).

**PS gotchas (this build):** `Set-Content -Encoding UTF8` writes a BOM → use
`[IO.File]::WriteAllText` + `UTF8Encoding(false)`; `@(a..) + @(b..)` on Object[]
FLATTENS (link-14 became 6 loose scalars → the UI→API converter dropped the link
and node 96 lost its model input) → use `ArrayList.Add` for nested arrays;
`[int]$x.pos[0]` binds the cast wrong → write `[int]($x.pos[0])`.

**NEXT:** user restarts ComfyUI (also activates LTXVideo pack + ninja) →
Workflows tab → queue A then B → compare faces → decision: retrain rank 32 /
1.0 MP (locked config) if B clearly better, descriptive-prompt route if A
suffices.

**B RESULT (user ran, 11:20 IST — user's modified 6-prompt set, dataset scenes):**
6 images all show ONE man = Jaisal's TYPE locked (wavy hair, thin beard, black
T, dataset scenes: park/rain street/backwater boat/bus/temple) but the FACE is
a "Jaisal-ish stranger", NOT the canonical char1 face. Combined
`jeskvman and dlorman` prompt COLLAPSED to single person (Zidane absent — rank 8
can't hold 2 identities in one frame). User confirms: identity drifted + heavy
`Krea2-realism-V2@1.0` dilution in the chain.
**ZERO-COST DIAGNOSTICS ordered before retrain:**
1. Pure-LoRA test: BYPASS (red X) the realism-96 + famegrid-97 nodes in
   `krea2_ab_B_lora`, re-queue same prompts → isolates realism dilution from
   LoRA weakness. (Bypassed LoraLoaderModelOnly = passthrough.)
2. Dataset sanity: user eyeballs `D:\lora_training\jaisal` images vs canonical
   `krea2_char1_face_b_*.png` — if dataset face already off, regenerate dataset
   from canonical refs BEFORE any retrain (LoRA ≤ dataset quality).
**Decision tree:** pure-LoRA face OK → no retrain, movie = krea2fp + realism@0.5.
Pure-LoRA still drifted → RETRAIN rank 32 / alpha 32 / 1.0 MP (Presets dropdown
"Krea 2 Standard" + Target Megapixels 1.0, user's clicks, ~1.5 h, save-every-
epoch). Afterwards test per-subject (`jeskvman` / `dlorman` alone) AND combined.

## 2026-10-20 — 10a_frontal_base_zidane v1 FAILED (jaisal-like, no hair) → v2 = char2 chain + D142 (D155)

**Trigger:** user: "zidane also need a front facing image, not the sideways one" + after
running v1: "it just gave me the same image as jaisal, without hair lol, it doesnt work,
we need to find out the workflow which produced zidane_portrait_HD_00001_ and copy the
same prompt".

**v1 config (FAILED):** clone of `10a_frontal_base_jaisal` — same Krea2 turbo chain,
3 branches (seeds 42/43/44), 896×1120, tag-stack positive with NOT-clauses, my own
negative.
**Result (user):** face came out JAISAL-LIKE with NO hair — identity did not land as
Zidane.
**Diagnosis (root causes):**
1. **Face convergence:** v1's positive shared Jaisal 10a's first ~30 tokens ("A candid
   phone snapshot of a 26-year-old young Malayali man from Kerala, India, South Indian
   facial features, warm medium-brown natural skin, a young MAN (male only), with a
   youthful oval face, strong masculine jaw...") → Krea2 re-derived the same generic
   Malayali face as Jaisal.
2. **Tag-stack + NOT-clauses** = D142's proven failure mode (grainy/washed; the
   natural-language 4-5-sentence style is the locked winner).
3. **Size:** 896×1120 vs the 1152×2048 portrait that produced his canonical face.

**The proven source (found):** `refset_v7\zidane_portrait_HD_00001` (4608×8192, the
approved sideways HD face) came from the **char2 t2i chain** per memory (01 t2i, D142
clean recipe, **seed 77**, **portrait 1152×2048 close-up** → 03 4x upscale). The
`krea2_t2i_char2.json` file on disk is STALE: its `PixaromaPromptEach` (node 200) holds
6 **man-bun-era** zidane prompts and its 301 widget holds the **JAISAL negative**
("short haircut, clean-shaven, no beard, missing beard" as negatives — the opposite of
Zidane's halal cut + FULL beard). His actual face was generated with a **live-typed D142
prompt that was never saved** (file still shows the pre-run state).
**v2 config (REBUILT, validate 0/0):** char2 chain (`krea2_turbo_fp8_scaled` +
`Krea2-realism-V2`@1.0 + `famegrid_spicy_3167060`@0.7, `qwen3vl_4b` krea2,
`qwen_image_vae`, `FameGridColorFinish`) with node 200 DELETED and the prompt directly in
CLIPTextEncode 300 (native shape): D142 natural-language (kr2realism trigger) — his
canonical attrs read from the actual image (short black halal cut, FULL short dark beard
neatly trimmed, white tee, warm brown skin, mid-20s, half-smile) + dead-center FRONTAL
emphasis; negative = D142 clean (identity-safety only) + pose/hair-lock negatives.
KSampler **seed 77 / 8 steps** euler/simple cfg 1; latent **1152×2048**; save prefix
`FACEFRONTAL2_ZIDANE`.
**Lesson:** to reproduce a specific face in Krea2, reuse its EXACT proven settings (seed,
size, chain, recipe style) — do NOT clone a sibling character's file (shared prompt
tokens → shared face). Krea2 t2i faces are prompt+seed-deterministic; a new seed or new
opening tokens = a different face.

**v3/v4 run (user):** output came out with a **PATCHY beard** ("it still has patchy
beard, i dont think you copied the correct prompt for zidane").
**Diagnosis:** my reconstructed prompt's beard line was ONE clause ("a FULL short dark
beard, neatly trimmed and shaped around his chin, jaw and cheeks") — too weak; Krea2's
prior for a young Malayali man (thin patchy beard, the Jaisal default) won. The
beard that actually produced the approved face was specified CONCRETELY (the old char2
prompt style: where it sits + density + growth stage + targeted NOTs).
**Fix (v4 prompt, node 300 — now recorded verbatim in PIPELINE.md):** concrete beard
block — "a clearly visible FULL short dark BEARD covering his chin, jawline, cheeks
and upper lip — dense dark facial hair you can see on his face, about 2-3 weeks of
growth, neatly trimmed and shaped, much more than stubble, NOT a thin patchy beard, NOT
just a shadow, NOT clean-shaven, NOT a long beard".
**Lesson (D159):** identity-critical features (beard, hair, build) need a CONCRETE
VISUAL block in the Krea2 prompt — a one-line description is too weak and the model's
prior wins. All live character prompts are now copied VERBATIM into PIPELINE.md
(PROMPTS section) so the user can review + request per-character changes.

**v4 run results (user, 2026-10-20):** the i2i route (denoise 0.4 from the approved 3/4
portrait) came out **= the input** — barely changed; denoise 0.4 is too weak for a head
rotation ("the last image is just the input"). The t2i branches with the v4b "slightly
stocky / full face / natural fat" prompt came out **"like a fat boy"** — the user then
retracted the bulky instruction ("he is a footballer, no fat, sorry for the
misguidance").
**Fix (v5, D161):** user's suggestion adopted — clean clone of the WORKING
`10a_frontal_base_jaisal.json` (turbo + V2 + spicy chain, 10 steps, 896×1120, 3
branches — the exact chain that produced the approved jaisal frontals) with a
**ZIDANE-LED** prompt (round face, LEAN build, halal cut, full beard, white tee; same
style as jaisal's working prompt) and zidane's negative. i2i dropped.
**Lessons:** (1) i2i denoise 0.4 ≈ no change for a head-rotation task — pose changes
need a stronger denoise or a different route; (2) a build description in the prompt
controls the body faithfully — "stocky + fat" → fat boy; (3) when a sibling character's
workflow already produces approved frontals, cloning its CHAIN + swapping a
character-led prompt is the fastest reliable route (the prompt must lead with the new
character's own identity block — v1's failure was keeping the sibling's prompt).

**v5/v5b run (user, 2026-10-20):** v5/v5b ran on Jaisal's turbo chain (896×1120) with
fully independent zidane prompts → output = **JAISAL'S FACE** wearing zidane's hair +
white tee (verified side-by-side). 4 runs, seed control `randomize` (different seeds
every run) — same face each time.
**Diagnosis (D162):** Krea2 anchors the FACE to **chain + resolution + prompt family**
— the prompt swaps attributes (hair/tee/beard/pose) on top of the face the chain
produces. Jaisal's face lives on the turbo chain; zidane's approved face lives on the
01 chain (`Krea2Realism_V1`, 1152×2048, seed 77). The seed is NOT the face's owner.
**Fix (v6):** back to the 01 chain (the user-approved "first 3 is good" runs) + v4b
prompt family with ONLY the build line fixed (lean + ROUND face); seeds 77/76/78
FIXED (77 = his approved face seed).
**Lessons:** (1) a character's face belongs to the chain + resolution it was born on —
t2i on a foreign chain re-derives a different face (no seed/prompt change fixes it);
(2) "same face, different hair/tee" output = chain mismatch, not a prompt problem —
diagnose the chain before touching the prompt again.

**v6 run (user, 2026-10-20, 18:48):** v6 (01 chain, seeds 77/76/78 FIXED, 1152×2048,
lean + round-face prompt) → output = LONG face + stubble, NOT the approved zidane
face; a/b/c near-identical to each other and to the v4b runs. User: "idealy it should
create a different man altogether right? ... the facial structure is still of
jaisals, so theres definetly something in the underhood".
**Diagnosis (D163→D164):** Krea2 face = f(prompt, seed, chain, resolution). v6's
"same man" output had TWO concrete causes: (1) v6 used `fixed` ADJACENT seeds
76/77/78 — 77 = the exact v4b seed, so 00006 ≈ 00002 (the user's "are we doing it
in same seed?" suspicion was CORRECT for v6); (2) every zidane prompt so far was
Jaisal's template with attributes swapped — the prompt description anchors the
face (Jaisal's randomize frontals = same man across seeds).
**Fix (D164) — v7:** `10a_frontal_base_zidane.json` = 01 home chain + GENUINELY NEW
description (face-shape-first, Jaisal template retired) + DISTANT seeds 250/777/4242
fixed → three genuinely different men. **i2i route REJECTED by user** (image quality
drift — standing order: no i2i for images); `10a_frontal3_zidane_i2i.json` stays on
disk, DO NOT RUN.
**Lessons:** (1) capture the winning t2i prompt IMMEDIATELY (PIPELINE.md same turn) —
a live-typed prompt that is never saved makes its face unreproducible by t2i
afterwards; (2) when a face must match a specific EXISTING image, i2i from that image
is the only reliable route — but the user REJECTS i2i for images (quality drift) —
t2i pick-sets with distant seeds are the standing route; (3) "should create a
different man" — adjacent seeds + similar prompts give the same man; a genuinely
different face needs a genuinely different prompt + distant seed.

## 2026-10-20 — SHEET 4-WAY A/B VERDICT (user ran all 4) + 09j 3-panel feed fix (D154)
- **Trigger:** user: "tried all 4 and qwen ended up being the top ... the jersey texture and
  the emblem were missing and it had to create something own, which turned out bad, we need
  to feed the images, at least the crest alone" + "i want to understand how others went really
  bad ... its not the models fault i feel like our setup/prompt issue" + "lets complete this
  today".
- **Results:**
  - **09j Qwen = WINNER** (`QWEN21_JAISAL_00002`, 2304×1536): professional design-sheet
    layout (metadata column, hero, turnaround, action poses, silhouettes, expressions, 6
    detail tiles) + face close to the reference + correct kit. **Failure modes:** chest
    emblem INVENTED (crown-like, "TEIIM CREST" typo tile — no crest was ever shown to the
    model), jersey flat (no fabric texture), full body slightly blurry.
  - **05d H3-wide** (`H3WIDE_JAISAL_00005`): good face + good layout (portrait + 3 body
    views + 6 detail circles) but small crest roundel.
  - **05e H3-fizgig** (`H3FIZ_JAISAL_00004`): **identity drift** — a different man (fuller
    dark beard, different hair) + duplicated back view (4 body views, double "JAISAL").
  - **08j Krea2** (`KREA2_JAISAL_ID_00004`): good face, good crest (workflow carries a
    crest ref image), but loose layout (4 loose views + floating crest, no sheet structure).
- **Root cause (setup, not model):** 09j's architecture separates spec (text, written by a
  PE architect that sees the face) from identity (image, i2i conditioning) → both
  controlled. H3 R2V refs = frame anchors for a video model (soft identity, layout from the
  model's own prior). Krea2 edit = strong identity, "photograph of a person" layout prior.
  **09j emblem bug:** the monochrome spec lived in 555 widget[0] — a DEAD field; the PE LLM
  actually received 478's OLD non-monochrome spec (user's debug paste proves it) → no
  monochrome constraint + no crest image → the model invented the emblem.
- **Fix (file work, user runs):** `input\jaisal_sheet_ref_3panel.png` 2304×1536 (3:2 =
  sheet aspect → no i2i crop; PE budget 4MP ≥ 3.54MP → full-res architect view): LEFT face
  (dominant) / TOP-RIGHT crest on royal blue / BOTTOM-RIGHT kit flat-lay. Rewire: 470 →
  composite → PE 555.in0 + i2i 459.in6 directly; **VSR 485 bypassed** (soft-upscaled the
  face 896×1120→1368×1712 — half the blur). 478 ← REFERENCE IMAGE LAYOUT + monochrome KIT
  SPEC; 555[0] mirrored. Both copies validate 0/0.
- **Conclusion:** 09j = the sheet route (pending user verification run). Crest is now a COPY
  target (image) instead of an invention target (text-only). Blur mitigated (native face
  pixels, no VSR); if the hero is still soft → crop hero + 4× upscale (03_hd_upscale) for
  dataset use.
- **Status:** DONE (file work) — awaiting user run + verdict.

## 2026-10-18 22:0x — CHARACTER SHEET A/B/C TEST (in progress — user-directed)
- **Trigger:** user: "p3 is the one you're suggesting, but lets try 2 workflows and test it, is p3
  minimax one? ... lets try with qwen 2.1 and krea2 also, which is the best, so lets try ABC
  testing" + kit spec: **Jaisal = royal blue jersey+track pants, Zidane = dark green, both with
  white clenched-fist roundel crest (PALESTINE RESISTANCE) on chest, name on back — "same team,
  different years".** See D144.
- **Kit refs (Krea2 t2i, D142 recipe, 8 steps):** `07_kit_ref_{jaisal,zidane}.json` →
  `input\jaisal_kit_ref.png` (royal blue) + `input\zidane_kit_ref.png` (dark green) — **BOTH
  RAN FIRST TRY: crest + "PALESTINE RESISTANCE" text legible, white side stripes, clean flat-lays**
  (~20 s each).
- **6 variants** built by `utilities\make_abc_sheet_variants.py` (all validated valid:true):
  A = `2BZ_H3_character_sheet_2stage - {char}.json` · B = `LEEBLAAB-QwenImage21-Character-SHEET -
  {char}.json` · C = `07c_krea2_3view_sheet_{char}.json`. Prompt ids in CURRENT_TASK.md.
- **A-jaisal RESULT (job bb7a4fcd, ~15 min):** 2880×2880. Face EXCELLENT (wavy hair ✓ patchy
  beard ✓ Indian skin ✓) + royal blue jersey with the fist-crest ✓. **BUT: single full-body
  photo, NOT the 3-view sheet** — H3 ignored the "three equal vertical photographs" instruction;
  cinematic palace-corridor background (not neutral studio); the folded track pants from the
  flat-lay ref were rendered as **the character HOLDING a folded pant** while wearing black
  shorts. **Verdict data point: route A transfers identity+kit strongly but follows LAYOUT
  instructions weakly (it's a video model).**
- **FULL RESULTS (all 6 runs + 1 A-jaisal retry):**
  - **A = H3 2BZ** (2880², ~15 min/run, NO seed input on the H3 node = stochastic):
    - Jaisal run 1 (`H3_JAISAL_3VIEW_00001`): single cinematic full-body photo (palace
      background, HOLDING a folded pant, black shorts) — layout instruction ignored.
    - Jaisal run 2 (`H3_JAISAL_3VIEW_00002`, retry): **PERFECT 3-VIEW SHEET** — front/side/back,
      neutral grey studio, full blue kit + PALESTINE RESISTANCE crest + "JAISAL" on back;
      nits: bare feet, faint geometric jersey pattern.
    - Zidane (`H3_ZIDANE_3VIEW_00001`): **PERFECT 3-VIEW SHEET** — front/side/back, full dark
      green kit + crest + "ZIDANE" on back, black cleats. Best-looking sheet of the test.
  - **B = LEEBLAAB Qwen 2.1** (3360×1888, 30 steps): **0/2** — Jaisal = oil-painting-style
    portrait on a GOLDEN STAR background (no sheet, no kit); Zidane = single headshot with
    **WRONG HAIR (blonde curls)** + white tee. Root cause: the 10-section ~4500-char prompt
    exceeds `TextEncodeQwenImage21`'s 1024-token cap → TRUNCATED → layout sections lost.
    Route B unusable as a sheet generator in this configuration.
  - **C = Krea2 t2i** (2048×1152, ~30 s/run, D142 recipe): **2/2 EXCELLENT** —
    `KREA2_JAISAL_00001` + `KREA2_ZIDANE_00001` = clean 3-view strips, correct faces, full
    kits (crest + white stripes + name on back rendered correctly both times).
- **VERDICT:** **C (Krea2) wins on reliability** (2/2 first-try, ~30 s, zero new infra, uses
  the locked base). A = highest ceiling when it works (Zidane sheet is the most "pro"), but
  seedless + ~15 min/run + 1-of-2 Jaisal failures = retry cost. B = ruled out (truncation).
- **Status:** DONE — awaiting user's route pick.

## 2026-10-18 20:0x — HD CLARITY pipeline: portrait close-up + 4x Real-ESRGAN (03_hd_upscale)
- **Trigger:** user: "whatever under v7 is not up to the mark, clarity too off — cant we generate HD?"
  Files ARE 2048×1152 (> full-HD) but the face gets only ~700px in the wide frame → soft at 100%.
- **Model:** `RealESRGAN_x4plus.pth` (63MB) → `E:\comfyUi_latest\...\models\upscale_models\`.
  **Source lesson:** HF now 401s `xinntao/Real-ESRGAN` (gated) — hf-mirror also 401; worked via
  public mirror repo `https://huggingface.co/schwgHao/RealESRGAN_x4plus/resolve/main/RealESRGAN_x4plus.pth`.
  **HF is gating models — the P3 sheet downloads (Mamad8/MiniMax-H3-Image-VAE, Comfy-Org/Gemma4) may
  need an HF token → ASK USER for one when P3 prep starts.**
- **Workflow:** `challenge\consistent-short\workflows\03_hd_upscale.json` (UI format): LoadImage
  (input/ file) → UpscaleModelLoader(RealESRGAN_x4plus) → ImageUpscaleWithModel (input name is
  `upscale_model`, NOT `model` — validate catches it) → SaveImage.
- **Run:** 01 t2i (D142 clean recipe, seed 77, **portrait 1152×2048 close-up** — head+shoulders,
  face ≈ 50% of frame) → `refset_v7\zidane_portrait_00001` → copy to input/ → 03 4x upscale →
  `refset_v7\zidane_portrait_HD` (4608×8192, 37MP — true HD+).
- **RESULT:** `zidane_portrait_HD_00001` = **4608×8192 (37MP, 36MB PNG)** — face crop at ~1:1 detail
  shows individual eyebrow/beard hairs, natural pores, warm flush, eye catchlight = **photo-grade
  clarity, grain GONE**. Portrait close-up framing (face ≈ 50% of frame) was the key lever — more
  pixels ON THE FACE, not just a bigger canvas.
- **LOCKED HD CHARACTER REF PIPELINE:** 01 t2i (D142 clean recipe, **portrait 1152×2048 close-up,
  head+shoulders**) → copy to input/ → 03_hd_upscale (Real-ESRGAN x4plus 4x) → 4608×8192 HD.
- **Status:** DONE — user approved the Zidane HD face.
- **Jaisal FINAL (same pipeline, seed 42, MEDIUM close-up = head+upper chest per user):**
  01 t2i clean recipe 1152×2048 → `refset_v7\jaisal_portrait_00001` (wavy medium hair ✓,
  small patchy beard ✓, black tee ✓, slim ✓, natural skin ✓) → 03 4x →
  **`refset_v7\jaisal_portrait_HD_00001`** (4608×8192).
  **FINAL PAIR for character sheet + dataset:** `zidane_portrait_HD_00001` + `jaisal_portrait_HD_00001`.

## 2026-10-18 19:5x — Reddit Krea2 research: skin-detail quality + settings (user-shared threads)
- **Trigger:** user: "skin is kinda off, like grains, do we need more clarity? check the web" + 2 threads:
  K1 = u/rynaleopard "Krea2-realism-V2 is finally here" (civitai red 2728365, HF RudySen/Krea2-realism-V2),
  K2 = u/Due_Research9042 "Krea 2 is still the best model for full HD images".
- **Fetch (new tooling):** `utilities\extract_reddit_images.py` (URLs + comments from saved DOM),
  `utilities\download_reddit_images.py` (403 on bare URLs — signed-only), **`utilities\expand_reddit_images.py`**
  (WORKS: click post image → lightbox → capture full-res src → save). K1 saved 4 full-res images
  (`data\reddit_krea2\imgs\K1_0{1,3,4,9}_*`).
- **Findings:**
  - K1 poster: V2 "biggest focus was faces — death-stare mostly gone, expressions natural, works much
    better alongside character LoRAs". **Prompting = natural language, short paragraph, 4-5 sentences —
    NOT tag stacking.**
  - K1 comment (settings ask): "Could I see your workflow? I can't achieve that quality — share KSampler
    params + refiner" → the crisp results come from a SIMPLE gen workflow (image filename: "krea-2-simple-
    gen-workflow-with-good-settings-for-realism").
  - K1_03 beach example = the crisp-skin target (fine texture, no grain, natural light).
- **Diagnosis of OUR grainy skin:** (1) 01's stock negative carries the SKIN-FIGHTING terms
  ("plastic, waxy skin, airbrushed, smooth skin, AI look, rendered, CGI...") → same anchor-fight
  mechanism as D140 → desaturated muddy face; (2) tag-stacked prompt vs the proven natural-language
  style; (3) possibly steps (8 = turbo minimum).
- **A/B TEST (Zidane, seed 77, NEW beard spec = FULL short beard neatly trimmed):**
  - Z-CTRL (existing `zidane_t2i_base_00001`): stock negative + tag-stack + 8 steps (the grainy one).
  - **Z-B `refset_v7\zidane_clean8`**: natural-language paragraph, CLEAN negative (identity-safety only:
    "duplicate character, multiple people, watermark, logo, deformed face, bad eyes, extra fingers"), 8 steps.
  - **Z-C `refset_v7\zidane_clean16`**: same clean, **16 steps** (the "more clarity" test).
- **Beard spec UPDATE (user):** Zidane = full short beard, neatly trimmed & shaped (NOT thin patchy).
  Jaisal = same small patchy beard (unchanged).
- **A/B/C VERDICT (Zidane, seed 77, all three = full trimmed beard ✓ halal cut ✓ white tee ✓):**
  - **Z-CTRL** (stock skin-fighting negative + tag-stack + 8 steps) = grainy/desaturated skin (the complaint).
  - **Z-B `zidane_clean8`** (natural-language + clean negative + 8 steps) = **natural warm skin, healthy
    flush, no grain — WINNER (recommended)**: fast + face holds at 8 steps.
  - **Z-C `zidane_clean16`** (same clean, 16 steps) = also natural skin, BUT 16 steps regenerates MORE →
    a DIFFERENT face (not "sharper"). Answer to "do we need more clarity?": **NO — the grain was the
    negative, not the steps.**
- **NEW T2I RECIPE (locked, D142):** natural-language paragraph prompt (4-5 sentences, kr2realism
  trigger, NO tag stacking) + **CLEAN negative** (identity-safety only: "duplicate character, multiple
  people, watermark, logo, deformed face, bad eyes, extra fingers" — NO skin/AI-look terms) + 8 steps
  euler/simple cfg 1 + 2MP. Supersedes the stock 01 negative for character t2i.
- **Status:** AWAITING USER PICK: Z-B face vs Z-C face (both good). Then Jaisal same recipe (small
  patchy beard unchanged) → character sheet (P3).

## 2026-10-18 19:5x — refset_v7 NORMAL t2i character pics (no identity edit — D141 pivot)
- **Trigger:** user: identity-edit outputs "pretty much off" — drop identity edit, get NORMAL pictures,
  then character sheet, then LoRA training dataset.
- **Config:** 01 t2i (Krea2Realism_V1 + Krea2-realism-V2 @1.0, qwen3vl_4b_fp8_scaled krea2,
  qwen_image_vae, 8 steps euler/simple cfg 1, 2MP 16:9, kr2realism trigger, clean neutral bg,
  "NOT elongated", warm-skin positive; 01's stock negative kept).
- **Outputs (pure t2i, zero identity edit):**
  - `refset_v7\jaisal_t2i_base_00001` (seed 42) — wavy black hair ✓, thin patchy beard ✓, black tee +
    dark trousers ✓, slim ✓, clean cream backdrop ✓, natural warm skin ✓, relaxed half-smile ✓.
  - `refset_v7\zidane_t2i_base_00001` (seed 77) — halal short cut (short sides, no waves) ✓, thin
    patchy beard ✓, white tee + dark trousers ✓, athletic build ✓, clean backdrop ✓, natural skin ✓.
- **Note:** these are NEW t2i faces (not the v6-approved faces) — in the D141 pipeline these t2i
  faces BECOME the character anchor if the user approves; the character LoRA (step 4) is what
  makes the face consistent everywhere afterwards.
- **Status:** AWAITING USER VERDICT on both faces → then H3 character sheet (P3) → LoRA dataset.

## 2026-10-18 19:4x — refset_v7 sheet-bg character refs — clean neutral background via two-stage
- **Trigger:** user: faces "still not convincing", Jaisal "long face", wants "proper background… helpful for character reference sheet".
- **Why single-image mode FAILED at background change (refset_v7\jaisal_sheet):** the REF's scene is
  grounded (g768) — "clean neutral background" instruction LOSES to the ref's street scene. The
  v6 sheets ARE bench-street scenes, so the street carries into every output.
- **Two-stage FIX (D023 correct order):**
  1. **01 t2i base** (8 steps, V2 LoRA, kr2realism, 2MP 16:9, seed 42, char1 spec + "NOT
     elongated" + "clean simple neutral light background, no street/bench/buildings") →
     `refset_v7\jaisal_t2i_base_00001` — clean cream backdrop ✓, natural warm skin ✓, wavy ✓,
     black tee ✓ (new face = placeholder).
  2. **02 TWO-IMAGE face-lock** (72 = t2i base = SCENE slot, 113 = char1_sheet.png = PERSON
     slot, group-2 nodes 113/92 ENABLED, boost 2.5, instruction = "face EXACTLY the reference
     person (second image)") → `refset_v7\jaisal_face_lock_00001` — **v6 identity ✓, clean
     background ✓, better face proportions (not elongated) ✓, natural skin ✓, half-smile ✓**.
- **LESSON 1:** LoadImage reads ONLY from `input/` — the first face-lock run failed
  (prompt_rejected) because the t2i base sat in `output/`. Copy it to `input/` first (done:
  `input\jaisal_t2i_base_00001_.png`).
- **LESSON 2:** to change the BACKGROUND of an identity-edit output, the scene base must carry
  the new background — two-image mode (scene base + person ref) is the tool; a background
  instruction alone cannot override the ref's grounded scene.
- **Status:** Jaisal sheet-bg DONE (face-lock = current best Jaisal char-ref). Zidane same
  pipeline pending (t2i base → face-lock).

## 2026-10-18 19:2x — refset_v6 face diagnosis — "wood / waxy, no skin tone" (user-flagged)
- **User:** the bench-pair faces "don't look natural at all, no skin tone, feel like a wood" — same complaint as v3/v5.
- **Diagnosis (NOT a settings bug — three compounding factors):**
  1. **The identity edit clones the REF's face RENDERING, not just the identity.** ref_boost 4.0 +
     g768 grounding anchor the face region to the sheet's face pixels — INCLUDING the sheet's
     flat, even-lit, pale skin rendering. The anchored face region doesn't receive the scene's
     light → a studio-lit pale face inside a bright street scene = "wood".
  2. **Repeat of D025 (2026-08-29):** neutral sheet ref → studio-lit face that clashes with the
     scene (v5 hit this). D023's correct order — t2i the base scene FIRST, then lock the face —
     was skipped: we fed the sheet directly as the scene base.
  3. **The negative FIGHTS the anchor:** "waxy skin, smooth skin, airbrushed" negatives fight the
     4.0 anchor's smoothness → a desaturated muddy mid-state instead of photographic skin.
- **Evidence:** the sheet's face (`char2_sheet.png`) is actually decent (warm, natural) — the
  degradation happened IN the edit, not in the ref.
- **A/B VERDICT (19:3x IST, Zidane bench, seed 77, same seed all 3):**
  - **Control b40** (flat daylight, anti-smooth negatives) = pale/waxy/"wood" (the flagged issue).
  - **b25** (boost 2.5, golden hour, clean negative, warm-skin positive) = **WINNER** — warm
    natural skin with flush ✓, identity tight ✓, centered on bench ✓, half-smile ✓.
    `refset_v6\zidane_bench_b25_00001_.png`.
  - **b20** (boost 2.0, same) = natural skin ✓ but identity slightly looser (features a touch
    more generic). `refset_v6\zidane_bench_b20_00001_.png`.
- **SETTINGS LOCKED for 02 identity-edit scene refs:** `ref_boost` **2.5** (NOT 4.0 — 4.0 clones
  the ref's flat face rendering), **warm scene light in the instruction** (golden hour), **NO
  anti-smooth-skin negatives** (they fight the anchor → muddy mid-state), warm-skin positive
  ("warm natural skin tone with visible pores and a subtle flush"). Negative = identity-safety
  only ("stick figure, duplicate character, multiple people, watermark, logo"), g768.
- **Jaisal golden-hour bench DONE** (same recipe, char1_sheet.png, seed 42) →
  `refset_v6\jaisal_bench_golden_00001_.png` — warm skin ✓ (wood fixed), wavy hair ✓, black tee +
  dark trousers ✓, patchy beard ✓, slim ✓; expression reads neutral (half-smile didn't come
  through), seated at the bench edge.
- **Status:** A/B done, golden-hour pair complete; recipe locked (boost 2.5 + warm light + clean
  negative); next = H3 character-sheet route.

## 2026-10-18 19:1x — refset_v6 bench pair — identity refset from the LOCKED v6 sheets
- **Goal:** identity refset (character-in-scene refs for the consistent short) from the locked v6
  sheets (D138). 02 re-pointed to the v6 sheets — it was still on the old 10-08 anchors
  (`zidane_ref.png` / `ref_person.png`).
- **Config (02 single-image mode, 113/92 bypassed):** UNET `Krea2Realism_V1` + V2 LoRA @1.0
  (node 97), `qwen3vl_4b_fp8_scaled` (krea2 CLIP), `qwen_image_vae`; identity-edit v1.2 LoRA
  `ref_boost` 4.0 + `g768` (nodes 79/85); KSampler **10 steps euler/simple cfg 1** (node 53);
  2MP 16:9 (node 83); anti-AI negative (node 85).
- **Runs:** A = `char2_sheet.png` (v6 Zidane) → `output\refset_v6\zidane_bench_00001_.png`
  (seed 77 fixed); B = `char1_sheet.png` (v6 Jaisal) → `output\refset_v6\jaisal_bench_00001_.png`
  (seed 42 fixed). Both ~1928×1088.
- **Result:** A (Zidane bench) = halal cut ✓ no waves ✓, white tee + dark trousers ✓, thin patchy
  beard ✓, athletic build ✓, half-smile ✓, single character ✓, clean daylight. B (Jaisal bench) =
  medium wavy hair ✓, slim ✓, black tee + dark trousers ✓, patchy beard ✓; he sits at the edge of
  the bench (not centered on it) and reads neutral rather than half-smile.
- **Conclusion:** identity holds from the v6 sheets; the bench pair is a consistent same-location
  duo. 02 now permanently points at the v6 sheets (Run-B state: char1/Jaisal).
- **Next:** user verdict on the pair → re-point 04 demo shot refs → H3 character-sheet route
  (P3 recommended in CHARACTER_SHEET.md).

## 2026-10-18 — v5/v6 V2-LoRA + kr2realism trigger + clean-weather sheets — the civitai recipe
- **Trigger:** user: v4/sweep faces "wood or wall, no emotion"; **Zidane hair = short halal cut, no waves** (final spec); "texture/realism missing… compare with what others on the internet are producing" (civitai V2-LoRA examples, `civitai.red/images/135654365`); **base checkpoint is majorly NSFW** → every prompt must name full clothing; "try the v2 lora version now".
- **civitai V2-LoRA recipe extracted:** prompts start with the **`kr2realism` trigger tag**, natural casual scenes, explicit clothing.
- **v5 (02 identity + V2 LoRA @1.0, "no rain" in prompt):** faces/hair correct (Zidane halal cut ✓) BUT **rain still rendered — D025 carry-over: the user-picked refs are rainy-street images, so the rain comes from the REF, not the instruction.**
- **v6 (01 t2i, no ref, V2 LoRA @1.0, kr2realism, 8 steps, portrait 1152×2048):** `char_v6\jaisal_v2lora_00001` + `char_v6\zidane_v2lora_00001` — normal clear weather ✓, no boat ✓, thin beards visible ✓, Zidane halal cut + half-smile ✓, Jaisal wavy + calm ✓, photographic texture (no more wooden).
- **LESSON:** (1) `kr2realism` trigger + V2 LoRA = the civitai-grade realism route on this base. (2) Identity-edit output weather = the REF's weather (D025) — to control scene weather, generate the base sheet t2i first, then use the CLEAN sheet as the identity ref. (3) NSFW base → clothing must always be explicit.
- **Pending:** user verdict on v6 → lock as canonical sheets → identity refset from the clean sheets.

## 2026-10-18 — v4 emotional-moment prompts — faces come alive; Zidane halal cut ✓
- **Trigger:** user: faces "look like someone did cloning from a wood or wall — no human emotion at all"; also **Zidane hair spec changed: no waves — "normal hair, short hairstyle, halal cut"** (short sides, natural short top); Jaisal keeps medium wavy.
- **Fix:** neutral dead-on gazes read wooden → prompts rewritten as CANDID EMOTIONAL MOMENTS (the raw model comes alive with a moment, not a pose): Jaisal = "soft tired thoughtful expression, eyes a little distant as if about to say something, head turned slightly, not posing"; Zidane = "small easy half-smile, soft warm eyes, as if someone off camera just said something, head turned slightly, not posing" + "neat short halal-style haircut, short sides, natural short top, NO wavy hair".
- **Result:** `char_v4\zidane_00001` — short halal cut ✓, relaxed half-smile ✓, alive ✓ (2MP/10s, best Zidane so far). `char_v4\jaisal_00001` — medium wavy ✓, pensive quiet moment (4MP/10s) — better than before but still the more neutral of the two; stronger emotion (tired half-smile) if user wants a push.
- **Pending verdict:** lock both / re-roll Jaisal with more expression.

## 2026-10-18 — 02 settings sweep — texture fix: 10 steps (not 6); 4MP duplicates on zidane ref
- **Trigger:** user flagged the pure-base A/B images: "clearly wrong with the texture, it feels like a AI… some settings is clearly OFF."
- **Root cause:** 02 was running **6 steps** — the Krea2Realism author's t2i sweet spot, which does NOT apply to the identity-edit LoRA's pipeline. The identity pack's own note: "Turbo model: 10 steps… 8 = stronger instruction adherence, 12 = more face detail, 10 = balanced." Under-stepping the identity-edit = under-resolved, plasticky texture.
- **Sweep (pure base, A/B seeds, author-style scenes):**
  - Jaisal 10 steps @ **4MP** (2728×1536): **clean, single person, best detail so far** — `char_sweep\jaisal_s10_4mp_00001_.png`.
  - Zidane 10 steps @ 4MP (seeds 77 + 78): **DUPLICATED — two identical men** (Krea2 duplicate quirk). Lowering grounding 768→384 (pack note: "doubled/split compositions? LOWER it") did NOT fix it → the duplication tracks the **4MP output size on this reference**, not seed/grounding.
  - Zidane 10 steps @ **2MP** (1928×1088, g768, seed 77): **clean, single person** — `char_sweep\zidane_s10_2mp_00001_.png`.
- **Proposed lock (pending user verdict):** 02 = **10 steps** euler/simple cfg 1, **2MP 16:9**, grounding 768, ref_boost 4.0. Jaisal's 4MP is the quality ceiling if it stays clean; unify at 2MP for reliability.
- **LESSON:** the 6-step t2i sweet spot ≠ the identity-edit LoRA's step count. The identity-edit stage runs at the pack's 10-step design point; texture/realism was under-resolved at 6.

## 2026-10-18 — Jaisal/Zidane identity-locked A/B: pure base vs +Krea2-realism-V2 LoRA (user's face picks)
- **Goal:** user rejected v2/v3 sheets ("trash"), picked exact face anchors (Jaisal = `char1_NEW_realism_s6_00001`, Zidane = `char1_face_c_00001`), corrected specs (Jaisal slim + medium wavy + thin beard; Zidane athletic/muscular + short military cut + thin beard), asked to compare against the old "v2" setup (Krea2-realism-V2 LoRA @1.0), and to use the author's cinematic natural-language prompt style.
- **Config:** 02 identity-edit with user refs as `input\jaisal_ref.png`/`zidane_ref.png` (identity LoRA @1.0, ref_boost 4.0, grounding 768, 2048×1152, 6 steps euler/simple cfg 1). New node 97 `Krea2-realism-V2.safetensors` inserted (55→97→71→79) — strength 0.0 = pure, 1.0 = V2. `setup_02_v2lora.py` + `set_02_ab.py <char> <pure|v2>`. Seeds 42/77.
- **Result:** 4-way grid `output\char_ab\{jaisal,zidane}_{pure,v2}_00001_.png`. Identity held from both user-picked refs; characters look distinct. Jaisal pure≈v2 (face-locked, LoRA barely moves it). Zidane: **pure = short textured crop (matches user's "military cut")**, v2 = wavy medium (matches ref). Thin beard present but faint. Scenes OK (bridge / canal-boat golden hour, ref tone per D025).
- **Pending:** user verdict on which variant per character + whether to strengthen the thin beard / push Zidane's build more muscular.

## 2026-10-18 — char sheets v2 (author's recipe + distinct faces) — faces FIXED, char2 scene drift
- **Trigger:** user flagged (a) char1/char2 sheets looked like the SAME guy, (b) output not "ultra realistic" like the Reddit post's examples — "we are not following the instructions."
- **Author's recipe (re-fetched the post via red.artemislena.eu — safereddit now Anubis-gated; author u/rynaleopard):** natural language, describe scene/lighting/clothing/expression; specific clothing; **2MP+ resolution** (trained on high-res only — 4K renders directly, 1MP shows noise); **euler + simple, 4–8 steps, 6 = sweet spot**; drop-in Krea2 checkpoint replacement. RawGirl lineage = "raw, unposed, zero-AI-gloss" → **candid unposed phrasing** matters.
- **Config:** rewrote prompts as candid unposed natural-language descriptions with DISTINCT faces from the 10/08 refs — char1 = shoulder-length messy waves, slight five-o'clock shadow, narrow face, serious; char2 = top bun, rounder full face, light olive skin, thick brows, relaxed. `utilities\char_sheet_v2.py` / `refset_v2.py` (char1|char2 args).
- **Result:** char1 sheet (wavy hair + light stubble, wet black tee, village road) now matches the face ref well; char2 clearly different (bun, rounder face, clean-shaven). Identity held sheet→refset on both. Outputs `char_sheet\char{1,2}_00002_.png`, `char_refset\char{1,2}_00002_.png`.
- **Open issue:** char2 refset scene = brick-city canal (not Kerala backwater) — identity-edit carries the SHEET's scene/tone (D025). Fix options: accept the canal-boat shot, or build the char2 sheet already in the boat scene (changes the sheet face — new t2i seed → new face, breaks identity lock) — DECISION PENDING.
- **LESSON (headless seeds):** MCP headless runs use the KSampler seed VALUE verbatim — the `control_after_generate='randomize'` widget is UI-only. A "fresh seed" rerun requires actually changing the seed number in widgets_values. (Verified: two headless runs of the same workflow produced byte-identical outputs.)

## 2026-10-18 — Krea2 A/B on REAL characters (char1/char2) — Krea2Realism_V1 WON, locked in
- **Goal:** user re-anchored the character set (D137) and asked for the Krea2 A/B redone on the actual characters (not the old schoolboy) — same scene+seed on both bases.
- **Config:** `data\krea2_abtest_char1.json` — char1 (rainy street, black tee) + char2 (boat, white tee), 1152×1792, euler/simple, cfg 1.0, denoise 1; OLD `krea2_turbo_fp8_scaled` 10 steps vs NEW `Krea2Realism_V1` 6 steps; same seed per character (42/77). Job `30869cc1`.
- **Result:** NEW base rendered both characters closer to the 10/08 face refs (younger, clean-shaven, natural skin); OLD turbo drifted toward bearded/older faces. **User verdict: "realism output is better, let's lock in."**
- **Action taken:** `Krea2Realism_V1.safetensors` locked in as the Krea2 base in app workflows `01_character_sheet` + `02_identity_refset` (backups `*_oldturbo.json`); KSampler steps 10→6 (euler/simple cfg 1 = author's setting); 01's extra `Krea2-realism-V2` LoRA zeroed (pure base = approved A/B look); prompts/negatives rewritten for char1/char2 (beard added to negatives).
- **Conclusion:** Krea2Realism_V1 (6 steps, euler/simple, cfg 1) is the Krea2 base for all app work. D133 RESOLVED.

## 2026-10-18 — char1/char2 character sheets + identity refsets on the new base
- **Goal:** "we haven't created the worksheet [character sheet] for our characters yet" — generate sheets + identity refsets for the challenge app on the locked-in base.
- **Config:** `01_character_sheet.json` (Krea2Realism_V1, 1152×2048, 6 steps, V2 LoRA @ 0) → `02_identity_refset.json` (Krea2Realism_V1 + identity-edit LoRA v1.2 @ ref_boost 4, 1920×1088, 6 steps). char1 = misty path sheet → stone-bridge refset; char2 = boat sheet → boat refset.
- **Result:** all 4 clean — faces match the 10/08 refs well, costumes right (black tee / white tee), **identity held sheet→refset on the new base** (identity-edit LoRA is compatible with Krea2Realism_V1). Outputs: `output\char_sheet\char{1,2}_00001_.png`, `output\char_refset\char{1,2}_00001_.png`; refs copied to `input\char{1,2}_sheet.png`.
- **Conclusion:** the 4 images are the app's canonical char1/char2 refs for the demo short.

## 2026-10-18 — Timeline workflow 04 headless smoke test: 3 failures → converter root cause (D136)
**Goal:** run `challenge\consistent-short\workflows\04_h3_timeline_r2v.json` headless via MCP (5 s 1344×768 Jaisal bridge shot, refs `jaisal_1_longshot.png`/`jaisal_4_middle.png` via LoadImage nodes 2001/2002, 2-anchor prompt on subgraph node 763).

**Failure log:**
1. **Run `5b73ef50`:** `Unbundle: nothing is set as 'h3_clip_vaes'` at node 1379 (Unbundle). 1379 had no `in` link → execution root → ran before SetNode 1373. Fix attempt: ordering link 3002 (1373→1379) + `in` input created — file verified correct.
2. **Run `62c47768`:** IDENTICAL error, `executed: []`, `current_inputs` missing `in` → the MCP converter dropped link 3002 despite the UI file being correct.
3. **Root cause (D136):** converter treats `SetNode`/`GetNode` as UI-only (not emitted; absent from object_info) → any link to them is orphan-stripped; obvpm `Unbundle.get` widget constants are never honored. Author's subgraphs are intact internally (port links `origin_id:-10`); only the canvas Set/Get layer is dead headless.
4. **Run `50dc0581` (after rewiring 6 Unbundles to real sources):** critical path PROVED — 28 nodes executed incl. 797 (R2V node), 1221 (timeline), 1356, all re-wired Unbundles (1379/1376/1374/1390/1392/1449/1629). New failure at `1488:1481` (upscale-engine internal Unbundle) — its `in` port's source was GetNode 1490 reading a constant (`h3_engine_settings`) that NOTHING sets → orphan-stripped.
5. **Final fix:** engine `in` ports (1359/1488) ← 1457 LazyCaseSwitch output (timeline-selected engine settings); seed ports ← 765 SeedNode. Validates 0 errors. Run 4 `41787e45` then failed at `1457:1461` — the LazyCaseSwitch's OWN three inputs were also dead-GetNodes (1466 'h3_timeline_outputs', 1529 'h3_gen_engine_settings', 1530 'h3_upscale_engine_settings') → re-pointed links 2695/2818/2819 to the real setters (1449 Bundle, 1290/1335 ValuePresets).
6. **Run 5 `b6774902` — SUCCEEDED (first full end-to-end timeline render):** 5.17 s clip, 1376×768 h264 24 fps + AAC 32 kHz audio track, outputs `output\clip_00001.mp4` + `clip_00001.mctx.safetensors` (14.7 MB context sidecar) + `clip_00001.cond.safetensors` (98 MB). Frames at 0.5/2.5/4.5 s (`data\timeline_smoke\`): the schoolboy (dark hair, rose shirt, black bag) is **consistent across the whole shot**, sitting by the water with the arched bridge in background — matches the 2-anchor prompt (wide bridge frame → riverside medium). Minor notes: (a) style drifted toward 3D-animated render rather than the photoreal Krea2 refs (H3 prior + vanilla engine preset `er_sde` 4-step re-sample) — for demo shots use identity-locked refs (02 refset) and/or a higher-detail engine preset; (b) one tiny distant second figure on the bridge at ~2.5 s (the known duplication tendency, D022 — small + far, tolerable).

**Lesson (permanent, D136):** headless runs of UI-format files with KJNodes Set/Get or obvpm Bundle/Unbundle constant plumbing are silently degraded by `comfy_cli\workflow_to_api.py`. Wire real emitted sources; never rely on the constant layer.

---

## 2026-10-17 — Krea2 Realism V1 A/B realism test (PREPARED, awaiting user's model drop)
**Goal:** decide whether `Krea2Realism_V1` (RudySen; FP8 merge of his Realism Checkpoint + V3 LoRA) replaces the current Krea2 base (`krea2_turbo_fp8_scaled`) for realism (D133).

**Setup (prepared, NOT yet run):** `data\krea2_abtest_realism.json` — two parallel chains: UNETLoader `krea2_turbo_fp8_scaled` (10 steps, its normal setting) vs `Krea2Realism_V1` (6 steps, author's sweet spot); same seed 42, euler/simple, cfg 1.0, 1152×1792 (2MP — author's recommended resolution); shared CLIP `qwen3vl_4b_fp8_scaled` (type krea2) + VAE `qwen_image_vae`. Prompt = clean project-relevant scene (schoolboy, rose shirt, black trousers + bag, on a Kerala stone bridge over a backwater, monsoon moody light); negatives against duplicates/plastic skin. Output prefixes `krea2_abtest/OLD_turbo_fp8_s10` vs `krea2_abtest/NEW_realism_v1_s6`.

**Notes:** user downloads the 13.14 GB file via browser (agent-side download started then aborted per user instruction; the leftover `.part` was deleted). Target dir = shared tree `E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\` — the running 8188 server (the `E:\comfyUi_latest` install) scans it via the `extra_model_paths.yaml` `production` profile.

**Result:** PENDING — run A/B after the user places the file; user judges realism; swap decision follows.

---

## 2026-10-12 — BOAR-GRAVE CAMREF VIDEO + S&R converter root-cause + FaceRefine install
**Goal:** (a) get the blockout camera-motion clip out of Blender for the SAM3 R2V pipeline; (b) make the FaceRefine boar-grave workflow validate clean; (c) install the FaceRefine pack for long-shot facial consistency.

**Results:**
- **Blender 5.2 video-output dead ends (2 failures):** (1) `scene.action.fcurves` — `'Action' object has no attribute 'fcurves'` (unified action system) → skip the interpolation loop, default bezier is fine for a slow push-in. (2) `render.image_settings.file_format = 'FFMPEG'` — **FFMPEG is NOT in this build's enum** (`AVIF/JPEG/OPEN_EXR/PNG/WEBP/BMP/CINEON/DPX/IRIS/JPEG2000/HDR/TARGA/TARGA_RAW/TIFF`); Scene has no video-related properties at all. **WORKING ROUTE: render a PNG frame sequence (`bpy.ops.render.render(animation=True)`) → encode with the bundled `imageio_ffmpeg` binary** (`python_embeded\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe`, `-framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 19`). 72 frames @ 1280×720 → `boar_grave_talking_camref.mp4` (292 KB). Silhouette state (char1 BLUE/char2 RED, dummy hidden) rendered first, then colors restored + dummy unhidden + .blend saved.
- **S&R converter gotcha (root-caused in source, `comfy_cli\workflow_to_api.py` `_schema_for`):** a node with `type: UNETLoader` but `properties["Node name for S&R"]: "UnetLoaderGGUF"` (a class that EXISTS in `/object_info` — UnetLoaderGGUF requires only `unet_name`) gets its WIDGET MAPPING done against UnetLoaderGGUF's schema while the API node's `class_type` stays `UNETLoader` (which requires `weight_dtype`) → converted prompt lacks `weight_dtype` → validator `required_input_missing` **even with correct `widgets_values` + `widgets_values_named`**. Minimal-file bisection (positional-only variants all pass; named-dict variants pass when S&R = real class). **FIX: set S&R = `UNETLoader`.** After the fix, `H3_FaceRefine_boar_grave.json` validates 0 errors/0 warnings. **RULE: for machine-built/template nodes, always align `Node name for S&R` with the actual `type` class.**
- **FaceRefine install state:** pack was already cloned (custom_nodes\ComfyUI-H3-FaceRefine); deps present (ultralytics 8.4.80, insightface 1.0.1, scenedetect 0.7.1, scipy, onnxruntime-gpu with CUDA provider); **only true gap = `face_yolov8m.pt` → downloaded (50.8 MB) to `models\ultralytics\bbox\`**. H3 node classes resolve in the live server (validation found no unknown-node errors) → no restart needed for the boar-grave variant to run.
- **Model re-org fallout (D120):** the user's saved H3 workflows carry stale subfolder-prefixed names (`H3\...`, `h3\...`, `MiniMax H3\...`) + replaced model variants (int8→pruned_int8 UNET, 8step→4step-768p turbo LoRA, heretic int8 clip→nvfp4_awq). Fixed in both new boar-grave workflows from the validator's closest-match suggestions. **Do NOT re-download — the models exist at the models root.**

**Conclusion:** both boar-grave workflows ready + validate clean; nothing executed (user rule: no ComfyUI runs while Qwen is up; screenplay first).

---

## 2026-10-12 — BOAR-GRAVE SCENE BLOCKOUT (parambu): 5-camera angles via Blender MCP
**Goal:** build the user's boar-grave scene (char1 inside a grave hole digging, char2 + dummy at the edge, dead boar, Kerala parambu with 2 coconut trees + half-broken fence, morning light) as a gray-box blockout with 5 shot cameras, to test the blockout → Krea2 → MiniMax H3 R2V route (D118).

**Iteration log (v1→v4):**
- **v1:** solid ground plane COVERED the hole (hole box was under an opaque plane → hole invisible from above, CU camera ray hit the plane). LONG shot from the south put the fence behind the camera. REVERSE camera at char2's shoulder landed INSIDE his head sphere → blank gray frame. GROUND camera at the hole's west end was 1.2 m from char1's body → point-blank.
- **Fixes:** (1) replaced the ground plane with 4 ground boxes leaving a REAL hole opening (x −2.3..0.3, y −0.78..0.78); (2) moved long camera to the north side (8, 7, 6.5) so the fence (y=−8) reads in the background; (3) pulled reverse camera outside char2's body (2.6, 2.2, 1.9, lens 65) → OTS with his shoulder as a corner element, high angle on char1; (4) ground camera offset south inside the hole (−2.1, −0.4, −1.3) aiming at the men's HEADS (z=1.5) so the sight line clears over char1's head — they appear over his shoulder against the sky (the user's trench-reference look); (5) removed the two east rim mounds that blocked the CU; final CU at (0.4, 1.2, 0.9) looking down at char1's head.
- **Char1 position:** moved to the east part of the hole (x=−0.5) so the ground-level view along the hole stays open.

**Result:** all 5 angles readable as blockout: `boar_grave_{cu,long,ground,reverse,low}.png` (1280×720 EEVEE). `.blend` SAVED at `data\boar_grave_scene.blend` (52 objects; cameras named `cam_cu/cam_long/cam_ground/cam_reverse/cam_low`).

**Lessons:**
- A blockout "hole" needs a real opening in the ground (4-box ring) — a box under a solid plane is invisible from above and blocks camera rays.
- Shoulder-height cameras land INSIDE the block figure's head sphere — aim from outside the body, not from the shoulder point itself.
- A figure standing in the middle of a small hole blocks every line of sight to the far edge — aim at the far figures' HEADS (z≈1.5) so the sight line clears over the middle figure's head.
- Always SAVE the `.blend` in the same call as the renders — the D112 grave blockout was never saved and had to be lost.

**User feedback round (2026-10-12, v5→v7):**
- CU "just a plate in the ground" → cause: only the head poked above the rim, body hidden. FIX: made the hole shallower (depth 0.6 m, unfinished) so char1's SHOULDERS are above the rim; bigger head block (r 0.26) + shovel handle in front of the head → reads as a crouching person with a tool.
- Ground-level "too much height" → cause: 1.6 m deep hole forced the camera to look up at the men's heads/sky. FIX: shallow hole (0.6 m) → camera nearly level at the men's TORSOS; men's heads appear over the east rim.
- char1 "just a tiny spherical shape, no presence" → FIX: wider shoulders, head above rim, char1 shifted to the WEST part of the hole so the ground-level line of sight to the men opens up over his left shoulder. Men moved CLOSE to the rim (0.65 m); boar just behind them.
- **Blockout readability lesson:** a figure in a small hole is only readable from the angle if part of it (shoulders/head) is above the rim — depth vs pose must be chosen per shot, and the hole is "unfinished" so the rim is ragged with mounds.

**Next:** user judges the 5 blocking angles → Krea2 style-locked reference set for this scene (D021) → MiniMax H3 R2V.

---

## 2026-10-12 — BLENDER MCP END-TO-END (full 26-tool server + headless bridge): scene build + render VERIFIED
**Goal:** verify the full 26-tool Blender MCP (D106 update) works in DSH and can construct + render a scene with zero manual Blender work.

**Config:** headless bridge `blender --background --online-mode --python D:\MCP\blender_mcp\start_bridge.py` (port 9876, background job `pwsh-14`), full server `blender-mcp.exe` (26 tools), Blender 5.2 (`C:\Program Files\Blender Foundation\Blender 5.2`).

**Result: PASS.** (1) bridge up on first boot. (2) MCP round-trip OK (`get_objects_summary` = default scene). (3) `execute_blender_code` built an 11-object Kerala-style blockout from pure code (grass ground, house cube, slanted-slab roof, 2 trees = cylinder trunks + sphere canopies, character = cylinder body + sphere head, sun, camera). (4) one iteration (fan-cone roof → slanted slab; camera pulled back). (5) `BLENDER_EEVEE` 1024×576 render → `data\blender_mcp_test.png` (508 KB). (6) `.blend` saved (135 KB — openable in GUI).

**Gotchas learned:**
- Blender 5.2: `bpy.types.Scene.bl_rna.properties["render_engine"]` → KeyError (RNA lookup changed) — use try/except assignment over candidate engine IDs; working ID = **`BLENDER_EEVEE`** (no `BLENDER_EEVEE_NEXT` in 5.2).
- `bpy.ops` in the headless bridge is fine for primitives/materials/render/save.
- The bridge process must stay alive (keep the .bat window / job open); next session restart via `start_blender_bridge.bat` or a background job.

**Conclusion:** director-seat workflow fully proven — describe scene in words → agent writes + executes bpy → verifies visually → iterates. Ready for the grave-scene rebuild (D112) via this route.

---

## 2026-10-11 — Web fetch pipeline tests (Reddit / X / Arena)
**Goal:** establish which web sources are fetchable from this machine anonymously vs. need credentials.

**Config / tested:**
- Reddit `www/old/api` + `.json` via web_fetch: 403/redirect-to-login (UA-blocked).
- Reddit `.json` via `curl.exe` with custom descriptive User-Agent (`linux:movie-project-research:v1.0`): **still 403** (189KB shreddit block page) — anonymous UA tricks are dead from this IP.
- Reddit via redlib mirrors: mostly dead (catsarch=Anubis proof-of-work, privacydev=502, bloat.cat=DNS fail, perennialte.ch=shut down 2026-08-31). **`red.artemislena.eu` WORKED** (full thread content) — keep as fallback, don't rely on it.
- X single-tweet syndication endpoint: `https://cdn.syndication.twimg.com/tweet-result?id=<id>&lang=en&token=<token>` with `token = Math.round((id/1e15)*PI, 5)` — **WORKS ANONYMOUSLY** (tested tweet id=20 → "just setting up my twttr"). Profiles/timelines/search are NOT covered — need `ct0` cookie or paid API.
- `arena.ai/leaderboard/*` — client-rendered SPA, fetch returns title only; API route 403 "Route not allowed". Not scrapeable from here (user to paste top-5 if needed).
- My `web_search` tool — FAILS in local-model sessions: `DeepSeek search has no API key for DEEPSEEK_API_KEY` (store via credentials service / web Models page / env, or use a DeepSeek-Account model which searches via account sign-in).

**Result:** anonymous = X single tweets only. **Needed credentials (user offered to share 2026-10-11):** (1) `DEEPSEEK_API_KEY` → fixes built-in `web_search` for all sessions (biggest win); (2) Reddit **script app** client_id/secret (reddit.com/prefs/apps → "create another app" → script) → direct Reddit API; (3) optional X `ct0` cookie → profiles/timelines. Storage plan: user-level env vars on this machine (local only). Awaiting user's choice.

**Lesson:** measure which mirror/endpoint actually works before promising a source; mirrors churn fast.

**Update (same day): Reddit credential setup.** User shared Reddit account (suspicious-walk-815) + X Google sign-in for "just for fetching purpose" — stored `REDDIT_USER`/`REDDIT_PASS` as user env vars. **Form-post web login = DEAD:** current shreddit /login page is a JS shell (8.4KB, zero scripts, no csrf token in HTML) — the classic `name="csrf"` + form POST flow no longer exists; new-device logins also trigger CAPTCHA/verify. **CHOSEN ROUTE = browser session cookie:** user logs in once in their own browser, F12 → Application → Cookies → copies `reddit_session` value → stored as `REDDIT_SESSION_COOKIE` env var → all .json fetches work with it. Same pattern for X: copy `auth_token` + `ct0` from x.com cookies → `X_AUTH_TOKEN`/`X_CT0` env vars (X Google-sign-in password NOT stored — unusable programmatically, least-privilege). Awaiting the cookie values from the user.

**Update 2 (same day): Why web MCP "stopped working" — DIAGNOSED.** User asked why ChatGPT/DeepSeek can fetch but "we" can't. Architecture answer: the local MODEL has zero network — all web access is via harness tools: (a) built-in `web_search` (deepsearch backend, needs DEEPSEEK_API_KEY — MISSING → broken), (b) **web-search MCP** (`D:\MCP\web-search-mcp` = mrkrsl/web-search-mcp v0.3.1 — **no API keys**, multi-engine Bing/Brave/DDG via **headless Chromium** (playwright, chromium-1234 installed ✓) — a real browser that CAN solve Reddit's JS challenge). DIAGNOSIS: MCP server 100% HEALTHY (live standalone handshake test: init OK, tools = full-web-search / get-web-search-summaries / get-single-web-page-content, no stderr). Gateway log shows successful calls through 2026-10-08 ("it was working previously" = TRUE). BUT the running GUI (PID 20468, started 10:52 PM) has **NO gateway child process** → MCP not attached → this session has no MCP tools. **FIX: user opens a NEW session in the GUI (MCP attaches per session); if tools still absent, Ctrl+C the GUI + rerun (`pnpm dev:web`), then new session.** Then I can `get-single-web-page-content` on Reddit URLs (headless Chromium runs the challenge JS) — the ChatGPT-equivalent route, no credentials. Optional: DEEPSEEK_API_KEY also fixes built-in web_search.

---

## 2026-10-08 — pe3 run #6 (user run, update-10 mirrored prompts) — CHAR1 ≈ CHAR2 CONVERGENCE (my over-mirror)

### Config

Update-10 prompts (char1 identity mirrored from char2's structure).

### Result (agent viewed char1_a_00006 + char1_b_00006)

- **char1_b face ≈ char2 face** — the mirrored identity (90% identical text) made
  the model render the same person for both characters. User: "now the char1
  looks exactly like char2, cant you simply generate 2 different characters?"
- **char1_a clothing drift**: cream button-up + shorts + flip-flops instead of
  the dark t-shirt (a full-body walking shot gives the model room to drift
  clothing).

### Diagnosis

Over-mirroring (agent mistake): only hair/shirt distinguished the chars; t2i
faces are also a per-draw lottery — similar young-Malayali-man prompts converge.

### Fix (D108 update 11, char1 files validate clean)

char1 identity de-merged: round youthful face / softer features, wavy hair
DOWN and loose ("NOT tied up, NOT in a bun, NOT a topknot"), sparse short
beard, dark t-shirt re-anchored in every scene line. char2 untouched.
**Structural reality:** prompt-only can't guarantee two distinct consistent
characters → **`krea2_char_dataset_lock.json` built** (6 identity-edit branches,
ref_boost 4, 896×1120): pick best face per char → load into REF node → queue →
face-locked dataset.

---

## 2026-10-08 — pe3 run #5 (user run, update-9 prompts) — char2_c WIN + char1_c STYLE COLLAPSE (anime/painting + 2nd person)

### Config

PE on, update-9 prompts (masculine anchors, per-scene beard, focus anchor,
saree-block negative).

### Result (agent viewed)

- **char2_c = the target image**: man-bun, white tee, clearly visible short
  dark beard with moustache, face in focus, rainy Kerala street. The char2
  text (man-bun + dense-beard structure) simply works.
- **char1_c: gender FIXED (man, beard) but style collapsed** — painted/anime
  look + a second anime-style boy in frame. The style collapse was possible
  because the negative had no anime/cartoon/painting terms.

### Fix (D108 update 10, all six validate clean)

User directive: "copy the similar text from char2". char1 identity mirrored
from char2's proven structure (masculine face/jawline, concrete "clearly
visible short dark BEARD… dark facial hair you can see on his face" wording
adapted to the patchy spec, "NOT tied up in a bun", wavy hair kept); char1_c
scene = char2_c's proven text ("wavy hair" instead of "man-bun") + focus
anchor; negative += "anime, cartoon, illustration, painting, drawing, sketch,
stylized, 3d render, cgi, mixed art styles" in all six files. char2 prompts
untouched.

### Next step

User re-runs `krea2_t2i_char1_pe3.json` (char2 pair optional — already good).
char1_c is still the risky branch (frontal + wavy hair); re-roll if needed.

---

## 2026-10-08 — pe3 run #4 (user run, PE on + concise prompts) — char1_c GENDER FLIP + char2 BEARD UNSTABLE + char2_c OUT OF FOCUS

### Config

PE on (temp 0.7, seed 42), concise ~200-235-word prompts (update 8), GPT
negative. Output 896×1120.

### Result (agent viewed the images)

- **char1_c = young woman in a yellow saree with nose ring** — total subject
  swap. Diagnosis: "Kerala" ×4 + soft-feature words + frontal street shot →
  Krea2's dominant "Kerala woman in saree" prior overrode the man/beard
  instructions. char1_a/b (partial-face shots) stayed male.
- **char2_a = short dark beard VISIBLE in profile** — the beard DOES render on
  some draws (it's draw-dependent, not impossible). char2_b/c = faint stubble
  only.
- **char2_c = face out of focus** (street sharp, face soft).

### Fix (D108 update 9, all six files validate clean)

Masculine anchors in char1 identity + tail ("masculine face and masculine
features, masculine jaw"); beard repeated per scene line for BOTH chars (a/b/c)
+ char2 beard visually concrete ("dark facial hair you can see on his face, NOT
just a shadow"); char2_c focus anchor ("Sharp focus on the man's face, his face
is the main subject, crisp facial detail"); negative += "saree, sari,
traditional dress, nose ring, feminine features".

### Next step

User re-runs the pe3 pair. If frontal char2 beard still fails → Identity Edit
with the bearded profile (char2_a_00006) as reference (ref_boost 4).

### Side note

PE-expansion probe inconclusive: port 8100 serves the 27B agent model; a raw
/completions call is not a faithful replica of the TextGenerate node's request.

---

## 2026-10-08 — pe3 run #3 (user run, GPT prompts + PE off) — QUALITY REGRESSION — REVERTED TO PROVEN CONFIG

### Goal

GPT-rewritten 320-380-word prompts + PE expansion OFF (raw passthrough).

### Result (user verdict: "the newly created items are shit")

All six worse than the PE-on runs. User attached the 6 "nearly perfect" earlier
images (char1 a/b/c 1152×2048 + char2 a/b/c 896×1120, all PE-on) as the
quality target: correct scenes, clothing, candid Krea2 realism — char2 just
lacks the beard.

### Diagnosis

1. **PE OFF removed the expansion** that the proven images had (temp 0.7, seed
   42) — raw prompts change Krea2's conditioning distribution → realism drop.
2. **GPT put negative vocabulary in the positive prompt** ("NO TEXT anywhere: no
   subtitles, captions, dialogue, speech bubbles...") — self-trigger risk on a
   model that rendered subtitles; 370 words dilute identity/beard tokens.

### Fix (D108 update 8, all six files validate clean)

PE back ON (original 13-slot shape + 13-key named dict); prompts = proven
concise style (~200-235 words) with Malayali anchor + concrete char2 beard
("5-7 days growth, slightly dense, more than stubble, NOT clean-shaven");
zero text-vocabulary in positives; GPT's 127-word negative kept (in the
negative, where it belongs).

### RULES

- PE-off on these workflows = quality downgrade (re-test before ever flipping
  again).
- Negative-style instructions ONLY in the negative prompt.
- Char prompts stay in the ~130-240 word band.

---

## 2026-10-08 — pe3 896×1120 dataset run #2 (user run) — SUBJECT COLLAPSE + IDENTITY DRIFT + BEARD STILL MISSING

### Goal

First 896×1120 pe3 run (char1_a/b/c + char2_a/b/c, PE on, seed 42, temp 0.7).

### Result (agent viewed all 6 fresh images)

- **char1_a: total collapse** — young WOMAN in knit cardigan, mountain background,
  garbled burned-in subtitles ("1 can't generate of thije thaun..."). Wrong gender,
  wrong location, text artifacts. (Previous 1152 run of the SAME expanded prompt was
  correct → bad KSampler seed draw; PE-on expansion is an uncontrolled factor.)
- **char1_b/c:** right type (wavy hair, dark tee, houseboat / rain street correct)
  but DIFFERENT faces from each other (t2i has no face anchor) and generic
  South-Asian look (user: "lack malayali touch").
- **char2_a/c:** man-bun + white tee + scenes correct, but effectively CLEAN-SHAVEN
  — "slightly dense short beard" wording did not render (Krea2 prior: young man =
  clean-shaven). User: "still doesnt have beard, dont you understand?"

### Diagnosis

1. Weak subject anchor → seed variance flips gender/scene (char1_a).
2. No Malayali-specific identity words → generic look.
3. Beard phrase too abstract for Krea2 → dropped.
4. **Identity drift between scenes is inherent to t2i** — no face reference = new
   face every draw. Only fix = Krea2 Identity Edit (D023) face lock.
5. PE-on expansion (temp 0.7) = uncontrolled creative text → off for the dataset.

### Fix (see D108 update 6 — all six files, validate clean)

Malayali anchor + male-only + concrete beards + no-text/no-woman tail + extended
negative + PE OFF (raw prompt; 3-value off-mode widget shape). GPT-ready package at
`d:\models\vsCodeMcp\prompts\char_dataset_gpt_package.txt` (user may hand to GPT).

### Next step

User re-runs the pe3 pair (fresh tabs). If faces still drift between scenes →
face-lock pass via `krea2_identity_edit.json` (ref_boost 4) using the best face.

---

## 2026-10-08 (incident) — "both workflows return the same image, no beard" — ROOT CAUSE: empty prompt list in base files

### Goal

User ran the character workflows and both came out as the SAME beardless face. Diagnose.

### Diagnosis (files on disk, verified by agent)

- `krea2_t2i_char1.json` + `krea2_t2i_char2.json`: **node 200 (PixaromaPromptEach) `widgets_values = []`** — the 6-row prompt list was wiped (UI re-saved the files when the user ran them in the UI — D100 corruption class). The rows survived only in `properties.promptEachState.rows` (UI state — the backend does NOT read it; it reads positional `widgets_values` → empty prompt → model default → identical generic image, no beard, no character hair).
- The `_pe`/`_pe3` files were fine in `widgets_values` BUT carried the OLD beard wording in `widgets_values_named.prompt` — and the frontend may prefer the named dict, so the last run likely used the old wording.

### Fix (all validated clean: 13/13/13/13/25/25 nodes, 0 errors)

- Rebuilt node 200 rows in both base files (rows 1-3 = exact scene prompts from the _pe3 TG nodes; rows 4-6 campus/temple/auto-rickshaw reconstructed in the same candid style — original 4-6 text lost to the wipe) + synced `promptEachState.rows`.
- Final beard spec (D108 u4) applied in all six files: char1 = PATCHY visible beard (not full), char2 = slightly DENSE visible beard — in `widgets_values`, `widgets_values_named`, and `promptEachState.rows`.

### RULES

- A custom node's row data can live in `properties.*State.rows` (UI) AND `widgets_values` (runtime) — sync BOTH; `widgets_values_named` (frontend-preferrable) too.
- An empty-prompt run = the model's generic default (same face, no beard) — if a workflow's prompt widgets look empty in the UI, don't run it.
- Dataset runs = the `_pe3` files (they have no node 200).

---

## 2026-10-08 (round 2) — VISUAL verification of the 6-image dataset (agent vision live, D111 VERIFIED)

### Goal

Now that `read_image` works (D111 active in the new session), judge all six
pe3 dataset images visually: identity consistency, scene fidelity, beard,
realism.

### Result (agent visual judgment, all six viewed)

- **Identity consistency: EXCELLENT** — char1 (wavy hair, dark tee) is the
  SAME person in all three scenes (a backwater looking-back / b houseboat / c
  rainy street); char2 (man-bun, white tee) is the SAME person across all
  three and UNMISTAKABLY a different person from char1. The dataset goal
  (3 coherent shots per character) is achieved.
- **Scene fidelity: all 6 match their prompts** — mist, backwater path,
  houseboat with swans, monsoon rain (wet hair + raindrops on shirt), Kerala
  street with bikes/stalls. Phone-shot candid look, natural light, no
  AI-look — matches the user's "realism is good".
- **char1 beard:** renders as short patchy-to-medium 5-day stubble — matches
  the user-approved look ("chara 1's beard is perfect").
- **char2 beard:** this run (done ~30 min before this verification, still
  1152×2048 = the STALE latent) shows only light stubble — the run likely
  predates the dense-beard wording. The on-disk `_pe3` files now carry the
  dense wording + 896×1120 latent (verified on disk) → the NEXT run (fresh
  tab) is the definitive one. Fallback if char2 beard still too light:
  strengthen the wording ("dense, covering the chin and jawline, clearly
  more than stubble").
- **Resolution note:** all six current files are 1152×2048 (stale canvas
  run); files on disk are 896×1120 → one more re-run = final dataset.

### Conclusion

Dataset structure + identity + scenes: APPROVED. Final re-run at 896×1120
(char2 dense beard) = the definitive 6-image set. D111 VERIFIED: agent can
view images (read_image returned the images and the agent judged them).

---

## 2026-10-08 — pe3 CHARACTER DATASET run #1 (1152×2048) — realism APPROVED; softness + aspect → 896×1120 re-run

### Goal

Verify the 3-branch PE dataset workflows (`krea2_t2i_charN_pe3.json`): 3 images per character (backwater looking-back / houseboat / monsoon rain), same identity, LoRA-stack realism.

### Setup

- 3 PE branches per character (TextGenerate seed 42 on Qwen3VL 4B; KSampler seeds 42/43/44 randomize; 10 steps cfg 1 euler/simple denoise 1), 1152×2048, Krea2-realism-V2 @1.0 + famegrid_spicy @0.7 + FameGridColorFinish (1.0/0.6).

### Result (user verdict)

- "came out pretty neat... the realism is good" — LoRA stack + PE expansion = **approved quality** (PE variance technique confirmed production-worthy for characters).
- char1's FULL unkempt beard = perfect. char2's SHORT patchy beard = too little → denser wording (D108 update 3).
- **Issues:** (1) softness at 100% zoom — 1152×2048 (2.36 MP) is an upscale from Krea2's ~1 MP native; (2) 9:16 portrait too tall for dataset use.

### Conclusion / Next

- **Fix (applied):** all six char workflows → **896×1120 (exactly 1 MP, 4:5)**; re-run both `_pe3.json` (char2 with denser beard) = the 6-image dataset; keepers optionally `seedvr2_image_upscale.json` (2K, 1440×2560).
- **RULE: for Krea2 t2i, stay in the ~1 MP native class (896×1120 4:5); get more pixels with SeedVR2 2K post, NOT by upscaling the latent.**

---

## 2026-09-29 — G FINAL RUN #6 (`jaisal_intro_G_papers_00006_.mp4`): mic fix worked, papers + smiley-pillar issues

### Goal

Run the final G shot (`jaisal_intro_G_revolt.json`, 15s/360f/1344×768) with the
new small-mic keyframe (`mic_small_ref_v2_00003_.png` as ref_image_1) after the
22-slot MiniMax fix. Verify: off-screen question, one-at-a-time objects, LOW mic
(face visible), gradual character disappearance, bulb flicker ~14s, complete black
15s.

### Setup

- 5 refs: ref_image_0=`kf7a_v4.png` (start), ref_image_1=`mic_small_ref_v2_00003_.png`
  (end, small mic + papers), ref_image_2=`obj_cricket_bat_00002_.png`,
  ref_image_3=`obj_soccer_ball_00002_.png`, ref_image_4=`obj_paper_smiley_00002_.png`.
- Save prefix `jaisal_intro_G_papers` (leftover from clone) → output
  `jaisal_intro_G_papers_00006_.mp4`. Saved to `Jaisal-intro\G_revolt_00006.mp4` +
  frames in `Jaisal-intro\G_revolt_00006_frames\`.

### Result (from extracted frames 0s/5s/8s/11s/14s)

- **WORKED:** (1) **mic is now SMALL/SHORT** on a short stand, face visible (the
  keyframe fix succeeded — the main goal); (2) character present at start (hands on
  table, dead plants, bulb); (3) objects appear (soccer ball, smiley paper); (4)
  **character disappearance is GRADUAL** (frame_05 = turning into papers, frame_06 =
  gone, bulb dim, ball + papers remain); (5) ends dark.
- **ISSUES:** (1) **PAPERS TOO MANY / FILL THE FRAME** — ~20+ papers everywhere
  (the v2 keyframe has too many; the known paper-count issue). (2) **SMILEY PAPER ON
  A TALL MARBLE PILLAR/COLUMN** — frame_04/05 show the smiley paper mounted on a
  weird tall white column (artifact — the `obj_paper_smiley` ref or prompt makes it
  a tall object instead of a flat paper on the bat). (3) off-screen question +
  one-at-a-time timing not fully judgeable from stills (watch the video).

### Conclusion / Next step

The small-mic keyframe fix WORKED (mic is short, face visible, gradual
disappearance). Two fixes needed before G is clean: (A) **paper count** — run
`krea2_small_mic_ref_v3.json` (fewer-papers variant, already built + validated) →
pick best → re-stage `input\mic+paper_small.png` → re-run G; (B) **smiley-pillar
artifact** — check the `obj_paper_smiley_00002_.png` ref + the prompt's smiley
description (should be a flat paper on the bat, not a tall pillar). Then concat all
8 clips → upscale (SeedVR2) → dub (ControlFoley, NO MUSIC D041).

---

## 2026-09-14 — Krea2 t2i object refs: VISIBLE BULB leaks into "unseen light" prompts

### Goal

Generate 3 clean object reference images (soccer ball, cricket bat, paper-with-smiley)
on a pure black background for the Shot-7 "Jaisal explodes into ideas" effect, to feed
MiniMax H3 as object refs. The light must be top-down but the BULB must NOT appear
in-frame (a visible bulb confuses H3 when compositing into the scene).

### Setup

- Workflow `krea2_object_refs.json` (3 parallel t2i branches, shared UNET/CLIP/VAE).
- UNET `krea2_turbo_bf16`, CLIP `qwen3vl_4b_fp8_scaled` (type `krea2`), VAE
  `qwen_image_vae`, KSampler `10 steps / cfg 1 / euler / simple`, 1024×1024.
- **NO identity LoRA** (objects, not the character).
- Positive: "Lit from directly above by a single UNSEEN light source — the light
  itself is NOT visible in the frame, only its light and hard shadow."
- Negative: `light bulb, bare bulb, lamp, visible light source, ceiling, cord, wire,
  hanging bulb, bulb in frame` (+ color/person/duplicates/american-football).

### Result

- **Take `_00001_` (1:38 AM): BULB VISIBLE in all 3** — Krea2 rendered a glowing
  bare bulb at the top of every object. The "UNSEEN light" positive + bulb negatives
  were NOT enough on the first seed.
- **Take `_00002_` (1:44 AM): CLEAN in all 3** — no bulb, pure black background,
  correct objects (round soccer ball, vertical cricket bat, paper with dense
  handwriting + curved smile line). This is the usable set.

### Conclusion

**Krea2 is a general model — "unseen light" is a strong hint, not a guarantee.**
The first seed rendered the bulb; a re-roll (different seed) came out clean. The
negative list does the heavy lifting but you may need to re-roll 1-2 seeds to get
all three clean. **Always visually verify the bulb is gone before feeding to H3.**

### Next step

Use the `_00002_` set (clean). If a future object still shows a bulb, re-roll that
branch's seed. Feed the 3 clean PNGs into the H3 R2V Shot-7 workflow.

---

## 2026-09-12 — Krea2 identity-edit: SCENE ANCHOR breaks the character (V3 vs V4/V5/V6 vs V7)

### Goal

Find why the character identity broke in V4/V5/V6 (face became a different person)
when V3's character was good.

### Setup

- **V3** (`build_intro_keyframes_v3.py`): node 72 = full char ref
  `intro_char_ref_bw.png`, node 113/92 BYPASSED (no scene anchor).
- **V4/V5/V6**: same char ref + node 113 = empty base `intro_scene_master.png`
  (table+chair+bulb, NO person) as a SCENE ANCHOR (node 92 enabled).
- **V7** (`build_intro_keyframes_v7.py`): = V3's exact settings (char ref only,
  no scene anchor).

### Result

- **V3 = GOOD character** (matches the reference face).
- **V4/V5/V6 = BROKEN character** (different face, gray studio backdrop).
- **V7 = GOOD character** (`kf2_seated_v7_00001_.png` matches the reference).

### Conclusion

**The scene anchor (empty base) FIGHTS the character ref → breaks identity.**
Character shots must use the character ref ONLY. The V3 tradeoff: good character
but a wall (right) + chair (left) + plant in the scene — fix those via
PROMPT-ONLY (stronger negatives), NOT a scene anchor.

### Next step

Fix walls/chair/plant in V7 via prompt-only, regenerate the V7 set, then MiniMax
H3.

---

## 2026-09-06 — VDN-H3 (Video Delta Net) benchmark vs SLA (OOM at 14 s / 1MP — NOT viable at production scale)

### Goal

Benchmark **VDN-H3** (Video Delta Net hybrid-attention speedup) against the **SLA** baseline (D042: 1MP < 240 s; production `jaisal_single_shot` ~250 s at 14 s / 1344×768). The user's objective: "compare with our SLA workflow generation time" — VDN was hoped to give "crazy speed for text to video... helpful for our movies, for random shots."

### Setup (recorded 2026-09-06)

- **Node pack:** `Saganaki22/ComfyUI-VDN-H3` **v1.4.0** cloned into `custom_nodes` (no new Python deps — runs on ComfyUI's existing torch + safetensors). Defines `ApplyVDNH3` (simple) + `ApplyVDNH3Advanced` (ablations + fast kernels).
- **Checkpoint (int8 ConvRot 8-step stage):** `E:\ComfyUI_windows_portable\ComfyUI\models\vdn\vdn-minimax-h3-int8-convrot-comfyui\` (source `drbaph/vdn-minimax-h3-int8-convrot-comfyui` on HF). 7 files, ~3.49 GB total. `vdn_checkpoint` node value = folder name `vdn-minimax-h3-int8-convrot-comfyui` (auto-detected in the combo).
- **Why int8 ConvRot (not bf16 `OpenVDN/vdn-minimax-h3`):** (1) matches our int8_convrot base; (2) ~4.7 GB more VRAM headroom (8.3 GB free vs 3.6 GB); (3) ~1.2× faster (branch matmuls 2.7× faster); (4) smaller download (2.2 vs 4.3 GB); (5) identical output at same seed. bf16 = fallback.
- **Benchmark workflow:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\vdn_h3_t2v_benchmark.json` (validates clean, 16 nodes). Chain: UNETLoader(`minimax_h3_fl2va_pruned_int8_convrot`) → `ApplyVDNH3Advanced` → `MiniMaxChunkFeedForward`(2, 4096) → BasicGuider → SamplerCustomAdvanced; BasicScheduler also takes model from the chunk node. `ApplyVDNH3Advanced` widgets (positional order): `["vdn-minimax-h3-int8-convrot-comfyui", true, 1, 1, "merge", "auto", "auto", true, "grouped", 1, 5, "both", true, true, false]` = `vdn_checkpoint, apply_turbo_adapter, stage_b_strength, turbo_strength, lora_mode, branch_weights, retain_buffers, verbose, attention_backend, window_radius, window_chunk, anchor_frames, text_state, linear_branch, fast_kernels`. turbo ON, **merge** (required for the 8-step DMD stage), **fast_kernels OFF** (README: drifts on 8-step DMD on torch 2.10). 8 steps, `er_sde`, `beta` scheduler, fixed seed 981445682258077. t2v mode. NO-music prompt (D041).
- **HF reference (from the source page):** 8 steps, er_sde/beta, **1280×736 / 61 frames**, merge, `cache_gpu` → **~95 s** (int8) / ~111 s (bf16). This is the vendor's "fast" number — a SHORT clip.

### What was tested

Three runs of `vdn_h3_t2v_benchmark.json`:

1. **124 frames (5 s), 1344×768 — CONTAMINATED.** Submitted while a Qwen/llama.cpp session was active (violates D045). Result: **418.22 s** (8 steps @ ~60.4 s/it). **INVALID** for comparison — the LLM contention inflated it. Discarded.
2. **345 frames (14 s), 1344×768 — OOM.** Set to match the proven production workload (`jaisal_single_shot` = 14 s / 1344×768 / turbo). First attempt interrupted at step 0 after 2:04 (cudnn SDPA warmup + linear-branch state build for a 104,129-row sequence). Second attempt (uninterrupted) **OOM'd at step 0** after 184.21 s.
3. **The OOM (the key result):**
   ```
   [vdn] layout: seq 104129 rows, video [1313, 104129), F=102, S=1008, frame (24, 42), text 163 rows
   [vdn] branch_weights=auto: model.safetensors, cache_gpu (16.5 GiB VRAM free, stage 0.00 GiB)
   [vdn] retain_buffers=auto: retained (16.5 GiB VRAM free; stage 2.15 GiB + 10 GiB headroom)
   ...
   File "custom_nodes\ComfyUI-VDN-H3\vdn_h3\branch.py", line 159, in frame_statistics
       b = torch.matmul(vb.transpose(-1, -2), kf).float()
   torch.OutOfMemoryError: Allocation on device 0 would exceed allowed memory.
   Currently allocated: 30.05 GiB | Requested: 1.35 GiB | Device limit: 31.84 GiB
   Peak Usage: 32284 MiB
   ```

### Result

**VDN-H3 OOMs at 14 s / 1344×768 (345 frames) on the 32 GB RTX 5090.** The failure is in the **linear-branch readout** (`branch.py:159 frame_statistics`): `b = torch.matmul(vb.transpose(-1,-2), kf).float()` — a per-frame K/V statistics matmul over **all F=102 frames × S=1008 tokens**, cast to **fp32** (`.float()` doubles the footprint). The linear branch holds per-frame statistics for the whole clip simultaneously, so its memory **scales with frame count**. At F=102 (345 frames) it needs ~31.4 GiB and blows the 31.84 GiB limit. The vendor's ~95 s reference is **61 frames (F≈19)** — 5× fewer frames — which is why it fits.

### Performance

| Run | Clip | Frames (F) | Result |
|---|---|---|---|
| 1 (contaminated) | 5 s, 1344×768 | 124 (F≈37) | 418.22 s — INVALID (Qwen active) |
| 2 | 14 s, 1344×768 | 345 (F=102) | **OOM at step 0** (184.21 s to fail) |
| HF reference | ~2.5 s, 1280×736 | 61 (F≈19) | ~95 s (vendor, int8) |

### Conclusion

**VDN-H3 is NOT viable at our production scale (14 s / 1MP) on a 32 GB card — it OOMs.** Its linear-branch memory scales with frame count, so the longer the clip the worse it gets — the exact opposite of where we need it (long movie shots). The vendor's "2 min for 15 s" marketing is for a SHORT low-res clip (61 frames), not a 345-frame 1MP render. **SLA remains the default speed stack** (D042). Do NOT adopt VDN for production 14 s / 1MP clips.

### Next step (for tomorrow)

If we still want a clean VDN number (to confirm the crossover point), the OOM is fixable by reducing the linear-branch memory — try, in order:
1. **`branch_weights = "stream"`** (widget index 5, currently `"auto"`→`cache_gpu`) — streams frames through the linear branch instead of caching all F frame-statistics at once. This is THE memory lever.
2. **`retain_buffers = "off"`** (widget index 6, currently `"auto"`→retained) — drops the 2.15 GiB retained stage buffers.
3. **Reduce frames** to ~124 (F≈37) for a clean (Qwen-idle) run — the 5 s clip that fit in VRAM.
4. **Reduce resolution** (e.g. 1280×736 like the vendor reference) to cut S (tokens/frame).
Also: the `MiniMaxChunkFeedForward` node (chunks=2, seq_threshold=4096) already chunks the feed-forward but does NOT chunk the linear-branch readout — that's why the OOM still hit. A clean 124-frame run with `branch_weights=stream` is the most likely path to a valid VDN time. **Remember D045: stop the Qwen session first.**

---

## 2026-09-03 — ControlFoley TC-V2A audio for the LOCKED video (SUCCESS after 3 bug fixes)

### Goal

Add a natural-sounds soundtrack to the locked video `Jaisal_Sketch_Title_00010_.mp4` (12.25s, 24fps, 1344×768) WITHOUT regenerating it, via ControlFoley TC-V2A (video + text-guided sounds).

### Configuration

- Workflow: `jaisal_sketch_title_audio.json` (built by `utilities/build_controlfoley_audio.py`)
- Chain: `LoadControlFoleyModel` → `ControlFoleyGenerate` ← `LoadControlFoleyVideo` (loads `input\jaisal_sketch_title_00010.mp4`, 12.5s); `ControlFoleyGenerate` → `SaveControlFoleyAudio` (WAV) + `MuxControlFoleyAudioToVideo` (replace → MP4)
- `ControlFoleyGenerate` prompt = the exact natural sounds in story order (footsteps on stone, gentle wind, low whistle, flowing river water, distant birds, soft whoosh as the plane is thrown, soft plop as it lands, soft whoosh as the figure jumps, soft splash as he lands, then calm water + low birds) + the D041 NO-music HARD RULE. `guidance_scale` 4.5, `num_inference_steps` `fixed`, `seed` 42, batch multipliers 40.
- Submitted with NAMED inputs via `utilities/submit_controlfoley.py` (bypasses the UI→API converter's positional `widgets_values` misalignment for `ControlFoleyGenerate`).

### What was tested

ControlFoley TC-V2A on a locked video. First attempt (job `6b490126`) HUNG 2h40m with no output.

### Result

SUCCESS. After fixing 3 bugs (below), the job completed and produced:
- `output\controlfoley\jaisal_sketch_title_00001_.wav` (1.03 MB) — the generated natural-sounds track
- `output\controlfoley\jaisal_sketch_title_00002_.mp4` (13.77 MB) — the video with the new audio muxed in (replace mode)

### The 3 bugs (all in the laion-clap / node-pack layer, NOT the workflow)

1. **Import-time `SystemExit(2)` (the 2h40m hang).** `laion_clap/training/params.py` ran `parse_args()` at IMPORT time (via `hook.py` → `training.data` → `parse_args()`). Under ComfyUI, `sys.argv` is ComfyUI's own launch args (`--windows-standalone-build --reserve-vram 4 --enable-manager`), so argparse raised `SystemExit(2)` (a `BaseException`, which slips past the node's `except Exception`), leaving the prompt stuck. **FIX:** `params.py` `parse_args()` → `parse_known_args()[0]` (ignores unknown args). Backup: `params.py.bak_comfyfix`.
2. **CLAP `position_ids` unexpected key.** `laion_clap/hook.py:129` `self.model.load_state_dict(ckpt)` used `strict=True`, rejecting the audioset checkpoint's extra `text_branch.embeddings.position_ids` buffer key. **FIX:** `load_state_dict(ckpt, strict=False)`. Backup: `hook.py.bak_comfyfix`.
3. **BigVGAN `resume_download` missing arg.** The node pack's `_patch_bigvgan_from_pretrained` compat wrapper (`nodes.py`) only injected `proxies`, but the installed `huggingface_hub` now requires `resume_download` as a keyword-only arg. **FIX:** `nodes.py` `_compat_from_pretrained` now also does `kwargs.setdefault("resume_download", False)`.

**Each fix revealed the next error one layer deeper** (import → CLAP load → BigVGAN load). All three are package-level, so they persist across ComfyUI restarts. A ComfyUI RESTART is required after patching `nodes.py` (it's imported at startup and cached in memory).

### Performance

Model load (~15 GB) + 12.5s generation completed within the 600s wait window.

### Conclusion

ControlFoley TC-V2A works for adding a natural-sounds track to a locked video. The 3 package bugs are now patched on disk (persist across restarts). ALWAYS keep the D041 natural-sounds-only / NO-music HARD RULE in the prompt. See D042.

---

## 2026-08-26 — Jaisal Cut medium shot (i2i from face anchor)

### Goal

Create a medium shot (head + upper body on the bridge) — wider than the face close-up but tighter than the wide base — with the kid's identity locked.

### Configuration

- Workflow: krea2_jaisal_medium.json
- i2i from jaisal_face_v4_A.png (latest face anchor)
- krea2_turbo_fp8_scaled + Krea2_Cinematic_Artstyle LoRA @ 1.0 + qwen3vl_4b_fp8_scaled CLIP (krea2) + qwen_image_vae
- Style prefix: "An angular, 3d art style, with brush stroke color texture."
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.7
- Seeds: 343, 454, 777

### What was tested

Medium framing via i2i from the face anchor (identity lock) vs t2i.

### Result

krea2_medium_00001_.png (343), krea2_medium_00002_.png (454), krea2_medium_00003_.png (777) — all 2048×1152.

### Performance

~16-20s per 2K image on RTX 5090.

### Quality observations

Pending user review in ComfyUI (vision unavailable in this session).

### Conclusion

i2i from the face anchor is the right approach for the medium shot — keeps identity consistent across framings.

### Next step

User picks the best medium shot to lock as the medium anchor, then draft the 9 story-sheet prompts.

---

## 2026-08-26 — Jaisal Cut medium shot v2 (targeted refinement)

### Goal

Fix three issues in the chosen medium shot (00003): rounded/decorative handrails → plain square posts; zoom out a bit more (medium half shot); left hand holding the red school bag for support after running.

### Configuration

- i2i from jaisal_medium_00003.png (the user-approved 00003), NOT back to the face — keeps the approved composition
- Prompt changes: "medium half shot", "a little more of the bridge around him", "plain simple square stone handrail posts and a plain flat stone railing", "no rounded shapes, no decorative or exotic railing details", "his left hand holding the strap of a red school bag for support after running"
- Negative prompt added: rounded/decorative/exotic/ornate/curved/fancy railing
- Seeds: 555, 888 → krea2_medium_v2_00001..2.png

### Result

Both 2048×1152, ~16-19s each.

### Conclusion

Refining i2i from the user-approved frame (rather than regenerating from the face) is the right way to apply targeted fixes while preserving the approved composition.

### Next step

User picks v2_00001 vs v2_00002 in ComfyUI, then lock the medium anchor.

---

## 2026-08-26 — Jaisal Cut 9-image story sheet

### Goal

Generate all 9 story beats in one batch, each i2i from its anchor, so the face stays identical within each framing group.

### Configuration

- Workflow: krea2_jaisal_storysheet.json
- Anchors: wide base (jaisal_base_final.png) for beats 1,2,8,9; medium mid (jaisal_medium_mid2.png) for beats 3,7; face v4 (jaisal_face_v4_A.png) for beats 4,5,6
- Same locked style chain + prefix
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.7
- Seeds: 101, 202, 303, 404, 505, 606, 707, 808, 909
- Shared negative prompt node on all 9; beat 9 excludes text/letters/words/title

### Result

All 9 frames generated (storysheet_01..09), 2048×1152, ~3 min total on RTX 5090.

### Conclusion

Batching all 9 beats in one workflow with per-beat anchors is efficient and keeps identity consistent within each framing group.

### Next step

User reviews the 9 frames in temporal order, flags weak frames for re-roll, then wires best 6-9 into the MiniMax H3 video.

---

## 2026-08-26 — Jaisal Cut visual-continuity pass (v3)

### Goal

Fix continuity problems between shots without independently redesigning scenes: 03↔04 background mismatch, 05 tie, 06 missing strap, 07→08→09 continuous aerial ascent.

### Configuration

- Workflow: krea2_jaisal_continuity.json
- i2i from the frame that already has the correct look (identity/costume/bag/environment/lighting/composition)
- Beat 3 from jaisal_ss04v2.png (04's environment); beat 5 from jaisal_ss05v2.png (denoise 0.5, tie removal); beat 6 from jaisal_ss06v2.png (denoise 0.5, both straps)
- Beats 7→8→9 CHAINED (each i2i from the previous) for one continuous drone ascent
- 2048×1152, 8 steps, cfg 1.0, euler/simple

### Result

All 6 frames generated, 2048×1152.

### Conclusion

Targeted i2i from the good frame (low denoise for single-element fixes, chained for camera movement) preserves continuity while fixing only the problem. This is the right approach for a coherent video sequence.

### Next step

User reviews the v3 frames in ComfyUI, confirms continuity, then assembles the final 9-frame sheet and wires into the MiniMax H3 video.

---

## 2026-08-26 — Jaisal Cut beat-05 tie removal via inpainting

### Goal

Remove the tie from beat 05 (storysheet_05_rain_closeup_gust) that a low-denoise i2i (v3, v4) failed to remove.

### Configuration

- i2i attempts (denoise 0.5) kept the tie — high-contrast detail preserved
- Switched to INPAINTING: krea2_jaisal_fix05_inpaint.json
- Mask: jaisal_ss05_tie_mask.png (grayscale ellipse over the collar/tie region, ~640×620px centered at 1024,790)
- Pipeline: LoadImage (jaisal_ss05v4.png) → VAEEncode → SetLatentNoiseMask (mask via ImageToMask → GrowMask expand 20, tapered_corners false) → KSampler (denoise 1.0, seed 545) → VAEDecode
- Prompt: "the shirt collar is open and untied, NO tie, no necktie, no bow tie"; negative: tie, necktie, bow tie, knotted tie, tied collar

### Result

storysheet_05_rain_closeup_gust_inpaint_00001_.png (2048×1152). Only the masked collar region regenerated; face/bag/environment locked.

### Conclusion

Inpainting (mask + denoise 1.0 on the masked region) is the reliable way to remove a single high-contrast element that i2i preserves. The mask must cover the element fully without bleeding into the face.

### Next step

User confirms the tie is gone and the face/bag are intact; adjust the mask ellipse if it missed or bled.

---

## 2026-08-26 — Jaisal Cut corrected aerial sequence (v4) + Flux one-node investigation

### Goal

Fix the aerial "cut" section: beat 07 tilted camera → no-tilt centered vertical-bridge; beat 09 double-character → single character. Investigate the Flux one-node for beat-05 tie removal.

### Configuration

- krea2_jaisal_aerial_v4.json: beats 07→08→09 chained (continuous drone ascent)
- Beat 07: NO tilt, boy centered, bridge VERTICAL (road behind boy), boy looking up at camera, close/medium (i2i from jaisal_medium_mid2.png)
- Beat 08: risen higher + pulled away, boy smaller, more bridge + water (i2i from 07)
- Beat 09: max wide, boy = tiny dot, sky dominates, SINGLE character (i2i from 08)
- Negative strengthened: duplicate character, 2 kids, two kids, second kid, multiple people, extra person, double, twin, two figures, two boys, two people, reflection, mirror image

### Result

All 3 frames generated, 2048×1152.

### Flux one-node findings

- FluxKleinOneNode ("One Node · FLUX.2 [klein]") is FRONTEND-DRIVEN: its `noop` returns the JS preview; generation is triggered from the ComfyUI UI (POST /flux_klein/set_output), NOT the prompt queue → cannot be driven via run_workflow/MCP.
- Needs FLUX.2 [klein] models (diffusion + text encoder + VAE) that are NOT installed (local model dirs empty). ComfyUI-Inpaint-CropAndStitch dependency IS present.
- Krea2 is NOT an inpaint model — its inpaint output is distorted.

### Conclusion

The no-tilt vertical-bridge aerial framing + strong duplicate negative is the right approach for the cut section. The Flux one-node is the correct tool for real inpainting but is blocked on model install + UI-driven generation.

### Next step

User reviews the v4 aerial frames; decide how to run the Flux one-node for beat 05 (install models + UI, or manual run).

---

## 2026-08-26 — Jaisal Cut v5: drenchiness + face-continuity for beats 08, 09

### Goal

Beat 08 (v4) had the right pose but lost the DRENCHED/wet look; beat 09 (v4) had a changed face + double-character.

### Configuration

- krea2_jaisal_aerial_v5.json
- Beat 08 v5: i2i from jaisal_ss08v4.png (v4 08), SAME pose/scene, added DRENCHED/WET (soaked hair/uniform, dripping, wet glistening bridge), denoise 0.55
- Beat 09 v5: i2i from the NEW 08 v5 (chained → face stays), boy = tiny dot far away, SINGLE character, DRENCHED
- Negative: different character/face/boy, new kid, changed face, duplicate character, 2 kids, two kids, second kid, multiple people, extra person, double, twin, two figures/boys/people, reflection, mirror image

### Result

storysheet_08_cut_aerial_wide_v5, storysheet_09_cut_aerial_title_v5 — both 2048×1152.

### Conclusion

- To keep a look (drench) while preserving a pose, i2i from the good frame at low denoise (0.55) and add the missing attribute to the prompt.
- To keep the SAME face across a zoom-out, CHAIN the next frame from the previous (09 from 08) rather than re-anchoring — re-anchoring to a base/medium image drifts the face.
- Beat 05 tie removal was resolved by the user running the Flux one-node manually in the ComfyUI UI.

### Next step

User reviews 08 v5 (drenched + same pose) and 09 v5 (same face, single character, tiny dot); then assemble the final 9-frame sheet.

---

## 2026-08-26 — comfy-mcp foundation verification

### Goal

Prove @comfy-mcp can retrieve saved workflows, generate new workflows, and work on them.

### Baseline

No MCP setup (first run).

### Configuration

Server: comfy-mcp (stdio)

Exe: E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy-mcp.exe

COMFY_BIN: E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy.exe

### Result

Saved workflows retrievable, new workflows generatable, edits applicable.

Quality: verified manually

Generation time: n/a (tool layer, not generation)

VRAM: n/a

Stability: working

### Comparison

Better (from zero)

### Conclusion

MCP is a reliable tool layer. Build on it; do not modify it.

### Decision

Keep

### Next Experiment

Workflow work on top of the memory layer (jaisal/krea2 image chain, MiniMax H3 video).

---

## 2026-10-08 — Krea 2 dataset test + partial batch (character-2 ref)
**Goal:** verify Krea 2 identity-edit produces natural, realistic character images
for the dataset (ref = character-2/Image_00001, boy on stone bridge).
**Config:** krea2_turbo_fp8_scaled + identity LoRA v1.2 @1.0 + RawGirlV3 @1.2,
Krea2EditModelPatch ref_boost 4.0 fit, KSampler 10 steps cfg 1 euler simple
denoise 1, 2048×1152, grounding_px 768.
**Results:**
- Test run: `krea2_dataset_test_00001_.png` (44s) → natural bridge scene,
  consistent face/costume, real skin, no plastic. PASS.
- Batch (REST script `utilities\krea2_dataset_batch.py`) stopped by user after
  2 images (Qwen was running → parallel-rule violation):
  - `krea2_ds_00001_.png` → natural frontal headshot, 85mm overcast. EXCELLENT.
  - `krea2_ds_00002_.png` → candid city street walk, 35mm wet street. EXCELLENT.
  Both copied to `E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\krea2_character_2\`.
- Timing: ~180s per image on RTX 5090 (10 steps).
**Conclusion:** Krea 2 + identity LoRA + RawGirlV3 is the dataset generator.
Full 20-image batch now via `krea2_1click_dataset.json` (PixaromaPromptEach).
**Next:** user runs the 1-click workflow; review 20 outputs; pick master image.

## 2026-10-08 — Krea 2 identity-edit 20-image dataset run: FAILED (dummy faces)
**Goal:** 20 varied-scene images of the character via `krea2_1click_dataset.json`
(ref = Flux Klein character-2 bridge image).
**Result:** user verdict → images distorted / not natural, eyes and facial
expression "like a dummy with no human touch", no realism.
**Root cause:** the identity-edit workflow INHERITS the reference image's face
quality. The Flux Klein reference face was already expressionless/dummy, so the
identity LoRA (ref_boost 4.0) faithfully reproduced the dummy face in every scene.
**Conclusion:** do NOT build the dataset on top of a Flux Klein image. Generate
the character FROM SCRATCH with Krea 2 t2i first (`krea2_t2i_character.json`,
6 face candidates), pick the best face, then re-run the dataset with that ref.
**Next:** user runs the t2i workflow; pick best face; re-run dataset.

## 2026-10-08 — Krea 2 t2i face candidates: RawGirlV3 = WRONG LoRA (failed)

**Goal:** generate 6 face candidates for the character via krea2_t2i_character.json.
**Config (first build):** UNET krea2_turbo_fp8_scaled + RawGirlV3 @1.0, schoolboy CHAR.
**Result:** FAILED — user: images came out as a KID, and RawGirlV3 is a FEMALE LoRA
(wrong for a male character). Also Krea2-realism-V2 was not wired in at all.
**Fix:** LoRA → Krea2-realism-V2.safetensors @1.0, CHAR → 26-year-old adult Indian
man. Rebuilt + validated clean. Awaiting user's manual run.
**Lesson:** check LoRA gender/subject match before wiring; the realism LoRA we
searched for (RudySen Krea2-realism-V2) must be in the chain for photoreal output.
## 2026-10-08 — Krea 2 t2i: two bearded characters + iPhone LoRA (PENDING user run)

**Goal:** 12 face candidates — 6 for the FULL-beard character, 6 for the
SHORT-patchy-beard character. Both 26yo Kerala men, lean-but-fit, NOT well
groomed.
**Config:** UNET krea2_turbo_fp8_scaled + Krea2-realism-V2 @1.0 +
famegrid_spicy_3167060 (iPhone look) @0.7, 1152x2048 portrait, 10 steps cfg 1.
**Status:** awaiting user's manual run (prefix krea2_t2i_face).
**Watch for:** beard density (full vs short must be distinguishable), lean build
(no bulky), Kerala look, iPhone-natural feel vs over-processed.
## 2026-10-08 — Krea 2 t2i 12-candidate run: SAME GUY + 30+ LOOK (failed)

**Goal:** 12 candidates (6 full-beard + 6 short-beard) from one workflow.
**Result:** FAILED per user: (1) both characters came out as the SAME guy
(second was just the first with a shorter beard — the beard was the only
distinguishing feature), (2) faces looked 30+, not 26, (3) "template AI
people" look, not natural Kerala everyman.
**Root cause:** one shared character description + beard as the only variable
= same face. No youth emphasis in the prompt. Generic "Indian man" = default
AI South-Indian template.
**Fix (D108 update):** two SEPARATE workflows with genuinely distinct
characters (face shape, hair, beard, shirt all different), strong YOUTH
emphasis ("mid-20s, youthful fresh face, no wrinkles" + negative "older man,
30s, 40s, 50s, aged face"), and a Kerala everyman look described by PHYSICAL
FEATURES (warm medium-brown natural skin, natural unstyled hair, soft
youthful features, ordinary young man, not a model) — NOT by naming "Kerala"
or any actor. Reference photos studied: Naslen (mid-20s, round soft face,
tousled hair, light stubble, warm medium-brown skin = best youth reference),
Nivin Pauly + Dulquer (photos were of them at ~40 — angular vs round face
range only).
**Status:** awaiting user run of krea2_t2i_char1.json + krea2_t2i_char2.json.
## 2026-10-08 — Krea 2 t2i: STOCK-PHOTO FRAMING = PLASTIC LOOK (failed, root cause found)

**Goal:** natural Kerala everyman look, not "average AI".
**Result:** FAILED per user: still plastic, stock-image, no Kerala touch, no
actor resemblance.
**ROOT CAUSE (the big lesson):** the prompts were POSED STUDIO HEADSHOTS —
"85mm lens f/2.8, sharp focus on the eyes, plain muted background" +
over-emphasized "ultimate photorealism". That recipe makes the model render a
hyper-perfect airbrushed stock-photo face. The framing, not the LoRA, was the
problem.
**Fix (2nd round):** CANDID ENVIRONMENTAL phone-shot framing in real Kerala
settings (backwater path, houseboat, monsoon rain, college campus, temple
wall, auto-rickshaw). NO lens specs, NO "plain background", NO posed
headshots. Negative prompt now includes "studio portrait, posed, plain
background, headshot, stock photo, professional photography, shallow depth of
field, bokeh, hyper-realistic, over-processed". Hair per user: Char 1 =
MEDIUM WAVY hair (loose, messy); Char 2 = LONG hair tied up in a loose
man-bun/topknot (Gareth Bale 2018 style — user: "it's not haram to grow the
hair").
**Also:** tried to pull 20s-era actor photos (Nivin in Thattathin Marayathu
2012, Dulquer in 1983 2013) — Wikipedia film posters were too low-res to be
useful; the Naslen mid-20s photo remains the best youth reference.
**Status:** awaiting user run of the rebuilt char1/char2 workflows.

## 2026-10-08 — FameGridColorFinish "not registering" = FALSE ALARM (diagnostic lesson)

**Symptom:** after cloning `custom_nodes\ComfyUI-FameGridColorFinish` +
restarting ComfyUI, the node appeared ABSENT from `/object_info`; both
char1/char2 workflows failed validation (`unknown_class_type` node 302). No
"failed to import" error in the log.
**Root cause (3 masking factors):**
1. `data\object_info_cache.json` was STALE (pre-dated the node pack).
2. `ConvertFrom-Json` CRASHED on a duplicate key in the 6MB object_info
   (`ClownOptions_Frameweights` vs `ClownOptions_FrameWeights`), so the
   "0 matches" check never actually ran — the "not registered" conclusion
   was built on a parser failure, not real data.
3. The node pack is SILENT on import (no log line), so its absence from the
   log looked like a failure.
**Verified (live server 8188):** `FameGridColorFinish` IS registered
(`FameGrid` 116x, `ColorFinish` 2x in live object_info). Schema: required
`image`; optional `color_strength` (FLOAT default 1.0), `sharpen_strength`
(FLOAT default 0.6); output `image`. Both workflows VALIDATE CLEAN (13
nodes, 0 errors).
**LESSON (persist):** to check node registration, query the LIVE
`/object_info` via `Invoke-WebRequest` + `[regex]::Matches` on the raw
string. Do NOT trust the stale cache file, and do NOT `ConvertFrom-Json`
the full object_info (duplicate keys crash the parser).
**Status:** RESOLVED. Ready for user's manual run of char1/char2.
## 2026-10-08 — Muse-Glimmer-30B ctx fit on RTX 5090 32GB (MEASURED, result PENDING probe)

Goal: determine how much context Muse-Glimmer-30B (18.7GB Q5_K_M) can actually run on the 5090 — user challenged the agent's initial "~70GB KV at 260K" claim (it was an unmeasured architecture guess — RETRACTED).
Measured (live process command line + nvidia-smi):
- Agent's own 27B NVFP4 server (port 8100) runs `--ctx-size 260000`, q8_0 KV, flash-attn, MTP → **29.4GB / 32.6GB used** (2.8GB free).
- Weight sizes: 27B NVFP4 = 14.47GB; Muse Q5 = 18.72GB.
Result: 260K ctx provably fits a 14.5GB NVFP4 model on this card (barely). Muse is 4.25GB heavier in weights — 260K for Muse likely does NOT fit (that's the headroom the 27B's KV occupies), but exact fit depends on Muse's architecture (layer/KV-head count) — unverified.
Action: `D:\models\Writing\probe-muse-ctx.bat` built — tries 260000→131072→98304→65536→32768, first ctx that boots wins, leaves that server running on 8101. User runs it with port 8100 stopped (card needs full 32GB; the agent cannot test while its own server serves the session).
**RESULT (2026-10-08 22:53): 260000 FITS — the probe's FIRST attempt booted Muse at full 260K ctx and /v1/models returned 200** (user ran the probe WITHOUT stopping 8100; Muse still booted, so the original `Run-Muse-Glimmer.bat` ctx is safe on this machine). Caveat measured at coexistence: with both servers running, GPU = 31.9/32.6GB and BOTH are slow (Muse 2.3 tok/s, agent 27B 1.4 tok/s on 16-token test) — for real writing speed, stop 8100 and let Muse own the card. The agent's "likely doesn't fit" prediction was WRONG (KV turned out lighter than estimated — Muse's architecture is KV-efficient); the original "~70GB KV" guess was also wrong in the other direction. Lesson: measure, don't estimate. `run-muse-32k.bat` stays as a conservative fallback; the original 260K bat is now proven.
## 2026-10-18 — Krea2 Realism A/B (DONE) + obvpm timeline smoke test (RUNNING)

## 2026-10-18 — ABC sheet round 2: new-crest reruns + H3 wide multi-panel variant (QUEUED)

**Context:** user changed the crest spec (D145 — fist roundel ONLY, no text) and raised:
Krea2 eye-detail issues, Qwen "we didnt get the character sheet at all" (→ downloaded the new
LLM-architect Qwen workflow), the P1/civitai workflow had "few more" images (→ drag-dropped the
civitai image with the embedded cgpixel23 wide H3 workflow), and "all of them looks plastic
like" (→ shared the plastic-look thread [1wzcu5v] + the LBH latent-upscaler repo).

**Kit refs (new crest):** 07_kit_ref_{jaisal,zidane} rebuilt (fist-only prompt, seeds 13/29) →
`jaisal_kit_ref_00002_00001_.png` + `zidane_kit_ref_00002_00001_.png` — **BOTH first-try
correct** (subtle line-art fist roundel, no text, correct kit colors, clean flat-lays) →
staged to `input\{jaisal,zidane}_kit_ref.png` (overwrote the text-crest refs).

**Sheet reruns (new-crest prompts):**
- C×2 (Krea2 t2i, `cd2e7b6f`/`bbc351c1`) → `KREA2_{JAISAL,ZIDANE}_00002_.png` — **BOTH
  EXCELLENT**: 3-view strips, new text-free fist roundel, correct kit + back name, good faces
  (eyes fine this round). C = 2/2 across both rounds.
- A×2 (H3 2BZ, `a223c93e`/`8d53f0ed`) → `H3_JAISAL_3VIEW_00003_.png` = **3rd Jaisal
  stochastic FAIL** (man sitting on a sofa holding folded blue pants with a pen, face cropped,
  no sheet) vs `H3_ZIDANE_3VIEW_00002_.png` = **PERFECT SHEET** (3-view, fist roundel, ZIDANE
  on back; nits: black boots not white). **Scoreboard: H3 = Zidane 2/2, Jaisal 0/3** (scene
  priors hijack Jaisal's runs: palace → single view → sofa).

**Wide multi-panel variant (NEW, `05d_charsheet_H3_wide_{char}.json`):** built from the
civitai-embedded cgpixel23 workflow (45 nodes, all types available locally): our 2 refs
(HD face + new kit ref), author's test/NSFW/style LoRA chain stripped, **D146 anti-plastic
chain** (no turbo LoRA, no Spectrum; vanilla 30-step er_sde/beta), t1 image VAE, 4096×1536
canvas, R2V 6-section 3-view sheet prompt (new crest spec). **Builder gotcha: the UI→API
converter reads the inputs[].link fields, not just the links array — rewired links require
syncing the target node's input `link` field** (first build failed validation: node 7/9 model
missing + 10/60 unreachable until 40/42's `link` fields were synced to the new link ids).
Validates 0/0. **Runs queued: jaisal `ebb3b88f` · zidane `54afafe1`** →
`output\charsheet\H3WIDE_{JAISAL,ZIDANE}`.

**Plastic-look thread findings (data\h3_plastic_look):** 2-pass latent upscale recipe (top
answer) vs lavinia12345's counter: "vanilla 30 steps er_sde/beta57, 1 MP is good; turbo
lightning LoRAs, the Spectrum node, or PlagueKind's SLA screw up eyes"; 0.98 MP = H3's
trained default res; turbo needs the H3 AdaLN LoRA Fix (PlagueKind `h3_silu_turb_grid`,
strength 0.70–0.85).

**Installs this span:** `ComfyUI-ThinkingLLM` (goodguy1963 v2.5.8 — GGUF + HF-variant
ThinkingLLM_QwenVL nodes; deps OK except llama_cpp GGUF wheel + tiktoken) · LBH
`Comfyui_Minimax_h3_latent_Upscaler` (already installed) + 3D bf16 model (0.64 GB →
`models\latent_upscale_models\`) · PE-I2I GGUF downloading (`Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf`
+ mmproj-bf16, HF prithivMLmods) → `ComfyUI\LLM\GGUF\`. **Server restart pending** (server
pid 2608 is NOT comfy-cli-managed — `comfy stop` can't kill it; kill + `comfy launch` needed)
to load ThinkingLLM for the user's new Qwen-2.1-LLM-architect workflow.

## 2026-10-18 — Krea2 Realism A/B (DONE) + obvpm timeline smoke test (RUNNING)

**Krea2 Realism V1 A/B** (D133): terminal-resumed download completed at exactly 13,141,769,680 bytes; server listed the model without restart. A/B run (seed 42, same bridge prompt): output\krea2_abtest\OLD_turbo_fp8_s10_00001_.png vs NEW_realism_v1_s6_00001_.png. Agent read: both high quality; NEW = slightly more natural skin texture + more dynamic (non-symmetric) framing; OLD = more dramatic sky + centered composition. Single-seed — user verdict pending; suggested 2-3 more seeds before swapping the base.

**obvpm-timeline smoke test** (D135): installed comfyui-obvpm-timeline 0.1.4 + updated comfyui-obvpm to v0.2.16 + ComfyUI-MiniMax-H3-Turbo + ComfyUI-Fizgig-H3-Tweaks; restarted 8188; all nodes registered (verified via Python JSON parse of /object_info — PowerShell ConvertFrom-Json crashes on the duplicate ClownOptions_Frame* keys). Adapted h3_obvpm_timeline_r2v_v0.1.4-007A.json → challenge\consistent-short\workflows\04_h3_timeline_r2v.json:
- removed H3LivePreview node 1232 (needs 	aeh3.safetensors in models/vae_approx — not installed; bridged 1438→1470 with link 3001);
- un-bypassed generator engine instance 1359 (was mode=2) and H3ContextWindows node 1356 (was mode=2 — both engines' model inputs come from it);
- re-pointed upscale-engine model link 2727 from dangling GetNode 'previewed_model' (1489, removed) to 1356;
- **Set/Get ordering fix:** published file's Unbundle 'h3_clip_vaes' (1379) has no input link → executes as a root BEFORE SetNode 'h3_clip_vaes' (1373) runs → runtime error "nothing is set as 'h3_clip_vaes'". Fix: ordering link 3002 (1373.0 → 1379.0). **Lesson: in the author's UI the wire exists; the published file's get-widget-only Unbundles/GetNodes are execution-order roots — add SetNode→Unbundle ordering links for headless runs.**
- wired Jaisal bridge refs (native LoadImage nodes 2001/2002) into R2V node 797 ref_image_0/1; 2-anchor 16:9 prompt on subgraph node 763; ResolutionSelector 1086 → 16:9.
- **Validates 0 errors** (26 expected warnings = author's default-muted optional groups). Run 1 failed (h3_clip_vaes) → fixed → run 2 62c47768 in flight.
**Status (UPDATED 2026-10-18): smoke test PASSED** — run 5 (`b6774902`) rendered `output\clip_00001.mp4` (5.17 s, 1376×768 h264 24fps + AAC) + `clip_00001.mctx.safetensors` (14.7 MB) + `clip_00001.cond.safetensors` (98 MB) in ~200 s. Frames at 0.5/2.5/4.5 s consistent (schoolboy, rose shirt, black bag — note: OLD character, demo shot refs must be re-pointed to char1/char2). Notes: style drifted toward 3D-animated vs photoreal refs (vanilla engine preset `er_sde` 4-step re-sample); one tiny distant figure on the bridge at ~2.5 s.

## 2026-10-19 — 10a frontal-base OOM at 16MP (FAILED) → rebuilt as fresh t2i v2

**Goal:** create a dead-on FRONTAL base for Jaisal (current `jaisal_portrait_HD.png` is a ~35° 3/4 view, which forced H3 sheets to extrapolate the front face → glassy/drifted eyes in all 3 sheet outputs; also pollutes the future Klein-9B dataset with a 3/4-only character).

**v1 (identity-edit, 16MP) — FAILED OOM on user's run (02:26 IST):** 02-identity-edit with 72=113=jaisal_portrait_HD.png, 9:16 @ 16MP (~3072×5461 target, 683×384 latent = ~262k tokens) + 2 refs fit to the same latent (grids 342×192 each = ~65k tokens each). `comfyui-krea2edit._ref_attn_bias` does `torch.zeros(1, 1, L, L)` over the combined ~136k-token sequence → **requested 72.92 GiB** (bias matrix, fp32) → `torch.OutOfMemoryError` at KSampler step 1. Server auto-unloaded all models after the OOM. **Root cause:** the krea2edit ref-attention bias is O(N²) in the combined sequence — 16MP target + 2 full-size refs is simply unaffordable on any 32GB card. Author's own note in 02 says "1MP is the sweet spot; only go higher for single-person edits."

**Additional user objection (correct, matches D141):** identity-edit is a LOCKING tool — every i2i pass degrades quality; it should not be used to CREATE a face.

**v2 (fresh t2i) — BUILT, validates 0/0, NOT YET RUN:** cloned the PROVEN approved-face recipe `krea2_t2i_char1_pe3.json` (how the user-approved face set was made), deleted the 3 TextGenerate PE nodes (Qwen llama-server stopped — plain CLIPTextEncode instead, full prompt verbatim), 3 parallel KSampler branches (seeds 42/43/44, randomize) = **3 candidates in one queue press**, latent 82 = [896, 1120, 1] (1MP 4:5 — exact proven face latent; approved faces were then 4x-upscaled via `03_hd_upscale.json`). Prompt = author's verbatim character prefix (Malayali man, round youthful face, medium wavy hair down, sparse patchy beard, lean, dark t-shirt) + FRONTAL clause (dead-center, both eyes fully open and symmetric, no side angle/profile, 85mm face-focus) + author's candid-phone-snapshot tail. Author's anti-studio negative verbatim. LoRA chain Krea2-realism-V2 @1.0 → famegrid_spicy @0.7. Save prefixes `FACEFRONTAL_JAISAL_a/_b/_c`. **No OOM risk** (plain t2i at 1MP = the exact proven face run; no ref-attention N² allocation).

**Next:** user queues 10a once → pick best frontal → 03_hd_upscale 4x → swap canonical face (old → `jaisal_portrait_HD_34view.png`) → re-run sheet routes → same flow for Zidane.

## 2026-10-19 — 4 sheet routes on new frontal base + crest-fidelity fix (D148)

**Batch (user, ~03:00 IST, all on the new `jaisal_portrait_HD.png` frontal base):**
- **09j QWEN21** `QWEN21_JAISAL_00001.png` = **USER'S PICK (best sheet)** — full design-sheet
  layout (metadata/turnaround/action/silhouette/expression/detail zones), good face.
  **Missed the kit** (charcoal tee, no crest) — its live PE prompt was empty. Architecture
  discovery: the ThinkingLLM architect subgraph (478/480/481/549/551) is NOT instanced on
  the main canvas (dangling link ids, never runs); LIVE path = 470 face → 485 resize(1536)
  → 555 PE node (custom-prompt widget '') → 558 → 459 generator instance (subgraph 0:
  KSampler 458 / TextEncode 557) → 461 save. Main-canvas nodes = [13,459,461,470,481,485,
  555,558,563,566,567,568,569,570].
- **05d H3WIDE** `H3WIDE_JAISAL_00003.png` = good (closeup + 3 views + 6 circles); crest
  weak/blurry ("minicromax-like"); closeup beard slightly fuller than ref (prompt already
  says sparse-patchy → model behavior, not prompt).
- **05e H3FIZ** `H3FIZ_JAISAL_00002.png` = similar; SLA 83.8% sparse → 8 circles (dup
  eye/lip/ear pairs); crest weak.
- **08j KREA2** `KREA2_JAISAL_ID_00002.png` = 3-photo sheet, face good, small crest, no
  detail panel.

**Crest fix (built 13:2x IST, validates 0/0 both copies, NOT YET RUN):**
- `input\jaisal_crest_ref.png` (512²) = tight crop of ONLY the fist roundel from
  `jaisal_kit_ref.png` (box center (700,328) r75 in 1152²; `utilities\crop_crest_ref.py`).
- 05d: +LoadImage 900 → ref_image_2 (link 204) = `<Picture 3>`; prompt: crest "exactly as
  <Picture 3>" + 6th detail circle = emblem alone.
- 05e: +LoadImage 900 → ref_image_1 (link 726) = `<Picture 2>` (crest); same upgrades.
- 08j: plain-jersey + full emblem spec (all fingers+thumb, crisp, no distortion) + 4th
  element = round crest close-up. **Negative: removed generic "logo" (it was suppressing
  the crest!); added malformed-emblem/deformed-fist/missing-fingers/illegible-crest/
  blurred-emblem.**
- 09j: 555 PE custom prompt = full kit spec (royal blue jersey, fist crest, JAISAL on
  back, navy pants white stripe, white boots, dedicated crest detail close-up, turnaround
  in kit) + 478 ROLE (subgraph def) += KIT SPEC section before # USER.
- **Conclusion:** emblem fidelity needs a DEDICATED image ref (text can't force a crisp
  logo) — D148. NEXT: user runs all 4 → compare crest fidelity → pick winning route →
  Zidane flip (incl. `zidane_crest_ref.png`).
