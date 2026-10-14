# episode1/workflows/

Reusable ComfyUI workflow JSONs for Episode 1 scenes (UI format — `nodes` list +
`links` array, per AGENTS.md).

## Naming
`<scene>_<purpose>.json` — e.g. `scene3_mindtrip_1950_i2v.json`,
`scene1_academy_ground_kf.json`.

## What goes here
ONLY workflows that are **reusable and needed in the future** (per the 2026-10-14 git
standard, D131):
- Reusable = another scene/session will re-run it, or it is the known-good version of
  a pipeline step.
- NOT here: one-shot test workflows, broken attempts, generated images/videos/audio
  (those are gitignored and live under `data/` / ComfyUI outputs).

## Git rule
Workflows are **not** part of the daily auto-commit. When a workflow here is
finalized as reusable, commit it explicitly:

```powershell
git -C D:\models\vsCodeMcp add episode1/workflows/<file>.json
git -C D:\models\vsCodeMcp commit -m "episode1: <what it does> (reusable)"
```

## Before using a workflow from here
Read `DECISIONS_EPISODE1.md` (scene decisions) + the scene in
`episode1_script_part1.md` first — the workflow is the vehicle, the script + decisions
are the spec.
