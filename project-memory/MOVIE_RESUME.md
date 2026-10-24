# MOVIE RESUME — new session, read first (2026-10-24 ~16:00 IST)

Self-contained entry point for the 2-man football movie. Read order: **this file →
`PENDING_ITEMS.md` → `CURRENT_TASK.md` header → `DECISIONS.md` (D183, D151, D041, D050).**

## The movie (2 men, rural Kerala)
- **char1 Jaisal** — ~26, warm Keralite tan, slim, **crooked naturally-bent nose** (key
  differentiator), medium wavy black hair (eyebrow length), clean-shaven / faint stubble,
  **plain black tee**.
- **char2 Zidhan** — warm Keralite tan, rounder face, **sharp angular prominent nose**
  (Dulquer-Salman-style), **full short dense beard**, short neat black hair (halal fade crop),
  **plain white tee**.
- **6 scenes FINAL (no boat):** S1 post-harvest paddy field (rain, people working), S2 behind a
  normal Kerala house, S3 inside a Kerala house, S4 on a Kerala bike, S5 minimal local 7's
  football ground (small goals, low fence, benches — NOT a stadium), S6 rural village
  (paddy + homes + palms).
- Video = **MiniMax H3 R2V** (SLA, <4 min/1 MP). **NO MUSIC (D041 — hard rule, user is Muslim).**
- **HARD DEADLINE: Nov 22.**
- Script = `episode1\` (writer track is separate — resume via `episode1\CONTINUE_SCRIPT.md`;
  writer model = Gemma4-31B QAT, creative output only, never edits existing files).

## IMMUTABLE anchors (hash-verify after EVERY batch; never regenerate/overwrite)
- `data\character_finals\jaisal_final.png` — SHA256
  `B2B4EB8C94797D68BA18D8DBB1851B4B654BCFFC34D613DD1B86A506C2511CB2`
- `data\character_finals\zidhan_final.png` — SHA256
  `D8BEBB85601E1E7470F1D18E91F92FC70650B9B2276EB2DD65BBF9A889F1565F`
  (both = byte-identical to `data\locked_refs\*_LOCKED.png`; staged to ComfyUI
  `input\{jaisal,zidhan}_final_ref.png`.)
- Milestone workflows `k2f_jaisal_crookednose.json` (run `65468343`, seed 90201) +
  `k2f_zidhan_sharpnose.json` (run `c6b83489`, seed 90101) = **DO NOT MODIFY** (D151, recorded
  in WORKFLOW_HISTORY.md "CHARACTER MILESTONE WORKFLOWS (LOCKED)").

## Current position (2026-10-24)
1. **USER REJECTED all Krea2 2-pass face-lock outputs** (all 7 Jaisal: face drift + noisy
   "2021-AI" skin + blackouts; my "good/acceptable" self-ratings were VOID). The 2-pass recipe
   (t2i base → identity-edit face-lock denoise 0.4) = **FAILED** — Krea2 cannot transfer face
   consistency consistently; face-locking a broken/random-faced base = garbage in, garbage out.
   **D183 supersedes D175 for the character route.**
2. **PIVOT (user-directed, in progress):** 20-image dataset (10 Jaisal + 10 Zidhan) from the
   fixed refs via **`flux-2-klein-9b` + `Flux2-Klein-9B-consistency-V2`** → **rank-32 LoRA,
   ~15–20 epochs, triggers `jeskvman`/`dlorman`** (~2–3 h; full rank 7 h rejected). **Zidhan
   bearded in all 10.** **User is building + running the Klein workflow himself.**
3. **Pending queue** = `PENDING_ITEMS.md`: P1 Malayalam lip-sync + audio (D050, NOT started —
   RVC + LatentSync, WSL2 verified installed), P2 Blender layout→video (proven on boar-grave;
   movie scenes not started), P3 LoRA v2 (in progress), P4 H3 R2V 6 scenes (blocked on P3),
   P5 ControlFoley SFX + DaVinci (blocked on P4), P6 SeedVR2 2K (ready). P1 and P2 are
   independent of P3 — can run in parallel.

## Standing rules
- **D041** NO music, ever (dialogue + natural ambience only). **D045** no LatentSync while
  ComfyUI is active (18 GB VRAM). **D131** commit every `.md` change in the same turn
  (`powershell -ExecutionPolicy Bypass -File "D:\models\vsCodeMcp\utilities\commit_md.ps1"`).
  **D151** characters locked. **Strict quality bar (2026-10-24):** never self-certify
  marginal outputs — show the user and ask; "good/acceptable" is NOT the bar.
- Env: ComfyUI port 8188 (`E:\comfyUi_latest` install; ALL models in
  `E:\ComfyUI_windows_portable\ComfyUI\models` via `extra_model_paths.yaml`), embedded python
  `E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe`, user TZ
  Asia/Calcutta, user works alone — results first, no groveling.

## First actions next session
1. Klein dataset state (user's run) → strict curation of the 20 → rank-32 train (~2–3 h).
2. Work `PENDING_ITEMS.md` one by one (P1/P2 parallel with P3).
