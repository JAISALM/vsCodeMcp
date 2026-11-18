# EPISODE 1 — FESTIVAL-REALISM PLAN (2026-11-18, agent-prepared, D230)

Goal: the Episode 1 film as a **festival-caliber AI short** — target the AI-film category
(AI Fest / AI sections of larger festivals: the medium is EXPECTED there, so the CRAFT is
what is judged). Disclose AI generation per festival rules.

## The honest read (why this is not "AI slop" material)

- **Rules, not vibes:** the script carries four hard rules — the anachronism rule (modern
  words translated by villagers), the three-color rule (B&W except T-shirts / fire / watch),
  the sound bible (no score; only world sounds; the anthem SONG), the watch rule (a tool of
  remembering, not a time machine). AI slop has none of these.
- **Local texture:** Azan, kaikkott, parambu, matchbox-label tickets (₹10), newspaper shin
  guards, rubber sandals, "SPRAY: 0", the commentator's cracked loudspeaker voice with the
  Malayalam original kept for dubbing. Slop is generic; this is Beypore.
- **A real historical skeleton:** India's 1950 World Cup is REAL (qualified by default;
  sailed; lost 4-0 to Sweden; anthem sung). The script's fact-vs-fiction section is careful
  about exactly what is invented. The invented parts (village, ship, cable fire) hang off
  real anchors — that is what gives a story "depth" instead of "content".
- **A prop throughline:** the watch chain (table slide → boy → Jaisal's fist → Grandpa's
  wrist) is craft.
- **The risk is the EXECUTION layer, not the writing.** The film will only read as "slop"
  if the AI tells show; the script's rules are all seam-hiding devices. The pipeline's job =
  hold the rules.

## Realism levers (in priority order)

1. **The 1950 B&W half is the SAFE half.** Black & white hides skin detail, material
   fidelity, texture smearing — the three loudest AI tells. The 2026 COLOR half is where
   tells show, so: 2026 shots stay handheld-CLOSE (the script's own camera rule: "close and
   sweaty"), photo-grade Klein/Krea2 stills for frames, H3 video with 2–3 ref sets (D021).
2. **The unit = the 5 s R2V clip (D020).** Generate short, cut often. The edit hides the
   seams; long takes expose them.
3. **Sound = 50% of perceived realism.** The sound bible is already excellent (no score —
   D041; Azan; the watch TICK as a sonic throughline; crowd claps; oars; coconut thuds; the
   anthem SONG). Add the P1 dub (user's own voice + the commentator's Malayalam line). A
   film whose SOUND is right reads as "film" faster than one whose pixels are right.
4. **Bake the grade per era** — 2026 = wet green / red mud / harsh noon white; 1950 =
   B&W + golden-hour bloom + vignette. The script's visual bible IS the grade spec; apply
   it as consistent LUTs/prompt prefixes so every shot of an era looks like the same film.
5. **The three color exceptions = compositing, not model hope.** T-shirt colour drain
   (Sc. 14–16), the golden fire (Sc. 13), the watch glint (Sc. 4/23/25): render the 1950
   half B&W, then selectively colorize in DaVinci (mask the T-shirts/fire/watch).
   Controllable, repeatable, exactly the script's rule.
6. **The 360° spin (Sc. 23) = the blockout pipeline's payoff shot.** The most
   AI-tell-prone shot in the film (violent camera move) gets a Blender 360° orbit camref →
   H3 R2V with the scoreboard still as frame anchor. The most-tested shot (multiple seeds).
7. **Faces-echo = lock the kid faces EARLY.** Batch 1 of the sheet batch = Adam + the
   starting five (Anto, Gopu, Babu, Ragu). The reveal ("faces we know from black and
   white") is the emotional payoff — it only works if the 2026 face and the 1950 echo are
   the SAME locked sheet.
8. **Crows are the loudest AI tell.** The Maracanã crowd (Sc. 17–23): keep the crowd in
   background/bokeh, shots tight on the two (Jaisal in the gallery, Zidhan on the sideline);
   the B&W half helps. Same for the village matches (S5/S1): crowd = a few painted
   backgrounds + sound, not a generated throng.
9. **Water is the hardest environment** (Sc. 12, 14–16): ship at sea = wide, SLOW cameras
   (a ship at anchor / a calm dawn), B&W, and the coconut-on-deck shots are TIGHT (deck +
   coconuts + hands — no horizon needed).
10. **Final frames via the SeedVR2 2K route (P6)** — 1 MP H3 output → clean 2K; the
    festival deliverable is a 2K master.

## Hard-shot risk list (what to test first, most-tell → least)

| Shot | Why it's risky | Mitigation |
|---|---|---|
| Sc. 23 the 360° spin | violent camera move = the loudest tell | Blender orbit camref + scoreboard anchor; test 5–10 seeds; cut on the spin (it's a 1–2 s beat) |
| Sc. 13 the post-office fire | fire + B&W + one color exception | short clip; the fire IS the golden exception; the lamp-turn is a 1 s slow-mo beat |
| Sc. 12/14–16 ship at sea | water + sail + motion | wide slow cameras, B&W, dawn; the coconut-deck shots are tight (no horizon) |
| Sc. 17–23 Maracanã | crowds = tell | tight two-shots, crowd in bokeh, B&W |
| The T-shirt colour drain (14–16) | per-scene gradient consistency | composite (lever 5), NOT model-driven |
| The faces-echo reveal (23) | identity continuity across eras | lever 7 (lock early); the reveal is a MATCH-CUT of the same sheet |

## Festival path (stages)

- **Stage 0 (this offline week):** lock the cast (sheet batch + lead LoRAs), the 7 new
  blockouts + S1/S5 set-dress (scoreboard, banners), the 6 camrefs. All local work.
- **Stage 1:** the 2026 half (scenes 1–6, 23-return, 25) — 5 s R2V clips, the dub, the
  2026 grade.
- **Stage 2:** the 1950 half (B&W + ship + Madras + Maracanã) + the color-exception
  compositing + the 360° spin test batch.
- **Stage 3:** DaVinci assembly (user) → 2K master (SeedVR2) → festival submission with AI
  disclosure.

## What makes the jury stay (the pitch line)

"A two-timeline Kerala football film: a man who quit and a coach who stayed, linked by a
watch and a 1950 mind-trip to the World Cup India sailed to and never told anyone about."
The rules (B&W, the sung anthem, the watch) are the craft statement; the 1950 truth is the
depth.
