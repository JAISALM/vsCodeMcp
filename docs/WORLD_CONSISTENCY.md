# World / Location Consistency (2026-11-16)

Standing system for **location + scene consistency** across all shots of the film.
Built on the proven H3-Image reference-anchor mechanism (same as pose refs):
a reference slot is an anchor — pose ref locked the body, a panorama ref locks
the world.

**Status:** rig built + validated 11-16 (`h3image_world_shot.json`, 0/0, 15/15
wires in real frontend). PENDING: first panorama generation (user queues).

---

## Core idea — the WORLD BOOK

One canonical **master panorama per location** = the single source of truth for
that location. Every image and every video at that location is derived from it,
so the world cannot drift between shots.

```
LOCATION BIBLE (text, fixed)          ← stage 0
        ↓
MASTER PANORAMA (wide, no people)     ← stage 1  → input\world_<LOC>_pano.png
        ↓
ANGLE SET (optional, 2-4 views)       ← stage 2  → input\world_<LOC>_<angle>.png
        ↓
SHOT STILLS (character in world)      ← stage 3  → h3image_world_<loc>_*
        ↓
VIDEO (animate the still)             ← stage 4  → H3 R2V rig
        ↓
CONTINUITY QA (side-by-side grid)     ← stage 5
```

---

## Stage 0 — LOCATION BIBLE (write this FIRST, reuse VERBATIM)

6-8 lines, one per location, reused in every prompt at that location —
the same discipline as the character bible (D137) that solved face consistency.

Template (bridge example — the film's first location):

```
LOCATION BIBLE — LOC-A: the old stone bridge over the backwater
- old stone bridge, SQUARE plain handrails (no ornate/round/staircase details)
- wide open river below (NOT a canal, NOT a bund), dark green monsoon water
- wet stone surface, low mist on the water, lush tropical vegetation on the banks
- one streetlamp at the bridge end, slightly bent
- overcast monsoon daylight, moody subdued tone, muted desaturated palette
- no signage, no modern buildings in frame
```

Rules (D024 climate consistency):
- ONE climate tone per location — once rain starts, keep the moody tone on ALL
  shots of that location.
- The architectural SIGNATURE lines (square railings, open river) go into
  EVERY prompt at that location — these are the continuity check points.

---

## Stage 1 — MASTER PANORAMA (wide establishing view)

- **Rig:** `h3image_world_shot.json` in PANO PASS:
  - UNWIRE the face LoadImage (node 4 → image_0) — pure world pass, no people.
  - Prompt = the location bible + `empty scene, no people, no humans, no
    figures, wide establishing view`.
  - Width/height (conditioning widgets): **3392×1184** (21:9 wide, ~4 MP).
  - Seed: fixed 77 for the first attempt; vary only if re-rolling.
- Save the best take to `input\world_<LOC>_pano.png`
  (root of `input\` — keeps the LoadImage widget a plain filename).
- Iterate 2-4 takes until the location "feels right" — this image is now THE
  location. Judge: railings square? river open? palette = the bible?
- **Style seed (optional):** if the H3-Image world doesn't carry the film's
  Krea2 angular-brush look, generate a Krea2 t2i of the same location
  (`krea2_t2i_char1.json` rig, latent node 82 → wide 1664×928) and feed it as
  a STYLE reference (image_0) while keeping the H3 world panorama as image_1.
  H3-Image drifts to its own look (D021) — a Krea2 style ref pulls it back.

## Stage 2 — ANGLE SET (when shots need other camera angles)

One panorama = ONE camera angle. A shot from a different angle makes H3-Image
re-derive the unseen geometry (hallucinated back of the bridge). Prevent it:

- For each needed angle (front / side / wide / low-from-water), generate it
  FROM the master: same rig PANO PASS + `world_<LOC>_pano.png` wired as image_1
  (face still unwired) + prompt = bible + `camera: SIDE view of the same
  bridge, same square railings, same open river`.
- Save as `input\world_<LOC>_<angle>.png`.
- 2-4 angles per location is enough for the film.

## Stage 3 — SHOT STILLS (character in the world)

- **Rig:** `h3image_world_shot.json` in SHOT PASS:
  - face LoadImage (node 4) → `image_0` = `jaisal_face_frontal.png` (identity)
  - world LoadImage (node 5) → `image_1` = `world_<LOC>_<angle>.png` (world)
  - optional: wire a third LoadImage to `image_2` for a pose ref
    (H3-Image conditioning has 5 ref slots `image_0..4`)
  - Prompt = character (D137 description) + `<ACTION>` +
    `The location is EXACTLY the second reference image: same architecture,
    same railings, same river, same props, same light` + `[SCENE: camera
    angle, cinematic]`
  - Width/height: **2560×1440** (16:9) for shot stills.
- Check against the bible's signature lines before accepting.
- **Pose tweak after a good still:** VNCCS (background frozen, pose-only) —
  the user's confirmed split: H3-Image = the cinematic shot with max character
  detail; VNCCS/pose = position tweaks on the finished still (11-16).

## Stage 4 — VIDEO (animate the still)

- Existing H3 R2V rig (no new build). Reference layout (D017/D020 rules):
  - `ref_image_0` = the SHOT STILL (first-frame anchor — the video begins
    exactly from this frame)
  - `ref_image_1` = face/character ref (identity)
  - `ref_image_2` = `world_<LOC>_pano.png` (world anchor — optional but
    recommended for long takes; 2-3 refs max, each with a clear job)
- Short prompt, official R2V 6-section style (`docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md`),
  NO-music rules (D041).
- The panorama keeps the world coherent even when the character moves out of
  frame; the still anchors the first frame.

## Stage 5 — CONTINUITY QA

- Per location, build a side-by-side grid: panorama + all accepted shots.
- Check the bible signature lines on every shot (railings square? river open?
  one climate tone? palette match?).
- Rejected shots = re-roll with the matching ANGLE ref, not the master, when
  the angle differs.

---

## Naming convention

| Asset | Path |
|---|---|
| master panorama | `input\world_<LOC>_pano.png` |
| angle views | `input\world_<LOC>_<angle>.png` |
| shot stills (output) | `h3image_world_<loc>_*.png` (rig prefix `h3image_world`) |
| location bibles | this doc, "Location bibles" section below (one block per location) |

`<LOC>` = bridge · village · interior · boat · … (film locations, TBD per scene list)

---

## Failure modes + mitigations

| Symptom | Cause | Fix |
|---|---|---|
| location architecture drifts (round railings, canal) | H3-Image re-derives instead of copying the ref | stronger anchor text ("EXACTLY the second reference image") + bible signature lines in prompt |
| unseen geometry hallucinated (back of bridge) | shot angle ≠ panorama angle | use the matching ANGLE SET image, not the master |
| world loses the Krea2 film style | H3-Image prior (D021) | Krea2 style ref as image_0 + H3 world pano as image_1 |
| climate jumps between shots | no bible discipline | D024: one tone per location, climate line in bible |
| world ref too small in output | H3-Image scales refs internally | keep panorama ≥4 MP wide; shot canvas 2560×1440 |
| character duplicated | Krea2/H3 quirk | "ONLY ONE character, no other people" line; re-roll seed |

## Multi-person + world

Orthogonal: add one face ref per character (`image_0` = char1 face,
`image_1` = char2 face… shift world/pose refs up the slots). The multi-person
workflow test is pending; world refs work the same way regardless.

---

## Location bibles

(Write one block per location here, using the Stage-0 template. Bridge =
LOC-A example above — finalize wording when the first panorama is accepted.)
