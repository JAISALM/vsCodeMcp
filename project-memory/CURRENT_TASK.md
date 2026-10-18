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
