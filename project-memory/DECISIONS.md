# Project Decisions

## D001 — Use ComfyUI MCP for workflow interaction

Date: 2026-08-26
Status: Active

### Decision

Use ComfyUI MCP as the primary interface for inspecting, creating, modifying, and executing ComfyUI workflows.

### Reason

MCP can interact with the actual ComfyUI environment and saved workflows instead of relying on the model's knowledge of ComfyUI.

### Alternatives

Manual workflow editing and manually describing nodes to the model.

### Result

ComfyUI MCP is successfully generating and modifying workflows.

---

## D002 — Use local Qwen as the reasoning model

Date: 2026-08-26
Status: Active

### Decision

Use the local Qwen model through llama.cpp rather than relying on Claude/Codex for ComfyUI reasoning.

### Reason

Local inference provides control over the model, context, performance, and cost.

### Result

Qwen is successfully interacting with ComfyUI through MCP.

---

## D003 — Preserve project knowledge in Markdown

Date: 2026-08-26
Status: Active

### Decision

Use Markdown files under `project-memory/` as persistent project state.

### Reason

The AI chat context is temporary. Important project decisions must survive model/session changes.

### Result

Project state, decisions, experiments, and workflow history are stored separately from chat history.

---

## D004 — "The Jaisal Cut" title is composited in post, not rendered

Date: 2026-08-26
Status: Active

### Decision

Do NOT render the "The Jaisal Cut" title text with the diffusion model. Generate the title frame as the scene (kid looking up, sky clearing) without text, then composite the title + the J-dot effect (kid becomes the dot in the J) in post (After Effects / DaVinci Resolve).

### Reason

Diffusion is unreliable at spelling text correctly. The J-dot is a 2-second post effect, not a generation problem. This is the single biggest quality win.

### Alternatives considered

- In-image text rendering (rejected — unreliable spelling)

### Result

Title frame generated text-free; title + J-dot added in post.

---

## D005 — Locked Krea2 style chain for all Jaisal Cut frames

Date: 2026-08-26
Status: Active

### Decision

Every Jaisal Cut frame uses the same chain: `krea2_turbo_fp8_scaled.safetensors` + `Krea2_Cinematic_Artstyle.safetensors` LoRA (strength 1.0) + `qwen3vl_4b_fp8_scaled.safetensors` CLIP (type krea2) + `qwen_image_vae.safetensors`, with the style prefix "An angular, 3d art style, with brush stroke color texture." on every prompt. 2048×1152, 8 steps, cfg 1.0, euler/simple, denoise 0.7 for i2i.

### Reason

Consistent style = MiniMax blends the 9 frames smoothly into the 15s video. Identity is locked by i2i from the face anchor.

### Alternatives considered

- Per-frame style variation (rejected — breaks MiniMax blending)

### Result

All frames share one style; identity locked via i2i anchors.

---

## D006 — Medium shot is i2i from the face anchor

Date: 2026-08-26
Status: Active

### Decision

The medium shot (head + upper body on the bridge) is generated i2i from the face anchor (jaisal_face_v4_A.png), not t2i, to lock the kid's identity while widening the framing.

### Reason

t2i would risk a different face; i2i from the face keeps identity consistent across the wide / medium / close-up framings.

### Alternatives considered

- t2i medium shot (rejected — identity drift)

### Result

krea2_jaisal_medium.json generates the medium anchor with locked identity.

---

## D007 — Single character only, no duplicates

Date: 2026-08-26
Status: Active

### Decision

Every frame must show exactly ONE kid. No duplicate characters, no second kid. Added "duplicate character, 2 kids, duplicated kids, two kids, second kid" to the shared negative prompt, and "a single young Indian schoolboy, one kid only" to the wide-shot prompts.

### Reason

storysheet_01 rendered two characters (start and end of the bridge). The story is about one kid.

### Result

Single-character constraint enforced on all frames.

---

## D008 — Consistent costume: red school bag, no tie

Date: 2026-08-26
Status: Active

### Decision

The kid's red school bag must stay RED across all frames (it turned blue in the close-up). The kid wears NO tie (a tie appeared in the gust frame that wasn't in the others). Added "red school bag" to close-up prompts and "tie, necktie, blue bag, blue school bag" to the negative.

### Reason

Costume consistency is critical for MiniMax to blend the frames smoothly. A color change or added accessory breaks continuity.

### Result

Red bag + no tie enforced on all frames.

---

## D009 — Close-up frames keep the moody atmosphere

Date: 2026-08-26
Status: Active

### Decision

The close-up frames (4, 5, 6) keep the same moody overcast atmosphere. Beat 6 (rain clearing) is NOT a sunny/cleared sky — the rain has just stopped for a moment, the sky is still dark and moody. The rain effect from the generated frames is preserved by i2i from the current frames (jaisal_ss04/05/06.png).

### Reason

The emotional core is the rain coming and going in a moody setting. A sudden sunny sky breaks the mood. The rain effect in the generated frames is good and should be kept.

### Result

Moody atmosphere + preserved rain effect on close-up frames.

---

## D010 — The "cut" section camera is above the kid, zooming out

Date: 2026-08-26
Status: Active

### Decision

The "cut" section (beats 7, 8, 9) uses a HIGH-ANGLE camera above the kid (looking down, seeing the bridge + water body underneath), the kid looking up at the sky, and the camera panning + zooming out. Beat 8 CONTINUES the zoom-out (does NOT revert to the initial river-level camera). Beat 9 is the final wide shot of the whole river bridge (kid = the dot in the J), no text. Beats 7→8→9 are chained (each i2i from the previous) for a smooth zoom-out.

### Reason

The initial river-level camera (beats 1-2) is a different shot. The "cut" is a new camera angle (above the kid) that pans and zooms out to reveal the whole bridge for the title. Reverting to the river camera broke the flow.

### Result

Smooth high-angle zoom-out for the cut section, ending on the whole bridge for the title.

---

## D011 — Visual continuity is the top priority; fix by i2i from the good frame

Date: 2026-08-26
Status: Active

### Decision

When fixing a continuity problem between shots, do NOT independently redesign the scene. i2i from the frame that already has the correct look (identity, clothing, bag, environment, lighting, composition) and change only the specific problem. Use low denoise (0.5) for single-element fixes (tie removal, strap fix) and ~0.6-0.7 for camera/framing changes. For a continuous camera movement (the 07→08→09 aerial ascent), CHAIN the frames (each i2i from the previous) so the sequence reads as one drone shot.

### Reason

Independently regenerating shots breaks character/costume/environment continuity, which breaks MiniMax's ability to blend the frames into a coherent video. The rain effect in the close-ups is good and must be preserved — so close-up fixes i2i from the current close-up frames, not from the face anchor.

### Alternatives considered

- Regenerate from the face/base anchor (rejected — loses the environment/rain continuity)
- High denoise re-rolls (rejected — risks identity/environment drift)

### Result

Continuity fixes applied via targeted i2i: 03 from 04's environment, 05 tie removal (denoise 0.5), 06 both straps (denoise 0.5), 07→08→09 chained aerial ascent.

---

## D012 — Use inpainting for single-element removal that i2i can't fix

Date: 2026-08-26
Status: Active

### Decision

