# Workflow History

Newest changes first.

---

## 2026-10-19 — BUILT `logo_transparent.json` (VALIDATE CLEAN 0/0, 5 nodes) — transparent-logo (background-removal) pipeline, crest v3 (D145-v3)

**Purpose:** user approved the monochrome 1-fist roundel (`LOGO_FISTS_H3_1fist_00002`) and
asked for an ABSTRACT/transparent version so the crest can be applied to t-shirts of any
color. **Chain:** LoadImage (`logo_1fist_mono.png` — copy of the approved logo, in
`input\`) → **PixaromaRemoveBackground** (`comfyui_fearnworksnodes` pack, BiRefNet) →
SaveImage `LOGO_TRANSPARENT/logo_1fist` (RGBA PNG) + PreviewImage (checkerboard check).
**Model:** `birefnet.safetensors` (424MB) already in
`E:\ComfyUI_windows_portable\ComfyUI\models\background_removal\` — no download.
**Generic:** change the LoadImage filename + SaveImage prefix to process the 3-fist
variant or any future logo. **Status:** built, validated, NOT YET RUN (D150 — user runs).
**Watch:** BiRefNet is a salient-object ML mask — the solid fist is safe; the thin white
ring may soften at edges. Fallback if the ring gets eaten: deterministic color-key
(solid blue background → alpha via PIL) — crisp for logos. On white shirts a white-fill
logo needs a black-fill variant.

## 2026-10-18 — BUILT 8 SHEET-TEST workflows (D144) — `07_kit_ref_{jaisal,zidane}.json` (kit flat-lays) + `05a/05b/05c_charsheet_*.json` (A/B/C routes × 2 chars) — ALL VALIDATE CLEAN

**Purpose:** the user-directed A/B/C character-sheet test (which route wins) + the team-kit refs
(D144: blue/dark-green jerseys, fist-crest "PALESTINE RESISTANCE", name on back, track pants).

**`07_kit_ref_{jaisal,zidane}.json`** — 01-based Krea2 t2i (8 steps D142) → 1152×1152 jersey+track-
pants flat-lays. **Both ran first try** (crest + PALESTINE RESISTANCE text legible).
→ `input\{jaisal,zidane}_kit_ref.png`.

**`05a_charsheet_H3_{char}.json`** (A = 2BZ H3 2-stage, stage 2 OFF): node 16 =
`{char}_portrait_HD.png`, node 21 = `{char}_kit_ref.png`, 22/57/58/59 =
`neutral_placeholder.png`, node 106 = `charsheet/H3_{CHAR}_3VIEW`. **Stage-2-only nodes DELETED
(111/125/126/127)** + the character master prompt injected into **node 24's text** (H3 prompt
slot is linked from 24 — the node's own prompt widget is runtime-ignored). A-jaisal ran:
face+kit excellent, but **single cinematic view, not the 3-panel sheet** (H3 layout weakness).

**`05b_charsheet_QWEN_{char}.json`** (B = LEEBLAAB Qwen Image 2.1): 470 = `{char}_portrait_HD.png`,
459 widget0 = 10-section 7-zone design-sheet prompt (per char), **subgraph internals patched**
(451 = `qwen_image_2.1_bf16`, 453 = `qwen3vl_8b_int8_convrot`, 454 = `qwen_image_2.1_vae_bf16` —
instance widgets are runtime-ignored), 461 = `charsheet/QWEN_{CHAR}`. 30 steps.

**`05c_charsheet_KREA2_{char}.json`** (C = Krea2 t2i strip): 01-based, 300 = 3-view strip prompt
(front/side/back, kit + name-on-back), 82 = [2048,1152], 29 = `charsheet/KREA2_{CHAR}`, 8 steps.

**Builder:** `utilities\make_abc_sheet_variants.py` (regenerates all 6). **Status:** all 6 queued
(prompt ids in CURRENT_TASK.md); A-jaisal done, A-zidane running.

---

## 2026-10-18 — BUILT `03_hd_upscale.json` (VALIDATE CLEAN, 4 nodes) + Real-ESRGAN x4plus model — HD CHARACTER-REF PIPELINE (D142)

**Purpose:** true-HD clarity for character t2i refs (user: "clarity too off — cant we generate HD?").
**Location:** `challenge\consistent-short\workflows\03_hd_upscale.json` (UI format).
**Structure:** LoadImage (1; file in `input/`) → UpscaleModelLoader (2; `RealESRGAN_x4plus.pth` in
`models\upscale_models\`) → ImageUpscaleWithModel (3; input name is **`upscale_model`**, not `model`
— the first version failed validation) → SaveImage (4; prefix `refset_v7/zidane_portrait_HD`).
**Pipeline:** 01 t2i (D142 clean recipe, **portrait 1152×2048 head+shoulders close-up** — the face
framing is the key lever) → copy output to `input/` (LoadImage rule) → run 03 → **4608×8192 (37MP)**.
**Result:** `refset_v7\zidane_portrait_HD_00001` = photo-grade face at ~1:1 (individual eyebrow/beard
hairs, pores, catchlight, no grain).
**Model source:** `https://huggingface.co/schwgHao/RealESRGAN_x4plus/resolve/main/RealESRGAN_x4plus.pth`
(63MB; HF now 401s the original `xinntao/Real-ESRGAN` repo — gated).
**Next improvement:** Jaisal same pipeline; then feed the HD faces into the H3 character sheet (P3).

---

## 2026-10-12 — BUILT `minimax_h3_boar_grave_talking_r2v.json` (VALIDATE CLEAN, 0 errors) + `H3_FaceRefine_boar_grave.json` (VALIDATE CLEAN, 0 errors/0 warnings) — boar-grave talking scene ready (D119/D120)

**`minimax_h3_boar_grave_talking_r2v.json`** — the talking scene (char1 in the hole + char2 + dummy at the rim). Base = user's `minimax_h3_sam_r2v_2char_cinematic.json` (82 nodes). Edits: node 153 video = `boar_grave_talking_camref.mp4` (start_time 0); refs 137/143 = `boar_char1/char2_identity.png` (Krea2 face_00001 copies in `input/`), 142 = `boar_char1_pose_digging.png` + 139 = `boar_env_parambu.png` (pending Krea2 t2i); node 138 = `[video editing]` blue→char1 (rose-pink shirt, crouched digging) / red→char2 (white tee) + third plain man, parambu env, slow push-in, 2 timed shots, natural-only soundscape, NO MUSIC (D041); node 305 prefix `boar_grave`; models fixed per D120 (pruned int8 UNET, 4step 768p turbo LoRA, nvfp4_awq CLIP, root VAEs, SAM3 root ckpt — the template's `H3\`/`h3\`/`sam3\` subfolder names were stale after the models re-org). **Validates clean** (2 pre-existing pipeline warnings = ImageBlend type mismatch + VAEDecodeAudio unreachable, present in the user's original template too). **RUN (after screenplay, stop Qwen first):** Queue → `output\boar_grave_00001.mp4`.

**`H3_FaceRefine_boar_grave.json`** — long-shot facial consistency (D120): Auto-Select template adapted — video = `output\boar_grave_00001.mp4`, refs = both identities, char1 subject prompt, models = installed stack. **Fix applied: node 108 `properties["Node name for S&R"]` = `UnetLoaderGGUF` → `UNETLoader`** (the converter uses S&R as the schema class → weight_dtype was being dropped; gotcha + root cause in D120). Run AFTER the R2V take; multi-person = chain per subject (README in the boar-grave kit).

**Also:** boar-grave kit staged at `E:\minimax_workflow\blender+minimax\boar_grave\` (blend + 5 renders + camref mp4 + identity refs + both workflows + README); `face_yolov8m.pt` → `models\ultralytics\bbox\`; FaceRefine example templates saved (`H3_Face_Refine_Auto/Manual_Select.json`); camref render route = Blender PNG frames → `imageio_ffmpeg` binary encode (Blender 5.2 has NO FFMPEG image_format + `Action.fcurves` absent — skip interpolation).

---

## 2026-10-08 — BUILT `krea2_dataset_char1.json` + `krea2_dataset_char2.json` — 20-image-per-character DATASET pipeline (143 nodes each, validate clean); DELETED `krea2_char_dataset_lock.json` (user: "clear that workflow")

**Purpose:** the character dataset for LoRA training (D113). **Structure:** shared chain UNET `krea2_turbo_fp8_scaled` → LoraLoader `krea2_identity_edit_v1_2`@1.0, CLIPLoader `qwen3vl_4b_fp8_scaled` (krea2), VAELoader `qwen_image_vae` → 3 anchor LoadImage refs (id 210/211/212 = `krea2_ds_cN_ref_{a,b,c}.png` — user-approved anchors pre-copied to `input/`) → **17 identity-edit branches** (ids 300-435, 8 nodes each): VAEEncode(ref) + Krea2EditGroundedEncode (scene instruction, grounding_px 512) + negative encode (cfg>1 only) + EmptySD3LatentImage 896×1120 + Krea2EditModelPatch (ref_boost 4, ref_boost_a 1, fit) + KSampler (10 steps, cfg 1, euler/simple, denoise 1, seed randomize base 5000+num) + VAEDecode + SaveImage `krea2_ds_cN_XX`. **Scene list (17):** backwater-mist frontal close-up / temple-wall 3-4 / palm-path back / auto-rickshaw market / ferry deck / fishing jetty / coconut grove / houseboat edge / awning rain / dusk streetlamp / beach back / college bench / courtyard close-up / paddy field / houseboat-bow profile / rain-face close-up / water-edge jetty. **Anchor cycling:** frontal scene → ref c, 3/4 → ref b, profile/back → ref a. **char1 traits:** wavy medium hair down, round face, light stubble, dark tee; **char2:** man-bun, angular face, CLEAN-SHAVEN (user's approved anchors — beard spec superseded), white tee. char1 anchors 1152×2048, char2 896×1120; all outputs 896×1120. Builder bug history: closure `global lid` NameError → state dict; branch-13 patch id collided with Note (400) → Note moved to 500. **Next:** user queues both (fresh tabs) → 34 images → user review → keep 20/char → character LoRA training.

---

## 2026-10-08 — BUILT `krea2_char_dataset_lock.json` — 2-character FACE-LOCKED dataset pipeline (54 nodes, validate clean) — **DELETED 2026-10-08** (user: "the workflow which you created is also not working / not getting what i wanted, lets clear that workflow")

**Purpose:** the reliable character-dataset route after t2i face-lottery proved
unreliable for "two different consistent characters". **Structure:** shared
chain — UNETLoader `krea2_turbo_fp8_scaled` → LoraLoader `krea2_identity_edit_v1_2`@1.0
(NO style/RawGirlV3 LoRA), CLIPLoader `qwen3vl_4b_fp8_scaled` (krea2),
VAELoader `qwen_image_vae` → 2 LoadImage ref slots (id 210 = char1 REF, id 211
= char2 REF; user loads the picked best-face image) → **6 identity-edit
branches** (char1_a/b/c, char2_a/b/c; node ids 300-347): VAEEncode(ref) +
Krea2EditGroundedEncode (scene instruction, grounding_px 512) + negative encode
(cfg>1 only) + EmptySD3LatentImage 896×1120 + Krea2EditModelPatch (ref_boost 4,
ref_boost_a 1, fit_mode fit) + KSampler (10 steps, cfg 1, euler/simple, denoise
1, seed randomize) + VAEDecode + SaveImage `krea2_charN_face_X`. **USAGE:**
pick best char1 + char2 t2i images → load into REF nodes → Queue → 6
face-locked 896×1120 images. Bad branch → re-queue that branch only (new
seed). Builder: machine-built (pattern: `krea2_identity_edit.json` v1.2,
D023/D025). char1 instructions carry "wavy hair down, sparse beard, dark
tee"; char2 "man-bun, short dark beard, white tee" + "Preserve the exact
facial identity". **Status: ready for user pick-and-lock.**

---

## 2026-10-08 — (discovered, pre-existing) `E:\minimax_workflow\blender+minimax\` — Blender→MiniMax H3 R2V pipeline package (D112)

**Location:** `E:\minimax_workflow\blender+minimax\` (created 2026-10-06/07, same batch as the `kerala_grave` blockout renders in `D:\MCP\blender_mcp\renders\`). **Purpose:** render a scene in Blender as blocks (blockout) + a 5s square camera-motion reference → create the finished scene in **MiniMax H3 R2V**.
**Core workflow: `video_minimax_h3_r2v-workflow.json` (UI format, 25 nodes, 27 links):** `MiniMaxH3ReferenceToVideo` **node 136** (widgets `['', 1344, 768, 124, 'match']` = prompt, width 1344, height 768, 124 frames (5s @ 25fps), mode 'match') ← LoadImage 137 `character-ref-2.png` (**CHARACTER identity ref**) + LoadImage 139 `environment_reference.png` (**ENVIRONMENT ref**) + **LoadVideo 142 `camera_reference_5s_square (1).mp4`** (**CAMERA MOTION/TIMING ref** — R2V accepts a video reference) → SaveVideo 92 prefix `video/MiniMax_H3`. **Demo variant:** `video_minimax_h3_r2v_blender_Comfyui_demo.json` (29 nodes, same core 136/92 + LoadImage 153).
**Camera reference source:** `camera_reference_5s_square.blend` + `.mp4` (5s, square) built per `blender_camera_motion_prompt.txt` (Blender-MCP prompt: mannequin on checkerboard, soft light; speed-ramp orbit — quick settled holds + fast travels; single extreme closeup ~3.75s (both eyes visible); ends exactly at opening framing for a seamless loop; save editable .blend + render square mp4).
**R2V prompt template:** `minimax_h3_reference_to_video_prompt.txt` (female + male character variants): Image 1 = character identity (face/hair/outfit/proportions preserved), Image 2 = environment (place character there, extend with parallax, preserve style), supplied video = **CAMERA MOVEMENT AND TIMING ONLY** ("Do not copy its mannequin, gray background, checkerboard floor, lighting"). 5s sequence: frontal waist-up → quick push/ease → alternating L/R 3/4 sweeps → max ~35° at 2.8–3.0s → low side view 3.0–3.3s → single ECU 3.57–3.73s (both eyes, eye contact) → pull back to exact opening framing at 5.0s (seamless loop); motion blur on fast moves, crisp on holds.
**Also in package:** `Blender_to_MiniMax_Complete_Guide.pdf` (14.7 MB), `character-ref.png` / `character-ref (1).png` / `character-ref-2.png`, `environment_ref.png`, `video_minimax_h3_r2v-workflow.png` (screenshot).
**Application to the GRAVE scene (plan, after character lock-in):** environment ref = `D:\MCP\blender_mcp\renders\kerala_grave_side.png` (or `kerala_grave_upper.png`), character ref = locked dataset face image, camera ref = the 5s square ref (or a grave-specific one) → H3 R2V 1344×768 124f 'match' → finished grave scene. **User: the two existing blockout angles (side + upper) are ENOUGH — no rebuild.** Note: the `MiniMaxH3ReferenceToVideo` widget shape `[prompt, width, height, frames, 'match']` is native-verified from this file.

---

## 2026-10-08 — ALL SIX char workflows: REVERT to proven config (PE ON + concise prompts, D108 update 8)

**Trigger:** run #3 (GPT 320-380-word prompts + PE off) came out worse than the
PE-on runs — user attached the 6 "nearly perfect" earlier images as the
quality target. **Changes (all six files, validate clean):** (1) PE back ON —
TG 310/311/312 (and _pe TG 310) restored to the original 13-slot shape
`[prompt, 1024, "on", 0.7, 64, 0.95, 0.05, 1.05, 42, 0.0, false, true,
"off"]` + full 13-key `widgets_values_named` — the exact config that produced
the attached images; (2) prompts = proven concise style (~200-235 words):
identity block (Malayali anchor, male only, concrete beards — char2 "about 5-7
days of growth, slightly dense, more than stubble, NOT clean-shaven") + scene
(a = backwater three-quarter looking-back with beard on jaw side, b =
houseboat three-quarter profile, c = rain street with wet hair/beard + neutral
expression) + candid tail; (3) zero text/subtitle vocabulary in positives —
all no-text/no-woman/no-multi-people terms live ONLY in node 301 (GPT's
127-word negative kept); (4) base-file rows 1-3 = the concise prompts (rows
4-6 kept). **RULE: PE off = quality downgrade on these workflows;
negative-style instructions only in the negative; ~130-240 word band.**

---

## 2026-10-08 — ALL SIX char workflows: GPT-rewritten prompts wired in (D108 update 7)

**Input:** user's GPT pass on our package →
`d:\models\vsCodeMcp\prompts\KREA2_character_dataset_rewritten_2026-10-08.md`
(6 prompts char1_a/b/c + char2_a/b/c, 320-380 words each, repeated identity +
beard blocks, per-scene no-text/no-woman anchors, extended 127-word negative).
**Wiring:** `_pe3` files TG 310/311/312 = charN_a/b/c; `_pe` files TG 310 =
charN_a; base files node 200 rows 1-3 = charN_a/b/c (rows 4-6 campus/temple/
auto-rickshaw kept as-is); node 301 negative = GPT's (all 6 files). All six
validate clean (13/13/13/13/25/25 nodes, 0 errors). **Loop NOT started (user
instruction).** Run = the `_pe3` pair in fresh tabs → 6 images at 896×1120.

---

## 2026-10-08 — ALL SIX char workflows: Malayali anchor + concrete beards + PE OFF + text/woman negatives (after failed 896×1120 run #2)

**Trigger:** user's pe3 run #2 (896×1120) — char1_a = woman + mountains +
garbled burned-in subtitles; char1_b/c = right type, different faces, "lack
malayali touch"; char2 = no visible beard. **Changes (all six files, validate
clean):** (1) every prompt now starts "A candid phone snapshot of a 26-year-old
young Malayali man from Kerala, India (South Indian features, warm
medium-brown natural skin), a young MAN, male only (NOT a woman, NOT a girl),
..."; (2) beards made concrete — char1 "a short PATCHY BEARD (clearly visible
sparse uneven patches of dark hair on the chin and jawline, more than a
clean-shaven face, NOT a full beard, short and uneven, not well groomed)",
char2 "a clearly visible short dark BEARD on the chin and jawline (about 5-7
days of growth, slightly dense, a little more than stubble, NOT clean-shaven,
NOT a full long beard, short and a bit uneven, not well groomed)"; (3) every
prompt ends "ONLY ONE man in focus, no other people in the foreground, no text,
no subtitles, no captions, no watermark, no logo, no speech bubbles, no
dialogue text."; (4) negative (node 301) extended with text/subtitles/captions/
words/letters/writing/watermark/logo/screenshot/social media overlay/woman/
girl/female/other people/multiple people; (5) **PE expansion OFF** — TextGenerate
`sampling_mode = "off"` in all 4 PE files (raw prompt passthrough; KSampler
randomize keeps draw variance). **GOTCHA (AGENTS.md lesson):** `sampling_mode`
is a DYNAMIC combo — `off` mode has only 3 widgets; `widgets_values` must be
`[prompt, 1024, "off"]` + 3-key named dict (the 13-slot on-mode array broke
validation: thinking got float, mtp got 0.95). **GPT-ready package:**
`d:\models\vsCodeMcp\prompts\char_dataset_gpt_package.txt` (identity blocks +
all 6 exact prompts + negatives + acceptance criteria + ask of GPT). **Face
drift is inherent to t2i** — lock = `krea2_identity_edit.json` (ref_boost 4)
after picking the best face.

---

## 2026-10-08 (incident fix) — krea2_t2i_char1.json + krea2_t2i_char2.json REPAIRED (node 200 prompt list wiped by UI re-save) + final beard spec across all six files

**Incident:** user's run = same beardless face from both base files. **Root cause:** node 200 (PixaromaPromptEach) `widgets_values` wiped to `[]` when the UI re-saved the files (rows survived only in `properties.promptEachState.rows`, which the backend does NOT read → empty prompt → model default). **Fix:** node 200 rows rebuilt — rows 1-3 = exact scene prompts (backwater looking-back / houseboat / monsoon rain, taken from the _pe3 TG nodes), rows 4-6 = campus / temple wall / auto-rickshaw reconstructed in the same candid phone-shot style (original 4-6 text lost to the wipe); `promptEachState.rows` synced. **Beard spec finalized (D108 u4):** char1 = "a PATCHY beard (clearly visible short sparse patches on the chin and jaw, more than clean-shaven, short and uneven, NOT a full beard, not well groomed)"; char2 = "a slightly DENSE short beard (clearly visible on the chin and jaw, a little more than stubble, short and a bit uneven, NOT a full long beard, not well groomed)" — applied in all six files in `widgets_values` + `widgets_values_named` + `promptEachState.rows` (the PE files' named dicts had kept the OLD wording — the frontend may prefer named, so both were synced). All six validate clean (13/13/13/13/25/25 nodes, 0 errors, 0 warnings). **Dataset runs = the `_pe3` files (no node 200); base files repaired but watch for another empty-prompt-list UI wipe.**

---

## 2026-10-08 — krea2_t2i_char1_pe3.json + krea2_t2i_char2_pe3.json (new) — 3-image CHARACTER DATASET PE (D110 update) + resolution/beard changes across ALL char workflows

**Purpose:** single-prompt PE (D110) = good realism but ONE image per character; goal = 3 images per character for the dataset. **Built via `utilities\build_krea2_t2i_char_pe3.py`** (clones char files, removes `PixaromaPromptEach` node 200 + link 11, adds the 3rd branch + TG nodes 310/311/312). **3 PE branches per character** (each = TextGenerate → CLIPTextEncode → KSampler → VAEDecode → FameGridColorFinish → SaveImage; shared UNET(55)/CLIPLoader(56)/VAELoader(57)/LoRA(96 Krea2-realism-V2 @1.0 → 97 famegrid_spicy @0.7)/latent(82)/negative(301)):
- **a** = row 1 backwater "looking back" (approved): TG 310 → 300 → KS 53 (seed 42) → 54 → 302 → SI 29, prefix `krea2_charN_face_a`
- **b** = row 2 houseboat: TG 311 → 313 → KS 314 (seed 43) → 315 → 316 → SI 317, prefix `_b`
- **c** = row 3 monsoon rain: TG 312 → 318 → KS 319 (seed 44) → 320 → 321 → SI 322, prefix `_c`

All TG: on-mode 13-slot `widgets_values`, PE seed 42, max_length 1024, thinking OFF, mtp off. KSampler 10 steps cfg 1 euler/simple denoise 1, `control_after_generate` "randomize". New links: 14/15 (branch A TG), 36 = 56→313.clip, 37 = 56→318.clip (each cloned CLIPTextEncode needs its OWN clip link — builder bug caught by validation). 25 nodes / 36 links, both files validate clean (0 errors, 0 warnings). Rows 4–6 (campus, temple wall, auto-rickshaw) = one-line prompt-widget swap.

**Changes across ALL char workflows (char1, char2, _pe ×2, _pe3 ×2 — all re-validated clean):**
- **Resolution:** EmptySD3LatentImage(82) 1152×2048 → **896×1120 (exactly 1 MP, 4:5; both dims multiples of 32)** — user verdict: soft at 100% (2.36 MP upscale from ~1 MP native) AND 9:16 too tall.
- **char2 beard:** "a SHORT patchy beard (short length, sparse, not well groomed, NOT a full beard)" → "a SHORT dense beard (clearly visible on the chin and jaw, more than just stubble, short and a bit uneven, NOT a full long beard, not well groomed)" — 14 occurrences (char2.json 6 rows + _pe 2 + _pe3 6). char1 beard UNCHANGED (perfect).

**2K keepers (optional):** `seedvr2_image_upscale.json` — SeedVR2 7B sharp DiT (`seedvr2_ema_7b_sharp_fp16.safetensors`) + ema VAE, `SeedVR2VideoUpscaler` @ 1440×2560; set LoadImage node 1 = keeper png + SaveImage node 5 prefix, Queue → `output\seedvr2_2k_*_00001_.png`.

**Status:** BUILT + VALIDATED, awaiting user re-run (D100: stop Qwen first, fresh tab). Old 1152×2048 a/b/c outputs superseded. **RULE: keep Krea2 t2i in the ~1 MP native class (896×1120 4:5); for more pixels, SeedVR2 2K post — don't upscale the latent.**

---

## 2026-10-08 — krea2_t2i_char1_pe.json + krea2_t2i_char2_pe.json (new) — Krea 2 single-prompt PE variance (D110)

**Purpose:** no-LoRA character variance for the char1/char2 t2i workflows (D108) using the built-in `TextGenerate` LLM expansion (Reddit PSA technique — Qwen3VL 4B text encoder expands ONE strong prompt; variance = PE seed (dramatic) + KSampler seed (fine)). **Built via `utilities\build_krea2_t2i_char_pe.py`** (clones char1/char2, removes `PixaromaPromptEach` node 200 + link 11, inserts node 310 `TextGenerate`). **Chain:** UNETLoader(55 `krea2_turbo_fp8_scaled.safetensors`) → LoraLoaderModelOnly(96 `Krea2-realism-V2.safetensors` @1.0) → LoraLoaderModelOnly(97 `famegrid_spicy_3167060.safetensors` @0.7) → KSampler(53: seed 42, randomize, 10 steps, cfg 1, euler/simple, denoise 1) ← EmptySD3LatentImage(82, 1152×2048); CLIPLoader(56 `qwen3vl_4b_fp8_scaled.safetensors` type krea2) → CLIPTextEncode positive(300).text ← **TextGenerate(310).generated_text** (link 15) ← 310.clip (link 14 from 56); negative = CLIPTextEncode(301) as before; VAEDecode(54) → FameGridColorFinish(302, 1.0/0.6) → SaveImage(29, prefixes `krea2_char1_face`/`krea2_char2_face`). **Node 310 `TextGenerate` (on-mode, 13-slot expanded widgets_values):** prompt = one strong prompt per character (char1: round face, wavy hair, full beard, dark tee, backwater path; char2: angular face, man-bun, short patchy beard, white tee, same scene) = row 1 of the removed 6-row set; sampling_mode ON {temperature 0.7, top_k 64, top_p 0.95, min_p 0.05, repetition_penalty 1.05, **seed 42**, presence_penalty 0.0}, max_length 1024, thinking OFF, use_default_template ON, mtp OFF. **Variance nobs:** PE seed = node 310 `sampling_mode.seed` (dramatic); KSampler seed = node 53 "randomize" (fine, fresh each run). **Models used:** krea2_turbo_fp8_scaled.safetensors, qwen3vl_4b_fp8_scaled.safetensors, qwen_image_vae.safetensors, Krea2-realism-V2.safetensors, famegrid_spicy_3167060.safetensors (all present at main models path). **Important custom nodes:** none (TextGenerate + FameGridColorFinish; both core/verified live). **Resolution:** 1152×2048 portrait. **Known issues:** none — both VALIDATE CLEAN (13 nodes, 0 errors, 0 warnings, mcp validate_workflow, live 8188). **Last successful result:** n/a (awaiting user run). **Next improvement:** after user judges takes — tune PE temperature/max_length, or sampling_mode OFF for raw-prompt runs. **Run order (user, stop Qwen first, fresh tab):** open `_pe.json` → Queue Prompt → `output\krea2_charN_face_0000N_.png`.

## 2026-09-28 — krea2_identity_edit_small_mic.json (new) — Krea2 IDENTITY EDIT small-mic end reference (D096 update 7)

**Purpose:** t2i-from-scratch (update 6) threw away the scene (table, papers, chair, bulb, composition) — user rejected it: "we need to give the base image and then do the I2I with identity... keep the identity transfer workflow, don't forget things." **CORRECT TOOL = Krea2 Identity Edit v1.2** (`krea2_identity_edit.json`): takes the BASE image and regenerates it keeping the scene identity, applying only the instruction. **Built via `utilities/build_krea2_identity_small_mic.py` (clones `krea2_identity_edit.json`, validates clean 0 errors/0 warnings, 15 nodes):** node 72 LoadImage = `mic+paper.png` (base scene); node 84 = instruction ("Make the microphone SMALL and COMPACT, on a SHORT LOW stand... ONLY ONE microphone... Keep EVERYTHING ELSE exactly the same: papers, table, empty chair, bare bulb, black void, B&W cinematic. Preserve the entire original image exactly. No other changes. No people."); node 85 = negative ("large/tall mic, two mics, color, people, extra objects..."); node 29 SaveImage = `jaisal_cut/mic_small_id`; node 95 (Typnosis) BYPASSED. **Kept proven identity params:** node 79 `Krea2EditModelPatch` ref_boost=4 fit, node 83 `ResolutionSelector` 16:9 2MP, node 53 KSampler 10 steps cfg 1 euler/simple denoise 1, node 71 `LoraLoaderModelOnly` `krea2_identity_edit_v1_2.safetensors` @1.0, UNET `krea2_turbo_fp8_scaled.safetensors`, CLIP `qwen3vl_4b_fp8_scaled.safetensors` type `krea2`, VAE `qwen_image_vae.safetensors`. All krea2edit nodes LIVE; identity LoRA present. **G's node 139 (ref_image_1) points at `mic+paper_small.png`.** **Status:** BUILT + VALIDATED, awaiting user run. **Run order (user, stop Qwen first, fresh tab):** run `krea2_identity_edit_small_mic.json` → `output\jaisal_cut\mic_small_id_00001_.png` → copy to `input\mic+paper_small.png` → run `jaisal_intro_G_revolt.json` → restart Qwen. **RULE: to change ONE attribute of a scene while keeping the scene, use Krea2 Identity Edit v1.2 (base image + instruction, ref_boost=4) — NOT t2i (loses scene), NOT inpaint (region-shape prior).**

---

## 2026-09-28 — krea2_t2i_small_mic_end.json (new) — Krea2 TEXT-TO-IMAGE small-mic end reference (D096 update 6) — SUPERSEDED by identity edit (update 7)

**Purpose:** inpainting can't shrink the mic — the mask must cover the old big mic's FULL HEIGHT (head + tall stand) to erase it, so the region is TALL and the model fills it tall; "small" in the prompt can't beat the region shape + big-mic prior. **User chose: regenerate the end reference FROM SCRATCH** (no big-mic prior to fight). **Built via `utilities/build_krea2_t2i_small_mic_end.py` (validates clean 0 errors/0 warnings, 9 nodes, all standard):** UNETLoader `krea2_turbo_bf16.safetensors` + CLIPLoader `qwen3vl_4b_fp8_scaled.safetensors` type `krea2` + VAELoader `qwen_image_vae.safetensors` + CLIPTextEncode (positive = small mic on short low stand + papers + bare bulb + black void + B&W cinematic; negative = large/tall mic, color, people, chair, extra objects) + `EmptySD3LatentImage` (1920×1088) + KSampler (10 steps cfg 1.0 euler/simple denoise 1.0, seed 42 randomize) + VAEDecode + SaveImage `jaisal_cut/mic_small_end`. **G's node 139 (ref_image_1) points at `mic+paper_small.png`.** **Status:** BUILT + VALIDATED, awaiting user run. **Run order (user, stop Qwen first, fresh tab):** run `krea2_t2i_small_mic_end.json` → pick the best `output\jaisal_cut\mic_small_end_0000N_.png` → copy to `input\mic+paper_small.png` → run `jaisal_intro_G_revolt.json` → restart Qwen. **RULE: when the unwanted attribute is anchored by the region SHAPE (tall mic), regenerate from scratch (t2i), don't inpaint.**

---

## 2026-09-28 — krea2_inpaint_small_mic.json (new) — Krea2 INPAINT small-mic reference (D096 update 4) — SUPERSEDED by t2i (update 6)

**Purpose:** Qwen-Image-Edit failed twice (empty-latent = regeneration; VAEEncode = prior too strong, mic stayed big). The proven Krea2 SAM3 inpaint workflow (`krea2_inpaint_kf2_chair.json`) can't run — its `SAM3Segment` + `CR Upscale Image` nodes are NOT loaded in the live server (no SAM3 pack installed). **FINAL: manual mask + standard Krea2 inpaint.** **Built via `utilities/build_krea2_inpaint_small_mic_v2.py` (validates clean, 0 errors, 0 warnings, 11 nodes, ALL standard nodes):** (1) `utilities/make_mic_mask.py` → `input/mic_mask.png` (white = mic region: head ellipse + stand rect + base ellipse, GaussianBlur 12) — deterministic, no model; (2) workflow: LoadImage `mic+paper.png` + LoadImage `mic_mask.png` (MASK out) → `VAEEncodeForInpaint` (pixels+vae+mask) → KSampler (Krea2 `krea2_turbo_bf16.safetensors`, CLIPLoader `qwen3vl_4b_bf16.safetensors` type `krea2`, VAELoader `qwen_image_vae.safetensors`, 8 steps cfg 1.0 euler/simple denoise 1.0) → VAEDecode → SaveImage `jaisal_cut/mic_small`. `VAEEncodeForInpaint` keeps everything OUTSIDE the mask pixel-identical, regenerates only the mic. **G's node 139 (ref_image_1) points at `mic+paper_small.png`.** **v2 RUN FAILED (user: "the same thing")** — `VAEEncodeForInpaint` + denoise 1.0 does NOT set a noise mask → regenerated the WHOLE image (papers/chair/bulb all shifted, mic still big — confirmed in `output\jaisal_cut\mic_small_00007_.png`). The mask was correct. **v3 FIX (`utilities/build_krea2_inpaint_small_mic_v3.py`, validates clean 0 errors/0 warnings, 12 nodes):** correct mechanism = **`VAEEncode` (full image) + `SetLatentNoiseMask` (mask = mic region) → KSampler** — `SetLatentNoiseMask` restricts regeneration to the masked region; everything outside stays pixel-identical. Prompt strengthened ("its top well below the height of a tall broadcast mic" + negative `tall object`). **RULE: true region inpaint = `VAEEncode` + `SetLatentNoiseMask` + KSampler — NOT `VAEEncodeForInpaint`.** **Status:** v3 BUILT + VALIDATED, awaiting user run. **Run order (user, stop Qwen first, fresh tab):** run `krea2_inpaint_small_mic.json` → copy `output\jaisal_cut\mic_small_00008_.png` (next number) to `input\mic+paper_small.png` → run `jaisal_intro_G_revolt.json` → restart Qwen.

---

## 2026-09-28 — qwen_edit_small_mic.json (new) — Qwen-Image-Edit small-mic reference (D096 update 3) — SUPERSEDED by Krea2 inpaint (update 4)

**Purpose:** the G end reference `mic+paper.png` (1928×1088) shows a BIG broadcast mic on a tall stand — that anchors the huge mic in the G video; prompt words "small" can't beat a reference image. **Fix: EDIT the reference** with Qwen-Image-Edit-2509 GGUF to produce `mic+paper_small.png` (small compact mic on a short low stand, everything else identical), which becomes G's ref_image_1. **Built via `utilities/build_qwen_edit_small_mic.py` (validates clean, 0 errors, 0 warnings, 10 nodes).** **Chain:** LoadImage `mic+paper.png` → `TextEncodeQwenImageEdit` (positive "Make the microphone SMALL and COMPACT, on a SHORT LOW stand... Keep EVERYTHING ELSE exactly the same: papers, table, empty chair, bare bulb, black void, B&W cinematic style" + negative "large microphone, tall stand, color, people, extra objects") + `UnetLoaderGGUF` (`Qwen-Image-Edit-2509-Q8_0.gguf` 21.76 GB, fits 32 GB VRAM no offload) + **`CLIPLoader` (`qwen_2.5_vl_7b_fp8_scaled.safetensors`, `qwen_image`, `default`)** + `VAELoader` (`qwen_image_vae.safetensors`) + `EmptyQwenImageLayeredLatentImage` (1920×1088) + KSampler (8 steps, cfg 1.0, euler/simple, denoise 1.0, seed 123456789 randomize) + VAEDecode + SaveImage `jaisal_cut/mic_small`. **G's node 139 (ref_image_1) now points at `mic+paper_small.png`.** **Build bugs fixed:** (1) link 103 (VAE→node 5) was at slot 2 colliding with image — moved to slot 1 (native order clip/vae/image/prompt); (2) link 106 (negative conditioning) came from node 5 (positive) — must come from node 10 (negative TextEncode); (3) **TEXT-ENCODER DIMENSION MISMATCH** — first build used `CLIPLoaderGGUF` + `qwen3vl_4b_fp8_scaled.safetensors` (Qwen3-VL-4B, 2560-dim) → crashed at sample time `RuntimeError: Given normalized_shape=[3584], expected input with shape [*3584], but got input of size[1, 1152, 2560]`. The Qwen-Image-Edit-2509 UNet needs **3584-dim = Qwen2.5-VL-7B** → **`CLIPLoader` + `qwen_2.5_vl_7b_fp8_scaled.safetensors` + type `qwen_image`** (the 2.5-VL-7B file is `.safetensors`, not GGUF, so it needs the regular `CLIPLoader`); (4) **EDIT vs GENERATION WIRING** — user ran the first working build 6×: "no change... none of them has any changes apart from lighting". Root cause: `EmptyQwenImageLayeredLatentImage` (empty latent) + `denoise=1.0` = TEXT-TO-IMAGE, not an edit — the big-mic prior in the reference won each regeneration. **Fix: `VAEEncode` (pixels = LoadImage, vae = VAELoader) → KSampler `latent_image` = encoded latent, `denoise=1.0` (correct for a dedicated editing model), 20 steps.** **RULE: image-edit = `LoadImage → VAEEncode → KSampler(latent_image=encoded, denoise=1.0)`; never an empty latent for an edit.** **Status:** BUILT + VALIDATED (0 errors/0 warnings), awaiting user run. **Run order (user, stop Qwen first, fresh tab):** run `qwen_edit_small_mic.json` → `output\jaisal_cut\mic_small_00001_.png` → copy to `input\mic+paper_small.png` → run `jaisal_intro_G_revolt.json` (fresh tab) → restart Qwen.

---

## 2026-09-28 — jaisal_intro_G_revolt.json (new, then extended to 15s) — Shot G = SINGLE SEQUENTIAL take (D096)

**Purpose:** the G1/G2 split (D095) was overcomplicating it. The real structure = ONE continuous take where the character STAYS PRESENT at the table while a SEQUENCE of objects appear (each triggered by its specific Malayalam word), and the character disappears at ONE clean moment. **Built `jaisal_intro_G_revolt.json`** (cloned from `jaisal_intro_G_papers.json` via `utilities/build_G_revolt_11s.py`, then extended in-place to 15s). **5 refs:** ref_image_0 = `kf7a_v4.png` (start: character at table, dead plants), ref_image_1 = `mic+paper.png` (end: papers + mic), ref_image_2 = `obj_cricket_bat_00002_.png` (node 165), ref_image_3 = `obj_soccer_ball_00002_.png` (node 166), ref_image_4 = `obj_paper_smiley_00002_.png` (node 167). **Latent chain:** Load clip 7 (F2 tail) → Save clip 8. **Chain now A(1)→B(2)→C(3)→D(4)→E(5)→F1(6)→F2(7)→G(8).**

**11s version (264f) — RUN GOOD (user: "that was good"):** sequential one-action-at-a-time: question first (00:00–00:01) → PAPERS for "കഥകൾ" (00:02–00:03) → MIC for "രാഷ്ട്രീയം" (00:03–00:04) → BAT+BALL for "കായികം" (00:04–00:05) → SMILEY PAPER for "fantasy" (00:06–00:07) → Jaisal present through the sequence → disappears on "നോക്കാം" (00:09–00:10) → camera guy "നോക്കാം" (00:10–00:11). Prompt: `Jaisal-intro/prompts/shot_G_revolt_11s.txt`.

**15s version (360f) — CURRENT (D096 update):** user: "increase to 15s, the issues are the sudden removal of the character and the plant, give them proper details, second 14 light flickering, 15 complete black, rest same." **Changes:** (1) length 264→360; (2) **CHARACTER DISAPPEARANCE = 2-beat GRADUAL unraveling** — 00:09–00:10 "നോക്കാം": body BEGINS to come apart (outline softens, edges turn into paper sheets, form loses solidity — NOT a sudden pop); 00:10–00:11 COMPLETES (silhouette thins into final sheets, chair empty — SLOW, DETAILED, GRADUAL over 2s); (3) **PLANT BEHAVIOR section** — dead plants SLOWLY CRUMBLE and WITHER throughout the shot (leaves curl to dust, stems bend and sink), NOT a single-frame vanish; (4) **new tail:** 00:11–00:12 camera guy "നോക്കാം" → 00:12–00:13 still beat → **00:13–00:14 bulb FLICKERS once** → **00:14–00:15 COMPLETE BLACK, CUT TO BLACK**; (5) negatives += `Jaisal vanishing in a single frame, Jaisal popping out suddenly, the plants vanishing in a single frame, the plants popping out suddenly, the plants disappearing before the character`. **Prompt: `Jaisal-intro/prompts/shot_G_revolt_15s.txt` (14353 chars). Validates clean (0 errors, 29 nodes).**

**15s v2 (D096 update 2) — CURRENT:** user: "we're almost there. the first dialogue should come from the camera man, and the mic should be a little lower so we can see the character's face." **Changes (prompt `Jaisal-intro/prompts/shot_G_revolt_15s_v2.txt`, 15290 chars, synced in-place):** (1) **CAMERA-GUY VOICE = the PROVEN F1 timing-mimic workaround** — question = FULL 3s off-screen beat (00:00–00:03, Jaisal's mouth COMPLETELY CLOSED, he only listens) → Jaisal's first line starts IMMEDIATELY after (00:03, "പറഞ്ഞപോലെ... കഥകൾ...", NO long silent gap) + SPEAKER ATTRIBUTION (CRITICAL) block (<Subject 2> = AUDIO ONLY) + negatives `Jaisal speaking the question, lip-sync to the off-screen voice, Jaisal's lips opening before 00:03, a long silent gap between the question and Jaisal's first line`; (2) **LOW MIC** — settles LOW on the table, top BELOW Jaisal's face level so his face stays visible (negatives `the microphone blocking Jaisal's face, the microphone rising above Jaisal's face level`); (3) **timing shift:** everything after the question shifts +2s (papers 00:03–00:05 → mic 00:05–00:06 → bat+ball 00:06–00:07 → fantasy 00:08–00:09 → "നോക്കാം" + disappearance 00:11–00:13 → camera guy "നോക്കാം" 00:13–00:14 → bulb flicker + COMPLETE BLACK 00:14–00:15). **Validates clean (0 errors, 29 nodes).**

**15s v3 (D096 update 3) — CURRENT:** user: "the character is still speaking the dialogue, and the mic is still huge. we need a small mic." **Changes (prompt `Jaisal-intro/prompts/shot_G_revolt_15s_v3.txt`, 14862 chars, synced in-place):** (1) **QUESTION REMOVED FROM VIDEO** — the question's `<d>` line is dropped entirely; 00:00–00:03 is a pure silent-listen beat (Jaisal mouth closed), the camera-guy question is DUBBED IN POST (prompt-only attribution never fully holds, D090); (2) **SMALL MIC** — the mic is now SMALL + LOW (face visible); the huge-mic anchor is fixed by EDITING THE END REFERENCE (see `qwen_edit_small_mic.json` above) — G's node 139 (ref_image_1) now points at `mic+paper_small.png`. **Validates clean (0 errors, 29 nodes).**

**Status:** 11s RUN GOOD. 15s v3 BUILT + VALIDATED, awaiting small-mic ref + user run.

**Run order (user, stop Qwen first, fresh tab):** run `qwen_edit_small_mic.json` → copy `output\jaisal_cut\mic_small_00001_.png` to `input\mic+paper_small.png` → stage F2 last frame → G_revolt (15s v3) → restart Qwen.

**SUPERSEDED (do NOT run):** D095 G1/G2 split (`jaisal_intro_G1_burst.json`, `jaisal_intro_G2_aftermath.json`), `jaisal_intro_G_papers.json` (15s single), `jaisal_intro_G_vanish_burst.json` (old 3s) — keep as backups.

**Known issues:** none (validated clean).

---

## 2026-09-28 — jaisal_intro_G1_burst.json + jaisal_intro_G2_aftermath.json (new) — Shot G SPLIT (D095)

**Purpose:** the single 15s shot G (`jaisal_intro_G_papers.json`) came out with the CHARACTER STAYING — as soon as the paper burst happened the character should be GONE, but the identity prior won and he "stayed". One 15s shot asked MiniMax to hold the character + shrink plants + emerge a mic + enter 3 objects + burst the character into papers — too many simultaneous events. **Split into two chained shots** so the hard "disappear" moment is isolated and the aftermath has NO character reference at all.

**G1 = `jaisal_intro_G1_burst.json` (10s = 240f @ 24fps, 1344×768):** character present → camera-guy question (off-screen `<Subject 2>`) → Jaisal speaks ("As I said... stories, politics, sports, fantasy" + "I don't know if it'll work... Let's see.") + dead plants SLOWLY SHRINK and vanish → **00:08–00:10 JAISAL BURSTS INTO papers** (body EXPLODES OUTWARD, NOT a fade) → chair EMPTY. **Refs:** ref_image_0 = `kf7a_v4.png` (start: character at table, dead plants), ref_image_1 = `jaisal_gone_papers_alone.png` (END: papers only, empty chair, NO character). **2 refs only** (object-ref nodes 165/166/167 removed). **Latent chain:** Load clip 7 (F2 tail) → Save clip 8. **Prompt:** `Jaisal-intro\prompts\shot_G1_burst_10s.txt` (node 138).

**G2 = `jaisal_intro_G2_aftermath.json` (10s = 240f @ 24fps, 1344×768):** **NO character at any point** — papers-only start → camera guy's OFF-SCREEN voice "Let's see." (00:02–00:04) → mic emerges SEPARATELY (00:04–00:06) → cricket bat flies in (00:06–00:08) → soccer ball rolls in + smiley paper settles on bat (00:08–00:10). **Refs:** ref_image_0 = `jaisal_gone_papers_alone.png` (start: papers only, NO character), ref_image_1 = `mic+paper.png` (end: papers + mic), + object refs `obj_cricket_bat_00002_.png` (node 165), `obj_soccer_ball_00002_.png` (node 166), `obj_paper_smiley_00002_.png` (node 167). **Latent chain:** Load clip 8 (G1 tail) → Save clip 9. **Prompt:** `Jaisal-intro\prompts\shot_G2_aftermath_10s.txt` (node 138).

**WHY IT WORKS:** G2 has NO character reference, so the character CANNOT "stay" — MiniMax only has papers+objects to track. The hard "disappear" moment is isolated into G1 where the END ref (papers only, empty chair) forces the character out.

**Chain now A(1)→B(2)→C(3)→D(4)→E(5)→F1(6)→F2(7)→G1(8)→G2(9).**

**Built via:** `utilities\build_G1_G2_split.py` (clones `jaisal_intro_G_papers.json`, swaps refs/prompt/length/latent, removes object-ref nodes for G1). Both validate clean (0 errors; G1 26 nodes, G2 29 nodes; 2 known harmless orphan-math warnings 131/132).

**Status:** BUILT + VALIDATED. Awaiting user runs.

**Run order (user, stop Qwen first, fresh tabs):** stage F2 last frame → G1 → stage G1 last frame → G2 → restart Qwen.

**SUPERSEDED:** `jaisal_intro_G_papers.json` (15s single) + `jaisal_intro_G_vanish_burst.json` (old 3s) — do NOT run these; keep as backups.

**Known issues:** none (validated clean).

---

## 2026-09-28 — jaisal_intro_F1_plants_listen.json + jaisal_intro_F2_plants_wither.json (new) — Shot F SPLIT (D094)

**Purpose:** the single 17s shot F (`jaisal_intro_F_plants_die.json`) came out well (camera-guy voice, listening, plant sorrow, detailing) but `<pause>` tags didn't work (character talked through them), 17s > MiniMax ~15s limit, and micro-expressions were too weak. Split into two shots.
**F1 = `jaisal_intro_F1_plants_listen.json` (10s = 240f @ 24fps, 1344×768):** E's ending (plants blooming) → camera-guy question (off-screen `<Subject 2>`) → Jaisal LISTENS (micro-expressions) → speaks "Cinema... or if you want to tell a story... You need effort." Plants stay mostly blooming, left plant's top leaf just begins to droop. **Refs:** ref_image_0 = `kf5_plants_alive_v9_00004_.png` (start), ref_image_1 = `kf6_plants_dead_v9_00004_.png` (end direction). **Latent chain:** `MiniMaxH3MotionContextLoadLatent` (node 161, `["h3_context", 5]`) → `MiniMaxH3MotionContext` (node 162, `[22, 24]`) → `MiniMaxH3MotionContextTrim` (node 163, `[0, 24, True]`) → `MiniMaxH3MotionContextSaveLatent` (node 164, `["h3_context/clip", 6]`). **Prompt:** `Jaisal-intro\prompts\shot_F1_plants_listen.txt` (node 138).
**F2 = `jaisal_intro_F2_plants_wither.json` (12s = 288f @ 24fps, 1344×768):** first leaf drooping → fully wilted. "Or you need one or two people... I'm alone... limitations... let's try this show using AI." **Refs:** ref_image_0 = `shot_F1_lastframe.png` (USER STAGES after F1 run via `seedvr2_lastframe_2k.json` → `output\lastframe_2k_00001_.png` → copy to `input\shot_F1_lastframe.png`), ref_image_1 = `kf6_plants_dead_v9_00004_.png`. **Latent chain:** Load clip 6 → Save clip 7. **Prompt:** `Jaisal-intro\prompts\shot_F2_plants_wither.txt` (node 138).
**G updated:** `jaisal_intro_G_papers.json` LoadLatent 6→**7**, SaveLatent 7→**8**. **Chain now A(1)→B(2)→C(3)→D(4)→E(5)→F1(6)→F2(7)→G(8).**
**PAUSE FIX (key lesson):** MiniMax does NOT honor `<pause>`/`<long pause>` timing tags in `<d>` dialogue. Instead, make the pause a VISUAL PERFORMANCE: explicit SILENT mouth-closed beats as action lines ("SILENT beat — his mouth stays CLOSED. A slow, heavy blink. His gaze drops to the plant. A quiet, honest, almost tired look settles. His shoulders drop a little more. (NO mouth movement during this beat.)") + dedicated MICRO-EXPRESSIONS section (slow blink, gaze drop, subtle frown, small breath, shoulders dropping, eyes glisten, small swallow, determined glint) + negatives `talking through the pause, mouth moving during the silent beat`. Mood shift (bloom→wilt, hope→limitation→resolve) carried by VISUALS + plant action.
**Built via:** `utilities\build_F1_F2.py` (clones F, sets length 240/288, swaps prompt, sets F2 ref_image_0, bumps F2 latent 6→7, bumps G 7→8). All 3 validate clean (0 errors, 2 known harmless orphan-math warnings 131/132).
**Status:** BUILT + VALIDATED. Awaiting user runs (morning of 2026-09-29).
**Run order (user, stop Qwen first, fresh tabs):** F1 → stage F1 last frame → F2 → G → restart Qwen.
**Known issues:** none (validated clean). `jaisal_intro_F_plants_die.json` (the original single 17s F) is now SUPERSEDED by F1+F2 — keep as backup.

---

## 2026-09-20 — Continuation packs installed (Ep29 consistent-audio + NikoDemon80 latent-tail)

**Installed (staged into `custom_nodes\`, ComfyUI restart pending):**

- **`SatoDive/Minimax-H3-Latent-Continuation`** (24★, MIT, HEAD 4142527) — the
  **Ep29 consistent-audio continuation pack** (D092). All 8 Ep29 node classes
  confirmed present in source: `MiniMaxH3EasyVideoTailSlicer_SatoDive`,
  `MiniMaxH3EasySegmentDecode_SatoDive`, `MiniMaxH3EasyModelAdapter_SatoDive`,
  `MiniMaxH3EasyStitchContinuation_SatoDive`, `MiniMaxH3EasySegmentRender_SatoDive`,
  `MiniMaxH3EasySaveLatent_SatoDive`, `MiniMaxH3EasyLoadLatent_SatoDive`,
  `MiniMaxH3EasyContextSegments_SatoDive`. No extra pip deps.
- **`NikoDemon80/ComfyUI-H3-Motion-Context`** (988★, v0.6.2, HEAD 5335715) —
  visual latent-tail slicing (D091). Nodes: H3 Motion Context, Trim,
  Save/Load Latent pair, Chain, Seam Probe. No extra pip deps.

**Ep29 workflow** (`E:\minimax_workflow\Ep29 MiniMaxH3_Continuation_Workflow.json`,
UI format) — consistent-audio continuation for small English stories. Already
installed deps: KJNodes, Pixaroma, rgthree. **Verify after restart (install pack
if red):** `MiniMaxH3SigmaShift` + `MiniMaxH3DualClockSamplerT8` (H3 sampler
pack), `H3SLAAttention` + `MiniMaxH3MemoryEfficientSageAttentionPatch` +
`SolAttnPatch` (SLA attention), `JWFloatToInteger` + `VRAMCleanup`/`RAMCleanup`
(utility nodes).

**Status:** staged, NOT yet registered (needs ComfyUI restart). **NEXT:** restart
→ open Ep29 → confirm no red nodes → test D→E continuation with audio continuity.

---

## 2026-09-20 — Shot D SeedVR2 pipeline wired (upscale + last-frame 2K)

Shot D v3 (aggressive non-speaking) = GOOD (user confirmed). Wired the SeedVR2
pipeline for take `jaisal_intro_D_reverse_00006_.mp4` via
`utilities/wire_seedvr2_shot_D.py` (both validate clean 0 errors 0 warnings):

- **`seedvr2_video_upscale.json`**: LoadVideo (node 21) =
  `jaisal_intro_D_reverse_00006_.mp4` (staged to `input\`); SaveVideo (node 23)
  prefix = `intor_selected_Upscale/upscaled_D` →
  `output\intor_selected_Upscale\upscaled_D_00001_.mp4` (1920×1080 2K, SeedVR2
  7B Sharp FP16, batch 33, lab color, offload cpu).
- **`seedvr2_lastframe_2k.json`**: LoadVideo (node 21) =
  `jaisal_intro_D_reverse_00006_.mp4` (the ORIGINAL take — the workflow's
  internal upscaler re-upscales the last frame to 2K, so NO manual copy of the
  upscaled video is needed); GetImageRangeFromBatch (node 30) = `[-1, 1]` (last
  frame); SaveImage (node 31) prefix = `lastframe_2k` →
  `output\lastframe_2k_00001_.png` (shot D's 2K last frame).
- Both SeedVR2 models confirmed present (`seedvr2_ema_7b_sharp_fp16.safetensors`
  16.48 GB + `ema_vae_fp16.safetensors` 0.50 GB in `models\SEEDVR2\`).

**Run order (user, stop Qwen first):** `seedvr2_video_upscale.json` →
`seedvr2_lastframe_2k.json` → copy `lastframe_2k_00001_.png` to `Jaisal-intro\` +
stage `input\shot_D_lastframe.png` → prep Shot E (Jaisal SPEAKING, plants grow)
with `ref_image_0` = `shot_D_lastframe.png`.

---

## 2026-09-15 — seedvr2_video_upscale.json (new) — SeedVR2 2K Video Upscaler

### Workflow

`seedvr2_video_upscale.json` (UI format, validated `valid: true` 0 errors 0 warnings, 7 nodes) built by `utilities/build_seedvr2_video_upscale.py` — cloned from the OFFICIAL `custom_nodes/seedvr2_videoupscaler/example_workflows/SeedVR2_HD_video_upscale.json` so all native widget shapes are preserved.

**Chain:** `LoadVideo` (node 21, `widgets_values=[filename, "image"]`, default = `jaisal_intro_A_walkin_00005_.mp4`) → `GetVideoComponents` (node 22) → `JoinImageWithAlpha` (node 17, alpha input left None) → `SeedVR2VideoUpscaler` (node 10, `widgets_values=[42, 'fixed', 1080, 0, 33, True, 'lab', 3, 0, 0, 0, 'cpu', False]` — seed 42, resolution **1080 shortest-edge** (1376×768 → **1920×1080**), batch_size 33, uniform_batch True, color_correction lab, temporal_overlap 3, offload cpu) ← `SeedVR2LoadDiTModel` (node 14, `['seedvr2_ema_7b_sharp_fp16.safetensors', 'cuda:0', 0, False, 'cpu', False, 'sdpa']` — **7B Sharp FP16 = max quality**, 15.35 GB, confirmed in `E:\ComfyUI_windows_portable\ComfyUI\models\SEEDVR2\`) + `SeedVR2LoadVAEModel` (node 13, `['ema_vae_fp16.safetensors', 'cuda:0', True, 1024, 128, True, 768, 128, 'false', 'cpu', False]` — tiled encode/decode) → `CreateVideo` (node 24, fps from source) → `SaveVideo` (node 23, prefix `intor_selected_Upscale/upscaled`).

**Purpose:** upscale the 3 selected intro shots (A/B/C, all 1376×768 @ 24fps) to 1920×1080. **Run 3×** — swap the LoadVideo filename each time (A is default; then `jaisal_intro_B_setup_00003_.mp4`, then `jaisal_intro_C_starting_2ref_00006_.mp4`). All 3 staged into `input\`. Outputs: `output\intor_selected_Upscale\upscaled_00001_.mp4` (A), `_00002_` (B), `_00003_` (C) in run order — rename after.

**Status:** Built + validated, NOT yet run (user runs — stop Qwen first). **NEXT:** after upscaling, take the LAST FRAME of the upscaled C video → feed it to shot D's workflow as the start ref (avoids the stitching glitch).

---

## 2026-09-14 — krea2_object_refs.json (new) — Shot-7 Object Reference Generator (t2i)

### Workflow

`krea2_object_refs.json` (UI format, validated `valid: true` 0 errors 0 warnings,
21 nodes) built by `utilities/build_krea2_object_refs.py`. **3 parallel Krea2 t2i
branches** sharing UNET/CLIP/VAE loaders, each: `CLIPTextEncode`(pos) +
`CLIPTextEncode`(neg) + `EmptySD3LatentImage [1024,1024,1]` +
`KSampler [42,'randomize',10,1,'euler','simple',1]` + `VAEDecode` + `SaveImage`.

### Objective

Generate the 3 Shot-7 object references (soccer ball, cricket bat, paper-with-smiley)
on a pure black background so MiniMax H3 can extract them as clean object refs for
the "Jaisal explodes into ideas" effect. **NO identity LoRA** (objects, not the
character).

### Configuration

- UNET `krea2_turbo_bf16.safetensors`, CLIP `qwen3vl_4b_fp8_scaled.safetensors`
  (type `krea2`), VAE `qwen_image_vae.safetensors`.
- KSampler `10 steps / cfg 1 / euler / simple`, 1024×1024.
- **UNSEEN top light (D066):** positives say "Lit from directly above by a single
  UNSEEN light source — the light itself is NOT visible in the frame, only its light
  and hard shadow"; negatives add `light bulb, bare bulb, lamp, visible light
  source, ceiling, cord, wire, hanging bulb, bulb in frame`.
- Save prefixes: `jaisal_cut/obj_{soccer_ball,cricket_bat,paper_smiley}`.

### Models used

Krea2 turbo (bf16) + Qwen3VL 4B (krea2 type) + Qwen image VAE. All confirmed live in
the running install (`E:\comfyUi_latest\...`).

### Important parameters

- Native `widgets_values` shapes copied from `krea2_identity_edit.json` (KSampler 7
  values w/ hidden `randomize`; CLIPTextEncode `[text]`; EmptySD3LatentImage
  `[w,h,batch]`; VAEDecode `[]`; SaveImage `[prefix]`).
- Link integrity verified: 27 links, 0 orphan/mismatched.

### Known issues

- **First seed (`_00001_`) rendered a VISIBLE bulb** in all 3 (Krea2 is a general
  model — "unseen light" is a hint, not a guarantee). **Re-roll (`_00002_`) came out
  clean.** Always visually verify the bulb is gone.

### Last successful result

`_00002_` set (1:44 AM) = clean: round soccer ball, vertical cricket bat, paper with
handwriting + smile line, all on pure black, no bulb. Copied to
`D:\models\vsCodeMcp\Jaisal-intro\obj_refs\` (6 PNGs: 2 takes × 3 objects).

### Next improvement

Feed the 3 clean `_00002_` PNGs into the H3 R2V Shot-7 workflow (5-ref plan:
ref0=empty scene, ref1=paper, ref2=bat, ref3=ball, ref4=end anchor).

---

## 2026-09-06 — jaisal_continuity_character.json (new) — Character Consistency (Continuity H3)

### Workflow

`jaisal_continuity_character.json` — a SINGLE `MiniMaxH3Creator` node (ComfyUI-Continuity, roadmaus/ComfyUI-Continuity). Continuity is an all-in-one node (NO sockets, it's an output node) — the cast, references, prompt and model selection all live in its `creator_data` JSON blob, managed by the Continuity frontend (`Ctrl+Shift+M` fullscreen editor). A "workflow" is just this one node.

### Objective

Character consistency WITHOUT a LoRA for the Jaisal Cut intro (natural face, close-up + medium shot). Cast-based: add the character to the cast, hang reference stills on them, write the shot with `@`-references. Fully local, supports MiniMax H3.

### Configuration

- All 5 H3 model slots pre-wired to files we ALREADY have (NO new downloads): FL2VA `minimax_h3_fl2va_pruned_int8_convrot.safetensors`, Ref2VA `minimax_h3_ref2va_pruned_int8_convrot.safetensors`, text encoder `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`, video VAE `minimax_h3_video_vae_fp16.safetensors`, audio VAE `minimax_h3_audio_vae_fp32.safetensors`.
- Widget order (15 values): `creator_data, seed, steps, cfg, sampler_name, scheduler, shift_video, shift_audio, block_cache, spectrum, spectrum_blend, sage, attention, chunk_ffn, fp16_accumulation`. Defaults: seed 0, steps 20, cfg 1.0, sampler `res_multistep`, scheduler `simple`, shift_video 12.0, shift_audio 3.0, block_cache `off`, spectrum false, spectrum_blend 0.5, sage false, attention `default`, chunk_ffn false, fp16_accumulation false.
- `creator_data` blob: `models` = dict keyed by slot name → filename; `segments` = list of `{prompt, assets, loras, duration_s, checkpoint}`; references attached with `@` in the prompt (UI).
- Output lands in `output/continuity/`.
- Validates `valid: true`, 0 errors, 0 warnings.

### Status

BUILT + validated. **NOT YET TESTED** (user will test after some time). The prompt is a Jaisal placeholder — replace in the UI. See D046.

---

## 2026-09-06 — jaisal_single_shot_semantic.json (new) — SLA i2v + Semantic Bridge

### Workflow

`jaisal_single_shot_semantic.json` — a copy of the working `jaisal_single_shot.json` (SLA i2v, 14 s / 1344×768 / turbo 4-step) with the **MiniMax H3 Semantic Bridge** added on the conditioning path.

### Objective

Improve prompt adherence on the i2v (FL2VA) workflow using the Semantic Bridge conditioning-space adapter (`speach1sdef178/MiniMax-H3-Semantic-Bridge`).

### Changes

- Copied from the clean `jaisal_single_shot.json` (backup `workflow_backups\jaisal_single_shot.pre_semantic_bridge.json`).
- Inserted **`SenseNovaH3DistilledBridge`** node (id 300) INSIDE the subgraph on the conditioning path: `node 104 (i2v positive) → [link 187] → node 300 (bridge) → [link 301] → node 16 (BasicGuider)`.
- Bridge widgets: `distilled_adapter = MiniMaxH3_SemanticBridge_v1.safetensors`, **`alpha = 0.10`** (recommended start; 0.15 = stronger), `magnitude_match = per_token`.
- SLA node (150), turbo LoRA (121), models, prompt, 1344×768/345 frames all UNCHANGED.
- Validates `valid: true`, 0 errors (2 pre-existing harmless warnings on nodes 119/120).

### Configuration

- Pack: `custom_nodes\MiniMax_H3_Semantic_Bridge` (nodes `MiniMaxH3DistilledImageToVideo`, `SenseNovaH3DistilledBridge`, `SenseNovaH3ClearDistilledCache`).
- Adapter: `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\semantic_bridge\MiniMaxH3_SemanticBridge_v1.safetensors` (~11 MB).
- **SCOPE: i2v/FL2VA (text-conditioned) ONLY — does NOT work for Ref2VA/R2V workflows.**
- **Tuning:** barely any change → raise `alpha` to 0.15; output looks off → lower to 0.05. `Clear Semantic Bridge Cache` node if swapping adapters mid-session.
- **GOTCHA:** the running ComfyUI is the `comfyUi_latest` instance — the adapter MUST be in `E:\comfyUi_latest\...\models\semantic_bridge\` (not the main `E:\ComfyUI_windows_portable\...` path) or the node shows "Missing Models".

### Status

Built + validated. NOT yet run. The working `jaisal_single_shot.json` was RESTORED clean (no bridge). See D046.

---

## 2026-08-31 — krea2_jaisal_sketch.json (new)

### Workflow

krea2_jaisal_sketch.json — Krea2 2D vector / line-art t2i generator for the Jaisal Cut title animation (stick figure).

### Objective

Generate the 2D line-art reference images for the title animation (a stick figure that walks the bridge, throws a paper plane, jumps into the river). The first image is the WALKING medium shot — the anchor we feed to MiniMax H3 so it animates the walk + head-turn + whistle + jump.

### Changes

- Cloned from the native `krea2_jaisal_refs.json` (preserves all native widget shapes / pos / size / inputs / outputs — no machine-built widget bug).
- LoRA node (15) → `krea2_lineart_v1_fp16.safetensors` @ 1.0 (the Civitai "Krea2 Line Art Style" LoRA, downloaded 2026-08-31).
- Positive prompt (node 6) → the WALKING stick-figure medium-shot prompt (2D vector line art, stick figure, line-art bridge + wavy line river, full body visible, medium shot).
- Negative prompt (node 13) → the sketch negative (excludes 3D / shading / color fill / cartoon / wide shot / close-up / special effects).
- SaveImage (29) → `jaisal_cut/sketch`.
- KSampler (3): 8 steps, cfg 1.0, euler/simple, denoise 1.0 (t2i). EmptyLatentImage (5): [2048, 1152, 1].

### Configuration

- Chain: UNET `krea2_turbo_fp8_scaled` → LoRA `krea2_lineart_v1_fp16` @1.0 → KSampler → VAEDecode → SaveImage.
- CLIP `qwen3vl_4b_fp8_scaled` (krea2), VAE `qwen_image_vae`.
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 1.0.
- Build script: `d:\models\vsCodeMcp\utilities\build_krea2_sketch.py`.

### Result

RAN (22.7s) → `output\jaisal_cut\sketch_00001_.png` (2048×1152). Pending user review in ComfyUI (vision unavailable in agent).

### Decision

Pending user review — confirm the line-art stick figure is clean (lines only, no shading/color fill, single character, medium shot). If good, this is the MiniMax anchor.

### Reason

User wants a 2D vector / line-art title animation (a stick figure, lines only, no cartoon/3D). The line-art LoRA carries the look. See D027.

---

## 2026-08-27 — krea2_jaisal_title_moody.json (new)

### Workflow

krea2_jaisal_title_moody.json — i2i fix for the FINAL/title shot: add ONLY moody climate, keep structure + boy position.

### Objective

- The final (aerial/title) shot was "messed up". Rather than recreate it, take the existing `storysheet_09_cut_title_scene_00001_.png` (staged as `jaisal_title_scene.png`) and add **only moody climate** — the bridge structure, river, banks, and the boy's position (MIDDLE of the bridge) stay EXACTLY the same.
- The camera ANGLE is handled separately by the user via their Qwen multi-angle workflow — this i2i does NOT change the angle.

### Changes

- Source image: `jaisal_title_scene.png` (from `output\jaisal_cut\storysheet_09_cut_title_scene_00001_.png`).
- Positive prompt: same scene/composition as reference (wide aerial stone bridge, boy in middle), keep structure/river/banks/position EXACTLY, ONLY change climate to MOODY (heavy dark overcast storm clouds, dim cold grey light, low mist, light rain, wet glistening stones, muted desaturated colors, dramatic moody lighting). Style prefix + single-character guard.
- KSampler: seed 424242, 8 steps, cfg 1.0, euler/simple, **denoise 0.4** (atmosphere-only, structure preserved).
- SaveImage prefix `jaisal_cut/title_moody`.
- Negative: carried over from krea2_jaisal_medium.json (identity/structure guard).

### Configuration

- Locked Krea2 chain: UNET `krea2_turbo_fp8_scaled` + LoRA `Krea2_Cinematic_Artstyle` @1.0 + CLIP `qwen3vl_4b_fp8_scaled` (krea2) + VAE `qwen_image_vae`.
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.4.
- Built from krea2_jaisal_medium.json template (UI format). Validated via MCP (valid, 0 errors).

### Result

Built + validated, NOT yet run. Pending user run + review in ComfyUI.

**2026-08-27 FIX (root cause):** machine-built `widgets_values` arrays were built from the API `/object_info` order, which is MISSING hidden widgets → arrays too short → positional shift → KSampler `cfg='euler'`/`sampler_name='simple'`/`scheduler=0.4` validation errors + LoadImage not showing. **Native UI-saved files use a DIFFERENT shape:** KSampler = **7** values `[seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]` (hidden `control_after_generate` = randomize/fix/+1/-1 dropdown next to seed), LoadImage = **2** values `[filename, "image"]`, and native files have **NO `widgets_values_named` key**. Fixed with `fix_native_shape.py` (KSampler=`[424242, 'randomize', 8, 1.0, 'euler', 'simple', 0.4]`, LoadImage=`['jaisal_title_scene.png', 'image']`, all `widgets_values_named` removed). Verified against native files + MCP validation (`valid: true`, 0 errors). **Open in a FRESH tab (not the stale `#converted-` view).** NOTE: this bug affects ALL machine-built workflows (the 08-27 converted batch + `jaisal_drone_optimized.json` + `krea2_jaisal_medium.json`) — fix them the same way before running.

### Decision

Pending user review — confirm the moody climate is added while the bridge structure and the boy's middle-of-bridge position are preserved.

**2026-08-27 POSE-DRIFT FIX:** user reported the boy's HEAD POSITION was changing between the reference and the i2i output. Root causes: (1) denoise 0.4 regenerates enough of the figure to re-derive the head angle; (2) the prompt re-described the pose as a fresh action ("looking at the sky above") instead of anchoring it to the reference, so the model re-posed it; (3) the negative's "different head position, different look" was too vague to push against. Fix applied via `fix_title_moody_prompts.py`:
- **Denoise 0.4 → 0.3** (biggest lever — preserves pose far better for a climate-only edit).
- **Positive:** anchor pose to reference — "EXACTLY matching the reference pose and head angle", "Keep ... body pose, and head angle EXACTLY the same as the reference", and describe the pose as a static state ("head tilted back with face and gaze turned upward toward the sky") rather than a new action.
- **Negative:** replaced the vague "different head position, different look" with concrete pose-locking terms: "changed pose, different pose, different body position, head facing forward, head turned to the side, looking down, looking at camera, turned away, different head angle, different body angle, shifted position, moved position".
- Validated: `valid: true`, 0 errors.
- **If head still drifts at 0.3:** try denoise 0.25, or use an inpaint/mask workflow (mask = sky + background only, exclude the boy) so the figure is never regenerated.

### Reason

User: "lets not recreate, lets add the moody climate alone for this storysheet_09_cut_title_scene_00001_ image in i2i, then i will get the angle from qwen multiple character angle workflow."

---

## 2026-08-26 — krea2_jaisal_aerial_v5.json (new)

### Workflow

krea2_jaisal_aerial_v5.json — drenchiness + face-continuity fixes for beats 08, 09

### Objective

- Beat 08 (v4) had the right pose/scene but was missing the DRENCHED/wet look from the previous shot.
- Beat 09 (v4) had a changed face (new kid) + a double-character problem.

### Changes

- **Beat 08 v5** (storysheet_08_cut_aerial_wide_v5): i2i from jaisal_ss08v4.png (the v4 08), SAME pose/scene, added DRENCHED/WET look (soaked hair/uniform, dripping, water droplets, wet glistening bridge), denoise 0.55.
- **Beat 09 v5** (storysheet_09_cut_aerial_title_v5): i2i from the NEW 08 v5 (chained, so the face stays consistent), boy = tiny dot far away, SINGLE character, DRENCHED, strong duplicate + "different face/new kid" negative.
- Negative strengthened: different character, different face, different boy, new kid, changed face, duplicate character, 2 kids, two kids, second kid, multiple people, extra person, double, twin, two figures, two boys, two people, reflection, mirror image.

### Configuration

- Same locked style chain + prefix
- 2048×1152, 8 steps, cfg 1.0, euler/simple
- Denoise: 0.55 (beat 8 — keep pose, add drench), 0.6 (beat 9 — zoom to tiny dot)
- Beats 8→9 chained for face continuity

### Result

All 2 frames generated, 2048×1152.

### Decision

Pending user review — confirm 08 v5 (drenched + same pose) and 09 v5 (same face, single character, tiny dot).

### Reason

The aerial section must keep the drenched look and the SAME kid's face across 08→09. Chaining 09 from the new 08 preserves the face; the drench prompt restores the wet look.

---

## 2026-08-26 — krea2_jaisal_aerial_v4.json (new)

### Workflow

krea2_jaisal_aerial_v4.json — corrected aerial sequence (beats 07, 08, 09)

### Objective

Fix the aerial "cut" section: beat 07 had a tilted camera; beat 09 had a double-character problem.

### Changes

- **Beat 07** (storysheet_07_cut_aerial_start_v4): NO camera tilt, boy centered (horizontally + vertically), bridge runs VERTICALLY through the frame (road/bridge surface behind the boy visible), boy looking up at the camera, close/medium. i2i from jaisal_medium_mid2.png.
- **Beat 08** (storysheet_08_cut_aerial_wide_v4): camera risen higher + pulled away (drone zoom-out), boy smaller + centered, more bridge + water revealed. i2i from beat 07 (chained).
- **Beat 09** (storysheet_09_cut_aerial_title_v4): max wide, boy = tiny dot, sky dominates upper frame (negative space for title), SINGLE character. i2i from beat 08 (chained).
- **Negative prompt strengthened** against duplicates: duplicate character, 2 kids, duplicated kids, two kids, second kid, multiple people, extra person, double, twin, two figures, two boys, two people, reflection, mirror image.

### Configuration

- Same locked style chain + prefix
- 2048×1152, 8 steps, cfg 1.0, euler/simple
- Denoise: 0.7 (beat 7), 0.6 (beats 8, 9)
- Beats 7→8→9 chained for a continuous drone ascent

### Result

All 3 frames generated, 2048×1152.

### Decision

Pending user review — confirm 07 no-tilt centered vertical-bridge, 08 zoom-out, 09 single-character max-wide.

### Reason

The aerial section must read as one continuous no-tilt drone ascent ending on a single-character wide shot for the title.

---

## 2026-08-26 — krea2_jaisal_fix05_inpaint.json (new)

### Workflow

krea2_jaisal_fix05_inpaint.json — inpaint the collar/tie region of beat 05 to remove the tie

### Objective

Remove the tie from storysheet_05 (rain close-up gust) that a low-denoise i2i (v3, v4) failed to remove. Inpainting regenerates ONLY the masked collar/tie region; the face, bag, and environment stay locked.

### Pipeline

- LoadImage (jaisal_ss05v4.png) → VAEEncode → SetLatentNoiseMask (mask) → KSampler (denoise 1.0, seed 545) → VAEDecode
- Mask: jaisal_ss05_tie_mask.png (grayscale ellipse over the collar/tie region) → ImageToMask (red channel) → GrowMask (expand 20, tapered_corners false)
- Prompt: "the shirt collar is open and untied, NO tie, no necktie, no bow tie"; negative: tie, necktie, bow tie, knotted tie, tied collar

### Result

storysheet_05_rain_closeup_gust_inpaint_00001_.png (2048×1152).

### Decision

Pending user review — confirm tie gone, face/bag intact. Adjust the mask ellipse if it missed the tie or bled into the face.

### Reason

A high-contrast element (tie) survives low-denoise i2i. Inpainting isolates the change to the masked region.

---

## 2026-08-26 — krea2_jaisal_continuity.json (new)

### Workflow

krea2_jaisal_continuity.json — visual-continuity fixes for the Jaisal Cut story sheet

### Objective

Fix continuity problems between shots WITHOUT independently redesigning scenes. i2i from the frame that already has the correct look, change only the specific problem.

### Fixes

- **Beat 3** (storysheet_03_run_medium_rain_v3): i2i from jaisal_ss04v2.png (04's preferred environment) + medium running prompt → transfers 04's background into 03's composition. Fixes the 03→04 background mismatch.
- **Beat 5** (storysheet_05_rain_closeup_gust_v3): i2i from jaisal_ss05v2.png + "NO tie, no necktie, open collar", denoise 0.5 → removes ONLY the tie, preserves bag color/environment/composition.
- **Beat 6** (storysheet_06_rain_closeup_clearing_v3): i2i from jaisal_ss06v2.png + "red school bag with BOTH shoulder straps visible", denoise 0.5 → fixes the missing strap, preserves everything else.
- **Beats 7→8→9** (chained aerial ascent): 07 from medium anchor (close/medium, kid centered, looks up at camera, bridge+water below) → 08 from 07 (risen higher, kid smaller, full bridge + more water) → 09 from 08 (max wide, kid = tiny dot, sky dominates, negative space for title). One continuous drone shot.

### Configuration

- Same locked style chain + prefix
- 2048×1152, 8 steps, cfg 1.0, euler/simple
- Denoise: 0.7 (beat 3, 7), 0.5 (beats 5, 6 — single-element fixes), 0.6 (beats 8, 9 — camera changes)
- Shared negative prompt node (includes tie, necktie, blue bag, duplicate character)

### Result

All 6 frames generated, 2048×1152.

### Decision

Pending user review — confirm 03↔04 background match, 05 tie removed, 06 both straps, 07→08→09 continuous aerial ascent.

### Reason

Visual continuity is the top priority for MiniMax to blend the frames into a coherent video. Targeted i2i from the good frame preserves identity/environment while fixing only the problem.

---

## 2026-08-26 — krea2_jaisal_storysheet.json (new)

### Workflow

krea2_jaisal_storysheet.json — the 9-image story sheet for "The Jaisal Cut"

### Objective

Generate all 9 story beats in one batch, each i2i from its anchor, so the face stays identical within each framing group.

### Anchors

- Beats 1, 2, 8, 9 (wide): jaisal_base_final.png (Anchor A)
- Beats 3, 7 (medium): jaisal_medium_mid2.png (medium anchor, kid at middle of bridge)
- Beats 4, 5, 6 (close-up): jaisal_face_v4_A.png (Anchor B)

### Beats (temporal order)

1. storysheet_01_run_wide — kid at start of bridge, calm sky, rain clouds on horizon
2. storysheet_02_run_mid_rain — kid mid-bridge running, first rain streaks, sky darkening, wind
3. storysheet_03_run_medium_rain — kid running, rain falling, dynamic, water splashing
4. storysheet_04_rain_closeup_start — kid's face, rain starting, looking ahead
5. storysheet_05_rain_closeup_gust — gust of rain sweeping across, droplets in frame, moody, wind-blown
6. storysheet_06_rain_closeup_clearing — rain gone, kid stopped, looking up, droplets on face
7. storysheet_07_cut_medium_pan — kid looking up, camera beginning to pan, sky clearing
8. storysheet_08_cut_wide_clearing — full scene, kid small figure, sky clearing, light breaking through
9. storysheet_09_cut_title_scene — title moment scene (kid looking up, sky clearing) WITHOUT text (title composited in post)

### Configuration

- Same locked style chain + prefix as base/face/medium
- 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.7
- Seeds: 101, 202, 303, 404, 505, 606, 707, 808, 909
- Shared negative prompt node (NEG) on all 9
- Beat 9 prompt explicitly excludes text/letters/words/title

### Result

All 9 frames generated, 2048×1152, ~3 min total on RTX 5090.

### Decision

Pending user review — flag weak frames for re-roll, then wire best 6-9 into MiniMax H3 video.

### Reason

9-image story sheet is the input for the MiniMax H3 ref-image-to-video (15s). Temporal order matters (MiniMax reads refs left-to-right as a storyboard).

---

## 2026-08-26 — krea2_jaisal_medium.json (new)

### Workflow

krea2_jaisal_medium.json — medium shot anchor for "The Jaisal Cut"

### Objective

Create a medium shot (head + upper body on the bridge) — wider than the face close-up (Anchor B) but tighter than the wide base (Anchor A). i2i from the face anchor to lock the kid's identity.

### Previous Version

krea2_jaisal_face_v3.json (face close-up, Anchor B)

### Changes

- i2i from jaisal_face_v4_A.png (latest face anchor)
- Prompt: medium shot, head + upper body, stone bridge handrails, paddy fields + coconut palms + open sky, no houses
- Same locked style chain + prefix as base/face
- denoise 0.7, 8 steps, cfg 1.0, euler/simple, 2048×1152
- Seeds: 343, 454, 777

### Result

krea2_medium_00001_.png (343), krea2_medium_00002_.png (454), krea2_medium_00003_.png (777) — all 2048×1152, ~16-20s each on RTX 5090.

### Performance

~16-20s per 2K image.

### Decision

User picked **00003 (seed 777)** as the base. Refined v2 (i2i from 00003): plain square handrail posts (no rounded/decorative), zoomed out a bit more (medium half shot), left hand holding the red school bag for support after running. krea2_medium_v2_00001_.png (555), krea2_medium_v2_00002_.png (888).

### Reason

Medium shot is the bridge between the wide base and the face close-up; needed for the story sheet's medium framing beats.

### Refinement notes (v2)

- Anchor changed from jaisal_face_v4_A.png → jaisal_medium_00003.png (keep approved composition, apply targeted fixes)
- Prompt: "medium half shot", "a little more of the bridge around him", "plain simple square stone handrail posts and a plain flat stone railing", "no rounded shapes, no decorative or exotic railing details", "his left hand holding the strap of a red school bag for support after running"
- Negative prompt added: rounded handrail, rounded railing, decorative railing, exotic railing, ornate railing, curved railing, fancy railing
- Output prefix → jaisal_cut/krea2_medium_v2

### Refinement notes (mid — middle of bridge)

- User preferred v2_00001 but the framing showed the kid at the START of the bridge with close trees/paddy fields
- Anchor changed → jaisal_medium_mid.png (the preferred v2_00001)
- Prompt: "standing at the middle of the stone bridge, the bridge stretching away on both sides", "the lush paddy fields and tall coconut palms are far in the background, distant and small"
- Negative prompt added: close trees, close paddy fields, foreground trees
- Output prefix → jaisal_cut/krea2_medium_mid
- Result: krea2_medium_mid_00001..2.png (seeds 666/999). **jaisal_medium_mid2.png (mid_00001) staged as the medium anchor** for the story sheet.

---

## 2026-08-26 — Baseline inventory (no changes)

### Workflow

All existing saved workflows in E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows

### Objective

Record the known-good baseline before any modifications begin.

### Previous Version

None — initial inventory.

### Changes

None. Inventory only.

Image:

- jaisal_shot1_t2i.json
- jaisal_shot2_i2i.json
- jaisal_shot3_i2i.json
- jaisal_sketch_shot1_i2i.json
- jaisal_sketch_shot2_i2i.json
- jaisal_sketch_shot3_i2i.json
- krea2_jaisal_base.json
- krea2_jaisal_face.json
- krea2_jaisal_face_v2.json
- krea2_jaisal_face_v3.json
- kerala_kid_2d_ref.json
- _ref_krea2_t2i_int8.json
- oneNode-Flux.json

Video:

- video_minimax_h3_t2v.json
- mini-max-refrance-to-video-1.json
- MiniMaxH3_NativeAudio_MusicVideo_TEMPLATE.json
- RIFE_WAN_Method_Interpolation_TEMPLATE.json

Chained series (each with a GGUF variant):

- 05_Chained.json / 05_GGUF_Chained.json
- 06_Chained_AudioLock.json / 06_GGUF_Chained_AudioLock.json
- 07_Chained_RefImage.json / 07_GGUF_Chained_RefImage.json
- 08_Chained_RefImage_AudioLock.json / 08_GGUF_Chained_RefImage_AudioLock.json

### Result

Baseline recorded.

### Performance

Not benchmarked yet.

### Decision

Keep all as-is until individually changed.

### Reason

Preserve known-good workflows; compare every new version against this inventory.

---


---

## jaisal_drone_optimized.json (MiniMax H3 optimized drone ascent)

Date: 2026-08-27
Status: Built + validated, NOT yet run

### Purpose

Fast 15s drone-ascent shot for "The Jaisal Cut" (kid on bridge -> tiny dot). First-last-frame interpolation via fl2va model, optimized for RTX 5090 speed.

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_drone_optimized.json

### Models

- UNET: minimax_h3_fl2va_pruned_int8_convrot.safetensors (first-last-frame)
- LoRA: minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors (turbo 4-step, strength 1.0)
- CLIP: qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (type minimax)
- VAE: minimax_h3_video_vae_fp16.safetensors + minimax_h3_audio_vae_fp32.safetensors

### Key custom nodes

- MiniMaxH3ActivationChunkStar7 (Star7 pack) - attention_backend=comfy_kitchen_int8, chunk_tokens=8192, mlp=8192, qkv=4096
- RTXVideoSuperResolution (comfyui_nvidia_rtx_nodes) - 2x ULTRA upscale
- MiniMaxH3ReferenceToVideo (core) - ref_image_0=jaisal_mm_start.png, ref_image_1=jaisal_mm_final.png

### Resolution / params

- 864x480 (0.4MP 16:9), 362 frames (15s @24fps), BasicScheduler simple/8/1, KSamplerSelect res_multistep
- Save prefix: video/Jaisal_Drone

### Chain

UNETLoader -> LoraLoaderModelOnly -> MiniMaxH3ActivationChunkStar7 -> BasicScheduler + BasicGuider -> SamplerCustomAdvanced -> VAEDecode -> RTXVideoSuperResolution -> CreateVideo(24fps) -> SaveVideo

### Known issues

- NOT yet run. First run should be timed (target <15-20 min for 2K; this is 0.4MP so faster).
- Star7 pack must be loaded (ComfyUI restarted after clone).
- widgets_values_named were stale from the turbo template and FIXED (all 7 modified nodes consistent).

### Next improvement

- Run at 0.4MP, time it, review quality. Then bump to 2K (1344x768 or higher) and re-time.
- If CK INT8 quality is too approximate, try attention_backend=existing (native pytorch cross-attention) or Spectrum.

## jaisalproduction1.json + jaisalproduction2.json (MiniMax H3 R2V, 2-pipeline — CURRENT)

Date: 2026-08-30
Status: Built + validated (`valid: true`, 22 nodes each), NOT yet run

### Purpose

The full ~26s title sequence split into **two separate MiniMax R2V generations** (shorter clips = less style drift, cleaner 3-ref mapping, the jump is a natural splice point). Shot 3 (running medium) removed.

- **`jaisalproduction1.json`** — run-up, **15s**, save `video/Jaisal_Production_1` (prompt v10 + REFERENCE VIDEO + 1MP, 2026-08-30):
  - ref_image_0 = jaisal_1_longshot.png → [Shot 1] **WIDE ANGLE** establishing shot (camera positioned FAR AWAY, boy a small figure with full landscape/sky/river visible, NOT a medium/close-up, camera fixed), ONLY ONE boy (standing on the LEFT side of the bridge, NO extra characters) WALKS and SLOWLY RUNS (natural gait, feet lift+land separately, NOT a slide), MAIN PURPOSE = ESTABLISH THE CLIMATE AND MOOD (sky clear→moody, RAIN BEGINS TO FALL and builds, landscape shifting) **~4s** (00:00.000)
  - ref_image_1 = jaisal_2_closeup.png → [Shot 2] close-up, boy RUNS, then SLOWS + STOPS + TURNS toward HIS RIGHT = the VIEWER'S LEFT (toward the river), the turn is clear and deliberate (body rotates fully) **~6s** (00:04.000 → 00:10.000) (UNCHANGED — stable)
  - ref_image_2 = jaisal_4_middle.png → [Shot 3] SIDE view from the VIEWER'S LEFT (boy on viewer's left, facing the handrail) → the boy is **NOT a static frame** - he is **SLOWLY LIFTING HIS LEG and CLIMBING over the handrail, then JUMPING** (NO hand gestures/head shake - that confused the model), he is not repeating the movement, he breathes in after the run → then **LEAPS over the handrail SLOWLY fully airborne** (the bridge is TALL - a real leap from height over the wide river, NOT a shallow pool) → camera ANCHORED on viewer's left + TRACKS him (NOT a left-to-right sweep) → camera swings to his BACK side, ENDS at his back mid-air **BEFORE he reaches the water** (the cut happens here so the next clip picks up the jump) **~5s** (00:10.000)
  - **ORIENTATION block:** "The boy's RIGHT side is the VIEWER'S LEFT side of the frame. When the boy turns toward his right, he turns toward the VIEWER'S LEFT. [Shot 3] is a side view from the VIEWER'S LEFT side, and the boy is on the VIEWER'S LEFT of the frame." + "All left/right references use the VIEWER's perspective".
  - **RAIN enforced in EVERY shot (v7):** detailed_description global line "RAIN is present in EVERY shot - rain is falling in [Shot 1], [Shot 2], and [Shot 3]" + overall_soundscape "RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3])". Shot 1 = rain BEGINS and builds; Shot 2 = rain streaks visible; Shot 3 = HEAVY RAIN.
  - **Sound (v10):** "Clear footsteps on the stone bridge, RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3]), a building thunderstorm with distant thunder rumbles, splashing water on the bridge stones, then a rising tension as the boy climbs and leaps."
  - **overall_landscape (v10, NEW):** "We should see VISIBLE RAINFALL throughout the sequence after the first picture - rain is clearly falling and visible in [Shot 2] and [Shot 3]."
  - **REFERENCE VIDEO (motion anchor, 2026-08-30):** a `MiniMaxH3ReferenceVideoLoadStar7` node (id 149) loads `input\jaisal_prod1_ref.mp4` (= the good output `Jaisal_Production_1_00011_.mp4`) → wired to `ref_videos.ref_video_0` (link 303) + `ref_video_audios.ref_video_audio_0` (link 304) so the new render FOLLOWS THE SAME ACTION. The 3 reference images stay as visual anchors.
  - **Resolution (2026-08-30):** `ResolutionSelector` (node 115) set to `['16:9 (Widescreen)', 1.0, 32]` → **1344×768 (MiniMax H3 NATIVE canvas)**. The 2K (2.4 MP) render VRAM-thrashed (stuck at 0/8 steps in "Model Initializing" for 10+ min on the 32 GB card) so it was dropped. 1MP fits VRAM, ~25–40 min. For 2K, render at 1MP then UPGRADE with an upscaler (Topaz/RTX/Hunyuan, all installed). Render-time baseline from the user's own outputs: ~10–15 min per 0.4 MP, so 1MP ≈ 25–40 min.
  - **CRITICAL (v3→v4):** MiniMax DROPPED Shot 3 entirely in the v2 run → prompt hard-emphasizes "ALL THREE shots must appear in this order, each getting its full time - do not skip, compress, or drop any shot, especially [Shot 3]" (in summary + detailed_description). **v4:** the wide shot is ALSO a hard demand — "[Shot 1] MUST be a LONG WIDE establishing shot (a hard requirement - it must NOT be cut short, NOT turned into a close-up, NOT skipped)" + slow running + the shot's MAIN PURPOSE is to ESTABLISH THE CLIMATE CHANGE. **v5:** orientation fix (boy's right = viewer's left, all left/right from viewer's perspective), shot 3 camera anchored on viewer's left + tracks (NOT a left-to-right sweep), sound = running footsteps + thunderstorm rumbles, sliding fix (real gait, feet lift+land separately). **v6:** CHARACTER COUNT block HARD-DEMANDS ONLY ONE character / no duplicates (v5's shot 1 came out with 2 boys), shot 3 JUMP made explicit + sped up (crouch → plant → LEAP over handrail → DIVE into river fully airborne, "NOT just climbing/standing/walking"), sound adds a big SPLASH as he jumps. **v7:** SIMPLIFIED (removed the heavy CHARACTER COUNT block + over-stuffed negative constraints that "didn't apply well"), shot 1 focuses on CLIMATE + MOOD (boy WALKS / SLOWLY RUNS), shot 3 ENDS mid-air BEFORE the water (bridge is TALL, NOT a shallow pool, cut at the apex so the next clip picks up the jump), RAIN enforced in EVERY shot (detailed_description global line + overall_soundscape). **v8:** timing split 4/6/5 (shot 1 = 4s, shot 2 = 6s 00:04.000→00:10.000 with a clear deliberate turn, shot 3 = 5s 00:10.000), shot 3 STARTS IN MOTION ("the boy is ALREADY RUNNING and IN MOTION at the start - he is NOT standing still" + <Picture 3> definition = "already running toward the handrail") because v7's shot 3 starting frame came out standing still. **v9:** shot 3 camera moves RESTORED to v5 (anchored on viewer's left + tracks, swings to back), shot 3 is NOT a static frame - the boy PREPARES while the camera moves (shakes head, hand gestures, gets ready) then LEAPS (replaces v8's over-constrained "already running at the start"), <Picture 3> definition = "preparing to jump over the handrail", CLEAN RULE = state WHERE he is + WHAT he is doing in ONE direction (no running back and forth). **v10:** shot 1 = **WIDE ANGLE** establishing shot (camera positioned FAR AWAY, boy a small figure with full landscape/sky/river visible, NOT a medium/close-up) + ONLY ONE boy on the LEFT side of the bridge (NO extra characters), shot 3 = **SLOWLY LIFTING HIS LEG and CLIMBING over the handrail, then JUMPING** (removed the v9 hand gestures/head shake that confused the model), he is not repeating the movement, he breathes in after the run, LEAPS SLOWLY, new **overall_landscape** section (VISIBLE RAINFALL throughout after the first picture).
- **`jaisalproduction2.json`** — leap + title, **11s**, save `video/Jaisal_Production_2`:
  - ref_image_0 = jaisal_5_jump.png → [Shot 1] SHORT natural leap CLOSE to bridge (NOT a long throw) ~2s
  - ref_image_1 = jaisal_6_underwater.png → [Shot 2] underwater, sinks completely down, rising bubbles ~4.5s
  - ref_image_2 = jaisal_7_title.png → [Shot 3] title card, bubbles foam up, 'The Jaisal Cut' slowly becomes visible, color grade matches shot 2 ~4s

Both prompts lock a consistent color grade (same dark moody palette / dim grey light / water color). **Splice:** pipeline 1 ends mid-launch, pipeline 2 starts in-air → hard cut + color-match the splice frame in post. Build script: `build_production_pipelines.py`.

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json
E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction2.json

---

## jaisal_lowangle.json (MiniMax H3 R2V, 7-image — SUPERSEDED by the 2-pipeline split)

Date: 2026-08-30 (rebuilt from the 2-image version)
Status: Built + validated (`valid: true`, 0 errors, 26 nodes), NOT yet run

### Purpose

Cinematic 7-shot R2V sequence for "The Jaisal Cut" (production-quality intro). Uses **7 reference images** as frame anchors, one per shot:
- `jaisal_1_longshot.png` → `ref_image_0` → `<Picture 1>` → [Shot 1] long shot (boy runs, sky darkens, wind + rain begins)
- `jaisal_2_closeup.png` → `ref_image_1` → `<Picture 2>` → [Shot 2] close-up (camera push-in + wind)
- `jaisal_3_running.png` → `ref_image_2` → `<Picture 3>` → [Shot 3] running (camera tracks alongside, wind + rain)
- `jaisal_4_middle.png` → `ref_image_3` → `<Picture 4>` → [Shot 4] middle full figure (ADD heavy rain)
- `jaisal_5_jump.png` → `ref_image_4` → `<Picture 5>` → [Shot 5] wide low-angle jump (camera completes motion into river)
- `jaisal_6_underwater.png` → `ref_image_5` → `<Picture 6>` → [Shot 6] underwater (boy sinks completely down)
- `jaisal_7_title.png` → `ref_image_6` → `<Picture 7>` → [Shot 7] title card (bubble-formed 'The Jaisal Cut')

All transitions smooth and organic. **CRITICAL:** `<Picture N>` maps 1-to-1 to `ref_image_N` in connection order (each reference = its shot's first frame). Bag color = BLACK school bag. Title shown in Shot 7 (not a text overlay).

### 2026-08-30 rebuild (2-image → 7-image)

Rebuilt with `build_minimax_7shot.py`: copied the 7 output images to `input\` (clean names), added 5 LoadImage nodes (147-151), grew node 136 to 7 `ref_image` slots (3-9), shifted downstream link slots (prompt→13/width→14/height→15/length→16), added links 289-294, wrote the 7-shot prompt (node 138). **Note:** this is a deliberate departure from the earlier "keep R2V to 2-3 refs" lesson — the user has a full 7-image set and wants a 7-shot cinematic sequence, so each reference is a clean per-shot anchor (not a confused 5-anchor storyboard).

### Purpose (2-image, 2026-08-28 — SUPERSEDED)

15s two-shot R2V sequence. Uses **2 reference images** as frame anchors: `1.png` (boy at START of bridge) → [Shot 1], `2.png` (boy in MIDDLE of bridge) → [Shot 2]. The boy walks → weather turns → runs through the rain. Title composited in post.

### 2026-08-28 rebuild (5-image → 2-image)

The 5-image version came out bad (style drift, kid not running, model confused by 5 `<Picture N>` tags + a 500-word prompt). Rebuilt with `build_2ref.py`: deleted LoadImage nodes 143/LA4/LA5 (3.png/4.png/5.png) + links 285/289/290, cleared `ref_image_2/3/4` link fields, wrote a SIMPLE prompt with only 2 `<Picture N>` tags (each explicitly "the first frame of [Shot N]"). **Lesson: keep R2V to 2-3 reference images max with a simple prompt — the model maps refs to shots far better with fewer, clearer anchors.**

### Purpose (original 5-image, 2026-08-27 — SUPERSEDED)

15s five-shot R2V sequence for "The Jaisal Cut" low-angle ending. Uses 5 reference images (1.png–5.png) as frame anchors for 5 shots, ending on a low-angle long shot with negative space for the title (composited in post).

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json

### Models

- UNET: minimax_h3_ref2va_pruned_int8_convrot.safetensors (ref2va — reference-to-video)
- LoRA: minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors (turbo 4-step, strength 1.0)
- CLIP: qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (type minimax)
- VAE: minimax_h3_video_vae_fp16.safetensors + minimax_h3_audio_vae_fp32.safetensors

### Key custom nodes (CURRENT 7-image)

- MiniMaxH3ReferenceToVideo (core, node 136) — 7 ref images wired (slots 3-9):
  - ref_image_0 = jaisal_1_longshot.png → `<Picture 1>` → [Shot 1]
  - ref_image_1 = jaisal_2_closeup.png → `<Picture 2>` → [Shot 2]
  - ref_image_2 = jaisal_3_running.png → `<Picture 3>` → [Shot 3]
  - ref_image_3 = jaisal_4_middle.png → `<Picture 4>` → [Shot 4]
  - ref_image_4 = jaisal_5_jump.png → `<Picture 5>` → [Shot 5]
  - ref_image_5 = jaisal_6_underwater.png → `<Picture 6>` → [Shot 6]
  - ref_image_6 = jaisal_7_title.png → `<Picture 7>` → [Shot 7]
- LoadImage nodes: 137 (1), 139 (2), 147 (3), 148 (4), 149 (5), 150 (6), 151 (7)
- ref_image_size: match

### Resolution / params

- 1344x768 (2K 16:9), 15s, BasicScheduler simple/8/1, KSamplerSelect res_multistep
- Save prefix: video/Jaisal_2Ref_1_2 (update to e.g. video/Jaisal_7Shot for the 7-shot run)

### Prompt style (CURRENT 2-image — SIMPLE)

Official MiniMax H3 R2V style but SIMPLIFIED (see `d:\models\vsCodeMcp\docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md`):
- Only `<Picture 1>` + `<Picture 2>` tags, each explicitly "the first frame of [Shot N]"
- `<Subject 1>` = the boy (both pics), `<Subject 2>` = the stone bridge (both pics)
- 6-section structure kept but SHORT (no 500-word bloat)
- 2 shots: [Shot 1] boy at start of bridge, walks, sky darkens, wind, rain, starts running; [Shot 2] At 00:07.000 boy in middle of bridge, running through heavy rain, drenched
- Title composited in post (NOT rendered by the model)

### Shot plan (15s, 2 shots)

- Shot 1 (0-7s): boy at start of bridge (from 1.png), walks forward, sky darkens, wind picks up, rain begins, boy starts running
- Shot 2 (7-15s): boy in middle of bridge (from 2.png), running through heavy rain, fully drenched, water splashing on stones, camera follows

### Known issues

- 5-image wiring bug FIXED (2026-08-27): `ref_image_3`/`ref_image_4` had `link=None` despite links existing. Fixed by setting `link` by slot index (6/7), not name number (3/4). See `fix_lowangle_wiring_and_prompt.py`.
- 5-image version came out bad (style drift, no running) → rebuilt as 2-image (2026-08-28).
- NOT yet run. Confirm ComfyUI running with Star7 pack before running.

### Next improvement

- Run the 2-image version, review quality in ComfyUI.
- If 2-image works, this is the template for all future R2V shots (2-3 refs max, simple prompt).
- If the boy still doesn't run, try adding a 3rd reference (a running pose) or a stronger motion verb in the prompt.

## krea2_identity_edit.json (Krea2 Identity Edit v1.2 — face consistency)

Date: 2026-08-29
Status: Validated (`valid: true`, 1 expected warning), ready to use

### Purpose

Lock the SAME face across the Jaisal Cut reference set (D023). "Use an image like a LoRA": load a reference (character sheet / clean close-up), write a plain-English instruction, regenerate the scene keeping the same face/identity. Fixes the "different guy every time" problem from t2i.

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json

### Models / nodes

- UNET: krea2_turbo_fp8_scaled.safetensors
- LoRA: krea2_identity_edit_v1_2.safetensors @ 1.0 (INSTALLED, 1.83 GB)
- CLIP: qwen3vl_4b_fp8_scaled.safetensors (type krea2)
- VAE: qwen_image_vae.safetensors
- Krea2EditModelPatch (ref_boost=4, ref_boost_a=1, fit_mode=fit) — from `comfyui-krea2edit` node pack (INSTALLED)
- Krea2EditGroundedEncode (instruction + grounding_px=768)
- KSampler: 10 steps, cfg 1, euler/simple (turbo)
- ResolutionSelector: 1:1 1MP (1024×1024) — the 1MP sweet spot

### Key params

- `ref_boost` (fidelity dial) = 4.0 recommended (strong face+body likeness; >10 over-copies, <1 suppresses the ref)
- `grounding_px` 384-768 (lower if compositions double/split)
- 2nd-image group (person-into-scene) ships BYPASSED — enable by right-clicking the group title → toggle Bypass off

### Usage for Jaisal Cut

1. Load a clean character reference (character sheet or close-up) in the LoadImage node (node 72)
2. Write the instruction in node 84 (e.g. "the same boy running on the stone bridge in heavy rain, square stone handrails, moody overcast")
3. Queue → same face, new scene

### Known issues

- 1 expected warning: node 79 `source_latent_b` edge_type_mismatch (the optional 2nd-image group ships bypassed — harmless).

## krea2_jaisal_refs.json (Krea2 reference-image generator)

Date: 2026-08-28
Status: Built + validated (`valid: true`, 0 errors), ready to run

### Purpose

Generate the Krea2-styled REFERENCE SET for the Jaisal Cut (D021): character sheet (faceless), abstract, bridge, medium, close-up, water, running. Feed 2-3 of these to MiniMax H3 R2V so it holds the angular brush-stroke style across the WHOLE video (not just the first 2-3s).

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_refs.json

### Models (locked Krea2 chain)

- UNET: krea2_turbo_fp8_scaled.safetensors
- LoRA: Krea2_Cinematic_Artstyle.safetensors @ 1.0
- CLIP: qwen3vl_4b_fp8_scaled.safetensors (type krea2)
- VAE: qwen_image_vae.safetensors

### Params

- KSampler: 8 steps, cfg 1.0, euler/simple, denoise 1.0 (t2i)
- 2048×1152 (2K 16:9)
- Save prefix: jaisal_cut/refs
- Default positive prompt = faceless character sheet (front/side/back turnaround)

### Character (D022)

Normal young schoolboy with short dark hair (face OK — Krea2 can't do faceless). Costume: rose-pink collared shirt, full-length black trousers, black school bag. ALWAYS "ONLY ONE character, no duplicates". Bridge prompt pins the boy ON THE BRIDGE DECK (left side), NOT in the water.

### Prompts

`d:\models\vsCodeMcp\prompts\jaisal_ref_prompts.txt` — 7 ready-to-paste prompts (character sheet, abstract, bridge, medium, close-up, water, running) + shared negative + how-to-use.

### Next improvement

- Run each prompt, save as refs_*.png, stage the best 2-3 into input\, feed to MiniMax R2V.
- Update the MiniMax prompt (v2) to "black school bag" + faceless when re-running.

## jaisal_single_shot.json (MiniMax H3 i2v single-shot, 1 image)

Date: 2026-08-28
Status: Built + validated (`valid: true`, 0 errors), NOT yet run

### Purpose

PIVOT from the 5-image R2V (which came out bad — style drift, no running, no intro). ONE continuous shot from `1.png` (wide base): boy walks the bridge → sky darkens, wind, rain → boy runs → boy jumps into the river midway → camera dips underwater with bubbles (title composited in post over the bubbles).

### Location

E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json

### Built from

`video_minimax_h3_i2v` template (Image to Video). Built via `build_single_shot.py` + `fix_single_shot.py` + inline subgraph LoRA fix.

### Models

- UNET: minimax_h3_fl2va_pruned_int8_convrot.safetensors (first/last-frame)
- LoRA: minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors (turbo 4-step, strength 1.0) — on INTERNAL subgraph node 121
- CLIP: qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors (type minimax)
- VAE: minimax_h3_video_vae_fp16.safetensors + minimax_h3_audio_vae_fp32.safetensors

### Key custom nodes

- MiniMaxH3ImageToVideo (SUBGRAPH, type UUID `4c314f31-ecda-4b08-ae98-faaba1bf613f`, instance id=105) — first_frame = 1.png, last_frame = none
- ResolutionSelector: 16:9 (Widescreen), 0.98MP → 1344×768
- Save prefix: video/Jaisal_SingleShot

### Prompt

Simple single-shot (NOT the 500-word R2V structure): opens exactly on `<Picture 1>` (boy at start of bridge) → walks → sky darkens/wind/rain → runs → jumps into river midway → camera dips underwater with bubbles. Title composited in post (NOT rendered). Audio: wind building, rain, splash, muffled underwater.

### Gotchas

- The i2v template's main node is a SUBGRAPH — widget values (prompt, duration, turbo, LoRA) must be set on the INTERNAL nodes (`definitions.subgraphs[0].nodes`), not just the instance. LoRA on internal node 121.
- Template default LoRA (`fl2v_turbo_8step`) not installed → swapped to 4-step 768p.
- `ResolutionSelector` aspect enum is `16:9 (Widescreen)` (template's `Widescreeen` spelling fails validation).
- Instance node's `widgets_values_named` dict is preferred over `widgets_values` by the converter — update both.

### Next improvement

- Run, review in ComfyUI. If the jump-to-river is too much for one shot, split into two i2v runs (walk→run→jump, then underwater) and stitch in post, or drop the jump and end on the run.

## krea2_1click_dataset.json (2026-10-08)
**Purpose:** one-Run 20-image Krea 2 character dataset (same boy, 20 scenes).
**Status:** BUILT + validates clean; awaiting user's manual run.
**Location:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_1click_dataset.json`
**Models:** krea2_turbo_fp8_scaled (UNET), qwen3vl_4b_fp8_scaled (CLIP, type krea2),
qwen_image_vae, krea2_identity_edit_v1_2 @1.0, RawGirlV3 @1.2.
**Custom nodes:** Krea2EditModelPatch + Krea2EditGroundedEncode (comfyui-krea2edit),
PixaromaPromptEach (ComfyUI-Pixaroma).
**Resolution:** 2048×1152 (16:9).
**Key params:** ref_boost 4.0, fit, grounding_px 768, 10 steps, cfg 1, euler/simple,
denoise 1. Ref image `krea2_test_ref.png`.
**Known issues:** none (validates clean). Second-ref group + Typnosis LoRA bypassed.
**Builder:** `d:\models\vsCodeMcp\utilities\build_krea2_1click_dataset.py`.
**Next improvement:** after the 20-image run, pick the best master image and build
the character sheet from it.

## krea2_t2i_character.json (2026-10-08)
**Purpose:** generate the character FROM SCRATCH with Krea 2 t2i → 6 face
candidates in one Run; pick the best face as the MASTER reference.
**Status:** BUILT + validates clean; awaiting user's manual run.
**Location:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_character.json`
**Models:** krea2_turbo_fp8_scaled (UNET), qwen3vl_4b_fp8_scaled (CLIP, type
krea2), qwen_image_vae, RawGirlV3 @1.0. NO reference image, NO identity LoRA.
**Resolution:** 1152×2048 portrait.
**Key params:** 10 steps, cfg 1, euler/simple, denoise 1.
**Builder:** `d:\models\vsCodeMcp\utilities\build_krea2_t2i_character.py`.
**Next improvement:** after picking the best face, use it as ref in
`krea2_1click_dataset.json` (node 72).

## krea2_t2i_char1.json + krea2_t2i_char2.json (2026-10-08)
**Purpose:** generate TWO distinct 26yo Kerala male characters FROM SCRATCH
with Krea 2 t2i — 6 candid-environmental face candidates each; pick the best
face per character as the MASTER reference.
**Status:** BUILT + BOTH VALIDATE CLEAN (13 nodes, 0 errors); awaiting user's
manual run. FameGridColorFinish node 302 confirmed registered (false-alarm
blocker resolved 2026-10-08).
**Location:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json` / `krea2_t2i_char2.json`
**Models:** krea2_turbo_fp8_scaled (UNET), qwen3vl_4b_fp8_scaled (CLIP, type
krea2), qwen_image_vae. LoRA chain: Krea2-realism-V2 @1.0 (node 96) ->
famegrid_spicy_3167060 @0.7 (node 97). NO reference image, NO identity LoRA.
**Resolution:** 1152×2048 portrait.
**Key params:** 10 steps, cfg 1, euler/simple, denoise 1.
**Node 302:** FameGridColorFinish (color_strength 1.0, sharpen_strength 0.6)
wired VAEDecode(54) -> 302 -> SaveImage(29), links 10 & 13.
**Char 1:** ROUND soft face, MEDIUM WAVY hair (loose, messy), FULL unkempt
beard, dark t-shirt. Prefix `krea2_char1_face`.
**Char 2:** ANGULAR face + jawline, LONG hair tied-up man-bun (Gareth Bale
2018), SHORT patchy beard, white t-shirt. Prefix `krea2_char2_face`.
**Framing:** CANDID ENVIRONMENTAL phone-shots in real Kerala settings (backwater
path, houseboat, monsoon rain, college campus, temple wall, auto-rickshaw).
NO lens specs, NO posed headshots. Negative kills the stock-photo look.
**Builder:** `d:\models\vsCodeMcp\utilities\build_krea2_t2i_characters.py`.
**Next improvement:** after picking the best face per character, use it as ref
in `krea2_1click_dataset.json` (node 72) for the 20-image dataset.
