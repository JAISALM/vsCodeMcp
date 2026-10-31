# LORA TRAINING KIT — Jaisal & Zidhan character LoRAs (reusable tracker)

> **Purpose (user directive 2026-10-31):** ONE place that tracks every LoRA-training workflow,
> prompt, dataset, trained model and curation rule — so we REUSE assets instead of creating
> N throwaway workflows. Check here BEFORE building anything new.
>
> **Status 2026-10-31:** RESUME PLANNED (see §0 + §9). Last trained = `krea2fp_V2` (2026-10-22).
> Klein route DEAD (realism). Krea2-realism-stack route = the way forward.

---

## 0. Status & WHY WE STOPPED (the full story)

1. **2026-10-22:** `krea2fp` v1 trained (Fizgig, rank 8, dual-subject, 30 epochs) → A/B test:
   face DRIFT — rank 8 / 0.25 MP too weak (identity came 100% from the LoRA; quality bad).
2. **2026-10-22:** `krea2fp_V2` retrain (rank 32, 64 epochs, 1.0 MP) → **Jaisal strong, but
   Zidhan came out CLEAN-SHAVEN** (beard lost — the old LoRA's known failure mode).
3. **2026-10-24 (P3):** plan = rebuild the dataset via **Flux-2-Klein-9B** + consistency LoRA →
   **ABANDONED: Klein-generated images lack photorealism** ("expression like a dummy with no
   human touch, no realism" — EXPERIMENTS 2026-10-24). **Conclusion: never build a character
   dataset on top of Klein images.** (The `klein_v2_jaisal/` / `klein_v2_zidhan/` dirs never
   materialized / were cleaned — not on disk 2026-10-31.)
4. **The unblock (already solved):** Krea2's "wooden wall" realism is handled by the **D142
   realism stack** (§5) — proven 2026-10-23 for realistic images. So datasets go through
   **Krea2 + realism stack**, not Klein.
5. **Minimum to start the story:** ONE dual-subject LoRA (triggers `jeskvman`/`dlorman`) with a
   beard-verified Zidhan dataset = `krea2fp_v3` (§9). We already have `krea2fp_v2_ep64`
   covering both subjects — the retrain fixes the beard, not the architecture.

## 1. Characters & IMMUTABLE refs (D137)

| Character | Spec | Immutable refs (do NOT regenerate) |
|---|---|---|
| **Jaisal** (char1) | ~26, wavy black hair, slim build, plain black t-shirt, crooked nose, clean-shaven/faint stubble | `data\character_finals\jaisal_final.png` (4.5 MB) · `data\locked_refs\jaisal_LOCKED.png` |
| **Zidhan** (char2) | ~26, black hair in loose top bun, slim build, plain white t-shirt, **FULL short dense beard** | `data\character_finals\zidhan_final.png` (4.1 MB) · `data\locked_refs\zidhan_LOCKED.png` |

Krea2 quirks (every prompt): it CANNOT make faceless characters; it DUPLICATES the character —
"ONLY ONE character, no other people, no duplicates" in every dataset prompt.

## 2. Trained LoRAs inventory (disk-verified 2026-10-31)

| LoRA (in `E:\ComfyUI_windows_portable\ComfyUI\models\loras\`) | Size | What | Status |
|---|---|---|---|
| `krea2fp_rank8_ep16.safetensors` / `_ep30` | 56 MB | v1 dual-subject rank 8 | SUPERSEDED (drift) |
| `krea2fp_v2_ep32.safetensors` / `_ep64` | 224 MB | v2 rank 32 dual-subject | **CURRENT** — Jaisal good, Zidhan clean-shaven |
| `bfs_head_v1_flux-klein_9b_step3500_rank128.safetensors` | 632 MB | head LoRA on Klein base (step 3500) | parked |
| `krea2_identity_edit_v1_2.safetensors` | 1.7 GB | identity-edit v1.2 (D023, ref_boost 4.0) | ACTIVE (workflow `krea2_identity_edit.json`) |
| `Krea2-realism-V2.safetensors` (+ `Krea2Realism_V1`) | 1.5 GB | realism LoRA (D142, trigger `kr2realism`) | ACTIVE (the §5 stack) |
| `krea2_turbo_lora_rank_64_bf16.safetensors` | 448 MB | speed turbo LoRA | ACTIVE (in §5 stack @0.7) |

Training outputs (per-epoch + finals): `D:\tools\Fizgig\output_loras\` (`krea2fp-000001..030`,
`krea2fp_V2-000001..064`, loss files). Copy finals + a mid checkpoint to the shared `loras\`
folder as `<name>_rankNN_epNN.safetensors` (combo-ready bare names).

## 3. Dataset GENERATION workflows (REUSE — all in `E:\comfyUi_latest\...\user\default\workflows\`)

| Workflow | Role |
|---|---|
| `krea2_realism_2mp.json` | **THE dataset generator** — D142 realism stack, 1440×2560 (see §5) |
| `krea2_dataset_char1.json` / `krea2_dataset_char2.json` | per-character dataset batches |
| `krea2_t2i_char1.json` / `krea2_t2i_char2.json` (+ `_pe3` variants) | t2i PE3 dataset variant |
| `krea2_1click_dataset.json` | one-click dataset |
| `krea2_face_lock.json` / `_v2` / `_batch` / `_jaisal_hd` / `_zidhan` / `_zidhan_hd` / `_zidhan_hd2` | face-lock passes (lock an approved face across the set) |
| `k2e_zidhan_beard_sweep.json` | **Zidhan beard recovery sweep** |
| `QWEN_click_multiple_character_angles-v1.0.json` | multi-angle set |
| Char sheets: `05d_charsheet_H3_wide_{jaisal,zidane}.json`, `05e_charsheet_H3_fizgig_jaisal.json`, `2BZ_H3_character_sheet_2stage*.json`, `LEEBLAAB-QwenImage21-Character-SHEET*.json` | sheet generation (Krea2/QwenImage21/H3) |
| `krea2_jaisal_char.json`, `krea2_official_char_test.json` | single-character tests |

**Dataset dir convention:** `D:\models\vsCodeMcp\data\<run_name>\` — existing runs:
`charlora_sweep_run` (6), `charlora_v3_run` (2), `jaisal_zidhan_v2_run` (3),
`jaisal_zidhan_v3_run` (3), `zidhan_beard_sweep` (3), `realism_2mp_run` (6), `face_lock_run` (1),
`face_lock_v2_run` (3), `locked_refs` (2). **`jaisal_variations` (6) = NOT a verified set —
DO NOT use as a dataset** (2026-10-24 user verdict).

## 4. Dataset CURATION rules (STRICT — 2026-10-24 user verdict)

- **~20 images per subject** (10 Jaisal + 10 Zidhan): the 6 movie scenes + close-ups +
  3-4 angles + profile + mixed lighting (overcast / warm / indoor); face clear & well-lit.
- **Zidhan: FULL short dense beard in ALL 10** (the ep64 failure mode).
- **Jaisal: clean-shaven/faint stubble, black tee, crooked nose.**
- Reject per image: noise/grain, face drift, blackouts, dummy expressions, bad anatomy —
  NO "acceptable".
- **Show the curated set to the USER before training — never self-certify.**
- Do NOT resurrect: `k2f_*_scenes` 2-pass approach (all 6 outputs REJECTED), face-lock-to-HD
  (REJECTED), t2i re-rolling for an approved face (D163 dead end).

## 5. Realism stack (D142 — the unblock, proven 2026-10-23)

`krea2_turbo_fp8_scaled` (UNET) + `krea2_turbo_lora_rank_64_bf16` @0.7 + `Krea2-realism-V2`
@0.8 (trigger `kr2realism`/`r3alism`) + `ApplyKrea2NegPiP` · **12 steps, cfg 1,
er_sde/simple** · 1440×2560 (4MP portrait). Fresh t2i seed variance in this stack = normal
(seed variance, NOT a broken setting — face-anchored low-denoise edits restore it).

## 6. Training recipe (Fizgig = PRIMARY — D167; AI Toolkit = SECONDARY)

- Tool: `D:\tools\Fizgig` (venv + `output_loras\`).
- **People mode = Fizgig LoRA Isolation** for the 2 subjects; sample prompts = ONE trigger per
  line (`jeskvman` / `dlorman`).
- **rank 32, alpha 32, ~15–20 epochs, 1.0 MP** (full-rank 7 h = rejected as overkill).
- ~2–3 h per run on the 5090. Loss files land in `output_loras\.fizgig_loss_<name>.jsonl`.
- Copy final + one mid checkpoint to shared `loras\` (bare names, see §2 naming).

## 7. VERIFICATION (strict — never self-certify)

- Workflows: `krea2_charlora_v3.json` (LoRA + realism stack, 4MP portrait, fresh seeds —
  dataset `charlora_v3_run`) · `krea2_charlora_sweep.json` · `krea2_ab_B_lora.json` /
  `krea2_ab_B_lora_v2.json` (pure-LoRA vs stack A/B; bypass realism nodes to isolate).
- Bar: face match per character, **beard present (Zidhan)**, skin realism, no drift across
  all 6 scenes. **Show user → verdict in chat → EXPERIMENTS.md.**

## 8. PROMPT inventory (REUSE — `D:\models\vsCodeMcp\prompts\`)

| File | Size | Role |
|---|---|---|
| `char_dataset_gpt_package.txt` | 14 KB | dataset prompt package |
| `KREA2_character_dataset_rewritten_2026-10-08.md` | 21 KB | rewritten character-dataset prompts |
| `jaisal_identity_instructions.txt` | 12 KB | Jaisal identity instructions |
| `jaisal_ref_prompts.txt` | 22 KB | reference-set prompts |
| `jaisal_sketch_prompts.txt` | 23 KB | sketch prompts |
| `zidane_v2_scenes.txt` | 4 KB | Zidhan scene prompts |
| `jaisal_single_ref_prompt{,_v2}.txt`, `jaisal_single_shot_prompt_v2…v8_{…}.txt` | 3–16 KB | shot-prompt iterations (v2–v8 — latest wins) |

## 9. RESUME PLAN (minimum to start the story — 2026-10-31)

1. **Dataset:** `krea2_realism_2mp.json` (+ `krea2_face_lock*` for approved faces,
   `k2e_zidhan_beard_sweep.json` for the beard) → 10 Jaisal + 10 Zidhan (beard in ALL Zidhan)
   into a NEW `data\<run>\` dir.
2. **Cure** per §4 → **user approves the set** (show all 20).
3. **Train:** Fizgig → `krea2fp_v3` (rank 32, 15–20 epochs, triggers `jeskvman`/`dlorman`,
   LoRA Isolation) → copy `krea2fp_v3_epNN.safetensors` to shared `loras\`.
4. **Verify:** `krea2_charlora_v3.json` with the new LoRA @1.0 → strict bar → user verdict.
5. **Record:** EXPERIMENTS.md + this file's §0 + PENDING_ITEMS P3.
6. **Then P4 unblocks** (H3 R2V for the 6 scenes) — the character LoRA is the identity pin.
