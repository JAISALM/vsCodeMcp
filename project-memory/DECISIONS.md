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

## D144 — Character-sheet A/B/C test + team-kit identity (2026-10-18, user-directed)
- **Decision:** the character-sheet step is a **3-route test** ("which is the best, so lets try
  ABC testing"): **A = P3 2BZ H3 2-stage (MiniMax)** (confirmed as the MiniMax route) ·
  **B = P5 LEEBLAAB Qwen Image 2.1** (7-zone design-sheet layout, 30 steps, bf16 UNET) ·
  **C = Krea2 t2i 3-view strip** (D142 recipe, 8 steps). User then approves the winning route
  before dataset runs.
- **KIT IDENTITY (same message):** both characters wear a **soccer jersey + track pants** team
  kit. **Jaisal = royal blue, Zidane = dark green** (different colors = "same team, different
  years" continuity). Crest = **white clenched-fist roundel with PALESTINE RESISTANCE
  wordmark** on the left chest; **player's name in white on the jersey back**; single white
  side stripe on the track pants. Kit refs = Krea2 t2i flat-lays (`input\{jaisal,zidane}_kit_ref.png`,
  `07_kit_ref_*.json`) — both rendered the crest + text legibly on first try.
- **Route notes:** A needs the 2BZ stage-2-only nodes removed for stage-1-only runs (111
  frontend muter / 125+126 PreviewImage / 127 CustomCombo) and the character master prompt
  must ride in **node 24's text** (H3 prompt slot is linked from 24 — the node's own prompt
  widget is ignored). B's model names must be patched on the **subgraph internal nodes**
  (451/453/454), not the instance widgets; models `qwen_image_2.1_bf16` (13.25GB) +
  `qwen3vl_8b_int8_convrot` (8.71GB) + `qwen_image_2.1_vae_bf16` (0.63GB) copied
  main-tree→latest-tree.
- **Status:** DONE — all 6 runs + A-jaisal retry complete. **C (Krea2) = 2/2 excellent sheets;
  A (H3) = 1.5/2 (no seed = stochastic, 15 min/run); B (Qwen 2.1) = 0/2 (prompt truncation at
  1024 tokens → layout lost).** Awaiting user's route pick (agent recommendation: C).

## D145 — Crest spec v2: fist roundel ONLY, no text (2026-10-18, user-directed — supersedes D144 crest)
- **User:** "the jersey should have the crest with logo only, we dont need palestine resistance
  in the logo, lets not make it obvious, but i want to have the emblem showing solidarity with
  them" → the chest emblem is a **white clenched-fist roundel ONLY** (thin circle, line-art fist,
  subtle) — **NO "PALESTINE RESISTANCE" wordmark, no slogan, no letters of any kind**.
- **Prompts:** all sheet/kit prompts updated (A master + detail_description, B TEAM row →
  "SOLIDARITY" + CREST MACRO "(no text)", C prompt) and NEGATIVES add "words, letters, slogan".
  Builders: `utilities\make_kit_ref_workflows.py` + `make_abc_sheet_variants.py`.
- **Kit refs regenerated:** 07_kit_ref_{jaisal,zidane} (seeds 13/29, prefixes `_00002`) →
  `input\{jaisal,zidane}_kit_ref.png` (overwrote old text-crest refs) — both verified first-try.
- **Status:** Active. The old "PALESTINE RESISTANCE" wordmark spec is DEPRECATED.
- **v3 update (2026-10-19, user, after colored logo v1):** "keep it as white fillers instead
  of colors, add black lines separating each color" → crest v3 = **MONOCHROME**: fist +
  forearm in SOLID WHITE FILL with clean black outline, NO colors (no red knuckles, no
  green/white/black stripes); thin BLACK SEPARATOR LINES where colored zones were (knuckle
  lines separating all 4 fingers + thumb; two horizontal lines dividing each forearm into 3
  zones). Source = user's 3-fist poster (`input\palestine_fist_ref.jpg`) for SHAPES/LAYOUT
  only. Two designs in comparison: (A) 3-fist emblem, (B) single fist in thin white circle
  (roundel) — royal blue background, no text. `logo_fists_compare.json` (4 branches: H3
  ref-based + Qwen 2.1 i2i). Status: awaiting user's run + pick.

## D146 — H3 sheet anti-plastic recipe: no turbo, no Spectrum, 30-step vanilla (2026-10-18, user-shared thread)
- **User:** "all of them looks plastic like — check this post [1wzcu5v]" (the H3 plastic-look
  thread) + the LBH-123-AI/Comfyui_Minimax_h3_latent_Upscaler repo link.
- **Thread findings (saved `data\h3_plastic_look`):** top answer = 2-pass latent upscale
  (half-res 20 steps no turbo → turbo 8-step @4 steps 0.35 denoise); 0.98 MP = H3's trained
  default res; **strong counter (lavinia12345): "latent upscale is shit... vanilla minimax
  model 30 steps, er_sde/beta57, 1 MP is good. Any use of lightning/turbo LoRAs, the Spectrum
  node, or PlagueKind's SLA node screw up eyes (even more)"**; turbo LoRA needs the H3 AdaLN
  LoRA Fix (`h3_silu_turb_grid` + PlagueKind node) at strength 0.70–0.85 if ever used.
- **Decision for our H3 sheet routes:** the wide variant (05d) runs **vanilla 30 steps,
  er_sde + beta scheduler, NO turbo/lightning LoRA, NO Spectrum node** (turbo + Spectrum
  DELETED from the civitai/cgpixel23 base). LBH latent upscaler pack (already installed) +
  3D bf16 model downloaded (`models\latent_upscale_models\minimax_h3_latent_upscaler_3d_conv_v1_bf16.safetensors`)
  kept as an optional 2nd-pass refinement — NOT in the main chain yet.
- **Status:** Active for the 05d wide variant; re-evaluate after user sees the outputs.

## D147 — New sheet routes from user downloads (2026-10-18): cgpixel23 wide H3 + Qwen-2.1-LLM-architect
- **User drag-dropped** `E:\minimax_workflow\character_sheet\1CJX8DERQKDMG6Z2C5QC4D6HW0.png`
  (civitai post 31291351 image, 4096×1536) — civitai embeds the FULL workflow as plain-text
  `workflow`/`prompt` tEXt chunks (NOT base64; `utilities\parse_new_user_downloads.py`
  extracts). The embedded = cgpixel23's wide multi-panel H3 sheet (sprite-sheet layout:
  portrait closeup + 3-angle full-body + 6 detail circles). **Adapted → `05d_charsheet_H3_wide_{char}.json`**
  (our 2 refs, author's test/NSFW/style LoRAs stripped, D146 anti-plastic chain, t1 image VAE,
  4096×1536, R2V 6-section sheet prompt).
