# Project Decisions

## D001 - D128: The Legacy Foundation
- **D001-D041:** Core setup, including the **NO MUSIC (D041)** rule for all future scenes.
- **D042:** Blender MCP official setup for the director-driven workflow.
- **D060-D110:** The "Silly-Silly" and "Krea2" style-locking experiments, including the PE (Prompt Expansion) variance.
- **D111-D119:** The "Boar-Grave" blockout, the MiniMax H3 R2V pipeline, and the 5-angle camera strategy.
- **D120:** FaceRefine armor for facial consistency in long shots.
- **D121:** The Bilingual Capture route (Dictation → Manglish → Bilingual Script).
- **D122:** Disk Space Rescue (Moving models to F: drive and creating junctions to save D: drive).
- **D123-D128:** The "Writing Model" bake-off. **D128.1: HauhauCS QAT Q4_K_M confirmed as the default writer.**

## D129 — The Grave Metaphor & IQ Selection (2026-10-13)
- **The Grave:** Digging a boar grave symbolizes digging up the past. Jaisal's transition from digging (down) to rising (up) with Zidhan's help represents his journey back into the academy.
- **IQ Selection:** In the 1950 mind-trip, Jaisal picks players based on "Football IQ" (math, space, and positioning) rather than raw power.
- **Tactics vs. Physicality:** The core clash is "Tactics" (Jaisal) vs "Kaalappoott" (Zidhan). The realization: Tactics dominate the game, but Physicality wins the final.

## D130 — Cinematic Transitions & Ground Reality (2026-10-14)
- **The Coconut Tree Wipe:** A seamless transition from Jaisal's backyard to the training ground using a coconut tree as a frame-wipe.
- **The Sputtering Spray:** A detail showing the lack of resources in the academy—the first-aid spray is nearly empty, highlighting the need for tournament victory to fund the academy.
- **The "Kaalappoott" Shift:** Shift from a Red Card to a **Yellow Card + Fight** in the first half, keeping Adam in the game while showcasing the messy, physical nature of 5's football.

