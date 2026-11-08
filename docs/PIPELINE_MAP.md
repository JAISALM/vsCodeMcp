# PIPELINE_MAP — how we get a shot done (state 2026-11-08)

Single source of truth for "how things get done." If you lost track, read this first.

## The stack (what we have, verified working)

| layer | what | where |
|---|---|---|
| brain | Qwen3.8-27B (llama.cpp, :8100) — planning/writing/agent | `D:\models\qwen` |
| stills | ComfyUI (:8188) + **Krea2 cine rig** (the proven recipe — see WORKFLOW_HISTORY.md top note) | `E:\comfyUi_latest` (running) · models `E:\ComfyUI_windows_portable\ComfyUI\models` |
| character LoRAs | `krea2jaisal_v2` (`jeskv`) · `krea2zidhan_v2` (`dlor`) · `krea2jaisal_v3` (`jaiv3`) · `krea2zidane_v3` (`zidv3`) — all in `models\loras\` | |
| video | MiniMax H3 (R2V from our stills; 2–3 refs, short prompt, 6-section R2V style D017/D020) | |
| audio | ControlFoley SFX — **NO music ever (D041)** | |
| LoRA training | AI-Toolkit V3 kit (`launch_*V3.bat` — user runs, D192) | `E:\AI-Toolkit-Easy-Install` |

## Who owns what (LoRA vs prompt) — the division of labor

| dimension | owner |
|---|---|
| face identity | **LoRA** (core) |
| hair | **LoRA** |
| skin color | mostly **LoRA** (in training images); lighting words nudge |
| build | **v2 LoRAs: prompt** (face-sheet trained — they know no body) · **v3 LoRAs: LoRA** (full-body-dominant training) |
| hands | base model + LoRA if hands were in the sheet |
| clothing | **prompt** (always explicit; LoRAs carry a mild tee bias) |
| pose / action / lighting / background / camera | **prompt** |
| count / positions / relative scale | **prompt** (base pass) |
| identity inside a multi-char frame | **the inpaint pass** (that character's mask band + their solo LoRA @1.0) |

## The standard shot loop (the only loop)

1. **Still (multi-char):** `krea2_quad_base.json` (LoRA-free base — 4 generic men, distinct outfits, build words, count guards) → check exactly 4 men → `krea2_quad_inpaint_1..4` sequential (each: LoadImage prev output, MaskRectArea band, solo LoRA @1.0, denoise 1.0) → check faces + scale + no bleed.
   - Two characters → `krea2_duo2pass_base.json` + `krea2_duo2pass_inpaint.json` (same idea, 1 pass).
   - One character → single cine file (e.g. `Krea2_jaisal_v2_cine.json` pattern) → judge.
2. **Video:** best still(s) → H3 R2V (2–3 refs max, each = a shot anchor, short prompt, 6-section D017; D020).
3. **Audio:** ControlFoley SFX from the video — natural ambience only (D041).
4. **Edit/assemble:** (final cut).

## What is FIXED vs EXPERIMENTAL

- **FIXED (proven, stop re-litigating):** Krea2 cine rig (recipe card) · identity-edit v1.2 (D023) · two-pass/quad multi-char technique (D214/D216 — the only reliable multi-char method; stacked LoRAs and Composer are exhausted) · v91 dataset generation · V3 LoRA training recipe · the LoRA-vs-prompt division above (D217).
- **EXPERIMENTAL (still being A/B'd):** H3 video chain (tiny sliders; TurboH3 FL2VA i2va pruned INT8 ConvRot — new 11-08; H3 drop-in KSampler speed-up — new 11-08) · Ideogram 4/4.5 as stills base (4.5 open-sourcing — watch item; A/B when it drops; **not a blocker** — current stack is enough).

## Pending items (the whole plate, 2026-11-08)

**Blocked on user info:**
- [ ] **2 new characters** → names + triggers + one-line descriptions → finalize quad `_3`/`_4` (still placeholders) + their LoRAs (v3 pattern if recurring).

**User GPU queue (free all day 11-08, marathon from 11-09):**
- [ ] **Quad kit run** — `quad_base` → `_1`→`_4` (fresh tabs, mask checks).
- [ ] **`krea2_duo2pass_inpaint.json`** on the existing duo base (left man → zidhan).

**Agent-ready on signal (no GPU needed):**
- [ ] **akatz V1.5 Character-Swap A/B wiring** (both versions local; user's go/no-go pending) — agent builds + validates, user runs.
- [ ] **Fat character (FUTURE, per user 11-08 — the fat/skinny example was a future scenario, not the current 2):** when he becomes recurring → full-body-dominant dataset + `aitk_*V3.yml` (agent builds, user runs the bat). Relative-scale contrast = base prompt (D217).

**Watch items (read-when-bored, no action):** unsloth Flash-Next V3.1 A/B (brain) · Krea 3 tech report · H3 image-edit workflow · gemma4 PR #31356 · Hy4 · Krea2 Turbo 133K LoRA · LTX 2.5 low-VRAM workflow · 0.1B embeddings (RAG upgrade) · KV-cache quant for Qwen3.8 27B.

## Rules that never change (hard constraints)

- **D192:** agent never queues GPU jobs — user runs ComfyUI/training.
- **D212:** native `LoraLoaderModelOnly` only.
- **D041:** no music, ever.
- **D216/D217:** multi-char = LoRA-free base + per-character mask inpaint (never stacked LoRAs, never Composer).
- **D131:** commit after every .md change.
