# Pipeline guide — techniques that make it work

This is the hard-won prompting/wiring knowledge behind Story-Short. Read it once;
it's shorter than a week of trial and error.

## Stage 1 — Character sheet (Krea2 t2i)

- UNet `krea2_turbo_fp8_scaled`, CLIP `qwen3vl_4b_fp8_scaled` (type **krea2**),
  VAE `qwen_image_vae`. Turbo base: **10 steps, cfg 1, euler/simple**.
- Krea2 t2i gives a *different face every run*. That's fine here — pick the best
  sheet; the next stage locks it.
- Krea2 quirks to prompt around:
  - it tends to **duplicate the character** → always say "ONLY ONE character,
    no other people, no duplicates".
  - it cannot make a faceless character — a normal face is the way.
  - keep the costume description exact and repeated (e.g. char1 = "wavy black
    hair, slim build, plain black t-shirt"; char2 = "black hair in a loose top
    bun, slim build, plain white t-shirt" — see D137).
- Natural-language prompts work best; natural skin texture, no "AI look" in the
  negative prompt.

## Stage 2 — Identity reference set (Krea2 identity-edit)

This is the core trick: **lock the face at the image stage, before video.**

- Workflow: `krea2_identity_edit.json` (Krea2 Identity Edit v1.2).
- Load your best sheet image in the LoadImage node; write a plain-English scene
  instruction; the workflow regenerates the scene keeping the same face/body.
- **`ref_boost` = 4.0** is the fidelity dial: >10 over-copies the reference
  (composition gets pinned), <1 suppresses it.
- KSampler 10 steps, cfg 1 (turbo).
- **Lighting match:** the workflow carries the reference image's color tone into
  the output. A bright neutral sheet makes moody scenes come out studio-lit.
  Fix: keep the lighting words in the instruction ("moody overcast light") and,
  once you have one in-scene reference, use *that* as the reference for later
  scenes — the tone matches automatically.
- Build a set of 4–8 references: frontal close-up, 3/4 view, profile, back view,
  and 2–3 in-scene references (the scenes your shots will use).

## Stage 3 — H3 R2V shots (2-anchor technique)

H3 is a general video model: its prior smooths toward its own default look, so
style drifts in over 15 s. The fix is **anchors, not essays**:

- **2 reference images per shot, max 3.** Map each reference 1-to-1 to a shot:
  `ref_image_0` = first frame of Shot 1 → `<Picture 1>`;
  `ref_image_1` = first frame of Shot 2 → `<Picture 2>`.
- A 5-anchor storyboard with a 500-word prompt performs *worse* than 2 anchors
  with a short prompt — the model animates between clear anchors far better.
- If the character isn't doing the action, add a 3rd reference showing that pose,
  or strengthen the motion verb.

### Prompt structure (per shot)

```
[Shot N] <Picture X> — [angle + framing], the character [concrete action],
[camera move], [lighting], [1–2 sound details].
```

Example:

```
[Shot 1] <Picture 1> — low-angle medium shot from the bridge deck, the boy
stands left of frame looking at the water, slow push-in, moody overcast light,
rain on the stone, distant water lapping.

[Shot 2] <Picture 2> — wide shot across the river, the boy walks along the
bridge from left to right, static camera, grey light, rain continuing.
```

### Audio (natural soundscapes only)

Describe only **natural sounds**: footsteps, wind, water, rain, ambient. No score,
no instruments, no beat — H3 models sound naturally when you don't ask it to
improvise a soundtrack. Dialogue can be added as quoted lines in the prompt.

### Climate continuity

Do not change the climate dramatically between shots. Once rain starts, keep ONE
moody tone across all rain/water shots. A drastic light change breaks continuity
and H3 won't bridge it.

## Assembly

```
ffmpeg -f concat -safe 0 -i shots.txt -c copy film.mp4
```

(`shots.txt` = one path per shot file. Re-encode with `-c:v libx264 -crf 18`
if the shots have different codecs.)

## Node packs

| Pack | Provides |
|---|---|
| core ComfyUI | H3 nodes (`MiniMaxH3ReferenceToVideo` etc.), Krea2Edit nodes (`Krea2EditGroundedEncode`, `Krea2EditModelPatch`) |
| [ComfyUI-H3-Multishot / H3-NativeAudioLock](https://github.com/Comfy-Org/ComfyUI) | H3 multishot / audio-lock nodes (merged into core) |
| [H3-Optimizations](https://github.com/Zironic/H3-Optimizations) | `H3SLAAttention` (Sparse Linear Attention — keeps 1MP H3 under ~4 min on a 5090) |
| [ComfyUI-H3-Motion-Context](https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context) | `MiniMaxH3MotionContext*` (shot-to-shot motion continuity) |
| [comfyui-rgthree](https://github.com/rigglestudio/comfyui-rgthree) | Image Comparer (side-by-side A/B in workflow 02) |
