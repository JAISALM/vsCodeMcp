# Current Task

## 🔴 PRIMARY GOAL: Scripting Episode 1
**Phase:** Moving from the "Red Card/Fight" of the first half into the 1950 Mind-Trip.

**Writer entry point (D132):** `episode1\CONTINUE_SCRIPT.md` — self-contained brief.
The writer model (Gemma) reads it and writes **only** the new file it names
(`episode1\episode1_script_part2.md`) — it must NOT edit existing files; the agent
model (Qwen) updates memory + commits afterwards.

**Next Milestones:**
1. **The Humorous Selection:** Define the IQ-based players (The Mathematician, The Lazy Genius, etc.).
2. **The Ship Journey:** Script the la lloC (Cura la lloC) journey to Brazil, including coconut practice and the "Fax" fix.
3. **The Brazil Final:** Detailed clash between Jaisal's Tactical India and Zidhan's Physical Brazil.
4. **The 360 Return:** Transition back to 2026 and the final handshake.

**Pending Technicals:**
- Verify MTP (Speculative Decoding) is active for Gemma writers.
- Maintain the 262K context window for long-term reasoning.

## 🔴 CHARACTER SHEET route analysis (2026-10-18, user-directed — TOP)
- User re-shared 5 reddit posts (P1 1wxixua, P2 1vov6jb, P3 1w2dujd, P4 1wsb4h3, P5 1wsee1y) + HF `PoopMan333/H3_Character_Sheet_Generator` + local folder `E:\minimax_workflow\character_sheet\` (4 workflows placed by user).
- **Reference file created: `project-memory\CHARACTER_SHEET.md`** — full source list, per-post explanations, local-workflow↔post mapping, model/pack gap analysis, fetch-route status.
- **Done:** HF README fetched (complete); all 4 local workflows node-analyzed; model + pack availability checked.
- **Reddit post bodies: ALL routes blocked** (reddit direct/helper 403 — `REDDIT_SESSION_COOKIE` stale from 10-11; mirrors dead/Anubis-gated; r.jina.ai unblocks **13:04 UTC = 18:34 IST** 10-18). Clean fix = user refreshes the cookie (F12 → reddit_session).
- **Key findings:** P1 ≈ PoopMan333 360°-orbit H3 sheet (best model match: ref2va + VAEs + turbo4step all present; gaps = int8_convrot 32B CLIP, v4 turbo LoRA); P2 ≈ `LocationOrbitSheetH3.json` (3 models + OrbitSheets pack missing); P3 ≈ `2BZ_H3_character_sheet_2stage_v1_EN.json` (toobusy + pysssss packs missing); P4 ≈ `minimaxh sheet patreon.json` (Fizgig stills + fused ref-delta turbo8 — 2 models missing); P5 ≈ `LEEBLAAB-QwenImage21-Character-SHEET.json` (models present; bf16 run CRASHED the server ~17:12; multi-angle format REJECTED by user).
- **HARD RULE (user): no ComfyUI workflow runs without explicit user confirmation.** Server currently DOWN (crash) — bring-up also needs go-ahead.
- **AWAITING USER:** (a) refreshed `REDDIT_SESSION_COOKIE`, (b) route choice (P1/P3/P4/P2/P5), (c) server bring-up.

## v6 sheets LOCKED (2026-10-18, user-approved — supersedes "pending verdict")
- User: v4/sweep "wood or wall, no emotion"; **Zidane = short halal cut (final)**; texture/realism gap vs civitai V2-LoRA; **base is NSFW → always explicit clothing**; sheets = normal weather, no rain/boat.
- **v6 = 01 t2i, V2 LoRA @1.0, `kr2realism` trigger, 8 steps, portrait** — `char_v6\jaisal_v2lora_00001`, `char_v6\zidane_v2lora_00001` — best sheets so far (weather clean, beards visible, halal cut, photographic texture).
- **LOCKED 2026-10-18:** copied to `challenge\consistent-short\refs\{jaisal,zidane}_sheet_v6.png` AND `input\char{1,2}_sheet.png` (overwrote the old 10-08 sheets). These are the canonical character refs — they REPLACE the rainy-street anchors as identity refs (D025 rain carry-over fix).
- **Next after sheet-route decision:** identity refset from CLEAN sheets → 04 demo → demo short.
- **Known limitation (user-acknowledged):** faces lack Kerala/South-Indian aesthetics (model + V2-LoRA European skew) — v6 is the best-so-far baseline; the new sheet workflows (esp. H3-based) are the lever for a better face prior.

## v4 emotional frames (2026-10-18) — pending user verdict
- User: v3/sweep faces "wood or wall, no human emotion"; **Zidane hair re-specified: short halal cut, no waves** (military/bun both deprecated); Jaisal = medium wavy (kept).
- v4 = candid emotional moments in prompts. **Zidane `char_v4\zidane_00001` = halal cut ✓ + half-smile ✓ (best so far)**. Jaisal `char_v4\jaisal_00001` = pensive, still the neutral one — may push expression harder.
- **After verdict:** lock refs → re-point 04 demo → demo short.

## Settings sweep — 02 runs at 10 steps now (2026-10-18)
- **User:** A/B images "feel like AI, some settings are clearly OFF." Root cause: 02 ran 6 steps (t2i sweet spot) — the identity-edit pack's design point is **10 steps** ("12 = more face detail").
- **Sweep:** Jaisal 10s@4MP clean + best detail (`char_sweep\jaisal_s10_4mp_00001`); Zidane @4MP DUPLICATED (seeds 77/78, grounding 384 didn't help — tracks 4MP on this ref); Zidane 10s@2MP clean (`char_sweep\zidane_s10_2mp_00001`).
- **Proposed lock (user verdict pending):** 02 = 10 steps, 2MP 16:9, g768, ref_boost 4. Jaisal may keep 4MP (clean there).
- **After verdict:** lock the two refs → re-point 04 demo shot → demo short.

## Jaisal/Zidane re-scope + V2-LoRA A/B (2026-10-18, user-directed — supersedes v3 face sheets)
- **User rejected v2/v3 sheets** ("trash, unworthy"). Picked exact face anchors: Jaisal = `char1_NEW_realism_s6_00001` (A/B output), Zidane = `krea2_char1_face_c_00001`. Corrected specs: Jaisal slim + medium wavy hair + thin beard; **Zidane athletic/muscular (not chubby) + SHORT military cut (bun spec deprecated) + thin beard**. Prompt style = author's cinematic natural language (user pasted the author's car prompt).
- **Done:** refs → `input\jaisal_ref.png`/`zidane_ref.png`; 02 gained V2-LoRA node 97 (pure vs +V2 @1.0); 4-way grid `output\char_ab\` (jaisal/zidane × pure/v2, author-style scenes: bridge / boat). Identity held both faces.
- **Read:** Jaisal pure≈v2 (near-identical). Zidane: pure = short crop (≈ military cut ✓), v2 = wavy like ref. Thin beard faint.
- **Pending user verdict:** variant per character + beard strength + Zidane build. Then lock refs → re-point 04 demo shot → demo short.

## Character sheets v3 — FACE-ONLY close-ups (2026-10-18, user-directed)
- **User directive:** v2 scene sheets "look awful, something is off — don't put anything about the background in the prompt, we want clear face images FIRST." → sheet prompts rewritten as face-only close-ups, ZERO scene/background words (`char_sheet_v3.py`), per-character distinct faces, explicit seeds (headless seed lesson).
- **Done:** `char_sheet\char1_00003_.png` (wavy shoulder hair, 5-o'clock shadow, narrow face, black tee) + `char_sheet\char2_00003_.png` (top bun, rounder face, thicker brows, white tee). Both clean plain-background close-ups, RAW skin quality, clearly different people. Copied to `input\char{1,2}_sheet.png` (overwriting v2 scene sheets).
- **Pending user verdict** on the two faces (char2 came out with light chin shadow despite clean-shaven ask — minor).
- **After verdict:** refset stage (02) uses these face refs + scene instructions (char1 bridge / char2 boat) — the scene words live ONLY in the refset instruction, not the sheet.

## Krea2 base LOCKED IN + character sheets DONE (2026-10-18)
- **User verdict:** Krea2Realism_V1 wins the A/B → locked in as the Krea2 base (D133 resolved).
- **Done:** app workflows `01_character_sheet`/`02_identity_refset` swapped to `Krea2Realism_V1` (6 steps, euler/simple, cfg 1; V2 LoRA zeroed in 01; old files kept as `*_oldturbo.json`).
- **Character sheets + refsets generated (new base):** `output\char_sheet\char{1,2}_00001_.png` + `output\char_refset\char{1,2}_00001_.png` (char1 = misty path → bridge; char2 = boat). Identity held sheet→refset. Refs in `input\char{1,2}_sheet.png`. These 4 are the app's canonical char1/char2 refs.
- **Remaining today:** user pick of canonical sheet (or keep 10/08 face set) · re-point 04 demo shot refs (2001/2002) from the old Jaisal bridge refs to `char_refset/char1` + a char1 second-frame ref · run the char1 bridge shot end-to-end on the timeline · episode1 age question (script says Jaisal 16).

## Character re-scope (2026-10-18, D137) — OLD schoolboy character DEPRECATED
- **New characters (user-directed):** char1 (Jaisal) ~26, wavy black hair, slim, plain black t-shirt; char2 (Zidhan) ~26, top bun, slim, plain white t-shirt. Face refs: `output\krea2_char{1,2}_face_{a,b,c}_*.png` (2026-10-08; a = misty forest profile, b = boat golden hour, c = rainy street).
- **Cleanup done:** AGENTS.md character section, PRODUCTION_CONSISTENCY.md costume lock, both challenge PIPELINE.md files, INTRO_VIDEO_PLAN.md, R2V guide examples — all updated. Violet-uniform/hat kid prompt verified already gone from all files. `prompts\jaisal_identity_instructions.txt` = OLD character (superseded).
- **Re-anchored A/B (D133 redo):** `data\krea2_abtest_char1.json` (validates 0/0) — char1 + char2 t2i, same prompt+seed on OLD turbo s10 vs NEW Krea2Realism_V1 s6, euler/simple cfg 1, 1152×1792. Job `30869cc1` queued 2026-10-18.
- **Open:** episode1 script still says "Jaisal (16, rose-pink shirt)" — user to confirm story age. Challenge demo shots (04 workflow) must be re-pointed to char1/char2 refs (currently still wired to the old Jaisal bridge refs).

## Krea2 Realism V1 A/B test (2026-10-17, D133) — A/B DONE, AWAITING USER VERDICT
- **Download:** terminal resume (user-sanctioned after 2 failed browser downloads) via `utilities\download_krea2_realism_resume.py` (Range-resumable). **COMPLETED 2026-10-18:** `E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\Krea2Realism_V1.safetensors` = exactly 13,141,769,680 bytes (verified); server lists it in `/models/diffusion_models` — no restart needed.
- **A/B run DONE 2026-10-18** (`data\krea2_abtest_realism.json`, seed 42, same prompt): outputs `E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\krea2_abtest\OLD_turbo_fp8_s10_00001_.png` vs `NEW_realism_v1_s6_00001_.png`. Agent read: both good; NEW slightly more natural skin/texture + more dynamic framing — but one seed only. **User judges; if NEW wins → swap Krea2 base (keep old files).** Suggested: 2-3 more seeds before swapping.

## Open Source Higgsfield challenge — RESCOPE to "character-consistent short app" (D135, 2026-10-18) — BUILDING
- **Entry (user-approved 2026-10-18):** character-consistent short app = our `krea2_identity_edit` face-lock front-end (workflows 01/02) + 2-anchor H3 shots + **obvpm-timeline engine** (public, credited) + ffmpeg assembly. Targets: **Most Viral + Open Weights (5090) + H3 bonus ($1K credits)**; Most Innovative claim dropped (frontier = obvpm/LongTakeNoCuts/clown-anchoring/fizgig — all public, all credited).
- **Folder:** `challenge\consistent-short\` (new; user pushes as a NEW public GitHub repo — user's only TODO, plus final submit). `CHALLENGE_PLAN.md` (D134) kept for the cloud-ops steps.
- **Done 2026-10-18:** packs installed + obvpm updated to v0.2.16 (see D135); `04_h3_timeline_r2v.json` adapted + **validates 0 errors**; smoke test runs 1-4 failed on the dead Set/Get constant layer → **root cause found + fixed (D136)**: MCP converter treats SetNode/GetNode as UI-only and never honors obvpm Unbundle `get` widgets → ALL 9 affected nodes re-wired to real emitted sources (1374/1379 ← 752, 1390 ← 761, 1392 ← 1383, 1436 ← 1526, 1629/1630 ← 1449, engines 1359/1488 `in` ← 1457 LazyCaseSwitch + seeds ← 765 SeedNode, 1457 cases ← 1290/1335 ValuePresets + `in` ← 1449). **SMOKE TEST PASSED (run 5, job `b6774902`): first full end-to-end timeline render — `output\clip_00001.mp4` 5.17 s 1376×768 24 fps + AAC audio + `.mctx` sidecar; character consistent across the shot** (style drifts toward 3D-animated vs photoreal refs — demo shots should use identity-locked refs from 02).
- **Next:** character-lock sanity (02 refset) + 2nd-shot cross-face check → app README + MODELS credits → 2-3 demo shots + demo video → comfy-cli cloud Build test → submit typeform `V1dSQrkS` before **10/30 9am PT**.

**Project files (read these when resuming) — Episode 1 hub = `episode1\`:**
- `episode1\DECISIONS_EPISODE1.md` — **story decisions** (characters, metaphors, scene beats) — read first
- `episode1\episode1_script_part1.md` — full Episode 1 script (Part 1 / first half; ends at the B&W transition — **second half NOT written yet** = the work above)
- `episode1\episode1_first_half.md` — first-half sequence summary
- `episode1\narrative_map.md` — characters, symbols, concept map
- `episode1\first_script.md` + `episode1\episode1_structure_prompt.txt` — earlier outline + the Gemma structure prompt (@8106)
- `episode1\workflows\` — reusable Episode 1 workflow JSONs (see its README)
- `docs\` — pipeline guides; `utilities\commit_md.ps1` — daily .md safety-commit (D131)
