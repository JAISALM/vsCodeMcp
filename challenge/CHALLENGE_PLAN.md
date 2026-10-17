# Open Source Higgsfield Challenge — Plan (D134, 2026-10-17)

**Entry:** "Story-Short" — one prompt → a short narrative film with a consistent character.
**Deadline:** 10/30, 9am PT (~22:30 IST). **Winners announced 11/6.**
**Targets (scoped):** H3 bonus ($1,000 API credits) + Open Weights Only (5090). Auto-entered for $10K Best Overall (don't chase). LTX $2K cash: skipped (no LTX pipeline, too tight).

## Why this entry
Our movie pipeline already IS the app: Krea2 character sheet → identity-edit face-locking → H3 R2V 2-ref shots → video. Most entrants start from zero; we package what's proven (D020/D021/D023). All node packs used are public GitHub repos (several merged into core ComfyUI) → public cloud Build is feasible.

## Scope decisions
- **App pipeline (3 core workflows, UI format):**
  1. `01_character_sheet.json` — Krea2 t2i character sheet (base UNET + qwen3vl_4b + qwen_image_vae).
  2. `02_identity_refset.json` — Krea2 identity-edit reference set (identity-edit LoRA v1.2, ref_boost 4, style LoRA optional).
  3. `03_h3_r2v.json` — H3 ReferenceToVideo, 2-ref anchors, short 6-section prompt (D020).
- **Dropped from cloud version:** local Qwen PE `TextGenerate` node (needs local llama.cpp — not cloud-deployable). Direct prompts instead.
- **Assembly:** shots concatenated via ffmpeg (documented in README; no custom node needed).
- **Audio:** H3 native audio + our no-music SFX prompting rule (D041) — keep prompts music-free.
- **Open-weights compliance:** all models open (Krea2 base, qwen3vl_4b, qwen_image_vae, H3 via Comfy-Org/MiniMax-H3 on HF); NO partner nodes/APIs in the entry graph.
- **Publishing (user-approved 2026-10-17):** identity-edit LoRA + character sheets become public with the repo.
- **License:** MIT (confirm with user).

## Division of labor
- **Agent (me):** repo packaging, workflow conversion/trimming, cloud Build + deployment test via comfy-cli, showcase generation, README + setup docs, demo-video assembly, submission-package checklist.
- **User:** (1) sign up at https://form.typeform.com/to/Ayn9Cwfj TODAY (first 200 signups get free credits), (2) create public GitHub repo (name TBD, e.g. `story-short`) + give push access, (3) approve concept + outputs, (4) submit form (https://form.typeform.com/to/V1dSQrkS) before 10/30 9am PT.

## Timeline
- 10/17: decision GO. ✅
- 10/18: repo skeleton + README; user signs up; pick exact workflows.
- 10/19-10/22: package 3 workflows (UI format, clean model names), model-download doc, local dry-run of each.
- 10/22-10/25: comfy-cli Build from workflows → deployment → test endpoint end-to-end (fix cloud env gaps).
- 10/25-10/27: generate 2-3 showcase outputs (different prompts), assemble demo video (script + footage).
- 10/28-10/29: buffer — fix breaks, polish README, record final demo.
- 10/30 (before 9am PT): submit. Then STOP/DELETE the deployment (storage billing).

## Risks / mitigations
- **Cloud env gaps** (custom node deps on managed GPU): mitigate early — build the Build by 10/22 and test-run day one; comfy-cli reports missing deps.
- **H3 on cloud GPU size/VRAM:** deployment GPU options include H100/H200/B200 — H3 fits; pick smallest GPU that loads it to keep per-second cost low.
- **Billing:** sign-up free credits cover most; min 0 workers (scale-to-zero); delete deployment after submission.
- **Movie priority:** challenge work runs in parallel; GPU jobs (showcase gens) scheduled around writing sessions; H3 cloud runs don't touch the local 5090 at all.
- **Identity-edit LoRA license:** it's ours (trained 2026-08-29, D023) — safe to publish; confirm no third-party weights inside.

## Status
- [ ] User: sign up (typeform) — first 200 credits
- [ ] User: create public GitHub repo
- [ ] Repo skeleton + README + LICENSE
- [ ] 3 workflows packaged (UI format)
- [ ] Model download doc (exact files + HF links)
- [ ] Local dry-run of each workflow
- [ ] comfy-cli Build + deployment test
- [ ] 2-3 showcase outputs
- [ ] Demo video
- [ ] Submit form (10/30 9am PT deadline)
- [ ] Stop/delete deployment after submission
