# MiniMax H3 — Micro-Expression Reference (tweet @EndFolding79421, 2026-11-23)

**Source:** https://x.com/EndFolding79421/status/2124619802757202007 ("FoldingEnd A.I.")
Prompt by @GrayNoteLab, timing adjusted to a 12-second clip, run through **MiniMax H3 in ComfyUI** — the user's own video stack.

## What it tests
How well H3 handles **subtle facial expressions, restrained emotions, small changes without exaggerated movements** — facial realism, emotional progression, cinematic consistency.

## The prompt's structure (the part worth stealing)

```
【Global Setup】(global setup)
  Photorealistic live-action, cinematic look, 16:9. Outdoor snowy setting.
  ONLY female lead A appears throughout the entire film.
  Theme = subtle emotion of holding back tears:
    no sobbing, no flood of tears ANYWHERE in the film.
    Emotion released ONLY through extreme close-ups of eyes/lips + hand clenching clothing.
  Audio: NO background music, NO singing — ambient only:
    cold wind, faint falling snow, suppressed breathing, fabric-clench rustle.

【Character Lock】(character lock)
  Female lead A: Image 1          ← the R2V reference-image tag (= our <Picture 1>)

【Continuity Lock】(continuity lock)   ← THE NEW SECTION
  Hair blown to her right, brushing her cheek; snow keeps falling throughout.
  Tear STATE PROGRESSES SHOT BY SHOT:
    shot 01 welling but not falling → 02 welling + fluttering lashes
    → 03 lips pressed tight → 04 eyes closed, bitter smile collapses
    → 05 hand clenching fabric → 06 SINGLE tear slides down
    → 07 calms down.
  "Only this one tear is allowed to slide down in the entire film;
   no flood of tears is permitted."   ← single-permitted-event constraint

【Shot Breakdown】(shot breakdown)
  Shot 01 【0.0–1.2s】 Duration 1.2 s
    【Camera Movement】 Fixed camera, completely still.
    【Image】 close-up face, looks front-left, eyes glistening, lips slightly
    parted, breathing trembles faintly, wind strands across face, snow in hair.
  Shot 02 【1.2–3.0s】 … extreme close-up right eye, tears well along lower
    eyelid, pupil trembles, gaze shifts upper-left, lashes flutter,
    snowflakes cling to lashes. No tears fall.
  Shot 03 【3.0–4.4s】 … extreme close-up lips (only below nose + chin framed),
    pressed tight, trembling, part for one restrained breath, chin quivers
    almost imperceptibly.
  Shot 04 【4.4–6.4s】 … close-up matching Shot 01, slowly closes eyes,
    faintest bitter smile, smile collapses almost immediately, reopens eyes
    red and brimming but none fall.
  Shot 05 【6.4–7.8s】 … close-up hand clutching clothing against chest,
    fingers tighten, knuckles pale, fabric gathers deep folds, snow settles.
  Shot 06 【7.8–10.4s】 … (the one tear)
```

## Techniques to adopt (map to our film)

1. **Continuity Lock section** (between character lock and shot list): a
   *per-shot state machine* for one evolving property (tear state, lighting,
   costume wear) + a **single-permitted-event constraint** ("only this one
   tear… no flood permitted"). Our R2V guide has `retention_analysis`
   (per-label preserved/drifted) — this is the *progression* variant:
   property X goes `state_a → state_b → state_c` across shots, with exactly
   one allowed release point. **Best fit for Ep1: the mourning/grave scenes
   (env L04 grave pit, bandicoot marker) — restrained grief is exactly this
   discipline.**
2. **Global theme sentence with double negatives**: "no sobbing, no flood of
   tears anywhere… ONLY through [these specific channels]" — states the
   emotional ceiling AND the permitted release channels in one line.
3. **Fixed camera for emotional close-ups**: every shot "completely still" —
   the test isolates the FACE, so zero camera motion (our pan/zoom camera
   strategy is for world shots; for grief close-ups, fixed is the pattern).
4. **Ambient-only audio spelled out per-source** (wind / snow / breathing /
   fabric) — identical shape to our D041 `non_diegetic_music` block; the
   author's prompt is D041-compliant by design.
5. **Extreme close-up framing vocabulary**: "framing only the area below her
   nose and her chin", "right eye with left blurred behind the bridge of the
   nose" — frame-bounding phrasing (not just "close-up").
6. **Per-shot duration budgeting**: every shot carries 【start–end s】 +
   explicit Duration — 12 s total across 7 shots; matches our guide's
   `[Shot N] At MM:SS.mmm` timed blocks.
7. **"matching Shot 01" cross-referencing** (Shot 04) — reuse a prior shot's
   framing explicitly instead of re-describing.

## Caveats
- 12 s total = short test clip; our H3 shots are 15 s — the per-shot
  durations here are ~1.2–2.6 s (7 shots) vs our typical 1–2 shots/15 s.
- Single character, single setting — the continuity lock is trivial at this
  scale; with multi-character scenes the same pattern must be per-character.
- The result video (how well H3 actually holds this) is the real data point —
  the prompt is the recipe, watch the clip before adopting wholesale.
