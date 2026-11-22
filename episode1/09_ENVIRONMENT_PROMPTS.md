# 09 — ENVIRONMENT REFERENCE PROMPTS (no people, no faces)

**Purpose:** environment-only reference images (backdrop plates) for every location.
Characters are NEVER in these — they are composited / identity-edited in later.
**Source:** set dressing from `03_LOCATIONS.md` · style + negatives from `00_INDEX_AND_RULES.md`.
**Rule (ERA):** 1950 locations are generated IN COLOUR (character sheets stay colour) and
graded B&W in post — do NOT generate black-and-white 1950 plates.

## WORKFLOW

`movies\sheets\krea2_t2i_env.json` (copy of the char1 rig, environment-tuned):
- 2048×1152 (16:9) default — override per card if noted
- prefix `ep1_env_`
- negative = the ENV negative below (people/face exclusion), NOT the character negative
- style LoRA (famegrid) zeroed for a clean documentary look; realism LoRA kept
- paste ONE card per queue from `utilities\ep1_env_prompts_paste.txt` (order = below)

**ENV STYLE TAIL** (end of every card):
`empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

**ENV NEGATIVE** (already in the workflow's negative node):
`people, humans, persons, faces, hands, crowds, players, text, watermark, logo, cartoon, 3d render, plastic smooth look, beauty retouching, brand logos, legible printed text`

## BATCH 1 — 2026 PRIORITY (shoot order, scenes 1→6)

### 1. L01 — Jaisal's bedroom (S1, 1A — dawn, blue→pale gold)
`An empty Kerala village bedroom at dawn, blue light shifting to pale gold through one small window, a thin cot bed with rumpled cotton sheets, one plastic chair, a stopped wall clock, muddy football socks draped over the window bar, a football half-hidden under the cot, bare laterite walls, NO wall photographs, low wide frame, {ENV STYLE TAIL}`

### 2. L02 — Kitchen (S1 — dawn)
`An empty small Kerala village kitchen at dawn, a steel kettle steaming on a wood stove, fresh mint in a glass, steel drinking glasses on a counter, a small fridge with mint on top, dim blue-gold dawn light, thin steam in the air, tight close frame, {ENV STYLE TAIL}`

### 3. L03 — Grandpa's room (S1, 4, 25 — dawn / late afternoon / night)
`An empty old Kerala bedroom, a wooden chair facing a window, a small wooden table with a glass of tea and a small pocket watch, a ceiling fan, plain walls, still and quiet, early dawn light through the window, wide still frame, {ENV STYLE TAIL}`
*(re-render variants later: late-afternoon light, night with a lamp — same set)*

### 4. L04 — Backyard / parambu (S1→2, 4 — morning)
`A cluttered Kerala village backyard in the morning, coconut palms, wet dark red earth, a freshly dug shallow grave pit with a shovel beside it, a washbasin, chicken-feed scraps, dogs far in the background, wide cluttered frame, soft morning light, {ENV STYLE TAIL}`

### 5. L05 — Paddy training ground (S2, 2A, 3 — late morning, hard sun)
`A muddy paddy-field football pitch under hard late-morning sun, a dead bandicoot in the centre circle as a no-go marker, six stones in a short drill line, farmers at the far edges, wet green paddy around the mud, coconut palms, high-contrast hard sun with short shadows, wide frame, {ENV STYLE TAIL}`

### 6. L06 — Field edge / road (S3 — near noon)
`The edge of a green paddy field near noon, a dented white Ambassador car parked on the dirt road at the field edge, hard noon glare, long dust, wide frame, {ENV STYLE TAIL}`

### 7. L07 — Shafiq's house + pathway (S5, 5A — afternoon)
`The front of a Kerala village house in the afternoon, a clothes line with drying cotton clothes, a narrow dirt path, one coconut palm, a dropped coconut on the path, crows in the branches, warm slanting afternoon light, medium-wide frame, {ENV STYLE TAIL}`

### 8. L08 — The match ground, 5-a-side (S6, 23 — 6 PM, low golden light) ⭐ TEAM BACKDROP
`A small 5-a-side football ground at 6 PM in low golden light, plank-and-bamboo gallery seating on one side, a boundary rope, a hand-painted bedsheet banner on two bamboo poles with a round open-hand emblem, an empty ticket-booth post, a portable speaker on a stool, a wooden scoreboard with sliding numbers, wet green paddy and coconut palms behind, the pitch mud glossy in the last light, wide frame, {ENV STYLE TAIL}`

**THIS ONE IS THE TEAM-SHOT BACKDROP** — the team lineup (kit refs or composite) gets placed on this plate.

## BATCH 2 — 1950 (generate COLOUR, grade B&W in post) — later

| # | Location | Note |
|---|---|---|
| 9 | L10 Silent stadium (S7, 7A) | **the same ground as L08 in amber golden hour, EMPTY, one rubber sandal in the mud** — must rhyme with L08/L26 (same gallery proportions, same mud). Best: derive from the L08 plate. |
| 10 | L11 Village road and fork (S8) | tin-roofed tea shop, a well, a tailor's stall, fence posts, the road forking to groves and sea, afternoon gold |
| 11 | L12 Shore (S9, 11) | fishing nets on poles like cobwebs, the boat MARJAN anchored far then near, a gangplank, late afternoon → dusk |
| 12 | L15 Arecanut grove — THE X SPOT (S10C) | two tall thin arecanut palms side by side bending and crossing in an X, gold shafts of light — **the set-piece; the X is reused in scenes 17, 19, 22 and on the mast** |
| 13 | L18 MARJAN deck + cabin (S11, 12, 14, 14A, 15, 20) | huge square sail, painted bow eyes, rope coils, a cabin with a hand-painted route map and a swinging lantern — the big one |
| 14 | L26 Maracanã (S17–19, 21–23) | gallery, rail, a mud pitch that looks exactly like the Kerala paddy, white lines vanishing in rain — **BIG; the climax plate** |

## HANDOFF (user, D192)

1. Fresh tab → `krea2_t2i_env.json` → paste card 1 (L01) → queue. Repeat per card (8 queues = batch 1).
2. Outputs land in `output\ep1_env_*`. Tell me when done → I pick the best plate per location and copy to `input\env_{L01..L08}_*.png`.
3. L08 plate = team backdrop for the composite route (rembg lineup on the L08 plate).
4. Batch 2 (1950) after batch 1 is confirmed.
