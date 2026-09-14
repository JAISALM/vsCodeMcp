# JAISAL KUT — INTRO KEYFRAME REFERENCE PLAN (for MiniMax H3)

**Purpose:** these keyframes are **REFERENCE IMAGES** we feed to MiniMax H3 (i2v/R2V).
H3 animates BETWEEN them. So each image must be a clean, correct **end-state** that
H3 can start or end on. **Always check `docs/INTRO_SCRIPT.md`** — the images must
match the script's shots.

**Status (2026-09-13, V8 keyframe set built):**
- **HEAD-SET (Shot 3 twist) — ALL 4 DONE** (see D059):
  - `kf2_hands_table` = ✅ GOOD (hands flat on table, facing camera) — anchored on `kf2_00004_ref.png`.
  - `kf3a_headnormal` = ✅ GOOD (back view, head normal).
  - `kf3c_head90` = ✅ GOOD (back view, head ~90° side profile) — anchored on `kf3a_headnormal_v7`.
  - `kf3b_head180` = ✅ **SOLVED 2026-09-13** (`kf3b_head180_00010_.png` — back-view body + FRONTAL face = the 180° horror-ghost twist).
  - **Consolidated folder (ONE path): `d:\models\vsCodeMcp\Jaisal-intro\kf2_headset\`** (`kf2_hands_table.png`, `kf3a_headnormal.png`, `kf3c_head90.png`, `kf3b_head180_00010_.png`).
  - **Camera motion** (the 90°/180° camera turn) = the MiniMax H3 CAMERA NODE's job (`H3LocalCameraEditor`, **CONFIRMED INSTALLED + LIVE in the running ComfyUI 2026-09-13** — it compiles a 3D camera trajectory into H3 prompts and has NO LoRA input, so it works as-is; the optional `camera_motion_h3_lora` just improves fidelity).
- **V8 KEYFRAME SET (2026-09-13) — the 6 remaining keyframes BUILT + VALIDATED:** `utilities/build_intro_keyframes_v8.py` → `krea2_intro_kf{5a_stem,5_plants_grown,6_plants_dead,7a_page,7b_page_mic,7c_cricket}_v8.json` (all `valid: true`). Changes vs V7: **DARK CHARCOAL WALL** baked in, **ONE CHAIR** enforced, **PLANT "FLORISH → DULL"** (kf5 = alive/lush, kf6 = SAME plants now dead/dull). Run one-by-one; re-anchor node 72 to the previous good output for the later keyframes (kf5→kf5a, kf6→kf5, kf7b→kf7a, kf7c→kf7b).
- **CHARACTER = SOLVED.** V3/V7 settings (full char ref `intro_char_ref_bw.png`,
  **NO scene anchor**) give the correct face. Do NOT add a scene anchor (it breaks
  the character — D058).
- **SCENE = the remaining work.** Extra chairs, the wall, plant consistency.
- **DECISION (user, 2026-09-12): ACCEPT A WALL.** Stop forcing a pure-black void
  (it doesn't fit well and keeps coming out cream/white). Treat the room as having
  a wall. The wall tone is the fix (below).
- **PROCESS: ONE BY ONE. No batch, no pipeline.** Generate one shot, review, then
  the next.

---

## THE WALL COLOR (user's question)

The images are **B&W (monochrome)**, so "wall color" = a **shade of gray**.

**Problem:** forcing a black void fails — the wall keeps rendering **cream /
monochrome-white** (too bright, washed out, kills the mood).

**Answer — use a DARK CHARCOAL wall (deep gray, near-black at the edges):**
- The script = **single bare bulb, no fill, hard shadow, high contrast, moody.**
- A **dark charcoal** wall makes the bulb's light pool the ONLY bright area →
  dramatic, cinematic, matches the spec.
- A **cream/white** wall (the current problem) is too bright → flat, washed out.
- In B&W, a **dark warm-gray** (slightly brownish charcoal) reads as an "aged
  plaster wall" — aesthetic and moody.

**Prompt block (use in every shot):**
> "a dark charcoal wall behind the table, deep gray, the wall falls into shadow
> away from the bulb's light pool, only the area under the bulb is lit."

**Negatives (add):** `bright wall, white wall, cream wall, light background,
washed out, overexposed background`

**Options (if charcoal is too dark):**
1. **Dark charcoal** (recommended) — moody, matches the single-bulb spec.
2. **Mid-gray** — softer, less dramatic.
3. **Avoid cream/white** — the current problem.

---

## THE FULL SET — 11 reference images (in script order)

V7 only has 7. **The 5 scenario anchors (kf3c, kf5a, kf7a, kf7b, kf7c) are MISSING
from V7** — they exist in v4/v5/v6. We need all 11 so MiniMax H3 doesn't
hallucinate the motion.

| # | Image | Script shot | What it shows | Status |
|---|-------|-------------|---------------|--------|
| 1 | `kf1_empty` | Shot 1 start | table + ONE chair + bulb, no person | ✅ have |
| 2 | `kf2_seated` | Shot 1 end / 2 / 4 / 5-start / 7-start | Jaisal seated, facing camera | ⚠️ extra chair left + wall right |
| 3 | `kf3a_headnormal` | Shot 3 start | back view, head NORMAL | ✅ **perfect** |
| 4 | `kf3c_head90` | Shot 3 mid | back view, head **90°** (twist mid) | ✅ **DONE** (`kf2_headset\kf3c_head90.png`) |
| 5 | `kf3b_headtwisted` | Shot 3 end | back view, head **180°**, **HEAD ONLY** (body stays) | ✅ **SOLVED 2026-09-13** (`kf2_headset\kf3b_head180_00010_.png`) |
| 6 | `kf5a_stem` | Shot 5 start | ONE tiny stem on the table | 🔄 **V8 built** (`krea2_intro_kf5a_stem_v8.json`) — run + review |
| 7 | `kf5_plants_grown` | Shot 5 end | plants grown (rose + stems) | 🔄 **V8 built** (`krea2_intro_kf5_plants_grown_v8.json`) — run + review |
| 8 | `kf6_plants_dead` | Shot 6 end | SAME plants as kf5, now dead | 🔄 **V8 built** (`krea2_intro_kf6_plants_dead_v8.json`) — run + review |
| 9 | `kf7a_page` | Shot 7 stage 1 | PAGE floats in (on "കഥകൾ") | 🔄 **V8 built** (`krea2_intro_kf7a_page_v8.json`) — run + review |
| 10 | `kf7b_page_mic` | Shot 7 stage 2 | page + MIC drops in (on "രാഷ്ട്രീയം") | 🔄 **V8 built** (`krea2_intro_kf7b_page_mic_v8.json`) — run + review |
| 11 | `kf7c_cricket` | Shot 7 stage 3 | cricket assembly (on "കായികം") | 🔄 **V8 built** (`krea2_intro_kf7c_cricket_v8.json`) — run + review |

**Motion pairs for MiniMax H3 (first → last):**
- Shot 1 walk-in: `kf1_empty` → `kf2_seated`
- Shot 3 twist: `kf3a` → `kf3c` → `kf3b`
- Shot 5 growth: `kf2` → `kf5a` → `kf5`
- Shot 6 dying: `kf5` → `kf6`
- Shot 7 assembly: `kf2` → `kf7a` → `kf7b` → `kf7c`
- Shot 4 reverse: `kf2` reversed in post

---

## SHOT-BY-SHOT — what each image must show + the fix

**Shared blocks (every shot):**
- **CHARACTER:** the same young man (preserve exact face/identity): dark wavy hair,
  dark complexion, black full-sleeve shirt unbuttoned halfway.
- **WALL:** dark charcoal wall (see above).
- **ONE CHAIR:** ONLY ONE chair (the one at the table), centered. NO extra chairs.
- **CAMERA:** straight-on, centered, symmetric, eye level, static.
- **B&W:** black and white cinematic, high contrast, clean (no grain speckles).

### 1. `kf1_empty` — Shot 1 start
- **Show:** table + ONE centered chair + hanging bulb, NO person.
- **Fix:** ONE chair (centered), dark charcoal wall.

### 2. `kf2_seated` — Shot 1 end / 2 / 4 / 5-start / 7-start
- **Show:** Jaisal seated in the ONE chair at the table, facing the camera, calm.
- **Fix (from V7):** REMOVE the extra chair on the LEFT. REMOVE/handle the wall on
  the RIGHT (→ dark charcoal wall). ONE chair only.

### 3. `kf3a_headnormal` — Shot 3 start
- **Show:** back view (back of chair + his back), head NORMAL (facing the table).
- **Status:** ✅ **PERFECT — keep as-is.**

### 4. `kf3c_head90` — Shot 3 mid (SCENARIO ANCHOR)
- **Show:** back view, head rotated **90° to the side** (profile, nose sideways),
  body/shoulders stay facing away.
- **Fix:** MISSING in V7 — regenerate. This is the mid-point of the slow twist.

### 5. `kf3b_headtwisted` — Shot 3 end
- **Show:** back view, head rotated **180°** (face turned around to the camera over
  the shoulder), **BUT the BODY and SHOULDERS stay in the back view** (facing away).
- **Fix (from V7):** the whole body turned — WRONG. **ONLY the head rotates; the
  body/shoulders stay put.** (The script: "Head begins to rotate SLOWLY 180°...
  Body does not react.")

### 6. `kf5a_stem` — Shot 5 start (SCENARIO ANCHOR)
- **Show:** Jaisal at the table, ONE tiny thin stem just pushing through the table
  surface (the very first sign of growth, nothing else).
- **Fix:** MISSING in V7 — regenerate. ONE chair, dark wall.

### 7. `kf5_plants_grown` — Shot 5 end
- **Show:** Jaisal looking down at the table, plants GROWN (tall stems, big leaves,
  one rose open).
- **Fix (from V7):** REMOVE the 2nd chair (ONE chair only). Plants must be the
  SAME design as kf5a (so kf5a→kf5→kf6 is a consistent growth→death sequence).

### 8. `kf6_plants_dead` — Shot 6 end
- **Show:** Jaisal looking at the table with a melancholic expression, the SAME
  plants as kf5 now DEAD (wilted, drooping, rose closed, one leaf falling).
- **Fix (from V7):** REMOVE the extra chair. Dark charcoal wall. Plants must MATCH
  kf5 (same stems/rose, just dead) — anchor kf6 to the good kf5.

### 9. `kf7a_papers` — Shot 7 stage 1 (SCENARIO ANCHOR)
- **Show:** Jaisal at the table, dozens of loose sheets of paper floating in the
  dark space above/around the table (the first sign of the idea-burst).
- **Fix:** regenerate. ONE chair, dark wall.

### 10. `kf7b_burst` — Shot 7 stage 2 (SCENARIO ANCHOR) — **THE DISPLACEMENT**
- **Show:** the exact same table/chair/room/bulb/camera, but **Jaisal is GONE** —
  a violent burst of dozens of loose sheets of paper erupts from the exact space
  where he was sitting (toward camera, sideways, upward into the darkness). The
  chair is EMPTY. A small microphone floats among the papers.
- **Prompt rule (CRITICAL):** make the ABSENCE the primary instruction —
  "Remove the man completely. There is NO PERSON in the final image." Do NOT say
  "papers behind the man" (that locks him in as the subject). See the
  **ABSENCE-FIRST prompt rule** below.
- **Fix:** regenerate. If the identity workflow keeps the man, drop `ref_boost`
  to ~2-3 so "NO PERSON" wins.

### 11. `kf7c_cricket` — Shot 7 stage 3 (SCENARIO ANCHOR)
- **Show:** Jaisal COMPLETELY GONE. A cricket bat stands vertically (body/neck),
  two stumps beside it (hands), a round SOCCER BALL (round, NOT an oval American
  football) below (lower body), a sheet of paper with a simple curved smile line
  on TOP of the bat (head). A small microphone floats nearby. Dozens of papers
  suspended in the air, some fading to dark.
- **Fix:** regenerate. Same ABSENCE-FIRST rule as kf7b. Soccer ball = round.

---

## THE ONE-BY-ONE ORDER (no batch)

Generate + review in this order (each depends on the previous for consistency):

1. `kf1_empty` → review
2. `kf2_seated` → review (fix: one chair, dark wall)
3. `kf3a_headnormal` → ✅ keep
4. `kf3c_head90` → review (new)
5. `kf3b_headtwisted` → review (fix: head only, body stays)
6. `kf5a_stem` → review (new)
7. `kf5_plants_grown` → review (fix: one chair, plants match kf5a)
8. `kf6_plants_dead` → review (fix: one chair, plants match kf5)
9. `kf7a_papers` → review (new)
10. `kf7b_burst` → review (new — Jaisal GONE, papers erupt)
11. `kf7c_cricket` → review (new — Jaisal GONE, cricket assembly)

**After each:** the user reviews the image. If good → stage it as the anchor for
the next dependent shot (kf5→kf6, kf2→kf7a/b/c). If not → adjust that ONE shot's
prompt and re-run just that one.

---

## KEY RULES (do not break)

1. **Character = full char ref, NO scene anchor** (D058). A scene anchor breaks
   the face.
2. **ONE chair, centered** — every shot.
3. **Dark charcoal wall** — not cream/white, not a forced black void.
4. **Plants consistent** — kf5a (stem) → kf5 (grown) → kf6 (dead) must be the SAME
   plants.
5. **kf3b = HEAD ONLY rotates** — body/shoulders stay in the back view.
6. **All 11 images** (including the 5 scenario anchors) — so MiniMax H3 doesn't
   hallucinate the motion.
7. **Check the script** (`docs/INTRO_SCRIPT.md`) for every shot.
8. **ONE BY ONE** — no batch, no pipeline.
9. **ABSENCE-FIRST prompt rule (for character-vanish keyframes, e.g. kf7b/kf7c):**
   the identity workflow is strongly biased toward PRESERVING the person. If you
   describe the scene as "papers behind the man" / "the man sits still", Krea
   locks him in as the permanent subject and the papers become a secondary effect
   — the character STAYS. To get a character-free frame, make the ABSENCE the
   PRIMARY instruction:
   - Open with: "Remove the man completely from the scene. There is NO PERSON
     remaining in the final image."
   - State the scene must stay identical (same table, chair, room, bulb, camera,
     lighting, composition) and the chair is now EMPTY.
   - Describe the effect as a **physical burst/displacement** ("papers violently
     erupt from the exact space where the man was sitting"), NOT a soft dissolve.
   - End with a hard FINAL STATE line: "empty chair + explosive cloud of loose
     papers. Absolutely no human figure."
   - **Negative prompt** must list the person explicitly: `man, person, human,
     face, head, body, arms, hands, legs, clothing, shirt, silhouette, ghost,
     transparent person, partial person, duplicate person, visible human,
     humanoid, mannequin`.
   - If the man still appears, drop `ref_boost` to ~2-3 (or ~1.5) so "NO PERSON"
     wins, and/or re-roll the seed.
