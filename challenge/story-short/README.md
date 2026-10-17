# Story-Short

**One prompt → a short narrative film with a consistent character.**

Story-Short is an open-source ComfyUI pipeline that turns a text description into a
multi-shot short film where the same character keeps the same face across every shot.
Built for the [Open Source Higgsfield challenge](https://comfy.org/open-source-higgsfield).

## The pipeline

```
 your prompt
     │
     ▼
┌─────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ 01 · Character      │ ──▶ │ 02 · Identity       │ ──▶ │ 03 · H3 R2V shots    │
│ sheet (Krea2 t2i)   │     │ reference set       │     │ (MiniMax H3, 2-ref   │
│                     │     │ (Krea2 identity     │     │ anchors per shot)     │
│                     │     │ edit LoRA)          │     │                      │
└─────────────────────┘     └──────────────────────┘     └──────────────────────┘
                                                              │
                                                              ▼
                                                     assembled film
                                                     (ffmpeg concat)
```

1. **Character sheet** — Krea2 (turbo, fp8) renders a multi-angle character sheet
   from your description. Natural skin texture, no plastic look.
2. **Identity reference set** — the `krea2_identity_edit` LoRA regenerates any scene
   *keeping the exact face and identity* from the sheet. A set of 4–8 references
   (frontal, 3/4, profile, in-scene) anchors the character for video.
3. **H3 R2V shots** — MiniMax H3 (open weights) animates 2–3 reference anchors into
   15-second shots with native audio. Two references per shot, each mapped 1-to-1 to
   a shot, keeps the character on-model far better than 5-anchor storyboards.

## Why the character stays consistent

- **Face locking happens before video, not in it.** Video models drift; a face locked
  at the image stage (identity-edit LoRA, `ref_boost` ≈ 4) survives the whole shot.
- **2 anchors per shot, simple prompt.** H3 animates *between* clear anchors; it
  follows short, concrete shot descriptions. See `docs/PIPELINE.md` for the prompt
  structure.
- **One climate.** Keep lighting consistent across shots (once rain starts, it
  stays moody) so H3 can bridge shots smoothly.

## Requirements

- ComfyUI (recent, with H3 support) — see `docs/PIPELINE.md` for the node pack list.
- Models — see [`MODELS.md`](MODELS.md) (all open-weights; H3 files are official
  Comfy-Org/MiniMax-H3 releases).
- ~32 GB VRAM for the Krea2 fp8 UNet + H3 chain (lower-VRAM variants exist).

## Quick start

1. Download the models listed in [`MODELS.md`](MODELS.md) into your ComfyUI `models/` folders.
2. Load `workflows/01_character_sheet.json` → enter your character description → queue.
3. Load your best sheet image into `workflows/02_identity_refset.json` → enter the scenes
   you want → queue (one run per scene, or branch it).
4. Pick 2 reference images per shot, load into `workflows/03_h3_r2v_2ref.json`, write the
   shot prompt (template in `docs/PIPELINE.md`) → queue.
5. Concat the shots: `ffmpeg -f concat -safe 0 -i shots.txt -c copy film.mp4`.

## Audio

Prompts in this repo are written for **natural soundscapes only** (no score, no
instruments, no beat) — footsteps, wind, water, ambient. Add dialogue or SFX by
describing them in the H3 prompt's audio section.

## License

MIT — see [LICENSE](LICENSE). The `krea2_identity_edit` LoRA was trained by the
authors for character consistency and is released with this repo.

## Credits

- Krea2 — Krea AI
- MiniMax H3 — MiniMax / [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3)
- Krea2Edit node pack — Comfy-Org
- H3 node packs — see `docs/PIPELINE.md`
