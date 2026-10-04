# Project Decisions

## D001 â€” Use ComfyUI MCP for workflow interaction

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

## D002 â€” Use local Qwen as the reasoning model

Date: 2026-08-26
Status: Active

### Decision

Use the local Qwen model through llama.cpp rather than relying on Claude/Codex for ComfyUI reasoning.

### Reason

Local inference provides control over the model, context, performance, and cost.

### Result

Qwen is successfully interacting with ComfyUI through MCP.

---

## D003 â€” Preserve project knowledge in Markdown

Date: 2026-08-26
Status: Active

### Decision

Use Markdown files under `project-memory/` as persistent project state.

### Reason

The AI chat context is temporary. Important project decisions must survive model/session changes.

### Result

Project state, decisions, experiments, and workflow history are stored separately from chat history.

---

## D004 â€” "The Jaisal Cut" title is composited in post, not rendered

Date: 2026-08-26
Status: Active

### Decision

Do NOT render the "The Jaisal Cut" title text with the diffusion model. Generate the title frame as the scene (kid looking up, sky clearing) without text, then composite the title + the J-dot effect (kid becomes the dot in the J) in post (After Effects / DaVinci Resolve).

### Reason

Diffusion is unreliable at spelling text correctly. The J-dot is a 2-second post effect, not a generation problem. This is the single biggest quality win.

### Alternatives considered

- In-image text rendering (rejected â€” unreliable spelling)

### Result

Title frame generated text-free; title + J-dot added in post.

---

## D005 â€” Locked Krea2 style chain for all Jaisal Cut frames

Date: 2026-08-26
Status: Active

### Decision

Every Jaisal Cut frame uses the same chain: `krea2_turbo_fp8_scaled.safetensors` + `Krea2_Cinematic_Artstyle.safetensors` LoRA (strength 1.0) + `qwen3vl_4b_fp8_scaled.safetensors` CLIP (type krea2) + `qwen_image_vae.safetensors`, with the style prefix "An angular, 3d art style, with brush stroke color texture." on every prompt. 2048Ã—1152, 8 steps, cfg 1.0, euler/simple, denoise 0.7 for i2i.

### Reason

Consistent style = MiniMax blends the 9 frames smoothly into the 15s video. Identity is locked by i2i from the face anchor.

### Alternatives considered

- Per-frame style variation (rejected â€” breaks MiniMax blending)

### Result

All frames share one style; identity locked via i2i anchors.

---

## D006 â€” Medium shot is i2i from the face anchor

Date: 2026-08-26
Status: Active

### Decision

The medium shot (head + upper body on the bridge) is generated i2i from the face anchor (jaisal_face_v4_A.png), not t2i, to lock the kid's identity while widening the framing.

### Reason

t2i would risk a different face; i2i from the face keeps identity consistent across the wide / medium / close-up framings.

### Alternatives considered

- t2i medium shot (rejected â€” identity drift)

### Result

krea2_jaisal_medium.json generates the medium anchor with locked identity.

---

## D007 â€” Single character only, no duplicates

Date: 2026-08-26
Status: Active

### Decision

Every frame must show exactly ONE kid. No duplicate characters, no second kid. Added "duplicate character, 2 kids, duplicated kids, two kids, second kid" to the shared negative prompt, and "a single young Indian schoolboy, one kid only" to the wide-shot prompts.

### Reason

storysheet_01 rendered two characters (start and end of the bridge). The story is about one kid.

### Result

Single-character constraint enforced on all frames.

---

## D008 â€” Consistent costume: red school bag, no tie

Date: 2026-08-26
Status: Active

### Decision

The kid's red school bag must stay RED across all frames (it turned blue in the close-up). The kid wears NO tie (a tie appeared in the gust frame that wasn't in the others). Added "red school bag" to close-up prompts and "tie, necktie, blue bag, blue school bag" to the negative.

### Reason

Costume consistency is critical for MiniMax to blend the frames smoothly. A color change or added accessory breaks continuity.

### Result

Red bag + no tie enforced on all frames.

---

## D009 â€” Close-up frames keep the moody atmosphere

Date: 2026-08-26
Status: Active

### Decision

The close-up frames (4, 5, 6) keep the same moody overcast atmosphere. Beat 6 (rain clearing) is NOT a sunny/cleared sky â€” the rain has just stopped for a moment, the sky is still dark and moody. The rain effect from the generated frames is preserved by i2i from the current frames (jaisal_ss04/05/06.png).

### Reason

The emotional core is the rain coming and going in a moody setting. A sudden sunny sky breaks the mood. The rain effect in the generated frames is good and should be kept.

### Result

Moody atmosphere + preserved rain effect on close-up frames.

---

## D010 â€” The "cut" section camera is above the kid, zooming out

Date: 2026-08-26
Status: Active

### Decision

The "cut" section (beats 7, 8, 9) uses a HIGH-ANGLE camera above the kid (looking down, seeing the bridge + water body underneath), the kid looking up at the sky, and the camera panning + zooming out. Beat 8 CONTINUES the zoom-out (does NOT revert to the initial river-level camera). Beat 9 is the final wide shot of the whole river bridge (kid = the dot in the J), no text. Beats 7â†’8â†’9 are chained (each i2i from the previous) for a smooth zoom-out.

### Reason

The initial river-level camera (beats 1-2) is a different shot. The "cut" is a new camera angle (above the kid) that pans and zooms out to reveal the whole bridge for the title. Reverting to the river camera broke the flow.

### Result

Smooth high-angle zoom-out for the cut section, ending on the whole bridge for the title.

---

## D011 â€” Visual continuity is the top priority; fix by i2i from the good frame

Date: 2026-08-26
Status: Active

### Decision

When fixing a continuity problem between shots, do NOT independently redesign the scene. i2i from the frame that already has the correct look (identity, clothing, bag, environment, lighting, composition) and change only the specific problem. Use low denoise (0.5) for single-element fixes (tie removal, strap fix) and ~0.6-0.7 for camera/framing changes. For a continuous camera movement (the 07â†’08â†’09 aerial ascent), CHAIN the frames (each i2i from the previous) so the sequence reads as one drone shot.

### Reason

Independently regenerating shots breaks character/costume/environment continuity, which breaks MiniMax's ability to blend the frames into a coherent video. The rain effect in the close-ups is good and must be preserved â€” so close-up fixes i2i from the current close-up frames, not from the face anchor.

### Alternatives considered

- Regenerate from the face/base anchor (rejected â€” loses the environment/rain continuity)
- High denoise re-rolls (rejected â€” risks identity/environment drift)

### Result

Continuity fixes applied via targeted i2i: 03 from 04's environment, 05 tie removal (denoise 0.5), 06 both straps (denoise 0.5), 07â†’08â†’09 chained aerial ascent.

---

## D012 â€” Use inpainting for single-element removal that i2i can't fix

Date: 2026-08-26
Status: Active

### Decision

When a low-denoise i2i fails to remove a high-contrast element (e.g. a tie â€” the model preserves it because it's a strong detail), use INPAINTING: mask just the region to change (collar/tie), and regenerate ONLY that region with denoise 1.0 while the rest of the image stays locked. Workflow: LoadImage (frame) â†’ VAEEncode â†’ SetLatentNoiseMask (mask) â†’ KSampler (denoise 1.0) â†’ VAEDecode. The mask is a grayscale image (white = regenerate) loaded via LoadImage â†’ ImageToMask â†’ GrowMask (expand ~20px, tapered_corners false).

### Reason

A full-image i2i at low denoise keeps the tie because the model preserves high-contrast details. Inpainting isolates the change to the masked region, so the face, bag, environment, and composition are untouched â€” only the collar/tie area is regenerated.

### Alternatives considered

- Higher-denoise full i2i (rejected â€” risks identity/environment drift)
- Prompt-only negative (rejected â€” tie persisted)

### Result

krea2_jaisal_fix05_inpaint.json removes the tie from beat 05 via a collar-region mask. Mask file: jaisal_ss05_tie_mask.png (ellipse over the collar/tie region). NOTE: Krea2 is NOT an inpaint model â€” the Krea2 inpaint came out distorted. Use the Flux one-node for real inpainting.

---

## D013 â€” Use the Flux one-node (FluxKleinOneNode) for real inpainting

Date: 2026-08-26
Status: Resolved (manual UI run)

### Decision

For single-element removal that Krea2 can't handle (Krea2 is not an inpaint model â€” its inpaint output is distorted), use the **Flux one-node** (`FluxKleinOneNode`, "One Node Â· FLUX.2 [klein]") in PAINT/Inpaint mode.

### Blocker

The one-node is a FRONTEND-DRIVEN UI widget: its `noop` function just returns the JS preview image; generation is triggered from the ComfyUI UI (via `POST /flux_klein/set_output`), NOT through the standard prompt queue â€” so it CANNOT be driven via `run_workflow`/MCP. It also needs **FLUX.2 [klein] models** (a diffusion model + matching text encoder + VAE) that are NOT installed (local model dirs are empty). The ComfyUI-Inpaint-CropAndStitch dependency IS present.

### Resolution options

- (a) Install FLUX.2 [klein] models (diffusion + text encoder + VAE) into the local model dirs, then drive the one-node from the ComfyUI UI (PAINT â†’ Inpaint: paint the tie region, describe "open collar, no tie").
- (b) User runs the one-node manually in the ComfyUI UI.

### Result

RESOLVED â€” the user ran the one-node manually in the ComfyUI UI (PAINT/Inpaint) and the tie was removed successfully. Beat 05 is done. The one-node works when driven from the UI; the MCP/prompt-queue path is not available for it.


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
- **KSampler = 7 values** `[seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]` â€” the hidden `control_after_generate` widget (randomize/fix/+1/-1 dropdown next to seed) is NOT in `/object_info`.
- **LoadImage = 2 values** `[filename, "image"]` â€” the 2nd literal `"image"` is NOT in `/object_info`.
- **No `widgets_values_named` key** â€” native UI-saved files don't have it; its presence marks a machine-built file.

### Reason

`/object_info` lists only the "required" widget inputs, which OMITS hidden widgets the UI actually renders. Building `widgets_values` from that order makes the array too short, so the server maps values positionally and they shift one slot left: KSampler `cfg` gets `'euler'`, `sampler_name` gets `'simple'`, `scheduler` gets `0.4` â†’ prompt validation fails ("could not convert string to float", "Value not in list"); LoadImage image not shown; UI shows "no details". This affected ALL 21 machine-built workflows (the 08-27 converted batch + jaisal_drone_optimized).

### Alternatives considered

- Building from `/object_info` order (the original bug â€” rejected).
- Adding `widgets_values_named` to disambiguate (rejected â€” native files don't use it; the UI ignores it and it's a machine-built marker).

### Result

`fix_all_widget_shapes.py` applied the native shape to all 21 machine-built workflows (435 changes; backups in `d:\models\vsCodeMcp\workflow_backups\pre_widget_fix\`). All 21 re-validated via MCP (`valid: true`, 0 errors). **Rule for all future workflow building: copy `widgets_values` shapes from a native UI-saved workflow, never from `/object_info`.** See AGENTS.md "CRITICAL: widgets_values must match the server's widget order EXACTLY".

---

## D016 - Machine-built workflows must use `type='COMBO'` + LoadImage `upload` input (not static lists)

Date: 2026-08-27
Status: Active

### Decision

When building/converting workflow JSON, widget-input `type` fields for combo widgets (KSampler `sampler_name`/`scheduler`, LoadImage `image`, CLIPLoader `clip_name`/`type`/`device`, UNETLoader `unet_name`/`weight_dtype`, VAELoader `vae_name`, LoraLoaderModelOnly `lora_name`) MUST be the string `'COMBO'`, NOT a static list of values. And every LoadImage node MUST include the `upload` input (`type='IMAGEUPLOAD'`, `localized_name='choose file to upload'`).

### Reason

A static list dumped into `type` is a stale snapshot â€” the UI shows it but it doesn't refresh, and (critically) the converter DROPPED the `upload` input, so the LoadImage node had no "choose file to upload" button and no live dropdown. The node still held the correct filename in `widgets_values` (so it "picked up the correct image"), but the user couldn't select/preview a different image in the UI. `type='COMBO'` tells the frontend to populate the dropdown from the server live; the `upload` input renders the file-picker.

### Alternatives considered

- Keeping the static list (rejected â€” stale, no upload button).
- Only fixing LoadImage (rejected â€” the same static-list problem affected KSampler/CLIPLoader/UNETLoader/VAELoader/LoraLoaderModelOnly combo inputs too; fixed all in one pass).

### Result

`fix_combo_inputs.py` set 253 static-list inputs to `'COMBO'` and added 37 `upload` inputs across all 21 machine-built workflows (backups in `d:\models\vsCodeMcp\workflow_backups\pre_combo_fix\`). All re-validated via MCP (`valid: true`, 0 errors). **Rule: combo widget inputs use `type='COMBO'`; LoadImage always has both `image` (COMBO) and `upload` (IMAGEUPLOAD) inputs.** See AGENTS.md.

## D017 - MiniMax H3 R2V prompts use the official 6-section reference style

Date: 2026-08-27
Status: Active

### Decision

All MiniMax H3 reference-to-video (R2V) prompts MUST follow the official MiniMax H3 R2V prompting style: reference each input by a tag in **connection order** (`<Picture 1>` = `ref_image_0`, `<Picture 2>` = `ref_image_1`, â€¦), assign each reference an explicit **job** (identity / style / motion / camera / frame anchor), and structure the prompt into the **6 sections** in order: `subject_definitions`, `summary` (with a `[task-type]` prefix like `[reference generation]`), `retention_analysis` (one line per label + a relationship marker), `detailed_description` (350-500 words, partitioned into `[Shot 1]`â€¦`[Shot N] At MM:SS.mmm` with camera angles + actions), `overall_soundscape`, `non_diegetic_music`.

### Reason

The MiniMax H3 R2V model is trained on prompts in this exact structure. Using `<Picture N>` tags in connection order tells the model precisely which reference provides what (identity vs. frame anchor vs. style). Partitioning into timed `[Shot N]` blocks with camera angles gives the model a clear storyboard. A free-form prompt (the old style) under-uses the references and produces weaker shot control. The official guide is saved at `d:\models\vsCodeMcp\docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md` for reuse.

### Alternatives considered

- Free-form prose prompt (rejected â€” under-uses references, weak shot control).
- Only `<Subject N>` labels without `<Picture N>` frame anchors (rejected â€” loses the per-shot frame anchoring that R2V is built for).

### Result

`jaisal_lowangle.json` prompt rewritten to this style (5 `<Picture N>` frame anchors, `<Subject 1>` boy / `<Subject 2>` bridge, 5 timed shots, title composited in post). Validated `valid: true`. **Rule: every R2V prompt uses `<Picture N>`/`<Subject N>` tags in connection order + the 6-section structure + timed `[Shot N]` blocks.** See `MINIMAX_H3_R2V_PROMPTING_GUIDE.md`.

## D018 - Multi-ref workflow wiring: set the input `link` field by SLOT INDEX, not name number

Date: 2026-08-27
Status: Active

### Decision

When building a workflow with multiple reference inputs (e.g. `MiniMaxH3ReferenceToVideo` `ref_image_0`â€¦`ref_image_8`), the `link` field on each input in the node's `inputs` array MUST be set to the link ID **by the input's array slot index**, NOT by the number in the input's name. The link's `to_slot` equals the input's position in the `inputs` array, which can differ from the number embedded in the input name.

### Reason

In `jaisal_lowangle.json`, the template had links 289 (LA4â†’136.6) and 290 (LA5â†’136.7) but the `MiniMaxH3ReferenceToVideo` node's `inputs` array had `link=None` on `ref_image_3` (slot 6) and `ref_image_4` (slot 7). The UI showed only 3 images wired and validation reported `node_not_reachable_from_output` for LA4/LA5. The bug: the input *name* number (`ref_image_3`â†’3) differs from the input *slot* position (index 6/7). Setting `link` by name number looked for a link targeting slot 3/4 (which don't exist for these inputs); setting it by actual array index (6/7) matched the real links.

### Alternatives considered

- Setting `link` by the name number (rejected â€” wrong slot, no match).
- Only creating the link without setting the input `link` field (rejected â€” UI shows no connection, validation flags unreachable).

### Result

`fix_lowangle_wiring_and_prompt.py` set `ref_image_3.link=289` and `ref_image_4.link=290` by slot index. All 5 images now wired; validation `valid: true`, 0 warnings. **Rule: when wiring multi-ref inputs, set each input's `link` field to the link ID whose `to_slot` equals that input's array index.**

## D019 - Subgraph templates: set widget values on INTERNAL nodes, not the instance

Date: 2026-08-28
Status: Active

### Decision

When a gallery template wraps its main node in a **subgraph** (the instance node's `type` is a UUID, e.g. `4c314f31-ecda-4b08-ae98-faaba1bf613f`), widget values (prompt, duration, turbo, LoRA, etc.) MUST be set on the **internal nodes** under `definitions.subgraphs[0].nodes`, NOT on the instance node's `widgets_values`. The instance node's `widgets_values_named` dict is also preferred over `widgets_values` by the UIâ†’API converter, so update both.

### Reason

The `video_minimax_h3_i2v` template's `MiniMaxH3ImageToVideo` node (instance id=105) is a subgraph. Editing the instance's `widgets_values[10]` (LoRA) had NO effect â€” the converter read the LoRA from the internal `LoraLoaderModelOnly` node (id=121), which still held the template default `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` (not installed) â†’ validation error `node 105/121: lora_name not in options`. The `105/121` notation = instance 105, internal node 121. Setting `lora_name` on internal node 121 (both `widgets_values[0]` and `widgets_values_named['lora_name']`) to the installed `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors` fixed it.

### Alternatives considered

- Editing only the instance `widgets_values` (rejected â€” ignored by the converter for subgraph nodes).
- Downloading the 8-step LoRA (rejected â€” we already have the 4-step 768p version, which is faster and proven on the drone workflow).

### Result

`jaisal_single_shot.json` validates `valid: true`, 0 errors. **Rule: for subgraph templates, locate the internal node and set its `widgets_values` + `widgets_values_named`; also update the instance's `widgets_values_named`.** Related: the `ResolutionSelector` aspect enum is `16:9 (Widescreen)` (the template's own `Widescreeen` spelling fails validation). See AGENTS.md.

## D020 - R2V: use 2-3 reference images max with a SIMPLE prompt (not 5 + 500 words)

Date: 2026-08-28
Status: Active

### Decision

For MiniMax H3 reference-to-video, use **2-3 reference images max**, each mapped 1-to-1 to a shot with an explicit "the first frame of [Shot N]" anchor, and a **short** prompt. Do NOT use 5 images + a 500-word 6-section essay.

### Reason

The 5-image `jaisal_lowangle.json` (5 `<Picture N>` tags + 500-word prompt) came out bad: style drift, the boy not running, and the model confused by the refâ†’shot mapping (it couldn't cleanly map `ref_image_0`â†’`<Picture 1>`â†’[Shot 1] across 5 anchors). The single-shot i2v alternative also came out bad (cartoon style, weak motion). The fix: **2 images** (`1.png` = boy at start of bridge â†’ [Shot 1], `2.png` = boy in middle of bridge â†’ [Shot 2]) with a simple prompt where each `<Picture N>` is explicitly "the first frame of [Shot N]". The model animates between 2 clear anchors far better than it follows a 5-anchor storyboard.

### Alternatives considered

- 5-image R2V (rejected â€” style drift, no running, confused mapping).
- Single-shot i2v (rejected â€” cartoon style, weak motion).
- 3-image R2V (fallback â€” add a 3rd reference showing the running pose if 2 images don't produce the run).

### Result

`jaisal_lowangle.json` rebuilt as 2-image via `build_2ref.py` (deleted LoadImage 143/LA4/LA5 + links 285/289/290, cleared `ref_image_2/3/4` link fields, simple 2-anchor prompt, save prefix `video/Jaisal_2Ref_1_2`). Validated `valid: true`, 0 errors. **Rule: 2-3 refs max, each an explicit frame anchor, simple prompt. If the character isn't doing the action, add a 3rd reference showing that pose or strengthen the motion verb.** See AGENTS.md.

## D021 - Hold the Krea2 style in MiniMax video via a Krea2-styled REFERENCE SET (not frame-by-frame)

Date: 2026-08-28
Status: Active

### Decision

To keep the Krea2 angular brush-stroke style across a WHOLE MiniMax H3 video (not just the first 2-3s), **generate a set of Krea2-styled reference images first** (character sheet, abstract, bridge, medium, close-up, water, running â€” all faceless character, rose shirt/black pant/black bag) and feed 2-3 of them as references to the MiniMax R2V workflow. Do NOT use a frame-by-frame Krea2 style-transfer pipeline (extra work).

### Reason

MiniMax H3 is a general video model â€” its prior smooths toward its own default look, so the Krea2 style "completely went" in the video. The turbo LoRA is a *speed* distillation, not a *style* LoRA. Reference images only anchor the first frame, so drift creeps in over 15s. A frame-by-frame Krea2 i2i pipeline would guarantee the style but is extra work (extract frames â†’ batch i2i â†’ reassemble). The cleaner path: create a proper Krea2-styled reference set upfront and feed it to MiniMax so it holds the style across the whole video.

### Alternatives considered

- Frame-by-frame Krea2 style transfer (rejected â€” extra work; user: "creating a video and snapping is extra work, let's create the images properly").
- Stronger style description in the prompt only (insufficient â€” text can't fully carry the style).
- Training a MiniMax H3 style LoRA (best long-term, but heavy â€” needs training infra; keep as a future option).

### Result

`krea2_jaisal_refs.json` (Krea2 t2i generator, validated) + `jaisal_ref_prompts.txt` (7 faceless-character prompts). **Rule: for style-consistent video, build a Krea2-styled reference set first and feed 2-3 of it to MiniMax.** See AGENTS.md.

## D022 - The Jaisal Cut character is FACELESS (head + hair only) with rose shirt / black pant / black bag

Date: 2026-08-28
Status: Active

### Decision

The Jaisal Cut character is a **normal young schoolboy with short dark hair** (face OK â€” see correction below). Costume: **rose-pink collared shirt, full-length black trousers, black school bag** (replacing the old red bag / school-uniform look). Every prompt must emphasize **ONLY ONE character, no duplicates** (Krea2 tends to duplicate the character).

### Reason

The user originally requested a faceless figure ("a head and hair, no nose, no face, no eyebrow, no mouth") because faces are the hardest thing to keep consistent in video. **Correction (2026-08-28): Krea2 CANNOT make a faceless character â€” it always renders a face.** The user accepted this: "krea 2 doesnt create faceless, but thats fine we are good with 1 character sheet." So the character is a normal boy with short dark hair + the new costume.

### Alternatives considered

- Faceless figure (rejected â€” Krea2 can't do it; it always renders a face).
- Keeping the red bag / school uniform (rejected â€” user changed the costume to rose shirt / black pant / black bag).

### Result

All reference images (`jaisal_ref_prompts.txt`) use the normal-face boy + new costume + "ONLY ONE character" emphasis. The bridge prompt pins the boy **ON THE BRIDGE DECK (left side), NOT in the water** (Krea2 had put him in the river). The MiniMax prompt (v2) still says "red school bag" â€” **update it to "black school bag"** when re-running MiniMax with the new references. **Rule: the Jaisal Cut character is a normal boy (short dark hair), rose-pink collared shirt, black trousers, black school bag, always a SINGLE character.**

## D023 - Face consistency via Krea2 Identity Edit v1.2 workflow (not t2i re-rolls)

Date: 2026-08-29
Status: Active

### Decision

To keep the SAME face across all Jaisal Cut reference images, use the **Krea2 Identity Edit v1.2** workflow (`krea2_identity_edit.json`, LoRA `krea2_identity_edit_v1_2.safetensors`, `comfyui-krea2edit` node pack â€” both already installed). Load a good reference (character sheet / clean close-up) in the LoadImage node, write a plain-English instruction for the new scene, and it regenerates the scene keeping the same face/identity. `ref_boost` = 4.0 (recommended fidelity), KSampler 10 steps cfg 1, `grounding_px` 384-768, 1MP output.

### Reason

Krea2 t2i gives a DIFFERENT face every time the character appears ("literally a different guy" across the reference set). The identity-edit model treats the reference image like a LoRA â€” much stronger face+body likeness than re-rolling t2i seeds. User found the workflow on reddit; it's the right tool for a production character.

### Alternatives considered

- Re-rolling t2i seeds until the face matches (rejected â€” unreliable, the face drifts every generation).
- Training a character LoRA (rejected â€” heavy; identity-edit is ready now).

### Result

`krea2_identity_edit.json` validates `valid: true` (1 expected warning: optional 2nd-image group ships bypassed). **Rule: for consistent-character reference sets, generate the base image with t2i, then lock the face with the identity-edit workflow (ref_boost 4).**

## D024 - Climate consistency: one moody tone once rain starts (no drastic changes)

Date: 2026-08-29
Status: Active

### Decision

Do NOT change the climate dramatically between shots. Once the rain starts, keep ONE moody tone across all rain/water shots (medium, close-up, water, running). The underwater shot must be DARK and moody (matching the rain), NOT bright/sunny.

### Reason

The generated water reference came out bright with a canal/bund look while the rest of the set was moody â€” a drastic light change between shots breaks continuity, and MiniMax won't bridge a hard climate jump between references.

### Result

Prompts 4-7 in `jaisal_ref_prompts.txt` updated: square handrails (not round/ornate/staircase), open river (not canal/bund), dark moody water (not bright), three-quarter view (not facing camera). **Rule: one moody tone from the first rain onward; no bright/sunny shots after rain starts.**

---

## D025 - Identity workflow: wire the STYLE LoRA in to match skin tone / lighting

Date: 2026-08-29
Status: Active

### Decision

Add the **style LoRA `Krea2_Cinematic_Artstyle.safetensors` @ 0.7** to the Krea2 Identity Edit v1.2 workflow (`krea2_identity_edit.json`) as a new node **95** between the identity LoRA (71) and the `Krea2EditModelPatch` (79). Chain: `55 UNETLoader â†’ 71 identity LoRA â†’ 95 style LoRA â†’ 79 patch â†’ 53 KSampler`.

### Reason

The identity workflow carries the **reference image's color tone** into the output. A neutral/bright character-sheet reference makes the boy come out studio-lit, clashing with the dark moody rainy scene (skin tone mismatch). The style LoRA pulls the output back into the angular brush-stroke style AND the moody palette of the scene.

### Alternatives considered

- Relying on the instruction's lighting words alone (helps but doesn't fully fix the reference's color tone).
- Using a reference that is already in the moody scene (best â€” then the tone matches automatically).

### Result

Style LoRA wired in + validated `valid: true`. **Tuning:** style too weak â†’ raise node 95 to 0.8-1.0; face distorts â†’ lower to 0.5. **Also:** keep the lighting words in the instruction ("moody overcast light"); if skin still too bright add "skin tone matching the dark moody overcast light, dim diffused light on the face, NOT studio lit". **Best:** use a reference already in the moody scene instead of the neutral character sheet. Backup: `krea2_identity_edit.json.pre_stylelora.bak`.

---

## D026 - Title card "The Jaisal Cut" via Krea2 i2i + Typnosis typography LoRA

Date: 2026-08-30
Status: Active

### Decision

Generate the title card with a dedicated Krea2 **i2i** workflow `krea2_jaisal_title.json`: load the underwater shot (`refs_water.png`), keep the SAME underwater scene, and swap the boy for the title **"The Jaisal Cut"** using the **Typnosis_Krea2** typography LoRA (verified: "Typnosis v2 triggerless Krea 2 Raw typography/domain LoRA") chained after the Cinematic style LoRA. Chain: `UNET krea2_turbo_fp8_scaled â†’ Cinematic LoRA @1.0 â†’ Typnosis LoRA @1.0 â†’ KSampler (8 steps cfg 1, denoise 0.55)`.

### Reason

The underwater shot has generous negative space for a title. An i2i (low-moderate denoise) keeps the scene consistent while the typography LoRA renders the title text. Verified we already have Krea2 i2i workflows (`krea2_jaisal_title_moody.json` etc.), so this reuses the proven i2i pattern.

### Alternatives considered

- Compositing the title in post (Photoshop) â€” works but the user wanted it generated in ComfyUI with the typography LoRA.
- t2i from scratch â€” would lose the consistent underwater scene.

### Result

`krea2_jaisal_title.json` built + validated `valid: true`. Prompt (prompt 10 in `jaisal_ref_prompts.txt`) keeps the underwater scene + swaps the boy for the title. **Tuning:** title garbled â†’ lower denoise to 0.4; boy still there â†’ raise denoise to 0.65-0.7.

### Update 2026-08-30 (STR5 + bubble-formed title)

User tested the title card and **STR5 (strength 5.0) on the Typnosis LoRA reads best** for the title (per the Typnosis author notes: STR1-STR2 is most prompt-faithful, STR4+ gets more stylized and compositions converge â€” STR5 is the balanced-strong sweet spot). Set node 32 `strength_model` = **5.0**. User also asked for **bubbles**: the title is now **formed ENTIRELY from clusters of rising air bubbles** (each letter built from many small/medium bubbles glowing against the dark water) with **additional bubbles drifting around the title** â€” fits the underwater scene. Prompt 10 positive updated accordingly. **Tuning:** STR5 over-stylizes/distorts letters â†’ drop to 3.0-4.0; bubbles too sparse â†’ strengthen the bubble wording ("DENSE clusters of many small bubbles") or nudge the LoRA up.

### Update 2026-08-30 (wavy floating layout)

User asked for a **wavy type** since the bubbles are in water â€” the words should **float a little**: not too adjacent (spaced apart with generous gaps), letters can be **different sizes/shapes**, but the whole **"The Jaisal Cut"** must stay clearly readable. Prompt 10 positive now adds: "the letters and words arranged in a gentle WAVY floating layout, each word drifting at a slightly different height as if floating in the water, the words spaced apart with generous gaps between them (NOT cramped, NOT adjacent), the individual letters varying slightly in size and shape for an organic floating feel, the whole title 'The Jaisal Cut' clearly readable and centered". **Tuning:** words too flat/straight â†’ strengthen the wavy wording ("each word drifting at a clearly different height, a gentle S-curve"); words too scattered / title stops reading as one line â†’ soften it ("a SUBTLE gentle wave, words only slightly offset, kept close enough to read as one title").

### Update 2026-08-30 (CPU RAM exhaustion on the 7-ref MiniMax run â€” CORRECTED diagnosis)

The 7-shot `jaisal_lowangle.json` run failed with `numpy._core._exceptions._ArrayMemoryError: Unable to allocate 24.0 MiB for an array with shape (1088, 1928, 3) float32` at `nodes_minimax_h3.py:229 _resize`. **This is a CPU RAM exhaustion, NOT a VRAM problem and NOT a workflow bug.**

**CORRECTED (2026-08-30, after measuring with `top_ram.py`):** my first claim â€” "the 7 Krea2 runs left ~17 GB of Krea2 models resident in CPU RAM" â€” was **WRONG / unverified**. Measured reality: ComfyUI's `python.exe` was only **1.37 GB**. The dominant RAM consumer is the **local Qwen `llama-server.exe` at ~19-22 GB** (a SEPARATE process ComfyUI cannot touch). The system was at **95% load / 2.7 GB free**, so even a 24 MB CPU allocation failed. The process list accounted for ~36 GB; the rest of the 66 GB was page file / memory compression / transient allocations. **The real pressure source is the Qwen llama-server, not ComfyUI's models.**

**FIX APPLIED (user):** removed `--lowvram` from the ComfyUI launch script (now: `--windows-standalone-build --reserve-vram 4 --disable-pinned-memory --use-pytorch-cross-attention --cache-none --enable-manager`). Without `--lowvram`, ComfyUI keeps its models in **VRAM** (32 GB free) instead of offloading to CPU RAM, so it no longer competes with the Qwen llama-server for CPU RAM. After restart: system at **66% load / 22.4 GB free**, llama-server 22.3 GB, ComfyUI 1.37 GB. **The MiniMax 7-ref resize (24 MB float32 per image on CPU) now trivially succeeds.**

**Rule: the dominant CPU-RAM consumer is the local Qwen llama-server (~22 GB), NOT ComfyUI. Run ComfyUI WITHOUT `--lowvram` so its models stay in VRAM (32 GB free) and don't compete with Qwen for CPU RAM. If a heavy run still OOMs, the constraint is the llama-server's footprint â€” reduce its context/concurrency, not ComfyUI's. VERIFY RAM consumers with `top_ram.py` before diagnosing â€” do NOT assume which process is holding the RAM.**

### Update 2026-08-30 (Pipeline 1 â€” 2K render VRAM-thrashed â†’ set to 1MP native; render-time baseline)

User: "I think we should have went with 1MP. [log: Model Initializing ... 0/8 [10:15<?, ?it/s] ... Prompt executed in 00:11:31] I had to stop this. Can you check the forums how much time it will take to render a 15 second 2mp REF2 on RTX 5090?"

**Diagnosis (from the user's own log, not forums):** the 2K render **never started sampling** â€” it was stuck at **0/8 steps, "Model Initializing", for 10+ minutes**. That is NOT slow sampling; it is the **~20 GB model (`19995MB Staged`) + 2K video activations thrashing in VRAM** (32 GB card, `--reserve-vram 4`). At 2048Ã—1152 the video latent + activations are so large ComfyUI spends all its time moving the model in/out of VRAM instead of generating. It likely would not have finished in reasonable time.

**Render-time baseline (from the user's OWN machine, not forums):** the 11 `Jaisal_Production_1` outputs were written ~10â€“15 min apart (04:31 â†’ 04:45 â†’ 04:55 â†’ 05:10 â†’ 05:23), so **~10â€“15 min per 0.4 MP render** is the real baseline. Video cost scales with pixels Ã— frames Ã— steps:
- 0.4 MP (864Ã—480): ~10â€“15 min (measured)
- **1.0 MP (1344Ã—768, native): ~25â€“40 min**
- 2.4 MP (2048Ã—1152, 2K): ~60â€“90 min AND VRAM-thrashing (what the user just hit)

The reference video barely adds compute (it's a conditioning input, not a big cost) â€” the cost is **output resolution Ã— 15s Ã— 8 steps**.

**âš ï¸ CORRECTION (2026-09-01) â€” the 25â€“40 min figure is for FULL-attention H3. Our ACTUAL speed stack is SLA, and 1MP generation is UNDER 240 SECONDS.** The user's production workflows (`jaisalproduction1.json`, `jaisal_2mp_test.json`, `beach_sprint_test.json`, `t2v_beach_sprint_test.json`) all wire an **`H3SLAAttention` node (id 150)** from `ComfyUI-PlagueKind-Nodes/ComfyUI-H3-SLA-Attention` (Sparse Linear Attention). Config in use: `widgets_values = [0.9, '32', 8192, 1, True, True, '0', 'comfy_kitchen', True, False, False]` â†’ **sparsity 0.90, dense_backend = `comfy_kitchen_int8`**. With SLA, a 1MP H3 render completes in **< 240 s (~4 min)**, NOT 25â€“40 min. **Do NOT quote the 25â€“40 min estimate for our current pipeline â€” that number is obsolete now that SLA is in the graph.** (The 2K VRAM-thrashing diagnosis above still stands â€” SLA speeds the attention math but does not remove the 2K activation/VRAM pressure.) See **D042**.

**Decision: set the `ResolutionSelector` (node 115) to `['16:9 (Widescreen)', 1.0, 32]` â†’ 1344Ã—768 (MiniMax H3 NATIVE canvas).** 1MP is what the model is designed for, fits comfortably in VRAM, and renders in a finite ~25â€“40 min. For 2K, the clean path is **render at 1MP â†’ upscale** (Topaz/RTX/Hunyuan upscalers are all installed) â€” faster and cleaner than a direct 2K render. The reference video node (149) stays wired as the motion anchor.

**Rule: do NOT render MiniMax H3 at 2K directly on a 32 GB card â€” the ~20 GB model + 2K activations thrash VRAM (stuck at 0/8 steps in "Model Initializing"). Render at the NATIVE 1344Ã—768 (1.0 MP) and upscale to 2K in a separate step. Estimate render time from the user's OWN output timestamps (file mtimes), not forums â€” forums rarely have a clean per-GPU benchmark. A render stuck at 0/8 steps in "Model Initializing" for many minutes = VRAM thrashing, not slow sampling.**

### Update 2026-08-30 (Pipeline 1 â€” added reference VIDEO (motion anchor) + 2K resolution)

User: "I got one output, and I'm okay with it. Can I add it as a reference and render it in 2K so that it follows the same action?" (referring to `Jaisal_Production_1_00011_.mp4`, the most recent good output).

Updated `jaisalproduction1.json` (validated `valid: true`, now 23 nodes):
- **Added a `MiniMaxH3ReferenceVideoLoadStar7` node (id 149)** that loads the good output video as a MOTION anchor. The node scans the `input` dir, so the video was copied to `input\jaisal_prod1_ref.mp4` (from `output\video\Jaisal_Production_1_00011_.mp4`).
- **Wired:** node 149 IMAGE output (slot 0) â†’ link 303 â†’ node 136 `ref_videos.ref_video_0` (slot 9); node 149 AUDIO output (slot 1) â†’ link 304 â†’ node 136 `ref_video_audios.ref_video_audio_0` (slot 10). The 3 reference IMAGES stay (visual anchors); the video adds the motion/action anchor so the new render follows the same action.
- **Set 2K:** the `ResolutionSelector` (node 115) was `['16:9 (Widescreen)', 0.4, 32]` (â‰ˆ864Ã—480). Set to `['16:9 (Widescreen)', 2.4, 32]` â†’ **~2048Ã—1152 (2K)**. The middle widget is MEGAPIXELS (1.0 â‰ˆ 1024Ã—1024); 2.4 MP @ 16:9 = 2048Ã—1152. The MiniMax node width/height accept up to 16384 (step 32), so 2K is valid.
- **`MiniMaxH3ReferenceVideoLoadStar7` widgets:** `[video, max_long_edge, allow_upscale]` = `['jaisal_prod1_ref.mp4', 1344, False]`. `max_long_edge` (default 1344) = the H3-aligned long edge the ref video is fitted to (keeps aspect). `allow_upscale` = False (avoids spending H3 reference tokens on interpolated detail; enable only for structure/motion A/B tests).

**Rule: to make a new MiniMax R2V render FOLLOW THE SAME ACTION as a good output, add a `MiniMaxH3ReferenceVideoLoadStar7` node that loads that output video and wire its IMAGE output to `ref_videos.ref_video_0` (+ AUDIO to `ref_video_audios.ref_video_audio_0`). The node scans the `input` dir, so copy the video there first. The reference images stay as visual anchors; the video is the motion anchor. For 2K, set the `ResolutionSelector` megapixels widget to ~2.4 (16:9 â†’ 2048Ã—1152). A 2K render is ~6Ã— the pixels of the 0.4 MP default, so it's much slower + more VRAM â€” run it when the machine is free (the Qwen llama-server holds ~22 GB CPU RAM).**

### Update 2026-08-30 (Pipeline 1 prompt v10 â€” Shot 1 WIDE ANGLE + Shot 3 climbs then jumps (no hand gestures))

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

### Update 2026-08-30 (Pipeline 1 prompt v9 â€” Shot 3 PREPARES while camera moves, then leaps)

User reviewed Pipeline 1 v8: "the 3rd shot was working fine 3 prompts ago (v5), we need those camera moves, but we have to mention that the 3rd one is NOT a static frame - when it loads he has to do some action, like shaking head or some hand gestures while the camera is moving, and then he can jump, so while the camera is moving he can prepare also, so that feels more natural. The rule should be: where he is moving and what he is doing - we don't want him to run back and forth. Explain it cleanly. I want to get it done, it's been 8 hours."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Shot 3 camera moves RESTORED to v5** (the user said v5's shot 3 was working fine): SIDE view from the VIEWER'S LEFT, boy on viewer's left, camera ANCHORED on viewer's left + TRACKS him (NOT a left-to-right sweep), swings to his BACK as he leaps, ENDS at his back mid-air BEFORE the water.
- **Shot 3 is NOT a static frame:** "The boy is NOT standing still - while the camera moves, he is PREPARING to jump: he shakes his head, makes hand gestures, and gets ready. Then the boy LEAPS over the low handrail." (This replaces v8's "ALREADY RUNNING and IN MOTION at the start" which was over-constraining and breaking the shot.)
- **<Picture 3> definition** updated: "the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, **preparing to jump over the handrail**" (was "already running toward the handrail").
- **summary** updated: "then prepares and leaps over the handrail" (was "then runs toward the handrail and leaps over it").
- **overall_soundscape** updated: "a rising tension as the boy prepares and leaps" (was "runs and leaps").
- **CLEAN RULE (user's):** state WHERE the boy is moving and WHAT he is doing - do NOT have him run back and forth. Shot 3: he is at the middle of the bridge, facing the handrail (toward the river), PREPARING (shaking head, hand gestures) while the camera moves, then LEAPS. One direction, one action, no back-and-forth.
- RAIN still enforced in every shot (unchanged). Timing still 4/6/5 (00:00.000 / 00:04.000 / 00:10.000).

**Rule: when a shot keeps breaking under over-constraint, GO BACK to the last version that worked (v5's shot 3 camera moves) and add ONLY the one missing element (the boy is NOT static - he PREPARES: shakes head, hand gestures, while the camera moves, then leaps). The rule for describing motion is: state WHERE the subject is and WHAT he is doing in ONE direction - do NOT have him run back and forth. A "preparing" action (head shake, hand gestures) while the camera moves feels more natural than a static frame AND is less likely to break than a full runâ†’crouchâ†’plantâ†’leap chain.**

### Update 2026-08-30 (Pipeline 1 prompt v8 â€” timing 4/6/5 + Shot 3 starts IN MOTION)

User reviewed Pipeline 1 v7: "(1) [Shot 1] should have 4 seconds, (2) [Shot 2] we can extend till 10 where we have proper direction, (3) [Shot 3] the same issue came back - the starting frame is standing still, we should not do that."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Timing:** [Shot 1] = **4s** (00:00.000), [Shot 2] = **6s** (00:04.000 â†’ 00:10.000, "proper direction" = the turn is clear and deliberate, body rotates fully toward the VIEWER'S LEFT), [Shot 3] = **5s** (00:10.000). Total = 15s (length node 132 stays 15).
- **Shot 3 starts IN MOTION:** "The boy is ALREADY RUNNING and IN MOTION at the start of this shot - he is NOT standing still, he is moving toward the handrail with momentum." Then he runs toward the handrail, crouches, plants, and LEAPS. (The v7 issue: the starting frame was standing still.)
- **<Picture 3> definition** updated: "the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, **already running toward the handrail**" (was "about to climb over the handrail and leap").
- **summary** updated: "then runs toward the handrail and leaps over it" (was "then climbs over the handrail and JUMPS").
- **overall_soundscape** updated: "a rising tension as the boy runs and leaps" (was "climbs and leaps").
- RAIN still enforced in every shot (unchanged from v7).

**Rule: when a shot's STARTING FRAME comes out standing still, say explicitly "the boy is ALREADY RUNNING and IN MOTION at the start of this shot - he is NOT standing still" AND update the <Picture N> definition to describe the in-motion pose ("already running toward the handrail") - the reference frame anchor + the explicit in-motion line together prevent a static opening. And when the user gives a timing split (4/6/5), set the [Shot N] timestamps to match (00:00.000 / 00:04.000 / 00:10.000) and keep the length node = the total (15s).**

### Update 2026-08-30 (Pipeline 1 prompt v7 â€” SIMPLIFIED + RAIN enforced in every shot + Shot 3 ends mid-air)

User reviewed Pipeline 1 v6: "the first clip had a lot of issues, the hard rule didn't apply well, check out the H3 prompt guide, let's clear out the confusion and keep it simple. (1) Shot 1 should focus on the CLIMATE and MOOD, the kid is WALKING / SLOWLY RUNNING. (2) Shot 2 is fine. (3) Shot 3 is fine BUT we do NOT want to show the kid jumping TO the water - the jump and the cut should happen AFTER the jump, we don't need to show till he reaches the water, and the bridge has HEIGHT - do not treat this as a swimming pool. (4) IMPORTANT: none of them has RAIN in it - we should enforce MiniMax to add RAINING."

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **SIMPLIFIED** the whole prompt (removed the heavy CHARACTER COUNT block + the over-stuffed negative constraints that "didn't apply well"). Kept the 6-section structure per the H3 guide. Kept the ORIENTATION block (boy's right = viewer's left).
- **Shot 1:** now focuses on the CLIMATE and MOOD - the boy WALKS and SLOWLY RUNS (natural gait, feet lift+land separately, NOT a slide), MAIN PURPOSE = ESTABLISH THE CLIMATE AND MOOD (sky clearâ†’moody, RAIN BEGINS TO FALL and builds, landscape shifting). Fixed wide static camera.
- **Shot 2:** UNCHANGED (user: "the second one is fine").
- **Shot 3:** the boy crouches â†’ plants â†’ LEAPS over the handrail, fully airborne. **The bridge is TALL - a real leap from height over the wide river, NOT a shallow pool.** The shot ENDS with the camera at his BACK as he is in the air, **BEFORE he reaches the water** - the cut happens right here so the next clip picks up the jump. (Removed the "DIVE into the river / SPLASH" - we do NOT show him reaching the water.)
- **RAIN enforced in EVERY shot:** "RAIN is present in EVERY shot - rain is falling in [Shot 1], [Shot 2], and [Shot 3]" (detailed_description global line) + "RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3])" (overall_soundscape). Shot 1 = rain BEGINS and builds; Shot 2 = rain streaks visible; Shot 3 = HEAVY RAIN.

**Rule: when a hard rule "doesn't apply well", SIMPLIFY - over-stuffed negative constraints (a whole CHARACTER COUNT block + many NOT-clauses) dilute the signal. Keep the 6-section structure, state the key requirement once clearly per shot, and ENFORCE the global element (RAIN) in BOTH the detailed_description global line AND the overall_soundscape so MiniMax can't drop it. For a jump that must NOT show the landing: end the shot mid-air BEFORE the water and say the bridge is TALL (a real leap from height, NOT a shallow pool) - the cut happens at the apex so the next clip picks up the jump.**

### Update 2026-08-30 (Pipeline 1 prompt v6 â€” ONLY ONE character + Shot 3 JUMP made explicit)

User reviewed Pipeline 1 v5: (1) **Shot 1 had 2 characters** â€” MiniMax duplicated the boy; need a HARD demand that there is ONLY ONE character. (2) **Shot 2 is fine** â€” keep as is. (3) **Shot 3 is fine on camera angle but the JUMP didn't happen** â€” the boy climbed but never actually jumped; need more detail so it speeds up and the leap actually occurs.

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Added a CHARACTER COUNT block** (new section): "There is ONLY ONE character in the entire video - the single young schoolboy <Subject 1>. There are NO other people, NO second boy, NO duplicates, NO extra figures, NO crowds, NO bystanders, NO reflections of a second person. Every shot shows exactly ONE boy and only that boy." Also added to summary, retention_analysis ("ALWAYS exactly ONE boy - never two, never a duplicate"), the detailed_description global line, and the [Shot 1] line ("ONLY ONE boy ... NO second person, NO duplicate, NO other figure anywhere in the frame").
- **Shot 2 UNCHANGED** (user: "second one is fine").
- **Shot 3 JUMP made explicit + sped up:** the boy "moves QUICKLY and with PURPOSE - he crouches, plants his feet, and then JUMPS: he LEAPS over the low handrail and DIVES into the river, his body fully airborne, arms out, a clear dynamic leap (NOT just climbing, NOT just standing, NOT just walking - he MUST actually JUMP and go over the handrail into the water)." Camera angle kept correct (SIDE view from viewer's left, anchored + tracks, swings to his back). summary + detailed_description now say "[Shot 3] MUST show the boy JUMPING into the river".
- **Sound:** added "a big SPLASH as he JUMPS into the river" to overall_soundscape.

**Rule: MiniMax DUPLICATES the character (a 2nd boy) unless you HARD-DEMAND "ONLY ONE character, no duplicates, no second figure" in a dedicated block + summary + retention + the wide-shot line (the wide shot is where a duplicate is most visible). And a JUMP/leap will NOT happen from a vague "climbs and leaps" â€” you must spell out the physical action (crouch â†’ plant â†’ LEAP over the handrail â†’ DIVE into the water, fully airborne) and forbid the failure modes ("NOT just climbing, NOT just standing, NOT just walking"). If the action still doesn't happen, add a reference frame that already shows the airborne pose.**

### Update 2026-08-30 (Pipeline 1 prompt v5 â€” left/right orientation fix + sound + sliding)

User reviewed Pipeline 1 v4: (1) **Sound is bad in the first sequence** â€” needs to clearly convey **running footsteps + a building thunderstorm** (thunder rumbles, heavy rain). (2) **The left/right was wrong** â€” "when I say he is moving right I meant HIS right (the VIEWER'S LEFT), and that's how our 3rd portion starts." (3) **Shot 3 camera angle is confusing** â€” it was sweeping **left-to-right**; the user wants it **anchored on the VIEWER'S LEFT** (where the boy is after turning), tracking him, NOT sweeping across.

Updated `jaisalproduction1.json` node 138 (validated `valid: true`):
- **Added an ORIENTATION block** (new section after subject_definitions): "The boy's RIGHT side is the VIEWER'S LEFT side of the frame. When the boy turns toward his right, he turns toward the VIEWER'S LEFT. [Shot 3] is a side view from the VIEWER'S LEFT side, and the boy is on the VIEWER'S LEFT of the frame." + "All left/right references use the VIEWER's perspective" in the detailed_description global line.
- **Shot 2:** the boy turns toward **HIS RIGHT = the VIEWER'S LEFT** (toward the river).
- **Shot 3:** now a **SIDE view from the VIEWER'S LEFT**, boy on the VIEWER'S LEFT of the frame; the camera is **anchored on the VIEWER'S LEFT and TRACKS the boy (does NOT sweep left-to-right)** as he climbs, then swings to his BACK as he jumps.
- **Shot 1 sliding:** even more forceful â€” "a REAL running gait - each foot clearly LIFTS and LANDS separately, visible leg movement, one step at a time (NOT a smooth slide, NOT a glide, NOT a blur, NOT a keyframe slide, NOT fast)".
- **Sound (overall_soundscape):** "Clear running footsteps on the stone bridge, heavy rain, a building thunderstorm with distant thunder rumbles, splashing water on the bridge stones, then a rising tension as the boy climbs and leaps."

**Rule: ALWAYS specify left/right from the VIEWER's perspective in R2V prompts (the boy's right = the viewer's left) â€” ambiguous "his right" makes MiniMax pick the wrong side. Anchor the camera to a fixed side (the viewer's left) and say it TRACKS the subject rather than "moves across" (which reads as a left-to-right sweep). And name the exact sounds you want (running footsteps + thunderstorm rumbles) in overall_soundscape â€” a vague "wind building" gives muddy audio.**

### Update 2026-08-30 (Pipeline 1 prompt v4 â€” wide shot as a HARD demand + slow run + climate change)

User: "make sure the wide shot is also a hard demand and the kid has to slowly run, but that shot should establish the climate change." Updated `jaisalproduction1.json` node 138 (validated `valid: true`): (1) the **wide shot is now a HARD REQUIREMENT** â€” added to the summary ("[Shot 1] MUST be a LONG WIDE establishing shot that shows the landscape and the climate change") and the detailed_description global line ("[Shot 1] MUST be a LONG WIDE establishing shot (a hard requirement - it must NOT be cut short, NOT turned into a close-up, NOT skipped)"), and the Shot 1 line itself ("a HARD REQUIREMENT - the camera does NOT move closer, does NOT push in, does NOT cut to a close-up - it stays a FIXED wide view the whole time"). (2) **Slow running** reinforced: "runs SLOWLY and DELIBERATELY... (NOT rushing, NOT sliding, NOT a blur, NOT fast)". (3) **Climate change is the shot's MAIN PURPOSE**: "The MAIN PURPOSE of this shot is to ESTABLISH THE CLIMATE CHANGE - the sky gradually darkens from clear to moody overcast, the wind picks up, and rain begins to fall, the whole landscape and environment shifting from clear to rainy." **Rule: when a shot has a specific job (establish the climate, hold the wide), state it as a HARD REQUIREMENT in BOTH the summary and the per-shot line, and explicitly forbid the failure modes (cut short / turned into a close-up / skipped) â€” MiniMax needs the negative constraints to hold the shot.**

### Update 2026-08-30 (Pipeline 1 prompt v3 â€” fixed wide shot 1, stop/turn-right shot 2, sideâ†’acrossâ†’back shot 3)

User reviewed Pipeline 1 v2: (1) **Shot 1** must be a **LONG WIDE STATIC shot** (camera does NOT move closer / NOT push in) â€” the whole purpose is to show the **landscape + sky slowly changing mood**, boy runs slowly, **5s**. (2) **Shot 2:** boy runs, stops, **looks toward his RIGHT side** (toward the river), **5s** for running + stopping + turning. (3) **Shot 3 "completely gone from the sequence, didn't appear, camera movement not showing"** â†’ new choreography: **SIDE view (his right) â†’ camera MOVES ACROSS (tracking) as he climbs over the handrail â†’ camera swings to his BACK side as he jumps**, ENDS at his back mid-leap. **CRITICAL FIX: MiniMax DROPPED Shot 3 entirely** (it compressed the sequence and skipped the last shot). Added strong emphasis to the prompt: "ALL THREE shots must appear in this order, each getting its full time - do not skip, compress, or drop any shot, especially [Shot 3]" (in summary + detailed_description). **Rule: MiniMax will DROP the last shot of a multi-shot R2V if the prompt doesn't explicitly demand all shots appear â€” add a hard "ALL N shots must appear, do not skip/compress/drop any" line. Also: a wide establishing shot's purpose is the LANDSCAPE + sky change, so keep the camera FIXED (no push-in) and let the environment shift; and specify the camera's exact path for the jump shot (side â†’ tracking across â†’ back side) rather than a vague "camera rotates".**

### Update 2026-08-30 (Pipeline 1 prompt v2 â€” slow running + stop/turn/pan + in-motion shot 3)

User reviewed `jaisalproduction1.json` (Pipeline 1 only â€” Pipeline 2 not yet tried): (1) **Shot 1 (7s)** the boy "rushing, doesn't feel like running, felt like sliding a keyframe, not real" â†’ now **SLOW, DELIBERATE, step-by-step** running: "each step clearly visible, one foot at a time, feet landing one after the other in a clear step-by-step rhythm (NOT rushing, NOT a fast blur, NOT sliding, NOT a smooth glide - real running with distinct steps)". (2) **Shot 2 (3s)** was good/matching pace â†’ kept, but added at the end: the boy **SLOWS and STOPS, then TURNS toward the river, and the camera PANS to follow him** into the next view (the user's "stop and turn, then pan to Picture 3" idea â€” motivates the cut). (3) **Shot 3 (5s)** was the worst â€” "static, standing still for 2s while camera tilts" â†’ now the boy is **IN MOTION the whole time**: "just stopped and turned toward the river, looks down at the water, takes a few steps toward the edge, crouches, and gathers himself to leap... NEVER standing still - every moment he is doing something (turning, stepping, looking down, crouching)". Kept the camera-rotate structure the user liked. **Rule: MiniMax makes running look like a "sliding keyframe" if you just say "runs" â€” specify SLOW + step-by-step + distinct footfalls. And a shot that opens on a static standing figure reads as dead â€” keep the character in motion from the first frame (turning/stepping/looking), and bridge the cut with a stop+turn+pan so the next shot's first frame is motivated.**

### Update 2026-08-30 (2-pipeline production split â€” `jaisalproduction1.json` + `jaisalproduction2.json`)

User: the full sequence should be ~25s (not 15s) with better rhythm â€” wide run-up 7s, close-up 3s, gather/climb/push-off 5s (15s run-up), then jump + drown 5-6s + title 4s. **Decision: split into TWO separate MiniMax R2V generations** (shorter clips = less style drift, cleaner 3-ref mapping, the jump is a natural splice point, re-run only the bad segment). Shot 3 (running medium) REMOVED entirely.

**Built two workflows** (both validated `valid: true`, 22 nodes):
- **`jaisalproduction1.json`** (run-up, **15s**, save `video/Jaisal_Production_1`): refs `jaisal_1_longshot` (ref_image_0), `jaisal_2_closeup` (ref_image_1), `jaisal_4_middle` (ref_image_2). Shots: (1) wide, boy RUNS ~7s, sky darkens clearâ†’moody, rain begins, static wide â†’ slow push-in; (2) close-up, boy RUNS (NOT static), camera tracks, wind + rain ~3s; (3) SIDE view at middle in HEAVY RAIN, crouches + gathers, camera ROTATES, climbs over low handrail, pushes off toward river, ENDS mid-launch ~5s.
- **`jaisalproduction2.json`** (leap + title, **11s**, save `video/Jaisal_Production_2`): refs `jaisal_5_jump` (ref_image_0), `jaisal_6_underwater` (ref_image_1), `jaisal_7_title` (ref_image_2). Shots: (1) SHORT natural leap CLOSE to bridge (NOT a long throw / stone) ~2s; (2) underwater, sinks completely down, rising bubbles ~4.5s; (3) title card, bubbles foam up, 'The Jaisal Cut' slowly becomes visible, color grade EXACTLY matches shot 2 ~4s.
- **Both prompts lock a consistent color grade** (same dark moody palette / dim grey light / water color across all shots) to minimize the two-generation seam.
- **Splice:** cut at the push-off moment (pipeline 1 ends mid-launch, pipeline 2 starts in-air), HARD CUT not crossfade, color-match the splice frame in post.
- **Build script:** `d:\models\vsCodeMcp\utilities\build_production_pipelines.py` (copies `jaisal_lowangle.json`, keeps 3 LoadImage nodes per pipeline, rebuilds node 136 to 3 ref slots, new links 300-302, sets length + save prefix + prompt).
- **Rule: for a long cinematic sequence, split into 2-3 shorter R2V generations at natural action splice points (push-off â†’ in-air) rather than one long run â€” less drift, cleaner refs, easier re-runs. Join in a video editor with a hard cut + color match.**

### Update 2026-08-30 (7-shot MiniMax R2V â€” `jaisal_lowangle.json`)

User: "now lets go to minimax... we have 7 images... first one is a long shot (add running + climate change), 2nd close-up (camera movement + wind), 3rd running (motion + camera + wind), 4th kid standing middle full figure (ADD rain), 5th wide low-angle jump (complete the motion into the river), 6th underwater (move kid completely down), 7th title. All transitions smooth and organic. NOTE: the picture added as 1 can be reference image 0 in the node and it can mess up the prompt if we add picture 1 in prompt â€” so let's not make that mistake. This is a multi-billion-dollar company's production animation â€” a cinematic masterpiece intro."

**Built `jaisal_lowangle.json` as a 7-shot R2V** (validated `valid: true`, 26 nodes):
- **7 LoadImage nodes** (137, 139, 147, 148, 149, 150, 151) â†’ `MiniMaxH3ReferenceToVideo` (136) `ref_image_0`..`ref_image_6`. Images copied to `input\` as `jaisal_1_longshot.png` â€¦ `jaisal_7_title.png`.
- **CRITICAL (user's note):** the `<Picture N>` tags map 1-to-1 to `ref_image_N` IN CONNECTION ORDER â€” `<Picture 1>` = `ref_image_0` = image 1 (long shot), etc. This is the correct pattern (each reference is a frame anchor for its shot), NOT a mistake. The old 2-ref workflow's "mess up" concern was about a single reference being both the style anchor AND the first frame; here each of the 7 references is its own shot's first frame, so the mapping is clean.
- **Prompt (node 138):** 7-shot R2V structure (subject_definitions / summary / retention_analysis / detailed_description with timed `[Shot N] At MM:SS.mmm` blocks / overall_soundscape / non_diegetic_music). Each shot: (1) long shot â€” boy runs, sky darkens clearâ†’moody, wind + rain begins, static wide â†’ slow push-in; (2) close-up â€” gentle camera push-in/drift + wind in hair/shirt; (3) running â€” camera tracks alongside at running pace, wind + rain + splashes; (4) middle full figure â€” ADD heavy rain, steady camera with subtle drift; (5) wide low-angle jump â€” camera completes his motion into the river, big splash; (6) underwater â€” camera follows him sinking completely down, rising bubbles; (7) title â€” calm dark water, bubble-formed 'The Jaisal Cut' title held steady. **All transitions smooth and organic.**
- **Bag color FIXED:** prompt now says **BLACK school bag** (was "red school bag" â€” the pending fix from earlier).
- **Title:** shown in Shot 7 (the title reference image), NOT rendered as a text overlay by the model.
- **Build script:** `d:\models\vsCodeMcp\utilities\build_minimax_7shot.py` (copies images, grows node 136 to 7 ref slots, shifts downstream link slots promptâ†’13/widthâ†’14/heightâ†’15/lengthâ†’16, adds links 289-294).

### Update 2026-08-30 (size hierarchy: The < Cut < Jaisal)

User asked for a **size hierarchy** in the title: **"The" = SMALL, "Jaisal" = BIG (the hero word, largest), "Cut" = MEDIUM** (between the two). Prompt 10 positive now states the hierarchy explicitly: "the title words sized in a clear hierarchy - the word 'The' SMALL, the word 'Jaisal' BIG and dominant (the largest word, the hero of the title), the word 'Cut' MEDIUM (between the two)". **Tuning:** 'Jaisal' not big enough â†’ strengthen it ("'Jaisal' MUCH larger than the other words, the clear focal point"); hierarchy lost (all words same size) â†’ restate more forcefully and/or lower denoise a touch so the layout is followed more faithfully.
---

## D027 - Title animation = 2D VECTOR / LINE-ART stick figure (not cartoon/3D), MEDIUM shots only

Date: 2026-08-31
Status: Active

### Decision

The title animation is a **2D vector / line-art** piece â€” a **stick figure** (round head + line body + line arms + line legs, clean confident line work, lines only, NO shading, NO 3D, NO cartoon shading). Story: the stick figure **walks slowly** on the bridge â†’ **throws a paper plane** into the river â†’ **jumps into the river** after the paper plane â†’ the paper plane is **still flying** as the title **"The Jaisal Cut"** appears. Simple, funny, **no special effects**. **MEDIUM SHOTS ONLY** (the figure's full body visible) â€” **NO wide shots**, NO extreme close-ups.

### Reason

The user wants a simple vector/line look ("just with lines and everything", "a stick with a head and hand and legs"), not the cartoon/2D brush-stroke style. The paper-plane gag makes it funny. Medium shots keep the figure readable. The line-art look is carried by the **`krea2_lineart_v1_fp16.safetensors`** LoRA (Civitai "Krea2 Line Art Style", downloaded 2026-08-31, 56 MB, in the main loras path).

### Alternatives considered

- Cartoon/2D brush-stroke style (rejected â€” user wants pure lines).
- Wide establishing shots (rejected â€” user: "lets not keep any wide shots, medium shots are fine").
- Other Civitai sketch/vector LoRAs (`SimpleFineVector_Krea2_v1`, `krea2_coloringbook_v1`, `friendlysketch-v2_krea2`) â€” found but the Civitai download hit a Cloudflare challenge page (10 KB HTML); only `krea2_lineart_v1_fp16` downloaded cleanly. Re-download the others if the line-art LoRA isn't clean enough.

### Result

`d:\models\vsCodeMcp\prompts\jaisal_sketch_prompts.txt` created â€” 4 ready-to-paste Krea2 t2i prompts (walk / throw paper plane / jump / title) + shared style prefix + shared negative (excludes 3D/shading/color-fill/carton/wide-shot/close-up) + a full MiniMax H3 R2V prompt (4 refs, 4 shots, 4s each, 16s). **Rule: the title animation is a 2D vector line-art stick figure, medium shots only, paper-plane gag, no special effects. Use the `krea2_lineart_v1_fp16` LoRA @ 1.0.** See `jaisal_sketch_prompts.txt`.

### Production pipeline note (2026-08-31)

The production workflow renders at **1MP (1344Ã—768, native) and is UPSCALED to 2MP** â€” we do NOT generate 2MP video directly (VRAM thrashing on the 32 GB card). Upscale path: `RTXVideoSuperResolution` (2Ã— ULTRA) or `TopazVideoEnhance` (Starlight 1080p/4K) inserted between `CreateVideo` and `SaveVideo`.

---

## D028 - MiniMax R2V prompts use standard cinematography vocabulary (shot size + angle + movement + focus per shot)

Date: 2026-08-31
Status: Active

### Decision

Every MiniMax H3 R2V `[Shot N]` line names the **shot size + camera angle + camera movement + focus** EXPLICITLY using standard cinematography terms (e.g. "a static eye-level MEDIUM shot, deep focus", "a slow tracking shot from the side", "a low-angle shot looking up"). The full vocabulary (shot size / framing / focus / angle / movement / mechanism, each with a ready-to-paste phrase) is saved at `d:\models\vsCodeMcp\docs\CAMERA_SHOT_VOCABULARY.md` (sourced from the StudioBinder "50+ Types of Camera Shots, Angles, and Techniques" guide).

### Reason

MiniMax responds to standard cinematography vocabulary far better than vague words like "the camera moves" or "a nice angle". Naming the exact shot size + angle + movement + focus per shot gives much tighter shot control. The Jaisal Cut title animation uses MEDIUM shots only, static camera (low-angle for the jump), deep focus.

### Alternatives considered

- Vague camera descriptions (rejected â€” weak shot control).
- Naming real camera gear (tripod/dolly/drone) in a 2D line-art prompt (rejected â€” can confuse the model; for 2D animation just say "static" or "smooth tracking").

### Result

`CAMERA_SHOT_VOCABULARY.md` created (complete cheatsheet + ready-to-paste phrases). The Jaisal Cut title-animation MiniMax prompt (`jaisal_sketch_prompts.txt`) rewritten to the user's exact sequence (walk â†’ stop â†’ look around both sides â†’ whistle â†’ jump â†’ title) using the camera vocabulary. **Rule: name shot size + angle + movement + focus explicitly for every [Shot N]; keep the vocabulary cheatsheet handy for reuse.**

## D029 - H3 camera-correction problem: force the angle with top-priority constraints + accept distortion + forbid the camera cheat

Date: 2026-08-31
Status: Active

### Decision

H3 has a strong internal prior to "correct" the camera toward a flattering eye-level view (especially with a face in frame). To force a specific camera angle, the prompt MUST: (1) put the camera constraint at the **absolute top** as a `MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: ...` line naming the exact angle (H3 weights the first lines most â€” a buried camera instruction is treated as background and ignored); (2) **explicitly accept the natural distortion** that angle causes ("ACCEPT NATURAL [ANGLE] PERSPECTIVE DISTORTION") so the face-enhancement tendency doesn't "fix" it by moving the camera; (3) **explicitly forbid moving the camera to fix the subject** ("DO NOT CORRECT CAMERA TO EYE-LEVEL TO FIX [SUBJECT] PROPORTION", "DO NOT auto-adjust camera perspective", "REJECT flat eye-level frontal camera"); (4) use **short hard negative commands** ("NO eye-level shot", "NO camera at face height", "FORBIDDEN: flat frontal camera") â€” long explanatory reasoning is less reliable than short `DO NOT`/`NO`/`FORBIDDEN` prohibitions; (5) **keep the reference's identity but discard its camera** ("COMPLETELY DISCARD <Picture N> original camera angle, framing, background, lighting, and pose") so the reference doesn't drag the camera back. For a STATIC shot, the lock is the inverse: "the camera is locked and does NOT move, does NOT push in, does NOT drift, does NOT tilt, does NOT pan, does NOT zoom." Also **be specific about what the subject does AND does not** â€” list the concrete action chain in order + an explicit NOT-list ("does NOT run, does NOT jump yet, is NOT duplicated").

### Reason

The user's high-overhead camera workflow (a 45-55Â° high-down overhead shot) kept failing because H3 silently moved the camera back to eye level to make the face look better (the cheat: camera stays eye-level, subject just tilts the head up). The fix is to lock the camera with top-priority constraints, accept the natural high-angle face distortion, and explicitly forbid the camera cheat. The same discipline applies to ANY forced angle (overhead, low-angle, static).

### Alternatives considered

- Burying the camera instruction in the middle of the prompt (rejected â€” H3 treats it as background and ignores it).
- Long explanatory reasoning about the camera (rejected â€” less reliable than short hard prohibitions).
- Letting the reference image set the camera (rejected â€” it drags the camera back to the reference's original angle).

### Result

Added a "Forcing a specific camera angle (the H3 camera-correction problem)" section to `docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md` (the 5 rules + a reusable camera-lock block). Rewrote BOTH title-animation prompts with this discipline: (1) the R2V prompt in `jaisal_sketch_prompts.txt` (top MANDATORY camera constraint + a GLOBAL CAMERA LOCK section + per-shot camera locks + per-shot action chains + NOT-lists); (2) the single-shot i2v prompt in `jaisal_single_shot.json` (nodes 105 + internal 104, validated `valid: true`). **Rule: to force a camera angle in H3, put the constraint at the top, accept the natural distortion, forbid the camera cheat with short hard negatives, discard the reference's camera, and give the subject an explicit action chain + NOT-list.** See D028 (cinematography vocabulary) for the shot-size/angle/movement/focus terms.

---

## D030 â€” Sketch title animation: B&W lock, plane stays small + in-air until 12s, wind, bubbles

Date: 2026-08-31
Status: Active

### Decision

The 2D vector line-art title animation (single-shot i2v, `jaisal_single_shot.json`) is updated with five hard rules after the first paper-plane run came out wrong:
1. **STRICTLY BLACK AND WHITE** â€” black ink lines on a pure white background ONLY, no color/grey/shading/warm tones (top-priority lock).
2. **BACKGROUND LOCK ACROSS ALL 15 SECONDS** â€” the pure white void is UNCHANGED and IDENTICAL from 0.00 to 15.00; explicitly forbid background change/shift/morph/new elements (the background was changing mid-video, around the 10s mark).
3. **PAPER PLANE SIZE LOCK** â€” the plane stays SMALL the whole time; never grows, never fills the screen, never huge (it was coming out huge after the throw).
4. **PAPER PLANE IN THE AIR UNTIL 12.00 SECONDS** â€” the plane stays flying/drifting in the AIR from the throw until 12.00s; it does NOT touch/float/land on the water before 12.00s; only floats on the water from 12.00s onward (it was floating on the water immediately).
5. **VISIBLE WIND** â€” line-art wind lines show the wind blowing throughout every second (the run felt windless).
Plus: after the figure sinks/drowns, a few small line-art bubbles rise in that area.

### Reason

User review of the first paper-plane run: (a) background still coming in / changing mid-video, (b) the paper plane huge after the throw, (c) the plane floating in the water instead of the air, (d) no visible wind, (e) wanted bubbles after the kid drowns.

### Alternatives considered

- Letting the plane fill the screen for the title (rejected â€” the user wants the plane to stay small; the title is composited in post per D004).
- A single "plain white" background line (rejected â€” not enough; must explicitly forbid the change/shift/morph family AND state the background is IDENTICAL across all seconds).

### Result

New prompt saved to `prompts/jaisal_single_shot_prompt_v2.txt` and applied to BOTH `jaisal_single_shot.json` instance node 105 (`widgets_values[0]` + `widgets_values_named['prompt']`) AND internal subgraph node 104 (D019 rule). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120). The R2V fallback prompt in `prompts/jaisal_sketch_prompts.txt` was updated to the SAME rules (B&W lock, background-identical-across-shots, plane small + in-air until 12.00s, wind lines, bubbles after sinking, title composited in post NOT rendered). **Rule: for the line-art title animation â€” strictly B&W, background IDENTICAL across all seconds, plane stays SMALL and IN THE AIR until 12.00s then floats on water, visible wind lines throughout, bubbles after the figure sinks.**


---

## D031 â€” Sketch title animation: 15s â†’ 10s (background-change mitigation)

Date: 2026-08-31
Status: Active

### Decision

The single-shot i2v title animation (`jaisal_single_shot.json`) is now **10 seconds** (was 15s). The user reported the SAME background issue persisted after the v2 prompt (D030), and asked to shorten to 10s "that might fix this". The background issue is flagged as something to CHECK on (see below).

### What changed

1. **Length 15s â†’ 10s** on BOTH nodes:
   - Instance node 105 `value_1` (length in SECONDS) = **10** (positional index 3).
   - Internal subgraph node 104 `length` (frame count at 24 fps, 17k+5 grid) = **243** (= 17Ã—14+5 = ~10.1s; was a stale 73 = ~3s). Per D019 the converter reads the internal node, so both were set to be safe.
2. **Prompt compressed to a 10-second timeline** (saved to `prompts/jaisal_single_shot_prompt_v3_10s.txt`, applied to both nodes' `widgets_values[0]` + `widgets_values_named['prompt']`):
   - 10 per-second parts (0.00-1.00 â€¦ 9.00-10.00).
   - Paper plane now stays IN THE AIR until **9.00 seconds** (was 12.00s), then floats on the water in the final second (9.00-10.00).
   - The jump (7.00-8.00) + fall (8.00-9.00) + land/sink/bubbles + plane-lands-on-water are all compressed into the final 3 seconds.
   - All D030 rules retained: strictly B&W, background IDENTICAL across all 10 seconds, plane stays SMALL, visible wind lines, bubbles after the figure sinks.
3. Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Reason

User: "same issue, lets do this for 10 seconds, that might fix this, the background issue is something we should check on". Shorter timeline = less room for the background to drift/change mid-video.

### Background issue â€” CHECK ON (open)

The background (pure white void) keeps changing/coming in mid-video despite the BACKGROUND LOCK. Hypotheses to investigate:
- **The reference image itself** (`input\sketch_1_walk.png`) may have a non-pure-white background (cream/paper tone) that the model drifts toward â€” check the actual reference image's background color.
- **The i2v model's prior** may add a subtle environment over time even with a white reference â€” a shorter clip (10s) reduces the drift window.
- **The `length` widget** on the internal node was stale (73 frames = ~3s) while the instance said 15s â€” now synced to 243 frames (~10s); verify the actual output duration matches 10s after the next run.

### Alternatives considered

- Keeping 15s with an even stronger background lock (rejected â€” the user explicitly chose 10s as the mitigation).
- Splitting into 2 shorter i2v runs (deferred â€” try the 10s single take first).

### Result

`jaisal_single_shot.json` is now a 10s single take. **NEXT: run it and (a) confirm the output is ~10s, (b) check whether the background stays pure white across the whole clip, (c) check the reference image's background color if it still drifts.**


---

## D032 â€” Sketch title animation: pure-white void â†’ minimal WATERCOLOR scene (overlay fix) + ONE plane + NO bubbles

Date: 2026-08-31
Status: Active

### Decision

The single-shot i2v title animation (`jaisal_single_shot.json`) prompt is changed from a **pure white void** background to a **FIXED MINIMAL WATERCOLOR SCENE** (a simple stone bridge over a river, soft pale blue-grey sky, soft muted blue river, soft muted green bank with a couple of simple line trees). The scene is COLORED (not pure white) and is the SAME fixed scene across all 10 seconds. Two more fixes: **ONLY ONE paper plane** (never two) and **NO bubbles** anywhere.

### Reason

User review of the v3 (10s, pure-white) run: (a) the **wooden overlay is STILL present** â€” the user's insight: a pure white void is unnatural, so the model hallucinates an overlay (wooden table/floor) to fill the "empty" space. Giving it a **consistent colored watercolor scene** gives it something to hold onto instead of inventing an overlay. (b) the model **threw TWO paper planes** â€” now locked to ONLY ONE. (c) the **bubbles were too high and too many** â€” removed entirely (only a small splash when the figure enters the water).

### What changed (prompt v4, saved to `prompts/jaisal_single_shot_prompt_v4_watercolor.txt`)

1. **STYLE** changed from "strictly BLACK AND WHITE" to "2D line-art + minimal watercolor" â€” clean black ink lines for the figure/bridge + SOFT MINIMAL WATERCOLOR COLOR WASHES for the scene (soft muted colors, flat 2D, no heavy shading/3d/photorealistic).
2. **BACKGROUND SCENE LOCK** (replaces the pure-white void): a FIXED MINIMAL WATERCOLOR SCENE â€” stone bridge over a river, soft pale blue-grey sky, soft muted blue river, soft muted green bank + a couple of simple line trees. The SAME fixed scene across all 10 seconds. Explicitly forbids background change/shift/morph/new scene/wooden overlay/room/wall/table/indoor setting.
3. **PAPER PLANE - ONLY ONE** (new top-priority lock): there is ONLY ONE paper plane in the whole video, NEVER two, NEVER a second plane, NEVER multiple. The figure throws ONE plane and only that ONE exists.
4. **NO BUBBLES** (new top-priority lock): NO air bubbles, NO rising bubbles, NO bubble clusters, NO bubble pops, NO bubble-formed anything. When the figure enters the water there is only a small splash (a few line-art splash lines), NO bubbles.
5. Retained from v3: 10-second timeline, paper plane stays SMALL + IN THE AIR until 9.00s then floats on the water, visible wind lines, static eye-level MEDIUM camera, deep focus, the figure NOT-list.

### Note on the file shape

The ComfyUI UI re-saved `jaisal_single_shot.json` between turns (native shape: all `widgets_values` are STRINGS, `widgets_values_named` stripped). The v4 prompt was written to the POSITIONAL `widgets_values[0]` on BOTH instance node 105 AND internal subgraph node 104 (105==104 verified). Node 104's `length` was reset to a stale `73` by the re-save and was re-set to `243` (~10s). Node 105's length stays `10` (seconds). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Alternatives considered

- Keeping the pure white void with an even stronger "no overlay" negative (rejected â€” the user's insight is that the void ITSELF invites the overlay; a consistent colored scene is the real fix).
- A fully detailed/photorealistic colored background (rejected â€” the user wants a MINIMAL watercolor look, not a detailed scene).

### Result

`jaisal_single_shot.json` now uses a minimal watercolor bridge-and-river scene (colored, consistent), ONE paper plane, NO bubbles. **Rule: for the line-art title animation, do NOT use a pure white void (it invites a hallucinated overlay) â€” use a FIXED MINIMAL WATERCOLOR SCENE (bridge + river + sky + bank, soft muted colors) that is IDENTICAL across all seconds; lock the paper plane to ONLY ONE; and use NO bubbles (only a small splash).** **NEXT: run `jaisal_single_shot.json` (10s, 1344Ã—768, turbo 4-step) and check (a) no wooden overlay, (b) ONE paper plane, (c) no bubbles, (d) the watercolor scene stays consistent.**


---

## D033 â€” Sketch title animation: the wooden/mica overlay is a "line-art = physical drawing on a surface" prior (NOT a wiring bug, NOT the reference)

Date: 2026-08-31
Status: Active

### Diagnosis (traced the ACTUAL workflow + reference, not guessed)

The wooden/mica overlay that keeps appearing "on top of the image" was traced to its real cause by inspecting the workflow wiring and the reference image:

1. **Wiring is CLEAN** â€” the reference image enters the model in exactly ONE way: `114 (LoadImage) â†’ 105.0 (IMAGE)` as the i2v **first frame**. There is NO IPAdapter, NO reference adapter, NO latent blend, NO separate image-conditioning node. So the overlay is NOT being fed in by a hidden node (rules out GPT's hypothesis #3/#4).
2. **The reference image is CLEAN** â€” `sketch_00008_.png` background is genuinely pure white (mean RGB 253-255, warm-tone fraction 0.000, R-B = -0.0). No wood/mica in the reference. So the overlay is 100% MODEL-GENERATED.
3. **ROOT CAUSE: the "line-art on white = a physical drawing on a surface" prior.** The model sees line art on a white background and interprets it as a PHYSICAL DRAWING ON A SHEET OF PAPER, so it renders the *paper/surface* the sketch is "drawn on" (wood grain / mica / paper grain). That's why it appears "applied on top of the image" â€” it's the model rendering the surface the drawing sits on. No amount of "NO WOOD" fixes it because we never told the model the line art is NOT on a physical surface at all.

### Fix (prompt v5, saved to `prompts/jaisal_single_shot_prompt_v5_flat.txt`)

1. **FLAT 2D ANIMATION, NOT A PHYSICAL DRAWING** (new top-priority lock, placed FIRST): the line art is NOT drawn on paper, NOT a sketch on a sheet, NOT a photo of a drawing, NOT on a physical surface. NO paper, NO paper texture, NO paper grain, NO surface, NO mica, NO mica texture, NO wood grain, NO wooden texture, NO texture of any kind on the background. The background is a flat clean 2D watercolor scene, NOT a textured surface/sheet/table/floor.
2. **GPT's structural cleanup applied:**
   - **REFERENCE IMAGE ROLE** (new): `<Picture 1>` is used ONLY as a reference for Subject 1's CHARACTER DESIGN. DO NOT preserve/copy/reconstruct the environment/background/floor/walls/objects/textures from `<Picture 1>`. The reference is NOT a scene reference; the environment is generated independently from the text.
   - **ENVIRONMENT LOCK** (replaces the old `<Subject 2> fully_preserved` retention): the environment is a FLAT 2D WATERCOLOR scene generated from the text description ONLY, NOT derived from `<Picture 1>`. The SAME fixed scene across all 10 seconds. NO wood/mica/paper/surface/room/table.
   - **DROPPED the `retention_analysis` section** (it told the model to "preserve" the reference's environment, which is what pulled the overlay in).
3. Retained: 10s timeline, ONE paper plane (never two), NO bubbles, plane SMALL + in-air until 9.00s then floats on water, visible wind lines, static eye-level MEDIUM camera, deep focus, the figure NOT-list.

### Note

The ComfyUI UI re-saves `jaisal_single_shot.json` in native shape (all `widgets_values` are STRINGS, `widgets_values_named` stripped). v5 was written to the POSITIONAL `widgets_values[0]` on BOTH instance node 105 AND internal subgraph node 104 (105==104 verified). Node 105 length = `10` (seconds), node 104 length = `243` (frames, ~10s). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Alternatives considered

- Adding more "NO WOOD" negatives (rejected â€” the overlay is a surface prior, not a text-following failure; more negatives don't break the "drawing on paper" interpretation).
- Changing the reference image (rejected â€” the reference is clean; the problem is the model's prior, not the reference).
- A different workflow / conditioning node (rejected â€” the wiring is already clean; there is no hidden conditioning node to remove).

### Result

`jaisal_single_shot.json` now uses a FLAT 2D watercolor scene with an explicit "NOT a physical drawing / NOT on a surface" lock + GPT's reference-role/environment-lock structural cleanup. **Rule: when line-art i2v renders a wooden/mica/paper overlay "on top of" the image, the cause is the model's "line art = a physical drawing on a surface" prior â€” fix it by explicitly stating the animation is FLAT 2D and NOT a drawing on paper/surface, and by telling the model the reference is CHARACTER-DESIGN-ONLY (not a scene reference) so it doesn't preserve the reference's environment. Do NOT just add more "NO WOOD" negatives.** **NEXT: run `jaisal_single_shot.json` (10s, 1344Ã—768, turbo 4-step, base `sketch_00008_.png`) and check (a) NO wooden/mica/paper overlay, (b) ONE paper plane, (c) no bubbles, (d) the flat watercolor scene stays consistent.**


---

## D034 â€” Sketch title animation: back to B&W line-art + water splash + smooth plane descent + title + 15s (wooden issue stays gone)

Date: 2026-08-31
Status: Active

### Decision

The single-shot i2v title animation (`jaisal_single_shot.json`) prompt is updated (v6, saved to `prompts/jaisal_single_shot_prompt_v6_bw_title.txt`) after the flat-2D fix (D033) successfully removed the wooden/mica overlay. Changes:

1. **Back to STRICTLY BLACK AND WHITE line-art** (removed the watercolor coloring from v4/v5) â€” the user wants it to match the plain 2D reference (black ink lines on a clean white background). The environment is now a FLAT 2D LINE-ART scene (stone bridge, clean white sky, river as scattered dots + wavy dashes, a couple of line trees), NOT colored.
2. **WATER SPLASH** â€” when the figure enters the water (10.00-11.00s), a small line-art splash (a few line-art splash lines). NO bubbles (kept).
3. **SMOOTH PAPER PLANE DESCENT** (fixes the "went down fastly / hovering near the water" problem) â€” the plane descends SLOWLY and GENTLY, gradually losing altitude over several seconds (11.00-13.00s), a smooth slow drift downward, NOT a fast drop, NOT a sudden fall, NOT hovering just above the water, NOT stopping near the water surface. It gently touches the water around 13.00s, then floats calmly.
4. **TITLE 'The Jaisal Cut' ADDED** (14.00-15.00s) â€” appears in clean line-art lettering (hand-drawn line letters, outlined, not filled), 'The' small / 'Jaisal' big / 'Cut' medium, spelled T-h-e J-a-i-s-a-l C-u-t. NO figure in the title shot. (D004 fallback: if the spelling comes out garbled, composite the title in post.)
5. **EXTENDED to 15 seconds** (was 10s) â€” instance node 105 `value_1` = `15` (seconds); internal subgraph node 104 `length` = `362` (frames = 17Ã—21+5 on the 17k+5 grid = ~15.08s at 24fps).
6. **WOODEN ISSUE STAYS GONE** â€” the FLAT 2D ANIMATION, NOT A PHYSICAL DRAWING lock (D033) is RETAINED at the top, plus the REFERENCE IMAGE ROLE (character-design-only) + ENVIRONMENT LOCK (generated from text, not derived from `<Picture 1>`) structural cleanup. NO wood/mica/paper/surface texture.

### Reason

User: "we have achieved an amazing feat, that wooden thing is gone now. now i feel like we can remove the coloring part or we can give some splash of existing white and black because since our image starts from plain 2d, so some kind of splashing will feel good right? also, now the paper plane is floating in the air, but it went down fastly, i think asking it to stay in the air its straight away moving to the near bottom layer of water and staying upthere, which feel like not real or smooth flow. also we can now add our title the jaisal cut and increase the title animation to 13 or 15 seconds, mind you that we should not get the wooden issue again. lets do this and fix the production intro."

### What changed (prompt v6)

- STYLE: watercolor â†’ STRICTLY BLACK AND WHITE line-art (matches the plain 2D reference).
- ENVIRONMENT: colored watercolor scene â†’ FLAT 2D LINE-ART scene (clean white sky, river as dots + wavy dashes, line trees).
- WATER SPLASH added at the figure's entry (10.00-11.00s).
- PAPER PLANE DESCENT: fast drop / hovering near water â†’ SLOWLY and GENTLY, gradually losing altitude over 11.00-13.00s, touches water ~13.00s, then floats.
- TITLE 'The Jaisal Cut' added at 14.00-15.00s (line-art lettering, 'The' small / 'Jaisal' big / 'Cut' medium).
- LENGTH: 10s â†’ 15s (instance `value_1`=15, internal `length`=362 frames).
- RETAINED: FLAT 2D NOT A PHYSICAL DRAWING lock, REFERENCE IMAGE ROLE (character-design-only), ENVIRONMENT LOCK, ONE paper plane, NO bubbles, visible wind lines, static eye-level MEDIUM camera, deep focus, the figure NOT-list.

### Note

The ComfyUI UI re-saves `jaisal_single_shot.json` in native shape (all `widgets_values` are STRINGS, `widgets_values_named` stripped). v6 was written to the POSITIONAL `widgets_values[0]` on BOTH instance node 105 AND internal subgraph node 104 (105==104 verified). Node 105 length = `15` (seconds), node 104 length = `362` (frames, ~15s). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Alternatives considered

- Keeping the watercolor coloring (rejected â€” the user wants plain B&W to match the 2D reference).
- A fast plane drop (rejected â€” the user wants a smooth, realistic, gradual descent).
- 13s instead of 15s (chose 15s â€” the user said "13 or 15"; 15s gives the title its own full second and matches the original production length).

### Result

`jaisal_single_shot.json` is now a 15s B&W line-art title animation: walk â†’ stop â†’ look around â†’ throw ONE plane â†’ wait â†’ jump (with a small splash) â†’ plane descends SLOWLY and GENTLY â†’ plane floats â†’ title 'The Jaisal Cut' appears. The wooden/mica overlay stays gone (flat-2D lock retained). **Rule: for the line-art title animation â€” keep it STRICTLY B&W line-art (match the plain 2D reference), add a small water splash at the figure's entry, make the paper plane descend SLOWLY and GENTLY (not a fast drop, not hovering near the water), add the title 'The Jaisal Cut' in line-art lettering in the final second, and KEEP the FLAT 2D NOT A PHYSICAL DRAWING lock so the wooden/mica overlay does not come back.** **NEXT: run `jaisal_single_shot.json` (15s, 1344Ã—768, turbo 4-step, base `sketch_00008_.png`) and check (a) NO wooden/mica overlay, (b) B&W line-art, (c) water splash at entry, (d) smooth slow plane descent, (e) title 'The Jaisal Cut' appears (if garbled, composite in post per D004).**


---

## D035 â€” Sketch title animation: REVERT v6 (B&W) â†’ v5 watercolor (the working one) + 12s. LESSON: change ONE thing at a time.

Date: 2026-08-31
Status: Active

### What happened

v6 (D034) REMOVED the watercolor and went back to a pure-white B&W background, added the title, and extended to 15s â€” all at once. The user reported the wooden/mica overlay came BACK ("again the same issue... gpt fixed it and you ruined it again"). **Root cause of the regression: removing the watercolor re-introduced the pure-white background, which re-triggered the "line art on white = a drawing on a sheet of paper" prior (D033). The watercolor in v5 was actually PROTECTING against that â€” a colored background does not read as a paper sheet.** v6 also piled on the title + 15s, so the regression could not be isolated.

### Fix (prompt v7, saved to `prompts/jaisal_single_shot_prompt_v7_12s.txt`)

**REVERTED to the exact v5 prompt** (the one that gave "the wooden thing is gone") â€” i.e. the FLAT 2D watercolor scene + FLAT 2D NOT A PHYSICAL DRAWING lock + REFERENCE IMAGE ROLE + ENVIRONMENT LOCK + ONE paper plane + NO bubbles â€” and made ONLY these changes:
1. **Timeline extended 10s â†’ 12s** (instance node 105 `value_1` = `12` seconds; internal subgraph node 104 `length` = `289` frames = 17Ã—17+1 on the 17k+5 grid = ~12.04s at 24fps).
2. **Paper plane in-air until 10.00s** (was 9.00s), then descends slowly and floats in the final second (11.00-12.00s).
3. **Title NOT rendered by the model** â€” back to "composited in post" (D004). The title is added in post over the final frame, NOT asked of the model (avoids the garbled-spelling risk and keeps the prompt focused).
4. **NO title in the prompt** (removed the v6 title-rendering beat).

Everything else is IDENTICAL to v5. Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### LESSON (recorded because it was a real mistake)

**Change ONE thing at a time.** v6 changed the style (watercolorâ†’B&W), added the title, AND changed the length simultaneously â€” when the result regressed, it was impossible to tell which change caused it. The style change (removing the watercolor) was the culprit. **Rule: when a prompt is WORKING (the wooden overlay is gone), do NOT change the style/background â€” only adjust the timeline/length. To add the title, composite it in POST (D004), do NOT ask the model to render it. The watercolor background is a PROTECTION against the "drawing on paper" prior â€” do NOT revert to a pure-white background.**

### Result

`jaisal_single_shot.json` is back to the WORKING v5 watercolor prompt, now at 12s, title composited in post. **NEXT: run `jaisal_single_shot.json` (12s, 1344Ã—768, turbo 4-step, base `sketch_00008_.png`) and confirm the wooden/mica overlay stays GONE. Then composite the 'The Jaisal Cut' title in post over the final frame.**

---

## D036 â€” Sketch title animation: v8 = 14s, B&W first second â†’ color fades in, plane lands in natural motion, title at end. Krea2 identity-edit title image.

Date: 2026-08-31
Status: Active

### What changed (prompt v8, saved to `prompts/jaisal_single_shot_prompt_v8_14s.txt`)

Built on the WORKING v7 (v5 watercolor + 12s). Changes:
1. **12s â†’ 14s** (instance node 105 `value_1` = `14` seconds; internal subgraph node 104 `length` = `345` frames = 17Ã—20+5 on the 17k+5 grid = ~14.375s at 24fps).
2. **First second (0.00-1.00) is STILL + PLAIN BLACK AND WHITE line art** (no color yet).
3. **From the second second (1.00) onward, COLOR FADES IN** â€” the watercolor colors (teal water, warm sand, green hills, blue sky) fade in smoothly over the first ~2 seconds while the figure starts walking. (User: "let the color change from the second second onwards.")
4. **Paper plane LANDS in NATURAL MOTION** (user: "let the paper plane land in normal motion, let it not wait or stay extra long in air, it feels unnatural"): thrown at 4.00s, flies in a NATURAL ARC (rises slightly, then descends in a smooth curve), LANDS on the water ~7.00s. Does NOT hover, does NOT stay in the air long.
5. **Title 'The Jaisal Cut' appears at 13.00-14.00** (line-art lettering, 'The' small / 'Jaisal' big / 'Cut' medium). NOTE: this is a RISK â€” diffusion is unreliable at spelling (D004). If the model garbles the title, composite it in post over the final frame instead.
6. **Retained from v5/v7**: FLAT 2D ANIMATION NOT A PHYSICAL DRAWING (top priority), watercolor background (the PROTECTION against the "drawing on paper" prior â€” D033/D035), REFERENCE IMAGE ROLE, ENVIRONMENT LOCK, ONE paper plane, NO bubbles, wind lines, static eye-level MEDIUM camera.

Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Krea2 title image (separate workflow)

`krea2_identity_edit.json` (Krea2 Identity Edit v1.2) set up to generate the TITLE image:
- Node 72 (LoadImage) = `FINAL_TITLE_REFERENCE.png` (the user's screenshot of the final frame, copied to `input\`).
- Node 84 (positive instruction) = `prompts/jaisal_title_instruction.txt` â€” adds 'The Jaisal Cut' in the SAME colored watercolor style ('The' small / 'Jaisal' big / 'Cut' medium), keeps the scene identical, NO figure.
- Node 85 (negative) = no figure, no text errors, no extra elements.
- Node 29 (SaveImage) prefix = `jaisal_cut/title_final`.
- ref_boost = 4.0 (fidelity dial), KSampler 10 steps cfg 1 (turbo), 16:9 2048Ã—1152.
- The user runs this in ComfyUI (vision unavailable in the agent session).

### Plan (user's final direction)

1. Run `krea2_identity_edit.json` â†’ title image (`jaisal_cut/title_final_*.png`).
2. Feed that title image to the MiniMax workflow as a reference (or use it as the final frame).
3. Run `jaisal_single_shot.json` (14s, 1344Ã—768, turbo 4-step, base `sketch_00008_.png`) â†’ colored video with the title.
4. Cut from ~1s to 14s (or first second to 14s) to get the colored video with the title.

### LESSON

**The watercolor background is a PROTECTION against the "drawing on paper" prior (D033/D035) â€” do NOT revert to a pure-white background.** The B&W first second is a TEMPORARY state (only 0.00-1.00s) before the color fades in; it is NOT a pure-white background for the whole video, so it should not re-trigger the paper-surface prior. **Change ONE thing at a time** (D035) â€” v8 changed the timeline + color transition + plane motion + title, so if it regresses, the title-rendering is the most likely culprit (drop it and composite in post).

---

## D037 â€” Krea2 identity-edit title workflow: added Typnosis_Krea2 typography LoRA (node 95, strength 5.0)

Date: 2026-08-31
Status: Active

### What changed

Added the **`Typnosis_Krea2.safetensors`** typography LoRA (457 MB, confirmed present in `E:\ComfyUI_windows_portable\ComfyUI\models\loras`) into `krea2_identity_edit.json` so the title 'The Jaisal Cut' renders with cleaner, more legible lettering.

**New node 95** (`LoraLoaderModelOnly`) inserted into the MODEL chain between the identity LoRA and the patch:
- Chain is now: `55 UNETLoader â†’ 71 identity LoRA (krea2_identity_edit_v1_2 @1.0) â†’ 95 Typnosis_Krea2 @5.0 â†’ 79 Krea2EditModelPatch â†’ 53 KSampler`.
- Node 95 `widgets_values` = `["Typnosis_Krea2.safetensors", 5.0]`.
- Rewired: link 2 (71â†’79) replaced by link 38 (71â†’95) + link 39 (95â†’79). Node 71 output â†’ [38]; node 79 model input â†’ 39.
- Updated the file-list note (node 100) to list both LoRAs.

**Strength 5.0** = the STR5 sweet spot from the earlier title-card work (D030-era: STR1-2 most prompt-faithful, STR4+ more stylized + compositions converge; STR5 = balanced-strong).

Validated `valid: true`, 0 errors (1 pre-existing harmless warning on node 79 `source_latent_b` â€” the optional second-reference latent input, bypassed by default).

### Tuning

- Title lettering too weak / not stylized enough â†’ raise node 95 to 6.0-7.0.
- Title over-stylized / letters distort â†’ lower node 95 to 3.0-4.0.
- Identity (face/scene) getting washed out by the typography LoRA â†’ lower node 95, or raise node 71 (identity) strength.
- The identity LoRA (71) stays at 1.0 â€” it is the face/scene fidelity anchor; the typography LoRA (95) only shapes the LETTERING.

### Rule

**For a Krea2 title image, chain the identity LoRA (face/scene fidelity) + the Typnosis_Krea2 typography LoRA (lettering) in series on the MODEL path, identity first then typography, both feeding the Krea2EditModelPatch.** The typography LoRA at STR5 gives the cleanest legible title lettering without destroying the scene identity.

---

## D038 â€” Title composition: title ON THE RIVER WATER + paper plane RIGHT NEXT TO it (the perfect end)

Date: 2026-08-31
Status: Active

### What changed (user: "i want the text to be on the river, after the kid drowned, there i need my title and right next to it we will have our paper plane, that will be our perfect end to the production pipeline")

The final beat (13.00-14.00s) of the title animation is now a **calm water surface** where:
1. **The title 'The Jaisal Cut' floats ON THE RIVER WATER** (lower-center of the frame, on the water surface â€” NOT in the sky, NOT on the bridge), in clean line-art lettering ('The' small / 'Jaisal' big / 'Cut' medium, spelled T-h-e J-a-i-s-a-l C-u-t).
2. **The ONE SMALL paper plane floats RIGHT NEXT TO the title** (a small line-art paper plane on the river surface, close to the title).
3. **NO figure / NO person / NO kid** â€” the figure has already drowned and is GONE.
4. The title-on-water + the paper plane next to it are the ONLY things in the frame.

Applied to BOTH:
- **`jaisal_single_shot.json`** (MiniMax i2v) â€” the 13.00-14.00s beat + the summary line updated (both instance node 105 + internal subgraph node 104, 105==104 verified, 14s / 345 frames). Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).
- **`krea2_identity_edit.json`** (Krea2 title image) â€” node 84 (positive instruction) updated to the SAME composition (title on the river water + paper plane next to it + NO figure). Saved to `prompts/jaisal_title_instruction.txt`. Validated `valid: true`, 0 errors (1 pre-existing harmless warning on node 79 `source_latent_b`).

### Why this is the "perfect end"

The story is: walk â†’ throw plane â†’ jump â†’ **drown** â†’ the water is calm â†’ the **title appears on the water** with the **paper plane floating beside it**. The drowned figure is gone, so the final frame is a clean, quiet, symbolic ending (title + plane on still water) â€” no character, just the title and the plane. This is the closing image of the production pipeline.

### Rule

**The title animation ENDS on a calm water surface: the title 'The Jaisal Cut' floats ON THE RIVER WATER (lower-center) with the ONE paper plane floating RIGHT NEXT TO it, NO figure (already drowned).** Both the MiniMax i2v final beat AND the Krea2 title-image instruction must match this composition so the video's last frame and the Krea2 title image agree.

---

## D039 â€” Title SIMPLIFIED: title ON THE RIVER (like the paper plane), Typnosis LoRA BYPASSED. LESSON: do not complicate.

Date: 2026-08-31
Status: Active

### What happened (user: "this aint working, we dont need the lora, so i reduced the strength and bypassed it... we need the The jaisal cut to be on river, just like we have our paper plane, do not complicate this")

Two things:
1. **The Typnosis_Krea2 typography LoRA (node 95) is BYPASSED** (mode 7) in `krea2_identity_edit.json` â€” it was not helping ("this aint working"). The chain is effectively back to `55 UNETLoader â†’ 71 identity LoRA @1.0 â†’ 79 Krea2EditModelPatch â†’ 53 KSampler` (node 95 stays in the graph, bypassed, so it can be re-enabled later if ever wanted).
2. **The title instruction was SIMPLIFIED** (node 84 + `prompts/jaisal_title_instruction.txt` + the v8 prompt's 13.00-14.00s beat + summary): the title 'The Jaisal Cut' floats **ON THE RIVER WATER, like floating in water**, lower-center, NOT in the sky / NOT on the bridge. Hierarchy: **'The' Small, 'Jaisal' (largest), 'Cut' Small** (was 'The' small / 'Jaisal' big / 'Cut' medium). The title is on the river **just like the paper plane is on the river** â€” the "paper plane RIGHT NEXT TO the title" complication was REMOVED. NO figure (already drowned, GONE).

Applied to BOTH `jaisal_single_shot.json` (nodes 105 + 104, 14s/345 frames, validated `valid: true` 0 errors) AND `krea2_identity_edit.json` (node 84, validated `valid: true` 0 errors).

### LESSON

**Do NOT complicate the title.** The user's mental model is simple: the title sits ON THE RIVER the same way the paper plane sits on the river â€” one calm water surface, the title floating on it. Adding extra elements (a plane "right next to" the title, size-hierarchy essays) made it worse. Keep the instruction SHORT and CONCRETE: title on the water, like the plane is on the water. **A typography LoRA is NOT needed for a simple line-art title on water â€” the identity workflow's own line-art style is enough; bypass the LoRA.**

---

## D040 â€” MiniMax title animation: TWO-FRAME (first-to-last) â€” figure (first) â†’ title-on-river (last). Title image wired as last_frame.

Date: 2026-08-31
Status: Active

### What changed (user: "im good with the title image, lets update the prompt and wire the 2 images in our minimax workflow")

The MiniMax H3 node in `jaisal_single_shot.json` is `MiniMaxH3ImageToVideo` running on `minimax_h3_fl2va` (first-**last**-to-video) â€” it has BOTH a `first_frame` and a `last_frame` input. Previously only `first_frame` was wired. Now BOTH images are wired:

1. **FIRST FRAME** = `sketch_00008_.png` (the walking figure on the bridge, B&W line art) â€” LoadImage node 114 â†’ node 105 slot 0 (`first_frame`, link 218). UNCHANGED.
2. **LAST FRAME** = `jaisal_title_final.png` (= the user's chosen title image `title_final_00015_.png`, copied to `input\`) â€” NEW LoadImage node 125 â†’ node 105 slot 1 (`last_frame`, link 229).

**Prompt updated to a TWO-FRAME (first-to-last) structure** (`prompts/jaisal_single_shot_prompt_v8_14s.txt`, applied to both node 105 + internal node 104, 105==104 verified, 14s/345 frames):
- The old "REFERENCE IMAGE ROLE" section (which said `<Picture 1>` is character-design-only) was REPLACED with a **TWO-FRAME ANIMATION (FIRST-TO-LAST)** section: FIRST FRAME = `<Picture 1>` (figure on bridge, B&W), LAST FRAME = `<Picture 2>` (title 'The Jaisal Cut' on the river water, colored). The video animates SMOOTHLY from first to last. **The title in the last frame is EXACTLY the title image provided in `<Picture 2>` â€” do NOT alter its spelling, position, size, or style. The FINAL frame MUST match `<Picture 2>` exactly.**
- The summary line + the 13.00-14.00s final beat updated: the scene CONVERGES to the last frame (the title image), the figure is GONE (drowned).

Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120), 28 nodes.

### Why this is the right approach

**The title is now GUARANTEED to be exactly the user's title image** â€” the last frame is the image itself, so there is NO spelling risk (the D004 garbled-title problem is eliminated for the final frame). The model only has to ANIMATE the transition (figure â†’ title on the river), not RENDER the title text. This is the "perfect end": the video ends on EXACTLY the title image the user approved.

### Rule

**For a title ending, use the MiniMax first-to-last (fl2va) node with BOTH frames wired: first_frame = the scene/figure image, last_frame = the approved title image. The prompt describes the two anchor frames + the transition, and explicitly says the final frame must EXACTLY match the last-frame image (do not alter its text/position/style).** This eliminates the title-spelling risk â€” the model animates TO the title, it does not render it.

---

## D041 â€” Audio: NATURAL SOUNDS ONLY (no instrumental music) â€” HARD RULE (user is Muslim, does not promote instrumental music)

Date: 2026-08-31
Status: Active

### What changed (user: "i am a muslim and i dont want to promote instrumental music in my videos, whether its a movie or title animation. lets use natural sound, footsteps, wind, water sound and birds sound thats it for the current video")

**HARD RULE (persistent, applies to ALL future videos/animations in this project): NO instrumental music, NO musical instruments, NO melody, NO beat, NO soundtrack, NO background music.** Only NATURAL ambient sounds.

Updated the `overall_soundscape` + `non_diegetic_music` sections of `prompts/jaisal_single_shot_prompt_v8_14s.txt` (applied to both node 105 + internal node 104, 105==104 verified, 14s/345 frames):
- **overall_soundscape** = NATURAL SOUNDS ONLY: soft footsteps on the stone bridge, a gentle continuous wind, the soft flowing river water, a few birds chirping in the distance (natural ambient), a soft whoosh as the plane is thrown, a soft plop as the plane lands, a soft splash as the figure jumps in, then a calm quiet hush with water + wind as the title appears. **NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO soundtrack (HARD RULE).** No dialogue, NO bubble pops.
- **non_diegetic_music** = NO music of any kind (HARD RULE - the creator does not promote instrumental music). ONLY natural ambient sounds: footsteps, wind, river water, birds. No dialogue, no subtitles.

Validated `valid: true`, 0 errors (2 pre-existing harmless warnings on template helper nodes 119/120).

### Audio-only option (user asked "can we add the audio alone for a video?")

The MiniMax H3 node (`minimax_h3_fl2va`) generates video **WITH** audio as one unit â€” the audio is baked in at generation time, so the cleanest fix is to **re-run the video with the updated natural-sounds prompt** (what we just did). If the user has a GOOD video but only wants to swap the audio track WITHOUT regenerating the video, that is a separate post step (extract video track + mux a natural-sounds audio file onto it in a video editor) â€” but since the model generates the audio, re-running with the corrected prompt is the intended path. **Rule: for this project, ALWAYS specify NATURAL SOUNDS ONLY (footsteps/wind/water/birds) + an explicit NO-music HARD RULE in the soundscape; never allow instrumental music.**

---

## D042 â€” Audio for a LOCKED video via ControlFoley (comfyui-controlfoley-official), TC-V2A mode

Date: 2026-09-02
Status: Active

### Decision

To add a natural-sounds soundtrack to an ALREADY-LOCKED video (without regenerating it), use the **ControlFoley** custom node pack (`comfyui-controlfoley-official`, Xiaomi Research's video-to-audio model) in **TC-V2A mode** (video + text-guided sounds). The locked video is `Jaisal_Sketch_Title_00010_.mp4` (12.25s, 24fps, 1344Ã—768).

### Workflow (`jaisal_sketch_title_audio.json`, built by `utilities/build_controlfoley_audio.py`)

Chain: `LoadControlFoleyModel` â†’ `ControlFoleyGenerate` â† `LoadControlFoleyVideo`; `ControlFoleyGenerate` â†’ `SaveControlFoleyAudio` (WAV) and â†’ `MuxControlFoleyAudioToVideo` (mode `replace` â†’ final MP4 with the new audio replacing the original).
- `LoadControlFoleyVideo` loads `input\jaisal_sketch_title_00010.mp4` (video staged there), duration 12.5.
- `ControlFoleyGenerate` prompt = the exact natural sounds in story order (footsteps on stone, gentle wind, low whistle, flowing river water, distant birds, soft whoosh as the plane is thrown, soft plop as it lands, soft whoosh as the figure jumps, soft splash as he lands, then calm water + low birds) + the D041 NO-music HARD RULE. `guidance_scale` 4.5, `num_inference_steps` `fixed`, `seed` 42, `clip/sync_batch_size_multiplier` 40.
- `MuxControlFoleyAudioToVideo` output = `controlfoley/jaisal_sketch_title.mp4`.

### Setup facts (verified 2026-09-02)

- Node pack installed at `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-controlfoley-official` (10 nodes: LoadControlFoleyDependencies/Model, ControlFoleyTorchCompile, LoadControlFoleyVideo, ControlFoleyGenerate/Advanced/SimpleGenerate, SaveControlFoleyAudio, MuxControlFoleyAudioToVideo, UnloadControlFoleyModel). Imports cleanly.
- **Missing pip deps installed** into the embedded Python: soundfile, librosa, laion-clap, open-clip-torch, nnAudio, torchdiffeq, torchlibrosa, julius, flashy, dora-search (imports as `dora`), submitit, treetable, retrying, num2words, spacy, colorlog, pillow.
- **The running ComfyUI (port 8188) was started BEFORE the node pack was installed â†’ the ControlFoley nodes are NOT registered** (validation shows `unknown_class_type`). **A ComfyUI RESTART is required** for the nodes to load. ComfyUI is a portable install started manually (NOT under comfy-cli control), so the USER restarts it.
- **First run auto-fetches** the ControlFoley source tree (pinned revision, shallow git clone into `<ComfyUI root>/controlfoley`) and **downloads ~16 GB of weights** from Hugging Face (`YJX-Xiaomi/ControlFoley`: `weights/controlfoley.pth` + 4 `ext_weights/*`) into `ComfyUI/models/controlfoley`, plus third-party HF deps (CLIP ViT-H, BigVGAN, musicgen-style, roberta/bart/bert-base, MERT). If huggingface.co is slow, set `$env:HF_ENDPOINT="https://hf-mirror.com"` before starting ComfyUI.
- `LoadControlFoleyModel` widgets: `[controlfoley_source_dir, model_weights_dir, variant=large_44k, device=auto, precision=bf16, low_vram=False, compile_encoders=False, auto_fetch_source=True]`. Leave `model_weights_dir` = `path/to/model_weights` (auto-downloads). `low_vram=False` is REQUIRED for V2A/TC-V2A (low_vram keeps video encoders on CPU and disables them).

### Reason

The user locked the video (`Jaisal_Sketch_Title_00010_`) and wants to add a natural-sounds soundtrack WITHOUT regenerating it. ControlFoley TC-V2A generates sound effects that FOLLOW the visual content, guided by a text prompt â€” exactly the "footsteps + whistle + wind + whoosh + splash + birds" the user described. This is the audio-only post path from D041 (swap the audio track on an existing video).

### Alternatives considered

- Re-running the MiniMax video with the natural-sounds prompt (D041's intended path) â€” rejected here because the user has ALREADY locked the video and only wants the audio added.
- Manual audio in DaVinci Resolve â€” the user explicitly wants to do it with AI (ControlFoley) for this simple video.

### Rule

**For a locked video, add a natural-sounds soundtrack with ControlFoley TC-V2A: `LoadControlFoleyVideo` (the video) + `ControlFoleyGenerate` (natural-sounds prompt + D041 NO-music rule) â†’ `SaveControlFoleyAudio` (WAV) + `MuxControlFoleyAudioToVideo` (replace â†’ final MP4). The node pack needs a ComfyUI restart to register, and the first run auto-downloads ~16 GB of weights. ALWAYS keep the D041 natural-sounds-only / NO-music HARD RULE in the prompt.**

### Resolution (2026-09-03) â€” WORKS after 3 package-level bug fixes

The first run (job `6b490126`) HUNG 2h40m with no output. Root cause was NOT the workflow â€” it was 3 bugs in the laion-clap package + node pack, each revealed one layer deeper:

1. **Import-time `SystemExit(2)` (the hang).** `laion_clap/training/params.py` ran `parse_args()` at import time (via `hook.py` â†’ `training.data`). Under ComfyUI, `sys.argv` = ComfyUI's launch args, so argparse raised `SystemExit(2)` (a `BaseException`, slips past `except Exception`), leaving the prompt stuck. **FIX:** `params.py` `parse_args()` â†’ `parse_known_args()[0]`. Backup `params.py.bak_comfyfix`.
2. **CLAP `position_ids` unexpected key.** `laion_clap/hook.py:129` `load_state_dict(ckpt)` used `strict=True`, rejecting the audioset checkpoint's extra `text_branch.embeddings.position_ids` buffer. **FIX:** `load_state_dict(ckpt, strict=False)`. Backup `hook.py.bak_comfyfix`.
3. **BigVGAN `resume_download` missing arg.** The node pack's `_patch_bigvgan_from_pretrained` wrapper only injected `proxies`, but the installed `huggingface_hub` now requires `resume_download` (keyword-only). **FIX:** `nodes.py` `_compat_from_pretrained` now also `kwargs.setdefault("resume_download", False)`.

**All three are package-level (persist across restarts). A ComfyUI RESTART is required after patching `nodes.py` (imported at startup, cached in memory).** After the fixes, the job completed and produced `output\controlfoley\jaisal_sketch_title_00001_.wav` (1.03 MB) + `jaisal_sketch_title_00002_.mp4` (13.77 MB, audio muxed in, replace mode).

**Submit with NAMED inputs** via `utilities/submit_controlfoley.py` (the UIâ†’API converter mis-maps `ControlFoleyGenerate`'s positional `widgets_values` â€” a hidden widget shifts them â€” so `run_workflow` fails validation; named inputs bypass it). See EXPERIMENTS.md 2026-09-03.

---

## D043 â€” ControlFoley `LoadControlFoleyVideo` resolves the video from the `input\` dir (stage it there first)

Date: 2026-09-03
Status: Active

### Decision

The `LoadControlFoleyVideo` node's `video_path` widget is a **relative filename resolved against the ComfyUI `input\` directory** (via `_resolve_path`, which tries `input\`, the node dir, the ComfyUI root, and cwd in order). It is NOT a path into `output\`. So to feed a generated video to ControlFoley, **copy it from `output\video\` into `input\` first**, then set the node's `video_path` to that filename.

### Reason

The user tried to run the audio workflow on the actual video `Jaisal_Sketch_Title_00011_` and got `FileNotFoundError: Input video not found: jaisal_sketch_title_00011.mp4`. Two mismatches: (1) the node looks in `input\`, but the video lives in `output\video\`; (2) the actual output filename is `Jaisal_Sketch_Title_00011_.mp4` (capitalized, with a trailing `_` before `.mp4`), while the node's widget held `jaisal_sketch_title_00011.mp4` (lowercase, no trailing `_`). The node has **no file-picker UI** â€” the filename is a plain STRING widget, so the user can't browse to the file; it must be staged + named to match.

### Alternatives considered

- Pointing `video_path` at the absolute `output\video\Jaisal_Sketch_Title_00011_.mp4` path (works â€” `_resolve_path` accepts absolute paths â€” but the staged `input\` copy is the established convention and keeps the workflow portable).

### Result

Staged `output\video\Jaisal_Sketch_Title_00011_.mp4` â†’ `input\jaisal_sketch_title_00011.mp4` and set node 2 (`LoadControlFoleyVideo`) `widgets_values` = `["jaisal_sketch_title_00011.mp4", 15.0]` (duration 15.0 = upper limit; the video is 14.33s so the output follows the input length). **Rule: to change the ControlFoley input video, copy the desired `output\video\*.mp4` into `input\` and set the `LoadControlFoleyVideo` `video_path` widget to that filename (the node has no file browser). The `duration` widget is an upper limit, not the output length.**

---

## D044 â€” ControlFoley prompt: use a TIMED, video-synced sound design (not a flat list); put exclusions in the NEGATIVE prompt; align duration to the video

Date: 2026-09-03
Status: Active

### Decision

For ControlFoley TC-V2A (videoâ†’audio), the `ControlFoleyGenerate` `prompt` must be a **TIMED, beat-by-beat sound design synced to the video** (e.g. `0-2s: soft footsteps`, `2-3s: whistle + plane whoosh`, `6s: plane plop on water`, `9s: splash`, `11s onward: flowing water only`), NOT a flat un-timed list of ~10 sounds. The **NO-music / NO-noise exclusions belong in the `negative_prompt` widget**, not crammed into the positive prompt. And the `duration` widget must be **â‰¥ the actual video length** (upper limit) so the tail is not cut.

### Reason

The first 00011 run came out as **static noise, no real sounds** (user: "the output have only static noise, no real sound we wanted"). Three causes: (1) the positive prompt was a **flat, un-timed list** of ~10 sounds with no temporal structure â€” a video-to-audio model needs to know WHEN each sound happens to sync it to the visuals; an undifferentiated blob of sound words degrades into incoherent noise. (2) the **NO-music/NO-instrument/NO-melody/NO-beat/NO-soundtrack exclusions were stuffed into the positive prompt**, adding conflicting signal. (3) the `duration` widget was **12.5 but the video is 14.33s**, so the last ~2s (the title at ~11s) was cut/misaligned.

### Alternatives considered

- Keeping the flat list but adding "synced to the video" (insufficient â€” still no per-second structure).
- Leaving the NO-music words in the positive prompt (rejected â€” they belong in the negative prompt, which is what that widget is for).

### Result

Rewrote node 3 (`ControlFoleyGenerate`) via `utilities/update_controlfoley_prompt.py`: (1) **timed prompt** matching the user's exact beat-by-beat (footsteps 0-2s â†’ whistle+throw 2-3s â†’ quiet 3-6s â†’ plane plop 6s â†’ jump whoosh 6-7s â†’ land+second jump 7-8s â†’ splash 9s â†’ calm water 9-11s â†’ flowing water only 11s+); (2) **negative_prompt** = `music, instrumental music, musical instruments, melody, beat, rhythm, soundtrack, song, dialogue, speech, talking, voice, loud sounds, harsh noise, distortion, static, electronic sounds, beeps, alarms`; (3) **duration 12.5 â†’ 15.0** (upper limit; video is 14.33s). Re-ran via `submit_controlfoley.py` â†’ `output\controlfoley\jaisal_sketch_title_00005_.wav` (14.35s, matches the video) + `jaisal_sketch_title_00006_.mp4` (muxed, replace). **Rule: ControlFoley TC-V2A prompts are TIMED and video-synced (per-second sound beats), exclusions go in the negative prompt, and duration â‰¥ video length. If a run comes out as static noise, the prompt is too flat/undifferentiated â€” add per-second timing and move the exclusions to the negative prompt.**

### Update 2026-09-03 (v2 â€” NO-WATER A/B test)

The v1 timed prompt STILL came out as a continuous noise bed. **Hypothesis (user): the CONTINUOUS water/wind descriptions make the model fill the whole timeline with a water-noise bed that masks the discrete action sounds.** **v2 (`utilities/update_controlfoley_prompt_v2.py`):** removed ALL continuous water/wind beds â€” the prompt now has ONLY the discrete action sounds (footsteps, whistle+throw, plane plop, jump whoosh, land thud+second jump, splash) + an explicit "background is QUIET - no continuous water/wind/ambient bed" line; the NEGATIVE prompt also suppresses continuous water/wind (`continuous water, flowing water, river sound, water ambience, constant water, white noise, hiss, constant ambient, continuous wind, wind bed`). Re-ran â†’ `jaisal_sketch_title_00007_.wav` + `jaisal_sketch_title_00008_.mp4`. **Rule: if a ControlFoley run is a continuous noise bed, the CONTINUOUS ambient descriptions (water/wind) are the likely culprit â€” describe ONLY the discrete action sounds, explicitly say the background is quiet, and put continuous-water/wind in the negative prompt. If it's STILL noise after that, the problem is elsewhere (raise `guidance_scale` 4.5â†’6, try a different `seed`, or the model is weak at this videoâ†’audio task).**

### Update 2026-09-03 (v3 â€” SOURCE AUDIO NOT THE ISSUE; CONTROLFOLEY UNSUITABLE FOR LINE-ART VIDEO)

The v2 no-water prompt STILL came out as a flat noise bed (user: "still the same, there is no sound for the actions we mentioned either, and the noise sound is there, first it should make this video soundless or should we make it? maybe thats the issue?"). **Diagnosis (measured, not guessed):** (1) **The source video's audio is NOT used by ControlFoley** â€” the `LoadControlFoleyVideo` node outputs `{"path", "duration"}` (file path + duration, NO audio track); the `ControlFoleyGenerate` node's `video` input is that dict, and its `video_input` (VIDEO) and `images` (IMAGE) inputs are NOT connected. The node conditions on the video's FRAMES (CLIP video features â€” `clip_batch_size_multiplier` = "frames per CLIP encoder call"), not its audio. **Proof:** stripped the audio from `input\jaisal_sketch_title_00011.mp4` (ffmpeg `-an -c:v copy`) and re-ran â†’ the output `jaisal_sketch_title_00009_.wav` is **byte-for-byte identical** to the previous run (same per-second RMS ~-24 dB, same spectral centroid 5938 Hz, same peak/RMS ratio 10.88). (2) **The real cause: ControlFoley is NOT extracting the action sounds from this 2D line-art video.** The output is a **completely flat ~-24 dB broadband noise bed across all 14 seconds** (spectral centroid 5938 Hz = bright noise) â€” the model is NOT generating the footsteps/whistle/splash, it's just outputting a steady noise floor. The likely cause: **ControlFoley is trained on realistic video, but the video is a 2D line-art stick-figure animation** â€” it gives the CLIP video encoder almost no realistic visual cues to condition on, so the model falls back to a generic noise bed. **This is a fundamental limitation: ControlFoley is not suitable for 2D line-art video.** **Options:** (a) **Keep the MiniMax-generated audio** already in the video (it was generated with the natural-sounds prompt â€” footsteps, whistle, wind, water, birds, whoosh, splash â€” so its baked-in audio IS the natural-sounds track; simplest path); (b) **Generate action sounds separately** (text-to-audio / SFX library) and sync them manually in a video editor (more control, more work); (c) **ControlFoley is not suitable for this line-art video** â€” it's designed for realistic video, not 2D animation. **Rule: if a ControlFoley run on a stylized/line-art video produces a flat noise bed (not the action sounds), the video is too stylized for the model â€” the CLIP video encoder can't extract action cues from 2D animation. Keep the source video's own audio (if it's good) or generate the action sounds separately. Do NOT waste time tweaking the ControlFoley prompt for a line-art video.**

### Update 2026-09-03 (v4 â€” TEXT-ONLY MODE ALSO A NOISE BED; CONTROLFOLEY NOT SUITABLE)

The user wants a REUSABLE production workflow (strip audio + generate SFX alone) and asked to build the text-only ControlFoley path. **Built `jaisal_sketch_title_audio.json` in TEXT-ONLY mode** via `utilities/build_controlfoley_textonly.py` (backed up the video-mode version to `workflow_backups\jaisal_sketch_title_audio_video_mode.json`): removed the Node 2â†’Node 3 link (video no longer feeds the generator), set Node 3's `video` input link to None, updated the prompt to a clean text-only SFX timeline (no "synced to the video"), duration 14.5. Node 2 (LoadControlFoleyVideo) still feeds Node 5 (mux) so the SFX gets muxed into the soundless video. **Re-ran â†’ `jaisal_sketch_title_00011_.wav` + `jaisal_sketch_title_00012_.mp4`.** **Result: STILL a noise bed** â€” per-second RMS ~-29 to -34 dB (quieter than video mode's -24 dB but still flat), spectral centroid 6489 Hz (bright/noisy), peak/RMS 14.44. **Text-only mode did NOT produce clean discrete SFX (footsteps/whistle/splash) â€” it's still a broadband noise floor.** **CONCLUSION: ControlFoley is NOT suitable for clean SFX generation for this content, in EITHER video mode OR text-only mode.** It consistently produces a noise bed. **The reusable text-only workflow is still a valid production item** (the wiring is correct and reusable for other videos), but ControlFoley's SFX quality is the limitation. **Next options for clean music-free SFX:** (a) **Music separation** on the MiniMax audio (Demucs/Spleeter â€” NOT installed) to remove the music and keep the natural SFX (the MiniMax audio already has the natural SFX synced to the video, just mixed with music); (b) **Manual SFX** in a video editor (reliable, "old way"); (c) a different SFX-generation tool. **Rule: ControlFoley (video + text-only) produces a noise bed for this line-art video â€” do NOT keep burning compute on it. For clean music-free SFX, try music separation on the source audio or manual SFX.**

---

## D042 â€” SLA (Sparse Linear Attention) is the actual H3 speed stack; 1MP < 240 s

Date: 2026-09-01
Status: Active

### Decision

The MiniMax H3 speed stack in all production workflows is **SLA (Sparse Linear Attention)** via the **`H3SLAAttention` node** from `ComfyUI-PlagueKind-Nodes/ComfyUI-H3-SLA-Attention`. With SLA wired in, a **1MP (1344Ã—768) H3 render completes in UNDER 240 seconds (~4 min)** â€” NOT the 25â€“40 min full-attention estimate in D026.

### Reason

The user's production workflows (`jaisalproduction1.json`, `jaisal_2mp_test.json`, `beach_sprint_test.json`, `t2v_beach_sprint_test.json`) all wire `H3SLAAttention` (node id 150). Config in use: `widgets_values = [0.9, '32', 8192, 1, True, True, '0', 'comfy_kitchen', True, False, False]` â†’ **sparsity 0.90, dense_backend = `comfy_kitchen_int8`**. The user measured 1MP generation at **< 240 s** on this stack.

### Alternatives considered

- Quoting the D026 25â€“40 min figure (rejected â€” that is full-attention H3; SLA is in the graph and is far faster).
- VDN-H3 (Video Delta Net) â€” a different hybrid-attention speedup; **deferred to a later step** (see D043). VDN 8-step turbo REPLACES the community turbo LoRAs and adds ~4.3 GB VRAM; it is a separate setup to benchmark against SLA, not a drop-in.

### Result

**Rule: when estimating MiniMax H3 render time on THIS machine, use the SLA stack â€” 1MP â‰ˆ < 240 s. Do NOT quote 25â€“40 min (that is full-attention). The 2K VRAM-thrashing caveat from D026 still applies (SLA speeds attention but not 2K activation/VRAM pressure). When comparing speedups (e.g. VDN), benchmark against the SLA < 240 s baseline, not the 25â€“40 min figure.**

---

## D043 â€” Two new workflows ready: Face Detailer (close-ups) + SAM character/background swap

Date: 2026-09-01
Status: Active (installed; pending ComfyUI restart to register nodes)

### Decision

Two workflows are now installed and model-path-remapped for use in ~1â€“2 weeks (once the audio/dubbing path is settled):

1. **Face Detailer** â€” `WF-H3_zuanfilm-Face_Detailer.json` (close-up / face-refine shots). Node pack = **`Carasibana/ComfyUI-H3-FaceRefine`** (cloned into `custom_nodes`). Defines `H3FaceSelect`, `H3FaceTrackCrop`, `H3FaceStitch`, `H3InjectVideoLatent`, `H3PerFrameDenoise`, `H3FaceMaskSAM`, `H3FaceTransformInfo`. Chain: `VHS_LoadVideoPath` â†’ `H3FaceTrackCrop` (per-frame face crop, 512Â² canvas, `auto_capped_768`, crop_factor 0.35) â†’ `MiniMaxH3ReferenceToVideo` â†’ `H3InjectVideoLatent` (real frames â†’ img2img) â†’ `MiniMaxH3NativeAudioLock` (audioâ†’lipsync) â†’ `H3PerFrameDenoise` (0.8â†’0.35 by face size) â†’ `er_sde` 4-step / denoise 0.45 â†’ `VAEDecode` â†’ `H3FaceStitch` (face_only, feather 24px) â†’ `VHS_VideoCombine`. Key dials: base denoise 0.45, crop_factor 0.35, canvas `auto_capped_768`, turbo LoRA @ 0.75, `paste_region=face_only`.
2. **Character / Background swap** â€” `minimax_h3_sam_r2v_cinematic.json`. Node pack = **`yujianvip/ComfyUI-SetGet-Resolver`** (cloned; pure frontend `GetNode`/`SetNode`, right-click canvas). Chain: `VHS_LoadVideoFFmpeg` (driving video) â†’ `SAM3_VideoTrack` (person, thr 0.5) â†’ `SCAIL2ColoredMask` â†’ `ImageInvert` â†’ `ImageAddNoise` â†’ `ImageCompositeMasked` â†’ `MiniMaxH3ReferenceToVideo` (refs = character sheet, masked video as `ref_video`) â†’ `CreateVideo` â†’ `VAEDecode` â†’ `SaveVideo` (+ `RTXVideoSuperResolution` 2Ã— ULTRA). `ComfySwitchNode` toggles Char Replace (True) / Background Replace (False). Prompt = "omni" structure (subject_definitions, summary `[video editing]`, integrated_multimodal_description, overall_soundscape with dialogue `<Subject 1> says <d>[Language] transcript</d>`, non_diegetic_music).

### Reason

The user wants close-up shots (face detailer) and character/background swap (SAM R2V) available as reference/build-on-top workflows for the Malayalam channel intro. Both were sourced from the community (reddit) and needed their model paths remapped to our layout.

### Model-path remaps applied (backups saved as `*.pre-remap.bak`)

- **SAM R2V** (7 nodes): UNET `minimax_h3_fl2va_pruned_int8_convrot.safetensors`; LoRA `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`; video VAE `minimax_h3_video_vae_fp16.safetensors`; audio VAE `minimax_h3_audio_vae_fp32.safetensors`; CLIP `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`; SAM3 `sam3.1_multiplex_fp16.safetensors`; the NSFW `MysticXXX_MMH3-V3` LoRA (strength 0, no-op) repointed to the valid turbo LoRA so validation passes.
- **Face Detailer** (2 nodes): LoRA `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`; UNET `minimax_h3_fl2va_pruned_int8_convrot.safetensors`. (Detector `bbox\face_yolov8m.pt` already matched our `models/ultralytics/bbox/` layout.)
- **FaceRefine pip deps** installed into embedded Python: `insightface`, `scenedetect>=0.7` (`ultralytics` + `scipy` were already present).

### Validation status

- **SAM R2V** validates with all model paths resolving. Only error = node 153 source video (`scene_13_begging_clip01_trimmed.mp4` not in our `input/`) â€” user-specific driving clip. Two non-blocking warnings (SAM3 type-annotation on node 182; dangling `VAEDecodeAudio` node 121 in the original).
- **Face Detailer** reports the 4 H3Face nodes as `unknown_class_type` â€” these resolve **after a ComfyUI restart** loads the newly-cloned FaceRefine pack. 5th error = node 8 source audio (`GATONIEL_2.wav`), user-specific.

### Result

**Rule: the two packs are cloned into `custom_nodes` and both workflows' model paths point at our real files. A ComfyUI restart is REQUIRED for the H3Face nodes to register (verify `H3FaceTrackCrop`/`H3FaceStitch`/`H3InjectVideoLatent`/`H3PerFrameDenoise`/`GetNode`/`SetNode` appear in `/object_info` after restart). The source video/audio widgets are user-specific placeholders â€” set them to the actual clip before running. VDN-H3 setup is DEFERRED to a later step (benchmark VDN vs the SLA < 240 s baseline).**

---

## D045 â€” NEVER run a ComfyUI workflow while a Qwen/llama.cpp session is active (contaminates benchmarks)

Date: 2026-09-06
Status: Active (HARD RULE)

### Decision

**Never submit a ComfyUI workflow (via MCP `run_workflow`/`run_template` or the UI) while a local Qwen/llama.cpp session is running.** The two compete for the same GPU + CPU + memory, so BOTH slow down: the LLM's reasoning gets sluggish AND the ComfyUI render gets slower. Any generation time measured under this contention is **contaminated and unusable** for a speed comparison.

### Reason

The user's explicit instruction (2026-09-06): "you should never run the workflow parallely when an active qwen session is going on, it will affect both the usecase, your thinking will get slow, comfyui will also be slow." This was triggered when the VDN-H3 t2v benchmark (1MP, 124 frames, 8 steps) was submitted while Qwen was active and came back at **418.22 s** â€” a number the user correctly judged unusable ("from this, I cannot come to a conclusion"). The 418 s is NOT a valid VDN figure.

### Alternatives considered

- Running the benchmark anyway and noting the caveat (rejected â€” the user wants a clean number to compare against the SLA < 240 s baseline, D042).
- Reducing the workload to fit under the contention (rejected â€” still contaminated).

### Result

**Rule: before submitting ANY ComfyUI workflow for a timed/benchmark run, confirm no Qwen/llama.cpp session is active (stop it first). For benchmark comparisons (VDN vs SLA, etc.), the run MUST be done with the LLM idle so the time is clean. If a run was submitted during an active LLM session, discard its timing and re-run clean. The user will run the VDN benchmark manually (workflow `vdn_h3_t2v_benchmark.json`) to get the correct number.**

### VDN-H3 setup state (recorded 2026-09-06)

- **Node pack:** `Saganaki22/ComfyUI-VDN-H3` **v1.4.0** cloned into `custom_nodes` (no new Python deps â€” runs on ComfyUI's existing torch + safetensors). Defines `ApplyVDNH3` (simple) + `ApplyVDNH3Advanced` (ablations + fast kernels).
- **Checkpoint (int8 ConvRot 8-step stage):** `E:\ComfyUI_windows_portable\ComfyUI\models\vdn\vdn-minimax-h3-int8-convrot-comfyui\` (source `drbaph/vdn-minimax-h3-int8-convrot-comfyui` on HF). 7 files, ~3.49 GB total: `model_spec.json` (25,705 B), `linear_branch/model_int8_convrot_comfyui.safetensors` (2.30 GB), `linear_branch/config.json`, `adapters/turbo/adapter_model.safetensors` (851 MB) + config, `adapters/default/adapter_model.safetensors` (334 MB) + config. All verified byte-for-byte against the HF API.
- **Why int8 ConvRot (not bf16 `OpenVDN/vdn-minimax-h3`):** (1) matches our int8_convrot base model; (2) ~4.7 GB more VRAM headroom (8.3 GB free vs 3.6 GB â€” critical for the ~20 GB base + VAEDecode spike on the 32 GB card); (3) ~1.2Ã— faster (branch matmuls 2.7Ã— faster); (4) smaller download (2.2 vs 4.3 GB); (5) identical output at same seed. bf16 is the fallback if int8 misbehaves.
- **Benchmark workflow:** `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\vdn_h3_t2v_benchmark.json` â€” validates clean (16 nodes, 0 errors). Chain: UNETLoader(`minimax_h3_fl2va_pruned_int8_convrot`) â†’ `ApplyVDNH3Advanced` â†’ `MiniMaxChunkFeedForward`(2, 4096) â†’ BasicGuider â†’ SamplerCustomAdvanced; BasicScheduler also takes model from the chunk node. `ApplyVDNH3Advanced` widgets: `["vdn-minimax-h3-int8-convrot-comfyui", true, 1, 1, "merge", "auto", "auto", true, "grouped", 1, 5, "both", true, true, false]` (turbo ON, **merge** required for the 8-step DMD stage, **fast_kernels OFF** â€” README warns it drifts on 8-step DMD on torch 2.10). **14 s = 345 frames** (14Ã—24=336, snapped up to the 17k+5 grid â†’ 345) at **1344Ã—768 (1MP)** â€” set to match the PROVEN production workload `jaisal_single_shot.json` (14 s @ 1344Ã—768 @ turbo, the workload the SLA ~250 s number was measured on) so the speed comparison is apples-to-apples. 8 steps, `er_sde`, `beta` scheduler, fixed seed 981445682258077. t2v mode (no first/last frame). NO-music prompt (D041).
- **Run 1 (contaminated):** 124 frames (5 s), 418.22 s â€” INVALID (Qwen was active). Discarded.
- **Run 2 (clean, 345 frames / 14 s / 1344Ã—768):** **OOM at step 0** (184.21 s to fail). The linear-branch readout (`branch.py:159 frame_statistics`: `torch.matmul(vb.transpose(-1,-2), kf).float()`) holds per-frame K/V statistics for all F=102 frames in fp32 â†’ ~31.4 GiB, blowing the 31.84 GiB limit. The vendor's ~95 s reference is 61 frames (Fâ‰ˆ19) â€” 5Ã— fewer frames.
- **CONCLUSION: VDN-H3 is NOT viable at our production scale (14 s / 1MP) on the 32 GB card â€” it OOMs.** Its linear-branch memory scales with frame count (worse for longer clips â€” the opposite of where we need it). **SLA remains the default speed stack (D042).** Do NOT adopt VDN for 14 s / 1MP production clips.
- **If a clean VDN number is still wanted (tomorrow):** set `branch_weights="stream"` (widget idx 5) + `retain_buffers="off"` (idx 6) to cut linear-branch memory, and/or drop to 124 frames / 1280Ã—736. Stop the Qwen session first (D045). Full details in `EXPERIMENTS.md` (2026-09-06 VDN-H3 entry).

## D046 â€” Intro-video pipeline: character consistency via ComfyUI-Continuity (no LoRA), 2K via SeedVR2 TensorRT Studio, Semantic Bridge = i2v-only

Date: 2026-09-06
Status: Active (research conclusions â€” do NOT re-research)

### Decision

For the **channel-intro monologue video** (natural face, close-up + medium shot, the user's own voice), the pipeline is:
1. **Character consistency WITHOUT a LoRA â†’ `ComfyUI-Continuity`** (`roadmaus/ComfyUI-Continuity`, renamed from `ComfyUI-MiniMax-Creator`). Cast-based, `@`-references, drift guard, **supports MiniMax H3, fully local**, no pip install. This is the Reddit approach the user found.
2. **Generate â†’ the SLA i2v workflow** (`jaisal_single_shot.json`, ~200 s, D042).
3. **Upscale to 2K â†’ `VRGDG-SeedVR2-TensorRT-Studio`** (`github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio`) â€” a **standalone Windows app** (NOT a ComfyUI node): one-click `Install SeedVR Studio.bat` + `Launch SeedVR Studio Pro.bat`, drop the video in, render 2K. **~8 min for an 8 s clip â†’ 2K on the RTX 5090** (7B Sharp FP16). Run it AFTER ComfyUI generation.
4. **Audio** (today's main goal).

### Reason

- **Upscaler:** `RTXVideoSuperResolution` (installed + registered) is FAST but does NOT add detail / natural look (user-confirmed limitation). SeedVR2 TensorRT Studio is the fully-local path that ADDS detail and is still fast (~8 min/8 s/2K on the 5090).
- **RefMods / `.char` (malcolmrey/minimaxh3, `ComfyUI-MiniMaxH3Mod` pack, `MiniMaxH3RefModsLoader`+`MiniMaxH3RefModApply`, `models/refmods/`):** these are **pre-encoded reference-latent adapters (~1.5 MB each), ZERO-TRAINING, instant-load** â€” NOT a LoRA, NOT a dataset. **BUT the public ones are for OTHER people's characters (celebrities); there is NO clear public tool to create one for OUR OWN character â†’ DEAD END for our boy.** (Answer to the user's "is this for training our own dataset or LoRA?" = **neither**.)
- **Semantic Bridge (`speach1sdef178/MiniMax-H3-Semantic-Bridge`):** a conditioning-space adapter that improves prompt adherence. **SCOPE: i2v/FL2VA (text-conditioned) ONLY â€” does NOT work for Ref2VA/reference-conditioned (R2V) workflows** (model card: "Ref2VA / reference-conditioned workflows are not supported"). So it helps `jaisal_single_shot.json` (i2v) but NOT `jaisalproduction1/2.json` / `jaisal_lowangle.json` (R2V). Installed: pack `custom_nodes\MiniMax_H3_Semantic_Bridge` + adapter `E:\comfyUi_latest\...\models\semantic_bridge\MiniMaxH3_SemanticBridge_v1.safetensors`. Wired into a SEPARATE `jaisal_single_shot_semantic.json` (bridge node 300 on the conditioning path, alpha 0.10, per_token); the working `jaisal_single_shot.json` was RESTORED clean (backup `workflow_backups\jaisal_single_shot.pre_semantic_bridge.json`).
- **FastVideo-FastH3 (t2v) = NOT a fit:** t2v-only (FL2VA/Ref2VA not distilled), built for 4Ã—B200 datacenter GPUs in the FastVideo runtime (not ComfyUI), needs the VSA-H3 backend. Our SLA + turbo LoRA already does 4-step t2v at ~200 s on one card.

### Alternatives considered

- **RefMods for our own character** (rejected â€” no public tool to create a RefMod for a custom character; only celebrity ones exist).
- **RTX upscaler for 2K** (rejected as the primary â€” fast but no detail/natural look; keep as the quick-preview option).
- **Semantic Bridge on the R2V production workflows** (rejected â€” not supported for reference-conditioned generation).

### Result

**Rule: for the intro video â€” character consistency via ComfyUI-Continuity (no LoRA), generate via SLA i2v, upscale to 2K via SeedVR2 TensorRT Studio (local), then audio. Semantic Bridge is i2v-only. RefMods are a dead end for our own character. FastVideo-FastH3 is not a fit.**

### GOTCHA (two ComfyUI instances)

The **running** ComfyUI is the **`comfyUi_latest`** instance â€” its models dir is `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models`, NOT the main `E:\ComfyUI_windows_portable\ComfyUI\models` path. **Put models in the `comfyUi_latest` path or you get "Missing Models".** (This is why the Semantic Bridge adapter first showed "Missing Models" â€” it was in the main path.)

---

## D047 â€” Character voices: create our own via a small curated reference set (timbre swap, not TTS)

Date: 2026-09-06
Status: Active (reference-sourcing approach pending user confirmation)

### Decision

For the 15-character bilingual movie, do NOT rely on 15 friends' voice messages. Instead **create our own character voices** by curating a small set of DISTINCT reference voices (~4â€“6: young male, older male, young female, older female), assigning one per character (similar characters can share a voice type), and cloning each character's lines onto their reference via **voice conversion (timbre swap)** â€” OpenVoice V1 (zero-shot, validated 2026-09-06) for quick tests, RVC/GPT-SoVITS for final quality. The user dubs ALL characters (Malayalam + English) in their own voice; only the timbre is swapped.

### Reason

- The user dubs well and wants to dub almost all characters themselves; a timbre swap keeps their performance (pace/emotion/expression = the acting) and only changes the voice color â†’ **non-robotic by design** (the dub is the "soul", the reference only provides the color).
- 15 distinct friends' voices is hard to source and hard to keep consistent; a small curated set is easier to manage and consistent (same reference for all of a character's lines).
- Female voices are just a female reference sample â€” same pipeline, nothing special.
- The OpenVoice two-way test (premâ†”jaisal) came out GOOD (user-confirmed), validating the zero-shot VC path.

### Alternatives considered

- **15 friends' voice messages** (rejected â€” hard to source, consistency risk, user prefers to dub all).
- **TTS per character (IndicF5/Svara)** (fallback only â€” TTS is less "the user's performance"; use for characters with no reference or if VC underperforms).
- **Reference sourcing:** (a) record real samples [CHOSEN 2026-09-07 â€” from VOICE NOTES]; (b) TTS speaker profiles as references (no recording, synthetic base); (c) public datasets (licensing caveats).

### UPDATE (2026-09-07) â€” reference source = voice notes

The user chose **(a) real samples from voice notes** (WhatsApp/Telegram .ogg/.m4a). Voice notes are PROVEN (the first successful test used two Opus voice notes). Collection pipeline built + tested: `collect_references.py` (batch-clean a folder of voice notes â†’ 16 kHz mono reference files) + `convert_character.py` (per-character dubâ†’reference-voice conversion). See `AUDIO_PIPELINE_PLAN.md` (VOICE STRATEGY section).

### Result

**Rule: create our own character voices from a small curated reference set (male/female/old/young) + the user's dubs + timbre-swap VC (OpenVoice now, RVC/GPT-SoVITS final). More/cleaner reference samples (30 sâ€“1 min mono) = better, more consistent results. Same reference for all of a character's lines.** See `AUDIO_PIPELINE_PLAN.md` (VOICE STRATEGY section).

## D048 â€” OpenVoice timbre-swap: clean SOURCES + multi-clip reference (no music, no TTS base)

Date: 2026-09-07
Status: Active (v3 Malayalam fix built + run; user to listen)

### Decision

For OpenVoice timbre-swap to produce NATURAL, non-robotic output, the **SOURCE** must be clean speech and the **REFERENCE** must be a list of short clean clips:

1. **Multi-clip reference (not one long file):** pass the individual clean reference clips as a LIST to `extract_se` (per-clip embedding, then averaged). Never one long concatenated file â€” the `ref_enc` encoder was trained on short coherent utterances, so a 158 s heterogeneous blob â†’ one blurry embedding â†’ output stays close to the source with a muddy tint ("robotic / forcing a different audio").
2. **Clean source (no music):** movie/source audio with a music bed â†’ run **Demucs** `--two-stems=vocals` FIRST, then convert the clean vocals. Timbre-swap keeps the source's CONTENT and only swaps the voice color, so a music bed comes through as HUMMING.
3. **No TTS base for natural lines:** for a natural English line, use a REAL human dub as the source (not MeloTTS). `convert()` keeps the source PROSODY and only swaps color â†’ a robotic TTS base = robotic output.

### Reason

- The good premâ†”jaisal test (user-confirmed) used a single ~6 s clean clip â†’ clean embedding â†’ good result. The bad Jaisal test used a 158 s concatenated reference â†’ blurry embedding â†’ robotic.
- Spectral analysis (`scripts\analyze_source.py`) confirmed the movie clip `reference.ogg` has a music bed (flatness 0.0132, RMS std 2.6 dB) â†’ the "only humming" in the v2 output.
- MeloTTS base is robotic (centroid 2600 Hz, flatness 0.067) â†’ "foreigner speaking".

### Alternatives considered

- **One long concatenated reference** (rejected â€” blurry embedding).
- **MeloTTS base for English** (rejected for natural lines â€” robotic prosody).
- **Convert movie audio directly** (rejected â€” music bed â†’ humming).

### Result

**Rule: for OpenVoice timbre-swap â€” (1) multi-clip reference as a LIST, (2) Demucs `--two-stems=vocals` on any source with music, (3) real human dub (not TTS) for natural lines.** Tools: `scripts\convert_multi_ref.py`, `scripts\english_test_multi.py`, `scripts\analyze_source.py` (diagnostic). v3 Malayalam output: `03_audio_processed\ml_reference_vocals_in_jaisal_v3.wav` (clean, no humming). See `AUDIO_PIPELINE_PLAN.md` (JAISAL VOICE TEST v3 section).

## D049 â€” Malayalam words: IndicF5 TTS (correct words) + OpenVoice (voice color); OpenVoice alone CANNOT do Malayalam words

Date: 2026-09-08
Status: Active (IndicF5 test in progress; batch Jaisalâ†’Midhun done)

### Decision

OpenVoice is an **English-centric timbre swap** â€” it does NOT understand Malayalam words, it only swaps voice color in the frequency domain. For Malayalam (retroflex consonants, allophonic variations, complex consonant combinations), that swap **distorts the phonemes** â†’ the voice changes correctly but the WORDS get mangled. **Flipping the conversion direction does NOT fix this** (it's a tool limitation, not a direction issue).

**The fix:** use **IndicF5** (Malayalam-native TTS, proper G2P) to generate the words CORRECTLY first, then **OpenVoice** to swap the voice color. Pipeline: user dubs line â†’ `clean_audio.py` â†’ Whisper transcribe â†’ IndicF5 speaks the text in the character's voice (Malayalam) / OpenVoice or GPT-SoVITS (English).

**Best-option recommendation (production house):**
1. **IndicF5 = Malayalam workhorse** (only Malayalam-native tool we have; zero-shot `model(text, ref_audio, ref_text)` = correct words + character voice).
2. **GPT-SoVITS = English workhorse** (production-ready, zero-shot + few-shot; Malayalam support uncertain â€” test before committing).
3. **Main character (user) = use clean dub directly** (no conversion = highest quality).

**Reference sourcing:** Midhun's audio (`D:\voice_notes\mithun_audio\`, 3 EN + 2 ML, comprehensive) is the current test reference. **Prem audio CANNOT be used** (no permission). The user's **52-letter idea** (record 5 files covering all 52 Malayalam letters per character) gives a more complete voice embedding â†’ better conversion.

### Reason

- User confirmed (2026-09-08): "the voice is good, we can see change, but the wordings are not correct... the dialogue lacks the perfection of the letters they speak in malayalam."
- OpenVoice `convert()` preserves source CONTENT (words + prosody) and only swaps TIMBRE â€” a frequency-domain swap that mangles Malayalam phonemes.
- IndicF5 is explicitly Malayalam-native (fine-tuned for 11 Indian languages) â†’ correct G2P â†’ correct words.
- The user is an alone warrior aiming for Cannes â€” voice is the last piece (image/video models are in place).

### Alternatives considered

- **OpenVoice alone for Malayalam** (rejected â€” mangles words).
- **Flipping the conversion direction** (rejected â€” doesn't fix the tool limitation).
- **GPT-SoVITS for Malayalam** (uncertain â€” test before committing; use for English).
- **A2TTS / OmniVoice** (depsek suggestions â€” not yet evaluated; IndicF5 is already installed and Malayalam-native).

### Result

**Rule: for Malayalam dialogue â€” IndicF5 TTS (correct words) + OpenVoice (voice color). For English â€” user's dub + OpenVoice (or GPT-SoVITS). Main character = clean dub directly. More/cleaner reference samples (52-letter coverage) = better results.** See `AUDIO_PIPELINE_PLAN.md` (VOICE STRATEGY + 2026-09-08 sections).

---

## D050 ï¿½ Voice pipeline: VC (RVC/OpenVoice) for the movie, TTS (IndicF5/S2 Pro) for future kids content

Date: 2026-09-08
Status: Active

### Decision

**For the current 15-character bilingual movie: use VOICE CONVERSION (VC), not TTS.** The user performs ALL 15 characters' dialogue themselves (they are alone in this project, have the script, no one else is involved). VC preserves the user's performance (emotion, timing, delivery, Malayalam pronunciation) and only changes the voice identity (timbre) to the character's voice.

**For future kids videos / content where natural voice is NOT needed: use TTS** (IndicF5 for Malayalam, Fish S2 Pro for multilingual) ï¿½ text-to-speech, no performance required.

**VC tool choice: RVC (primary) over OpenVoice (fallback).** RVC is the established VC tool ï¿½ it preserves prosody (rhythm, pitch contour, emotion) while changing only timbre. OpenVoice is a pure timbre swap that keeps the user's skeleton (confirmed limitation: output "still sounds like me"). RVC trains a per-character model from 10+ min clean audio.

**Workflow (per character):**
1. User records 10+ min clean audio of the target voice (or uses existing references like Midhun's).
2. Train RVC model on that audio (F0 extraction via RMVPE + HuBERT content features + FAISS index).
3. User dubs the character's lines (headset, quiet room, dry).
4. clean_audio.py (denoise + loudnorm + 16 kHz mono).
5. RVC converts the dub ? character's voice (preserving user's performance).
6. LatentSync lip-sync ? DaVinci Resolve mix.

**Key insight (user + DeepSeek agreed):** TTS fails at Malayalam because the AI doesn't understand Malayalam prosody/pronunciation. VC sidesteps that entirely ï¿½ the USER speaks the Malayalam (correct pronunciation, natural emotion), and RVC just changes the voice color. This is NOT a trade-off ï¿½ it's exactly what the user wants ("without it it feels like we are doing some blind translation").

**Two-track system:**
| Track | Tool | Use case |
|-------|------|----------|
| **VC (movie)** | RVC (primary) / OpenVoice (fallback) | 15-character movie ï¿½ user performs, VC changes voice |
| **TTS (future)** | IndicF5 (ML) / Fish S2 Pro (multilingual) | Kids videos, content where natural voice not needed |

### Reason

- User confirmed (2026-09-08): "this is not the trade off, this is what actually wants... 15 voice overs i can do that because only i have the script and other people wont get involved here, its me, im alone in this."
- TTS (Fish S2 Pro) Malayalam output sounds non-native (Tamilian accent, flat flow) ï¿½ a general multilingual model approximating Malayalam.
- VC preserves the user's actual performance (acting, emotion, timing) ï¿½ the "soul" of the dialogue ï¿½ and only changes the voice identity.
- RVC is the established open-source VC tool (used by AI voice cover creators), RTX 5090-ready (~20 GB VRAM inference).
- User can dub a kid character and "he can go away" ï¿½ the RVC model persists, no need for the kid to remember/read lines.

### Alternatives considered

- **TTS for the movie** (rejected ï¿½ Malayalam quality is the bottleneck; AI doesn't understand ML prosody).
- **OpenVoice for the movie** (fallback ï¿½ pure timbre swap, keeps user's skeleton, "still sounds like me").
- **Seed-VC / ApexSVC** (zero-shot alternatives ï¿½ no per-character training, but lower quality ceiling than trained RVC).
- **Sarvam API** (rejected ï¿½ cloud API, user wants local).

### Result

**Rule: movie = VC (RVC primary, OpenVoice fallback) ï¿½ user performs all 15 characters, RVC changes voice identity. Future kids content = TTS (IndicF5/S2 Pro). See AUDIO_PIPELINE_PLAN.md (VOICE STRATEGY + 2026-09-08 sections).**

---

## D051 â€” The assistant runs ON the local Qwen: NEVER stop Qwen myself (user runs GPU jobs manually)

Date: 2026-09-08
Status: Active

### Decision

The local Qwen (`llama-server`) is the LLM that powers THIS assistant. If it is killed, the user **cannot talk to me anymore**. Therefore the assistant must **NEVER execute a command that stops/kills Qwen** (e.g. `Stop-Process -Name "llama-server"`), and must **NOT run GPU scripts that stop Qwen as a side effect** (e.g. `run_indicf5_gpu.ps1`, which stops Qwen in step 1 and restarts it in step 4).

### Correct workflow for any GPU-heavy job (ComfyUI, RVC, IndicF5, etc.)

1. Assistant PROVIDES the exact stop command as text for the user to run MANUALLY in their own terminal: `Stop-Process -Name "llama-server" -Force`
2. User runs it themselves (this temporarily cuts off the chat â€” expected and acceptable).
3. User runs the GPU job themselves (or tells the assistant it's done).
4. User restarts Qwen MANUALLY: `Start-Process "D:\models\qwen\Qwen3.827BMTP.bat"`

The assistant only ever PROVIDES these commands as text. It does not execute them.

### Reason

- User confirmed (2026-09-08): "youre running locally on my GPU, if i kill that task i cannot talk to u."
- The assistant's own inference depends on the local Qwen process staying alive.
- This supersedes the old pattern where GPU scripts auto-stopped/restarted Qwen â€” that pattern is now UNSAFE because it can kill the assistant's own runtime.

### Alternatives considered

- **Assistant auto-stops Qwen in a script** (rejected â€” kills the assistant's own LLM, user loses the chat).
- **Run GPU jobs while Qwen is active** (rejected â€” D045, contaminates benchmarks + both slow down).

### Result

**Rule: for any GPU job, the assistant gives the user the stop/run/restart commands to run MANUALLY. The assistant never executes a Qwen stop. See user-preferences.md (CRITICAL: I run ON the local Qwen).**

---

## D052 â€” RVC inference needs the WRAPPED checkpoint, not the raw G_*.pth

Date: 2026-09-08
Status: Active

### Decision

For RVC inference via `infer/cli.py`, ALWAYS use the **wrapped** inference
checkpoint (`assets/weights/<exp>.pth`), never the raw training checkpoint
(`logs/<exp>/G_*.pth`). The raw checkpoint is `{"model": {weights}, ...}`;
`infer/cli.py` `load_model_metadata()` requires the wrapped format
`{"weight": {...}, "config": [18 values], "info", "sr", "f0", "version"}`.

### Reason

- `train/process_ckpt.py savee()` is what produces the wrapped format, but it
  crashed on a missing `assets/weights/` dir, so the wrapped model was never
  saved â€” only the raw `G_2333333.pth` existed.
- `infer/cli.py` reads `checkpoint["weight"]["emb_g.weight"]`; the raw file
  has no `weight` key â†’ `Model does not contain weight/emb_g.weight`.
- **DeepSeek's "copy G_*.pth into assets/weights" was WRONG** â€” copying the raw
  file still fails (no `weight` key). The raw weights must be UNWRAPPED from
  `["model"]` and re-wrapped into the savee() format.

### Fix (applied, no re-run needed)

`scripts\wrap_ckpt.py` (rvc venv, CPU-only) reads `G_2333333.pth`, unwraps
`["model"]`, rebuilds the savee() format, saves to `assets/weights/midhun_v1_40k.pth`.

### Naming rule (CRITICAL)

The wrapped model MUST be named `<experiment>.pth` (e.g. `midhun_v1_40k.pth`),
**NOT** `<experiment>_e10.pth`. `infer/vc/utils.py get_index_path_from_model()`
strips `_e\d+_s\d+$` (requires BOTH `_e` AND `_s`); an `_e10`-only suffix is
not stripped, so the FAISS index auto-match fails. Named `midhun_v1_40k.pth`, the
index `assets/indices/midhun_v1_40k_added_IVF66_Flat_nprobe_1_midhun_v1_40k_v1.index`
matches via `startswith(experiment + "_added_")`.

### Verified

`python -m infer.cli --model midhun_v1_40k.pth --list-speakers` â†’ `0-108`
(CPU-only, loads the model, exits before GPU work).

### Inference command (user runs, Qwen stopped)

`cd D:\models\ai-movie\repos\rvc-webui; D:\models\ai-movie\envs\rvc\Scripts\python.exe -m infer.cli --model midhun_v1_40k.pth --input <source_wav> --output D:\models\ai-movie\03_audio_processed\rvc_midhun_test.wav --f0-method rmvpe --protect 0.33 --index-rate 0.75`

### Result

**Rule: RVC inference = wrapped `assets/weights/<exp>.pth` (named without `_eN`),
auto-matched index. Build it with `scripts\wrap_ckpt.py` if `savee()` never ran.**

---

## D053 â€” RVC voice quality: more Midhun data is the biggest lever; test the real source first

Date: 2026-09-08
Status: Active

### Decision

The Midhun RVC model (`midhun_v1_40k`, ~3.5 min training data) produces a
recognizable Midhun voice but **quirky words** on a Jaisal source. This is NOT
the ceiling. **Do NOT retrain immediately** â€” first test the REAL production
source (the user's own dub), because the quirkiness is largely a SOURCE
articulation mismatch (Jaisal's words + Midhun's timbre), not a model limit.

### Reason

- RVC is **audioâ†’audio** (no text): the source provides words/rhythm, the model
  provides the voice identity. A Jaisal source â†’ Jaisal articulation + Midhun
  timbre = quirky. A user dub â†’ user articulation + Midhun timbre = the real
  production result.
- Model stability is limited by ~3.5 min of training data (2 clips).
- **Two levers:** (1) MORE MIDHUN DATA (biggest) â€” 5â€“10 min clean, diverse
  speech (Malayalam + English, different topics/emotions/speeds) â†’ more
  consistent, more Midhun-like, less quirky; (2) TUNING (quick, no retrain) â€”
  `--index-rate 0.9` (stronger Midhun pull), `--protect 0.4`,
  `--f0-method pm` (A/B vs rmvpe).

### Workflow

1. **Test the real source first:** user dubs a line (headset, quiet room) â†’
   `clean_audio.py` â†’ RVC convert â†’ listen. If good â†’ done, use for the movie.
2. **If still weak:** collect 5â€“10 min clean, diverse Midhun speech â†’
   `collect_references.py` â†’ retrain via `rvc_train_midhun.py` (point at the
   new trainset) â†’ re-test.
3. **Tune** (no retrain): `--index-rate 0.9`, `--protect 0.4`,
   `--f0-method pm`.

### Result

**Rule: RVC quirkiness = source articulation + model stability. Test the real
source (user dub) before retraining. More clean, diverse Midhun data is the
biggest quality lever.**

---

## D054 â€” Intro video: Krea2 Identity Transfer (not LoRA) + Qwen3-VL prompt engine + Shot Composer

Date: 2026-09-10
Status: Active

### Decision

For the **Jaisal Kut channel-intro video** (`docs/INTRO_SCRIPT.md`, ~67s, B&W,
no music, 7 shots, JAISAL + CAMERA GUY):

1. **Character consistency = Krea2 Identity Transfer workflow**
   (`krea2_identity_edit.json`, Identity Edit v1.2) â€” NOT a LoRA. A Krea2 **LoRA**
   is reserved for the **movies** (full consistency across 100+ shots). The intro
   is short, so identity transfer (ref_boost 4.0, style LoRA @ 0.7) is enough.
   Reference set = `E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1`
   (20 PNGs).
2. **Qwen3-VL as the H3 prompt engine** â€”
   `D:\models\Writing\Qwen\Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf` +
   `...-mmproj-F32.gguf` (a VLM fine-tuned for MiniMax H3 â†’ emits H3-optimized
   prompts). Wire it into the H3 ComfyUI pipeline so prompts are H3-tuned.
3. **Shot Composer (open-media) = the "Blender way"** â€”
   `https://github.com/Anujatk1999/open-media` (browser-based local 3D
   shot/pose/camera composer, mannequin.js + three.js, MCP server). Previsualize
   the hard shots (3 head-twist, 5/6 plants, 7 object assembly) â†’ export
   MP4/PNG â†’ feed to H3 as a motion/pose reference.

### Reason

- The intro has hard VFX items (180Â° head twist, object assembly, plant
  growth/death, perfect reverse) that H3 alone will struggle with. Identity
  transfer keeps the character consistent without a training run; Shot Composer
  gives H3 an explicit motion reference for the hard shots; Qwen3-VL makes the
  H3 prompts adhere better.
- Shot 4 (perfect reverse) is done in **POST** (reverse the forward take), not
  asked of H3.
- B&W look applied in post (consistent across shots) or baked into the Krea2
  keyframes.

### Result

**Rule: intro = Krea2 Identity Transfer + Qwen3-VL prompts + Shot Composer motion
references + H3 (SLA) + RVC audio + diegetic SFX (NO MUSIC). Movies = Krea2 LoRA.**
Full plan: `project-memory/INTRO_VIDEO_PRODUCTION.md`.

## D055 â€” Intro video voice assignment: JAISAL = user's own voice, CAMERA GUY = Midhun (RVC)

Date: 2026-09-11
Status: Active (HARD RULE)

### Decision

The user is **alone** on this project â€” they write the stories, turn them into
scripts, direct, and check the camera (with AI help). They **dub ALL the
dialogue** themselves. Voice assignment for the Jaisal Kut intro:

1. **JAISAL (the main character, most of the dialogue) = the USER'S OWN VOICE.**
   The user dubs every JAISAL line (Malayalam + English). These are cleaned
   (`clean_audio.py`) and used as-is (the user's real voice) â€” NOT Midhun.
2. **CAMERA GUY (off-screen, asks the questions) = MIDHUN'S VOICE.** The user
   dubs the camera-guy lines (in their own voice), then RVC converts them to
   Midhun via the existing `midhun_v2_40k` model. **No second RVC model is
   needed** â€” we reuse `midhun_v2_40k` for the camera guy.

This **supersedes** the 2026-09-10 plan (Â§10b #1) that had JAISAL = Midhun and
CAMERA GUY = a new 26-yo male model. The roles are effectively swapped: the
main character now carries the user's own voice (they're the face/voice of the
channel), and the off-screen interviewer carries Midhun.

### Reason

- The user is the sole writer/director/performer; the main character is an
  extension of them, so their own voice is the natural fit and avoids a
  "not-me" feel on the hero.
- Midhun (`midhun_v2_40k`, 6.5 min data, already trained + wrapped) is a
  ready-made distinct voice for the interviewer â€” no new training run needed.
- RVC is audioâ†’audio: the user's camera-guy dub provides words/rhythm,
  `midhun_v2_40k` paints Midhun's timbre.

### Result

**Rule: JAISAL = user's own voice (cleaned dub). CAMERA GUY = user's dub â†’
RVC `midhun_v2_40k` (Midhun). The user dubs ALL lines.**

### Process decision (dub-first)

Because this is a fully post/AI pipeline (video is cheap + regenerable, unlike
traditional film where footage is the scarce asset), the **audio is the timing
spine**: each shot's duration is set by how long its line takes to say. So the
order is **dub first â†’ lock shot durations from the audio â†’ generate
keyframes + video to match â†’ SFX + assembly**. A quick B&W tone test (1-2
Krea2 keyframes) runs in parallel to lock the look while the dubs are recorded.

## D056 â€” Intro keyframes v4: scene-consistency lock + per-shot minimal change + head-180 effect

Date: 2026-09-11
Status: Active

### Decision

After the v3 keyframe review (2026-09-11), the v4 set is built with these hard rules:

1. **The BASE/scene-master image is the anchor** â€” it must be STRAIGHT-ON, centered, symmetric, eye-level, NO wall, NO tilt, pure blackness outside the light pool. The v3 base (kf1_scene_master_00001_.png) was rejected (tilted side shot with a wall). Regenerate it FIRST; every other shot is an identity-edit of it (or of a good shot) so the scene stays identical.
2. **Consistency lock in EVERY prompt** â€” bulb position (center-top, same height), table (same size/position/centered), ONE chair (centered, no extra chairs anywhere), character (dark wavy hair, black full-sleeve shirt unbuttoned halfway). No extra changes per shot â€” only the specified change.
3. **kf6 = identity edit OF kf5** â€” same composition, only the plants become dead + melancholy emotion. NOT a fresh generation (v3's kf6_00001 came out completely different).
4. **kf7 props** â€” ALL props (bat, ball, smiley paper, mic) SMALL and ON the table, not blocking the character; ONLY ONE mic at the table.
5. **kf3b head effect** â€” the HEAD ALONE rotated 180Â° (face visible from behind, body/shoulders stay facing away â€” an impossible pose), NOT a normal shoulder look-back.
6. **No dedicated head-rotation LoRA exists on Civitai** (API search 2026-09-11: only unrelated character/pose LoRAs). kf3b is attempted PROMPT-FIRST; if Krea2 can't hold the impossible pose, options are: (a) a custom Krea2 LoRA trained on a few head-180 reference images, (b) Shot Composer (3D) for the twist, (c) post compositing (cut the head, rotate, paste).

### Reason

The v3 set had: off-center chair (kf1), extra chairs (kf2/kf5/kf6_00002), visible walls (kf2/kf6_00001), plants too small (kf5), kf6 composition drift, kf7 props too big + 2 mics + giant robot figure, and a tilted/walled base image. The user's rule: "I don't want to mess it up again" â€” so the scene is locked to ONE anchor image and each shot changes exactly one thing.

### Alternatives considered

- Fresh t2i per shot (rejected â€” composition drift, the v3 problem).
- Custom LoRA for the head-180 effect (deferred â€” no public LoRA found; prompt-first, then custom LoRA / Shot Composer / post-composite fallbacks).

### Result

**Rule: v4 = regenerate the base image straight-on first, then identity-edit each shot from the anchor with the consistency lock; kf6 edits kf5; kf7 props small + one mic; kf3b = head-only 180Â° (prompt-first, no public LoRA exists).**

---

## D057 â€” Intro keyframes v5: TRAIN A KREA 2 LoRA for a natural (non-plastic) character look

**Date:** 2026-09-12

**Decision:** The Krea2 Identity-Edit keyframes look **plastic / AI-ish** on the
character. The user wants a **natural** look for the intro video. **NEXT STEP =
train a Krea 2 LoRA** (character + natural-look) if the identity-edit route can't
crack the natural look. The user explicitly said: "update the project, that we
need to train a KREA 2 lora."

**Context / findings (2026-09-12):**
- **Available Krea 2 LoRAs locally** (`E:\ComfyUI_windows_portable\ComfyUI\models\loras\`):
  `Krea2_Cinematic_Artstyle.safetensors`, `krea2_darkbrush.safetensors`,
  `krea2_identity_edit_v1_2.safetensors`, `krea2_lineart_v1_fp16.safetensors`,
  `Typnosis_Krea2.safetensors` (unknown purpose â€” no metadata). **No dedicated
  "natural / camera / realism" Krea 2 LoRA is installed.**
- **FameGrid "Spice" Krea 2 LoRA** (Reddit r/StableDiffusion, "corrected release",
  2026-09-12): the user shared this as a candidate for a natural look. **Could not
  scrape the Reddit/Civitai page (JS-rendered / 403) â€” the user should open the
  link and confirm what it does + download it.** If it's a natural/realism LoRA
  for Krea 2, test it in the identity-edit workflow (node 71 LoraLoaderModelOnly)
  before training.
- **1-click dataset workflow exists:** `1 Click Dataset (Klein 9b).json` (Flux 2
  Klein) â€” the user builds character datasets with it. **Check whether a Krea 2
  equivalent exists** for building the training set.
- **v5 started:** `utilities/build_intro_keyframes_v5.py` (copy of v4, writes
  `_v5` files). **kf2 V5 = character looking at the chair, BOTH hands on the
  table** (user's spec). Generated `kf2_seated_v5_00001_.png` â€” pose correct,
  natural look, clean void.

**Alternatives considered:**
- Use an existing natural/camera LoRA (none installed for Krea 2 â€” see above).
- Test the FameGrid Spice LoRA first (pending user confirmation of what it is).
- Train a custom Krea 2 LoRA (character + natural look) â€” **the chosen next step**.

**Status:** PENDING â€” (1) user confirms the FameGrid Spice LoRA + downloads it;
(2) test it in the identity-edit workflow; (3) if insufficient, build a Krea 2
training dataset (1-click dataset workflow) + train the LoRA.

---

## D058 â€” Intro keyframes v7: CHARACTER shots use the character ref ONLY (no scene anchor)

**Date:** 2026-09-12

**Decision:** CHARACTER keyframes (kf2, kf3a/b/c, kf5, kf5a, kf6, kf7a/b/c) use
the **character ref ONLY** (node 72 = full `intro_char_ref_bw.png`, node 113/92
BYPASSED). **Do NOT anchor character shots to the empty base** â€” the scene anchor
breaks the character identity.

**Root cause (user-confirmed 2026-09-12):** the scene anchor (node 113 = the
empty base `intro_scene_master.png` = table+chair+bulb, NO person) FIGHTS the
character ref ("put a person here" vs "empty room") â†’ the face distorts / becomes
a different person. Evidence: V3 (char ref only) = GOOD character; V4/V5/V6
(char ref + empty-base scene anchor) = BROKEN character; V7 (char ref only, V3
settings) = GOOD character again.

**The V3 tradeoff (user accepted):** V3's character is good, but the scene has a
wall (right) + chair (left) + plant. Fixing walls/chair/plant WITHOUT a scene
anchor = **PROMPT-ONLY** (stronger negatives: no wall, one chair centered). Do
NOT "fix" the scene by adding a scene anchor â€” it breaks the character.

**V7 = the good-character base** (`utilities/build_intro_keyframes_v7.py`,
workflows `krea2_intro_kf*_v7.json`). Built from V3's exact settings.

**Alternatives considered:**
- Scene anchor for consistency (REJECTED â€” breaks the character, the user's #1
  priority).
- Face-only char ref crop (REJECTED â€” also broke identity; see
  `krea2-identity-face-crop-failure.md`).

**Status:** V7 character VERIFIED good (`kf2_seated_v7_00001_.png`). NEXT: fix
walls/chair/plant via prompt-only in V7, regenerate the set, then MiniMax H3.

---

## D059 â€” Head-rotation keyframes: hands/90Â° SOLVED via identity-edit; 180Â° face-at-camera UNSOLVED by Krea2

**Date:** 2026-09-12

**Decision:** For the Shot-3 head-twist keyframes, anchor identity-edit on the
**GOOD FRAME** (not a fresh t2i): `kf2_hands_table` anchored on
`kf2_00004_ref.png` (the good manual-inpaint front view); `kf3c_head90` +
`kf3b_head180` anchored on `kf3a_headnormal_v7` (the perfect back view).
**A 180Â° head rotation with the face at the camera CANNOT be done by Krea2
identity-edit** â€” it over-rotates to ~270Â° (face sideways). Use manual inpaint
or let MiniMax H3 do the 90â†’180 motion in video.

**Results (user-verified 2026-09-12):**
- `kf2_hands_table` = âœ… GOOD (both hands flat on table, facing camera).
- `kf3c_head90` = âœ… GOOD (back view, head ~90Â° side profile). The camera in the
  image is at 180 (back view), NOT 90 â€” user ACCEPTS this; the camera motion is
  the MiniMax H3 CAMERA NODE's job (`H3LocalCameraEditor`, installed 2026-09-12,
  needs ComfyUI restart + `camera_motion_h3_lora_v1_3000_pruned.safetensors`).
- `kf3b_head180` = âŒ UNSOLVED. Anchored on the back view + "face looking
  STRAIGHT AT THE CAMERA over the shoulder" + negatives (face in profile, 270
  degree rotation, head over-rotated) â†’ seeds 501/601/602 ALL over-rotated to
  ~270Â° (face sideways). The body-stays-back constraint fights the head rotation.

**Root cause:** Krea2 identity-edit is CONSERVATIVE and holds the reference's
head orientation; asking it to rotate the head 180Â° while keeping the body in
back view is an impossible pose it resolves by over-rotating sideways.

**Alternatives for kf3b (when back):**
- (a) MANUAL INPAINT on kf3a (like the kf2 chair black-fill) â€” mask the head
  region, prompt "face turned around over shoulder looking at camera" (most
  controllable; matches how kf2 was solved).
- (b) Fresh t2i of the back-view-with-face-around (no anchor).
- (c) ACCEPT kf3c 90Â° as the only twist anchor and let MiniMax H3 do the
  90â†’180 motion itself (simplest â€” H3 is good at head turns in video).

**Consolidated folder (user's request â€” ONE path):**
`d:\models\vsCodeMcp\Jaisal-intro\kf2_headset\` = `kf2_hands_table.png`,
`kf3a_headnormal.png` (anchor), `kf3c_head90.png`, `kf3b_head180.png` (bad â€”
replace when solved).

**Workflows:** `krea2_kf2_hands_table.json`, `krea2_kf3c_head90.json`,
`krea2_kf3b_head180.json` (identity-edit clones; node 82 = [1928,1088,1],
ref_boost 4, grounding 768, Image Comparer node 114 BYPASSED mode=4 â€” the
submit script crashes on its type name otherwise). Build scripts:
`utilities/build_kf2_head_rotation.py`, `utilities/build_kf3_head_rotation.py`,
`utilities/run_kf3b_180_seeds.py`. Submit: `utilities/submit_krea2_workflow.py`.

**Status:** hands + 90Â° DONE. 180Â° UNSOLVED (pick option a/b/c when back).

---

## D060 â€” VoiceStudio added to the voice arsenal (local ElevenLabs alternative)

**Date:** 2026-09-12

**Decision:** Add **VoiceStudio** (github.com/debpalash/VoiceStudio, 23.8k stars,
AGPL-3.0, fully local) to the voice arsenal as a 5th option alongside RVC,
OpenVoice, IndicF5, Fish S2 Pro. It is a real local ElevenLabs alternative:
16 TTS engines (default **OmniVoice** = 600+ languages incl. Malayalam; also
CosyVoice 3, GPT-SoVITS, VoxCPM2, IndexTTS 2.5, etc.), 11 ASR engines, video
dubbing pipeline (transcribe â†’ translate â†’ preserve speakers â†’ synthesize â†’
export), zero-shot voice cloning from a 3-15s clip, voice design, MCP server
(`http://localhost:3900/mcp`) + OpenAI-compatible API
(`http://localhost:3900/v1`).

**Why:** the movie is bilingual (Malayalam + English). OmniVoice's 600+ language
coverage + zero-shot cloning (no training, unlike RVC) makes it a strong
candidate for the character voices. The user's hypothesis: it may be the best of
all 5. **Keep it READY in the arsenal; A/B test against RVC `midhun_v2_40k`
before committing.**

**Install (DONE 2026-09-12):** current-user MSI (NO admin) â†’
`C:\Users\user\AppData\Local\VoiceStudio (Current User)\omnivoice-studio.exe`.
MSI downloaded to `D:\models\VoiceStudio\VoiceStudio_Current_User_0.5.2_x64_en-US.msi`
(177.9 MB). Launched â€” first-run creates the Python env (via `uv`) + downloads
the default OmniVoice model (watch the splash). GPU = NVIDIA/CUDA-only on
Windows (our RTX 5090 gets CUDA accel; no CUDA Toolkit install needed).
Backend runs loopback-only on `localhost:3900`.

**First voice (when the app is up):** Voice Cloning tab â†’ add a clean 5-15s
reference clip (e.g. a Midhun or Jaisal clean wav from
`D:\models\ai-movie\references\`) â†’ enter text â†’ pick language (Malayalam /
English) â†’ Generate.

**Triton/torch.compile OOM note (Windows):** if an engine OOMs on first
synth, Settings â†’ Performance â†’ "Disable torch.compile (Windows)" (sets
`TORCH_COMPILE_DISABLE=1`).

**MCP (optional, later):** add to `.vscode\mcp.json` â†’
`{"voicestudio": {"url": "http://localhost:3900/mcp"}}` (or the stdio shim
`python -m backend.mcp_shim`).

**Status:** INSTALLED + LAUNCHED. NEXT: confirm first-run bootstrap finished,
clone a test voice, A/B vs RVC.

---

## D061 â€” kf3b 180Â° head shot: 2nd face reference + head-REPLACEMENT prompt (2026-09-13)

Date: 2026-09-13
Status: Active (workflow ready, awaiting user's manual seed runs)

### Decision
For the kf3b horror 180Â° head shot, use a **TWO-reference** identity-edit setup:
- **Node 72 (primary/scene):** `kf3a_v7_back_ref.png` (the back-view frame being edited).
- **Node 113 (secondary/identity):** `jaisal_face_mono_closeup.png` â€” a monochrome
  face-only close-up cropped from the CORRECT character
  (`E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1\Image_00001_.png`).
- **Node 79 = `[3, 1, fit]`** â€” `ref_boost` (3) applies to the LAST ref = the
  FACE (strong identity copy); `ref_boost_a` (1) applies to the FIRST ref = the
  scene (off, just the editing base).
- **Node 84 prompt = the user's WORKING head-REPLACEMENT prompt** (frames it as
  "replace only the head with a frontal view of the same man's face... looking
  directly into the camera... body/shoulders/torso facing completely away"), NOT
  "rotate 180 degrees" (which made Krea2 over-rotate to 270Â°).

### Reason
The single-reference attempts (D059) all over-rotated to ~270Â°. The user found
that (a) describing the END STATE (face at camera) instead of the rotation amount,
and (b) feeding a monochrome face close-up as a 2nd reference so the model COPIES
the actual face instead of hallucinating one, gets much closer.

### Key facts
- `Krea2EditModelPatch` boost semantics (from object_info): `ref_boost` = LAST
  ref (subject/face), `ref_boost_a` = FIRST ref (scene). `fit_mode` = `fit`.
- `ref_boost_mask` = optional region on the LAST ref to boost (e.g. the face).
- Face ref script: `utilities/make_mono_face_ref.py` (crop + grayscale +
  autocontrast). Project copy: `Jaisal-intro\kf2_headset\jaisal_face_mono_closeup.png`.
- **CORRECT character = `character_1` dataset** â€” NOT the Krea2 renders in
  `input/` (jaisal_face_*.png etc. are a DIFFERENT face). See repo memory
  `jaisal-correct-character-reference.md`.

### Status
Workflow `krea2_kf3b_head180.json` validated clean. User runs seeds manually.
If all seeds fail â†’ fallbacks (a) manual inpaint on kf3a head region, (b) fresh
t2i, (c) accept kf3c 90Â° + MiniMax H3 does the 90â†’180 motion.

---

## D062 â€” VoiceStudio model selection: OmniVoice + Whisper large-v3 only (2026-09-13)

Date: 2026-09-13
Status: Active

### Decision
For the Jaisal movie (Malayalam + English, 2 characters), install ONLY:
- **OmniVoice** (default, k2-fsa, 2.4 GB) â€” 600+ langs incl. Malayalam, zero-shot.
- **Whisper large-v3** (faster-whisper, 2.9 GB) â€” transcription for dubbing.
- **Whisper Tiny** (0.1 GB) â€” dictation shortcut only (90+ langs, auto-detect).

### Reason
The app "recommends" a broad list for all users, but for our specific job the
other engines are redundant or wrong-language: KittenTTS (English-only), Whisper
Turbo/Tiny/medium/small/base (redundant with large-v3), Parakeet/Moonshine/
Zipformer/Paraformer (EN/ZH dictation), VoxCPM2/GPT-SoVITS/MOSS/dots.tts/
Confucius4 (other-language TTS), pyannote (multi-speaker video only). CosyVoice 3
(9.8 GB) is the only optional A/B but only 9 langs (mostly NOT Malayalam) â€” skip.

### Notes
- OmniVoice weights = CC-BY-NC (non-commercial â€” fine for the movie).
- VoiceStudio is NOT ElevenLabs â€” it's a free local 80-90% alternative. Its real
  value: (1) 5th engine for A/B, (2) unified dubbing pipeline, (3) API/MCP
  (localhost:3900) so the agent can drive it, (4) voice design (textâ†’voice).
- **Convert tab is NOT a true voice conversion** â€” it transcribes (Whisper) then
  re-synthesizes (TTS), so emotion/delivery is LOST. For true voice conversion
  (keep performance, change timbre) use **RVC**.
- **Emotion on the default OmniVoice engine:** the #1 lever is an
  emotionally-performed reference clip (flat ref â†’ flat output). Plus punctuation
  + `[pause Nms]`, `class_temperature` 0.3-0.7 + seed farming, `[laughter]`/
  `[sigh]` tags, `whisper` style, `postprocess_output` off. The default engine
  does NOT accept `[happy]`/`[sad]`/`[excited]` tags (it speaks the word).
  IndexTTS 2.5 emotion sliders = no Malayalam.
- Summary doc for asking DeepSeek/OpenAI: `Jaisal-intro\voicestudio_summary.md`.

---

## D063 â€” RVC source-leakage recipe: protect 0.0 + double pass (2026-09-13)

Date: 2026-09-13
Status: Pending A/B confirmation (recipe built, winner not yet locked)

### Decision
To reduce RVC source leakage (output still sounding like the user), use:
1. **Clean the source** (denoise, normalize, mono) before conversion.
2. **`--protect 0.0`** (the #1 fix â€” default 0.33 means "keep 33% of the
   original voice", which is the leak).
3. **`--index-rate 0.7-1.0`**, `--f0-method rmvpe`, pitch 0.
4. **Double pass** â€” run the output through the same model a 2nd time (protect
   0.0 again) to strip residual source character.
5. **Light post** â€” high-pass 80-100 Hz, loudness normalize.

### Reason
RVC's Protect parameter is the main source-leakage dial. A double pass is the
classic fix for "still sounds a bit like me".

### Status
A/B test pending (tomorrow): same line, 3 ways (single pass / double pass /
double pass + post). Winner gets LOCKED as the standard RVC conversion pipeline
for the movie (consistency across all lines). If leakage persists after the
double pass, the ceiling is the target model quality â†’ retrain on cleaner/longer
data.

---

## D064 â€” C: drive cleanup: freed ~90 GB, pagefile stays on C: (2026-09-13)

Date: 2026-09-13
Status: Done

### Decision
Freed ~90 GB on C: (was 135 GB free â†’ now 215 GB free):
- HF cache `.cache\huggingface` (36.3 GB) â€” deleted (re-downloads on demand).
- pip cache (23.9 GB) â€” `pip cache purge`.
- Temp (5.4 GB) + CrashDumps (2.8 GB) â€” deleted.
- **hiberfil.sys (24.6 GB) â€” `powercfg /h off`** (hibernation disabled; safe,
  reversible with `powercfg /h on`).
- **pagefile.sys (61.8 GB) â€” KEPT on C:** (user's decision). It's functional
  (virtual memory), NOT junk. Moving it is fiddly + risky; resizing needs admin +
  reboot. At 215 GB free there's no need.

### Reason
The "missing 90 GB" was the two hidden system files at C:\ root (pagefile 61.8 +
hiberfil 24.6 = 86.4 GB) â€” not in the user folder. SSDs don't slow down until
~85-90% full, so boot speed was never at risk (was ~73% full).

### Notes
- uv cache (6.1 GB) + npm cache (1.3 GB) cleanup optional (uv not on PATH â†’
  delete `AppData\Local\uv\cache` directly; npm blocked by execution policy â†’
  use `npm.cmd`).
- VoiceStudio (~17 GB) fits easily in the 215 GB free.

---

## D065 â€” SeedVR2 single-IMAGE upscaling via the numz ComfyUI pack (not the Studio app)

**Date:** 2026-09-13

**Decision:** For 2K/4K upscaling of **single keyframe images**, use the
**`numz/ComfyUI-SeedVR2_VideoUpscaler`** ComfyUI nodes (installed 2026-09-13),
NOT the SeedVR2 TensorRT Studio app. The Studio app is video-oriented and its
image jobs failed on model loading (`7B Sharp FP16` â†’ `invalid python storage`).
The numz pack explicitly supports single images (`batch_size=1`).

**Why:** The Studio app's `POST /api/jobs` image submissions errored at 0.28
progress (model-load crash). The numz pack's `SeedVR2VideoUpscaler` node +
`SeedVR2LoadDiTModel`/`SeedVR2LoadVAEModel` handle a single image with
`batch_size=1` (per the official docs: "Use 1 only for single images").

**Setup done (2026-09-13):**
- Cloned `numz/ComfyUI-SeedVR2_VideoUpscaler` â†’
  `E:\comfyUi_latest\...\custom_nodes\seedvr2_videoupscaler`.
- Installed missing dep `rotary_embedding_torch` (0.9.1).
- **Fixed a transformers 5.9.0 bug** that blocked the import:
  `PACKAGE_DISTRIBUTION_MAPPING["flash_attn"]` KeyErrors when flash_attn is not
  installed. Patched 3 lines (988/1019/1030) in
  `transformers/utils/import_utils.py` â†’ `.get("flash_attn", [])`. Backup at
  `import_utils.py.flash_attn_bak`. (Re-apply after any transformers upgrade.)
- Restarted ComfyUI so the 9 SeedVR2 nodes register.

**Workflow:** `seedvr2_image_upscale.json` (UI format, validated clean) built by
`utilities/build_seedvr2_image_wf.py <input.png> [prefix]`. Native widget shapes
(from the official `example_workflows/SeedVR2_simple_image_upscale.json`):
- LoadImage `["<img>","image"]`
- SeedVR2LoadDiTModel `["<model>","cuda:0",0,false,"none",false,"sdpa"]`
- SeedVR2LoadVAEModel `["ema_vae_fp16.safetensors","cuda:0",false,1024,128,false,1024,128,"false","none",false]`
- **SeedVR2VideoUpscaler `[42,"randomize",1440,2560,1,false,"lab",0,0,0,0,"cpu",false]`**
  (13 values â€” hidden "randomize" after seed, same pattern as KSampler)
- SaveImage `["<prefix>"]`

**Settings:** `seedvr2_ema_7b_sharp_fp16.safetensors` (max quality, local),
resolution 1440 / max 2560 (2K), batch_size 1, color_correction `lab`,
attention `sdpa`.

**CLI alternative (no ComfyUI):**
`python custom_nodes\seedvr2_videoupscaler\inference_cli.py <img> --dit_model seedvr2_ema_7b_sharp_fp16.safetensors --resolution 1440 --max_resolution 2560 --batch_size 1 --color_correction lab`
(needs `PYTHONIOENCODING=utf-8` on Windows).

**Status:** Active. Workflow validated `valid: true`. Next: run it on the plant
keyframes, copy 2K outputs to `Jaisal-intro\v9\`.

---

## D066 â€” Object-ref images: UNSEEN top light, NO visible bulb (2026-09-14)

**Decision:** All Krea2 t2i object-reference images (soccer ball, cricket bat,
paper-smiley â€” `krea2_object_refs.json`) are lit from directly above by a single
**UNSEEN** light source. The bulb/lamp itself must NOT appear in the frame â€” only
its light and hard shadow.

**Reason:** A visible bare bulb in the object refs confuses MiniMax H3 when the
objects are composited into the scene (it tries to reconcile two light sources /
a bulb that isn't in the scene). The light *effect* (top-down, hard shadow) is
kept; the *source* is removed.

**Implementation:**
- Positive prompts: "Lit from directly above by a single UNSEEN light source â€”
  the light itself is NOT visible in the frame, only its light and hard shadow."
- Negatives: `light bulb, bare bulb, lamp, visible light source, ceiling, cord,
  wire, hanging bulb, bulb in frame`.

**Alternatives considered:** keeping the bulb for consistency with the scene
keyframes (rejected â€” H3 confusion outweighs consistency); a side light (rejected
â€” breaks the top-down look of the whole film).

**Status:** Active. Applies to all future object/prop reference images.

---

## D067 â€” Two new H3 node packs installed: H3-Relight + Neons Style Explorer (2026-09-14)

**Decision:** Installed two custom-node packs into the RUNNING install
(`E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\`):
1. **`H3-Relight-Minimax-ComfyUI`** (NyckM / bruxosdovfx, v1.1.2) â€” a 3D
   lighting studio for MiniMax H3: up to 3 lights on a 3D dome + reference
   sphere + a relight prompt for H3 Edit, following MiniMax's Relight skill.
   Nodes: `H3RelightEditor` ("Relight H3 Â· BruxosDoVFX"), `H3SunPosition`
   ("Sun / Sol H3 Â· BruxosDoVFX"). Deps `numpy` + `tzdata` â€” BOTH already
   present in the embedded Python (numpy 2.2.6). Purpose: better lighting when
   the final act comes in.
2. **`ComfyUI-NeonsStyleExplorer`** (Neon-Sparks, v2.4.5) â€” a hand-written
   style-prefix catalog (natural language or booru tags) + preview gallery.
   Nodes: `NeonsStyleExplorer`, `NeonsStyleExplorerEncode`,
   `NeonsGalleryCapture`, `NeonsLoraExplorer`. Pure Python, NO extra deps.
   Purpose: different styles for a SEPARATE video concept (not the current
   intro).

**Reason:** Relight = future lighting control for the intro's final act;
StyleExplorer = style variety for other concepts.

**Status:** Cloned + verified (node classes confirmed in `__init__.py`/
`nodes.py`). **NEEDS A COMFYUI RESTART** to register the nodes (user runs it â€”
D051). After restart, verify via `/object_info` that `H3RelightEditor`,
`H3SunPosition`, `NeonsStyleExplorer` are live.

**NOTE:** the Relight `__init__` registers a `/bruxos_h3/sun` route via
`PromptServer.instance` â€” that only exists inside a running ComfyUI, so an
out-of-context import test raises `AttributeError: type object 'PromptServer'
has no attribute 'instance'`. That is a FALSE ALARM; the pack loads fine when
ComfyUI starts it.

---

## D068 ï¿½ Intro shot C (180ï¿½ twist) = camera node + SLA speed stack (2026-09-14)

**Decision:** The 180ï¿½ head-twist shot (Shot C) uses the `H3LocalCameraEditor`
camera node (`minimaxH3Camera_v20.json` subgraph template) with the attention
backend swapped to our proven **H3SLAAttention** speed stack (sparsity 0.90,
block 32, dense_backend `comfy_kitchen`) and the LoRA set to
`minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`.

**Reason:** The shared camera template referenced `EastMoeSolAttn` (from the
uninstalled `eastmoe/ComfyUI-Sol-Attn` pack) and a missing
`fl2v_turbo_8step` LoRA. Rather than install a new pack, we reuse the SLA
stack already in every production workflow (D042) ï¿½ no new dependencies, same
~4 min/shot speed.

**Implementation:** `utilities/patch_intro_C_sla.py` patches the subgraph
internal nodes (138 EastMoeSolAttn?H3SLAAttention, 121 LoRA?4step turbo).
Camera trajectory: azimuth 0?90?180 over the take, distance 1?0.8 (slight
push-in), source image `jaisal_head_left_back_side.png`.

**Status:** Active. `jaisal_intro_C_headtwist_180.json` validates clean.

---

## D069 ï¿½ Intro shots run at 1 MP (not 2 MP); refs ONLY from the keyframes folder (2026-09-14)

**Decision:** All 10 intro shot workflows run at **1 MP** (`ResolutionSelector`
megapixels = 1, 16:9). The R2V node's width/height are LINKED from the
ResolutionSelector, so this is the real resolution control. All reference images
come from ONE place: `D:\models\vsCodeMcp\Jaisal-intro\keyframes\` (14 files).

**Reason:** User ran shot A at 2 MP and it took **2.3 min for 12%** ï¿½ too slow.
User confirmed **1 MP / 0.98 MP is what works** for MiniMax H3. Also the builder
had left a stray template ref `jaisal_4_middle.png` (node 148) in A/B/D/E/F/G/H/I
that is NOT in the keyframes folder ï¿½ user: "do not mix it up, all keyframes kept
in one place."

**Implementation:** `utilities/fix_intro_workflows.py` (run 2026-09-14):
(1) ResolutionSelector megapixels 2 -> 1 on all 10; (2) removed the stray
`jaisal_4_middle.png` LoadImage + its link + cleared the R2V ref slot it fed;
(3) fixed the prompt bug `<Subject 1> is <Subject 1> is` -> `<Subject 1> is`.
Also wired J's 4th ref (`obj_paper_smiley` node 151) whose `ref_image_3` input
`link` field was `None` while link 303 existed (multi-ref slot-index bug) ->
set `ref_image_3.link = 303`.

**SLA note:** SLA IS correctly wired (LoRA -> H3SLAAttention -> BasicGuider ->
Sampler) and enabled ï¿½ the slowness was the 2 MP resolution, NOT SLA.

**Status:** Active. All 10 validate clean (0 errors; J's orphan warning resolved).

---

## D070 ï¿½ Intro shot length bug: hidden math node forced 15s on every shot (2026-09-14)

**Decision:** The R2V node's `length` input must be UNLINKED from the hidden
`ComfyMathExpression` node so each shot uses its WIDGET length value.

**Reason:** The builder left the R2V `length` input LINKED from a
`ComfyMathExpression` (node 131) fed by a `PrimitiveFloat` (node 132) = **15
(seconds)**. The math node computed `max(5, round(15*24))` = 360 -> 362 frames
= **15.1s**, OVERRIDING the widget. So every shot ran at 15s even though the
widget showed the correct per-shot length (A=124=5.2s, B=73=3s, D=175=7.3s,
E=311=13s, F=430=17.9s, G/H/J=73=3s, I=56=2.3s). User: "i dont want to repeat
again and again, we need a 5 second video, you created a 15 second video."

**Implementation:** `utilities/fix_intro_lengths.py` (run 2026-09-14) set the
R2V `length` input `link` to `None` on all 9 R2V shots (A,B,D,E,F,G,H,I,J).
The orphaned math node 131 + primitive 132 are left in place (harmless - the
server prunes them; validation shows 2 `node_not_reachable` warnings, no
errors). Shot C is the camera node (length is camera-driven, no change).

**Status:** Active. All 9 R2V shots now run at their widget length.

---

## D071 ï¿½ Use the purpose-built H3 prompt model for R2V prompts (2026-09-14)

**Decision:** Generate/refine MiniMax H3 R2V prompts with
`Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf` (14.93 GB) + its
`mmproj` (2.38 GB) at `D:\models\Writing\Qwen\`, launched via
`run-minimax-h3-heretic.bat` (llama-server on **port 8104**, ctx 32768).

**Reason:** Hand-crafted R2V prompts kept getting the structure wrong - a generic
"school kid" instead of OUR character, and `<Picture N>` tags that didn't match
the actual reference images. This model is a **vision-language** model
fine-tuned on MiniMax H3 prompt data, so we feed it the ACTUAL reference images +
a short shot description and it writes a proper 6-section H3 prompt that matches
what's really in the images. It is a SEPARATE llama-server (port 8104) - it does
NOT stop Qwen, and it's a quick job (not a long render), so it's fine to run
while Qwen is up.

**Implementation:** `utilities/gen_h3_prompt.py` (single shot: `--desc` +
`--refs` in `<Picture N>` order -> OpenAI-compatible chat API on 8104) +
`utilities/gen_all_h3_prompts.py` (batch all 10; refs ONLY from the keyframes
folder, 2-3 per shot per D020). Shot descriptions in
`Jaisal-intro\prompts\shot_descriptions.txt`. Output:
`Jaisal-intro\prompts\shot_<X>.txt`.

**Status:** Active. Scripts built + parser verified. Awaiting the model being
launched on 8104, then run `gen_all_h3_prompts.py`.

---

## D072 ï¿½ Pruned H3 model CANNOT generate prompts; use hand-crafted R2V prompts (2026-09-14)

**Decision:** The `Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49` model is **pruned**
(layers 0-49, NO `output_norm`, NO `lm_head`) - it is a **text encoder only**
(for ComfyUI conditioning via the `Nif00/ComfyUI-GGUF` fork), NOT a text
generator. It CANNOT write prompts. The `run-minimax-h3-heretic.bat` fails with
`tensor 'output_norm.weight' not found` because the model has no output head.

**Reason:** Inspected the GGUF tensor list: `output_norm: 0`, `lm_head: 0`,
layers 0-49 (50 layers). The HF repo (`nif0/Qwen3-VL-32B-Instruct-MiniMax-H3-GGUF`)
confirms: "Pruned layers after 49 as they arent needed for use with MiniMax H3"
and "Can be used in ComfyUI with my fork of City96's ComfyUI-GGUF."

**Implementation:** Wrote all 10 R2V prompts by hand via
`utilities/write_intro_prompts.py` (output: `Jaisal-intro\prompts\shot_<X>.txt`).
Each prompt: (1) describes OUR character (Jaisal: short dark hair, rose-pink shirt,
black trousers, black bag) - not a generic "school kid"; (2) tags `<Picture N>`
to the ACTUAL reference images for that shot, in order; (3) uses the proper 6-section
H3 R2V structure, tight (no 500-word bloat); (4) NO MUSIC (D041). Shot J has exactly
4 refs (mic-alone start + 3 object refs) - the END state is described in words, never
tagged with a `<Picture N>` that has no matching image. Wired into the 9 R2V
workflows via `utilities/wire_intro_prompts.py` (node 138 = PrimitiveStringMultiline).
Shot C (camera node) left as-is (camera-driven prompt).

**Status:** Active. All 9 R2V workflows validate clean (0 errors; 2 harmless
`node_not_reachable` warnings from the orphaned math nodes 131/132).

---

## D073 ï¿½ Intro shot lengths: per-shot widget values (2026-09-14)

**Decision:** Each intro shot uses its WIDGET length value (not the hidden 15s math
node). Per-shot lengths: A=124f (5.2s), B=73f (3s), D=175f (7.3s), E=311f (13s),
F=430f (17.9s), G=73f (3s), H=73f (3s), I=56f (2.3s), J=73f (3s). Shot C = camera
node (length camera-driven).

**Reason:** The builder left the R2V `length` input LINKED from a hidden
`ComfyMathExpression` (node 131) fed by `PrimitiveFloat` (node 132) = 15
seconds -> computed 362 frames = 15.1s, OVERRIDING the widget. User: "we need a 5
second video, you created a 15 second video."

**Implementation:** `utilities/fix_intro_lengths.py` unlinked the R2V `length`
input on all 9 R2V shots. The orphaned math node 131 + primitive 132 are left in
place (harmless - the server prunes them).

**Status:** Active. All 9 R2V shots now run at their widget length.

## D074 â€” MiniMax H3 audio: the model's own prior adds music; fix = strengthen the audio sections + ControlFoley post (2026-09-14)

**Decision:** The "music" the user hears in a generated shot is NOT from the prompt
(the prompt already says `non_diegetic_music: NO music...` and a natural-only
`overall_soundscape`). It is the **MiniMax H3 model's own audio prior** â€” H3
generates NATIVE audio and has a strong "add a cinematic score / ambient music
bed" bias that a thin soundscape line cannot fully suppress.

**Fix (two layers):**
1. **Prompt layer (applied to all 10 shots):** make `overall_soundscape` a
   CONTINUOUS natural bed that fills the whole shot edge-to-edge (room tone,
   bulb hum, chair scrape, breath, creak) so there is no "gap" for the model to
   fill with music; and make `non_diegetic_music` an EXPLICIT exhaustive
   no-music list (NO score, NO background music, NO ambient music, NO cinematic
   score, NO soundtrack bed). `wire_intro_prompts.py` re-wires all 9 R2V shots.
2. **Post layer (the reliable fix):** the H3-native audio is unreliable for the
   no-music rule. The PROVEN path is **ControlFoley TEXT-ONLY SFX** (see
   `build_controlfoley_textonly.py`): strip the H3 audio (`ffmpeg -an`), generate
   a clean natural-SFX bed from a text prompt (with a music-free negative prompt),
   and mux it onto the video. This is the production audio path for the intro.

**Reason:** User: "we want surrounding sound or digestive sound but no music, but
i hear a music." The prompt was already correct, so the music is model-side.

**Status:** Active. Prompt layer applied to all 10 shots. ControlFoley post is the
fallback if a re-run still has music.

## D075 â€” MiniMax H3 RAM spike (~56 GB) is model weights + activations; prevent by freeing between shots (2026-09-14)

**Decision:** Running a MiniMax H3 R2V workflow spikes system RAM to ~56 GB,
forcing a ComfyUI restart before Qwen can come back up. This is EXPECTED, not a
bug.

**Why (measured model sizes):**
- UNET `minimax_h3_ref2va_pruned_int8_convrot.safetensors` = **19.53 GB**
- CLIP `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` = **14.61 GB**
- LoRA `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` = **1.82 GB**
- Total weights â‰ˆ **36 GB** â€” which EXCEEDS the 32 GB RTX 5090 VRAM. So ComfyUI
  loads the weights into system RAM first (safetensors â†’ RAM), then streams the
  layers that fit into VRAM and keeps the OVERFLOW in system RAM. That overflow
  (weights that don't fit in 32 GB VRAM) is the dominant RAM consumer. On top:
  the video latents (1344Ã—768 Ã— 124 frames) + audio latents + SLA attention
  buffers + Python/PyTorch overhead. That is how it reaches ~56 GB.
- **CORRECTION (2026-09-14):** an earlier note said "the 32B Qwen3-VL text
  encoder runs on CPU (RAM)" â€” that was WRONG. The CLIP text encoder runs on
  GPU like the rest. The real reason for the RAM spike is the 36 GB of weights
  exceeding the 32 GB VRAM (forcing RAM offload) + the generation working set.

**Prevention (do NOT restart ComfyUI between shots â€” just free memory):**
1. **Between shots:** call `free_memory` (MCP) â€” unloads the UNET/CLIP/LoRA from
   VRAM and resets the executor cache. This drops the working set so the next
   shot reloads cleanly without a full restart.
2. **Before Qwen:** after the LAST shot, `free_memory` again, then restart Qwen.
   The weights are reloaded on demand per shot, so you do NOT need to restart
   ComfyUI to bring Qwen back â€” just free the models first.
3. **Do NOT run Qwen + H3 simultaneously** (D045 / user rule) â€” they compete for
   the 32 GB VRAM and system RAM. Stop Qwen for the H3 batch, restart it after.
4. **Batch the shots:** run all 10 shots in ONE ComfyUI session (free_memory
   between each) rather than restart-per-shot â€” faster and avoids the restart
   churn.

**Status:** Active. Use `free_memory` between shots and before restarting Qwen.

## D076 â€” MiniMax H3 acting = VISUAL micro-expressions + AUDIO emotion tags, fused (2026-09-14)

**Decision:** To make Jaisal's face ACT (not just pose), use the r/StableDiffusion
"pushing AI emotions" technique: **one fused sentence** describing the subtle facial
movement *while* the line is delivered, with audio emotion tags inside the dialogue.
Full guide: `docs/MINIMAX_H3_MICRO_EXPRESSIONS.md`.

**Key rules:**
1. **LEAD WITH THE EYES** â€” the eyes are the primary micro-expression channel
   ("his eyes shift first, then the head rotates").
2. **FUSE** the micro-expression with the action/dialogue (not a separate "he looks
   sad" note).
3. **Dialogue format** `<d>[Language] ... </d>` with emotion tags inside
   (`<breath>`, `<pause>`, `<long pause>`, `<sighs>`, `<i>word</i>`, `<stutter>`,
   `<catches breath>`, `<softer>`, `<mhm>`, `<phew>`, etc.).
4. **NO MUSIC (D041):** do NOT use `<humming>` / melody tags in the intro â€” only
   natural-speech tags.
5. **Melody/humming** needs a `ref_audios` reference (`<Audio 1>`) â€” NOT used here.

**Per-shot micro-expressions** (in the doc): A=wary entry + breath; B=calm still
look; C=**the hook** (eyes shift first, head rotates SLOWLY 180Â°, eyes stay locked);
D=expression eases back to ordinary; E=wonder, eyes follow the stem, softening
smile; F=weight of limitation, slow breath, gaze drops, subtle frown; G=faint wry
half-smile, small shrug, then vanishes.

**AUDIO PATH (decide per-shot, do NOT change workflows yet):**
- **Path 1 â€” MiniMax NATIVE audio:** dialogue in the prompt as `<d>[Language] ...
  </d>`; MiniMax generates voice + lip motion. Fast, but a GENERIC voice (NOT the
  user's), Malayalam likely weak.
- **Path 2 â€” VC + LatentSync (D050):** user dubs Malayalam â†’ RVC/OpenVoice â†’
  LatentSync lip-sync. The user's ACTUAL voice, correct Malayalam.
- **The VISUAL micro-expressions apply in BOTH paths** â€” always prompt them.
- **NEXT:** run shot A first (visual micro-expressions only, no dialogue), judge the
  face acting, THEN pick the audio path.

**Settings note:** the post uses 30 steps + First Block Cache + res_multistep +
sage2++ + NO LoRA + a custom FL2VAâ†’REF2VA FP8 finetune. We keep our turbo 4-step +
SLA speed stack (D014) â€” the ACTING comes from the prompt, not the settings.

**Status:** Active. Technique documented; apply per-shot micro-expressions; audio
path pending the shot-A test.

## D077 â€” Dialogue = ENGLISH placeholder (native `<d>` tags) for dubbing; shot B = SMIRK only (2026-09-14)

**Decision:** The user will DUB the dialogue in Malayalam later. So for now, prompt
the lines in **ENGLISH** (the script's English lines) via MiniMax NATIVE audio
(`<d>[English] ... </d>` tags). The English audio is a PLACEHOLDER â€” it gives the
model mouth movement + timing to dub over; the final Malayalam dub replaces it
(Path 2: VC + LatentSync, D050). This is the "something to fill up" the user
asked for.

**Shot B (setup) specifics (user direction 2026-09-14):**
- **SMIRK only, NOT a full smile** â€” "a small smirk at one corner of his mouth,
  just a smirk, NOT a full smile, his eyes softening slightly" as his hands rise
  to the table edge.
- **Dialogue = MALAYALAM TEST (user: "i wonder if we put malayalam audio will it
  be able to do something? let's do that in this video itself"):** Jaisal says
  **à´¤àµà´Ÿà´™àµà´™à´Ÿàµà´Ÿàµ†** ("Let's start", his first script line) in Malayalam:
  `<d>[Malayalam] <breath> à´¤àµà´Ÿà´™àµà´™à´Ÿàµà´Ÿàµ† </d>`. This is a TEST of whether MiniMax H3
  can actually SPEAK Malayalam (vs mangling it). If it speaks it cleanly â†’ we can
  use native Malayalam audio directly (skip the dub). If it mangles it â†’ fall back
  to the English placeholder + Malayalam dub (Path 2).
- The smirk fades to a calm settled look by the end frame.

**Status:** Active. Shot B wired with smirk + Malayalam "à´¤àµà´Ÿà´™àµà´™à´Ÿàµà´Ÿàµ†" test. Run it and
judge: does MiniMax speak the Malayalam cleanly? Then apply the winning pattern to
the other dialogue shots (C, D, E, F, G).

## D078 â€” Shot C (head-twist hook) converted from CAMERA NODE to R2V (2026-09-14)

**Decision:** Shot C is now an **R2V workflow** (`jaisal_intro_C_headtwist_180_r2v.json`),
NOT the camera node. Built via `utilities/build_C_r2v.py` (copies shot B's proven R2V
model chain, swaps the refs + prompt + length).

**Why:** the original shot C used `H3LocalCameraEditor` (the camera node), whose source
literally says *"Freeze the captured scene in world space while the camera moves;
preserve identities, materials and lighting."* The camera node can ONLY move the
camera â€” it CANNOT turn the subject's head. But the hook IS the head turning 180Â°, so
the camera node is the wrong tool. R2V lets the head turn AND lets Jaisal speak the
Malayalam dialogue.

**Shot C R2V config:**
- `ref_image_0` = `jaisal_head_left_back_side.png` (start: head facing left-back)
- `ref_image_1` = `jaisal_head_180_dergree.png` (end: head turned 180Â° to camera)
- length = **240 frames (~10s)** (matches the script 0:08-0:18)
- 1344Ã—768 (1MP), SaveVideo prefix `jaisal_intro_C_headtwist_180`
- **Micro-expressions:** EYES shift FIRST (gaze turns to the lens before anything
  moves), then the head rotates SLOWLY/deliberately 180Â° while the BODY stays still
  and lit the same, eyes LOCKED on the lens the whole turn.
- **Dialogue (Malayalam, native):** `<d>[Malayalam] <breath> à´Žà´¨àµà´¤à´¾ à´ªà´±à´¯àµ‡à´£àµà´Ÿà´¤àµ
  à´…à´±à´¿à´¯à´¿à´²àµà´²... <pause> à´Žà´µà´¿à´Ÿàµà´¨àµà´¨à´¾ à´¤àµà´Ÿà´™àµà´™àµ‡à´£àµà´Ÿà´¤àµ à´Žà´¨àµà´¨à´±à´¿à´¯à´¿à´²àµà´². <long pause> à´ªà´•àµà´·àµ‡...
  <inhale> à´‡à´¤à´¾à´£àµ à´Žàµ»à´±àµ† à´¤àµà´Ÿà´•àµà´•à´‚. <pause> à´¸àµ‹ à´µàµ†àµ½à´•àµà´•à´‚ à´Ÿàµ à´¦à´¿ à´œàµˆà´¸àµ½ à´•à´Ÿàµà´Ÿàµ. </d>`
- `wire_intro_prompts.py` now includes shot C (key "C" â†’ the R2V file). `shot_C.txt`
  updated to the R2V prompt.

**Status:** Active. Shot C R2V validates clean (0 errors). The old camera-node file
(`jaisal_intro_C_headtwist_180.json`) is kept but superseded.

## D079 â€” Shot C: REVERT to the CAMERA NODE (subject CAN move via the instruction widget) (2026-09-14)

**Decision (CORRECTS D078):** shot C goes back to the **camera node**
(`jaisal_intro_C_headtwist_180.json`), NOT the R2V conversion. The R2V file
(`jaisal_intro_C_headtwist_180_r2v.json`) is kept as a fallback.

**Why (user + the node author):** the camera node's "Freeze the captured scene" line
is the **DEFAULT** because the node is built for **training Gaussians** (3D splats
need a static scene). But the author (NyckM, r/StableDiffusion "H3 camera control
update" + github.com/NyckM/BruxosSplat) confirms the subject **CAN move** â€” you just
add the motion to the prompt. The camera node's real advantage is the **precise
camera orbit** (azimuth 0â†’180 at exactly the head-turn rate), which is exactly what
the script wants ("the camera rotates and pushes in at exactly the same rate as the
head turns"). R2V can only *approximate* that in text.

**How (two surgical edits to the node source, backed up as
`experimental.py.bak_headturn`):**
1. `experimental.py` line ~30: the default source line changed from *"Freeze the
   captured scene in world space while the camera moves"* â†’ *"The subject may act
   (e.g. turn the head) while the camera moves; preserve identities, materials and
   lighting."*
2. `experimental.py` line ~56: dropped the trailing *"Silence."* so dialogue audio
   is allowed.
3. The camera node's **`instruction` widget** (widgets_values[3]) now carries the
   head-turn motion + Malayalam dialogue (set via
   `utilities/update_C_camera_instruction.py`): eyes shift first â†’ head rotates
   SLOWLY 180Â° at the same rate as the camera orbit â†’ body stays still â†’ he speaks
   `<d>[Malayalam] <breath> à´Žà´¨àµà´¤à´¾ à´ªà´±à´¯àµ‡à´£àµà´Ÿà´¤àµ à´…à´±à´¿à´¯à´¿à´²àµà´²... </d>`.

**IMPORTANT:** the node-source edits require a **ComfyUI restart** to take effect
(the running ComfyUI still has the old `experimental.py` loaded). The workflow file
itself is ready.

**Status:** Active. Shot C = camera node (precise orbit) + instruction (head-turn
motion + Malayalam dialogue). R2V version kept as fallback.

## D080 â€” Shot C = 2-STEP head turn (C1 normalâ†’90Â°, C2 90Â°â†’180Â°), R2V (2026-09-14)

**Decision (user: "should we not give the last frame of the second video and then
do a rotate to the 180 degree... or 2 step is needed, from the normal one to 90
degree with camera and then from that frame last image to the back twisted one?"):**
Shot C is a **2-STEP R2V head turn**, NOT a single 180Â° take and NOT the camera node.

**Why 2-step:** (1) **Continuity** â€” shot C must START from shot B's exact last
frame (`jaisal_with_hand_on_table.png` = normal frontal) for a seamless cut, NOT
from the 90Â° frame. (2) **Reliability** â€” a full 180Â° head turn in one take is a
big ask; two 90Â° steps are far more reliable, and the 90Â° frame is the SHARED
anchor so C1â†’C2 cuts seamlessly.

**The two workflows (both R2V, built via `utilities/build_C1_C2.py`, both validate
clean 0 errors, 120 frames ~5s each, 1344Ã—768):**
- **C1** `jaisal_intro_C1_headturn_90.json`: `jaisal_with_hand_on_table.png` (normal
  frontal, B's end) â†’ `jaisal_head_left_back_side.png` (90Â° left-back). **NO
  dialogue** (the turn happens silently). Eyes shift first, head rotates SLOWLY to
  the left-back side, body stays still.
- **C2** `jaisal_intro_C2_headturn_180.json`: `jaisal_head_left_back_side.png` (90Â°)
  â†’ `jaisal_head_180_dergree.png` (180Â° back-twisted, face turned back over the
  shoulder). **Malayalam dialogue** (the creepy reveal): `<d>[Malayalam] <breath>
  à´Žà´¨àµà´¤à´¾ à´ªà´±à´¯àµ‡à´£àµà´Ÿà´¤àµ à´…à´±à´¿à´¯à´¿à´²àµà´²... </d>`.

**Keyframes (verified visually):** `jaisal_with_hand_on_table.png` = facing camera,
hands on table (normal); `jaisal_head_left_back_side.png` = seen from left-back,
head turned left (~90Â°); `jaisal_head_180_dergree.png` = back to camera, FACE turned
back toward the camera over the shoulder (the creepy 180Â° twist).

**Status:** Active. C1 + C2 ready. The single-take R2V
(`jaisal_intro_C_headtwist_180_r2v.json`) and camera-node
(`jaisal_intro_C_headtwist_180.json`) versions are kept as alternatives.

## D081 â€” Shot C = SINGLE 3-ref R2V head turn (normalâ†’90Â°â†’180Â°), locked camera, 10s (2026-09-14)

**Decision (user: "its definitely moving [C1] but the head first looks like the
right side... we can add 3 reference, 90 degree one and full 180 degree one and
see once? i feel like its very much doable, but we might need to add prompt for
slowing down, the shot is 10 second bcs we have a dialogue with head twisted 180
degree so we should time that, lets add dialogue also"):** shot C is a **SINGLE
3-ref R2V** head turn (NOT the 2-step, NOT the camera node). Built via
`utilities/build_C_3ref.py` â†’ `jaisal_intro_C_headturn_3ref.json` (validates clean
0 errors, 23 nodes).

**Config:**
- `ref_image_0` = `jaisal_with_hand_on_table.png` (normal frontal, B's end frame)
- `ref_image_1` = `jaisal_head_left_back_side.png` (90Â° left-back, MIDDLE anchor)
- `ref_image_2` = `jaisal_head_180_dergree.png` (180Â° back-twist, END)
- **240 frames (~10s)**, 1344Ã—768, SaveVideo prefix `jaisal_intro_C_headturn_3ref`
- **LOCKED camera** (no camera node) â€” the head does all the motion.

**Timing (the user's key ask):** the turn happens in the **first ~5s** (eyes shift
first, head rotates SLOWLY to the LEFT through the 90Â° anchor at ~5s), then the
head **HOLDS at 180Â°** (back to camera, face turned back over the shoulder) while
he speaks the Malayalam dialogue in the **second ~5s**.

**Direction fix:** the head turns to the **LEFT** (toward his left shoulder), NOT
right â€” the prompt says "to the LEFT (toward his left shoulder, NOT to the right)"
and the negative adds "head turning to the right, head turning right".

**Status:** Active. 3-ref shot C ready. C1/C2 (2-step) + camera-node + single-2-ref
versions kept as alternatives.

---

## D082 â€” Shot C = CAMERA NODE (trolley orbit) + head turn LEFT + ENGLISH dialogue (2026-09-14)

**Decision (user: "that was messy, it didnt follow the camera angle, and the
dialogue lets keep it in english for now, malayalam i will dub later, we need
some lip movement thats it. the prompt didnt have the camera movement, camera
should be moving like we have in the camera node. we are going to look left side
meaning the camera must rotate on the right side it should move like in trolley
and the head should follow (head will be left side) since camera and face are
opposite. lets use camera node if we want, we need max perfection"):** the 3-ref
R2V (D081) came out MESSY and had NO camera movement. Reverting to the **CAMERA
NODE** (`jaisal_intro_C_headtwist_180.json`, node 127 `H3LocalCameraEditor`) for
the smooth trolley-like orbit. Dialogue is **ENGLISH** for now (user will dub
Malayalam later) with **clear lip movement**.

**Config:**
- **Reference image** = `jaisal_with_hand_on_table.png` (clean frontal start,
  continuity from shot B) â€” the camera orbits 180Â° from frontal to back.
- **Trajectory** (unchanged): `0Â° â†’ 90Â° (t=0.5) â†’ 180Â° (t=1)`, distance 1â†’0.9â†’0.8
  (slow push-in), profile `124 frames (~5.17s)`, interpolation `smooth`.
- **orbit_direction** = `same as HUD` (index 7) â†’ positive azimuth = camera's
  RIGHT = trolley. If the orbit comes out mirrored, flip this widget to
  `invert H3 orbit`.
- **Instruction** (node 127, index 3): head turns SLOWLY to the **LEFT** (toward
  his left shoulder), ending back-to-camera with face turned back over the
  shoulder; body stays still; in the second half he speaks ENGLISH with clear
  LIP MOVEMENT: `<d>[English] <breath> I don't know what to say... <pause> I
  don't know where to start. <long pause> But... <inhale> this is where I start.
  <pause> So welcome to the Jaisal Kut. </d>`; natural ambient only, NO music.

**Source patch (REQUIRES ComfyUI RESTART):** `camera.py` (backup
`camera.py.bak_headturn`) â€” the base camera path (`experiment_mode='Off'`)
hardcoded `sound='Silence.'` and `forbid='...no subject rotation...'`, which
froze the subject and killed the dialogue. Patched (via
`utilities/patch_camera_audio.py`, compiles clean): (1) `sound` â†’ natural
ambient + voice (NO music); (2) `forbid` â†’ allows the head turn (body stays
still); (3) `preserve` â†’ relaxed so the head may turn; (4) both `plan_text`
paths (non-sections + H3-sections) emit the ambient/voice soundscape instead of
`Silence.`/`N/A`.

**Why camera node over R2V:** the user wants the smooth trolley orbit the camera
node produces (the R2V 3-ref had no camera movement and was messy). The camera
node compiles the trajectory into a precise prompt; the head turn + dialogue come
from the instruction widget.

**Status:** Active. `jaisal_intro_C_headtwist_180.json` updated (ref +
instruction), validates clean 0 errors. **ComfyUI restart REQUIRED** to load the
patched `camera.py`. 3-ref R2V (D081) + C1/C2 kept as alternatives.

---

## D083 â€” Shot C: BYPASS the experimental Sage VRAM patch (Blackwell/sageattention 1.0.6) (2026-09-14)

**Problem (user: "got this issue ... sageattention is not new enough version or
could not determine CUDA architecture, cannot apply MiniMax H3 Memory Efficient
Sage Attention Patch"):** shot C's model chain (inside the subgraph) contained the
**experimental `MiniMaxH3MemoryEfficientSageAttentionPatch`** node (KJNodes,
internal node 136). It needs a `sageattention` that recognizes the RTX 5090's
Blackwell arch (SM_120 / capability (12,0)); the installed **sageattention 1.0.6**
does NOT (torch 2.12.0+cu130 detects the 5090 fine, but sage 1.0.6 predates
Blackwell). The node raised a RuntimeError and aborted the run.

**Fix (via `utilities/fix_C_sage_bypass.py`, backup `*.json.bak_sage`):**
**bypassed node 136** â€” retargeted link 404 (origin 6 UNETLoader) from 136 â†’ 137
(ModelAttentionBackend), removed link 269 (136â†’137) and node 136. New chain:
`6 (UNET) â†’ 137 (ModelAttentionBackend 'comfy kitchen attention') â†’ 138
(H3SLAAttention) â†’ 121 (LoraLoader turbo) â†’ 122 (switch)`. This keeps the proven
`H3SLAAttention` speed stack; we only drop the experimental sage VRAM patch.
Validates clean 0 errors (node count 40â†’39).

**Why bypass (not upgrade sage):** the sage patch is an *experimental* peak-VRAM
reduction. The H3SLAAttention node (138) is the actual speed/VRAM stack we rely
on, and it does NOT use sageattention â€” so dropping 136 loses nothing for our
pipeline. Upgrading sageattention to a Blackwell build is a separate, riskier
change (recompile wheels) not needed to run the shot.

**Status:** Active. `jaisal_intro_C_headtwist_180.json` no longer contains the
sage patch node. If a future shot's template re-introduces the sage patch node,
apply the same bypass (or upgrade sageattention).

---

## D084 â€” Shot C: 10s timing + scene description in the instruction (background lock) (2026-09-14)

**Problem (user: "the camera is moving correctly and character is somewhat
looking at it, but the problem is it didnt create the proper video meaning
timing is 5 seconds, and the background had changed, lets give our prompt now
along with camera movement"):** the camera-node run (a) was only **5s** (profile
was `124 frames (~5.17s)`) but the script's shot C is **0:08â€“0:18 = 10s**; (b)
the **background drifted** because the camera node's compiled prompt is thin
(trajectory + a short head-turn instruction) â€” it had NO scene description, so
the model re-invented the room.

**Fix (via `utilities/update_C_10s_background.py`):**
1. **Profile `124 frames (~5.17s)` â†’ `243 frames (~10.13s)`** (camera node
   widget idx 1). The video node's `length` is wired from the camera node's
   frame-count output (slot 5), so the 10s propagates automatically.
2. **Enriched the `instruction` widget** (idx 3) with the full SCENE description
   (boy at wooden table, dark room, single bare bulb above head, B&W high
   contrast fine grain) + a HARD BACKGROUND LOCK ("the room, table, chair and
   the single bare bulb stay EXACTLY the same throughout - do NOT change, add,
   remove or reposition any background element; the background is locked to the
   reference image") + the head-turn-LEFT motion + the ENGLISH dialogue with lip
   movement + natural ambient / NO music.

**Wiring facts (verified):** video node 201 (MiniMaxH3ImageToVideo) inside the
subgraph: `length` (slot 7) â† subgraph `length` input â† camera node slot 5
(frame count from profile); `prompt` (slot 4) â† camera node slot 4 (compiled
prompt incl. the instruction field). So profile + instruction are the only two
dials needed.

**Status:** Active. `jaisal_intro_C_headtwist_180.json` = 243 frames (~10.13s),
enriched instruction, validates clean 0 errors. `shot_C.txt` updated to match.

---

## D085 â€” Shot C: ABANDON the camera node, back to 3-ref R2V with guide-based prompt (2026-09-14)

**Problem (user: "the camera node is acting up, colors changed, face drifted, i
dont think its capable of doing this consistent 10 seconds apart from gaussian or
small 2 or 3 second. lets switch to the normal workflow, and get it done.
prompting is needed here, check the guide"):** the camera node (D082/D084) cannot
hold a consistent 10s â€” colors changed and the face drifted. The camera node is
prompt-only (no camera adapter), so over a long take the model's priors take over.

**Decision:** shot C = **3-ref R2V** (`jaisal_intro_C_headturn_3ref.json`) â€” the
refs anchor the face at 3 exact poses, so identity holds across the whole 10s.
The camera node workflow (`jaisal_intro_C_headtwist_180.json`) is kept but
abandoned for shot C.

**Prompt (node 138, via `utilities/update_C_3ref_prompt.py`, saved to
`Jaisal-intro\prompts\shot_C_3ref.txt`):** full guide 6-section structure:
- **MANDATORY SHOT CONSTRAINT at the top** (guide rule: H3 weights the first lines
  most): "the camera is completely static and locked - NO camera movement, NO pan,
  NO orbit, NO zoom, for the entire 10 seconds"
- **Face locked to refs:** "His face, hair, clothing and build come from the
  reference images, NOT from this text description" + `fully_preserved` on all 3
  pictures
- **3 anchors with timings:** <Picture 1> = first frame (frontal, hands on table);
  <Picture 2> = head passes through the 90Â° left-back pose at ~2.5s; <Picture 3> =
  final frame (back to camera, face over shoulder) reached at ~5s and held
- **Head turn LEFT** in the first half (eyes shift first, body still), **English
  dialogue with clear lip movement** in the second half (dub Malayalam later)
- Background locked to the refs; natural ambient only; NO music (D041)

**Status:** Active. `jaisal_intro_C_headturn_3ref.json` = 240 frames (10s),
1344Ã—768, 3 refs, validates clean 0 errors. This is the shot-C production path.

**CORRECTION (user: "how the fuck or where i mentioned it has to be rose pink
shirt? ... is this the reason why we have added references?"):** the first version
of this prompt wrote appearance text ("short dark hair, rose-pink collared shirt,
black trousers") â€” WRONG. The refs ARE the identity source; any appearance text
competes with them (and "rose-pink" is a color description in a B&W video â€” a
contradiction). **FIXED via `utilities/fix_C_3ref_no_appearance.py`:** ALL
appearance text removed. `<Subject 1>` is now defined ONLY by the pictures: "His
identity, face, hair, clothing and build come ENTIRELY from the reference images -
do not alter his appearance in any way."

**RULE (permanent, all R2V prompts): NEVER describe the character's appearance in
the prompt when reference images carry the identity.** The prompt describes ONLY:
poses, actions, camera, scene, sound, dialogue. Identity = refs. (This matches the
existing "character identity comes from the reference IMAGE, not text description"
rule â€” I violated it here and the user called it out.)

---

## D086 â€” Shot C REDESIGNED: "genuinely starting" (no 180Â° twist, no glitch) (2026-09-14)

**Decision (user: "i feel like we should reconsider the approach... I would make
the opening almost awkwardly simple... Black screen. Room tone. Bulb hum. Chair
scrape. Jaisal enters. Sits. Looks at camera. 'I don't know what to say.' Small
pause. Camera begins moving. 'I don't know where to start.' Camera reaches 90Â°.
Pause. He looks at the camera. 'But... here we start.' Beat. 'Welcome to the
Jaisal Kut.' Cut to the next scene. No glitch. No horror. No 180Â° impossible
neck... I'd choose this version over the 180Â° twist. It fits the channel you're
actually describing much better." + "we have a and b ready already, lets start
from C, B's last shot is jaisal with his hand on the table, so lets work on C as
independent one and close it"):** the 180Â° head-twist hook is DROPPED. Shot C is
now a **simple, human "genuinely starting" moment** â€” the strange visuals come
AFTER the viewer has accepted the person.

**Built (`jaisal_intro_C_starting_2ref.json`, via
`utilities/build_C_starting_2ref.py`, validates clean 0 errors, 22 nodes):**
- **2 refs:** `ref_image_0` = `jaisal_with_hand_on_table.png` (frontal START â€”
  B's last frame, continuity) â†’ `ref_image_1` = `jaisal_head_left_back_side.png`
  (90Â° left, head into lens, END). The 180Â° ref (node 152) removed.
- **240 frames (10s)**, 1344Ã—768, SaveVideo prefix `jaisal_intro_C_starting_2ref`.
- **Camera = ONE slow 90Â° orbit to his LEFT** (counter-clockwise from above),
  start = <Picture 1>, end = <Picture 2>. Explicitly NOT 180Â°, NOT a full circle,
  NOT returning to start.
- **Head follows the camera** (turns left to keep looking at the lens); **body
  stays completely still** (shoulders/torso/arms/hands/chair/table fixed).
- **PER-SECOND TIMELINE** (guide technique â€” the user's key ask: "minimax should
  have prompt for seconds (each second)"): 10 segments, one state per second:
  0-1s still + eyes shift + "I don't know what to say"; 1-2s pause, eyes hold;
  2-3s camera begins orbiting left + "I don't know where to start"; 3-6s head
  slowly follows the camera; 6-7s camera reaches his left side (~90Â°), pause;
  7-8s head ~90Â° into lens + "But... here we start"; 8-9s beat; 9-10s "Welcome
  to the Jaisal Kut", holds the <Picture 2> pose.
- **Micro-expressions:** eyes shift first, gaze holds the lens, quiet natural
  delivery, clear lip movement.
- **Background = PURE BLACK VOID** (locked per-second): no room/wall/door/ceiling/
  furniture/architecture revealed during the orbit; single bare bulb = only light.
- **English dialogue** (dub Malayalam later): "I don't know what to say." / "I
  don't know where to start." / "But... here we start." / "Welcome to the Jaisal
  Kut." NO glitch, NO horror, NO 180Â° twist.
- Prompt saved to `Jaisal-intro\prompts\shot_C_starting.txt`.

**Superseded (kept as alternatives):** `jaisal_intro_C_headturn_3ref.json` (3-ref
180Â° twist), `jaisal_intro_C_headtwist_180.json` (camera node), C1/C2 (2-step).

**CORRECTION (user: "i dont want the last frame to be the backside, i want the
last 'welcome to the jaisal kut' to be the first frame we gave... we need
cinematic blocking and shot division"):** the camera is now a **SMOOTH ROUND
TRIP** (via `utilities/update_C_starting_roundtrip.py`): frontal (<Picture 1>) â†’
orbit left to ~90Â° (<Picture 2>, the middle checkpoint) â†’ **back to frontal
(<Picture 1>)**. The **FINAL FRAME = THE FIRST FRAME** (frontal, hands on table)
â€” so the cut to shot D is seamless. The head follows the camera the WHOLE way
(turns left as the camera orbits left, turns back as it returns), so he keeps
looking at the lens; body stays dead still. Added **CINEMATIC BLOCKING** (5
phases: STILL frontal / ORBIT OUT / LEFT SIDE ~90Â° / ORBIT BACK / WELCOME
frontal) + a **per-second TIMELINE** (one state per second, each naming camera
position + subject position + dialogue beat). Dialogue beats: 0-1s "I don't know
what to say"; 2-3s "I don't know where to start"; 6-7s "But... here we start";
9-10s "Welcome to the Jaisal Kut" (final frame = <Picture 1>). Validates clean 0
errors.

**NEXT (user, submit today):** run `jaisal_intro_C_starting_2ref.json` (stop Qwen
first); judge: does the camera do the round trip smoothly? does the head follow
while the body stays still? does the FINAL frame = the FIRST frame (frontal)?
does the dialogue land on the beats? then prep shot D.

---

## D087 â€” Shot C = SINGLE STATIC MEDIUM SHOT + white "The Jaisal Kut" title flash (2026-09-15)

**Decision (user: "i feel like we dont need to do the rotation or anything, just a
static medium shot, cutting with perfect shot division... when the character says
welcome to the jaisal cut, in the background of the character we should write it in
white letters like a flash for a split second"):** the D086 round-trip camera orbit
is DROPPED. Shot C is now a **SINGLE STATIC MEDIUM SHOT** (50mm, eye level, camera
COMPLETELY STILL â€” no orbit/pan/zoom). The boy stays in the same seated pose the
whole 10s; only his mouth moves (speaking) + eyes shift subtly. All 4 English lines
in one take with clear lip movement. **TITLE FLASH:** as he says the final line
("So welcome to the Jaisal Kut"), the words **"The Jaisal Kut" flash in WHITE
letters in the background BEHIND him** (in the black void, above/behind his head)
for a SPLIT SECOND (~1s), then gone. Spelling locked exactly: T-h-e J-a-i-s-a-l
K-u-t.

**Built (`jaisal_intro_C_starting_2ref.json`, via `utilities/rebuild_C_static.py`,
validates clean 0 errors, 21 nodes):**
- **SINGLE ref:** `ref_image_0` = `jaisal_with_hand_on_table.png` (frontal, hands
  on table). The 90Â° ref (node 139) + its link (301) DELETED; `ref_image_1` link
  cleared â†’ None.
- **Prompt (node 138) rewritten** to the static-shot + title-flash structure
  (saved `Jaisal-intro\prompts\shot_C_static.txt`): MANDATORY SHOT CONSTRAINT =
  camera COMPLETELY STILL (no orbit/pan/zoom), boy stays in same pose, only mouth
  moves; 50mm medium, eye level, single bare bulb, PURE BLACK VOID background, ONE
  boy; a dedicated **TITLE FLASH** section (white "The Jaisal Kut" behind him,
  split second, exact spelling); per-second TIMELINE with the 4 lines on beats
  (0-1s "I don't know what to say"; 2-3s "I don't know where to start"; 4-5s "But...
  this is where I start"; 6-7s "So welcome to the Jaisal Kut"; 7-8s the white title
  FLASHES behind him; 8-10s he holds the pose).
- **240 frames (10s), 1344Ã—768** (unchanged).
- **NO MUSIC** (D041): `non_diegetic_music` = natural ambient only.

**WHY static:** a round-trip orbit over 10s is where face/color drift crept in
(D085/D082). A locked static medium shot is far more reliable â€” the model only has
to hold a pose + speak, not move the camera. Clean shot division (cut between B and
D in assembly) reads more cinematic than a slow orbit.

**RISK:** the model rendering the white "The Jaisal Kut" text is unreliable at
spelling (D004) and timing a split-second flash to the exact word. **FALLBACK if
the text comes out garbled / mistimed / not at all:** composite the white title
flash in POST (DaVinci Resolve) over the clean video, timed to the "Welcome" line
(matches D004 â€” title never rendered by the model). The video itself stays clean
either way.

**CORRECTION (2026-09-15, after the first run): the in-video title flash DID NOT
GO WELL â€” the FACE GOT DISTORTED.** Asking MiniMax to render text + hold a face +
speak all at once is too much pressure; the face (the priority) suffers first
because the model's attention goes to the text. **DECISION: REMOVE the title from
the video entirely.** The title is done in POST: the user takes the LAST FRAME of
the video, creates a NEW image with the text added, and uses that (then the white
"The Jaisal Kut" flash is a post effect over the clean video). **Rebuilt via
`utilities/rebuild_C_static_notext.py`** (validates clean 0 errors): (1) removed
the TITLE FLASH section + the text from the 7-8s timeline beat (now a still beat);
(2) added a **FACE CLARITY lock** (face SHARP/CLEAR/IN FOCUS/HIGH DETAIL in every
frame, does NOT distort/blur/morph/change shape, exactly as in <Picture 1>);
(3) added **NO text/letters/words/title/watermark/graphics** to the background
lock (so the model doesn't hallucinate text on its own). Prompt saved
`Jaisal-intro\prompts\shot_C_static_notext.txt`. **RULE: do NOT ask MiniMax to
render text in a face shot â€” it distorts the face. Keep the video text-free; add
any title in POST.**

**NEXT (user):** (a) stop Qwen; (b) run `jaisal_intro_C_starting_2ref.json`
(no-text version); (c) judge: is the camera truly static? is the FACE sharp/clear
in every frame (the main issue)? does he speak all 4 lines with clear lip
movement? (d) then the user takes the LAST FRAME â†’ adds the white "The Jaisal
Kut" text in a new image â†’ post; (e) then prep shot D (the perfect reverse).
**RULES:** NO MUSIC (D041); user runs GPU jobs manually (I never stop Qwen);
artifacts in `Jaisal-intro\`.


## D088 â€” Last-frameâ†’2K stitch pipeline (video last frame as next shot's start ref) (2026-09-15)

**Decision:** to stitch shots seamlessly (no glitch), the NEXT shot's 
ef_image_0
(start anchor) = the **last frame of the previous shot's video, upscaled to 2K** â€”
NOT a separately-generated keyframe. Built as a single one-run workflow
seedvr2_lastframe_2k.json (via utilities/build_seedvr2_lastframe_2k.py,
validates clean 0 errors 0 warnings).

**Pipeline:** LoadVideo â†’ GetVideoComponents â†’ GetImageRangeFromBatch
(start_index=-1, 
um_frames=1 = last frame; KJNodes, source-confirmed
start_index==-1 â†’ len-1) â†’ SeedVR2VideoUpscaler (atch_size=1, 1080
shortest-edge â†’ 1920Ã—1080, seedvr2_ema_7b_sharp_fp16 + ema_vae_fp16) â†’
SaveImage (prefix lastframe_2k). Works on the original OR already-upscaled
video (the upscaler re-upscales to 2K either way).

**Reason:** the last frame of shot N is the EXACT end state; feeding it as shot
N+1's start ref makes the cut seamless (same pose/room/lighting). A fresh
keyframe risks a mismatch. 2K (1920Ã—1080) matches H3's 16:9 1344Ã—768 aspect.

**Alternatives considered:** (a) separate Krea2 keyframe per shot (rejected â€”
mismatch risk + extra work); (b) ffmpeg last-frame extract + separate SeedVR2
image run (rejected â€” two steps, this is one).

**Status:** ACTIVE. **RULE: for every shot, last frame (2K) â†’ next shot's
ref_image_0.**

**KEY LESSON (2026-09-15): native UI links are ARRAYS
[id, from_node, from_slot, to_node, to_slot, type], NOT dicts.** A
machine-built file with dict links is silently ignored by the UIâ†’API converter
(validator: 
ode_not_reachable_from_output on every node +

equired_input_missing on the save node). Emit links as arrays.


## D089 â€” Shot D = CONTINUATION from C's last frame (reverse dropped) (2026-09-15)

**Decision:** the script's Shot 4 "PERFECT REVERSE" (everything reverses, 180 head
twist undone) is DROPPED â€” shot C no longer has the twist (D086/D087 made it a
static medium shot), so there is nothing to reverse. **Shot D is now a
CONTINUATION:** Jaisal stays seated in exactly C's last frame; the camera guy
(off-screen) asks "What's the purpose of this channel?"; Jaisal gives a subtle
LISTENING reaction (eyes shift, thoughtful expression, brief pause, tiny head
tilt). **The camera guy's line is DUBBED IN POST** (Midhun voice, D055) â€” the
video itself = Jaisal listening + ambient, NO in-video dialogue, NO music (D041).

**Config (`jaisal_intro_D_reverse.json`, via `utilities/setup_shot_D_continuation.py`,
validates clean 0 errors):** ref_image_0 = ref_image_1 = `shot_C_lastframe.png`
(C's last frame as BOTH start and end anchor â€” locks the pose, seamless cut).
Prompt = listening shot (node 138). Length 175 frames (~7.3s, script 0:18-0:25).
1344x768, 1 MP.

**Reason:** a single shared anchor (C's exact last frame) makes the cut seamless
and keeps the pose locked; a listening beat is the natural bridge to shot E
(plants grow). The off-screen question is audio-only (post dub) so MiniMax is
not asked to render a second person or in-video dialogue.

**Status:** ACTIVE. **RULE: shot D = continuation + listening reaction; camera
guy's line dubbed in post.**

---

## D090 â€” Shot D = PURE SILENT reaction; dialogue REMOVED from the video (2026-09-20)

**Decision:** the v4 off-screen-voice approach (a `<Subject 2>` off-screen
camera-guy voice + a `<d>` line + "lips stay CLOSED" lip-lock) STILL made H3
animate the boy's mouth (take `jaisal_intro_D_reverse_00004_` = lip-sync / the
boy appears to talk). **Shot D is now a PURE SILENT reaction shot:** the
in-video dialogue is REMOVED ENTIRELY (no `<d>` line, no `<Subject 2>`
off-screen voice). The boy is a silent listener/reactor (mouth CLOSED, lips
NEVER move; only eyes shift, thoughtful expression, quiet breath, tiny head
movement). The camera guy's line is DUBBED IN POST (Midhun voice, D055/D089).

**Config (`jaisal_intro_D_reverse.json`, via `utilities/fix_shot_D_silent.py`,
validates clean 0 errors):** node 138 prompt rewritten â€” no `<d>`, no
`<Subject 2>`; `overall_soundscape` = ambient only + "NO voice and NO speech in
this take"; negatives add `any speech, any voice, any dialogue, the boy's jaw
moving`. Refs/length (96f/4s) unchanged.

**Reason:** H3 animates the VISIBLE person's mouth whenever ANY dialogue line is
present â€” an off-screen `<Subject 2>` tag + lip-lock wording is NOT enough to
keep the only visible person's lips closed. Removing the dialogue from the video
entirely is the reliable way to keep the character silent.

**Status:** ACTIVE. **RULE: when the visible character must NOT talk, REMOVE the
dialogue from the video (pure silent reaction) and DUB the line in post â€” do NOT
rely on an off-screen-voice tag to hold the visible person's lips closed.**

**Update 2026-09-20 (v2 â€” HARD SILENT-AUDIO LOCK + post-strip):** removing the
dialogue (v1) was NOT enough â€” H3's **audio prior** (person facing camera =
talking) leaked **speech-like GIBBERISH** (not our line). Per the R2V guide's
"No dialogue/text if not wanted" rule, the prompt now carries a HARD SILENT lock
(`overall_soundscape` = "COMPLETE SILENCE except a faint ambient bedâ€¦ NO human
voice, NO speech, NO talking, NO words, NO gibberish"; `non_diegetic_music` +
negatives forbid ALL voice/speech/words/gibberish/vocalization). **BUT the
GUARANTEED fix is post:** the camera guy's line is dubbed in post anyway, so the
H3 audio is throwaway â€” **strip it (`ffmpeg -i <take>.mp4 -an -c:v copy
<take>_silent.mp4`) and build the audio track in post** (ambient + Midhun dub).
**RULE: a prompt-only silent lock helps but is NOT guaranteed to stop H3's
speech prior â€” for a silent-character shot, STRIP the H3 audio in post and build
the audio track in post.**

**Update 2026-09-20 (v3 â€” AGGRESSIVE NON-SPEAKING, GPT prompt adopted):** the v2
hard silent-audio lock was STILL not enough â€” H3 moved the boy's mouth because
(a) the *concept* of "listening to an off-screen question" primes a talking face,
and (b) a slightly-open/neutral mouth in the reference gets animated. **Fix (via
`utilities/fix_shot_D_silent_v3.py`, validates clean 0 errors):** adopted GPT's
AGGRESSIVE NON-SPEAKING prompt (2 tweaks: dropped "before speaking"; negative
`boy standing/walking/entering` â†’ `person ...`). The prompt now: (1) `<Subject 1>`
= the person from the reference image (NOT "young boy" â€” avoids identity/facial
drift); (2) a dedicated **CRITICAL PERFORMANCE RULE** block (DOES NOT SPEAK, NO
dialogue, mouth FULLY CLOSED first-to-last, lips/jaw completely still, teeth never
visible, no lip-sync/whisper/speech sounds); (3) the **listening/off-screen-question
concept REMOVED entirely** (the shot is just "a quiet natural moment"; dialogue
added in post); (4) per-second timeline; (5) CAMERA LOCK; (6) `overall_soundscape`
= diegetic room tone only + "ABSOLUTELY NO HUMAN VOICE / NO SPEECH / NO WORDS / NO
VOCALIZATION"; (7) comprehensive speech-movement negative. **NEW DOC:
`docs/PROMPTING_ISSUES_LOG.md`** (15 H3 R2V prompting issues + how we overcame
them + silent/speaking checklists). **RULE: for a silent-character shot â€” remove
the listening/reacting-to-a-question concept entirely, define the person via
`<Subject 1>` + the reference image (not "young boy"), make the non-speaking
instruction AGGRESSIVE (dedicated rule block + strong negative), hard silent-audio
lock, check the reference's mouth is closed, keep it short (4s), and STRIP the H3
audio in post (guaranteed).**

## D091 â€” Seamless shot-to-shot continuation: use NikoDemon80/ComfyUI-H3-Motion-Context (latent tail slicing)

**Date:** 2026-09-20
**Decision:** For seamless (no-hard-cut) integration between shots, install
**NikoDemon80/ComfyUI-H3-Motion-Context** (988 stars). It slices the previous
clip's LATENT TAIL bit-for-bit and feeds it as context to the next clip â€” no
decode/resize/re-encode between clips, so no seam.
**Reason:**
- Our ComfyUI is **0.34.3** (confirmed via `/system_stats`) â€” this pack needs
  **0.34.0+** for arbitrary keyframe anchors. âœ… Compatible.
- It works on our standard H3 model files (all present).
- The alternative **Herrgotts-H3-Infinite-Continuation-Suite** needs a ComfyUI
  with **PR #15375** (native H3 AV-mask) â€” we are on a stable 0.34.3, NOT that
  PR build. âŒ Not compatible without a risky ComfyUI upgrade.
- **Adudeguyman/ComfyUI-H3-Project-Suite** is a fork of NikoDemon80's and
  **CONFLICTS with it** (can't run both) â€” only 35 stars, adds a project-manager
  UI we don't need. âŒ Skip.
**Caveat (IMPORTANT):** our production workflow uses the **turbo LoRA** +
Spectrum. The pack's README warns **turbo LoRA + Spectrum cost audio in
chains** â€” H3 emits 32 kHz audio. Since we STRIP H3 audio in post anyway
(D090), this caveat is acceptable for us (we don't rely on chained H3 audio).
**Config (from README):** `context_length` 22, `audio_context_length` 24,
`context_latent` through a Save/Load Latent pair, `Trim match_tail` ON,
`Spectrum` OFF. Use the **"airlock" prompting** technique: open the next clip
holding the previous clip's exact closing framing (no dialogue, ~2s), then cut
to the new setup.
**Alternatives considered:** Herrgotts (needs PR #15375 â€” incompatible),
Adudeguyman (conflicts with NikoDemon80, low stars).
**Status:** DECIDED â€” install NikoDemon80/ComfyUI-H3-Motion-Context.
**NOTE on the `.char` workflow** (`E:\minimax_workflow\minimax-h3-guided-
consistent-characters-via-reference-identity-face-body-cloths.inline-graph.json`):
it is a **Comfy Cloud / Comfy-Org "inline-graph"** format (top keys
`app/graph/params/prompt/target/version/coreType`). Its nodes are
`character/references`, `character/write`, `character/encode` (face-detect
yunet + face-recog sface) + `minimax/h3-reference-to-video`. The `character/*`
nodes are a **Comfy Cloud hosted feature, NOT a local node pack** â€” so that
workflow runs on Comfy Cloud, not our local ComfyUI. It is a REFERENCE for the
face-encode consistency APPROACH, not something we install locally.

## D092 â€” Consistent-AUDIO continuation: SatoDive/Minimax-H3-Latent-Continuation (the Ep29 pack)

**Date:** 2026-09-20
**Decision:** For **consistent AUDIO across continued shots** (telling small stories in
English), use **SatoDive/Minimax-H3-Latent-Continuation** (24â˜…, MIT) â€” the pack
behind the user-found **`Ep29 MiniMaxH3_Continuation_Workflow.json`**. It does
segment render + **stitch continuation with audio continuity** (the
`MiniMaxH3Easy*_SatoDive` node family).
**Reason:** the user found the Ep29 workflow specifically for "consistent audio as
well for minimax â€¦ useful for telling small stories in english." This is the
**audio-continuity** complement to D091 (NikoDemon80 = visual latent-tail
continuity). Both are now installed.
**Installed (staged, no restart yet):** cloned into `custom_nodes\` on 2026-09-20.
All 8 Ep29 node classes confirmed present in the pack source:
`MiniMaxH3EasyVideoTailSlicer_SatoDive`, `MiniMaxH3EasySegmentDecode_SatoDive`,
`MiniMaxH3EasyModelAdapter_SatoDive`, `MiniMaxH3EasyStitchContinuation_SatoDive`,
`MiniMaxH3EasySegmentRender_SatoDive`, `MiniMaxH3EasySaveLatent_SatoDive`,
`MiniMaxH3EasyLoadLatent_SatoDive`, `MiniMaxH3EasyContextSegments_SatoDive`.
**Ep29 workflow also needs (already installed âœ…):** KJNodes
(`PathchSageAttentionKJ`, `ModelPreviewOverrideKJ`), Pixaroma
(`PixaromaMonitor`, `PixaromaRunTimer`), rgthree (`Label (rgthree)`), SLA
attention (`H3SLAAttention`, `MiniMaxH3MemoryEfficientSageAttentionPatch`,
`SolAttnPatch` â€” verify these resolve; if not, install the SLA pack),
`MiniMaxH3SigmaShift` + `MiniMaxH3DualClockSamplerT8` (verify; if not, install
the H3 sampler pack), `JWFloatToInteger` + `VRAMCleanup`/`RAMCleanup` (utility
nodes â€” verify).
**NEXT (user, stop Qwen first):** restart ComfyUI â†’ open Ep29 workflow â†’ confirm
no red nodes â†’ test a Dâ†’E continuation with audio continuity.
**Status:** DECIDED + INSTALLED (staged).

## D093 â€” H3 long-video pipeline: adopt pmhaidn/ComfyUI-Minimax-H3-Extender (seam smoothing + latent extend); skip MultiRef/ttulttul/Continuum

**Date:** 2026-09-28
**Decision:** For the Jaisal intro's long-video assembly (Aâ†’Bâ†’Câ†’Dâ†’Eâ†’Fâ†’G), adopt **pmhaidn/ComfyUI-Minimax-H3-Extender** (GPL-3.0, 10â˜…) as the **seam-smoothing + latent-extend** layer on top of the existing NikoDemon80 Motion-Context chain (D091). Use its `MiniMaxH3VideoMerge` node (`seam_smooth=1` Farneback optical-flow seam smoothing + `color_match="seam_fade"` luminance/chrominance cosine-fade over 24 frames) to smooth the Eâ†’F and Fâ†’G seams, and `MiniMaxH3VideoExtender`/`MiniMaxH3LoopTrim` for latent-based extension if needed. **Skip** the other 4 researched repos for now:
- **seitanism/ComfyUI-H3-Motion-Context-MultiRef** = a FORK of our installed NikoDemon80 pack (masked keyframes, AV Bridge/Extension, V2V transfer, 2MP de-roping; Update 9 2026-09-05). Installing alongside the original â†’ **node-ID conflict** (same class names). Only adopt if we later want its masked-keyframe/AV-bridge features AND are willing to replace the original pack.
- **ttulttul/ComfyUI-Minimax-H3-Continuation** (v0.6.3) = redundant latent-tail continuation â€” duplicates what NikoDemon80 already does. Skip.
- **ukr8b3g-cmyk/ComfyUI-H3-Continuum** (V3.8X2) = heavyweight production sampler (chunked gen, review-each-chunk, Run Storage, Masked-AV 22-frame, Second Pass). Needs ComfyUI â‰¥0.32 (we're on 0.34.3 âœ…) but is a **different workflow paradigm** + has **open Issue #13 (long-continuation drift)**. Revisit only if the simple chain proves insufficient.
- **Adudeguyman/ComfyUI-H3-Project-Suite** = already ruled out (D091 â€” conflicts with NikoDemon80).
- **RefMod safetensors** (from the Reddit thread) = dead-end for our character (D046 â€” public RefMods are other people's characters).

**CRITICAL CONFLICT FOUND + RESOLVED:** both the Extender and the original NikoDemon80 pack register 3 identical class types: `MiniMaxH3MotionContext`, `MiniMaxH3MotionContextLoadLatent`, `MiniMaxH3MotionContextSaveLatent`. Since `ComfyUI-H3-Motion-Context` loads before `ComfyUI-Minimax-H3-Extender` (alphabetical folder order), the Extender's **manual** `MiniMaxH3MotionContext` (widget layout: `conditioning, vae, latent, context_frames IMAGE, context_length, encode_mode, anchor_mode, crop, audio_context_length, audio_mode, target_start`) would silently override the original's **auto** node (widgets `[22, 24]`) that our F/G workflows use (F nodes 161/162/164) â†’ F/G would break. **FIX APPLIED:** renamed the Extender's 3 conflicting class-type keys in `custom_nodes\ComfyUI-Minimax-H3-Extender\nodes.py` `NODE_CLASS_MAPPINGS`/`NODE_DISPLAY_NAME_MAPPINGS`:
- `MiniMaxH3MotionContext` â†’ **`MiniMaxH3MotionContextManual`** (display "MiniMax H3 Motion Context (Manual)")
- `MiniMaxH3MotionContextSaveLatent` â†’ **`MiniMaxH3SaveLatent`** (display "MiniMax H3 Save AV Latent")
- `MiniMaxH3MotionContextLoadLatent` â†’ **`MiniMaxH3LoadLatent`** (display "MiniMax H3 Load AV Latent")
The Extender's unique nodes (`MiniMaxH3VideoExtender`, `MiniMaxH3VideoMerge`, `MiniMaxH3LoopTrim`) were already conflict-free. **VERIFIED post-restart (2026-09-28):** all 6 Extender nodes + all 6 original-pack nodes (`MiniMaxH3MotionContext`, `MiniMaxH3MotionContextLoadLatent`, `MiniMaxH3MotionContextSaveLatent`, `MiniMaxH3MotionContextTrim`, `MiniMaxH3MotionContextChain`, `MiniMaxH3MotionContextSeamProbe`) present in live `/object_info` â†’ both packs coexist. `jaisal_intro_F_plants_die.json` re-validated **clean (0 errors, 2 known harmless orphan-math warnings 131/132)**.
**Install details:** cloned to `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-Minimax-H3-Extender\` (nodes.py, av_timing.py, h3_audio_grid.py, patch_layout.py, patch_payload.py). Only dep = `opencv-python` (already present: opencv 4.12.0 in embedded Python). Auto-applies hot-patches at load (layout patch, payload patch preventing Ref2VA overwriting motion context, Turbo LoRA `_make_adaln_forward` patch). Example workflows: `video_minimax_h3_r2v_extend_pre_latent.json` (pure latent, recommended) + `video_minimax_h3_r2v_extend_video.json` (external MP4).
**Reason:** the user's production pipeline (Reddit "long minimaxh3 videos" thread) centers on chained workflows with seam handling; the Extender is the drop-in seam-smoothing + extend layer that complements (not replaces) our Motion-Context latent-tail chain.
**Status:** DECIDED + INSTALLED + CONFLICT RESOLVED + VERIFIED. ComfyUI restarted (PID 31556) to register the pack.
**NEXT:** (a) user runs F (stop Qwen first, fresh tab) â†’ judge â†’ `clip_00006`; (b) user runs G â†’ `clip_00007`; (c) optionally wire `MiniMaxH3VideoMerge` (seam_smooth=1, color_match=seam_fade) into the Eâ†’F / Fâ†’G seams for a smoother cut; (d) concatenate Aâ†’G (Trim removes 22 pinned head frames) â†’ single 2K upscale â†’ post audio (NO MUSIC, D041).

## D094 â€” Shot F SPLIT into F1 + F2 (pause fix + 15s-limit fix + stronger micro-expressions)

**Date:** 2026-09-28
**Decision:** the single 17s shot F (`jaisal_intro_F_plants_die.json`) came out WELL (camera-guy voice good, character listens, plant sorrow good, detailing good) BUT had 3 problems: (1) **`<pause>`/`<long pause>` tags did NOT work** â€” the character just talked through them (MiniMax ignores timing tags in dialogue); (2) **17s > MiniMax's ~15s limit** (it "will fail" beyond that); (3) **micro-expressions too weak** â€” felt like continuous talking, no cinematic narrative feel. **FIX: split F into TWO shots:**
- **F1 = `jaisal_intro_F1_plants_listen.json` (10s = 240f):** E's ending (plants blooming) â†’ camera-guy question â†’ Jaisal LISTENS (micro-expressions) â†’ speaks "Cinema... or if you want to tell a story... You need effort." Plants stay mostly blooming, left plant's top leaf just begins to droop. **Refs:** ref_image_0 = `kf5_plants_alive_v9_00004_.png` (start), ref_image_1 = `kf6_plants_dead_v9_00004_.png` (end direction). **Latent:** Load clip 5 â†’ Save clip 6.
- **F2 = `jaisal_intro_F2_plants_wither.json` (12s = 288f):** first leaf drooping â†’ fully wilted. "Or you need one or two people... I'm alone... limitations... let's try this show using AI." **Refs:** ref_image_0 = `shot_F1_lastframe.png` (USER STAGES after F1 run â€” see run order), ref_image_1 = `kf6_plants_dead_v9_00004_.png`. **Latent:** Load clip 6 â†’ Save clip 7.
- **G updated:** `jaisal_intro_G_papers.json` LoadLatent 6â†’**7**, SaveLatent 7â†’**8** (chain now A(1)â†’B(2)â†’C(3)â†’D(4)â†’E(5)â†’F1(6)â†’F2(7)â†’G(8)).
**PAUSE FIX (the key lesson):** MiniMax does NOT honor `<pause>`/`<long pause>` timing tags in `<d>` dialogue â€” the character talks through them. **Instead, make the pause a VISUAL PERFORMANCE:** explicit SILENT mouth-closed beats written as action lines ("SILENT beat â€” his mouth stays CLOSED. A slow, heavy blink. His gaze drops to the plant. A quiet, honest, almost tired look settles. His shoulders drop a little more. (NO mouth movement during this beat.)") + a dedicated **MICRO-EXPRESSIONS** section (slow blink, gaze drop, subtle frown, small breath, shoulders dropping, eyes glisten, small swallow, determined glint) + negatives `talking through the pause, mouth moving during the silent beat`. The mood shift (bloomâ†’wilt, hopeâ†’limitationâ†’resolve) is carried by the VISUALS + the plant action, not by timing tags.
**TIMING:** user extended to 10s/12s (from 8s/10s) â€” "the whole mood should change with this dialogue, with passion... that little stop and being natural is actually necessary in this intro." Both under the 15s limit.
**Built via `utilities\build_F1_F2.py`** (clones F, sets length 240/288, swaps prompt, sets F2 ref_image_0 = `shot_F1_lastframe.png`, bumps F2 latent 6â†’7, bumps G 7â†’8). All 3 workflows validate clean (0 errors, 2 known harmless orphan-math warnings 131/132). Prompts saved `Jaisal-intro\prompts\shot_F1_plants_listen.txt` + `shot_F2_plants_wither.txt`.
**F1/F2 FIX (2026-09-28, after first F1 run):** user ran F1 â€” dialogue good, BUT (1) **the dead-plant ref (ref_image_1 = `kf6_plants_dead_v9`) FORCED the plant death** â€” MiniMax saw the end-state and jumped to it, instead of the natural slow wither (leaves falling, plants slowly dying) that the original 17s F did well. (2) **character looked WAY TOO DOWN** â€” the prompt's repeated "eyes downcast / gaze drops to the plant" made him stare at the table instead of facing the camera / listening to the camera guy. **FIX (via `utilities\fix_F1_noref.py` + prompt edits):** (a) **F1 = FIRST-REF-ONLY** â€” removed node 139 (LoadImage `kf6_plants_dead_v9`) + link 317 + cleared node 136 `ref_image_1` link; F1 now has ONLY ref_image_0 = `kf5_plants_alive_v9` (blooming start). The prompt guides the natural slow wither: "top leaf slowly droops, a few leaves gently fall, plants begin to slowly wither â€” but STILL MOSTLY ALIVE at the end. Do NOT show fully dead plants." (b) **FACES THE CAMERA** â€” both F1 + F2 prompts now say Jaisal FACES THE CAMERA, eyes toward the lens, LISTENING to the off-screen voice; only a BRIEF glance at the plant then back to the camera. Added negatives `character looking down at the table, character facing away from the camera, character NOT facing the camera` (F1 also `plants fully dead, plants already dead, plants suddenly dead, forced plant death`). **F2 KEEPS the dead-plant ref** (ref_image_1 = `kf6_plants_dead_v9`) â€” that's where it's SUPPOSED to end fully wilted; only its character-facing was fixed. **Both re-validated clean (0 errors).** **LESSON: a dead/end-state reference image FORCES the model to jump to that state â€” for a shot where the change should be SLOW and natural, use FIRST-REF-ONLY (start anchor) + let the PROMPT guide the gradual change; reserve the end-state ref for the shot that's SUPPOSED to end there. And "gaze drops to the plant" repeated too many times makes the character stare at the table â€” anchor them FACING THE CAMERA with only a BRIEF glance.**
**F1 SPEAKER-ATTRIBUTION FIX (2026-09-28, 2nd + 3rd attempt â€” user ran F1 twice, both times Jaisal SPOKE the off-screen question instead of it being heard as an off-screen voice):**
- **Attempt 2 (prompt sharpening â€” FAILED):** added a SPEAKER ATTRIBUTION (CRITICAL) block + heavy lip-lock language ("mouth COMPLETELY CLOSED, does NOT mouth the question") + negatives `Jaisal speaking the question, lip-sync to the off-screen voice`. **Still failed** â€” Jaisal spoke the question.
- **ANALYSIS (why the 17s F `jaisal_intro_F_plants_die_00001_` WORKED â€” user's hypothesis confirmed):** the 17s F's TIMING is the key: (1) question at 00:00â€“00:03 (3s, off-screen), (2) Jaisal's first line starts IMMEDIATELY at 00:03 (no long silent gap), (3) micro-expressions FUSED into the speaking lines ("as he speaks, a leaf falls..."). The model sees a clear pattern: off-screen question â†’ character responds â†’ the question reads as "background" because the character's own speech anchors him as the speaker of the RESPONSE. F1 BROKE this by compressing the question to 2s + inserting a long explicit "SILENT thinking beat â€” mouth CLOSED" (3s) + heavy lip-lock language â€” the long silence + lip-lock backfired, the model "filled" the silence by having the character mouth the question.
- **Attempt 3 (TIMING MIMIC â€” current, BUILT + VALIDATED):** F1 prompt rewritten to mimic the 17s F exactly: 00:00â€“00:03 question (listening, eyes downcast) â†’ 00:03â€“00:06 Jaisal's first line RIGHT AFTER ("Cinema... or if you want to tell a story...") â†’ 00:06â€“00:10 "You need effort." + plant-wither micro-expressions fused in. REMOVED: the long silent beat, the SPEAKER ATTRIBUTION block, the heavy lip-lock language, the "Jaisal speaking the question" negatives. Micro-expressions fused into the action (like the 17s F). F1 = first-ref-only (blooming start) + natural slow wither (still mostly alive at end) â€” unchanged from attempt 2. **Validates clean (0 errors).**
- **RULE: for an off-screen question + character response, the character's first line must start IMMEDIATELY after the question (no long silent gap). A long explicit "silent beat" + heavy lip-lock language makes H3 mouth the question. Mimic the timing of a WORKING take.**
- **FALLBACK if attempt 3 still fails (D090, guaranteed):** strip the H3 audio in post (`ffmpeg -i <take>.mp4 -an -c:v copy <take>_silent.mp4`) + dub the camera-guy question in post â€” the video shows Jaisal LISTENING (silent), the question is added as audio in post.
**F1 TIMING-MIMIC WORKED (2026-09-28, user: "that came good"):** the 17s-F timing mimic (question 00:00â€“00:03 â†’ first line 00:03 â†’ "You need effort." 00:06) fixed the speaker-attribution â€” the question is now heard as an off-screen voice, Jaisal does NOT mouth it. **F1 is DONE.**
**G EXTENDED TO 15s + 5 REFS + PLANT-SHRINKING (2026-09-28, user: "lets extend it to 15 seconds... precisely mention the ref images, which is which, and whats the role of it... minimax can handle 9 ref image and 3 videos, so it can handle it pretty much... lets go for the final shot"):** G was 11s (264f) with 2 refs (kf7a_v4 start + mic+paper end). **FIX (via `utilities\build_G_v2_15s.py`):** (1) **length 264 â†’ 360 (15s)**; (2) **3 new LoadImage nodes** (165/166/167) for the object refs, wired to node 136 `ref_image_2/3/4` (slots 5/6/7, links 318/319/320); (3) **prompt rewritten** (`Jaisal-intro\prompts\shot_G_papers_v2_15s.txt`) with a **REFERENCE IMAGES section** that precisely defines each ref by name + role: `<Picture 1>` = `kf7a_v4.png` (START â€” Jaisal seated, dead plants on table, papers floating in), `<Picture 2>` = `mic+paper.png` (END â€” Jaisal gone, papers + mic), `<Picture 3>` = `obj_cricket_bat_00002_.png` (CRICKET BAT â€” flies in 00:09â€“00:11), `<Picture 4>` = `obj_soccer_ball_00002_.png` (SOCCER BALL â€” rolls in 00:09â€“00:11), `<Picture 5>` = `obj_paper_smiley_00002_.png` (SMILEY PAPER â€” settles on top of bat). **PLANT-SHRINKING (Option A, user's choice):** the dead plants from F2's end SLOWLY SHRINK and DISAPPEAR while Jaisal speaks (00:04â€“00:07) â€” NOT simultaneous with the mic/papers (Option B rejected: too many things at once = cluttered). **TIMING:** 00:00â€“00:02 papers float in â†’ 00:02â€“00:04 camera guy's question â†’ 00:04â€“00:07 Jaisal speaks "As I said... stories, politics, sports, fantasy" + plants shrink â†’ 00:07â€“00:09 mic emerges + "I don't know if it'll work... Let's see." â†’ 00:09â€“00:11 cricket bat + soccer ball + smiley paper enter â†’ 00:11â€“00:13 Jaisal VANISHES + camera guy "Let's see." â†’ 00:13â€“00:15 end on papers + mic + cricket objects + Jaisal gone. **Validates clean (0 errors, 29 nodes).** **RULE: for a shot with multiple object entrances, assign each object ref an EXPLICIT job + timing in the prompt (per the R2V guide) â€” don't just dump refs. And sequence the visual changes (one major change at a time) rather than simultaneous (cluttered). MiniMax handles up to 9 refs + 3 videos, so 5 refs is fine.**
**F2 EXTENDED TO 15s + SILENT BEATS AS DOMINANT FEATURE (2026-09-28, user: "F2 can be 15s... he is continuously speaking instead of expressing"):** F2 was 12s with 3s silent beats â†’ the character rushed through the lines (continuous talking). **FIX:** extended to **15s (360f)** and made the **SILENT beats the dominant feature** (4s each): 00:00â€“00:03 "You need effort. Or you need one or two people with you." â†’ **00:03â€“00:07 SILENT beat (4s)** (slow heavy blink, brief glance at plant, quiet honest tired look, shoulders dropping, NO mouth movement) â†’ 00:07â€“00:09 "I'm alone right now." â†’ **00:09â€“00:13 SILENT beat (4s)** (slow blink, eyes glisten, small swallow, weight of being alone settling, NO mouth movement) â†’ 00:13â€“00:15 "So there are some limitations... let's try this show using AI." (determined glint). The MICRO-EXPRESSIONS section now explicitly states "the SILENT beats are the dominant feature, not the talking." **Validates clean (0 errors).** **RULE: when a character "continuously speaks instead of expressing," extend the shot length + make the silent/expression beats LONGER (4s) so they dominate â€” the character needs ROOM to express (slow blink, gaze drop, shoulders dropping, eyes glisten, swallow) between lines, not a rush to the next line.**
**Status:** DECIDED + BUILT + VALIDATED. F1 DONE (timing-mimic worked). F2 15s + dominant silent beats READY. Awaiting user run.
**RUN ORDER (user, stop Qwen first, fresh tabs):** (1) run F1 â†’ judge (starts on E's ending? listens with micro-expressions? leaf starts drooping?) â†’ `clip_00006`; (2) **stage F1's last frame:** `seedvr2_lastframe_2k.json` (LoadVideo = F1 take) â†’ `output\lastframe_2k_00001_.png` â†’ copy to `input\shot_F1_lastframe.png` (F2's ref_image_0 already points there); (3) run F2 â†’ judge (starts on F1's ending? plants fully wilt by end? determined glint?) â†’ `clip_00007`; (4) run G â†’ `clip_00008`; (5) restart Qwen. **THEN:** concatenate Aâ†’Bâ†’Câ†’Dâ†’Eâ†’F1â†’F2â†’G (Trim removes 22 pinned head frames) â†’ single 2K upscale â†’ post audio (NO MUSIC, D041).

### D094b â€” G1 issues fixed in prompt (2026-09-15)
- **G1 result:** (1) music instead of paper-blast sound, (2) Jaisal FADED (opacity) instead of bursting into papers, (3) mic came WITH the paper burst.
- **Fixes in shot_G_papers_v2_15s.txt:**
  1. **Paper-blast sound:** AUDIO section now says LOUD natural PAPER BLAST (rustling/whooshing sheets) + explicit 'NOT music' on the burst.
  2. **Burst not fade:** 00:11-00:13 now says Jaisal BURSTS INTO papers â€” body EXPLODES OUTWARD into sheets that scatter (NOT a fade/opacity reduction). NEGATIVE: 'Jaisal fading out, dissolving, opacity reducing, disappearing like a fade'.
  3. **Mic separate:** 00:07-00:09 mic emerges SEPARATELY from the dark (NOT together with the paper burst). NEGATIVE: 'microphone appearing together with the paper burst, microphone appearing before 00:07'.
- **Lesson:** MiniMax defaults to FADE for 'disappears' â€” must say BURST/EXPLODES + negative 'fading/dissolving/opacity'. And simultaneous entrances (mic + papers) get merged â€” sequence them with explicit 'SEPARATELY' + timing.

### D095 â€” G split into G1 (burst) + G2 (aftermath) (2026-09-28)
- **Problem:** single 15s G kept the character "staying" â€” as soon as the paper burst happened the character should be GONE, but MiniMax left him in frame.
- **Decision:** split G into TWO chained shots so the hard "disappear" moment is isolated and the aftermath has NO character reference at all:
  - **G1 `jaisal_intro_G1_burst.json`** (10s/240f): ref_image_0=`kf7a_v4.png` (character at table), ref_image_1=`jaisal_gone_papers_alone.png` (papers only, empty chair). Character present -> speaks -> **BURSTS INTO papers -> GONE** by 00:08-00:10. End ref anchors "character gone". Load clip 7 (F2 tail) -> save clip 8.
  - **G2 `jaisal_intro_G2_aftermath.json`** (10s/240f): ref_image_0=`jaisal_gone_papers_alone.png` (papers only, NO character), ref_image_1=`mic+paper.png` (papers+mic), + object refs cricket bat/soccer ball/smiley paper. **NO character at all** â€” camera guy's off-screen voice "Let's see." + mic emerges + objects enter. Load clip 8 (G1 tail) -> save clip 9.
- **Why it works:** G2 has no character reference, so the character CANNOT "stay" â€” MiniMax only has papers+objects to track. The burst is isolated into G1 where the end ref (papers only) forces the character out.
- **Latent chain now:** A(1)->B(2)->C(3)->D(4)->E(5)->F1(6)->F2(7)->G1(8)->G2(9).
- **Old files superseded:** `jaisal_intro_G_papers.json` (15s single) and `jaisal_intro_G_vanish_burst.json` (old 3s) are now superseded by G1+G2.
- **Prompts:** `Jaisal-intro/prompts/shot_G1_burst_10s.txt`, `Jaisal-intro/prompts/shot_G2_aftermath_10s.txt`.
- **Build script:** `utilities/build_G1_G2_split.py` (clones G_papers, swaps refs/prompt/length/latent, removes object-ref nodes for G1).

### D096 â€” G = SINGLE 11s SEQUENTIAL take (supersedes D095 G1/G2 split) (2026-09-28)
- **User correction:** the G1/G2 split was overcomplicating it. The real structure (from the user's pasted prompt) is ONE continuous 11s take where the transformation is SEQUENTIAL, not simultaneous:
  1. Camera guy asks the question FIRST (00:00â€“00:01).
  2. Each object is triggered by its SPECIFIC WORD: PAPERS for "à´•à´¥à´•àµ¾" (stories, 00:02â€“00:03), MICROPHONE for "à´°à´¾à´·àµà´Ÿàµà´°àµ€à´¯à´‚" (politics, 00:03â€“00:04), CRICKET BAT + SOCCER BALL for "à´•à´¾à´¯à´¿à´•à´‚" (sports, 00:04â€“00:05), PAPER SMILEY on the bat for "fantasy" (00:06â€“00:07).
  3. ONE ACTION AT A TIME â€” NOT a 9-second paper explosion. The PAUSE after each word gives MiniMax time to physically appear + settle each object.
  4. Jaisal REMAINS PRESENT through the whole object sequence and DISAPPEARS at ONE clean moment on "à´¨àµ‹à´•àµà´•à´¾à´‚" (00:09â€“00:10) â€” chair empty, objects remain.
  5. Camera guy answers "à´¨àµ‹à´•àµà´•à´¾à´‚" (00:10â€“00:11), bulb flickers, CUT TO BLACK.
- **Why the split was wrong:** splitting into G1 (burst) + G2 (aftermath) put the object-entrances in G2 with NO character, but the user wants the character PRESENT while the objects appear (he watches them), and the disappearance is ONE clean beat, not a "burst". The sequential single take keeps the character in frame for the whole object sequence.
- **Built:** `jaisal_intro_G_revolt.json` (11s/264f, 1344Ã—768, 5 refs: kf7a_v4 start, mic+paper end, obj_cricket_bat, obj_soccer_ball, obj_paper_smiley). Latent: Load clip 7 (F2 tail) â†’ Save clip 8. Prompt: `Jaisal-intro/prompts/shot_G_revolt_11s.txt`. Built via `utilities/build_G_revolt_11s.py` (clones G_papers, length 360â†’264, swaps prompt). Validates clean (0 errors, 29 nodes).
- **Chain now A(1)â†’B(2)â†’C(3)â†’D(4)â†’E(5)â†’F1(6)â†’F2(7)â†’G(8).** (G = single 11s take, NOT G1+G2.)
- **SUPERSEDED:** D095 G1/G2 split (`jaisal_intro_G1_burst.json`, `jaisal_intro_G2_aftermath.json`) â€” keep as backups, do NOT run. `jaisal_intro_G_papers.json` (15s) + `jaisal_intro_G_vanish_burst.json` (old 3s) also superseded.
- **KEY LESSON:** for a shot where a character watches a SEQUENCE of objects appear, keep it ONE continuous take with the character PRESENT, trigger each object by its specific word, use pauses + micro-expressions to give MiniMax time per object, and make the disappearance ONE clean beat (not a burst). Do NOT split into character-present + character-absent shots.

### D096 update â€” G_revolt extended to 15s + GRADUAL disappearance (2026-09-28)
- **User verdict on the 11s G_revolt run: "that was good"** â€” the sequential one-action-at-a-time structure WORKED (objects on their words, character at the table makes sense).
- **Changes (user's ask):** (1) length 11s â†’ **15s (360f)**; (2) fix the SUDDEN removal of the character AND the plant â€” give both proper gradual detail; (3) second 14 = bulb flicker, second 15 = COMPLETE BLACK; (4) everything else stays the same.
- **New timing (15s):** 00:00â€“00:01 question â†’ 00:01â€“00:02 "à´ªà´±à´žàµà´žà´ªàµ‹à´²àµ†..." â†’ 00:02â€“00:03 PAPERS ("à´•à´¥à´•àµ¾") â†’ 00:03â€“00:04 MIC ("à´°à´¾à´·àµà´Ÿàµà´°àµ€à´¯à´‚") â†’ 00:04â€“00:05 BAT+BALL ("à´•à´¾à´¯à´¿à´•à´‚") â†’ 00:05â€“00:06 "à´ªà´¿à´¨àµà´¨àµ†..." â†’ 00:06â€“00:07 SMILEY PAPER ("fantasy") â†’ 00:07â€“00:08 "à´‡à´¤àµŠà´•àµà´•àµ†à´¯à´¾à´£àµ à´‰à´¦àµà´¦àµ‡à´¶à´¿à´•àµà´•àµà´¨àµà´¨à´¤àµ" â†’ 00:08â€“00:09 "à´¨à´Ÿà´•àµà´•àµà´®àµ‹ à´Žà´¨àµà´¨à´±à´¿à´¯à´¿à´²àµà´²..." â†’ **00:09â€“00:10 "à´¨àµ‹à´•àµà´•à´¾à´‚" â€” Jaisal BEGINS to come apart (outline softens, edges turn into paper sheets, form loses solidity â€” NOT a sudden pop)** â†’ **00:10â€“00:11 disappearance COMPLETES (silhouette thins into final sheets, chair empty â€” SLOW, DETAILED, GRADUAL over 2s)** â†’ 00:11â€“00:12 camera guy "à´¨àµ‹à´•àµà´•à´¾à´‚" â†’ 00:12â€“00:13 still beat â†’ **00:13â€“00:14 bulb FLICKERS once** â†’ **00:14â€“00:15 COMPLETE BLACK, CUT TO BLACK**.
- **PLANT BEHAVIOR section added:** dead plants SLOWLY CRUMBLE and WITHER throughout the shot (leaves curl to dust, stems bend and sink) â€” gradual, detailed, NOT a single-frame vanish; they crumble away as the new objects appear.
- **CHARACTER DISAPPEARANCE section added:** dedicated 2-beat gradual unraveling (00:09â€“00:11) with explicit "NOT a sudden pop / NOT a single-frame cut / NOT a teleport" wording.
- **Negatives added:** `Jaisal vanishing in a single frame, Jaisal popping out suddenly, the plants vanishing in a single frame, the plants popping out suddenly, the plants disappearing before the character`.
- **Prompt:** `Jaisal-intro/prompts/shot_G_revolt_15s.txt` (14353 chars). Workflow `jaisal_intro_G_revolt.json` updated in place (length 264â†’360, prompt swapped). Validates clean (0 errors, 29 nodes).
- **KEY LESSON:** when a disappearance looks "sudden", give it a DEDICATED 2-second gradual process with per-second detail (outline softens â†’ edges turn to paper â†’ silhouette thins â†’ chair empty) + negatives for single-frame vanish/pop-out/teleport. Same for plants: crumble/wither over the whole shot, not a single-frame vanish.

### D096 update 2 â€” G_revolt v2: camera-guy voice timing + LOW mic (2026-09-28)
- **User verdict on the 15s G run: "we're almost there"** â€” two corrections: (1) the FIRST dialogue (the question) should come from the CAMERA MAN (off-screen), not be mouthed by Jaisal; (2) the mic should settle a LITTLE LOWER so Jaisal's face stays visible.
- **Fix 1 â€” camera-guy voice (the PROVEN F1 timing-mimic workaround, UPDATE 4):** (a) question gets a FULL 3s off-screen beat (00:00â€“00:03) with Jaisal's mouth COMPLETELY CLOSED (he only listens); (b) Jaisal's first line starts IMMEDIATELY after the question (00:03, "à´ªà´±à´žàµà´žà´ªàµ‹à´²àµ†... à´•à´¥à´•àµ¾...") â€” NO long silent gap (a long silent beat + heavy lip-lock makes H3 mouth the question); (c) dedicated SPEAKER ATTRIBUTION (CRITICAL) block: two distinct speakers, <Subject 2> is AUDIO ONLY, Jaisal's mouth moves ONLY for his own lines; (d) negatives: `Jaisal speaking the question, the visible character speaking the off-screen line, lip-sync to the off-screen voice, Jaisal's lips opening before 00:03, a long silent gap between the question and Jaisal's first line`.
- **Fix 2 â€” LOW mic:** the microphone settles LOW on the table â€” its top stays BELOW Jaisal's face level so his face remains fully visible and unobstructed (stated in the 00:05â€“00:06 beat, the CHARACTER CONSISTENCY section, and negatives `the microphone blocking Jaisal's face, the microphone rising above Jaisal's face level`).
- **Timing shift:** everything after the question shifts +2s (question 00:00â€“00:03 â†’ papers 00:03â€“00:05 â†’ mic 00:05â€“00:06 â†’ bat+ball 00:06â€“00:07 â†’ "à´ªà´¿à´¨àµà´¨àµ†" 00:07â€“00:08 â†’ fantasy 00:08â€“00:09 â†’ "à´‡à´¤àµŠà´•àµà´•àµ†..." 00:09â€“00:10 â†’ "à´¨à´Ÿà´•àµà´•àµà´®àµ‹..." 00:10â€“00:11 â†’ "à´¨àµ‹à´•àµà´•à´¾à´‚" + disappearance begins 00:11â€“00:12 â†’ completes 00:12â€“00:13 â†’ camera guy "à´¨àµ‹à´•àµà´•à´¾à´‚" 00:13â€“00:14 â†’ bulb flicker + COMPLETE BLACK 00:14â€“00:15).
- **Prompt:** `Jaisal-intro/prompts/shot_G_revolt_15s_v2.txt` (15290 chars), synced into `jaisal_intro_G_revolt.json` node 138. Validates clean (0 errors, 29 nodes).
- **RULE:** for an off-screen question + character response, use the F1 timing-mimic (3s question beat, mouth closed, first line IMMEDIATELY after, no long silent gap) â€” this is the proven workaround. Keep objects LOW so they don't block the character's face.

### D096 update 3 â€” Qwen-Image-Edit small-mic reference (2026-09-28)
- **User verdict on the v2 G run:** the character STILL mouths the off-screen question AND the mic is STILL huge. Two fixes: (1) remove the question's `<d>` line from the video entirely (00:00â€“00:03 = pure silent-listen beat) + DUB the camera-guy question in post (prompt-only attribution never fully holds, D090); (2) the mic is anchored huge by the END REFERENCE `mic+paper.png` (1928Ã—1088, big broadcast mic on a tall stand) â€” prompt words "small" cannot beat a reference image.
- **Fix 1 â€” question removed from video:** `shot_G_revolt_15s_v3.txt` (14862 chars) drops the question's `<d>` line; 00:00â€“00:03 is a pure silent-listen beat (Jaisal mouth closed), the question is DUBBED IN POST.
- **Fix 2 â€” small-mic reference via Qwen-Image-Edit:** built `qwen_edit_small_mic.json` (via `utilities/build_qwen_edit_small_mic.py`, validates clean 0 errors/0 warnings, 10 nodes) to EDIT `mic+paper.png` â†’ `mic+paper_small.png` (small compact mic on a short low stand, everything else identical). Chain: LoadImage `mic+paper.png` â†’ `TextEncodeQwenImageEdit` (positive "Make the microphone SMALL and COMPACT, on a SHORT LOW stand... Keep EVERYTHING ELSE exactly the same" + negative "large microphone, tall stand, color, people, extra objects") + `UnetLoaderGGUF` (`Qwen-Image-Edit-2509-Q8_0.gguf` 21.76 GB, fits 32 GB VRAM no offload) + **`CLIPLoader` (`qwen_2.5_vl_7b_fp8_scaled.safetensors`, `qwen_image`, `default`)** + `VAELoader` (`qwen_image_vae.safetensors`) + `EmptyQwenImageLayeredLatentImage` (1920Ã—1088) + KSampler (8 steps, cfg 1.0, euler/simple, denoise 1.0) + VAEDecode + SaveImage `jaisal_cut/mic_small`. **G's node 139 (ref_image_1) now points at `mic+paper_small.png`.**
- **Build bugs fixed:** (1) link 103 (VAEâ†’node 5) was at slot 2 colliding with image â€” moved to slot 1 (native order clip/vae/image/prompt); (2) link 106 (negative conditioning) came from node 5 (positive) â€” must come from node 10 (negative TextEncode); (3) **TEXT-ENCODER DIMENSION MISMATCH** â€” first build used `CLIPLoaderGGUF` + `qwen3vl_4b_fp8_scaled.safetensors` (Qwen3-VL-4B, 2560-dim) which crashed at sample time with `RuntimeError: Given normalized_shape=[3584], expected input with shape [*3584], but got input of size[1, 1152, 2560]`. The Qwen-Image-Edit-2509 UNet's `txt_norm` needs **3584-dim = Qwen2.5-VL-7B**. **Fix: `CLIPLoader` (not GGUF) + `qwen_2.5_vl_7b_fp8_scaled.safetensors` + type `qwen_image`.** (4) **EDIT vs GENERATION WIRING (user: "no change, qwen edit doesnt work like that... none of them has any changes apart from lighting")** â€” the first working build used `EmptyQwenImageLayeredLatentImage` (empty latent) + `denoise=1.0` = **TEXT-TO-IMAGE**, not an edit: it re-drew the scene from scratch each run, so the big-mic prior in `mic+paper.png` won and only lighting varied (6 runs, all identical). **Fix: encode the ACTUAL input image with `VAEEncode` (pixels = LoadImage, vae = VAELoader) and feed that latent to the KSampler; `denoise=1.0` is CORRECT for a dedicated editing model (it's trained to preserve the input while applying the edit â€” unlike base SD where 1.0 = full regeneration); 20 steps (not 8).** **RULE: image-edit = `LoadImage â†’ VAEEncode â†’ KSampler(latent_image=encoded, denoise=1.0)`. NEVER use an empty latent for an edit â€” that's generation, not editing.**
- **RULE:** when a reference image anchors an unwanted attribute (huge mic), EDIT THE REFERENCE with an image-edit model (Qwen-Image-Edit GGUF) rather than fighting it with prompt words. When a character mouths an off-screen line, REMOVE the line from the video + dub it in post (prompt-only attribution never fully holds).

### D096 update 4 â€” small-mic ref = Krea2 INPAINT with MANUAL mask (supersedes update 3 Qwen-Image-Edit) (2026-09-28)
- **Qwen-Image-Edit failed twice:** (a) empty-latent + denoise 1.0 = text-to-image regeneration (big-mic prior won, only lighting varied); (b) VAEEncode + denoise 1.0 = the edit model's prior is too strong, mic stayed big. **The Krea2 SAM3 inpaint workflow (`krea2_inpaint_kf2_chair.json`) is the proven tool, but its `SAM3Segment` + `CR Upscale Image` nodes are NOT loaded in the live server (no SAM3 pack installed) â†’ that clone can't run.**
- **FINAL: manual mask + standard Krea2 inpaint.** (1) `utilities/make_mic_mask.py` â†’ `input/mic_mask.png` (white = mic region: head ellipse + stand rect + base ellipse, GaussianBlur 12) â€” DETERMINISTIC, no model, no SAM3; (2) `utilities/build_krea2_inpaint_small_mic_v2.py` â†’ `krea2_inpaint_small_mic.json` (validates clean 0 errors/0 warnings, 11 nodes, ALL standard nodes): LoadImage `mic+paper.png` + LoadImage `mic_mask.png` (MASK out) â†’ `VAEEncodeForInpaint` (pixels+vae+mask) â†’ KSampler (Krea2 `krea2_turbo_bf16.safetensors`, CLIPLoader `qwen3vl_4b_bf16.safetensors` type `krea2`, VAELoader `qwen_image_vae.safetensors`, 8 steps cfg 1.0 euler/simple denoise 1.0) â†’ VAEDecode â†’ SaveImage `jaisal_cut/mic_small`. `VAEEncodeForInpaint` keeps everything OUTSIDE the mask pixel-identical, regenerates only the mic. **G's node 139 (ref_image_1) points at `mic+paper_small.png`.**
- **RULES:** (a) when a reference anchors an unwanted attribute, INPAINT that region rather than full-image edit/regeneration; (b) **before handing a workflow to the user, confirm every node class is in the LIVE `/object_info`** (custom packs may not be loaded after a restart) â€” verify, don't guess; (c) verify before the user babysits â€” no more unverified handoffs (the user called out looping 4Ã— this session).

### D096 update 5 â€” INPAINT MECHANISM FIX: `VAEEncodeForInpaint` is NOT a true inpaint (2026-09-28)
- **User verdict on the v2 inpaint run: "the same thing"** â€” mic still big, whole scene shifted. **Root cause: `VAEEncodeForInpaint` does NOT set a noise mask** â€” with `denoise=1.0` it regenerated the WHOLE image, so the big-mic prior won again (confirmed by inspecting `output\jaisal_cut\mic_small_00007_.png`: papers/chair/bulb all re-drawn, mic unchanged). **The mask itself was CORRECT** (verified visually â€” clean head+stand+base coverage).
- **FIX (v3, `utilities/build_krea2_inpaint_small_mic_v3.py` â†’ `krea2_inpaint_small_mic.json`, validates clean 0 errors/0 warnings, 12 nodes):** the correct ComfyUI inpaint mechanism = **`VAEEncode` (full image) + `SetLatentNoiseMask` (mask = mic region) â†’ KSampler**. `SetLatentNoiseMask` is what actually restricts regeneration to the masked region; everything OUTSIDE stays pixel-identical. Chain: LoadImage `mic+paper.png` + LoadImage `mic_mask.png` (MASK out) â†’ `VAEEncode` (pixels+vae) â†’ `SetLatentNoiseMask` (samples+mask) â†’ KSampler (Krea2 `krea2_turbo_bf16.safetensors`, CLIPLoader `qwen3vl_4b_bf16.safetensors` type `krea2`, VAELoader `qwen_image_vae.safetensors`, 8 steps cfg 1.0 euler/simple denoise 1.0) â†’ VAEDecode â†’ SaveImage `jaisal_cut/mic_small`. Prompt strengthened: "its top well below the height of a tall broadcast mic" + negative `tall object`.
- **RULE: true region inpaint = `VAEEncode` + `SetLatentNoiseMask` + KSampler â€” NOT `VAEEncodeForInpaint` (that node does not set a noise mask, so denoise=1.0 regenerates the whole image).**

### D096 update 6 â€” small-mic end ref = Krea2 TEXT-TO-IMAGE from scratch (user-chosen, supersedes update 5 inpaint) (2026-09-28)
- **Why inpaint can't work here:** the mask must cover the old big mic's FULL HEIGHT (head + tall stand) to erase it, so the inpaint region is TALL â€” the model fills a tall region with a tall mic; "small" in the prompt can't beat the region shape + the big-mic prior. Every inpaint attempt (Qwen edit, Krea2 inpaint) came out "the same thing."
- **User chose: regenerate the end reference FROM SCRATCH** (Krea2 t2i) â€” no big-mic prior to fight. Tradeoff accepted: papers/chair/bulb won't be pixel-identical to the original, but that's fine for an R2V anchor (MiniMax animates between start and end).
- **Built `krea2_t2i_small_mic_end.json` via `utilities/build_krea2_t2i_small_mic_end.py` (validates clean 0 errors/0 warnings, 9 nodes, all standard):** UNETLoader `krea2_turbo_bf16.safetensors` + CLIPLoader `qwen3vl_4b_fp8_scaled.safetensors` type `krea2` + VAELoader `qwen_image_vae.safetensors` + CLIPTextEncode (positive = "A SMALL compact studio microphone on a SHORT LOW stand, sitting low on a weathered wooden table, its top well below the height of a tall broadcast mic. Loose sheets of paper with dense handwriting float in the air. A single bare bulb hangs from a thin wire above. Pure black void background. B&W high-contrast cinematic, fine film grain, static camera, medium-wide" + negative = "large microphone, tall stand, broadcast mic, tall object, color, people, a chair, extra objects, ...") + `EmptySD3LatentImage` (1920Ã—1088, matching the original) + KSampler (10 steps cfg 1.0 euler/simple denoise 1.0, seed 42 randomize) + VAEDecode + SaveImage `jaisal_cut/mic_small_end`.
- **RULE: when the unwanted attribute is anchored by the region SHAPE (a tall mic), inpainting can't shrink it â€” regenerate the reference from scratch (t2i) so there's no prior to fight. Inpaint only works when the region is small/localized.**

### D096 update 7 â€” small-mic end ref = Krea2 IDENTITY EDIT v1.2 (user-chosen, supersedes update 6 t2i) (2026-09-28)
- **User rejected t2i-from-scratch:** "this is the reason why i was against creating newly, it completely misses out the basic... we need to give the base image and then do the I2I with identity... the current one has lots of changes especially the table environment etc, keep the identity transfer workflow, don't forget things." t2i threw away the scene (table, papers, chair, bulb, composition).
- **CORRECT TOOL = Krea2 Identity Edit v1.2** (`krea2_identity_edit.json`): takes the BASE image (`mic+paper.png`) and regenerates it keeping the scene identity, applying only the instruction. **Built `krea2_identity_edit_small_mic.json` via `utilities/build_krea2_identity_small_mic.py` (clones `krea2_identity_edit.json`, validates clean 0 errors/0 warnings, 15 nodes):** node 72 LoadImage = `mic+paper.png` (base scene); node 84 = instruction ("Make the microphone SMALL and COMPACT, on a SHORT LOW stand... ONLY ONE microphone... Keep EVERYTHING ELSE exactly the same: papers, table, empty chair, bare bulb, black void, B&W cinematic. Preserve the entire original image exactly. No other changes. No people."); node 85 = negative ("large/tall mic, two mics, color, people, extra objects..."); node 29 SaveImage = `jaisal_cut/mic_small_id`; node 95 (Typnosis typography LoRA) BYPASSED (mode 4, not needed for a mic edit). **Kept the proven identity params:** node 79 `Krea2EditModelPatch` ref_boost=4 (fidelity dial) fit_mode=fit, node 83 `ResolutionSelector` 16:9 2MP, node 53 KSampler 10 steps cfg 1 euler/simple denoise 1, node 71 `LoraLoaderModelOnly` `krea2_identity_edit_v1_2.safetensors` @1.0, UNET `krea2_turbo_fp8_scaled.safetensors`, CLIP `qwen3vl_4b_fp8_scaled.safetensors` type `krea2`, VAE `qwen_image_vae.safetensors`. All krea2edit nodes confirmed LIVE in `/object_info`; identity LoRA present.
- **RULE: to change ONE attribute of a scene while keeping the scene (table/papers/chair/bulb/composition), use the Krea2 Identity Edit v1.2 workflow (base image in node 72 + plain-English instruction in node 84, ref_boost=4) â€” NOT t2i-from-scratch (loses the scene) and NOT inpaint (region-shape prior). This is the project's standard scene-preserving edit tool (D023).**

### D096 update 8 ï¿½ remove EXTRA mic via manual-mask INPAINT (supersedes update 7's 2-mic output) (2026-09-28)
- **User verdict on the identity-edit outputs (mic_small_id_00001/2): "we have 2 mics, remove the extra; others are fine."** Both takes came out with the small silver mic on the short stand (GOOD) PLUS an extra black mic on the left (REMOVE).
- **User chose manual-mask inpaint** ("i will manually draw"). **Built `krea2_inpaint_remove_mic.json` via `utilities/build_krea2_inpaint_remove_mic.py` (validates clean 0 errors/0 warnings, 12 nodes, all standard):** LoadImage `mic_small_id_00001_.png` (base, staged to input) + LoadImage `remove_mic_mask.png` (MASK out) ? `VAEEncode` ? `SetLatentNoiseMask` ? KSampler (Krea2 `krea2_turbo_bf16.safetensors`, CLIPLoader `qwen3vl_4b_bf16.safetensors` type `krea2`, VAELoader `qwen_image_vae.safetensors`, 8 steps cfg 1.0 euler/simple denoise 1.0) ? VAEDecode ? SaveImage `jaisal_cut/mic_single`.
- **MASK RULE:** white = the extra black mic (head + stand + base + its shadow), black = everything else. Mask must be 1928ï¿½1088 (same size as base). A placeholder all-black mask was created at `input\remove_mic_mask.png` ï¿½ user draws over it (or any mask file picked in the LoadImage node).
- **Prompt:** positive = "Remove the extra black microphone... Keep ONLY the small silver microphone on its short low stand... area becomes plain empty weathered wooden table surface matching surrounding wood grain and lighting"; negative = `microphone, mics, two microphones, extra microphone, black microphone, mic stand, ...`.
- **NEXT (user, stop Qwen first, fresh tab):** (1) draw the mask (white over the black mic only); (2) run `krea2_inpaint_remove_mic.json` ? `output\jaisal_cut\mic_single_00001_.png`; (3) pick best ? copy to `input\mic+paper_small.png`; (4) run `jaisal_intro_G_revolt.json` (v3 prompt) ? judge; (5) restart Qwen.
- **RULE: when a generated ref has ONE unwanted object among good content, manual-mask inpaint (VAEEncode + SetLatentNoiseMask) removes just that region ï¿½ everything outside the mask stays pixel-identical.**

### D096 update 8 fix ï¿½ MASK FORMAT BUG: ComfyUI LoadImage MASK = 1 - alpha (2026-09-28)
- **User: "i painted over the other mic, it didnt get removed, whats happening?"** First run was a NO-OP.
- **ROOT CAUSE (verified in nodes.py):** `LoadImage` MASK output = `1 - alpha` ï¿½ a grayscale (mode L) mask has NO alpha channel -> ALL-ZERO mask -> `SetLatentNoiseMask` keeps everything -> output = input. ALSO: the MaskEditor saves to `clipspace-paint-*.png` / `clipspace-mask-*.png`, NOT to the workflow's mask filename (`remove_mic_mask.png` stayed the all-black placeholder).
- **FIX:** `utilities/convert_paint_to_mask.py` ï¿½ takes the user's paint layer (`clipspace-paint-1790600217258.png`, mic region OPAQUE on transparent bg), INVERTS the alpha (`255 - alpha`), feathers edges (GaussianBlur 8), saves proper RGBA `remove_mic_mask.png` (transparent = regenerate). `utilities/overlay_mic_mask.py` renders the regenerate region in RED on the base to verify placement (confirmed: covers the tall black mic head+stand+base, small silver mic untouched). `utilities/inspect_mic_mask.py` = diagnostic (mode/alpha/white-coverage).
- **RULE: manual-mask inpaint mask files MUST be RGBA with the remove-region TRANSPARENT (alpha=0). Verify with an overlay before the user runs. A grayscale white-region mask is a silent no-op.**

### D096 update 8 fix 2 ï¿½ CORRECTED: standard single-LoadImage inpaint (user called out 5h looping) (2026-09-28)
- **User: "its one of the easiest way for an editing model... you're trying to avoid some nodes and we are ending up wasting 5 hours for a simple inpainting."**
- **CORRECTION: `VAEEncodeForInpaint` DOES set the latent `noise_mask`** (verified in nodes.py source: returns `{"samples": t, "noise_mask": mask_erosion.round()}` + zeroes masked pixels). The D096-update-5 claim was WRONG.
- **FINAL = clone the PROVEN `krea2_kf2_manual_inpaint.json`** (worked for the kf2 chair) via `utilities/rebuild_remove_mic_inpaint.py`: ONE `LoadImage` (base = `mic_small_id_00001_.png`) whose MASK output (1-alpha) feeds `VAEEncodeForInpaint` + `SetLatentNoiseMask`; user paints directly on the base image (right-click -> Open in Mask Editor); chain `LoadImage -> VAEEncodeForInpaint -> SetLatentNoiseMask -> KSampler -> VAEDecode -> ImageCompositeMasked -> SaveImage` (`jaisal_cut/mic_single`). Validates clean 0 errors. NO separate mask file, NO alpha-conversion scripts.
- **RULE: when a proven workflow exists, CLONE it ï¿½ swap only image filename + prompts + save prefix. Do not hand-build, do not re-derive mechanisms, do not loop.**

### D096 update 8 fix 3 ï¿½ FINAL: Qwen-Image-Edit-2509 instruction-based edit (supersedes all inpaint attempts) (2026-09-28)
- **User: "this aint working... the workflow i tried now is just a cut paste version of photoshop with bad IQ."** All generation-model inpaint routes (Krea2 VAEEncodeForInpaint, SetLatentNoiseMask, manual masks) failed or were no-ops.
- **FINAL TOOL = Qwen-Image-Edit-2509 (dedicated INSTRUCTION-BASED editing model)** ï¿½ image + natural-language instruction -> edit. NO mask, NO painting. It understands objects ("the black microphone") and finds them itself.
- **Built `qwen_edit_remove_mic.json` via `utilities/build_qwen_edit_remove_mic.py` (clones the WORKING `qwen_edit_small_mic.json` wiring, validates clean 0 errors, 10 nodes):** LoadImage `mic_small_id_00001_.png` -> `TextEncodeQwenImageEdit` (positive = "Remove the black microphone on the right side... Keep ONLY the small silver microphone... area becomes plain empty weathered wooden table surface... Keep EVERYTHING ELSE exactly the same") + `UnetLoaderGGUF` (`Qwen-Image-Edit-2509-Q8_0.gguf` 21.76 GB) + `CLIPLoader` (`qwen_2.5_vl_7b_fp8_scaled.safetensors`, `qwen_image`, `default`) + `VAEEncode` (the ACTUAL input image) + KSampler (20 steps cfg 1.0 euler/simple denoise 1.0 ï¿½ correct for a dedicated edit model) + VAEDecode + SaveImage `jaisal_cut/mic_single`.
- **RULE: for object-level edits (remove/replace ONE object, keep the scene), use an instruction-based editing model (Qwen-Image-Edit-2509), NOT a generation model + mask. Generation-model inpaint = "photoshop with bad IQ" (user's words). Clone the working `qwen_edit_small_mic.json` wiring ï¿½ do not hand-build.**

### D096 update 9 â€” ComfyUI UPDATED to v0.37.0-45 (latest master) + node verification (2026-09-28)
- **User direction: "first thing first Update comfyui, update frontend and backend to the latest."**
- **DONE:** E: install updated v0.34.3 -> **v0.37.0-45-g8d534945** (latest master; latest tag v0.37.4). git stash preserved the D027 VRAM patch; after update, upstream ALREADY removed .clone() (line 177 now  = v.view(s, self.heads, self.head_dim)) so **D027 is now built into upstream â€” no patch needed**. ComfyUI restarted (PID 4624), server up on 8188.
- **NODE VERIFICATION (all critical packs LIVE in v0.37.0-45):** H3SLAAttention, MiniMaxH3ReferenceToVideo, MiniMaxH3MotionContext(+Save/LoadLatent), MiniMaxH3VideoExtender, Krea2EditModelPatch, H3FaceSelect, ControlFoleyGenerate, SeedVR2VideoUpscaler, TextEncodeQwenImageEdit, UnetLoaderGGUF, VAEEncodeForInpaint, SetLatentNoiseMask, ImageCompositeMasked, MiniMaxH3EasyVideoTailSlicer_SatoDive, H3LocalCameraEditor â€” ALL OK (2527 total nodes). SetNode (SetGet-Resolver) NOT in object_info â€” that pack's nodes did not register; NOT needed for the mic-removal task.
- **VERIFICATION GOTCHA:** /object_info returns a JSON STRING; PowerShell ConvertFrom-Json FAILS on duplicate keys (ClownOptions_Frameweights/ClownOptions_FrameWeights). Use the embedded Python (E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe) with json.load (tolerates dup keys, keeps last) to parse + check node presence.
- **EDITING MODELS PRESENT (main path E:\ComfyUI_windows_portable\ComfyUI\models):** Qwen-Image-Edit-2509 (unet/Qwen-Image-Edit-2509-Q8_0.gguf 20.27 GB + 	ext_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors 8.74 GB + ae/qwen_image_vae.safetensors 0.24 GB) = READY. Flux-2-Klein-9B (diffusion_models/flux-2-klein-9b.safetensors 16.91 GB + lux-2-klein-9b-kv-fp8.safetensors 9.14 GB + ae/flux2-vae.safetensors) present BUT its T5 CLIP is MISSING (clip folder only has MiniMax H3 mmproj) â€” NOT ready without downloading the CLIP.
- **RULE: after a ComfyUI update, re-verify every critical node class is in the LIVE /object_info before handing a workflow (custom packs may fail to register). Parse object_info with Python, not PowerShell ConvertFrom-Json.**

### D096 update 10 â€” krea2T2iI2iInpaint2pass_v15 made RUNNABLE (production 2-pass pipeline) (2026-09-28)
- **User: "lets install those nodes and make it work... these are production pipeline we cannot say this is not working when we are going to continuously use these items for next weeks."**
- **Workflow E:\Krea2\krea2T2iI2iInpaint2pass_v15.json** (47 nodes + 1 subgraph; T2I/I2I/Inpaint 2-pass). 3 real blockers found + fixed:
  1. **ApplyKrea2NegPiP** (node 285, MODEL+CLIP passthrough that applies a negative-pipe to the model) â€” the installed comfyui-negpip-zimage is a VENDORED version that intentionally omits the standalone node (its docstring says so; it only registers NegPipPrompt). **FIX: cloned upstream lue-pen5805/ComfyUI-krea2-negpip** into custom_nodes\ComfyUI-krea2-negpip (imports only core comfy modules â€” no extra pip deps), restarted ComfyUI -> node LIVE (2528 nodes). Schema: model+clip required, value_strength (default 1.0), patch_txtfusion_refiners, block_start/end/stride.
  2. **VAE krea2RealVae_v10.safetensors** (node 37) not on disk -> swapped to **qwen_image_vae.safetensors**.
  3. **UNet Krea2_Turbo_convrot_int8mixed.safetensors** (node 259) not on disk -> swapped to **krea2_turbo_fp8_scaled.safetensors** (the Krea2 model used in all our other workflows -> consistent behavior).
- **FIXED COPY:** user\default\workflows\krea2T2iI2iInpaint2pass_v15_fixed.json (via utilities\fix_2pass_models.py). Original preserved.
- **VALIDATION:** 3 real blockers gone. Remaining 5 "errors" = Fast Groups Muter/Bypasser (rgthree) = FRONTEND-ONLY canvas widgets (rgthree-comfy installed -> render fine in UI; validator flags them because they're not server nodes; 7 warnings confirm the server PRUNES them -> no execution effect). NOT blockers. Generation chain intact.
- **RULE: a workflow's "unknown_class_type" errors for rgthree Fast Groups Muter/Bypasser + Note are FALSE POSITIVES â€” they're frontend-only widgets, not server nodes. Check the warnings: if they "feed no output node / server prunes it", they don't block the run. Only unknown_class_type on a node that IS in the execution chain is a real blocker.**
- **RULE: after installing a node pack, restart ComfyUI (Stop-Process the main.py PID, Start-Process with the SAME flags --windows-standalone-build --reserve-vram 4 --enable-manager), then verify the node is in /object_info before handing the workflow.**

### D096 update 11 â€” krea2T2iI2iInpaint2pass_v15 EXPLAINED + CONFIGURED (bf16 krea + turbo LoRA) (2026-09-28)
- **User: "i really need an explanation for this workflow... where should i paint or what... we will go with bf16 krea, and use turbo lora, and vae is already in place, lets set it up, there are some toggles which are custom nodes... i see load image is currently bypassed, so lets make this workflow work and then if it works we will document for future use."**
- **WHAT IT IS:** a Krea2 T2I/I2I/Inpaint **2-pass** workflow (fast 1st-pass KSampler + Clownshark 2nd-pass subgraph for quality) with optional "bells and whistles" toggles.
- **3 MODES (pick one via bottom-of-canvas rgthree Fast Groups toggles):** T2I (no base image) / I2I full image (LoadImage, whole image) / Inpaint (LoadImage + painted mask, region only). **Ships in T2I mode -> that's why LoadImage is BYPASSED (normal, not a bug).**
- **TOGGLES (rgthree Fast Groups, bottom of canvas):** Whatcha Up To? (text2image|image2image), Full Image i2i = On | Inpainting = Off (i2i Entire Image group), Latent Size (Aspect Ratio|Custom Size), Bells and Whistles (Turbo LoRA?|Negative Conditioning|Enhancer|Misc Quality Functions), untitled muter (2nd Pass group). **INPAINT RECIPE:** Whatcha Up To?->image2image; Full Image i2i->OFF; Latent Size->Aspect Ratio; Bells and Whistles->enable Turbo LoRA? + Negative Conditioning.
- **WHERE TO PAINT (inpaint):** set LoadImage to base image -> right-click LoadImage -> "Open in Mask Editor" -> paint the REGENERATE region WHITE -> mask feeds InpaintModelConditioning. **POLARITY CAVEAT:** LoadImage MASK = 1-alpha; if it regenerates the complement, invert the mask.
- **CONFIGURED COPY user\default\workflows\krea2_2pass_bf16_turbo.json (via utilities\configure_2pass.py):** UNet=krea2_turbo_bf16.safetensors (26 GB), Turbo LoRA=krea2_turbo_lora_rank_64_bf16.safetensors @1.0 (enabled in active Power Lora Loader node 279, feeds BOTH passes), VAE=krea2RealVae_v10.safetensors (now available on live server), CLIP=qwen3vl_4b_fp8_scaled.safetensors type krea2, LoadImage=mic_small_id_00001_.png. **NOTE:** author says enable Turbo LoRA only for RAW Krea2; we use Turbo base so it's redundant-but-harmless (toggle off if results look off).
- **MODEL CHAIN:** UNETLoader+CLIPLoader -> ApplyKrea2NegPiP (neg-pipe) -> Krea2T-Enhancer(bypassed) -> ModelSamplingFlux(bypassed)->CFGOverride(bypassed) -> Power Lora Loader(Turbo LoRA) -> [1st pass KSampler 307 (20 steps cfg1 exp_heun_2_x0_sde) + 2nd pass Clownshark subgraph 186] -> previews + Image Saver Simple.
- **VALIDATION:** 5 unknown_class_type errors = Fast Groups Muter/Bypasser (rgthree) = FALSE POSITIVES (frontend-only, server prunes). All real nodes clean.
- **DOC:** docs\KREA2_2PASS_WORKFLOW_GUIDE.md (full guide: modes, toggles, where-to-paint, model chain, run steps, setup scripts).
- **RULE: this is a PRODUCTION pipeline the user will reuse for weeks â€” keep it working + documented. The bottom-of-canvas rgthree Fast Groups toggles are the mode selectors; LoadImage bypassed = T2I mode (normal).**

### D096 update 12 â€” krea2_2pass_bf16_turbo.json set to INPAINT mode + mic-removal prompt (2026-09-28)
- **User: "i dont see you updated the prompt, negative prompt and the image is not active also, just update as per our requirement."**
- **WHY image was "not active":** the workflow ships in **T2I mode** (LoadImage bypassed). Mode is controlled by node modes because the **Any Switch (rgthree)** nodes output the FIRST NON-EMPTY input (Latent switch 271: any_01=EmptyLatentImage/T2I, any_02=InpaintModelConditioning/i2i; MaskChoice 298: any_01=SolidMask/full, any_02=LoadImage MASK/painted).
- **INPAINT MODE set (via utilities\set_2pass_inpaint.py):** LoadImage(265)=active (image=mic_small_id_00001_.png), ImageResizeKJv2(296)=active (1920x1088 landscape), InpaintModelConditioning(267)=active, EmptyLatentImage(254)=BYPASSED, SolidMask(297)=BYPASSED, denoise=1.0.
- **NO separate negative box** â€” negatives are (word:-1.0) tags INSIDE the positive prompt (node 247); ApplyKrea2NegPiP makes them work on Krea2. Prompt set to mic-removal: "Plain empty weathered wooden table surface, ... static camera (black microphone:-1.0) (microphone:-1.0) (mic stand:-1.0) (tall object:-1.0) (color:-1.0) (people:-1.0) (extra objects:-1.0)".
- **VALIDATES clean** (5 false-positive Fast Groups errors only; warnings 7->5).
- **NEXT (user, stop Qwen first, fresh tab):** open krea2_2pass_bf16_turbo.json -> right-click LoadImage -> Open in Mask Editor -> paint the black mic region WHITE -> Queue Prompt -> judge (black mic gone, silver mic + table + papers + chair + bulb intact) -> if it regenerates the COMPLEMENT, invert the mask (LoadImage MASK = 1-alpha).
- **RULE: when a workflow "looks wrong" (image bypassed, no negative box), it's usually in a different MODE â€” check node modes (0=active/4=bypassed) + Any Switch first-non-empty logic, not the prompt. Set mode by flipping node modes, then set prompt/negatives.**

### D096 update 13 â€” krea2_2pass_bf16_turbo.json switched to I2I FULL-IMAGE (table empty base) (2026-09-28)
- **User: "this is worse, the inpainting is bad than the photoshop generative fill... lets go with i2i workflow with the base image D:\models\vsCodeMcp\Jaisal-intro\keyframes, 1) table empty... lets do that same way, paper with small mic, or a small mic should be enough."**
- **INPAINT REJECTED** (worse than Photoshop generative fill). **NEW APPROACH = I2I FULL-IMAGE from the clean base 	able empty.png** (2550x1440, B&W: weathered table + empty chair + bare bulb + black void) -> regenerate the whole scene adding a SMALL compact mic + loose papers, keeping the table/chair/bulb/void/B&W style.
- **DONE (via utilities\set_2pass_i2i_table.py):** (1) staged 	able empty.png -> input\; (2) **I2I FULL-IMAGE MODE:** LoadImage(265)=active (	able empty.png), SolidMask(297)=ACTIVE (full-image mask = i2i, not painted), InpaintModelConditioning(267)=active, EmptyLatentImage(254)=BYPASSED, ImageResizeKJv2(296)=1920x1088 (16:9, matches base aspect), **denoise(270)=0.7** (partial: keep scene, add mic+paper); (3) **PROMPT (node 247)** = "A weathered wooden table with a single empty wooden chair behind it, a single bare bulb hanging from a thin wire above, pure black void background. On the table sits a SMALL compact studio microphone on a SHORT LOW stand, with a few loose sheets of paper with dense handwriting scattered on the table surface. B&W high-contrast cinematic, fine film grain, static camera, medium-wide (large microphone:-1.0) (tall stand:-1.0) (tall object:-1.0) (color:-1.0) (people:-1.0) (extra objects:-1.0) (multiple microphones:-1.0)". **VALIDATES clean** (5 false-positive Fast Groups errors only).
- **NEXT (user, stop Qwen first, fresh tab):** (1) Stop-Process -Name "llama-server" -Force; (2) open **krea2_2pass_bf16_turbo.json** (fresh tab); (3) Queue Prompt -> judge: **small mic (not tall) + paper on table, table/chair/bulb/void/B&W intact?** (4) **IF mic too big/tall:** lower denoise to 0.5 (keeps more base) or strengthen (tall stand:-1.0); **IF it ignores the base:** raise denoise toward 0.8; (5) copy best -> input\mic+paper_small.png; (6) run **jaisal_intro_G_revolt.json** -> clip_00008; (7) Start-Process "D:\models\qwen\Qwen3.827BMTP.bat".
- **RULE: when region INPAINT comes out worse than a full-scene regen, switch to I2I FULL-IMAGE from a clean base (SolidMask active = full-image mask, denoise 0.5-0.8 partial) â€” regenerate the whole scene adding the object, keep the base's composition/style. denoise is the keep-base-vs-add-object dial.**

### D096 update 14 â€” small-mic ref = CLEAN KREA2 I2I (base image + good prompt) â€” the "same trick" (2026-09-28)
- **User: "no no, not the t2i, its i2i with good prompt and better base image... how we created the papers one, lets do the mic also."** (rejected the 2-pass inpaint workflow AND t2i).
- **THE TRICK (same as the refs):** i2i = **LoadImage (better base) + good prompt + partial denoise** -> Krea2 regenerates the scene keeping the base's composition/style, applying the prompt. NOT t2i (no base), NOT the 2-pass inpaint workflow.
- **BUILT krea2_i2i_small_mic.json via utilities\build_krea2_i2i_small_mic.py (validates clean 0 errors/0 warnings, 10 nodes):**
  - **Base = 	able empty.png** (2550x1440, B&W: weathered table + empty chair + bare bulb + black void â€” the BETTER base, no mic to fight) staged to input\.
  - Chain: LoadImage -> VAEEncode -> **KSampler (denoise 0.6, 10 steps, cfg 1, euler/simple)** -> VAEDecode -> SaveImage jaisal_cut/mic_small_i2i. UNET krea2_turbo_bf16.safetensors, CLIP qwen3vl_4b_fp8_scaled.safetensors type krea2, VAE qwen_image_vae.safetensors.
  - **GOOD PROMPT (positive):** "A weathered wooden table with a single empty wooden chair behind it, a single bare bulb hanging from a thin wire above, pure black void background. On the table sits a SMALL compact studio microphone on a SHORT LOW stand, with a few loose sheets of paper with dense handwriting scattered on the table surface. Black and white, high contrast, clean smooth image, no grain, static camera, medium-wide."
  - **NEGATIVE:** "color, ... large microphone, tall stand, tall object, multiple microphones, broadcast mic, big mic".
- **NEXT (user, stop Qwen first, fresh tab):** (1) Stop-Process -Name "llama-server" -Force; (2) open **krea2_i2i_small_mic.json** (fresh tab); (3) Queue Prompt -> output\jaisal_cut\mic_small_i2i_00001_.png; (4) judge: **small mic (not tall) + papers on table, table/chair/bulb/void/B&W intact?** (5) **denoise is the dial:** mic too big/tall or base drifted -> lower to 0.4-0.5 (keeps more base); scene not changing enough -> raise to 0.7-0.8; (6) copy best -> input\mic+paper_small.png; (7) run **jaisal_intro_G_revolt.json** -> clip_00008; (8) Start-Process "D:\models\qwen\Qwen3.827BMTP.bat".
- **RULE: for a scene ref with ONE changed object (small mic), use CLEAN KREA2 I2I = better base image (no unwanted object) + good prompt + partial denoise (0.4-0.8). NOT t2i (loses the scene), NOT the 2-pass inpaint workflow (worse than Photoshop). denoise = keep-base-vs-apply-prompt dial.**

### D096 update 15 â€” SeedVR2 batch upscale = TensorRT STUDIO (not the ComfyUI JSON) + disk-full root cause (2026-09-29)
- **User: "we have all the videos here in the folder... how can i start, is it a batch job in comfyui? or should i try the first one now? i prefer doing 1st one and then batch running all the items."** then **"not the json, this D:\models\SeedVR2-TensorRT-Studio this is studio right"** then **"the seevr workflow went well for the first 2 videos... but got the above error for the third video... i stopped qwen and comfyui, only vram consumer was seedvr2."**
- **DECISION: the batch upscaler = the STANDALONE `D:\models\SeedVR2-TensorRT-Studio` (TensorRT-accelerated browser app at `http://127.0.0.1:7870/`), NOT the ComfyUI `seedvr2_batch_upscale.json`.** The Studio is faster (TensorRT VAE decode), has preview/compare/side-by-side, resumable long renders, and the models are already there (`models\SEEDVR2\seedvr2_ema_7b_sharp_fp16.safetensors` + `ema_vae_fp16.safetensors` + 3B/fp8 variants). Launch: `D:\models\SeedVR2-TensorRT-Studio\Launch SeedVR Studio Pro.bat`.
- **ONE-BY-ONE is the Studio's native mode** (drop a clip â†’ pick 7B Sharp FP16 + 1080p/1440p + `lab` color â†’ preview â†’ full render). The ComfyUI JSON is a single-clip preview tool only (re-point the `video` widget + re-queue 16Ã— for 8 clipsÃ—2 res) â€” NOT a true batch tool.
- **DISK-FULL ROOT CAUSE (the 3rd-video error):** the `RuntimeError: ios_base::badbit set: iostream stream error` + `unexpected pos 896 vs 790` at `torch.save` is a **DISK-WRITE failure, NOT a VRAM error** (user correctly ruled out Qwen/ComfyUI). **D: and E: were at 0 GB free.** Each Studio render writes **~875 MB `decoded_XXX.pt`** (decoded pixel frames, float32, per 21-frame temporal chunk) + **~21 MB `vae_latent_XXX.pt`** per chunk â†’ a 15s clip = 17 chunks â‰ˆ 15 GB. Across 12 job folders that's **196 `.pt` files = 85 GB** of regenerable checkpoint cache (for resumable renders + non-destructive finishing). Videos 1&2 fit; by video 3 the drive was full â†’ `torch.save` failed.
- **FIX APPLIED:** deleted all 196 `*.pt` files (85 GB) from `D:\models\SeedVR2-TensorRT-Studio\outputs` â€” **kept all 24 `*.mp4` results** (75 MB). D: went from 0 GB â†’ **~198 GB free** (verified via `Get-PSDrive`; `Get-Volume` gave a STALE 0 GB read â€” use `Get-PSDrive` for authoritative free space).
- **RULE: the Studio's `outputs\` fills the disk with `.pt` checkpoint cache (99% of the folder). Delete `*.pt` after each finished clip (keep `*.mp4`): `Get-ChildItem "D:\models\SeedVR2-TensorRT-Studio\outputs" -Recurse -File -Filter "*.pt" | Remove-Item -Force`. A 3 TB F: drive (3 TB free) is available for future heavy outputs if D: gets tight.**
- **PLASTIC-LOOK ANSWER (user's question):** SeedVR2 is a GENERATIVE upscaler (7B diffusion re-renders, not a sharpener) â†’ it CAN smooth the hand-drawn brush-stroke/paper texture into a too-clean/CG look. The `sharp` variant preserves the most texture (least plastic). For the B&W sketch style, a NON-generative sharpener (4x-UltraSharp/Real-ESRGAN) is the fallback if it goes smooth/CG. Test clip A at 1080p first, judge the brush texture in the Compare view.
- **STATUS: user ran the first 2 clips successfully ("i m okay with the result"), 3rd failed on disk-full (now fixed). NEXT: re-run the 3rd clip + continue Aâ†’G one-by-one in the Studio, deleting `.pt` between clips.**

### D096 update 16 â€” Post-production plan: black-screen questions + MALAYALAM subtitles + dub (2026-09-29)
- **User: "i will edit it in davinci... im thinking we should have a black screen with letters for the camera guy's question instead of keeping the frame still, because most questions take more than 2 seconds... also we can add subtitles... adding subtitles to the video, keeping it in malayalam, so people can still watch the content, the same way im intending for my main movie also... tomorrow we can dub and complete the progress, 4-5 hours work, we will smash it in the morning."**
- **DECISION 1 â€” BLACK-SCREEN QUESTION CARDS:** the camera guy's questions are OFF-SCREEN (Jaisal's mouth closed) and run >2s. Instead of holding a still frame, insert a **black screen with the question text (Malayalam)** as an intentional "interviewer asks" beat. This is a **DaVinci Resolve edit** (insert black clip + text), NOT a generation task. Applies to all camera-guy questions (shots B, D, F, G).
- **DECISION 2 â€” MALAYALAM SUBTITLES (permanent, for the intro AND the main movie):** burn **Malayalam** subtitles into the video so the content is watchable. **MiniMax H3 CANNOT do this** â€” H3 is a video *generation* model (promptâ†’new video); it does NOT take existing footage and burn captions in. Subtitles are a POST task. **Best options:** (a) **DaVinci Resolve Subtitles tab** (auto-generate from the Malayalam dub via speech-to-text, OR type manually) â€” best since the user is already editing there; (b) **Whisper** (local) transcribe the dub â†’ `.srt`; (c) **manual `.srt`** built from the exact Malayalam dialogue in `docs\INTRO_SCRIPT.md` (most accurate â€” known script, no transcription errors) â†’ burn in DaVinci or ffmpeg. **RECOMMENDATION: manual `.srt` from the script (or DaVinci's subtitle tab) â€” no transcription guesswork. Offer to generate the `.srt` from `INTRO_SCRIPT.md`.**
- **TOMORROW'S PLAN (user: ~4-5h, morning, "smash it"):** (1) finish the SeedVR2 batch upscale (re-run 3rd clip + continue Aâ†’G, delete `.pt` between clips); (2) **DUB** the Malayalam dialogue (user's voice, RVC/OpenVoice â€” see `AUDIO_PIPELINE_PLAN.md`); (3) **LatentSync** mouth-sync to the dub; (4) **DaVinci assembly**: concat 8 clips A(1)â†’B(2)â†’C(3)â†’D(4)â†’E(5)â†’F1(6)â†’F2(7)â†’G(8), insert black-screen question cards, add Malayalam subtitles, swap in the dub audio track. **NO MUSIC (D041) â€” diegetic/natural sound only.**
- **RULE: subtitles + question cards + dub + mouth-sync are ALL post-production (DaVinci + Whisper/LatentSync), NOT generation-model tasks. MiniMax H3 generates video from prompts; it does not caption existing footage.**

### D096 update 17 â€” English subtitles + black question cards BUILT + assembly plan prepared (2026-09-29)
- **User: "i've completed all the upscaling, need english subtitles, thats the pending item along with the dialogue in black screen"** then **"wait, we can do this tmrw, plan how to do this, prepare the plan, dont act now."**
- **STATUS (all 8 clips upscaled = 2520Ã—1440 @ 24fps):** (1) **English .srt** `Jaisal-intro\subs\jaisal_intro_english.srt` â€” 15 cues, **Jaisal's lines ONLY** (camera-guy's lines excluded â€” they live on the black cards). (2) **4 black question cards** `Jaisal-intro\subs\cards\` (`card_B_you_ready`, `card_D_purpose`, `card_F_why_ai`, `card_G_expect`) â€” 2520Ã—1440 @ 24fps, 3s each, Malayalam (large white) + English (smaller grey). Built via `utilities\build_question_cards.py`.
- **TECH LESSON (Malayalam rendering):** ffmpeg `drawtext` (libfreetype) does NOT do complex-script shaping â†’ mangles Malayalam combining marks. **CORRECT ROUTE = ffmpeg `subtitles` filter (libass + HarfBuzz + fribidi â€” all present in the D:\ffmpeg build).** The build writes a per-card `.ass` file (PlayResX/Y = 2520Ã—1440, `{\pos(x,y)}` overlays, styles `Mal` = Arial Unicode MS 120 white / `Eng` = Arial 58 grey) and runs ffmpeg with `cwd=OUT` + a RELATIVE `.ass` filename â€” because absolute Windows paths in the filtergraph break on the drive-colon (`fontfile=C\:/...` fails to parse). **RULE: for complex-script (Malayalam) text on video, use the `subtitles`/`ass` filter (libass), NOT `drawtext`; pass the .ass as a relative filename with cwd set to its folder.**
- **UNVERIFIED:** the card Malayalam rendering has NOT been visually checked yet (Phase 0 tomorrow: extract a frame, view it; if mangled, swap font to `Nirmala.ttc`).
- **TOMORROW'S ASSEMBLY PLAN (phased, in CURRENT_TASK.md):** Phase 0 (no GPU): verify cards + re-time .srt to the ACTUAL concatenated timeline (real clip lengths A=5.17, B=2.13, C=9.21, D=3.54, E=12.75, F1=9.21, F2=14.17, G=14.17; order `Aâ†’card_Bâ†’Bâ†’Câ†’card_Dâ†’Dâ†’Eâ†’card_Fâ†’F1â†’F2â†’card_Gâ†’G`). Phase 1 (GPU, user): DUB (Malayalam, user's voice, RVC/OpenVoice; Jaisal's lines mouth-synced, camera-guy's lines over the cards; NO MUSIC D041). Phase 2 (GPU, user): LatentSync mouth-sync on speaking shots (A, C, E, F1, F2, G). Phase 3 (user, manual): DaVinci assembly (timeline + burn subtitles + swap dub audio + natural SFX + export).

---

## D097 â€” PRODUCTION MOVIE PIPELINE (reusable, DUB-FIRST) â€” the Jaisal-intro is the first instance (2026-10-01)

Date: 2026-10-01
Status: Active (standing pipeline for ALL future films, not just the intro)

### Decision

The Jaisal-intro is the **first instance** of a **reusable production movie
pipeline**. The user will repeat this for more films, so it is captured here as the
standing process. **Order is DUB-FIRST** (audio is the timing spine):

```
SCRIPT â†’ DUB (user) â†’ CLEAN (clean_audio.py) â†’ [RVC for camera-guy lines]
       â†’ LIP-SYNC (LatentSync, speaking shots) â†’ SUBTITLES (re-time .srt to final cut)
       â†’ ASSEMBLY (DaVinci: concat + cards + dub audio + natural SFX + burn subs + export)
```

### Locked facts (user-confirmed 2026-10-01)

1. **FINAL LENGTH = 72s (1:12), NOT 82.34s.** The 4 black question cards are NOT
   full 3s segments â€” they **OVERLAP the clips** (e.g. card_B overlaps shot C), so
   the net timeline is 72s. Do NOT time the .srt against the raw 82.34s concat;
   time it against the FINAL DaVinci cut (72s).
2. **Card audio is NOT muted.** When a card is shown, the underlying clip's audio
   CONTINUES under it (the camera-guy line plays over the card while the scene
   audio carries) â†’ the audience gets audio continuity. Cards are a VIDEO overlay
   on top of the continuing clip, not a silent black segment.
3. **Order:** user dubs â†’ we lip-sync â†’ we add subtitles â†’ final. (Dub first, then
   sync, then subs.)
4. **Voice assignment (D055):** JAISAL = user's own voice (as-is, no RVC); CAMERA
   GUY = user's dub â†’ RVC `midhun_v2_40k` (Midhun timbre).
5. **NO MUSIC (D041):** natural SFX only (footsteps, wind, water, breath, ambient).
6. **Recording app = Audacity** (free): mono, 16-bit, 48 kHz, export WAV, quiet
   room, headset, one take per line. (Fallback: Windows Voice Recorder â€” fine since
   `clean_audio.py` denoises/normalizes.)
7. **Lip-sync = LatentSync** on the SPEAKING shots only (A, C, E, F1, F2, G).
   Listening shots (B, D) have the mouth closed â†’ no sync needed. LatentSync needs
   WSL2 (installed, **reboot pending**). Fallback: if the dub's timing is close to
   the generated mouth, skip lip-sync and just swap the audio track.
8. **DIALOGUE LANGUAGE = MALAYALAM.** The dub is in Malayalam (user speaks
   Malayalam). The English `.srt` subtitles are for the AUDIENCE (non-Malayalam
   viewers). The camera-guy lines are ALSO Malayalam (dubbed by user â†’ RVC Midhun).
   The H3-generated video has English placeholder audio (stripped in post).
9. **PIPELINE CAPTURE (post-intro):** after the intro is complete, build a
   **COMPLETE REFERENCE FOLDER** for the next project â€” all workflows, references
   (keyframes, object refs), the script, latent chain details, prompting ideas,
   card/subtitle pipeline, audio pipeline, assembly notes. Goal: a reusable
   "loop engineering" template for continuous video production.

### Per-film steps (the repeatable checklist)

- **Phase 0 (user):** record ALL lines (Jaisal + camera guy) in Audacity â†’ drop raw
  files in a folder.
- **Phase 1 (me, no GPU):** `clean_audio.py` â†’ 16 kHz mono clean wavs. Camera-guy
  lines â†’ RVC `midhun_v2_40k` (Midhun). Jaisal lines â†’ as-is.
- **Phase 2 (GPU, user runs â€” stop Qwen first):** LatentSync mouth-sync on speaking
  shots (A, C, E, F1, F2, G).
- **Phase 3 (me + user):** re-time the `.srt` to the FINAL 72s DaVinci cut; user
  fine-tunes in DaVinci's Subtitles page.
- **Phase 4 (user, DaVinci):** concat clips + cards (cards OVERLAP clips, audio
  continues under cards) â†’ place dub audio (Jaisal on speaking shots, camera guy on
  cards) â†’ add natural SFX (NO music) â†’ burn subtitles â†’ export.

### Rules

- NO MUSIC (D041). User runs GPU jobs (I never stop Qwen, D051). Artifacts in
  `Jaisal-intro\` (never loose in ComfyUI output). Cards overlap clips + audio
  continues (audio continuity). Final = 72s.

---

## D098 â€” Dub inside DaVinci Resolve + camera guy MUTED (card = question) (2026-10-02)

Date: 2026-10-02
Status: Active (supersedes the camera-guy RVC plan in D097)

### Decision

1. **Dub inside DaVinci Resolve** (built-in voice-over recording) â€” NOT Audacity. The user
   records Jaisal's lines directly on the timeline while watching the video, so the lines
   are timed to the actual mouth movement. No going back and forth between apps.
2. **CAMERA GUY = MUTED (no voice).** The 4 black question cards ARE the questions (visual
   text only). The audio under each card = ambient / background noise or a Jaisal line (NOT
   the camera guy's voice). This eliminates the need for RVC `midhun_v2_40k` and the camera
   guy's 5 takes.
3. **6 takes total** (Jaisal only: A, C, E, F1, F2, G) â€” down from 11.
4. **Lip-sync:** only if the mouth is clearly off. The user times the dub to the existing
   mouth inside DaVinci; if close enough, skip LatentSync and just use the dub audio. If a
   shot's mouth is off, export that shot's dub audio (WAV) â†’ LatentSync â†’ re-import.

### Reason

- Dubbing inside DaVinci = perfect timing (watch the video, record at the playhead).
- Removing the camera guy's voice = a big simplification (no RVC, fewer takes, the card
  carries the question visually).
- The card is a video overlay on the continuing clip (audio continuity, per D097).

### Alternatives considered

- Audacity recording + import (rejected â€” going back and forth, harder to time against the
  video).
- Camera guy voiced off-screen + RVC Midhun (rejected â€” the user wants the card to be the
  question, no camera guy voice).

### Result

Dubbing script reduced to 6 Jaisal takes. RVC `midhun_v2_40k` no longer needed for the
intro. The card is a silent visual question with ambient / Jaisal audio underneath.

---

## D099 â€” H3 is text-to-voice only; LatentSync is the bridge for THIS intro; LTX-2 (audio-driven) for FUTURE movies (2026-10-02)

Date: 2026-10-02
Status: Active

### Decision

1. **MiniMax H3 audio = built-in TTS from the prompt's dialogue tags. It has NO audio
   input** â€” you cannot feed it a Malayalam dub and have it mimic. So "dub first â†’ feed to
   H3" is NOT possible. The mouth in the generated clips is from the English placeholder.
2. **THIS intro (video already done): LatentSync is the bridge.** Dub the 6 Jaisal lines
   (Malayalam) â†’ LatentSync re-animates the mouth on the 6 speaking shots (A, C, E, F1,
   F2, G) to match the dub â†’ swap audio. Do NOT regenerate the video.
3. **FUTURE movies: flip to DUB-FIRST with an AUDIO-DRIVEN model = LTX-2 (Lightricks).**
   LTX-2 is a DiT-based audio-video foundation model that generates video FROM audio
   (voice drives motion/pacing/mouth â€” "audio-to-video"). Dub first â†’ generate with LTX-2
   â†’ the mouth matches by construction, no LatentSync needed.
4. **Recording device:** of the user's options, **Nothing Earbuds (in-ear) = best** (mic in
   the ear canal, close to mouth, rejects room noise). Phone is acceptable. In DaVinci,
   MUTE the timeline audio while recording (watch the mouth for timing only; don't let the
   timeline sound bleed into the take), speak into the earbuds, import, nudge to align,
   then `clean_audio.py`.

### Reason

- H3's audio is generated, not input-driven â€” so the dub must be matched in post
  (LatentSync) for the already-generated intro.
- LTX-2's audio-driven generation is the cleaner forward pipeline (dub-first, mouth
  matches by construction).

### Alternatives considered

- Regenerate the intro video with the Malayalam dub (rejected â€” H3 can't take audio input;
  and the video is already done + upscaled).
- Phone recording (acceptable but more room noise than the in-ear earbuds).

### Result

This intro: LatentSync bridge. Future movies: LTX-2 audio-driven, dub-first.

---

## D100 â€” TWO-VERSION strategy (English = MiniMax native, Malayalam = dub + LatentSync) + ADR recording workflow (2026-10-02)

Date: 2026-10-02
Status: Active

### Decision

1. **TWO versions from ONE video:**
   - **ENGLISH version:** use MiniMax H3's **native audio as-is**. The same model generated every line â†’ the voice is **consistent across all shots automatically** (no dub, no LatentSync). The mouth is already correct (it IS the English mouth). Camera guy muted (cards = questions).
   - **MALAYALAM version:** the user's **dub** + **LatentSync** (re-animates the mouth to the dub) + **English subtitles** (for the audience).
   - One video â†’ two deliverables. The English version is basically free (already in the clips).
2. **Recording workflow (ADR-style, simplified for solo):**
   - Production standard = **ADR (Automated Dialogue Replacement)**: actor watches the picture on ONE monitor, records into a mic, the **DAW** (Reaper/Pro Tools/Audacity) is on the SECOND monitor. Engineer times it.
   - **Solo simplification:** since LatentSync re-animates the mouth to match the dub, the dub does **NOT** need to be frame-synced during recording. Record each line **cleanly** at a natural pace, place it at the right spot in DaVinci, LatentSync makes the mouth match. The two-monitor dance is OPTIONAL.
   - **Best phone app:** **Dolby On** (free, iOS+Android, built-in AI noise reduction, "voice" mode) or **Riverside** (pro, records locally at 48 kHz, noise suppression). Avoid built-in Voice Memos (no noise reduction). `clean_audio.py` denoises + normalizes afterward.
3. **Repeatable for future films:** record clean lines â†’ place in editor â†’ English = native audio, Malayalam = dub + LatentSync + subs.

### Reason

- MiniMax's native audio is consistent across shots (same model) â†’ the English version needs no dub.
- LatentSync decouples the dub from the mouth â†’ the recording doesn't need frame-sync, which is what makes the workflow scale to a full feature film.

### Alternatives considered

- Frame-synced recording (two-monitor ADR) â€” works but unnecessary, since LatentSync re-animates the mouth.
- Regenerating the video for the Malayalam version â€” rejected (H3 can't take audio input; the video is already done + upscaled).

### Result

Two versions from one video. English = free (native audio). Malayalam = dub + LatentSync + English subs. Recording = clean standalone lines (Dolby On / Riverside), no frame-sync needed.

### Update 2026-10-02 â€” G Malayalam re-run TEST FAILED (inconsistent)

User asked whether MiniMax could generate the Malayalam dialogue natively (re-run G with the
Malayalam prompt). The re-run (`jaisal_intro_G_papers_00009_.mp4`) came out **inconsistent
with the locked clips** ("THIS WAS SO BAD, NOTHING WORKS, THE SHOTS ARE NOT CONSISTENT").
**Root cause:** re-running a shot is a brand-new stochastic generation â€” it cannot match the
locked 7 clips (character/objects/timing/style). **Confirmed decision:** the VIDEO STAYS
LOCKED (the 8 locked clips are the asset; the `00009` test take is discarded). Malayalam
audio = DUB + LatentSync (post), NOT a MiniMax re-run. The English version keeps MiniMax
native audio (consistent, already done).

### Update 2026-10-02 (v3) â€” MiniMax Malayalam TTS = UNRELIABLE (gibberish on long lines) â†’ dub + LatentSync confirmed

User: "THE FINALIZED TAKE HAS GIBBERISH SPEAKING IN MALAYALAM AFTER KATHAKAL, RASHTREEYA." **VERDICT:** MiniMax H3's native Malayalam audio is clean for the first ~2 words ("à´•à´¥à´•àµ¾, à´°à´¾à´·àµà´Ÿàµà´°àµ€à´¯à´‚") then **gibberish** on the long line. **MiniMax Malayalam TTS is UNRELIABLE for long lines.** **CONFIRMED DECISION:** the Malayalam version = **user's dub + LatentSync** (the only reliable path â€” clean Malayalam from the user's voice, LatentSync re-animates the mouth). The English version keeps MiniMax native audio (English is clean). **LESSON (agent error):** I assumed the finalized take's audio was clean Malayalam without ever hearing it â€” the user knows the output, the agent does not. **Never assume audio quality; the user's ears are the ground truth.**

### Update 2026-10-02 (v2) â€” CORRECTION: re-running is FINE (fresh-take workflow); the test was a bad seed

User pushback: "we had done this before, why are you saying this is not possible? just the dialogue
alone has to be different, we have latent, refs etc." **USER IS RIGHT.** "Can't reproduce the exact
take" is NOT a blocker â€” the project has ALWAYS worked with fresh takes (the whole Aâ†’G chain was
built this way; the original G was a fresh take too). The `00009` test was probably just a BAD
SEED (a bad roll). **THE FIX: run multiple seeds (3-5), pick the best** â€” the established workflow.
**G is the last shot (nothing downstream) â†’ safe to re-run freely.** **PLAN:** re-run G, 3-5 seeds,
pick the best, judge the Malayalam audio. If good â†’ use it, then re-run the other shots (A, C, E,
F1, F2) with Malayalam dialogue. If bad â†’ fall back to dub + LatentSync. **SEED RULE:** record the
seed of every good take (fix the `RandomNoise` node to a fixed seed, or note the seed from the run
log) so a good take can be reproduced.

### Update 2026-10-02 â€” CORRECTED diagnosis: setup WAS identical; the seed is the only variable

User pushed back: "we have latent input, so at least the setup should be the same." **VERIFIED
CORRECT.** The G workflow's setup is identical across runs: `MiniMaxH3MotionContextLoadLatent`
clip_index=7 (F2's tail) + 5 refs + the Malayalam prompt + SLA. The ONLY variable = the
**`RandomNoise` node (node 129) set to `randomize`** (seed `125001602048036`) feeding
`SamplerCustomAdvanced` â†’ every run gets a fresh random seed. The latent + refs anchor the
start/end/objects/motion-continuity, but the MIDDLE of the shot is a fresh stochastic
generation. **The original G seed was NOT recorded â†’ the exact original take CANNOT be
reproduced.** **STANDING RULE: record the seed of every good take** (set the RandomNoise node
to a fixed seed, or note the seed from the run log) so a good take can be reproduced exactly.
The locked clips are the only copies of their takes.

---

## D101 â€” VOICESTUDIO DUB HACK: user records per-dialogue audio â†’ VoiceStudio â†’ LatentSync (2026-10-03)

Date: 2026-10-03
Status: Active (supersedes the "record clean standalone lines in DaVinci" plan in D098/D100 for the Malayalam dub)

### Decision

1. **User records rough audio for EACH dialogue** (own voice, any app â€” Dolby On / phone /
   DaVinci voice-over) â†’ drops files in `Jaisal-intro\dubs\` (naming: `A_jaisal.wav`,
   `C_jaisal.wav`, `E_jaisal.wav`, `F1_jaisal.wav`, `F2_jaisal.wav`, `G_jaisal.wav`,
   optional `B/D/F/G_camguy.wav`).
2. **VoiceStudio processes each take** (backend `localhost:3900`, OpenAI-compatible API
   `/v1/audio/speech`, JAISAL clone = `dd8bc71f` Malayalam, midhun = `094d6afe`):
   - **Default = CLEAN-AS-IS** â€” denoise + normalize the user's take, keep THEIR delivery
     (most natural, preserves performance).
   - **A/B option = Convert / re-speak** â€” Whisper transcribes the take â†’ TTS re-speaks it
     in the JAISAL clone (very clean + consistent, but flatter â€” loses exact delivery).
3. **LatentSync** (WSL2 Ubuntu-22.04) mouth-syncs the processed audio on the 6 speaking
   shots (A, C, E, F1, F2, G).
4. **WHY:** removes the "record perfectly timed lines" hassle â€” the user just records each
   line roughly; VoiceStudio cleans it and LatentSync makes the mouth match. The recording
   does NOT need frame-sync (LatentSync re-animates the mouth).

### Environment fixes (2026-10-03)

- **VoiceStudio venv was BROKEN** â€” created on Python 3.13.6, where `curated-tokenizers`
  v0.0.9 (transitive dep of KittenTTS) has no cp313 wheel â†’ `uv sync` fell back to a source
  build that hit a Cython 3.x bug (`'NoneType' object is unsliceable`) â†’ venv left EMPTY
  (0 site-packages) â†’ backend never started. **FIX:** deleted the venv, rebuilt on
  **Python 3.12.11** (has prebuilt wheels), `uv sync` exit 0 (304 packages). Backend now UP.
- **Ubuntu-22.04 installed** (user ran `wsl --install -d Ubuntu-22.04`, provisioned, user
  account `user` created). WSL2 = 2.7.13.0. LatentSync ready after repo clone + model
  download inside Ubuntu.

### Alternatives considered

- Record clean standalone lines in DaVinci (D098/D100) â€” rejected for the Malayalam dub:
  the user prefers to record rough per-dialogue takes and let VoiceStudio clean them.
- MiniMax native Malayalam (D100) â€” rejected: gibberish on long lines.

### Result

Malayalam dub = user's rough per-dialogue recordings â†’ VoiceStudio (clean-as-is default) â†’
LatentSync mouth-sync. English version still = MiniMax native audio (unchanged).

---

## D102 â€” VS Code 1.140 Agent Host breaks local-Qwen chat: 128-tool cap â†’ disable built-in GitHub MCP (2026-10-04)

### Decision

Keep the built-in **GitHub MCP server DISABLED** for local-model agent sessions
(`githubMcpServerEnabled: false` in `agent-host-config.json` / the matching VS Code
setting). Do NOT re-enable it while the local Qwen endpoint is the active chat model.

### Why

- VS Code **1.140.0** (installed 2026-09-30, active after restart) switched the default
  chat to the new **Agent Host** (native process; state in `~/.copilot/`).
- The Agent Host sends **ALL** connected MCP tools + built-in tools in one request:
  comfy-mcp (~39) + web-search gateway (~3) + built-in **GitHub MCP** (~40-60) +
  VS Code built-ins. That total **exceeds 128**.
- llama.cpp **b9616** has a **hard 128-tools-per-request cap** with **no
  `--max-tools` flag** in this build â†’ every request to the local endpoint is rejected:
  `{"message":"Cannot have more than 128 tools per request.","type":"api_error"}`.
  (Verified in `~/.copilot/session-state/*/events.jsonl`.)
- Disabling GitHub MCP (not needed for a ComfyUI project) drops the count under 128.

### Alternatives

- Upgrade llama.cpp to a build with `--max-tools` (b9616 lacks the flag).
- Remove the web-search gateway (`mcp.json`) â€” smaller win (only ~3 tools).
- Switch the agent chat to a cloud model (user wants local Qwen).

### Result

`githubMcpServerEnabled: false` applied in
`C:\Users\user\AppData\Roaming\Code\User\globalStorage\agent-host-config.json`
(JSON validated). Requires a **full VS Code restart** (the Agent Host is a separate
process). If VS Code regenerates that file, set the same key to `false` via the VS Code
Settings UI (search "GitHub MCP") and restart again.

### Status

Active

### Update (2026-10-04, second breakage + fix that sticks)

The 09:02 VS Code restart **regenerated `agent-host-config.json` and flipped
`githubMcpServerEnabled` back to `true`** (file mtime 09:02:14 = startup) â†’
the built-in remote `github-mcp-server` (GitHub-hosted, large tool catalog)
came back â†’ tool count > 128 again â†’ 502 on every request. Verified from
`~/.copilot/logs/process-*.log`: the CLI connected 3 MCP servers â€”
`mcp-gateway` (web-search, 4 tools), `comfy-mcp` (39 tools), and the remote
`github-mcp-server` (the culprit). Also verified: **llama.cpp has NO 128-tool
limit** (string absent from `D:\llama\llama-server.exe`, build 10831) â€” the
limit is enforced by the Copilot side of the request path.

**Fix applied (two layers):**
1. `githubMcpServerEnabled: false` set directly in
   `C:\Users\user\AppData\Roaming\Code\User\globalStorage\agent-host-config.json`
   (this IS the agent host's root config resource â€” `agentHostMain.js`
   `rootConfigResource`; JSON validated).
2. **Shadow-stub**: added a zero-tool stdio MCP server named exactly
   `github-mcp-server` to `D:\models\vsCodeMcp\.vscode\mcp.json`
   (`node D:\models\vsCodeMcp\utilities\mcp-stub.js`). The agent host
   (`_hasConfiguredGitHubMcpServer` in `agentHostMain.js`) skips the built-in
   remote server when a user-configured server with the same name exists â€” so
   even if the config flag is regenerated back to `true`, the built-in cannot
   re-appear. The stub answers the MCP handshake and reports `tools: []`.
   Tested: handshake + `tools/list` verified with a live node test.

**Wrong keys (do NOT rely on these):** `agentHost.config.githubMcpServerEnabled`
in VS Code `settings.json` is NOT a real VS Code 1.140 setting (string absent
from all VS Code JS) â€” it is silently ignored. The VS Code setting
`github.copilot.chat.virtualTools.threshold` was also added (defense in depth;
groups tools into virtual directories) but alone did not fix it.

**Persistence rule:** after any VS Code update/restart that regenerates
`agent-host-config.json`, re-check the `githubMcpServerEnabled` key (search
"GitHub MCP" in VS Code Settings UI is the persistent way). The stub in
`mcp.json` is the durable layer â€” it survives config regeneration.

**Also (from the earlier note, confirmed):** the same 1.140 Agent Host does
NOT load legacy `.github/prompts/*.prompt.md` files â†’ `/resume-project` and
other slash prompts are gone for Agent Host sessions. Forward path = agent
skills / custom agents.

### Note (related)

The same 1.140 Agent Host **does NOT load** legacy `.github/prompts/*.prompt.md`
prompt files (deprecated for Agent Host sessions; they still work with the old Local
agent). That is why `/resume-project` and the other slash prompts stopped appearing.
Forward path = **agent skills** (`SKILL.md`) / custom agents, or VS Code's
"prompt file migration" (experimental, enabled by default). The 5 prompt files in
`.github/prompts/` are left as-is as the migration source.

### Update (2026-10-04, 09:45 — slash prompts MIGRATED + config flag re-applied)

1. **Slash prompts migrated to custom agents.** All 5 legacy prompts now have
   custom-agent equivalents in `.github/agents/` (frontmatter `name` +
   `description`, body = original prompt text): `resume-project.md`,
   `debug-workflow.md`, `optimize-workflow.md`, `save-decision.md`,
   `save-session.md`. The original `.github/prompts/*.prompt.md` files are
   left in place as the migration source. Custom agents are picked up by the
   Agent Host (they appear in the agent picker / can be invoked by name).
2. **Config flag regenerated AGAIN** (file mtime 09:21:11 = VS Code startup)
   → `githubMcpServerEnabled` flipped back to `true` → re-applied `false`
   directly in `agent-host-config.json` (verified `False` after write).
   The shadow-stub in `.vscode/mcp.json` (`github-mcp-server` →
   `utilities\mcp-stub.js`, zero tools) is still in place as the durable
   layer — even with the flag `true`, the built-in remote GitHub MCP is
   shadowed by the stub, so the tool count stays under the 128 cap.
3. **MCP verified working** (09:30): `comfy-mcp server_info` returned
   ComfyUI running at `127.0.0.1:8188`, comfy-cli 1.18.0, RTX 5090,
   workspace `C:\Users\user\Documents\comfy\ComfyUI` (note: comfy-cli's
   default workspace is NOT the portable install — runs target the
   Documents workspace unless `COMFYUI_URL`/workspace is pinned).
4. **User action (pending at session end):** FULL VS Code restart required
   (Agent Host is a separate process; the config-flag write + new
   `.github/agents/` files only take effect after restart). After restart:
   (a) the 5 commands should appear as **custom agents** (invoke by name,
   e.g. "resume-project" — NOT as `/resume-project` slash prompts);
   (b) if local-Qwen chat still fails with a tool-count error, the
   shadow-stub should have caught it — dig into `~/.copilot/logs/` and
   `~/.copilot/session-state/*/events.jsonl`.
5. **Per-chat session rule (user-confirmed 2026-10-04):** the chat session
   is PER-CHAT (temporary) — anything a future session needs to know MUST
   live in `project-memory/` (DECISIONS.md / PROJECT_STATE.md /
   CURRENT_TASK.md), never only in chat. When a fix is applied mid-session,
   record it in the decision details in the SAME turn so a fresh chat can
   resume without re-explaining.
## D103 â€” Runaway tool-loop in ghcp agent (local Qwen) + stop mechanism (2026-10-04)

**Symptom:** one question in ghcp (Copilot Agent Host + local Qwen 27B NVFP4,
thinking OFF) â†’ model kept emitting tool calls instead of a final answer â†’
GPU spinning 5+ min. A steer ("stop") message sent mid-turn never took effect.

**Why the steer didn't stop it:** steer messages are **queued behind the active
turn** â€” they are only processed after the turn completes. While the model is
in a tool loop the turn never completes, so the stop instruction never runs.
Steering â‰  aborting. (Verified in SDK: `steer` is queued; `abort`/`interrupt`
are the in-turn mechanisms.)

**Why the loop is unbounded:** (1) the model (thinking-off Qwen) keeps
preferring tool calls over a final answer; the CLI feeds tool results back and
re-dispatches. (2) The 1.140 CLI has **NO iteration/turn/tool-call cap**
(config has only `maxAiCredits`). (3) `Qwen3.827BMTP.bat` had **no `-n`
(max tokens per request)** â†’ llama.cpp could generate until EOS/context limit.
`--parallel 1` = one stuck request holds the whole server.

**Fix (3 layers):**
1. **Reliable stop (immediate):** UI **Stop button / Esc** sends the
   abort/interrupt (cancels the in-flight request). If that fails:
   `Stop-Process -Name copilot-runtime -Force` (VS Code respawns the agent
   host; session state is on disk in `~/.copilot/session-state`, so
   `/resume` still works). Nuclear: **Ctrl+C in the llama-server CMD window**
   aborts the current generation directly.
2. **Server-side bound:** `-n 8192` added to `D:\models\qwen\Qwen3.827BMTP.bat`
   (applies on next llama-server restart) â€” no single generation exceeds 8k
   tokens, so a runaway loop is forced to terminate and the CLI gets a bounded
   (possibly truncated) response instead of an infinite spin.
3. **Loop likelihood:** keep ghcp prompts short/single-tool (local models
   degrade on long agentic chains); if loops persist, test a llama-server
   instance WITHOUT `--spec-type draft-mtp` for the CLI session (MTP spec
   decoding in tool-call JSON is a prime suspect for malformed tool blocks).

**Rule:** to STOP a runaway agent turn use abort (Stop/Esc, or kill
`copilot-runtime`), never a steer message. Keep `-n` on the llama-server for
any agent use.