- **User downloaded** `E:\minimax_workflow\character_sheet\Qwen Image 2.1 Character Design
  Sheet.json` — **LLM-architect design**: `ThinkingLLM_QwenVL_GGUF_Advanced` (local GGUF
  `Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf`, temp 0.95, system prompt "Character Sheet Prompt
  Architect", `{{name}}` StringReplace) writes the sheet prompt at runtime → explains the
  author's working 12K-char sheets that defeated our static LEEBLAAB prompt (B-route 0/2).
- **Pack installed:** `custom_nodes\ComfyUI-ThinkingLLM` (goodguy1963 v2.5.8 — GGUF variant
  + HF-weights variant `ThinkingLLM_QwenVL(_Advanced)`; deps mostly present, missing =
  llama_cpp GGUF wheel + tiktoken). PE-I2I GGUF models downloading
  (`ComfyUI\LLM\GGUF\`, HF `prithivMLmods/Qwen-Image-2.1-PE-I2I-GGUF`). **Server restart
  pending** to load the pack; workflow adaptation (our refs/chars) after restart.
- **Status:** 05d wide variant queued for the first test run; Qwen-LLM-architect route =
  NEXT after the server restart.

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

## D143 (REVISED 2026-10-20) — Character LoRA target = **KREA 2** (was "Klein-9B DENSE"), stack with `Krea2-realism-V2`
- **User correction (turn 76):** "our lora target is to create lora for krea2 ... we should be able to
  combine our lora with krea2 realism lora or checkpoint, thats the whole point, otherwise i dont
  think we will be able to achieve consistency / good image generations. flux 9b also fine, but we
  often get plastic look there ... even on our dataset image i have the same issue ... to the
  limit we can get realism with krea lora."
- **Decision:** train BOTH character LoRAs on **Krea 2** (the Krea2Realism_V1 chain). At
  generation: char LoRA + `Krea2-realism-V2`@1.0 stacked = identity + realism.
- **Dataset reality:** the 40 dataset images (20 zidane + 20 jaisal, same pose/type) were
  generated on the **Klein-9B** dataset workflow — they carry some of Klein's plastic look.
  User ACCEPTS the limit: Krea2 base training pulls the LoRA back toward natural skin.
  Optional later: regenerate some dataset shots on the Krea2 chain.

## D173 — Hard-test verdict + production-quality model + movie-consistency architecture (2026-10-23)
- **Hard test (turbo) verdict (19:30):** identity HELD 6-7/8 hard cases (profile,
  low-angle, full-body sprint, crowd, both characters present as distinct men) —
  triggers `jeskvman`/`dlorman` are PRODUCTION-SOLID for identity. Failures:
  extreme close-up face drift (eyebrows wrong); 2-person action not performed.
  Overall quality SOFT — ROOT CAUSE: everything ran on the TURBO unet
  (`krea2_turbo_fp8_scaled`, 10 steps, cfg 1) = a speed model.
- **User's verdict: "output quality too low, not even usable"** (for the film).
  **Film release = Nov 22 (~30 days).**
- **Quality lever (on disk, unused):** `krea2_raw_bf16.safetensors` = production
  Krea2. Documented settings (workflow note in `krea2_identity_edit.json`):
  **40 steps, cfg 3-4, negatives matter**. Built `krea2_raw_qtest.json`
  (MCP-validated): same chain, raw unet, 40 steps, cfg 3.5, existing negative,
  3 identical hard prompts → direct turbo-vs-raw comparison, prefix
  `krea2_raw_qtest`.
- **Decision: movie consistency = REFERENCE-DRIVEN chain, not text+LoRA** —
  (0) finalize Jaisal v2 face (D172) + Zidhan final (locked) → (1) per-character
  ANCHOR SET (frontal/3-4/profile/close-up/2 expressions) at RAW quality,
  identity-edit locked (ref_boost 4.0, D023) → (2) 2-3 refs per movie shot via
  identity edit (D021) → (3) MiniMax H3 R2V 2-3 refs + short prompts, NO music
  (D020/D041) → (4) SFX-only audio + assembly. The video inherits faces from the
  reference images — that IS the consistency mechanism for the film.
- **LoRA retrain — see D175:** originally demoted here; PROMOTED by D175 (retrain
  character LoRAs on the RAW base — the official Krea workflow). Dataset =
  anchor set with angle/expression/framing variety (phosphene.cc methodology),
  not frontals only.
- **Timeline (Nov 22):** face decision today → anchor set day 2-4 → per-shot ref
  set day 5-10 → R2V video week 3 → SFX/assembly week 4 → buffer.

## D174 — Big-screen quality bar + Qwen-Image-2.1 as production-stills engine (2026-10-23)
- **User's bar:** Krea2 outputs are "pastey, no skin texture, no realism — nothing
  felt real"; face-similarity alone is NOT a reason to accept them. Film must
  survive BIG-SCREEN display.
- **Diagnosis:** Krea2 (turbo AND raw) is a fast/stylized model — its documented
  aesthetic is the brush-stroke/painterly look (D021). That is an ENGINE ceiling,
  not a prompt or LoRA problem: no prompting gives Krea2 real skin texture.
- **Decision: production stills engine = Qwen-Image-2.1.** All on disk: UNET
  `qwen_image_2.1_bf16` + VAE `qwen_image_2.1_vae_bf16` + CLIP
  `qwen3vl_8b_fp8_scaled` (loader type `qwen_image`). Proven settings from the
  09j subgraph: **25 steps, cfg 1, euler, simple**. Already wired in
  `09j_QWEN21_JAISAL_sheet` + `09k_QWEN21_ZIDANE_sheet`. Bonus on disk:
  `qwen_image_edit_2511_bf16` + `qwen-image-edit-2511-multiple-angles-lora`
  (multi-angle edit LoRA).
- **Built `qwen21_face_test.json`** (MCP-validated 0 errors; 2 benign warnings =
  the standard img2img IMAGE→latent conversion): 2-branch i2i from the locked
  face frontals (copied to `input\` as `jaisal_face_frontal.png` /
  `zidane_face_frontal.png`), denoise 0.55, 25 steps cfg 1, photorealistic
  monsoon-street prompt + anti-painterly negative. Prefixes
  `qwen21_face_{JAISAL,ZIDANE}`. USER TO RUN TODAY — the side-by-side skin-texture
  verdict vs the Krea2 outputs.
- **Role split:** Krea2 = iteration/concept engine (fast, cheap, style);
  Qwen-Image-2.1 = production stills (anchor set + per-shot reference set that
  R2V animates). All identity work (faces, descriptions, triggers, scenes, R2V
  pipeline, NO-music rule) transfers unchanged — only the stills renderer swaps.
- **If the face doesn't hold on Qwen i2i:** (a) character LoRA on the
  Qwen-Image base (Fizgig) trained on the anchor set — the LoRA-retrain effort
  now belongs HERE, not on Krea2; (b) the multiple-angles edit LoRA already on
  disk; (c) a PuLID/IP-Adapter-style identity pack.
- **Timeline unchanged (Nov 22)** — the engine swap is a same-day decision, not a
  restart.

## D175 — Krea2 STAYS the production engine; fix = RAW-based LoRA + RAW generation (2026-10-23)
- **User's call (19:5x IST):** "Krea2 is the best model we have for realism —
  check any forums... I don't know how we're ditching it blindly because of a
  skill issue." → **Krea2 is NOT ditched.** D174's Qwen-Image-2.1 pivot is
  demoted to fallback/comparison only.
- **Official backing (krea.ai/krea-2-open-source):** Krea 2 = "the most
  aesthetic open-source image model available"; official pairing: **Turbo for
  fast polished t2i, RAW as the malleable base for LoRA training — "Train LoRAs
  on RAW, then run them fast on Turbo."** Community reviews agree (buildfastwithai:
  "Train your LoRA on Krea 2 Raw — the undistilled base gives your fine-tuning
  room to move"; Raw/Turbo designed to work together, LoRA transfer between them).
- **Root cause of the "pastey, no skin texture" outputs = USAGE, not the model:**
  everything ran on `krea2_turbo_fp8` at 10 steps / cfg 1 (the fast lane), and
  the character LoRAs (`krea2fp_*`) were trained on the TURBO fp8 base — Krea's
  official workflow trains character LoRAs on RAW.
- **Fix (quality path):** (1) RETRAIN character LoRAs on `krea2_raw_bf16`
  (Fizgig) — the user's retrain wish is now the OFFICIAL recommendation; dataset
  = anchor set with angle/expression/framing variety (D173 methodology).
  (2) Production generation on RAW: **40 steps, cfg 3-4, real negatives**
  (settings already documented in our workflow notes). Turbo stays as the fast
  iteration lane (RAW-trained LoRA transfers to it).
- **Evidence today:** `krea2_raw_qtest.json` (same chain, RAW UNet, 40 steps,
  cfg 3.5, existing negative, 3 identical hard prompts) — user to run; also
  shows whether the existing turbo-trained LoRA still binds on RAW.
  `qwen21_face_test.json` kept as fallback comparison only.
- **Unchanged:** Jaisal v2 face decision (D172, still awaiting user confirm),
  reference-driven movie chain (D173), Nov 22 timeline.

## D176 — Krea2 cinematic recipe: film-still prompts + 16:9 + Turbo (2026-10-23)
- **User: "the test you gave me [was] stupid low quality... just check forums
  how to get good cinematic shots in krea2."** raw_qtest outputs graded: the
  close-up DID gain real skin texture on RAW ✓; profile + two-man came out as
  flat phone-photo looks.
- **Findings (Krea official prompting doc via the ComfyUI-Prompt-Studio guide;
  Andro-Meta local-studio guide; Krea2SizePreset tiers):**
  1. Krea2 prompting = natural-language grapher briefs; quality tags
     (masterpiece/8k) waste prompt budget; "cinematic" alone does little —
     name the MEDIUM early (35mm film, lens mm, DOF, light
     source/quality/temperature, grain, color grade).
  2. AGENT SKILL GAP (admitted): previous prompts said "candid phone
     snapshot... NOT a studio portrait" — actively anti-cinematic.
  3. Resolution: default tier 1K (1120×896 near-square); cinematic = 16:9 at
     1.5K (1920×1080) / 2K tiers.
  4. Official Turbo vs RAW: Turbo = polished OUTPUT checkpoint (8 steps,
     cfg 0.0, Mu 1.15, fp8); RAW = training/LoRA/research base. The
     raw_qtest 40-step/cfg-3.5 run was an untested mush setting — wrong tool.
- **Built `krea2_cine_test.json`** (validated 0/0): Turbo UNET, 10 steps cfg 1
  (proven identity settings), **1920×1080**, same 3 LoRAs, 3 prompts rewritten
  as film-still briefs (medium+lens+lighting+mood+grain+grade). If still soft →
  next lever: Krea-specific Mu=1.15 sampler param (stock KSampler doesn't
  expose it — needs a Krea sampler node) + reference-image style transfer.

## D177 — Official Krea2 sampling settings + missing ModelSamplingFlux node (2026-10-23)
- **User: "something clearly wrong... the details are off" — asked for the full
  workflow spec to post on Reddit.**
- **Official Krea 2 repo (github.com/krea-ai/krea-2 README, verified):**
  - **Turbo: 8 steps, CFG 0.0 (guidance disabled), mu 1.15 (timestep shift),
    1K–2K resolution** (official example 2048×2048).
  - **RAW: 52 steps, cfg 3.5, up to 1K** ("full sampler with classifier-free
    guidance").
  - "TRAIN on Raw and RUN on Turbo" (re-confirmed).
- **ComfyUI detail (comfy.icu Krea2KSampler):** "Krea2 shares the exact same
  **ModelSamplingFlux / shift=1.15** setup as Qwen-Image and the rest of the
  Flux family" — in ComfyUI the mu shift is applied with a
  `ModelSamplingFlux` node (shift 1.15), which was **MISSING from our chain**
  (stock KSampler euler+simple only) → TOP suspect for pasty/detail-less
  outputs.
- **Actual chain (verified from links):** `55 UNETLoader
  (krea2_turbo_fp8_scaled) → 303 krea2fp_v2_ep64@1.0 → 96 Krea2-realism-V2@1.0
  → 97 famegrid_spicy_3167060@0.7 → 53 KSampler → 54 VAEDecode
  (qwen_image_vae) → 302 FameGridColorFinish(1.0/0.6) → 29 SaveImage`; CLIP
  `qwen3vl_4b_fp8_scaled` type `krea2` → 300/301 CLIPTextEncode (200
  PixaromaPromptEach → 300); 82 EmptySD3LatentImage.
- **Built `krea2_mu_test.json`** (validated 0/0): same chain + **node 58
  ModelSamplingFlux(shift 1.15)** between 97 and 53, KSampler at official turbo
  settings **8 steps, cfg 0**, 1920×1080. Paste file
  `mu_test_3_prompts_paste.txt`. USER TO RUN — the decisive test of the
  missing-shift hypothesis.
- **Open:** if mu_test still soft → try bf16 turbo (fp8 quality check) and/or a
  Krea two-stage sampler pack.

## D178 — mu_test run forensics: prompts never reached the model (2026-10-23)
- **User ran `krea2_mu_test` → 3 outputs BYTE-IDENTICAL (same sha256), content
  = 3-panel face-grid (East-Asian woman, white bg) — NOT the prompted content.**
- **Forensics:** byte-identical outputs are impossible if the 3 different
  prompts + randomized seeds were applied → the run used the SAME (empty) text
  + fixed seed for all 3 items. The prompts WERE on disk (file verified intact:
  state blob + link 200→300 present) → the UI ran the CANVAS state, which was
  EMPTY (the known Pixaroma clobber/cached-canvas quirk — user's "issue with
  pixaroma group" was right all along).
- **Face-grid content = the `famegrid_spicy_3167060` LoRA prior dominating with
  no prompt** (empty text + cfg 0 → LoRA prior drives composition). Lesson: a
  3-panel face-grid LoRA at 0.7 is a strong contaminant for single-subject
  cinematic shots.
- **Decision: kill the hidden-state path for diagnostics.** Built
  `krea2_control_test.json` (validated 0/0) with **NO prompteach** — prompt
  text sits DIRECTLY in the CLIPTextEncode widgets (always visible, always
  applied, nothing to paste). Two branches, one queue, seed 42 fixed,
  1920×1080, official turbo settings (8 steps, cfg 0, ModelSamplingFlux 1.15):
  - A `krea2_bare_A`: bare engine — zero LoRAs (pure control).
  - B `krea2_lora_B`: engine + character LoRA `krea2fp_v2_ep64` ONLY (no
    realism, no famegrid).
- **Interpretation matrix:** A good → engine+official sampling proven, pasty
  outputs = our 3-LoRA stack (famegrid first suspect); A soft → fp8-turbo
  ComfyUI path is the ceiling → bf16 test + Reddit. B face holds → character
  LoRA alone carries identity.
- **Rule change:** diagnostic/control tests NEVER use prompteach — direct
  CLIPTextEncode widgets only. prompteach only for batch runs where the user
  confirms the rows are visible in the node before queueing.

## D172 — Fair test round 2 verdict + face-similarity problem + re-scope plan (2026-10-23)
- **Fair test round 2 (balanced 3/3/2) — 8/8 HELD:** Jaisal 3/3 (backwater path /
  houseboat / auto-rickshaw), Zidhan 3/3 (same 3 scenes), combined 2/2 (rainy
  street + backwater path) — BOTH combined shots showed two clearly distinct men
  (round 1's combined collapse did not repeat). `jeskvman`/`dlorman` triggers
  are solid. Jaisal's patchy beard renders faint (stubble-ish) in the solos.
- **User's call (confirmed from the 8 images):** the two faces are TOO SIMILAR —
  "same guy with different haircuts"; only hair/beard/tee differ, no facial
  feature difference. For two movie leads that is a real problem.
- **DECISION: re-scope Jaisal's face** — create Jaisal with clearly DIFFERENT
  facial features (proposed: LONGER OVAL face, leaner cheeks, more defined
  angular jaw, thicker straighter eyebrows, narrower straighter nose, slightly
  deeper-set eyes — vs Zidhan's round full-cheeked soft-jawed face); KEEP wavy
  hair + patchy beard + dark tee + Malayali skin. User confirms features → new
  face-lock → new dataset → **LoRA retrain** (user trains).
- **BEFORE retraining: hard stress-test the CURRENT LoRA `krea2fp_v2_ep64`**
  (user's order — "get actual results, see what to change in the next LoRA"):
  8 hard prompts (extreme angles, close-up, full-body action, crowd, night,
  2-person action) with COMPACT identity descriptions so the LoRA — not a long
  prompt — must carry the identity. Methodology from web (phosphene.cc
  acceptance test: "recognizable without reading the prompt? do locked traits
  survive expression/angle/framing changes?"; "the dataset is the product";
  captions must name identity markers and describe backgrounds as context).
  Files: `utilities\hard_test_prompts.json` +
  `utilities\hard_test_8_prompts_paste.txt` (8 prompts, one per line).
- **Open hypothesis:** face merging between the two characters may come from ONE
  combined LoRA carrying both faces → if the hard test shows drift/merge, the
  next LoRA may need to be TWO single-character LoRAs instead of one combined.

## D171 — Character finals LOCKED (2026-10-23): Jaisal = `FACEFRONTAL_JAISAL_b_00001_`, Zidhan = `FACEFRONTAL2_ZIDANE_c_00012_`
- **Supersedes** D137's char2 description (loose top bun + white tee — DEPRECATED,
  never prompt it) and the old `krea2_char{1,2}_face_*` set as identity authority.
- **Jaisal final:** `FACEFRONTAL_JAISAL_b_00001_.png` (generator workflow
  `10a_frontal_base_jaisal.json`). **Zidhan final:**
  `FACEFRONTAL2_ZIDANE_c_00012_.png` (generator workflow
  `10a_frontal_base_zidane.json`). Both in ComfyUI output dir.
- **Zidhan face:** buzz cut/fade ("halal" haircut — very short faded sides/back,
  short neat crop on top, no waves, no bun) + full short dense beard + white tee.
- **Handy doc:** `d:\models\vsCodeMcp\docs\CHARACTERS.md` — finals table,
  verified descriptions, VERBATIM face-frontal prompts + negatives (picked from
  the generator workflows), ready-to-use scene templates with triggers
  (`jeskvman`/`dlorman` first), and the combined 2-person FAIR TEST prompt.
- **Consequence:** the `D:\lora_training\zidane` dataset (buzz+beard face) MATCHES
  the final — dataset is FINE, no face regeneration. `krea2fp_v2` LoRA's `dlor`
  identity (e64 preview = buzz+beard) is the CORRECT Zidhan.
- **Prompt rule:** triggers first (`jeskvman`/`dlorman`), description second.
  NEVER "top bun / topknot" for Zidhan; NEVER "bun / topknot" for Jaisal (hair
  DOWN). UI prompt edits must be SAVED so file = what runs.
- **Fair test agreed:** jaisal + zidane in the SAME picture (combined prompt, both
  triggers + descriptions, side by side).
- **Workflow-file lesson:** ComfyUI UI state is what runs; the on-disk workflow file
  can be stale if the user edits prompts in the UI without saving. Verify the actual
  prompts before claiming what ran; ask the user to SAVE the workflow after UI edits.

## D170 — Fizgig GUI is agent-controlled via its REST API — "you click, I verify" (2026-10-21)
- **Decision:** the Fizgig web app (127.0.0.1:8081) exposes a full REST API; the
  agent drives/verifies the GUI state directly instead of screen-sharing (no live
  video; screenshots on "look" via PowerShell → read_image).
- **Mechanics:** token in the served page's `<meta name="fizgig-token">` (per
  session; re-extract after app restart); header `X-Fizgig-Token` on every
  `/api/*` call. `GET/POST /api/prefs` (model paths via `changes` dict),
  `GET/POST /api/state` (family, image_folder, per-family `model_values`),
  plus ~150 more routes (`/api/runs`, `/api/queue`, `/api/captions/*`,
  `/api/studio/*`) — source `D:\tools\Fizgig\src\fizgig\web\server.py`.
- **Done:** all 5 Krea 2 model paths written + verified (shared library), family
  → `krea2`, image_folder → `D:\lora_training\jaisal`.
- **Reason:** user asked for screen-sharing/agent help in the Fizgig GUI ("no
  agent in Fizgig"); the API closes that gap exactly — every field the GUI shows
  is readable/writable, so the user clicks and the agent confirms in real time.
- **Status:** active — in use for the Krea 2 dual-subject training run.

## D169 — LTX-2.5 VFX pipeline tracked in its own doc; weekly watch on (2026-10-21)
- **Doc:** `docs\VFX_PIPELINE_LTX25.md` — the Lightricks LTX-2.5 IC-LoRA "VFX week"
  (HF-verified timeline 2026-09-08→09-28: Day-To-Night, Water-Sim, Clean-Plate, Deblur,
  Colorization, Decompression, Ingredients, Layout-To-Render, Refine-Details, Restore,
  SDR-To-HDR + scene-emb, Alpha-Gen; X account @ltx_io for posts).
- **Our base stack is ALL LOCAL** (distilled DiT int8, gemma4-12b encoder, VAEs, latent
  upscaler; SDR→HDR + Alpha-Gen LoRAs already in loras/). **Only ~625 MB missing** for
  the core three: `sdr-to-hdr-scene-emb` (12.6 MB — completes the HDR pair),
  `clean-plate-1.0` (306 MB), `day-to-night-0.9` (306 MB) — download when the movie
  post stage starts.
- **Movie mapping:** Clean-Plate = background removal/compositing · Day-to-Night =
  moody night shots (D024 climate) · SDR→HDR = gradeable deliverables · Alpha-Gen =
  character mattes · Refine-Details = clarity pass · Layout-to-Render = storyboard →
  shot · Native Resolution = 4K/8K Tiled Fusion (single-GPU, test on the 5090 first).
- **ComfyUI gap:** `ComfyUI-LTXVideo` pack exists in the MAIN tree only — install into
  the running install + restart before any LTX VFX workflow runs.
- **"Background text addition" LoRA** (user's memory): NOT in the official org — closest
  = `Ingredients`; possibly community (ltx.io/ltx-community).
- **Monitoring:** weekly schedule (Mondays 09:00 IST) diffs the Lightricks HF org
  against the doc + watches X posts.
- **Status:** Active. Audio rule D041 applies to all LTX outputs (silent V2V; H3-native
  audio only).

## D168 — Model library audit + 261 GB archive to `F:\models_bkp`; LTX/H3/ditto UNTOUCHED (2026-10-21, user-confirmed)
- **Context:** E: models drive ~38 GB free; Krea 2 RAW DiT (25.9 GB) downloading in
  parallel (Fizgig GUI) → user: move unwanted models to `F:\models_bkp`, **confirm
  before moving, don't delete junk during the download**.
- **Method:** all 194 files in `E:\ComfyUI_windows_portable\ComfyUI\models` (817.9 GB)
  cross-referenced against all 63 workflow JSONs (both trees).
- **MOVED (80 files, ≈ 261 GB, background job pwsh-140, script
  `utilities\move_models_to_bkp.py`, structure preserved = recoverable):** Wan family
  (114.8 GB) · umt5/FLUX.1 encoders (41.7 — verified: klein workflows use
  `qwen_3_8b_fp8mixed`, umt5 = old FLUX.1 arch, zero references) · Qwen 2511/2512 gen
  (64.0 — user: "may need in future, pull from the drive when needed" — pull-back
  recipe in the doc) · SDXL + orphaned controlnets (16.05) · redundant encoders
  (16.9 — `qwen3vl_4b_bf16` redundant with in-use fp8_scaled; `qwen_3_4b` zero refs) ·
  small unused misc (14.3).
- **KEPT:** whole LTX family (~131 GB — D169's VFX tools), all H3 + H3-adjacent
  (~145 GB — movie stage is next), ditto (18.3 GB — style-variant workflow), the
  edit-2511 chain (`qwen_image_edit_2511_bf16` + Lightning + multiple-angles +
  `qwen_2.5_vl_7b` pair — `QWEN_click_multiple_character_angles`), `ae.safetensors`,
  the `.crdownload` junk (1.63 GB — no deletions this pass), ace_step (7.70),
  krea2_darkbrush/lineart + bfs_head + klein-consistency LoRAs (small, user's call).
- **Docs:** `docs\MODEL_INVENTORY.md` (full keep/moved/untouched lists with workflow
  references + pull-back procedure).
- **Status: DONE + VERIFIED (2026-10-21 11:14 IST).** Job `pwsh-140` PASSED —
  80/80 files at `F:\models_bkp` with matching byte sizes, all 80 sources gone,
  0 bad. **E: = 256.3 GB free** (was ~38 GB). `F:\models_bkp` also carries the
  user's earlier archives (`wan_model` 300.5 GB, `ltx` 97.6 GB, `qwe_2512`
  38.1 GB) — no filename collisions, nothing overwritten. Krea 2 RAW DiT
  (24.5 GB) landed in the shared `diffusion_models\` at 11:00 IST.
- **LTX VFX armour (same turn):** `ComfyUI-LTXVideo` pack copied into the running
  install + `ninja` pip-installed → activates on next restart. 4-5 VFX IC-LoRAs
  queued for user download (see `docs\VFX_PIPELINE_LTX25.md`).

## D167 — LoRA TOOLS: Fizgig PRIMARY (Krea2 + LoRA Isolation), AI Toolkit SECONDARY; both installed ("keep both in our armour") (2026-10-20)
- **Fizgig** (`D:\tools\Fizgig`, venv Python 3.12, CUDA 12.8 torch — install job
  pwsh-106 2026-10-20): "LoRA & Fine-tune Studio" — native **Krea 2** support +
  **LoRA Isolation** (v8.4+): multi-subject training where each person's face stays on
  its own trigger — BUILT FOR OUR 2-CHARACTER MOVIE (Jaisal + Zidane in one frame).
  Tests on Krea 2: normal LoRA bleeds subject face onto 48/50 strangers; isolation =
  0/50, likeness unchanged (ArcFace 0.78 vs 0.77). Mechanics: (1) DOP (from Ostris
  AI-Toolkit — trigger-free pass pinned to base-model output), (2) multi-subject
  identity anchoring (each subject own folder + trigger; "even for a LoRA of one
  person, training a second person alongside them is recommended"), (3) fused-token
  class decoupling (`trigger, a man` → `triggerman` so the subject never attaches to
  the shared " man" token), (4-6) negative-pair training + other-people description
  safety net. Setup: Training tab → Subjects card → pick 2 subjects, folders, set
  "Your subject and other people" = **Fizgig LoRA Isolation**. Docs:
  `docs/lora-tools/fizgig_LORA_ISOLATION.md`, `fizgig_MULTI_PERSON.md` (captioning
  guide), setup video youtu.be/8uW5NdL5b20, demo youtu.be/CNh4sN5vN_8. GUI:
  `Launch Fizgig.bat` (own window) / `Launch Fizgig in browser.bat`.
- **AI Toolkit** — **ALREADY INSTALLED (user, turn 76): `E:\AI-Toolkit-Easy-Install\`
  (easy-install v0.4.1 by ivo/Tavris1)**: `AI-Toolkit\` repo + own `python_embeded\`
  (Python 3.12.10) + `Start-AI-Toolkit.bat` (UI → localhost:8675) +
  `Update-AI-Toolkit.bat`. Verified working: torch 2.8.0+cu128, CUDA on RTX 5090 ✓,
  `aitk_db.db` = used before. **BUT Feb-2026 build had NO Krea 2 support (656 commits
  behind)** → updated in place 2026-10-20 (job pwsh-118: git pull + pip install
  requirements with the embedded python; log `AI-Toolkit\update_log_20261020.txt`).
  The redundant fresh-clone attempt (`D:\tools\ai-toolkit`, job pwsh-107) was KILLED +
  deleted. Latest master supports **Krea 2 Raw/Turbo** (+Edit variants), FLUX.2/klein,
  SDXL. DOP single-subject, LoKr, layer-specific training. Secondary/fallback.
- **Better alternatives checked:** none for Krea 2 — kohya sd-scripts / diffusion-pipe
  don't support it. Fizgig is the only tool with multi-subject face isolation.
- **Reddit source:** r/StableDiffusion post 1x8aplh "Fizgig LoRA Isolation: a new
  process for more..." (2026-10-17) — the feature above; links = LORA_ISOLATION.md +
  setup/demo videos (captured).

## D166 — 09k sheet DONE (user: "character sheet is done, and thats good"); Klein dataset node error = MISSING comfyroll PACK (2026-10-20)
- **Zidane sheet approved** — 09k stage complete; dataset stage is next (Klein-9B).
- **Dataset workflow `1 Click Dataset (Klein 9b).json`:** validate reported exactly ONE
  error — node 377 `CR Prompt List` = `unknown_class_type` (closest: `easy promptList`,
  different node). Root cause: the node comes from the **`comfyroll` pack**
  (`properties.cnr_id: "comfyroll"`), which was **no longer in `custom_nodes`**
  (80 packs present, none matching) — the pack was wiped (likely the portable
  install refresh / Manager update). User: "CR prompt list was there, i remember this
  workflow was working previously".
- **Fix:** `mcp install_node(["comfyroll"])` failed (`pack_not_found` — the CLI's
  GitPython backend keys on a field the cached entry lacks: `project_name: None`).
  **WORKAROUND:** direct `git clone --depth 1 https://github.com/Suzie1/
  ComfyUI_Comfyroll_CustomNodes` into `custom_nodes\` (= what the registry's
  git-clone install does). Pack verified: `node_mappings.py` line 60 maps
  `"CR Prompt List": CR_PromptList` (from `nodes/nodes_list.py`); no
  `requirements.txt` (no extra deps). **RESTART PENDING** — the running ComfyUI
  was launched by the user's portable launcher, NOT comfy-cli, so MCP
  `restart_comfyui` fails (`no_background_server`) — the USER closes and re-opens
  ComfyUI. After restart: re-validate the workflow (expect 0/0), then run the
  dataset (20-prompt list is inside node 377's widgets; index widget picks the
  prompt; ref image `ref_woman.png` — for zidane, swap to the locked face).
- **Workflow graph (verified):** `flux-2-klein-9b.safetensors` UNET + `qwen_3_8b_fp8mixed`
  CLIP (type flux2) + `flux2-vae` — LoadImage ref → ImageScaleToTotalPixels →
  GetImageSize (drives EmptyFlux2LatentImage 768×1120 defaults + Flux2Scheduler
  [5,1024,1024]) → VAEEncode → 2× ReferenceLatent → **Flux2KleinRefLatentController
  [104.6, 0, none, 0.5, false]** → **Flux2KleinTextRefBalance [0.995, false]** →
  CFGGuider [1] + KSamplerSelect euler + SamplerCustomAdvanced + RandomNoise
  [385795140905191, fixed] → VAEDecode → SaveImage `Dataset\Test_woman\Image`.
  Node 377's `prompt` output (link 687) → CLIPTextEncode 351 slot 1.

## D165 — ZIDANE FACE LOCKED = `FACEFRONTAL2_ZIDANE_c_00012_.png`; sheet composite built + verified (2026-10-20)
- **User picked `FACEFRONTAL2_ZIDANE_c_00012_.png`** (from the v7 run series 00007-00012,
  1152×2048, 01 chain) as the LOCKED zidane face — roundish face, full dark beard,
  short halal cut, white tee, frontal half-smile. Staged as
  `input\zidane_portrait_front.png`.
- **User's root-cause hypothesis (consistent with all evidence):** the face
  convergence is the **LoRA** (`Krea2-realism-V2.safetensors` @1.0 on every chain) —
  "i tried different prompt altering few things and still getting similar result".
  Unverifiable from here (LoRA training data unknown), but if V2 carries a strong
  face/style prior, prompt tweaks only nudge attributes while the face stays
  anchored. Recorded as the working theory; the face is locked either way.
- **`11_sheet_composite.json` — the "combine multiple images into one" workflow**
  (user request). CORE nodes only (no custom packs): `EmptyImage` (white 2304×1536
  canvas) + 3× `LoadImage` (native shape) + 3× `ImageScale` (lanczos, slot sizes,
  crop center) + 3× `ImageCompositeMasked` (destination canvas, source at x/y,
  resize_source=False) + `SaveImage` `SHEET_COMPOSITE` (root). Layout = the 09j/09k
  spec: LEFT face full-height (width computed from aspect: 864 for 1152×2048),
  TOP-RIGHT 760² @ (1212,0), BOTTOM-RIGHT 760² @ (1212,776), 16px gaps. Builder
  `build_sheet_composite.py` (stages face into input, computes layout from actual
  face aspect). **Validate 0/0 (11 nodes) + ran clean (5.4s, CPU-only) →
  `SHEET_COMPOSITE_00001_.png` verified: face left, green roundel top-right, dark
  green kit bottom-right.**
- **Sheet composite staged:** `output\SHEET_COMPOSITE_00001_.png` →
  `input\zidane_sheet_ref_3panel.png` (2304×1536) — what 09k's node 470 LoadImage
  reads. **NEXT: user runs 09k (fresh tab) → `charsheet/QWEN21_ZIDANE_00001_` →
  verify green-ground roundel crest + dark green kit + locked face.**
- **Reuse:** for any character sheet — stage the three refs into `input/`
  (face/crest/kit), edit the three LoadImage filenames in the UI (or re-run the
  builder with new names), Run. `ImageCompositeMasked` x/y widgets move panels;
  `ImageScale` width/height change slot sizes. For a simple N-image STRIP
  (not the sheet layout), KJNodes `ImageConcatMulti` (inputcount + direction +
  match_image_size) does it in one node.

## D164 — ROOT CAUSE of "same man every time": fixed ADJACENT seeds + Jaisal-templated prompt; v7 = distant seeds + new description (2026-10-20)
- **User (turn 72):** "we cannot go with i2i ... it will drift the quality ... we have
  to find out the root cause of why this is not generating a new image and holding
  back". **i2i route is DEAD for face locking — no more i2i suggestions (quality
  drift, user's standing order).** D163's i2i workflow (`10a_frontal3_zidane_i2i.json`)
  stays on disk but is NOT to be run.
- **Root cause (two layers, both verified):**
  1. **Fixed ADJACENT seeds.** v6 set KSampler seeds to `fixed` 76/77/78 — three
     adjacent numbers, and 77 = the exact seed of the v4b run (00002). Same seed +
     same chain + similar prompt → near-identical image: that's why 00006 was "so
     identical to 00002/00001". The user's original suspicion ("are we doing it in
     same seed?") was CORRECT for v6. Adjacent seeds are a micro-variant patch of
     face space, not new faces.
  2. **Jaisal-templated prompt.** Every zidane prompt written so far is structurally
     Jaisal's prompt with attributes swapped (same opening, same feature list) — and
     the PROMPT DESCRIPTION anchors the face (evidence: Jaisal's randomize frontals =
     same man across different seeds). Reconstructed zidane prompts kept landing near
     Jaisal's face.
- **v7 (CURRENT):** `10a_frontal_base_zidane.json` — 01 home chain (8 steps,
  1152×2048) + a GENUINELY NEW description (face-shape-first: "His face is round and
  full-cheeked — wide, soft, with a short strong jaw…"; different opening/words from
  every previous attempt — Jaisal's template retired; kr2realism trigger kept) +
  **DISTANT seeds 250/777/4242 fixed** (far from 42/76/77/78 and each other) → three
  genuinely different men to pick from. Builder `build_10a_zidane.py` (clones 01 +
  branches). Validate 0/0 (16 nodes), wiring verified. Saves
  `FACEFRONTAL2_ZIDANE_{a,b,c}` (root, next counter `_00007_`). **USER RUNS**
  (fresh tab).
- **Rule for all future pick-sets:** never use adjacent seeds for a pick-set; use
  distant seeds (hundreds apart) so each branch is a genuinely different candidate.
  Never clone a sibling character's prompt template — write the description from
  scratch with the target face shape FIRST.

## D163 — t2i re-rolling is a DEAD END for the approved zidane face; i2i lock REJECTED by user (quality drift) — see D164 (2026-10-20)
- **User (turn 71):** "the face is still somehow long ... a/b/c images are so identical
  to [previous runs] ... idealy it should create a different man altogether right?
  ... the facial structure is still of jaisals, so theres defenetly something in the
  underhood".
- **Verified facts:** v6 run (01 chain, seeds 77/76/78 FIXED, 1152×2048) output =
  long face, stubble, NOT the approved zidane face (verified side-by-side against
  `refset_v7/zidane_portrait_00001_.png`). 01 source file untouched (mtime 10-18) —
  the original zidane prompt that created the approved face (live-typed, never
  saved) is GONE — it exists nowhere on disk.
- **Full rule (supersedes D162's "reuse home chain + seed" hope):** Krea2 face =
  f(**prompt text**, **seed**, chain, resolution) — ALL FOUR together. Seed 77 alone
  does NOT reproduce the approved face without its exact original prompt. My
  reconstructed prompts (v3–v6) keep landing near Jaisal's face region (prompt
  wording similarity), and adjacent seeds (76/77/78) are micro-variants of the same
  face. **No seed/prompt combination I can write will bring the approved face back.**
- **Decision: the approved IMAGE is the character.** `refset_v7/zidane_portrait_00001_.png`
  (input dir copy `zidane_portrait_00001_.png`) is the identity anchor. The only
  reliable way to a frontal version = **i2i from that image**: his pixels anchor the
  face, the model only rotates the head.
- **`10a_frontal3_zidane_i2i.json` (THE LOCK, builder `build_10a_frontal3_zidane_i2i.py`):**
  01 home chain (`Krea2Realism_V1` + V2@1.0, `qwen3vl_4b` (krea2), `qwen_image_vae`,
  8 steps euler/simple cfg 1), LoadImage `zidane_portrait_00001_.png` → VAEEncode →
  KSampler **[77, fixed, 8, 1, euler, simple, denoise 0.55]** → VAEDecode →
  SaveImage `FACEFRONTAL3_ZIDANE` (root). Prompt = identity-anchor-first ("The exact
  same man as the reference image — the SAME face — now completely frontal…") +
  halal/beard/white-tee attributes; negative = zidane's clean + pose/hair lock.
  Denoise 0.55 because v4's 0.4 came out = the input (too weak for head rotation).
  Validate 0/0 (11 nodes). **USER RUNS** (fresh tab).
- **Fallback (zero-risk, user's own earlier suggestion):** use the approved 3/4 face
  as-is for the sheet's LEFT panel (D151: left panel is the sole identity source; a
  3/4 view is a perfectly good identity reference — the sheet does not require a
  frontal face). If the i2i misses, build the composite from
  `zidane_portrait_00001_.png` directly.
- **For future characters:** capture the winning t2i prompt IMMEDIATELY (save the
  live-typed prompt into PIPELINE.md the same turn — D159) or the face is
  unreproducible by t2i afterwards; i2i from the approved image is always the
  fallback lock.

## D162 — Krea2 anchors the FACE to chain + resolution + prompt family, NOT to seed or prompt details (2026-10-20)
- **User:** "the images looks exactly same as jaisals image without hair ... are we doing it
  in same seed? is that the reasons? think outside the box".
- **Diagnosis (verified, not guesswork):** the file ran with seed control `randomize`
  (4 different runs at 18:19/18:24/18:34/18:40 → same face every time). Side-by-side
  image check: v5b output = **Jaisal's face** wearing zidane's hair/white tee — the
  prompt DID work for attributes (hair, tee, pose, beard), the FACE did not move.
- **Rule (supersedes D161's "reuse jaisal's chain" for zidane):** a character's face
  belongs to the CHAIN + RESOLUTION it was born on. Jaisal's face = turbo chain
  (`krea2_turbo_fp8_scaled`, 896×1120). Zidane's approved face = 01 chain
  (`Krea2Realism_V1` + V2@1.0, **1152×2048**, seed 77). Running character B's
  attributes on character A's chain = A's face wearing B's attributes — no seed or
  prompt change fixes that. (The seed still varies minor detail; the face family is
  the anchor.)
- **v6 (CURRENT):** `10a_frontal_base_zidane.json` = clone of `01_character_sheet.json`
  (zidane's home chain, 8 steps, 1152×2048) + **v4b's prompt family** (the one whose
  face the user approved — "first 3 is good", only the build was fat) with ONLY the
  build line fixed (lean and fit + distinctly ROUND face, zero fat words). 3 branches
  seeds **77/76/78 FIXED** (77 = his approved face seed = the lock), saves
  `FACEFRONTAL2_ZIDANE_{a,b,c}` (root, next counter `_00006_`). Validate 0/0 (16
  nodes), wiring verified.
- **For future characters:** before locking a face, note WHICH chain + resolution the
  approved face was born on and run all face work there. If a character needs a face
  on a different chain, i2i from the approved face (denoise 0.5-0.6) is the bridge —
  t2i on a foreign chain re-derives a different face.
- **Status:** v6 — **USER RUNS** (fresh tab).

## D161 — SUPERSEDED (the "reuse jaisal's 10a chain for zidane" method is WRONG — see D162); zidane canonical LEAN + ROUND face (2026-10-20)
- **User:** "the last image [i2i] is just the input, first 3 is good now, but this is
  like a fat boy, we dont need this ... he is a footballer, no fat, sorry for the
  misguidance, and lets make his face looks round, so that jaisals long one doesnt
  look similar ... can we just use the jaisals workflow where we created these images
  [the good frontals]? those frontal ones, with the different prompt, isnt that the
  easiest way?"
- **Build re-correction (supersedes D160's "slightly bulky" — that instruction was a
  misguidance):** Zidane is LEAN and fit (footballer, no fat). D160's stocky prompt
  made him come out "like a fat boy".
- **Face shape:** distinctly ROUND (wider/rounder than a long oval face) — deliberately
  different from Jaisal's long/oval face so the two don't look similar.
- **Method (user's suggestion, adopted):** `10a_frontal_base_zidane.json` **v5 = clean
  clone of the WORKING `10a_frontal_base_jaisal.json`** — the exact chain that produced
  the approved jaisal frontals (`krea2_turbo_fp8_scaled` + V2@1.0 + spicy@0.7 +
  FameGridColorFinish, 10 steps, 896×1120, 3 branches) — with a **ZIDANE-LED prompt**
  (his own identity block up front: round face, halal cut, full beard, white tee; same
  working style/length as jaisal's) and zidane's negative (jaisal's minus "short
  haircut"/"perfectly groomed beard", plus hair locks long/wavy/man-bun/topknot).
  i2i route DROPPED.
- **i2i lesson:** denoise 0.4 from the approved 3/4 portrait came out = the INPUT
  (barely changed — too weak for a head rotation). Pose changes need higher denoise or
  a different route; t2i branches are the reliable pick-set.
- **v5b fix (same turn, user caught it — "just copied the jaisals prompt, didnt even
  replaced zidanes prompt with the new details i shared"):** the first v5 prompt kept
  Jaisal's first 80 characters verbatim = the D156 shared-opening-token failure mode
  all over again. Replaced with a **FULLY INDEPENDENT** prompt (verified: 0 shared
  characters with the jaisal prompt): "Realistic close-up photo of a young Malayali
  footballer from Kerala..." — ROUND full-cheeked face (wider than a long oval),
  clearly defined facial features, short black halal cut, FULL short dark beard, lean
  and fit / slim athletic (NOT bulky, NOT muscular, NOT fat), white tee, frontal,
  half-smile, real unposed photo. All 3 branches (300/313/318) identical. Validate 0/0.
- **Rule:** when cloning a sibling's workflow for a new character, the prompt must be
  written from scratch — ZERO shared opening tokens with the sibling (D156 applies to
  PROMPTS too, not just files).
- **Status:** v5b validate 0/0 — **USER RUNS** (fresh tab) → `FACEFRONTAL2_ZIDANE_{a,b,c}`.

## D160 — SUPERSEDED (build part, by D161) — prompt bloat kills realism (still valid) (2026-10-20)
- **User:** "the image has now lost its quality, the realism is gone ... lets start from the
  beginning with a good prompt and lets lock the characters ... zidane is little bulky so lets
  have him some facial structure and fat".
- **CANONICAL ZIDANE BUILD (supersedes "lean and athletic" from the man-bun-era prompts):**
  slightly stocky build — FULL face, soft full cheeks with a little natural fat, strong but
  ROUNDED jawline (facial structure + some fat). Short black halal cut, FULL short dark beard
  neatly trimmed, white tee, warm medium-brown skin, mid-20s, relaxed half-smile.
- **Diagnosis (quality loss):** the v4a prompt had grown to ~15 sentences + a NOT-tag block
  → D142's failure mode → realism/quality dropped (patchy beard run).
- **Rule:** face prompts stay in the LOCKED D142 shape — natural-language, ~5 sentences,
  concrete features (build/face/hair/beard stated positively and visually), ZERO NOT-tag
  spam in the positive (the negative carries safety: clean-shaven/no beard/missing beard).
  `10a_frontal_base_zidane.json` 300 REWRITTEN from scratch in that style (v4b). The sheet
  (09k) needs NO build-text change — its spec takes identity only from the left panel (D151),
  so the locked face image carries the stocky/full look into the sheet.
- **Status:** v4b validate 0/0 — **USER RUNS** (fresh tab).

## D159 — Live prompts recorded VERBATIM in PIPELINE.md; strong-feature specs need concrete visual detail (2026-10-20)
- **User:** "i dont think you copied the correct prompt for zidane, from now onwards i
  want to copy the prompt also into the md file, so that i can see and ask you to redo
  if needed for other characters".
- **Rule 1 (prompt appendix):** `PIPELINE.md` now has a **PROMPTS — LIVE, VERBATIM**
  section: every character workflow's positive + negative copied verbatim (01 jaisal,
  10a_jaisal, 10a_zidane, 07 kit refs, sheet-spec note, stale char2 note). Whenever a
  prompt changes in a workflow, update this section in the SAME turn — the user reads it
  to review and request per-character changes.
- **Rule 2 (feature spec strength):** the v4 zidane run came out with a PATCHY beard —
  the prompt's beard line was one clause ("a FULL short dark beard, neatly trimmed"),
  which let Krea2's prior (thin patchy beard) win. The beard that actually produced the
  approved face was SPECIFIED CONCRETELY (where it sits + density + growth stage +
  targeted NOTs: "much more than stubble, NOT a thin patchy beard, NOT just a shadow,
  NOT clean-shaven"). A one-line feature description is too weak for Krea2; every
  identity-critical feature (beard, hair, build) needs a concrete visual block.
- **Status:** v4 prompt refreshed (strong beard block), validate 0/0 — **USER RUNS**
  (fresh tab).

## D158 — Locking a character's face: 3 t2i branches around the proven seed + 1 i2i from the approved face (2026-10-20)
- **User:** "this one doesnt produce 3 images to pick which is a good one ... lets lock
  the charaters ffs" — a single-seed run gives no choice; the lock must come from a PICK.
- **`10a_frontal_base_zidane.json` v4 = one run, 4 candidates:** 3 t2i branches on the
  01 chain (`Krea2Realism_V1` + V2@1.0, 8 steps, 1152×2048) with seeds **77/76/78**
  (centered on his proven face seed) → `FACEFRONTAL2_ZIDANE_{a,b,c}` (output ROOT);
  plus **1 i2i route** from the APPROVED 3/4 face (`LoadImage zidane_portrait_00001_.png`
  → VAEEncode → KSampler **denoise 0.4** same model/prompt/negative →
  `FACEFRONTAL_I2I_ZIDANE`) — his actual pixels anchor identity, only the head rotation
  changes; strongest lock of the four.
- **Rule:** when locking a face, give the user a 3-branch pick (seeds N-1/N/N+1 around
  the proven seed) AND an i2i-from-approved-face route; the i2i is the primary when the
  target is "same face, different angle". User picks one → that image becomes the locked
  ref (staged to input, feeds the 3-panel composite).
- **Status:** v4 validates 0/0, wiring verified — **USER RUNS** (fresh tab).

## D156 — Reproducing a specific Krea2 face = reuse its exact proven settings; never clone a sibling's file (2026-10-20)
- **User:** "it just gave me the same image as jaisal, without hair lol, it doesnt work,
  we need to find out the workflow which produced zidane_portrait_HD_00001_ and copy the
  same prompt".
- **Finding:** `refset_v7\zidane_portrait_HD_00001` (via its 1152×2048 base
  `zidane_portrait_00001`) came from **`01_character_sheet.json`** (id
  `krea2-t2i-character`, the "01 t2i") — chain: **`Krea2Realism_V1.safetensors`** (NOT
  turbo) + `Krea2-realism-V2`@1.0, `qwen3vl_4b` (krea2), `qwen_image_vae`, 8 steps
  euler/simple cfg 1, **1152×2048** portrait, D142 clean negative verbatim. On-disk
  state is JAISAL's portrait (seed 42, save `refset_v7/jaisal_portrait`); the zidane run
  used the SAME file with his prompt live-typed + **seed 77** — never saved. The
  `krea2_t2i_char2.json` file (turbo + spicy chain, man-bun-era `PixaromaPromptEach`
  prompts, JAISAL negative) is a STALE template — NOT the source. (v2 of 10a was wrongly
  built on the char2 chain; **v3 = clone of 01**.)
- **Rule:** Krea2 t2i faces are prompt+seed-deterministic. To reproduce a face, reuse
  its EXACT settings (seed, size, chain, D142 natural-language style) and its own
  attribute description — do NOT clone a sibling character's workflow (shared opening
  tokens → the same face; tag-stacking → D142 failure mode). `10a_frontal_base_zidane.json`
  **v3 = clone of `01_character_sheet.json`** (the true source): D142 canonical-attr
  FRONTAL prompt (kr2realism trigger, medium close-up, 50mm style — mirroring 01's
  jaisal prompt structure), seed 77 fixed, 1152×2048, 8 steps, save `FACEFRONTAL2_ZIDANE`
  (no slash → output ROOT, like `FACEFRONTAL_JAISAL_*`).
- **Status:** v3 validate 0/0 — **USER RUNS** (fresh tab). If the face still misses, the
  user's remembered original prompt is the next input (the exact one was never saved).
- **D157 (output registry):** `PIPELINE.md` now carries the **OUTPUT REGISTRY** — every
  workflow → the images it produced → what each image is + status. RULE: whenever a
  workflow produces an approved output, record it there in the same turn (workflow,
  settings, output path, description, status). SaveImage convention: slash in prefix →
  subfolder; no slash → output ROOT.

## D155 — Zidane sheet = 09k (09j architecture) + PIPELINE.md as the production map (2026-10-20)
- **User:** "lets do the same thing for zidane also ... zidane also need a front facing image,
  not the sideways one, so lets do it from there" + "capture the pipeline ... all these
  workflows names must be there in the md file ... so that we can introduce as many
  characters as we want with this pipeline".
- **Zidane route = 09j's architecture, cloned** (`09k_QWEN21_ZIDANE_sheet.json`, both
  copies, validate 0/0): 470→`zidane_sheet_ref_3panel.png`, 481→`ZIDANE`,
  461→`charsheet/QWEN21_ZIDANE`, 478 live spec + 555[0] mirror with dark-green kit +
  green-ground crest. The existing `zidane_portrait_HD.png` (4608×8192) is the SIDEWAYS
  face — a FRONTAL face is generated first: `10a_frontal_base_zidane.json` (10a clone,
  ZIDANE's canonical attributes from `zidane_portrait_00001`: short black hair w/ faded
  sides, short FULL dark beard, white tee — the D137 "loose topknot" description is STALE,
  the on-disk canonical face rules). `build_zidane_sheet_ref.py` stages the chosen
  `FACEFRONTAL_ZIDANE_{a,b,c}` output → `input\zidane_portrait_front.png` → builds the
  2304×1536 composite. `input\zidane_crest_ref.png` = the approved roundel on a DARK GREEN
  ground (38,73,63 sampled from `zidane_kit_ref.png` — crest ground always matches the
  kit; roundel pixels untouched, blue ground recolored deterministically).
- **`PIPELINE.md` (workspace root) = the production map:** stage diagram + every workflow
  by name/details (Krea2 face/kit/identity stage, logo + transparent-crest stage, 3-panel
  combiner scripts, 09j/09k sheet stage, dataset → Klein-9B DENSE LoRA stage, H3 R2V +
  Blender + audio + seedvr2/RIFE movie stage), the **how-we-add-more-details methodology**
  (IMAGE channel = reference panel + one "copy EXACTLY — do not redesign" line in 478;
  TEXT channel = 478 spec; identity = LEFT panel ONLY per D151), and the 8-step
  new-character checklist (the "as many characters as we want" procedure).
- **Status:** Active. User run sequence: 10a_frontal_base_zidane → pick branch →
  `build_zidane_sheet_ref.py [branch]` (agent runs, no GPU) → 09k (fresh tab) → verify.
  Then dataset/LoRA stage, then the movie.

## D154 — Sheet A/B verdict: 09j (Qwen) wins; 3-panel reference feed + live spec layer (2026-10-20)
- **A/B results (user ran all 4 sheets):** **09j Qwen = winner** (user: "qwen ended up being
  the top") — the only route with both a professional design-sheet layout (metadata column,
  hero, turnaround row, action panel, silhouettes, expressions, detail grid) AND identity
  close to the reference. 05d H3-wide: good face + layout but small crest roundel. 05e
  H3-fizgig: **identity drift** (fuller beard — a different man) + duplicated back view.
  08j Krea2: good face + good crest (it carries a crest ref) but loose layout (no sheet
  structure).
- **Root cause (user's hypothesis confirmed — it's the setup, not the model):** the route
  ARCHITECTURE decides. 09j separates **spec (text)** from **identity (image)**: the PE
  architect (which sees the face) writes a precise 10-section sheet spec and the i2i
  generator is conditioned on face image + that spec. The other routes give the model
  image-only conditioning (H3 R2V refs = frame anchors for a video model, not identity
  locks for a static sheet) or a weak layout prior (Krea2 edit = "photograph of a person",
  not "design sheet document").
- **09j emblem-invention root cause — dead spec layer:** the PE LLM input = **internal
  subgraph node 478** (the 10,404-char architect spec). The turn-53 monochrome spec was
  placed in **instance 555 widget[0] — a dead field** (not in the named widget dict,
  absent from the LLM input — proven by the user's debug paste: the LLM input carried
  478's OLD non-monochrome KIT SPEC, "a white clenched raised fist inside a thin white
  circle", no no-color constraint) → with no crest image and no monochrome constraint the
  architect **invented its own crown-like emblem** ("TEIIM CREST" typo tile) and the
  jersey came out flat (no texture).
- **Fix (file work, user runs):** (1) **3-panel composite reference**
  `input\jaisal_sheet_ref_3panel.png` (2304×1536 = exactly the 3:2 sheet aspect → i2i sees
  the whole composite, no crop; PE image budget 4MP ≥ 3.54MP → architect sees it at full
  resolution): LEFT = face portrait (dominant, full height — SOLE identity source),
  TOP-RIGHT = crest emblem on royal blue (COPY target, not invention target), BOTTOM-RIGHT
  = kit flat-lay (color/fabric/texture source) — `build_3panel_ref.py`. (2) **Rewire:**
  470 → composite; PE 555.in0 + generator 459.in6 take the composite directly; **VSR node
  485 BYPASSED** (it soft-upscaled the face 896×1120→1368×1712 — half of the "full body is
  a bit blurry" cause). (3) **478 (live layer) updated:** new REFERENCE IMAGE LAYOUT
  section + monochrome KIT SPEC; 555[0] mirrored. `patch_09j_3panel.py`, both copies,
  validate 0 errors (orphan 485 warning = expected, harmless — pruned, doesn't run).
- **Rule: the PE's LIVE spec layer = the internal subgraph text node (478), NOT the
  instance's unnamed positional widget (555[0]). When changing a PE's behavior, verify
  which text layer actually reaches the LLM — the node's debug "Final prompt" is the
  ground truth.**
- **Status:** Active — user runs 09j (FRESH tab) with the 3-panel feed → verify crest =
  actual roundel + jersey texture → 09j = the locked sheet route → dataset/LoRA stage.

## D153 — Multi-layer model widgets: sync ALL layers to on-disk models (2026-10-20)
- **Problem (user saw errors in 09j UI):** author-baked model defaults persisted in the
  LAYER I hadn't patched. Workflows store model names in up to FOUR places:
  (1) internal-node `widgets_values` (positional) — what actually executes;
  (2) internal-node `widgets_values_named` — author's stale defaults (09j subgraph 451
  named = `qwen_image_2.1_int8_convrot`, 453 named = `qwen3vl_8b_bf16` ← the exact
  names the user had asked about); (3) instance-node `widgets_values` (09j 459
  widgets[8/9/10] = `qwen/`-prefixed author names); (4) instance-node
  `widgets_values_named`. UI displays layers 3/4 → red "not found" errors even when
  execution (layer 1) is fine.
- **Rule:** whenever a workflow is localized to this machine, set ALL four layers to
  the on-disk filename (bare name, no author path/prefix). `utilities\sync_model_layers.py`
  did it for all 4 sheet workflows (both copies): 09j 451→`qwen_image_2.1_bf16`,
  453→`qwen3vl_8b_fp8_scaled`, 459 instance→same bare names; 05d named layers ←
  positional (working) values incl. node 2 video VAE = `minimax_h3_t1_image_vae_step1597`;
  05e named ← positional (71 = `minimax_h3_ref2va_pruned_int8_convrot` — 05e's real
  working UNET, same as 05d; author's `fused_refdelta_r1024_turbo8_mystic07` existed
  only in the stale layer; 72 = `qwen3vl_32b_minimax_h3_nvfp4_awq`). 05d node 22
  (muted LoRA, mode=4) left alone. All 4 validate 0/0.
- **PE model fact:** `Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf` (5.24 GB) lives at
  `models\LLM\GGUF\` — the `[local]` prefix in the ThinkingLLM node is the node's
  lookup convention, it resolves fine (not a missing file).
- **Answer to "do we change models manually every time?": NO — the stored value is
  what the workflow runs; the dropdown's first entry is just the server's
  alphabetical list, not a default. Localize once (all layers) and it stays.**
- **Status:** Active. Every future author-template localization: run the
  all-layers model check (`utilities\check_all_sheets_models.py`) before handing off.

## D151 — Sheet pipeline: sheet prompts = face ref + kit ONLY, no attribute re-descriptions (2026-10-20)
- **User:** "lets not add more characters details when we make the character sheet. The pipeline
  should be: create character with all the attributes, and then create character sheet with face
  + clothing/style we need… otherwise if we keep adding character details at worksheet, we cannot
  compare the result of the worksheet workflows."
- **Rule (2-stage):** (1) CHARACTER = face ref with all attributes (`jaisal_portrait_HD.png`);
  (2) SHEET = that face ref image + clothing/style spec ONLY. Sheet prompts must NOT re-describe
  hair/beard/build/skin/age — identity comes 100% from the reference image; the prompt carries
  only the kit/style spec. Reasons: (a) fair A/B comparison — all 4 routes get identical input
  (same ref images, same kit text), so results differ only by ROUTE; (b) text fighting the image
  over identity = drift.
- **Applied (2026-10-20):** 05d/05e subject lines + 09j PE (555) attribute lists replaced with
  "the exact man from <Picture 1> — face, hair, beard, skin and build come ONLY from <Picture 1>
  (the image is the sole identity source)". 08j already compliant ("the same man from the
  reference image" — no attribute list). Retention lines unchanged (already "come only from
  <Picture 1>"). All 4 validate 0/0 (both copies).
- **Status:** Active. All future sheet/turnaround builds (Jaisal, Zidane, others) follow this.

## D152 — Qwen 2.1 best combo on this machine: bf16 UNET + fp8_scaled CLIP + bf16 VAE (2026-10-20)
- **Question (user):** 09j author defaults = int8 UNET + fp16 CLIP; disk has bf16 UNET + fp8
  CLIP. Best combo? Download defaults? Download `qwen3vl_8b_bf16`?
- **On disk (verified 2026-10-20):** UNET `qwen_image_2.1_bf16` 13.25 GB (strongest on machine),
  VAE `qwen_image_2.1_vae_bf16` ✓ (as the author expects), CLIPs: `qwen3vl_8b_fp8_scaled` 9.86 GB,
  `qwen3vl_8b_int8_convrot` 8.71 GB, 4b bf16/fp8, no 8b fp16/bf16.
- **Answers:** UNET bf16 = strongest (full precision > int8) — KEEP, do not download the default
  int8. CLIP: `fp8_scaled` > `int8_convrot` — upgraded 09j subgraph node 453 to
  `qwen3vl_8b_fp8_scaled` (text-encoder precision matters far less than UNET precision; fp8 is
  the strongest 8b clip on disk). `qwen3vl_8b_bf16` = NOT NEEDED — ~16 GB for a negligible gain
  on an 8B text encoder; mixing precisions across independent loaders (bf16 UNET + fp8 CLIP) is
  normal. NO downloads needed.
- **Wiring (2026-10-20):** 09j subgraph node 453 → `qwen3vl_8b_fp8_scaled.safetensors` (both
  copies); UNET 451 `qwen_image_2.1_bf16` + VAE 454 bf16 unchanged. 09j validates 0/0.
- **Status:** Active for all Qwen 2.1 routes.

## D150 — Run discipline: explicit per-run instruction + qwen/comfyui exclusivity (2026-10-19)
- **Incident:** agent misread "you create these and let me know" as run approval and
  queued the logo-comparison job on the user's ComfyUI. User stopped it: "dont run
  anything untill i specify".
- **Rule 1:** "create / make / update / wire" = file work ONLY. A run needs an EXPLICIT
  run instruction (run/queue/start/execute) for that specific workflow — D138
  reinforced, never inferred from "create these".
- **Rule 2:** NEVER run workflows in parallel. Qwen llama-server (port 8100) and
  ComfyUI (especially MiniMax H3 generation) cannot share the GPU at the same time
  (VRAM contention on the 32GB 5090). User manages both servers; the agent confirms
  server state before proposing any run, and runs ONE workflow at a time.
- **Status:** Permanent, all sessions.

## D148 — Crest fidelity: dedicated image ref + no "logo" in negatives (2026-10-19)
- **Problem (user):** sheets render the jersey crest weak/garbled ("looks like a minicromax
  one, not the Palestine resistance hand") — a text description alone cannot force a crisp
  emblem; 09j missed the kit entirely (charcoal tee) because its live PE prompt was empty.
- **Decision (user: "add image node for that as well"):** the crest gets a DEDICATED
  reference image — `input\jaisal_crest_ref.png` (512×512 tight crop of the fist roundel
  from `jaisal_kit_ref.png`, `utilities\crop_crest_ref.py`) — wired as its own ref slot:
  05d `ref_image_2` = `<Picture 3>` (node 900, link 204), 05e `ref_image_1` = `<Picture 2>`
  (node 900, link 726). Prompts: "crest rendered EXACTLY as <Picture N>" + a SEPARATE
  round detail panel of the emblem alone in ALL 4 workflows (08j adds it as a 4th element;
  09j = full kit spec in PE node 555's custom prompt since its architect subgraph is not
  instanced — live path is PE 555 → generator instance 459).
- **Negative gotcha:** a generic "logo" term in the NEGATIVE prompt SUPPRESSES the desired
  crest — 08j's negative carried it; removed, and added emblem-specific negatives
  (malformed emblem, deformed fist, missing/extra fingers, illegible crest, blurred
  emblem). **Rule: never put the word "logo" in negatives when a logo/crest is a desired
  element.**
- **Jersey = plain colors** (user): single flat royal blue, no patterns, no numbers on
  front; white crest on left chest; white "JAISAL" on upper back; navy track pants +
  single white side stripe; white boots.
- **Status:** Active. All 4 updated workflows validate 0/0 (both copies). Zidane variant
  gets the same treatment (`zidane_crest_ref.png` from `zidane_kit_ref.png`).

## D149 — krea2edit N² attention-bias ceiling + face bases are t2i-only (2026-10-19)
- **Hard limit discovered (user's 10a v1 OOM):** `comfyui-krea2edit._ref_attn_bias` allocates
  `torch.zeros(1, 1, L, L)` over the combined target+ref sequence — **O(N²) VRAM**. 16MP
  output + 2 full-size refs → L ≈ 136k → a **72.92 GiB** single tensor → OOM on a 32GB 5090
  (only 11 GB free at the step). Author's own note in 02: "1MP is the sweet spot".
- **Rule:** krea2edit (identity-edit) runs stay at **≤ ~2MP total** (target+refs). For bigger
  outputs use plain t2i (no ref attention → sdpa/flash, no N² allocation) + pick-from-seeds.
- **Face/character bases = FRESH T2I only** (extends D141): identity-edit is a LOCKING tool —
  every i2i pass degrades quality; it must not CREATE a face. Proven creation recipe
  (`krea2_t2i_char1_pe3.json`): author character prefix verbatim + scene clause, 896×1120
  1MP 4:5 latent, 3 KSampler seeds per queue, author's anti-studio negative, then 4x upscale
  (`03_hd_upscale.json`). **10a v2 = exactly this** (frontal clause replaces scene clause;
  3 candidates `FACEFRONTAL_JAISAL_a/_b/_c`; TextGenerate/PE nodes dropped — Qwen stopped —
  full prompt straight into CLIPTextEncode).
- **Status:** Active constraint. Any future identity-edit build: check target MP × ref count
  against the ~2MP ceiling BEFORE queuing.

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
