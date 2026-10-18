# PRODUCTION CONSISTENCY PLAN — the Jaisal movie (2026-10-08)

> The user's core concern: this is a BIG movie — many locations, characters,
> costumes. "As a normal guy we have an idea of how to make a movie" — capture
> ALL the details so nothing is missed. This file is the consistency bible.

## The 3-layer consistency stack (LOCKED-IN order)

### Layer 1 — CHARACTER IDENTITY (the face + body)
1. **Base character image** = Krea 2 + realism LoRA (V2 `r3alism` @1.5-2.0,
   RawGirl v3 @1.2, or FameGrid `Famegrid` @0.5) → super-natural, non-plastic
   boy. This is the MASTER reference.
2. **Character sheet** = multi-angle / multi-expression / multi-outfit reference
   set. Options (all available locally):
   - `2BZ_H3_character_sheet_2stage_v1_EN.json` (H3, semantic refs — already saved)
   - `QWEN_click_multiple_character_angles-v1.0.json` (Qwen 2.1 — already saved)
   - **Krea 2 identity-edit chain** (krea2_identity_edit.json) — BEST for
     natural look: generate base with t2i, then identity-edit each angle
     (front/side/back/3-4, expressions, outfits) keeping the same face.
   - **Decision: generate the character sheet WITH Krea 2** (identity-edit per
     angle) so the sheet is as natural as the base image → MiniMax H3 then
     animates from a natural sheet. (User's call, 2026-10-08.)
3. **Character LoRA** (the lock) — train a Krea 2 LoRA on ~20 character images
   (the sheet + variants) so the character is reusable WITHOUT re-deriving the
   face every shot. Trainer = **ai-toolkit** (ostris) — NOT yet installed
   (checked 2026-10-08: no `ai-toolkit` in python_embeded, no dir). Install
   into a venv, train on Krea 2 base. This is the production-grade answer to
   "reuse without hassling."

### Layer 2 — LOCATION / ENVIRONMENT
- **Lock ONE primary location** (the user may need to). Generate a LOCATION
  MASTER reference (Krea 2 t2i, natural look) and reuse it as the scene ref
  (node 113 in identity-edit) for every shot in that location.
- Keep the climate consistent (D024): once rain starts, ONE moody tone across
  all rain/water shots. Bridge handrails SQUARE, river OPEN (not canal).
- Each location = one master image + a short written description (lighting,
  time of day, weather) stored in this file.

### Layer 3 — COSTUME / PROPS
- **Costume lock (D137, 2026-10-18 re-scope)**: char1 (Jaisal) = plain black
  t-shirt, slim build, wavy black hair; char2 (Zidhan) = plain white t-shirt,
  black hair in a loose top bun. Face references: `krea2_char{1,2}_face_{a,b,c}_*.png`
  in ComfyUI output (2026-10-08 set). (OLD D022 schoolboy costume deprecated.)
  Do NOT change wardrobe between shots unless the story demands it.
- **Props**: mic, papers, etc. — each prop gets a reference image if it
  appears in multiple shots.
- Rule: one clear reference OWNS identity; wardrobe/environment refs have
  narrower roles (MiniMax consistency guide).

## MiniMax H3 consistency (video layer)
- **One primary identity reference** per shot; other refs = narrower roles.
- **RefMods** (zero-training reference adapters, malcolmrey /
  ComfyUI-MiniMaxH3Mod): encode a reference ONCE into a ~1-1.6 MB .safetensors
  and load it like a LoRA — no live VAE encode per run, no `<Picture N>`
  bleeding. Weights library on HF `malcolmrey/minimaxh3`. Files go in
  `ComfyUI/models/refmods/`. **Candidate for locking the character across
  shots without re-feeding images.** (Not yet installed.)
- **Fizgig H3 Still nodes** (shootthesound/ComfyUI-Fizgig-H3-Still) —
  **INSTALLED 2026-10-08** (cloned into custom_nodes). `FizgigH3StillLatent` +
  `FizgigH3StillDecode` render TRUE single-frame stills from H3 (crisp, no
  banding, best from 3 MP up, 8 MP = 3872×2176, no Turbo LoRA, 50 steps,
  er_sde). Example workflows in the pack: `h3_still_text_to_image.json`,
  `h3_still_text_to_image-8MP-NoTurboVersion.json`, `Edit_Workflow_example.json`.
  H3 models all present (fl2va/ref2va pruned int8, video VAE fp16/int8,
  qwen3vl_32b nvfp4_awq).
- **Character sheet folder**: `user\default\workflows\character sheet\`
  (created 2026-10-08) — user places the character-sheet workflow there.

## LoRA training (ai-toolkit) — the reuse answer
- **YES, train a character LoRA** if Krea 2 realism is good enough. ~20
  diverse images (angles, expressions, outfits, lighting) → train on Krea 2
  base → reuse the character across the whole movie without re-deriving.
- Dataset: use the 1-click dataset workflow (Klein 9b) pattern, or hand-curate
  from the Krea 2 character sheet.
- Trigger word: pick one (e.g. `jaisalboy`) and prefix every prompt.
- Strength: start 0.6-0.8, tune.
- **This is the production-grade consistency lock** — cheaper and more
  consistent than re-feeding references every shot.

## Production checklist (don't miss these)
- [ ] MASTER character image (Krea 2 + realism LoRA) — natural, non-plastic
- [ ] Character sheet (Krea 2 identity-edit per angle) — front/side/back/3-4,
      expressions, outfits
- [ ] Character LoRA (ai-toolkit, ~20 images) — the reuse lock
- [ ] LOCATION master(s) — lock ONE primary location + climate
- [ ] COSTUME reference — rose shirt / black trousers / black bag
- [ ] PROP references (mic, papers)
- [ ] RefMods for H3 (optional, zero-training) — encode character once
- [ ] Consistency rules: one ref owns identity, wardrobe/env refs narrower,
      don't change wardrobe+age+lighting+camera at once
- [ ] Climate continuity (D024) — one moody tone for rain/water shots

## Sources (2026-10-08)
- Fizgig H3 Still: github.com/shootthesound/ComfyUI-Fizgig-H3-Still (INSTALLED)
- MiniMax H3 REF + Fizgig SOTA ref2img: reddit r/StableDiffusion 1wsb4h3
- Character sheet Qwen 2.1: reddit r/comfyui 1wsee1y (workflow already saved)
- MiniMax H3 consistent character: reddit r/comfyui 1wxixua
- RefMods: comfyui-wiki.com 2026-09-07 (malcolmrey / ComfyUI-MiniMaxH3Mod)
- civitai.red/posts/31291351 (403 — user to open manually)