When a low-denoise i2i fails to remove a high-contrast element (e.g. a tie — the model preserves it because it's a strong detail), use INPAINTING: mask just the region to change (collar/tie), and regenerate ONLY that region with denoise 1.0 while the rest of the image stays locked. Workflow: LoadImage (frame) → VAEEncode → SetLatentNoiseMask (mask) → KSampler (denoise 1.0) → VAEDecode. The mask is a grayscale image (white = regenerate) loaded via LoadImage → ImageToMask → GrowMask (expand ~20px, tapered_corners false).

### Reason

A full-image i2i at low denoise keeps the tie because the model preserves high-contrast details. Inpainting isolates the change to the masked region, so the face, bag, environment, and composition are untouched — only the collar/tie area is regenerated.

### Alternatives considered

- Higher-denoise full i2i (rejected — risks identity/environment drift)
- Prompt-only negative (rejected — tie persisted)

### Result

krea2_jaisal_fix05_inpaint.json removes the tie from beat 05 via a collar-region mask. Mask file: jaisal_ss05_tie_mask.png (ellipse over the collar/tie region). NOTE: Krea2 is NOT an inpaint model — the Krea2 inpaint came out distorted. Use the Flux one-node for real inpainting.

---

## D013 — Use the Flux one-node (FluxKleinOneNode) for real inpainting

Date: 2026-08-26
Status: Resolved (manual UI run)

### Decision

For single-element removal that Krea2 can't handle (Krea2 is not an inpaint model — its inpaint output is distorted), use the **Flux one-node** (`FluxKleinOneNode`, "One Node · FLUX.2 [klein]") in PAINT/Inpaint mode.

### Blocker

The one-node is a FRONTEND-DRIVEN UI widget: its `noop` function just returns the JS preview image; generation is triggered from the ComfyUI UI (via `POST /flux_klein/set_output`), NOT through the standard prompt queue — so it CANNOT be driven via `run_workflow`/MCP. It also needs **FLUX.2 [klein] models** (a diffusion model + matching text encoder + VAE) that are NOT installed (local model dirs are empty). The ComfyUI-Inpaint-CropAndStitch dependency IS present.

### Resolution options

- (a) Install FLUX.2 [klein] models (diffusion + text encoder + VAE) into the local model dirs, then drive the one-node from the ComfyUI UI (PAINT → Inpaint: paint the tie region, describe "open collar, no tie").
- (b) User runs the one-node manually in the ComfyUI UI.

### Result

RESOLVED — the user ran the one-node manually in the ComfyUI UI (PAINT/Inpaint) and the tie was removed successfully. Beat 05 is done. The one-node works when driven from the UI; the MCP/prompt-queue path is not available for it.


---

## D014 - MiniMax H3 speed stack: Star7 + Comfy Kitchen INT8 + turbo 4-step LoRA

Date: 2026-08-27
Status: Active

### Decision

For fast MiniMax H3 video on the RTX 5090, use:
- **Star7 pack** (minimax-h3-chunk-star7) node MiniMaxH3ActivationChunkStar7 with attention_backend=comfy_kitchen_int8 (Comfy Kitchen INT8 attention + QKV/RoPE/MLP activation chunking).
- **Turbo 4-step LoRA** minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors (strength 1.0) with BasicScheduler simple/8/1.
- **fl2va model** for first-last-frame shots (drone ascent).
- **RTXVideoSuperResolution** (2x ULTRA) for 2K output; measure at 0.4MP (864x480) first.

### Reason

- triton is MISSING in the embedded Python -> KJNodes PathchSageAttentionKJ crashes (sage path is dead). comfy_kitchen IS installed, so CK INT8 is the working fast attention backend.
- Turbo 4-step halves the sampling steps vs 8-step.
- fl2va natively interpolates between a start and end frame - ideal for the drone-ascent shot.
- 0.4MP keeps the test fast; RTX VSR 2x brings it to ~2K.

### Alternatives considered

- KJNodes SageAttention (needs triton - unavailable).
- Spectrum SpectrumApplyMiniMaxH3 (spectral step-forecasting - installed, but Star7 CK INT8 is the simpler proven fast path; Spectrum kept as fallback).
- H3-Multishot H3MultishotMemorySampler (Joey Gambino long-form sampler - used by v11/v13 seamless templates; good for multi-shot, but single-shot drone ascent is simpler with core MiniMaxH3ReferenceToVideo + fl2va).

### Result

jaisal_drone_optimized.json built and validated (not yet run). All 5 models present in main path.

---

## D015 - Machine-built workflows must use NATIVE widget shape (not /object_info order)

Date: 2026-08-27
Status: Active

### Decision

When building or converting ComfyUI workflow JSON, `widgets_values` arrays MUST match the **native UI-saved shape**, NOT the API `/object_info` widget order. Specifically:
- **KSampler = 7 values** `[seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]` — the hidden `control_after_generate` widget (randomize/fix/+1/-1 dropdown next to seed) is NOT in `/object_info`.
- **LoadImage = 2 values** `[filename, "image"]` — the 2nd literal `"image"` is NOT in `/object_info`.
- **No `widgets_values_named` key** — native UI-saved files don't have it; its presence marks a machine-built file.

### Reason

`/object_info` lists only the "required" widget inputs, which OMITS hidden widgets the UI actually renders. Building `widgets_values` from that order makes the array too short, so the server maps values positionally and they shift one slot left: KSampler `cfg` gets `'euler'`, `sampler_name` gets `'simple'`, `scheduler` gets `0.4` → prompt validation fails ("could not convert string to float", "Value not in list"); LoadImage image not shown; UI shows "no details". This affected ALL 21 machine-built workflows (the 08-27 converted batch + jaisal_drone_optimized).

### Alternatives considered

- Building from `/object_info` order (the original bug — rejected).
- Adding `widgets_values_named` to disambiguate (rejected — native files don't use it; the UI ignores it and it's a machine-built marker).

### Result

`fix_all_widget_shapes.py` applied the native shape to all 21 machine-built workflows (435 changes; backups in `d:\models\vsCodeMcp\workflow_backups\pre_widget_fix\`). All 21 re-validated via MCP (`valid: true`, 0 errors). **Rule for all future workflow building: copy `widgets_values` shapes from a native UI-saved workflow, never from `/object_info`.** See AGENTS.md "CRITICAL: widgets_values must match the server's widget order EXACTLY".

---

## D016 - Machine-built workflows must use `type='COMBO'` + LoadImage `upload` input (not static lists)

Date: 2026-08-27
Status: Active

### Decision

When building/converting workflow JSON, widget-input `type` fields for combo widgets (KSampler `sampler_name`/`scheduler`, LoadImage `image`, CLIPLoader `clip_name`/`type`/`device`, UNETLoader `unet_name`/`weight_dtype`, VAELoader `vae_name`, LoraLoaderModelOnly `lora_name`) MUST be the string `'COMBO'`, NOT a static list of values. And every LoadImage node MUST include the `upload` input (`type='IMAGEUPLOAD'`, `localized_name='choose file to upload'`).

### Reason

A static list dumped into `type` is a stale snapshot — the UI shows it but it doesn't refresh, and (critically) the converter DROPPED the `upload` input, so the LoadImage node had no "choose file to upload" button and no live dropdown. The node still held the correct filename in `widgets_values` (so it "picked up the correct image"), but the user couldn't select/preview a different image in the UI. `type='COMBO'` tells the frontend to populate the dropdown from the server live; the `upload` input renders the file-picker.

### Alternatives considered

- Keeping the static list (rejected — stale, no upload button).
- Only fixing LoadImage (rejected — the same static-list problem affected KSampler/CLIPLoader/UNETLoader/VAELoader/LoraLoaderModelOnly combo inputs too; fixed all in one pass).

### Result

`fix_combo_inputs.py` set 253 static-list inputs to `'COMBO'` and added 37 `upload` inputs across all 21 machine-built workflows (backups in `d:\models\vsCodeMcp\workflow_backups\pre_combo_fix\`). All re-validated via MCP (`valid: true`, 0 errors). **Rule: combo widget inputs use `type='COMBO'`; LoadImage always has both `image` (COMBO) and `upload` (IMAGEUPLOAD) inputs.** See AGENTS.md.

## D017 - MiniMax H3 R2V prompts use the official 6-section reference style

Date: 2026-08-27
Status: Active

### Decision

All MiniMax H3 reference-to-video (R2V) prompts MUST follow the official MiniMax H3 R2V prompting style: reference each input by a tag in **connection order** (`<Picture 1>` = `ref_image_0`, `<Picture 2>` = `ref_image_1`, …), assign each reference an explicit **job** (identity / style / motion / camera / frame anchor), and structure the prompt into the **6 sections** in order: `subject_definitions`, `summary` (with a `[task-type]` prefix like `[reference generation]`), `retention_analysis` (one line per label + a relationship marker), `detailed_description` (350-500 words, partitioned into `[Shot 1]`…`[Shot N] At MM:SS.mmm` with camera angles + actions), `overall_soundscape`, `non_diegetic_music`.

### Reason

The MiniMax H3 R2V model is trained on prompts in this exact structure. Using `<Picture N>` tags in connection order tells the model precisely which reference provides what (identity vs. frame anchor vs. style). Partitioning into timed `[Shot N]` blocks with camera angles gives the model a clear storyboard. A free-form prompt (the old style) under-uses the references and produces weaker shot control. The official guide is saved at `d:\models\vsCodeMcp\docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md` for reuse.

### Alternatives considered

- Free-form prose prompt (rejected — under-uses references, weak shot control).
- Only `<Subject N>` labels without `<Picture N>` frame anchors (rejected — loses the per-shot frame anchoring that R2V is built for).

### Result

`jaisal_lowangle.json` prompt rewritten to this style (5 `<Picture N>` frame anchors, `<Subject 1>` boy / `<Subject 2>` bridge, 5 timed shots, title composited in post). Validated `valid: true`. **Rule: every R2V prompt uses `<Picture N>`/`<Subject N>` tags in connection order + the 6-section structure + timed `[Shot N]` blocks.** See `MINIMAX_H3_R2V_PROMPTING_GUIDE.md`.

## D018 - Multi-ref workflow wiring: set the input `link` field by SLOT INDEX, not name number

Date: 2026-08-27
Status: Active

### Decision

When building a workflow with multiple reference inputs (e.g. `MiniMaxH3ReferenceToVideo` `ref_image_0`…`ref_image_8`), the `link` field on each input in the node's `inputs` array MUST be set to the link ID **by the input's array slot index**, NOT by the number in the input's name. The link's `to_slot` equals the input's position in the `inputs` array, which can differ from the number embedded in the input name.

### Reason

In `jaisal_lowangle.json`, the template had links 289 (LA4→136.6) and 290 (LA5→136.7) but the `MiniMaxH3ReferenceToVideo` node's `inputs` array had `link=None` on `ref_image_3` (slot 6) and `ref_image_4` (slot 7). The UI showed only 3 images wired and validation reported `node_not_reachable_from_output` for LA4/LA5. The bug: the input *name* number (`ref_image_3`→3) differs from the input *slot* position (index 6/7). Setting `link` by name number looked for a link targeting slot 3/4 (which don't exist for these inputs); setting it by actual array index (6/7) matched the real links.

### Alternatives considered

- Setting `link` by the name number (rejected — wrong slot, no match).
- Only creating the link without setting the input `link` field (rejected — UI shows no connection, validation flags unreachable).

### Result

`fix_lowangle_wiring_and_prompt.py` set `ref_image_3.link=289` and `ref_image_4.link=290` by slot index. All 5 images now wired; validation `valid: true`, 0 warnings. **Rule: when wiring multi-ref inputs, set each input's `link` field to the link ID whose `to_slot` equals that input's array index.**

## D019 - Subgraph templates: set widget values on INTERNAL nodes, not the instance

Date: 2026-08-28
Status: Active

### Decision

When a gallery template wraps its main node in a **subgraph** (the instance node's `type` is a UUID, e.g. `4c314f31-ecda-4b08-ae98-faaba1bf613f`), widget values (prompt, duration, turbo, LoRA, etc.) MUST be set on the **internal nodes** under `definitions.subgraphs[0].nodes`, NOT on the instance node's `widgets_values`. The instance node's `widgets_values_named` dict is also preferred over `widgets_values` by the UI→API converter, so update both.

### Reason

The `video_minimax_h3_i2v` template's `MiniMaxH3ImageToVideo` node (instance id=105) is a subgraph. Editing the instance's `widgets_values[10]` (LoRA) had NO effect — the converter read the LoRA from the internal `LoraLoaderModelOnly` node (id=121), which still held the template default `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` (not installed) → validation error `node 105/121: lora_name not in options`. The `105/121` notation = instance 105, internal node 121. Setting `lora_name` on internal node 121 (both `widgets_values[0]` and `widgets_values_named['lora_name']`) to the installed `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors` fixed it.

### Alternatives considered

- Editing only the instance `widgets_values` (rejected — ignored by the converter for subgraph nodes).
- Downloading the 8-step LoRA (rejected — we already have the 4-step 768p version, which is faster and proven on the drone workflow).

### Result

`jaisal_single_shot.json` validates `valid: true`, 0 errors. **Rule: for subgraph templates, locate the internal node and set its `widgets_values` + `widgets_values_named`; also update the instance's `widgets_values_named`.** Related: the `ResolutionSelector` aspect enum is `16:9 (Widescreen)` (the template's own `Widescreeen` spelling fails validation). See AGENTS.md.

## D020 - R2V: use 2-3 reference images max with a SIMPLE prompt (not 5 + 500 words)

Date: 2026-08-28
Status: Active

### Decision

For MiniMax H3 reference-to-video, use **2-3 reference images max**, each mapped 1-to-1 to a shot with an explicit "the first frame of [Shot N]" anchor, and a **short** prompt. Do NOT use 5 images + a 500-word 6-section essay.

### Reason

The 5-image `jaisal_lowangle.json` (5 `<Picture N>` tags + 500-word prompt) came out bad: style drift, the boy not running, and the model confused by the ref→shot mapping (it couldn't cleanly map `ref_image_0`→`<Picture 1>`→[Shot 1] across 5 anchors). The single-shot i2v alternative also came out bad (cartoon style, weak motion). The fix: **2 images** (`1.png` = boy at start of bridge → [Shot 1], `2.png` = boy in middle of bridge → [Shot 2]) with a simple prompt where each `<Picture N>` is explicitly "the first frame of [Shot N]". The model animates between 2 clear anchors far better than it follows a 5-anchor storyboard.

### Alternatives considered

- 5-image R2V (rejected — style drift, no running, confused mapping).
- Single-shot i2v (rejected — cartoon style, weak motion).
- 3-image R2V (fallback — add a 3rd reference showing the running pose if 2 images don't produce the run).

### Result

`jaisal_lowangle.json` rebuilt as 2-image via `build_2ref.py` (deleted LoadImage 143/LA4/LA5 + links 285/289/290, cleared `ref_image_2/3/4` link fields, simple 2-anchor prompt, save prefix `video/Jaisal_2Ref_1_2`). Validated `valid: true`, 0 errors. **Rule: 2-3 refs max, each an explicit frame anchor, simple prompt. If the character isn't doing the action, add a 3rd reference showing that pose or strengthen the motion verb.** See AGENTS.md.

## D021 - Hold the Krea2 style in MiniMax video via a Krea2-styled REFERENCE SET (not frame-by-frame)

Date: 2026-08-28
Status: Active

### Decision

To keep the Krea2 angular brush-stroke style across a WHOLE MiniMax H3 video (not just the first 2-3s), **generate a set of Krea2-styled reference images first** (character sheet, abstract, bridge, medium, close-up, water, running — all faceless character, rose shirt/black pant/black bag) and feed 2-3 of them as references to the MiniMax R2V workflow. Do NOT use a frame-by-frame Krea2 style-transfer pipeline (extra work).

### Reason

MiniMax H3 is a general video model — its prior smooths toward its own default look, so the Krea2 style "completely went" in the video. The turbo LoRA is a *speed* distillation, not a *style* LoRA. Reference images only anchor the first frame, so drift creeps in over 15s. A frame-by-frame Krea2 i2i pipeline would guarantee the style but is extra work (extract frames → batch i2i → reassemble). The cleaner path: create a proper Krea2-styled reference set upfront and feed it to MiniMax so it holds the style across the whole video.

### Alternatives considered

- Frame-by-frame Krea2 style transfer (rejected — extra work; user: "creating a video and snapping is extra work, let's create the images properly").
- Stronger style description in the prompt only (insufficient — text can't fully carry the style).
- Training a MiniMax H3 style LoRA (best long-term, but heavy — needs training infra; keep as a future option).

### Result

`krea2_jaisal_refs.json` (Krea2 t2i generator, validated) + `jaisal_ref_prompts.txt` (7 faceless-character prompts). **Rule: for style-consistent video, build a Krea2-styled reference set first and feed 2-3 of it to MiniMax.** See AGENTS.md.

## D022 - The Jaisal Cut character is FACELESS (head + hair only) with rose shirt / black pant / black bag

Date: 2026-08-28
Status: Active

### Decision

The Jaisal Cut character is a **normal young schoolboy with short dark hair** (face OK — see correction below). Costume: **rose-pink collared shirt, full-length black trousers, black school bag** (replacing the old red bag / school-uniform look). Every prompt must emphasize **ONLY ONE character, no duplicates** (Krea2 tends to duplicate the character).

### Reason

The user originally requested a faceless figure ("a head and hair, no nose, no face, no eyebrow, no mouth") because faces are the hardest thing to keep consistent in video. **Correction (2026-08-28): Krea2 CANNOT make a faceless character — it always renders a face.** The user accepted this: "krea 2 doesnt create faceless, but thats fine we are good with 1 character sheet." So the character is a normal boy with short dark hair + the new costume.

### Alternatives considered

- Faceless figure (rejected — Krea2 can't do it; it always renders a face).
- Keeping the red bag / school uniform (rejected — user changed the costume to rose shirt / black pant / black bag).

### Result

All reference images (`jaisal_ref_prompts.txt`) use the normal-face boy + new costume + "ONLY ONE character" emphasis. The bridge prompt pins the boy **ON THE BRIDGE DECK (left side), NOT in the water** (Krea2 had put him in the river). The MiniMax prompt (v2) still says "red school bag" — **update it to "black school bag"** when re-running MiniMax with the new references. **Rule: the Jaisal Cut character is a normal boy (short dark hair), rose-pink collared shirt, black trousers, black school bag, always a SINGLE character.**

## D023 - Face consistency via Krea2 Identity Edit v1.2 workflow (not t2i re-rolls)

Date: 2026-08-29
Status: Active

### Decision

To keep the SAME face across all Jaisal Cut reference images, use the **Krea2 Identity Edit v1.2** workflow (`krea2_identity_edit.json`, LoRA `krea2_identity_edit_v1_2.safetensors`, `comfyui-krea2edit` node pack — both already installed). Load a good reference (character sheet / clean close-up) in the LoadImage node, write a plain-English instruction for the new scene, and it regenerates the scene keeping the same face/identity. `ref_boost` = 4.0 (recommended fidelity), KSampler 10 steps cfg 1, `grounding_px` 384-768, 1MP output.

### Reason

Krea2 t2i gives a DIFFERENT face every time the character appears ("literally a different guy" across the reference set). The identity-edit model treats the reference image like a LoRA — much stronger face+body likeness than re-rolling t2i seeds. User found the workflow on reddit; it's the right tool for a production character.

### Alternatives considered

- Re-rolling t2i seeds until the face matches (rejected — unreliable, the face drifts every generation).
- Training a character LoRA (rejected — heavy; identity-edit is ready now).

### Result

`krea2_identity_edit.json` validates `valid: true` (1 expected warning: optional 2nd-image group ships bypassed). **Rule: for consistent-character reference sets, generate the base image with t2i, then lock the face with the identity-edit workflow (ref_boost 4).**

## D024 - Climate consistency: one moody tone once rain starts (no drastic changes)

Date: 2026-08-29
Status: Active

### Decision

Do NOT change the climate dramatically between shots. Once the rain starts, keep ONE moody tone across all rain/water shots (medium, close-up, water, running). The underwater shot must be DARK and moody (matching the rain), NOT bright/sunny.

### Reason

The generated water reference came out bright with a canal/bund look while the rest of the set was moody — a drastic light change between shots breaks continuity, and MiniMax won't bridge a hard climate jump between references.

### Result

Prompts 4-7 in `jaisal_ref_prompts.txt` updated: square handrails (not round/ornate/staircase), open river (not canal/bund), dark moody water (not bright), three-quarter view (not facing camera). **Rule: one moody tone from the first rain onward; no bright/sunny shots after rain starts.**

---

## D025 - Identity workflow: wire the STYLE LoRA in to match skin tone / lighting

Date: 2026-08-29
Status: Active

### Decision

Add the **style LoRA `Krea2_Cinematic_Artstyle.safetensors` @ 0.7** to the Krea2 Identity Edit v1.2 workflow (`krea2_identity_edit.json`) as a new node **95** between the identity LoRA (71) and the `Krea2EditModelPatch` (79). Chain: `55 UNETLoader → 71 identity LoRA → 95 style LoRA → 79 patch → 53 KSampler`.

### Reason

The identity workflow carries the **reference image's color tone** into the output. A neutral/bright character-sheet reference makes the boy come out studio-lit, clashing with the dark moody rainy scene (skin tone mismatch). The style LoRA pulls the output back into the angular brush-stroke style AND the moody palette of the scene.

### Alternatives considered

- Relying on the instruction's lighting words alone (helps but doesn't fully fix the reference's color tone).
- Using a reference that is already in the moody scene (best — then the tone matches automatically).

### Result

Style LoRA wired in + validated `valid: true`. **Tuning:** style too weak → raise node 95 to 0.8-1.0; face distorts → lower to 0.5. **Also:** keep the lighting words in the instruction ("moody overcast light"); if skin still too bright add "skin tone matching the dark moody overcast light, dim diffused light on the face, NOT studio lit". **Best:** use a reference already in the moody scene instead of the neutral character sheet. Backup: `krea2_identity_edit.json.pre_stylelora.bak`.

---

## D026 - Title card "The Jaisal Cut" via Krea2 i2i + Typnosis typography LoRA

Date: 2026-08-30
Status: Active

### Decision

Generate the title card with a dedicated Krea2 **i2i** workflow `krea2_jaisal_title.json`: load the underwater shot (`refs_water.png`), keep the SAME underwater scene, and swap the boy for the title **"The Jaisal Cut"** using the **Typnosis_Krea2** typography LoRA (verified: "Typnosis v2 triggerless Krea 2 Raw typography/domain LoRA") chained after the Cinematic style LoRA. Chain: `UNET krea2_turbo_fp8_scaled → Cinematic LoRA @1.0 → Typnosis LoRA @1.0 → KSampler (8 steps cfg 1, denoise 0.55)`.

### Reason

The underwater shot has generous negative space for a title. An i2i (low-moderate denoise) keeps the scene consistent while the typography LoRA renders the title text. Verified we already have Krea2 i2i workflows (`krea2_jaisal_title_moody.json` etc.), so this reuses the proven i2i pattern.

### Alternatives considered

- Compositing the title in post (Photoshop) — works but the user wanted it generated in ComfyUI with the typography LoRA.
- t2i from scratch — would lose the consistent underwater scene.

### Result

`krea2_jaisal_title.json` built + validated `valid: true`. Prompt (prompt 10 in `jaisal_ref_prompts.txt`) keeps the underwater scene + swaps the boy for the title. **Tuning:** title garbled → lower denoise to 0.4; boy still there → raise denoise to 0.65-0.7.

### Update 2026-08-30 (STR5 + bubble-formed title)

User tested the title card and **STR5 (strength 5.0) on the Typnosis LoRA reads best** for the title (per the Typnosis author notes: STR1-STR2 is most prompt-faithful, STR4+ gets more stylized and compositions converge — STR5 is the balanced-strong sweet spot). Set node 32 `strength_model` = **5.0**. User also asked for **bubbles**: the title is now **formed ENTIRELY from clusters of rising air bubbles** (each letter built from many small/medium bubbles glowing against the dark water) with **additional bubbles drifting around the title** — fits the underwater scene. Prompt 10 positive updated accordingly. **Tuning:** STR5 over-stylizes/distorts letters → drop to 3.0-4.0; bubbles too sparse → strengthen the bubble wording ("DENSE clusters of many small bubbles") or nudge the LoRA up.

### Update 2026-08-30 (wavy floating layout)

User asked for a **wavy type** since the bubbles are in water — the words should **float a little**: not too adjacent (spaced apart with generous gaps), letters can be **different sizes/shapes**, but the whole **"The Jaisal Cut"** must stay clearly readable. Prompt 10 positive now adds: "the letters and words arranged in a gentle WAVY floating layout, each word drifting at a slightly different height as if floating in the water, the words spaced apart with generous gaps between them (NOT cramped, NOT adjacent), the individual letters varying slightly in size and shape for an organic floating feel, the whole title 'The Jaisal Cut' clearly readable and centered". **Tuning:** words too flat/straight → strengthen the wavy wording ("each word drifting at a clearly different height, a gentle S-curve"); words too scattered / title stops reading as one line → soften it ("a SUBTLE gentle wave, words only slightly offset, kept close enough to read as one title").

### Update 2026-08-30 (CPU RAM exhaustion on the 7-ref MiniMax run — CORRECTED diagnosis)

The 7-shot `jaisal_lowangle.json` run failed with `numpy._core._exceptions._ArrayMemoryError: Unable to allocate 24.0 MiB for an array with shape (1088, 1928, 3) float32` at `nodes_minimax_h3.py:229 _resize`. **This is a CPU RAM exhaustion, NOT a VRAM problem and NOT a workflow bug.**

**CORRECTED (2026-08-30, after measuring with `top_ram.py`):** my first claim — "the 7 Krea2 runs left ~17 GB of Krea2 models resident in CPU RAM" — was **WRONG / unverified**. Measured reality: ComfyUI's `python.exe` was only **1.37 GB**. The dominant RAM consumer is the **local Qwen `llama-server.exe` at ~19-22 GB** (a SEPARATE process ComfyUI cannot touch). The system was at **95% load / 2.7 GB free**, so even a 24 MB CPU allocation failed. The process list accounted for ~36 GB; the rest of the 66 GB was page file / memory compression / transient allocations. **The real pressure source is the Qwen llama-server, not ComfyUI's models.**

**FIX APPLIED (user):** removed `--lowvram` from the ComfyUI launch script (now: `--windows-standalone-build --reserve-vram 4 --disable-pinned-memory --use-pytorch-cross-attention --cache-none --enable-manager`). Without `--lowvram`, ComfyUI keeps its models in **VRAM** (32 GB free) instead of offloading to CPU RAM, so it no longer competes with the Qwen llama-server for CPU RAM. After restart: system at **66% load / 22.4 GB free**, llama-server 22.3 GB, ComfyUI 1.37 GB. **The MiniMax 7-ref resize (24 MB float32 per image on CPU) now trivially succeeds.**

**Rule: the dominant CPU-RAM consumer is the local Qwen llama-server (~22 GB), NOT ComfyUI. Run ComfyUI WITHOUT `--lowvram` so its models stay in VRAM (32 GB free) and don't compete with Qwen for CPU RAM. If a heavy run still OOMs, the constraint is the llama-server's footprint — reduce its context/concurrency, not ComfyUI's. VERIFY RAM consumers with `top_ram.py` before diagnosing — do NOT assume which process is holding the RAM.**

### Update 2026-08-30 (Pipeline 1 — 2K render VRAM-thrashed → set to 1MP native; render-time baseline)

User: "I think we should have went with 1MP. [log: Model Initializing ... 0/8 [10:15<?, ?it/s] ... Prompt executed in 00:11:31] I had to stop this. Can you check the forums how much time it will take to render a 15 second 2mp REF2 on RTX 5090?"

**Diagnosis (from the user's own log, not forums):** the 2K render **never started sampling** — it was stuck at **0/8 steps, "Model Initializing", for 10+ minutes**. That is NOT slow sampling; it is the **~20 GB model (`19995MB Staged`) + 2K video activations thrashing in VRAM** (32 GB card, `--reserve-vram 4`). At 2048×1152 the video latent + activations are so large ComfyUI spends all its time moving the model in/out of VRAM instead of generating. It likely would not have finished in reasonable time.

**Render-time baseline (from the user's OWN machine, not forums):** the 11 `Jaisal_Production_1` outputs were written ~10–15 min apart (04:31 → 04:45 → 04:55 → 05:10 → 05:23), so **~10–15 min per 0.4 MP render** is the real baseline. Video cost scales with pixels × frames × steps:
- 0.4 MP (864×480): ~10–15 min (measured)
- **1.0 MP (1344×768, native): ~25–40 min**
- 2.4 MP (2048×1152, 2K): ~60–90 min AND VRAM-thrashing (what the user just hit)

The reference video barely adds compute (it's a conditioning input, not a big cost) — the cost is **output resolution × 15s × 8 steps**.

**Decision: set the `ResolutionSelector` (node 115) to `['16:9 (Widescreen)', 1.0, 32]` → 1344×768 (MiniMax H3 NATIVE canvas).** 1MP is what the model is designed for, fits comfortably in VRAM, and renders in a finite ~25–40 min. For 2K, the clean path is **render at 1MP → upscale** (Topaz/RTX/Hunyuan upscalers are all installed) — faster and cleaner than a direct 2K render. The reference video node (149) stays wired as the motion anchor.

**Rule: do NOT render MiniMax H3 at 2K directly on a 32 GB card — the ~20 GB model + 2K activations thrash VRAM (stuck at 0/8 steps in "Model Initializing"). Render at the NATIVE 1344×768 (1.0 MP) and upscale to 2K in a separate step. Estimate render time from the user's OWN output timestamps (file mtimes), not forums — forums rarely have a clean per-GPU benchmark. A render stuck at 0/8 steps in "Model Initializing" for many minutes = VRAM thrashing, not slow sampling.**

### Update 2026-08-30 (Pipeline 1 — added reference VIDEO (motion anchor) + 2K resolution)

User: "I got one output, and I'm okay with it. Can I add it as a reference and render it in 2K so that it follows the same action?" (referring to `Jaisal_Production_1_00011_.mp4`, the most recent good output).

Updated `jaisalproduction1.json` (validated `valid: true`, now 23 nodes):
- **Added a `MiniMaxH3ReferenceVideoLoadStar7` node (id 149)** that loads the good output video as a MOTION anchor. The node scans the `input` dir, so the video was copied to `input\jaisal_prod1_ref.mp4` (from `output\video\Jaisal_Production_1_00011_.mp4`).
- **Wired:** node 149 IMAGE output (slot 0) → link 303 → node 136 `ref_videos.ref_video_0` (slot 9); node 149 AUDIO output (slot 1) → link 304 → node 136 `ref_video_audios.ref_video_audio_0` (slot 10). The 3 reference IMAGES stay (visual anchors); the video adds the motion/action anchor so the new render follows the same action.
- **Set 2K:** the `ResolutionSelector` (node 115) was `['16:9 (Widescreen)', 0.4, 32]` (≈864×480). Set to `['16:9 (Widescreen)', 2.4, 32]` → **~2048×1152 (2K)**. The middle widget is MEGAPIXELS (1.0 ≈ 1024×1024); 2.4 MP @ 16:9 = 2048×1152. The MiniMax node width/height accept up to 16384 (step 32), so 2K is valid.
- **`MiniMaxH3ReferenceVideoLoadStar7` widgets:** `[video, max_long_edge, allow_upscale]` = `['jaisal_prod1_ref.mp4', 1344, False]`. `max_long_edge` (default 1344) = the H3-aligned long edge the ref video is fitted to (keeps aspect). `allow_upscale` = False (avoids spending H3 reference tokens on interpolated detail; enable only for structure/motion A/B tests).

**Rule: to make a new MiniMax R2V render FOLLOW THE SAME ACTION as a good output, add a `MiniMaxH3ReferenceVideoLoadStar7` node that loads that output video and wire its IMAGE output to `ref_videos.ref_video_0` (+ AUDIO to `ref_video_audios.ref_video_audio_0`). The node scans the `input` dir, so copy the video there first. The reference images stay as visual anchors; the video is the motion anchor. For 2K, set the `ResolutionSelector` megapixels widget to ~2.4 (16:9 → 2048×1152). A 2K render is ~6× the pixels of the 0.4 MP default, so it's much slower + more VRAM — run it when the machine is free (the Qwen llama-server holds ~22 GB CPU RAM).**

### Update 2026-08-30 (Pipeline 1 prompt v10 — Shot 1 WIDE ANGLE + Shot 3 climbs then jumps (no hand gestures))

User reviewed Pipeline 1 v9: "(1) the first shot is literally NOT a wide angle shot - it went back to a different structure. (2) the 2nd one is stable. (3) the 3rd one is not good - I think it's because we said he is doing hand gestures, it confused [the model]. Let's remove that. He is SLOWLY LIFTING HIS LEG and CLIMBING and then JUMPING. That's it. But there should NOT be a static shot. Let's tweak the prompt a little more and I will try again."

User's inline edits in the pasted prompt (folded into v10):
- Shot 1: "we should not have any extra characters apart from the first character which is standing on the LEFT side of the bridge, only that character has to run" + "NOT an Extra Character" in the gait line.
- Shot 3: "he is not repeating the movement, he breathes in after the run" + "LEAPS over the low handrail SLOWLY".
- New `overall_landscape` section: "we should see VISIBLE RAINFALL, after the first picture throughout the sequence".

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Shot 1 = WIDE ANGLE:** "a WIDE ANGLE establishing shot - the camera is positioned FAR AWAY, showing the boy as a small figure on the bridge with the full landscape, sky, and river visible. This is a WIDE ANGLE view (NOT a medium shot, NOT a close-up)." + "ONLY ONE boy <Subject 1> is on the bridge, standing on the LEFT side of the bridge - there are NO other people, NO second boy, NO duplicates, NO extra characters. Only that ONE boy runs."
- **Shot 2:** UNCHANGED (user: "the 2nd one is stable").
- **Shot 3 = climbs then jumps (NO hand gestures):** "The boy is NOT standing still - he is SLOWLY LIFTING HIS LEG and CLIMBING over the low handrail, then JUMPING. He is not repeating the movement - he breathes in after the run." Then "LEAPS over the low handrail SLOWLY - his body fully airborne." (Removed the v9 "shakes his head, makes hand gestures" which confused the model.)
- **`<Picture 3>` definition** kept: "preparing to jump over the handrail".
- **summary** updated: "then climbs over the handrail and leaps" (was "then prepares and leaps").
- **overall_soundscape** updated: "a rising tension as the boy climbs and leaps" (was "prepares and leaps").
- **New `overall_landscape` section:** "We should see VISIBLE RAINFALL throughout the sequence after the first picture - rain is clearly falling and visible in [Shot 2] and [Shot 3]."
- RAIN still enforced in every shot. Timing still 4/6/5 (00:00.000 / 00:04.000 / 00:10.000).

**Rule: when a shot comes out NOT wide-angle, say "WIDE ANGLE establishing shot - the camera is positioned FAR AWAY, showing the boy as a small figure with the full landscape/sky/river visible (NOT a medium shot, NOT a close-up)" - the word "wide" alone is not enough, you need to describe the camera being FAR AWAY + the boy being a SMALL FIGURE. When a "preparing" action (head shake, hand gestures) confuses the model, REPLACE it with a concrete physical action that leads into the main action (SLOWLY LIFTING HIS LEG and CLIMBING over the handrail, then JUMPING) - a clear physical chain is less confusing than vague gestures. And to keep a shot from being static, say "he is NOT standing still - he is [concrete action]" + "he is not repeating the movement, he breathes in after the run" (a breath beat between actions prevents a frozen frame without adding confusing gestures).**

### Update 2026-08-30 (Pipeline 1 prompt v9 — Shot 3 PREPARES while camera moves, then leaps)

User reviewed Pipeline 1 v8: "the 3rd shot was working fine 3 prompts ago (v5), we need those camera moves, but we have to mention that the 3rd one is NOT a static frame - when it loads he has to do some action, like shaking head or some hand gestures while the camera is moving, and then he can jump, so while the camera is moving he can prepare also, so that feels more natural. The rule should be: where he is moving and what he is doing - we don't want him to run back and forth. Explain it cleanly. I want to get it done, it's been 8 hours."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Shot 3 camera moves RESTORED to v5** (the user said v5's shot 3 was working fine): SIDE view from the VIEWER'S LEFT, boy on viewer's left, camera ANCHORED on viewer's left + TRACKS him (NOT a left-to-right sweep), swings to his BACK as he leaps, ENDS at his back mid-air BEFORE the water.
- **Shot 3 is NOT a static frame:** "The boy is NOT standing still - while the camera moves, he is PREPARING to jump: he shakes his head, makes hand gestures, and gets ready. Then the boy LEAPS over the low handrail." (This replaces v8's "ALREADY RUNNING and IN MOTION at the start" which was over-constraining and breaking the shot.)
- **<Picture 3> definition** updated: "the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, **preparing to jump over the handrail**" (was "already running toward the handrail").
- **summary** updated: "then prepares and leaps over the handrail" (was "then runs toward the handrail and leaps over it").
- **overall_soundscape** updated: "a rising tension as the boy prepares and leaps" (was "runs and leaps").
- **CLEAN RULE (user's):** state WHERE the boy is moving and WHAT he is doing - do NOT have him run back and forth. Shot 3: he is at the middle of the bridge, facing the handrail (toward the river), PREPARING (shaking head, hand gestures) while the camera moves, then LEAPS. One direction, one action, no back-and-forth.
- RAIN still enforced in every shot (unchanged). Timing still 4/6/5 (00:00.000 / 00:04.000 / 00:10.000).

**Rule: when a shot keeps breaking under over-constraint, GO BACK to the last version that worked (v5's shot 3 camera moves) and add ONLY the one missing element (the boy is NOT static - he PREPARES: shakes head, hand gestures, while the camera moves, then leaps). The rule for describing motion is: state WHERE the subject is and WHAT he is doing in ONE direction - do NOT have him run back and forth. A "preparing" action (head shake, hand gestures) while the camera moves feels more natural than a static frame AND is less likely to break than a full run→crouch→plant→leap chain.**

### Update 2026-08-30 (Pipeline 1 prompt v8 — timing 4/6/5 + Shot 3 starts IN MOTION)

User reviewed Pipeline 1 v7: "(1) [Shot 1] should have 4 seconds, (2) [Shot 2] we can extend till 10 where we have proper direction, (3) [Shot 3] the same issue came back - the starting frame is standing still, we should not do that."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Timing:** [Shot 1] = **4s** (00:00.000), [Shot 2] = **6s** (00:04.000 → 00:10.000, "proper direction" = the turn is clear and deliberate, body rotates fully toward the VIEWER'S LEFT), [Shot 3] = **5s** (00:10.000). Total = 15s (length node 132 stays 15).
- **Shot 3 starts IN MOTION:** "The boy is ALREADY RUNNING and IN MOTION at the start of this shot - he is NOT standing still, he is moving toward the handrail with momentum." Then he runs toward the handrail, crouches, plants, and LEAPS. (The v7 issue: the starting frame was standing still.)
- **<Picture 3> definition** updated: "the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, **already running toward the handrail**" (was "about to climb over the handrail and leap").
- **summary** updated: "then runs toward the handrail and leaps over it" (was "then climbs over the handrail and JUMPS").
- **overall_soundscape** updated: "a rising tension as the boy runs and leaps" (was "climbs and leaps").
- RAIN still enforced in every shot (unchanged from v7).

**Rule: when a shot's STARTING FRAME comes out standing still, say explicitly "the boy is ALREADY RUNNING and IN MOTION at the start of this shot - he is NOT standing still" AND update the <Picture N> definition to describe the in-motion pose ("already running toward the handrail") - the reference frame anchor + the explicit in-motion line together prevent a static opening. And when the user gives a timing split (4/6/5), set the [Shot N] timestamps to match (00:00.000 / 00:04.000 / 00:10.000) and keep the length node = the total (15s).**

### Update 2026-08-30 (Pipeline 1 prompt v7 — SIMPLIFIED + RAIN enforced in every shot + Shot 3 ends mid-air)

User reviewed Pipeline 1 v6: "the first clip had a lot of issues, the hard rule didn't apply well, check out the H3 prompt guide, let's clear out the confusion and keep it simple. (1) Shot 1 should focus on the CLIMATE and MOOD, the kid is WALKING / SLOWLY RUNNING. (2) Shot 2 is fine. (3) Shot 3 is fine BUT we do NOT want to show the kid jumping TO the water - the jump and the cut should happen AFTER the jump, we don't need to show till he reaches the water, and the bridge has HEIGHT - do not treat this as a swimming pool. (4) IMPORTANT: none of them has RAIN in it - we should enforce MiniMax to add RAINING."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **SIMPLIFIED** the whole prompt (removed the heavy CHARACTER COUNT block + the over-stuffed negative constraints that "didn't apply well"). Kept the 6-section structure per the H3 guide. Kept the ORIENTATION block (boy's right = viewer's left).
- **Shot 1:** now focuses on the CLIMATE and MOOD - the boy WALKS and SLOWLY RUNS (natural gait, feet lift+land separately, NOT a slide), MAIN PURPOSE = ESTABLISH THE CLIMATE AND MOOD (sky clear→moody, RAIN BEGINS TO FALL and builds, landscape shifting). Fixed wide static camera.
- **Shot 2:** UNCHANGED (user: "the second one is fine").
- **Shot 3:** the boy crouches → plants → LEAPS over the handrail, fully airborne. **The bridge is TALL - a real leap from height over the wide river, NOT a shallow pool.** The shot ENDS with the camera at his BACK as he is in the air, **BEFORE he reaches the water** - the cut happens right here so the next clip picks up the jump. (Removed the "DIVE into the river / SPLASH" - we do NOT show him reaching the water.)
- **RAIN enforced in EVERY shot:** "RAIN is present in EVERY shot - rain is falling in [Shot 1], [Shot 2], and [Shot 3]" (detailed_description global line) + "RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3])" (overall_soundscape). Shot 1 = rain BEGINS and builds; Shot 2 = rain streaks visible; Shot 3 = HEAVY RAIN.

**Rule: when a hard rule "doesn't apply well", SIMPLIFY - over-stuffed negative constraints (a whole CHARACTER COUNT block + many NOT-clauses) dilute the signal. Keep the 6-section structure, state the key requirement once clearly per shot, and ENFORCE the global element (RAIN) in BOTH the detailed_description global line AND the overall_soundscape so MiniMax can't drop it. For a jump that must NOT show the landing: end the shot mid-air BEFORE the water and say the bridge is TALL (a real leap from height, NOT a shallow pool) - the cut happens at the apex so the next clip picks up the jump.**

### Update 2026-08-30 (Pipeline 1 prompt v6 — ONLY ONE character + Shot 3 JUMP made explicit)

User reviewed Pipeline 1 v5: (1) **Shot 1 had 2 characters** — MiniMax duplicated the boy; need a HARD demand that there is ONLY ONE character. (2) **Shot 2 is fine** — keep as is. (3) **Shot 3 is fine on camera angle but the JUMP didn't happen** — the boy climbed but never actually jumped; need more detail so it speeds up and the leap actually occurs.

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Added a CHARACTER COUNT block** (new section): "There is ONLY ONE character in the entire video - the single young schoolboy <Subject 1>. There are NO other people, NO second boy, NO duplicates, NO extra figures, NO crowds, NO bystanders, NO reflections of a second person. Every shot shows exactly ONE boy and only that boy." Also added to summary, retention_analysis ("ALWAYS exactly ONE boy - never two, never a duplicate"), the detailed_description global line, and the [Shot 1] line ("ONLY ONE boy ... NO second person, NO duplicate, NO other figure anywhere in the frame").
- **Shot 2 UNCHANGED** (user: "second one is fine").
- **Shot 3 JUMP made explicit + sped up:** the boy "moves QUICKLY and with PURPOSE - he crouches, plants his feet, and then JUMPS: he LEAPS over the low handrail and DIVES into the river, his body fully airborne, arms out, a clear dynamic leap (NOT just climbing, NOT just standing, NOT just walking - he MUST actually JUMP and go over the handrail into the water)." Camera angle kept correct (SIDE view from viewer's left, anchored + tracks, swings to his back). summary + detailed_description now say "[Shot 3] MUST show the boy JUMPING into the river".
- **Sound:** added "a big SPLASH as he JUMPS into the river" to overall_soundscape.

**Rule: MiniMax DUPLICATES the character (a 2nd boy) unless you HARD-DEMAND "ONLY ONE character, no duplicates, no second figure" in a dedicated block + summary + retention + the wide-shot line (the wide shot is where a duplicate is most visible). And a JUMP/leap will NOT happen from a vague "climbs and leaps" — you must spell out the physical action (crouch → plant → LEAP over the handrail → DIVE into the water, fully airborne) and forbid the failure modes ("NOT just climbing, NOT just standing, NOT just walking"). If the action still doesn't happen, add a reference frame that already shows the airborne pose.**

### Update 2026-08-30 (Pipeline 1 prompt v5 — left/right orientation fix + sound + sliding)

User reviewed Pipeline 1 v4: (1) **Sound is bad in the first sequence** — needs to clearly convey **running footsteps + a building thunderstorm** (thunder rumbles, heavy rain). (2) **The left/right was wrong** — "when I say he is moving right I meant HIS right (the VIEWER'S LEFT), and that's how our 3rd portion starts." (3) **Shot 3 camera angle is confusing** — it was sweeping **left-to-right**; the user wants it **anchored on the VIEWER'S LEFT** (where the boy is after turning), tracking him, NOT sweeping across.

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Added an ORIENTATION block** (new section after subject_definitions): "The boy's RIGHT side is the VIEWER'S LEFT side of the frame. When the boy turns toward his right, he turns toward the VIEWER'S LEFT. [Shot 3] is a side view from the VIEWER'S LEFT side, and the boy is on the VIEWER'S LEFT of the frame." + "All left/right references use the VIEWER's perspective" in the detailed_description global line.
- **Shot 2:** the boy turns toward **HIS RIGHT = the VIEWER'S LEFT** (toward the river).
- **Shot 3:** now a **SIDE view from the VIEWER'S LEFT**, boy on the VIEWER'S LEFT of the frame; the camera is **anchored on the VIEWER'S LEFT and TRACKS the boy (does NOT sweep left-to-right)** as he climbs, then swings to his BACK as he jumps.
- **Shot 1 sliding:** even more forceful — "a REAL running gait - each foot clearly LIFTS and LANDS separately, visible leg movement, one step at a time (NOT a smooth slide, NOT a glide, NOT a blur, NOT a keyframe slide, NOT fast)".
- **Sound (overall_soundscape):** "Clear running footsteps on the stone bridge, heavy rain, a building thunderstorm with distant thunder rumbles, splashing water on the bridge stones, then a rising tension as the boy climbs and leaps."

**Rule: ALWAYS specify left/right from the VIEWER's perspective in R2V prompts (the boy's right = the viewer's left) — ambiguous "his right" makes MiniMax pick the wrong side. Anchor the camera to a fixed side (the viewer's left) and say it TRACKS the subject rather than "moves across" (which reads as a left-to-right sweep). And name the exact sounds you want (running footsteps + thunderstorm rumbles) in overall_soundscape — a vague "wind building" gives muddy audio.**

### Update 2026-08-30 (Pipeline 1 prompt v4 — wide shot as a HARD demand + slow run + climate change)

User: "make sure the wide shot is also a hard demand and the kid has to slowly run, but that shot should establish the climate change." Updated `jaisalproduction1.json` node 138 (validated `valid: true`): (1) the **wide shot is now a HARD REQUIREMENT** — added to the summary ("[Shot 1] MUST be a LONG WIDE establishing shot that shows the landscape and the climate change") and the detailed_description global line ("[Shot 1] MUST be a LONG WIDE establishing shot (a hard requirement - it must NOT be cut short, NOT turned into a close-up, NOT skipped)"), and the Shot 1 line itself ("a HARD REQUIREMENT - the camera does NOT move closer, does NOT push in, does NOT cut to a close-up - it stays a FIXED wide view the whole time"). (2) **Slow running** reinforced: "runs SLOWLY and DELIBERATELY... (NOT rushing, NOT sliding, NOT a blur, NOT fast)". (3) **Climate change is the shot's MAIN PURPOSE**: "The MAIN PURPOSE of this shot is to ESTABLISH THE CLIMATE CHANGE - the sky gradually darkens from clear to moody overcast, the wind picks up, and rain begins to fall, the whole landscape and environment shifting from clear to rainy." **Rule: when a shot has a specific job (establish the climate, hold the wide), state it as a HARD REQUIREMENT in BOTH the summary and the per-shot line, and explicitly forbid the failure modes (cut short / turned into a close-up / skipped) — MiniMax needs the negative constraints to hold the shot.**

### Update 2026-08-30 (Pipeline 1 prompt v3 — fixed wide shot 1, stop/turn-right shot 2, side→across→back shot 3)

User reviewed Pipeline 1 v2: (1) **Shot 1** must be a **LONG WIDE STATIC shot** (camera does NOT move closer / NOT push in) — the whole purpose is to show the **landscape + sky slowly changing mood**, boy runs slowly, **5s**. (2) **Shot 2:** boy runs, stops, **looks toward his RIGHT side** (toward the river), **5s** for running + stopping + turning. (3) **Shot 3 "completely gone from the sequence, didn't appear, camera movement not showing"** → new choreography: **SIDE view (his right) → camera MOVES ACROSS (tracking) as he climbs over the handrail → camera swings to his BACK side as he jumps**, ENDS at his back mid-leap. **CRITICAL FIX: MiniMax DROPPED Shot 3 entirely** (it compressed the sequence and skipped the last shot). Added strong emphasis to the prompt: "ALL THREE shots must appear in this order, each getting its full time - do not skip, compress, or drop any shot, especially [Shot 3]" (in summary + detailed_description). **Rule: MiniMax will DROP the last shot of a multi-shot R2V if the prompt doesn't explicitly demand all shots appear — add a hard "ALL N shots must appear, do not skip/compress/drop any" line. Also: a wide establishing shot's purpose is the LANDSCAPE + sky change, so keep the camera FIXED (no push-in) and let the environment shift; and specify the camera's exact path for the jump shot (side → tracking across → back side) rather than a vague "camera rotates".**

### Update 2026-08-30 (Pipeline 1 prompt v2 — slow running + stop/turn/pan + in-motion shot 3)

User reviewed `jaisalproduction1.json` (Pipeline 1 only — Pipeline 2 not yet tried): (1) **Shot 1 (7s)** the boy "rushing, doesn't feel like running, felt like sliding a keyframe, not real" → now **SLOW, DELIBERATE, step-by-step** running: "each step clearly visible, one foot at a time, feet landing one after the other in a clear step-by-step rhythm (NOT rushing, NOT a fast blur, NOT sliding, NOT a smooth glide - real running with distinct steps)". (2) **Shot 2 (3s)** was good/matching pace → kept, but added at the end: the boy **SLOWS and STOPS, then TURNS toward the river, and the camera PANS to follow him** into the next view (the user's "stop and turn, then pan to Picture 3" idea — motivates the cut). (3) **Shot 3 (5s)** was the worst — "static, standing still for 2s while camera tilts" → now the boy is **IN MOTION the whole time**: "just stopped and turned toward the river, looks down at the water, takes a few steps toward the edge, crouches, and gathers himself to leap... NEVER standing still - every moment he is doing something (turning, stepping, looking down, crouching)". Kept the camera-rotate structure the user liked. **Rule: MiniMax makes running look like a "sliding keyframe" if you just say "runs" — specify SLOW + step-by-step + distinct footfalls. And a shot that opens on a static standing figure reads as dead — keep the character in motion from the first frame (turning/stepping/looking), and bridge the cut with a stop+turn+pan so the next shot's first frame is motivated.**

### Update 2026-08-30 (2-pipeline production split — `jaisalproduction1.json` + `jaisalproduction2.json`)

User: the full sequence should be ~25s (not 15s) with better rhythm — wide run-up 7s, close-up 3s, gather/climb/push-off 5s (15s run-up), then jump + drown 5-6s + title 4s. **Decision: split into TWO separate MiniMax R2V generations** (shorter clips = less style drift, cleaner 3-ref mapping, the jump is a natural splice point, re-run only the bad segment). Shot 3 (running medium) REMOVED entirely.

**Built two workflows** (both validated `valid: true`, 22 nodes):
- **`jaisalproduction1.json`** (run-up, **15s**, save `video/Jaisal_Production_1`): refs `jaisal_1_longshot` (ref_image_0), `jaisal_2_closeup` (ref_image_1), `jaisal_4_middle` (ref_image_2). Shots: (1) wide, boy RUNS ~7s, sky darkens clear→moody, rain begins, static wide → slow push-in; (2) close-up, boy RUNS (NOT static), camera tracks, wind + rain ~3s; (3) SIDE view at middle in HEAVY RAIN, crouches + gathers, camera ROTATES, climbs over low handrail, pushes off toward river, ENDS mid-launch ~5s.
- **`jaisalproduction2.json`** (leap + title, **11s**, save `video/Jaisal_Production_2`): refs `jaisal_5_jump` (ref_image_0), `jaisal_6_underwater` (ref_image_1), `jaisal_7_title` (ref_image_2). Shots: (1) SHORT natural leap CLOSE to bridge (NOT a long throw / stone) ~2s; (2) underwater, sinks completely down, rising bubbles ~4.5s; (3) title card, bubbles foam up, 'The Jaisal Cut' slowly becomes visible, color grade EXACTLY matches shot 2 ~4s.
- **Both prompts lock a consistent color grade** (same dark moody palette / dim grey light / water color across all shots) to minimize the two-generation seam.
- **Splice:** cut at the push-off moment (pipeline 1 ends mid-launch, pipeline 2 starts in-air), HARD CUT not crossfade, color-match the splice frame in post.
- **Build script:** `d:\models\vsCodeMcp\utilities\build_production_pipelines.py` (copies `jaisal_lowangle.json`, keeps 3 LoadImage nodes per pipeline, rebuilds node 136 to 3 ref slots, new links 300-302, sets length + save prefix + prompt).
- **Rule: for a long cinematic sequence, split into 2-3 shorter R2V generations at natural action splice points (push-off → in-air) rather than one long run — less drift, cleaner refs, easier re-runs. Join in a video editor with a hard cut + color match.**

### Update 2026-08-30 (7-shot MiniMax R2V — `jaisal_lowangle.json`)

User: "now lets go to minimax... we have 7 images... first one is a long shot (add running + climate change), 2nd close-up (camera movement + wind), 3rd running (motion + camera + wind), 4th kid standing middle full figure (ADD rain), 5th wide low-angle jump (complete the motion into the river), 6th underwater (move kid completely down), 7th title. All transitions smooth and organic. NOTE: the picture added as 1 can be reference image 0 in the node and it can mess up the prompt if we add picture 1 in prompt — so let's not make that mistake. This is a multi-billion-dollar company's production animation — a cinematic masterpiece intro."

**Built `jaisal_lowangle.json` as a 7-shot R2V** (validated `valid: true`, 26 nodes):
- **7 LoadImage nodes** (137, 139, 147, 148, 149, 150, 151) → `MiniMaxH3ReferenceToVideo` (136) `ref_image_0`..`ref_image_6`. Images copied to `input\` as `jaisal_1_longshot.png` … `jaisal_7_title.png`.
- **CRITICAL (user's note):** the `<Picture N>` tags map 1-to-1 to `ref_image_N` IN CONNECTION ORDER — `<Picture 1>` = `ref_image_0` = image 1 (long shot), etc. This is the correct pattern (each reference is a frame anchor for its shot), NOT a mistake. The old 2-ref workflow's "mess up" concern was about a single reference being both the style anchor AND the first frame; here each of the 7 references is its own shot's first frame, so the mapping is clean.
- **Prompt (node 138):** 7-shot R2V structure (subject_definitions / summary / retention_analysis / detailed_description with timed `[Shot N] At MM:SS.mmm` blocks / overall_soundscape / non_diegetic_music). Each shot: (1) long shot — boy runs, sky darkens clear→moody, wind + rain begins, static wide → slow push-in; (2) close-up — gentle camera push-in/drift + wind in hair/shirt; (3) running — camera tracks alongside at running pace, wind + rain + splashes; (4) middle full figure — ADD heavy rain, steady camera with subtle drift; (5) wide low-angle jump — camera completes his motion into the river, big splash; (6) underwater — camera follows him sinking completely down, rising bubbles; (7) title — calm dark water, bubble-formed 'The Jaisal Cut' title held steady. **All transitions smooth and organic.**
- **Bag color FIXED:** prompt now says **BLACK school bag** (was "red school bag" — the pending fix from earlier).
- **Title:** shown in Shot 7 (the title reference image), NOT rendered as a text overlay by the model.
- **Build script:** `d:\models\vsCodeMcp\utilities\build_minimax_7shot.py` (copies images, grows node 136 to 7 ref slots, shifts downstream link slots prompt→13/width→14/height→15/length→16, adds links 289-294).

### Update 2026-08-30 (size hierarchy: The < Cut < Jaisal)

User asked for a **size hierarchy** in the title: **"The" = SMALL, "Jaisal" = BIG (the hero word, largest), "Cut" = MEDIUM** (between the two). Prompt 10 positive now states the hierarchy explicitly: "the title words sized in a clear hierarchy - the word 'The' SMALL, the word 'Jaisal' BIG and dominant (the largest word, the hero of the title), the word 'Cut' MEDIUM (between the two)". **Tuning:** 'Jaisal' not big enough → strengthen it ("'Jaisal' MUCH larger than the other words, the clear focal point"); hierarchy lost (all words same size) → restate more forcefully and/or lower denoise a touch so the layout is followed more faithfully.
---

## D027 - Title animation = 2D VECTOR / LINE-ART stick figure (not cartoon/3D), MEDIUM shots only

Date: 2026-08-31
Status: Active

### Decision

The title animation is a **2D vector / line-art** piece — a **stick figure** (round head + line body + line arms + line legs, clean confident line work, lines only, NO shading, NO 3D, NO cartoon shading). Story: the stick figure **walks slowly** on the bridge → **throws a paper plane** into the river → **jumps into the river** after the paper plane → the paper plane is **still flying** as the title **"The Jaisal Cut"** appears. Simple, funny, **no special effects**. **MEDIUM SHOTS ONLY** (the figure's full body visible) — **NO wide shots**, NO extreme close-ups.

### Reason

The user wants a simple vector/line look ("just with lines and everything", "a stick with a head and hand and legs"), not the cartoon/2D brush-stroke style. The paper-plane gag makes it funny. Medium shots keep the figure readable. The line-art look is carried by the **`krea2_lineart_v1_fp16.safetensors`** LoRA (Civitai "Krea2 Line Art Style", downloaded 2026-08-31, 56 MB, in the main loras path).

### Alternatives considered

- Cartoon/2D brush-stroke style (rejected — user wants pure lines).
- Wide establishing shots (rejected — user: "lets not keep any wide shots, medium shots are fine").
- Other Civitai sketch/vector LoRAs (`SimpleFineVector_Krea2_v1`, `krea2_coloringbook_v1`, `friendlysketch-v2_krea2`) — found but the Civitai download hit a Cloudflare challenge page (10 KB HTML); only `krea2_lineart_v1_fp16` downloaded cleanly. Re-download the others if the line-art LoRA isn't clean enough.

### Result

`d:\models\vsCodeMcp\prompts\jaisal_sketch_prompts.txt` created — 4 ready-to-paste Krea2 t2i prompts (walk / throw paper plane / jump / title) + shared style prefix + shared negative (excludes 3D/shading/color-fill/carton/wide-shot/close-up) + a full MiniMax H3 R2V prompt (4 refs, 4 shots, 4s each, 16s). **Rule: the title animation is a 2D vector line-art stick figure, medium shots only, paper-plane gag, no special effects. Use the `krea2_lineart_v1_fp16` LoRA @ 1.0.** See `jaisal_sketch_prompts.txt`.

### Production pipeline note (2026-08-31)

The production workflow renders at **1MP (1344×768, native) and is UPSCALED to 2MP** — we do NOT generate 2MP video directly (VRAM thrashing on the 32 GB card). Upscale path: `RTXVideoSuperResolution` (2× ULTRA) or `TopazVideoEnhance` (Starlight 1080p/4K) inserted between `CreateVideo` and `SaveVideo`.

---

## D028 - MiniMax R2V prompts use standard cinematography vocabulary (shot size + angle + movement + focus per shot)

Date: 2026-08-31
Status: Active

### Decision

Every MiniMax H3 R2V `[Shot N]` line names the **shot size + camera angle + camera movement + focus** EXPLICITLY using standard cinematography terms (e.g. "a static eye-level MEDIUM shot, deep focus", "a slow tracking shot from the side", "a low-angle shot looking up"). The full vocabulary (shot size / framing / focus / angle / movement / mechanism, each with a ready-to-paste phrase) is saved at `d:\models\vsCodeMcp\docs\CAMERA_SHOT_VOCABULARY.md` (sourced from the StudioBinder "50+ Types of Camera Shots, Angles, and Techniques" guide).

### Reason

MiniMax responds to standard cinematography vocabulary far better than vague words like "the camera moves" or "a nice angle". Naming the exact shot size + angle + movement + focus per shot gives much tighter shot control. The Jaisal Cut title animation uses MEDIUM shots only, static camera (low-angle for the jump), deep focus.

### Alternatives considered

- Vague camera descriptions (rejected — weak shot control).
- Naming real camera gear (tripod/dolly/drone) in a 2D line-art prompt (rejected — can confuse the model; for 2D animation just say "static" or "smooth tracking").

### Result

`CAMERA_SHOT_VOCABULARY.md` created (complete cheatsheet + ready-to-paste phrases). The Jaisal Cut title-animation MiniMax prompt (`jaisal_sketch_prompts.txt`) rewritten to the user's exact sequence (walk → stop → look around both sides → whistle → jump → title) using the camera vocabulary. **Rule: name shot size + angle + movement + focus explicitly for every [Shot N]; keep the vocabulary cheatsheet handy for reuse.**