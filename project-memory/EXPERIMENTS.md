# Experiments

Newest experiments first.

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