## D131 — Daily .md safety-commit standard (2026-10-14)
- **Decision:** All `.md` changes (project memory, docs, scripts, root) are committed to git **immediately after changing** via `utilities\commit_md.ps1`, which **also pushes `origin/main`** (GitHub `JAISALM/vsCodeMcp` — the true safety net beyond local disk). Windows scheduled task `VsCodeMcp-MdDailyCommit` (daily **22:30**) runs it as a safety net.
- **Reason:** a session nuked `project-memory/` state + task files on 2026-10-14 (recovered from git history). The commit history is the only reliable recovery path.
- **Gitignore:** new images/media (`*.png`/`*.jpg`/`*.mp4`/`*.wav`/`*.blend`/`*.log`) are NOT committed; previously tracked images stay tracked. Do not `git add -A`.
- **What goes into git (refined 2026-10-14):** `.md` files = always (auto). **Workflow JSONs = manual, only when reusable/needed in the future** (Episode 1 ones: `episode1\workflows\`). Generated images/audio/video = never.
- **Restore recipe:** `git log --oneline -- <file>` → `git checkout <commit> -- <file>`.
- **Status:** Active. Also recorded in AGENTS.md ("Daily .md safety-commit standard").

## D132 — Writer-model boundary + resume brief (2026-10-14)
- **Decision:** the **writer model (Gemma4-31B QAT)** does creative output ONLY — it
  **never edits existing project files**; it may **create new files only** (e.g.
  `episode1\episode1_script_partN.md`). All edits to existing files (memory, decisions,
  docs, commits) are done by the **agent model (Qwen)** session or the user.
- **Resume brief:** `episode1\CONTINUE_SCRIPT.md` = the self-contained entry point for
  "continue the script" — the writer reads it, writes the ONE new file it names, touches
  nothing else. Framing rule: writer tasks are always ONE action, never multi-step
  file juggling (Gemma is weak at agentic work).
- **Reason:** makes "start a new session → 'let's continue the script'" reliable:
  AGENTS.md points to the brief; the brief carries all canon (characters, motifs,
  milestones, anchor line, NO-MUSIC rule).
- **Status:** Active. Also recorded in AGENTS.md ("Writer-model boundary").

## D133 — Krea2 Realism V1: A/B test → possible Krea2 base replacement (2026-10-17)
- **Candidate:** `Krea2Realism_V1.safetensors` (FP8, 13.14 GB; HF `RudySen/Krea2-Realism-Checkpoint`) — a merge of the author's Realism Checkpoint + V3 LoRA (LoKr); drop-in UNET replacement for Krea2 pipelines (keep `qwen3vl_4b` CLIP + `qwen_image_vae`). Community: image-edit works well (still pair with `krea2_identity_edit` LoRA for face locking), character LoRAs work, no refusal-reduction LoRA needed. Recommended: **Euler + Simple, 6 steps (4–8), CFG 1.0, 2MP** (1152×1792 — trained high-res; 1MP can show minor noise, fix with RTX upscaling). NSFW-capable → be specific about clothing in prompts. Author's RTX 5090 speeds: 736×1344 = 7 s, 1472×2688 = 15 s, 2944×5376 = 1 m 38 s; 4K direct, ~24 GB peak VRAM.
- **Ops facts (user-confirmed):** ALL models live in `E:\ComfyUI_windows_portable\ComfyUI\models` (the running 8188 server is the `E:\comfyUi_latest` install, which scans that tree via `extra_model_paths.yaml` `production` profile). User downloads models **via browser, not terminal**. Drop the new model into `E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\` (per README).
- **Test:** A/B workflow `data\krea2_abtest_realism.json` — same prompt + seed 42: old `krea2_turbo_fp8_scaled` @10 steps vs new `Krea2Realism_V1` @6 steps, euler/simple, cfg 1, 1152×1792; output prefixes `krea2_abtest/OLD_turbo_fp8_s10` vs `krea2_abtest/NEW_realism_v1_s6`.
- **VERDICT 2026-10-18 (user): "realism output is better, let's lock in."** Re-anchored A/B on the REAL characters first (`data\krea2_abtest_char1.json` — char1 rainy street + char2 boat, same seed both bases): Krea2Realism_V1 rendered both characters younger/clean-shaven/natural-skinned, matching the 10/08 face refs; the OLD turbo base drifted toward bearded/older faces.
- **LOCKED IN 2026-10-18:** `Krea2Realism_V1.safetensors` is now the Krea2 base in app workflows `01_character_sheet` + `02_identity_refset` (backups kept as `*_oldturbo.json`). Changes: UNET swapped, KSampler steps 10→6 (euler/simple cfg 1 — author's setting), 01's extra `Krea2-realism-V2` LoRA zeroed (pure base = approved A/B output), prompts/negatives rewritten for char1/char2 (no more beard — negatives now include "beard, stubble").
- **Reddit access recipe:** www/old.reddit + `.json` endpoints are blocked (headless "network security" + login redirect) → use redlib mirrors via web_fetch: `https://safereddit.com/r/<sub>/comments/<id>/` works (verified on 1x76buu).
- **Status: RESOLVED — Krea2Realism_V1 locked in as the Krea2 base.**

## D135 — Challenge entry RESCOPE: "character-consistent short app" (2026-10-18, user-approved)
- **Decision:** the challenge entry is NOT a frontier-solver (long-take/continuity problems are already solved by public open packs — `comfyui-obvpm-timeline` (chanon/obvpm, GPL-3.0, mini H3 video editor: extend/bridge/loop from latents, seam rating, live preview, latent upscale), `h3_clown_anchoring` (roycho87 — flash-free joins via noise-mask-hold of next shot's real latents), `H3-LongTakeNoCuts` (xyzDist — SAM3-masked refine + frame-blend kills the "photocopy" degradation), `Fizgig H3 Tweak` (shootthesound — detail/contrast, scene-variation, prompt-strength dials), `SceneCut` (PedroMarinhoDev, MIT — shot detection + trim). All user-shared or community-published.)
- **The entry:** a **character-consistent short app**: our `krea2_identity_edit_v1_2` LoRA face-locks the character (Krea2 sheet → identity refset → 2-anchor H3 shots, D020/D023), **obvpm-timeline as the timeline engine (credited, public)**, ffmpeg assembly, natural-sounds-only (D041). Our moat = the identity LoRA (original trained weights) + the 2-anchor technique + app packaging/docs; the frontier repos are credited, not re-solved.
- **Prize targets (honest):** Most Viral ("your face in a short, same face every shot") + Open Weights Only (5090) + H3 bonus ($1,000 credits). **Dropped the Most Innovative claim** (obvpm et al. own that ground). Best Overall = bonus if the demo lands.
- **Build (in `challenge\consistent-short\`, new folder in the vsCodeMcp repo — user pushes it as a new GitHub repo):** `workflows/01_character_sheet.json`, `02_identity_refset.json` (both validated 0/0 earlier), `03_h3_r2v_2ref.json` (validated 0/0), `04_h3_timeline_r2v.json` = the author's `h3_obvpm_timeline_r2v_v0.1.4-007A` adapted: removed `H3LivePreview` (missing `taeh3.safetensors`), un-bypassed generator engine (inst 1359) + `H3ContextWindows` (1356), re-pointed upscale engine model link to 1356, **Set/Get constant layer re-wired to real sources (D136)**. **Validates 0 errors** (11 warnings = author's default-muted optional groups).
- **Packs installed 2026-10-18 into `E:\comfyUi_latest\...\custom_nodes`:** `comfyui-obvpm` UPDATED to **v0.2.16** (was Aug-old; timeline needs ≥0.2.16), `comfyui-obvpm-timeline` 0.1.4, `ComfyUI-MiniMax-H3-Turbo` (Larryvrh), `ComfyUI-Fizgig-H3-Tweaks` (shootthesound). ComfyUI restarted; all nodes verified in object_info (`MiniMaxH3Timeline`, `FizgigH3Tweaks`, `MiniMaxH3TurboLoRA`, `ValuePresets (obvpm)` etc.).
- **Smoke test (2026-10-18): PASSED.** Jaisal bridge refs (`jaisal_1_longshot.png` + `jaisal_4_middle.png` wired as ref_image_0/1 via native LoadImage nodes 2001/2002), 2-anchor 16:9 1MP prompt on subgraph node 763, 5 s timeline. Runs 1-4 failed on the dead Set/Get layer (D136) → fully re-wired → run 5 `b6774902` = **first full end-to-end timeline render**: `output\clip_00001.mp4` (5.17 s, 1376×768, 24 fps, AAC audio) + `.mctx` sidecar. Character consistent across the shot; style drifts toward 3D-animated vs the photoreal refs → demo shots use identity-locked refs (02 refset).
- **Remaining:** character-lock sanity (02 refset) + cross-shot face check, write app README (credits + setup), user's public GitHub repo, comfy-cli cloud Build test, 2-3 demo shots + demo video, submit typeform `V1dSQrkS` before **10/30 9am PT**.
- **Status:** Active — build in progress; **Jaisal Episode 1 remains the primary goal** (challenge work done in bursts).

## D136 — MCP UI→API converter drops SetNode/GetNode + obvpm `get` widgets (2026-10-18)
- **Symptom:** timeline workflow `04` headless runs failed at Unbundle nodes: `Unbundle: nothing is set as 'h3_clip_vaes'` / `no bundle. Connect a bundle to 'in'` — even with explicit ordering links added to the UI file (verified present on all three sides).
- **Root cause:** `comfy_cli\workflow_to_api.py` (the converter behind `run_workflow`/`validate`):
  - `_UI_ONLY_NODE_TYPES = {Note, MarkdownNote, PrimitiveNode, GetNode, SetNode, Reroute}` — **SetNode and GetNode are never emitted** to the API prompt (they're also absent from the live `/object_info` — KJNodes' JS handles them UI-side only).
  - Any link input whose source is a non-emitted node is **orphan-stripped** (`_strip_orphan_link_inputs`) → the consumer silently loses the input → falls back to widget defaults at runtime.
  - The converter's Set/Get tracer (`_collect_get_set_mappings`/`trace_get_set`) only bridges **wired GetNode→SetNode KJNodes pairs**; it has **no awareness of obvpm `Bundle.set` / `Unbundle.get` widget constants** (`bundle.py` L199–211: `get` is consulted ONLY when the `in` input is None).
  - Author's subgraphs are otherwise intact: port→internal bindings use `origin_id: -10`/`target_id: -20` in the subgraph def's `links` array (verified complete for engines 1359/1488/1334).
- **Fix applied to `04_h3_timeline_r2v.json` (permanent, committed with the file):** rewire every affected consumer to a REAL emitted source, bypassing the dead Set/Get layer:
  - Unbundle 1374/1379 (`h3_clip_vaes`) ← subgraph 752 slot 0 (CLIP/VAE bundle)
  - Unbundle 1390 (`h3_input`) ← subgraph 761 slot 0 · Unbundle 1392 (refs) ← Bundle 1383
  - Unbundle 1436 (`h3_upscale_vaes`) ← subgraph 1526 slot 0 · Unbundle 1629/1630 (`h3_timeline_outputs`) ← Bundle 1449
  - Engine `in` ports (1359 slot 4 / 1488 slot 4) ← 1457 LazyCaseSwitch output (timeline-selected gen/upscale engine settings bundle) · engine `noise_seed` ports ← 765 SeedNode
  - Author's test media nodes (LoadVideo 1082, LoadAudio 1083/1094) already mode=4 (bypassed) — their files don't exist.
- **Rule for all future obvpm-timeline work:** never rely on SetNode/GetNode/`get`-widget constant plumbing in UI-format files that will run headless via comfy-cli/MCP. Always wire the real bundle source. `h3_upscale_options` (1499/1502) has no setter anywhere in the file — only matters if the gated-off upscale-options path is ever enabled.
- **Status:** Fixed + verified (run 3 executed 28 nodes incl. all re-wired nodes; run 4 `41787e45` pending).

## D137 — Character re-scope: two adult men (char1/char2); schoolboy character DEPRECATED (2026-10-18, user-directed)
- **Decision (user, 2026-10-18):** the lead characters are NOW **char1 (Jaisal)** — ~26-year-old Indian man, wavy black hair, slim build, plain black t-shirt — and **char2 (Zidhan)** — ~26, black hair in a loose top bun, slim, plain white t-shirt. Canonical face refs (Krea2, 2026-10-08): `output\krea2_char1_face_{a,b,c}_*.png` + `krea2_char2_face_{a,b/c}_*.png` (a = misty forest profile, b = wooden boat golden hour, c = rainy street frontal; latest batch `_00007`/`_00008`).
- **DEPRECATED (never prompt again):** the old "young schoolboy, short dark hair, rose-pink collared shirt, black trousers, black school bag" character (D022) and the even-older "kid with violet uniform + hat" iteration (user had its prompt removed earlier — verified gone from all .md/.txt).
- **Reason:** user's actual project characters are the two adult men (the 10/08 face sets); all character work (A/B tests, identity refsets, H3 shots, challenge demo) must use them.
- **Cleanup done 2026-10-18:** AGENTS.md character section rewritten; `PRODUCTION_CONSISTENCY.md` costume lock updated; both challenge `PIPELINE.md` costume examples updated; `INTRO_VIDEO_PLAN.md` character line updated; `docs\MINIMAX_H3_R2V_PROMPTING_GUIDE.md` example subject updated. History files (WORKFLOW_HISTORY, old EXPERIMENTS entries) left as-is. `prompts\jaisal_identity_instructions.txt` still holds OLD-character instructions — superseded for new work (char1/char2 identity instructions to be written when needed).
- **Open question for user:** `episode1` script still says "Jaisal (16, rose-pink shirt)" in the school scene — confirm whether the story ages Jaisal up to ~26 (writer task) or the school scene keeps a younger version.
- **NSFW-base discipline + V2-LoRA realism recipe (2026-10-18):** user flagged the Krea2Realism base is majorly NSFW — any prompt without explicit clothing gets "spicy" output. **RULE: every Krea2 prompt MUST name full clothing ("plain black t-shirt and dark trousers, fully clothed") — no exceptions, halal project.** User decision: keep the base only if realism justifies it (it does so far); V2-LoRA is the realism route. **V2-LoRA civitai recipe (from `civitai.red/images/135654365`):** prompt starts with the **`kr2realism` trigger tag**, natural casual real-life scenes, explicit clothing, warm/natural lighting.
- **Character sheets = CLEAN identity frames (2026-10-18):** user: "why is he on a boat bro.. just place him in a normal weather, not in rain" — sheets are **normal clear dry weather, simple residential-street background, NO rain, NO scene props** (rain belongs to demo scenes only). D025 rain carry-over means identity-edit refs must be non-rainy images → **sheets are generated t2i (no ref), then used AS the identity refs** (ref = clean sheet → downstream scenes keep their own weather).
- **v6 result (pending user lock):** t2i (01), V2 LoRA @1.0, kr2realism trigger, 8 steps, portrait 1152×2048 — `char_v6\jaisal_v2lora_00001` (slim, medium wavy, thin beard now VISIBLE, black tee, calm) and `char_v6\zidane_v2lora_00001` (short halal cut, muscular arms, half-smile, white tee) — best sheets so far; texture reads photographic (no more "wood or wall").
- **USER RE-SCOPE 2026-10-18 (supersedes the earlier sheet prompts):** the v2/v3 scene+face sheets were rejected ("trash, unworthy"). User's picks + corrected specs:
  - **Jaisal (char1):** face anchor = `output\krea2_abtest_char1\char1_NEW_realism_s6_00001_.png` (copied to `input\jaisal_ref.png`) — **slim build, medium-length wavy black hair, thin/patchy beard** (~26).
  - **Zidane (char2):** face anchor = `output\krea2_char1_face_c_00001_.png` (copied to `input\zidane_ref.png`) — **athletic/muscular build (NOT chubby, same base attributes as Jaisal), SHORT military-style haircut, thin/patchy beard** (~26). (Zidane's old "loose top bun" spec is deprecated — user: "shorter hair, military cut or something".)
  - Both have patchy/thin beards (26-year-old men, not clean-shaven).
  - **Prompt style:** user pasted the author's example prompt (African man driving, cinematic, natural language) — "similarly we need to get the image for our character" → author-style cinematic natural-language prompts (see `set_02_ab.py` INSTR).
  - **V2-LoRA A/B (user asked to compare):** 02 now carries `Krea2-realism-V2.safetensors` node 97 (55→97→71→79; strength 0.0 = pure base). 4-way grid in `output\char_ab\`: `jaisal_pure`/`jaisal_v2` (seed 42, ref jaisal_ref), `zidane_pure`/`zidane_v2` (seed 77, ref zidane_ref), landscape 2048×1152.
  - **A/B read:** identity held both faces from the user-picked refs; the two characters look distinct. V2 LoRA @1.0 made little difference on Jaisal (near-identical, face is identity-locked); on Zidane it changed HAIR (pure = short textured crop ≈ the military cut the user wants; v2 = wavy medium, like the ref). Scenes carried ref tone per D025 (bridge/canal both rendered fine).
- **Character sheets + identity refsets generated 2026-10-18 (app workflows, NEW base):**
  - `output\char_sheet\char1_00001_.png` — char1 sheet (wavy hair, clean-shaven, black tee, misty backwater path, 1152×2048). Copied to `input\char1_sheet.png`.
  - `output\char_refset\char1_00001_.png` — char1 identity-locked on the stone-bridge scene (1928×1088). Face held from the sheet → identity-edit LoRA works on Krea2Realism_V1.
  - `output\char_sheet\char2_00001_.png` — char2 sheet (top bun, white tee, wooden boat, golden hour). Copied to `input\char2_sheet.png`.
  - `output\char_refset\char2_00001_.png` — char2 identity-locked boat scene (1928×1088). Face held.
  - App workflow files after the swap: `01_character_sheet.json` (currently set to char2 — flip prompt+prefix per character via `utilities\sheet_char2.py` / the char1 text in `swap_krea2_base.py`), `02_identity_refset.json` (currently char2 — flip via `utilities\refset_char2.py`). Backups: `*_oldturbo.json`.
  - These 4 images are the challenge app's canonical char1/char2 refs for the demo short (bridge shot uses `char_refset/char1`, boat shot uses `char_refset/char2` or the 10/08 face set).
- **Status:** Active — all new character work uses char1/char2 on Krea2Realism_V1.

## D134 — Open Source Higgsfield challenge entry "Story-Short" (2026-10-17, user-approved GO)
- **Decision:** enter the Comfy "Open Source Higgsfield" challenge (deadline **10/30 9am PT**, winners 11/6) with a **"Story-Short" app**: one prompt → Krea2 character sheet → identity-edit face-locked reference set → H3 R2V 2-ref shots (D020) → assembled video. Scoped to **H3 bonus ($1,000 API credits) + Open Weights Only (5090)**; $10K Best Overall = free auto-entry, don't chase; LTX $2K cash bonus = skipped (no LTX pipeline).
- **Reason:** our movie pipeline already IS the app (D020/D021/D023) — packaging proven workflows ≈ packaging work, not new development. All node packs used are public GitHub repos (several merged into core ComfyUI) → public cloud Build feasible. H3-bonus credits are directly usable for the movie.
- **Scope rules:** 3 core workflows (character sheet / identity refset / H3 R2V), UI format; local Qwen PE `TextGenerate` node DROPPED from cloud version (needs local llama.cpp); assembly via ffmpeg; NO partner nodes/APIs (open-weights compliance); identity-edit LoRA + character sheets become PUBLIC (user-approved).
- **Ops:** entry runs on Comfy cloud GPUs (Comfy API Build/Release/Deployment via comfy-cli) — does NOT touch the local 5090; sign up EARLY (first 200 signups get free credits, form: `form.typeform.com/to/Ayn9Cwfj`); stop/delete deployment after submission (storage billing); user creates the public GitHub repo.
- **Status:** Active — plan + checklist in `challenge\CHALLENGE_PLAN.md`.

## D138 — Character-sheet route analysis + no-run-without-confirmation rule (2026-10-18)
- **HARD RULE (user directive):** NO ComfyUI workflow runs without explicit user confirmation. Applies to all sheet workflows and, until rescinded, everything else. (Trigger: the Qwen-2.1 multi-angle sheet was pointed at a wrong format and the user stopped it mid-analysis.)
- **v6 sheets LOCKED** (user-approved "the best we can produce yet"): `char_v6\jaisal_v2lora_00001_.png` + `char_v6\zidane_v2lora_00001_.png` → canonical at `challenge\consistent-short\refs\{jaisal,zidane}_sheet_v6.png` and `input\char{1,2}_sheet.png` (replaced the old 10-08 sheets). They replace the rainy-street anchors as identity refs.
- **Kerala-aesthetics limitation (user-acknowledged):** Krea2 + V2-LoRA face prior skews European; v6 = best-so-far baseline. H3-based sheet workflows (new analysis) are the next lever.
- **Reference file:** `project-memory\CHARACTER_SHEET.md` — 5 reddit posts (P1 1wxixua / P2 1vov6jb / P3 1w2dujd / P4 1wsb4h3 / P5 1wsee1y) + HF `PoopMan333/H3_Character_Sheet_Generator` + local `E:\minimax_workflow\character_sheet\` (4 workflows).
- **DSH Reddit route (RESOLVED 18:35 IST, supersedes "blocked on every route"):** DSH's built-in
  web fetch is text-only (no JS) — Reddit's JS challenge is impassable for it. New helper
  `utilities\reddit_browser_fetch.py` (local Playwright Chromium + persistent profile, system
  Python `C:\Program Files\Python310\python.exe`) + `utilities\extract_reddit_text.py` —
  **all 5 post bodies fetched headless, no session, 18:25–18:35 IST** →
  `data\char_sheet_reddit\P{1..5}_{dsh.html,text.txt}`. Authors verified: P1 u/cgpixel23
  (H3 image-gen sheet — NOT the PoopMan333 orbit repo), P2 u/lumos_ai (OrbitSheets pack,
  FREE on github), P3 u/inazma44 (2BZ — all 6 model links extracted from the workflow's note
  node), P4 u/-Ellary- (civitai.red/posts/31291351), P5 u/LeebLaab (local-LLM nodes removed).
  Helper `is_gated` fixed to title-based detection (a bare `recaptcha` shell script tag is NOT
  a gate).
- **Status:** Active — awaiting user's route choice (ranked P3 → P4 → P1 → P2 → P5 in
  CHARACTER_SHEET.md); server DOWN (crashed on the P5 bf16 attempt).

## D143 — FLUX.2 KLEIN 9B DENSE for the LoRA dataset workflow (2026-10-18, user call)
- **Decision:** use **FLUX.2 [klein] 9B** (not 4B) for the character-dataset stage — "we are
  aiming for quality not garbage ... stick with the more heavy weights which will fit our
  hardware" (32 GB VRAM, 64 GB RAM).
- **Workflow:** `E:\Flux_klein\1 Click Dataset (Klein 9b).json` (user-selected: "this is what
  we are going to use") — Ref-Latent-Controller (u/Capitan01R), one reference face in → full
  dataset set out (768×1120).
- **Models (all open-source, no token):** `flux-2-klein-9b.safetensors` (17.3 GB,
  `black-forest-labs/FLUX.2-klein-9B`) + `qwen_3_8b_fp8mixed.safetensors` (8.3 GB,
  `Comfy-Org/vae-text-encorder-for-flux-klein-9b`) + `flux2-vae.safetensors` (0.3 GB, done).
- **Why fits:** 9B bf16 ≈ 17 GB < 32 GB VRAM; text encoder offloads to 64 GB RAM after encoding.
- **External source locations now logged** in `docs\EXTERNAL_WORKFLOW_SOURCES.md`
  (`E:\Flux_klein\` + `E:\minimax_workflow\`); user-workflows folder triaged (D143 companion:
  `docs\WORKFLOW_TRIAGE_2026-10-18.md` — 34 kept / 211 archived, reversible).
- **Status:** Active — models downloading (job pwsh-183).

## D142 — T2I CHARACTER RECIPE: natural language + clean negative + 8 steps (2026-10-18, A/B-proven)
- **Problem:** t2i character faces "kinda off, like grains". Web research (Krea2 V2 thread, u/rynaleopard):
  crisp results = **natural-language 4-5 sentence prompts, NOT tag stacking** + simple workflow;
  our stock 01 negative carried SKIN-FIGHTING terms ("plastic, waxy skin, airbrushed, smooth skin,
  AI look, rendered, CGI") → same anchor-fight mechanism as D140 → desaturated grainy face.
- **A/B/C (Zidane seed 77):** stock negative 8s = grainy · **clean negative 8s = natural warm skin
  (WINNER)** · clean negative 16s = also natural but 16 steps regenerates more → different face, NOT
  more clarity.
- **LOCKED recipe for 01 character t2i:** natural-language paragraph (4-5 sentences, `kr2realism`
  trigger first, no tag stacking) · **CLEAN negative = "duplicate character, multiple people,
  watermark, logo, deformed face, bad eyes, extra fingers"** (NO skin/AI-look terms — they make mud)
  · 8 steps euler/simple cfg 1 · 2MP 16:9 · explicit seeds.
- **Beard spec UPDATE (user, 2026-10-18):** Zidane = **full short beard, neatly trimmed & shaped**
  (replaces "thin patchy beard"). Jaisal = small patchy beard (unchanged).
- **Outputs:** `refset_v7\zidane_clean8` (recommended) + `refset_v7\zidane_clean16` (alt face).
- **Status:** Active recipe. 01's stock negative is superseded for character t2i (keep a backup copy
  of the old negative string in this entry: "plastic, waxy skin, airbrushed, smooth skin, AI look,
  rendered, CGI, 3d render, cartoon, illustration, duplicate character, multiple people, watermark,
  logo, deformed face, bad eyes, extra fingers, bulky body, muscular, beard, stubble, full beard").

## D141 — CHARACTER PIPELINE PIVOT: identity-edit DROPPED for char-refs (2026-10-18, user call)
- **User:** identity-edit outputs "pretty much off" (waxy/long faces) — "let's get rid of that and get a normal picture";
  frustration that simple items are tiring "because we don't have a proven workflow/pipeline yet".
- **Decision:** NO more identity-edit for character refs/sheets. The **t2i path is the proven one**
  (v6 sheets = pure t2i, user-approved). New pipeline:
  1. **Normal t2i pictures** (01, v6 recipe: Krea2Realism_V1 + V2 LoRA @1.0, kr2realism trigger, 8 steps,
     2MP, explicit seeds, clean neutral bg, "NOT elongated", warm-skin positive, D140 negative rules).
  2. **Character sheet** (H3 2BZ 2-stage, P3 route — see D138/CHARACTER_SHEET.md) from the approved t2i face.
  3. **LoRA training dataset** — the consistent set (sheets + t2i pics).
  4. **Train the character LoRA** — the LoRA itself becomes the face-lock for all future refs/sheets/frames.
     No identity-edit machinery.
- **Status:** Active. 02 identity-edit stays available ONLY for scene edits the user explicitly asks for,
  with the D140 recipe.
- **Outputs so far (t2i, no identity edit):** `refset_v7\jaisal_t2i_base_00001` (Jaisal seed 42, clean bg,
  natural face) + `refset_v7\zidane_t2i_base_00001` (Zidane seed 77).

## D140 — 02 identity-edit scene-ref recipe locked (2026-10-18, A/B-proven)
- **Problem:** bench-pair faces "wood/waxy, no skin tone" (same as v3/v5). Root cause: ref_boost
  4.0 clones the REF's face RENDERING (the sheet's flat even-lit pale face) into the scene — the
  anchored face region doesn't receive scene light — AND the anti-smooth-skin negative fights the
  anchor → desaturated muddy mid-state. Repeat of D025 (neutral ref → studio-lit face).
- **A/B (Zidane bench, seed 77, same seed all):** b40 = wood; **b25 = natural warm skin, identity
  tight (WINNER)**; b20 = natural but identity slightly looser.
- **LOCKED settings for 02 scene refs:** `ref_boost` **2.5** (not 4.0) · **warm scene light in the
  instruction** (golden hour) · **NO anti-smooth-skin negatives** (negative = identity-safety only:
  "stick figure, duplicate character, multiple people, watermark, logo") · **warm-skin positive**
  ("warm natural skin tone with visible pores and a subtle flush") · g768 · 10 steps euler/simple
  cfg 1 · 2MP.
- **Outputs:** `refset_v6\zidane_bench_b25_00001_.png` + `refset_v6\jaisal_bench_golden_00001_.png`
  (golden-hour bench pair, natural skin).
- **Status:** Active recipe. If a face still reads flat: warm the REF itself or use two-image mode
  (scene base + sheet as PERSON ref).

## D139 — DSH + GHCP (GitHub Copilot / VS Code agent) cross-client collaboration verified (2026-10-18)
- **Milestone (user-approved "we did good"):** the two agent clients worked as one pipeline —
  GHCP (VS Code agent) diagnosed DSH's Reddit gap, built `utilities\reddit_browser_fetch.py`
  (Playwright Chromium + persistent profile), and documented it; DSH then took the helper,
  ran it on all 5 posts headless (no session), fixed its `is_gated` false-positive, added
  `extract_reddit_text.py`, and folded all post bodies into `CHARACTER_SHEET.md`. User
  confirmed the collaboration worked well.
- **Persistent pattern (how to work across clients):**
  - Agents can build tools FOR each other: a helper committed to `utilities/` is immediately
    usable by the other client via its shell. The git repo is the hand-off channel.
  - **DSH can now fetch JS-gated pages itself** (Reddit et al.) via the shell-callable helper —
    no session/cookies needed for public posts. DSH's built-in web fetch stays for the open
    web (text-only is fine there).
  - **Verification discipline worked:** each client's claims were independently re-verified
    (DSH re-ran the helper 5/5; the "reCAPTCHA tier" verdict from both clients turned out to
    be a shared false positive — the bare `recaptcha` shell script tag).
- **Status:** Active pattern — reuse for any future JS-gated fetch need (civitai, HF gated
  pages, etc.).
