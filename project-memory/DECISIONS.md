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
- **Decision PENDING user verdict:** if realism is good → replace the Krea2 base in workflows with `Krea2Realism_V1` (old files kept, not deleted).
- **Reddit access recipe:** www/old.reddit + `.json` endpoints are blocked (headless "network security" + login redirect) → use redlib mirrors via web_fetch: `https://safereddit.com/r/<sub>/comments/<id>/` works (verified on 1x76buu).
- **Status:** waiting on user's browser download + A/B run.

## D135 — Challenge entry RESCOPE: "character-consistent short app" (2026-10-18, user-approved)
- **Decision:** the challenge entry is NOT a frontier-solver (long-take/continuity problems are already solved by public open packs — `comfyui-obvpm-timeline` (chanon/obvpm, GPL-3.0, mini H3 video editor: extend/bridge/loop from latents, seam rating, live preview, latent upscale), `h3_clown_anchoring` (roycho87 — flash-free joins via noise-mask-hold of next shot's real latents), `H3-LongTakeNoCuts` (xyzDist — SAM3-masked refine + frame-blend kills the "photocopy" degradation), `Fizgig H3 Tweak` (shootthesound — detail/contrast, scene-variation, prompt-strength dials), `SceneCut` (PedroMarinhoDev, MIT — shot detection + trim). All user-shared or community-published.)
- **The entry:** a **character-consistent short app**: our `krea2_identity_edit_v1_2` LoRA face-locks the character (Krea2 sheet → identity refset → 2-anchor H3 shots, D020/D023), **obvpm-timeline as the timeline engine (credited, public)**, ffmpeg assembly, natural-sounds-only (D041). Our moat = the identity LoRA (original trained weights) + the 2-anchor technique + app packaging/docs; the frontier repos are credited, not re-solved.
- **Prize targets (honest):** Most Viral ("your face in a short, same face every shot") + Open Weights Only (5090) + H3 bonus ($1,000 credits). **Dropped the Most Innovative claim** (obvpm et al. own that ground). Best Overall = bonus if the demo lands.
- **Build (in `challenge\consistent-short\`, new folder in the vsCodeMcp repo — user pushes it as a new GitHub repo):** `workflows/01_character_sheet.json`, `02_identity_refset.json` (both validated 0/0 earlier), `03_h3_r2v_2ref.json` (validated 0/0), `04_h3_timeline_r2v.json` = the author's `h3_obvpm_timeline_r2v_v0.1.4-007A` adapted: removed `H3LivePreview` (missing `taeh3.safetensors`), un-bypassed generator engine (inst 1359) + `H3ContextWindows` (1356), re-pointed upscale engine model link to 1356, added ordering link 3002 (SetNode `h3_clip_vaes` 1373 → Unbundle 1379 — the published file's Set/Get roots execute before their setters). **Validates 0 errors** (26 expected warnings = author's default-muted optional groups).
- **Packs installed 2026-10-18 into `E:\comfyUi_latest\...\custom_nodes`:** `comfyui-obvpm` UPDATED to **v0.2.16** (was Aug-old; timeline needs ≥0.2.16), `comfyui-obvpm-timeline` 0.1.4, `ComfyUI-MiniMax-H3-Turbo` (Larryvrh), `ComfyUI-Fizgig-H3-Tweaks` (shootthesound). ComfyUI restarted; all nodes verified in object_info (`MiniMaxH3Timeline`, `FizgigH3Tweaks`, `MiniMaxH3TurboLoRA`, `ValuePresets (obvpm)` etc.).
- **Smoke test (2026-10-18):** Jaisal bridge refs (`jaisal_1_longshot.png` + `jaisal_4_middle.png` wired as ref_image_0/1 via native LoadImage nodes 2001/2002), 2-anchor 16:9 1MP prompt on subgraph node 763, 5 s timeline. First run FAILED at `h3_clip_vaes` Set/Get ordering → fixed with link 3002 → re-run `62c47768`.
- **Remaining:** confirm smoke-test video (face consistency), write app README (credits + setup), user's public GitHub repo, comfy-cli cloud Build test, 2-3 demo shots + demo video, submit typeform `V1dSQrkS` before **10/30 9am PT**.
- **Status:** Active — build in progress; **Jaisal Episode 1 remains the primary goal** (challenge work done in bursts).

## D134 — Open Source Higgsfield challenge entry "Story-Short" (2026-10-17, user-approved GO)
- **Decision:** enter the Comfy "Open Source Higgsfield" challenge (deadline **10/30 9am PT**, winners 11/6) with a **"Story-Short" app**: one prompt → Krea2 character sheet → identity-edit face-locked reference set → H3 R2V 2-ref shots (D020) → assembled video. Scoped to **H3 bonus ($1,000 API credits) + Open Weights Only (5090)**; $10K Best Overall = free auto-entry, don't chase; LTX $2K cash bonus = skipped (no LTX pipeline).
- **Reason:** our movie pipeline already IS the app (D020/D021/D023) — packaging proven workflows ≈ packaging work, not new development. All node packs used are public GitHub repos (several merged into core ComfyUI) → public cloud Build feasible. H3-bonus credits are directly usable for the movie.
- **Scope rules:** 3 core workflows (character sheet / identity refset / H3 R2V), UI format; local Qwen PE `TextGenerate` node DROPPED from cloud version (needs local llama.cpp); assembly via ffmpeg; NO partner nodes/APIs (open-weights compliance); identity-edit LoRA + character sheets become PUBLIC (user-approved).
- **Ops:** entry runs on Comfy cloud GPUs (Comfy API Build/Release/Deployment via comfy-cli) — does NOT touch the local 5090; sign up EARLY (first 200 signups get free credits, form: `form.typeform.com/to/Ayn9Cwfj`); stop/delete deployment after submission (storage billing); user creates the public GitHub repo.
- **Status:** Active — plan + checklist in `challenge\CHALLENGE_PLAN.md`.
