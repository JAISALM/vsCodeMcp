# Intro Video — Channel Intro ("Jaisal Cut")

Last Updated: 2026-09-08
Status: AWAITING SCRIPT (user is drafting)

## Goal

Channel-intro video for **Jaisal Cut**: a monologue about what the channel is
going to do. Natural face, close-up + medium shot, the user's own voice (dubbed,
converted via RVC).

## Pipeline (4 stages)

```
Stage 0: SCRIPT (user drafts — AWAITING)
   ↓
Stage 1: AUDIO — user dubs the line (headset, quiet room)
   → clean_audio.py (openvoice venv) → RVC convert (midhun_v2_40k or character model)
   → final voice track
   ↓
Stage 2: IMAGES — Krea2 (title card, character sheet, keyframes)
   → existing workflows: krea2_jaisal_title_moody.json, krea2_identity_edit.json (v1.2)
   → prompts: prompts/jaisal_ref_prompts.txt, jaisal_title_instruction.txt
   ↓
Stage 3: VIDEO — MiniMax H3
   → i2v from Krea2 keyframes (or R2V with 2-3 Krea2-styled refs — D021)
   → existing workflows: jaisal_single_shot (SLA stack, D042), R2V guide (docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md)
   ↓
Stage 4: ASSEMBLY — video editor (mux audio + video + title)
```

## Stage details

### Stage 0 — Script (AWAITING USER)
- User drafts the monologue (bilingual Malayalam + English OK).
- Once provided: break into shots (close-up / medium / wide), assign camera
  angles (docs/CAMERA_SHOT_VOCABULARY.md), time each shot.

### Stage 1 — Audio (RVC pipeline, D050)
- User dubs the line: headset, quiet room, natural pace.
- `clean_audio.py` (openvoice venv) → 16 kHz mono clean wav.
- RVC convert: `infer.cli --model <char>.pth --input <dub> --output <out> --f0-method rmvpe --protect 0.33 --index-rate 0.75`
- Current models: `midhun_v2_40k` (6.5 min data, best so far).
- **Known issue (2026-09-08):** RVC wording sounds "weird/quirky" on Jaisal
  sources — the user's own dub is the next test (removes the source-articulation
  mismatch). If still weak: `--index-rate 0.9`, more Midhun data (v3 retrain).
- Fallback: IndicF5 (Malayalam TTS, parked, working) if a line can't be dubbed.

### Stage 2 — Images (Krea2)
- Title card + character sheet + keyframes in the Krea2 angular brush-stroke style.
- Workflows: `krea2_jaisal_title_moody.json` (moody title), `krea2_identity_edit.json`
  (Identity Edit v1.2 — locks the face across shots, ref_boost 4.0, style LoRA
  `Krea2_Cinematic_Artstyle.safetensors` @ 0.7 wired as node 95).
- Character (D022): normal young schoolboy, short dark hair, rose-pink collared
  shirt, black trousers, black school bag. SINGLE character, no duplicates.
- Climate consistency (D024): ONE moody tone across all shots; square bridge
  handrails; open river.

### Stage 3 — Video (MiniMax H3)
- i2v from the best Krea2 keyframes, or R2V with 2-3 Krea2-styled refs (D021:
  build a Krea2-styled reference SET first so the style holds across the video).
- R2V rules (D017/D020): 2-3 refs max, each an explicit frame anchor for one
  shot, SHORT prompt, 6-section structure, `<Picture N>` tags in connection order.
- Speed stack: SLA (D042) — 1MP H3 under 240 s.
- **NO MUSIC (D041 HARD RULE):** natural sounds only (footsteps, wind, water,
  birds, ambient). `non_diegetic_music` = NO music statement.

### Stage 4 — Assembly
- Video editor: mux the RVC voice track + H3 video + title card.
- Upscale if needed: SeedVR2 TensorRT Studio (2K, ~8 min/8 s on the 5090).

## Rules that apply
- **NO MUSIC** (D041) — natural sounds only, all audio.
- **D045:** no heavy GPU jobs while Qwen is active (H3 generation = stop Qwen;
  RVC small jobs = OK to run alongside).
- **D051:** I never stop Qwen myself — user runs stop/restart commands.
- Character consistency: Krea2 Identity Edit v1.2 for face lock (D023).

## Status / Next
- [ ] **AWAITING: user's script** (they are drafting it now).
- [ ] Break script into shots + camera plan.
- [ ] User dubs the line → clean → RVC → listen.
- [ ] Krea2 keyframes (title + character).
- [ ] H3 video generation.
- [ ] Assembly + review.
