# 13 — SHOT → PLATE MAP (operational background-consistency reference, 2026-11-27)

Built from `06_SCENE_CONTINUITY_MAP` (scene states) + `11_MAJOR_LOCATION_PLATES_RICH`
(plates + USE FOR lines). This is the lookup for the H3 chain: **every shot = its
scene's plate(s) as `ref_image_0` (environment anchor) + character refs + the scene's
ENVIRONMENT BLOCK below, appended into the R2V prompt's `detailed_description`.**

## THE 3-LAYER RULE (background consistency)
1. **Plate anchor** — feed the shot's plate (`11` doc) as `ref_image_0`; the shot
   "begins from <Picture 1>" (D020 pattern: 1 environment anchor + character refs,
   simple prompt).
2. **Environment block** — the scene's block below goes verbatim into
   `detailed_description` (time of day, weather, mud state, colour state, kit state).
3. **ENV tail + ENV negative** (from `11`, every plate AND every character shot):
   - tail: `empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`
   - negative: `people, humans, persons, faces, hands, crowds, players, text, watermark, logo, cartoon, 3d render, plastic smooth look, beauty retouching, brand logos, legible printed text`
   - 1950 shots: plates are generated in colour, **graded B&W in post** (the colour
     survivors per `06` get their grade lifted selectively).

## PART 1 (2026, COLOUR) — scene → plate
| Sc | Location · state (`06`) | Plate(s) |
|---|---|---|
| 1 | L01-L03 · dawn · Jaisal O1 (vest + mundu), Grandpa white · Azan | **F1** (exterior, Azan), **F2** (bedroom), **F3** (kitchen), **F4** (Grandpa's room) |
| 1A ⊕ | L01 · dawn | F1, F2 |
| 2 | L04→L05 · morning · Zidhan mustard logo tee, kids' clean-dirty kits | **F5** (backyard/parambu) |
| 2A ⊕ | L05 · morning | F5 |
| 3 | L05, L06 · near noon · formal Father · spray can, "SPRAY: 0", car | **GAP — no street plate (see bottom)** |
| 4 | L03, L04 · midday · Jaisal teal hibiscus tee, muddy hands | **F4** (Grandpa's room), **F5** (backyard), **F6** (washbasin insert), **F7** (veranda) |
| 5 | L07 · afternoon · Rayyan in kit + sandals | **GAP — no L07 plate** |
| 5A ⊕ | L07 · afternoon | GAP (same as 5) |
| 6 | L08 · 6 PM golden · Winning Eleven kits splashed, Rockstar black stars | **C1** (wide from gallery), **C2** (reverse from pitch), **C4** (gallery rail), **C5** (sideline corner) |
| 25 | L03 · night · full colour · watch buckled on Grandpa | **F4** (Grandpa's room, night) |

## PART 2 (1950, B&W + colour survivors) — scene → plate
| Sc | Location · state (`06`) | Plate(s) |
|---|---|---|
| 7 | L10 · amber · one sandal in the mud | **B1** (silent stadium, wide), **B2** (sandal insert), **B3** (gallery steps) |
| 8 | L11 · afternoon gold · the only colour in the village | **GAP — no L11 plate** |
| 9 | L12, L19 · late afternoon → night | **D1** (shore at dusk), **D1a** (MARJAN far), **D3** (pathemari at night) |
| 10 | L13-L17 · gold, noon · five-shot recruitment | **E1** (coconut grove), **E2** (sea shallows), **E3** (arecanut grove, THE X), **E4** (coir beach), **E5** (market alley) |
| 11 | L12 · dusk · Jaisal gives the boy the watch | **D1** (shore), **D1b** (gangplank, boarding) |
| 12 | L18 · dawn · coconut mountains | **D2** (MARJAN deck at dawn) |
| 13 | L20 · dawn · fire in gold, the NOT burns first | **GAP — no L20 plate** |
| 14 | L21→L18 · morning · muted | **D2** (deck), **D2c** (cabin, route map — 14A) |
| 15 | L22, L18 · all day / night · greying daily | **D2** (deck), **D2a** (deck at night), **D2b** (open sea above), **D2d** (mast, the X) |
| 16 | L23-L25 · misty dawn · grey · sung anthem | **A2** (tunnel, 16-06..09) — **16-01..05 = GAP** |
| 17 | L26 · day · India vs Sweden, the X, 4-0 | **A1** (Maracana dry overcast) |
| 18 | L25/L27 · day · Italy, Paraguay | **GAP — 18-xx unassigned (nearest: A1)** |
| 19 | L26 · day · India vs Brazil, the wingers' X | **A1** |
| 20 | L28 · night · the quarrel | **D2a** (deck at night), **D4** (Rio quay at night), **C5** (20-04 sideline) |
| 21 | L26 · day · India vs Spain | **A1** |
| 22 | L26 · day, rain · soaked mud | **A0** (Maracana rain hour HERO) |
| 23 | L26→L08 · rain → 6 PM golden · grey → colour floods | **A3** (pitch-edge rail, 23-01..03), **C1** (23-04..06), **C3** (scoreboard 3-1, 23-06), **C4** (mirrored handshake) |

## SHOT-LEVEL INDEX (from `11` USE FOR lines — the exact per-shot lookup)
- **F1** → 1-01 · **F2** → 1-02, 1-03, 1A-01 · **F3** → 1-04 · **F4** → 1-05..1-07, 4-01, 4-09..4-11, 25-01..25-05
- **F5** → 1-08, 2-01, 4-02..4-07 · **F6** → 4-08 · **F7** → 4-01
- **C1** → 6-01..6-14, 23-04..23-06 · **C2** → 6-03, 6-04 · **C3** → 23-06 (3-1 in post) + 0-0 version for S6 · **C4** → 6-05, 6-11, 23-04 · **C5** → 6-02, 6-03, 20-04
- **B1** → 7-01..7-07 · **B2** → 7-01 (insert) · **B3** → 7-04
- **D1** → 9-01, 9-02, 11-01..11-08 · **D1a** → 9-01 · **D1b** → 11-03, 11-08 · **D2** → 12-01..12-06, 14-03, 15-02..15-06 · **D2a** → 15-08, 20-01..20-06 · **D2b** → 15-01, 15-07 · **D2c** → 14A · **D2d** → 15-03 · **D3** → 9-07, 9-08 · **D4** → 20-01, 20-06
- **E1** → 10-01..10-04 · **E2** → 10-05..10-07 · **E3** → 10-08 · **E4** → 10-09, 10-10 · **E5** → 10-11..10-13
- **A0** → 22-01, 22-03..22-10 · **A1** → 17-01, 19-01..19-06, 21-01, 21-02 · **A2** → 16-06..16-09 · **A3** → 23-01..23-03

## ENVIRONMENT BLOCKS (verbatim, per scene — append into `detailed_description`)
- **Sc 1 (dawn):** "Kerala village at first light, the azan just ending, thin blue-grey dawn haze, wet veranda tiles, oil lamp glow inside, no wall photographs."
- **Sc 2-3 (morning → noon):** "Kerala street in bright morning, coconut palms and the Activa, then near-noon flat white light, a car parked by the boundary wall, spray can and notepad on the ground."
- **Sc 4 (midday):** "Midday hard light, Jaisal's teal hibiscus tee with muddy hands, the boar and shovel in the yard, Grandpa's room half-dark against the bright yard."
- **Sc 6 (6 PM golden):** "The village ground at 6 PM golden hour, low backlight through the coconut palms, splashed Winning Eleven kits, the speaker on its stool, banners on bamboo poles."
- **Sc 7 (amber mind-trip):** "The same village ground in amber golden hour, completely silent, one rubber sandal in glossy red-brown mud, the plank gallery empty, scoreboard 0-0, one watch tick as the only sound."
- **Sc 8 (afternoon gold):** "The village square in warm afternoon gold — the only fully-colour space in the 1950 village."
- **Sc 9 (late afternoon → night):** "The shore at dusk, MARJAN anchored close, then pathemari at night, firelight on wet sand, the telegraph form written on the ground."
- **Sc 10 (gold noon):** "Recruitment ground at gold noon — coconut grove, sea shallows, arecanut grove, coir beach, market alley; five separate shots, same warm hard light."
- **Sc 11 (dusk):** "The shore at dusk, the team line on the gangplank, Jaisal handing the boy the watch."
- **Sc 12 (dawn, sea):** "MARJAN deck at dawn, coconut mountains on the horizon, the first coconut floating away, muted grey-gold light."
- **Sc 13 (dawn fire):** "Dawn, a fire burning in gold, the word NOT burning first."
- **Sc 14-15 (voyage, muted → greying daily):** "Open sea in muted light, then the days grey out one by one; the coconut stock shrinking on deck; the mast and the X at the top."
- **Sc 16 (misty dawn):** "The stadium approach in misty grey dawn, the sung anthem, a sea of small shapes of hats and paper flags in the distance."
- **Sc 17-19, 21 (group matches, dry):** "The vast 1950 concrete bowl on a dry overcast day, flat soft light with no shadows, the small open-hand banner almost lost against the vastness."
- **Sc 20 (night, quarrel):** "The MARJAN deck at night, then the Rio quay at night, the quarrel in the dark, one bare bulb."
- **Sc 22 (rain hour):** "The Maracana under heavy overcast after hours of rain, the pitch a swamp of dark red-brown glossy mud exactly like a Kerala paddy field, white lines vanishing under standing water."
- **Sc 23 (rain → golden):** "Rain thinning to mist over the pitch, then the 6 PM golden flood back into colour; the rail, the 360° spin, the scoreboard 3-1."
- **Sc 25 (night, home):** "Grandpa's room at night, the watch buckled on Grandpa's wrist, sand falling."

## GAPS — scenes with shots but NO plate assignment in `11` (author decision needed)
1. **Sc 3** (L05/L06 street, spray-can scene) — no street plate. Options: new plate (G1 — "the street, near noon") or derive from F5/F7 context.
2. **Sc 5/5A** (L07, Shafiq's home, Rayyan) — no L07 plate. New plate (G2 — "the neighbour's house, afternoon")?
3. **Sc 8** (L11, the only-colour village square) — new plate (G3)?
4. **Sc 13** (L20, dawn fire) — new plate (G4) or a D1-derive (shore at dawn)?
5. **Sc 16, shots 16-01..05** (L23-L25 approach, before the tunnel) — A2 covers 16-06..09 only.
6. **Sc 18** (L25/L27, Italy/Paraguay) — unassigned; nearest = A1 (same bowl, different light?).

## GENERATION QUEUE (35 plates, `krea2_t2i_env_cine.json`, 2048x1152, paste file `utilities\ep1_major_prompts_paste.txt`)
A0, A1, A2, A3 · B1, B2, B3 · C1..C5 · D1, D1a, D1b, D2, D2a, D2b, D2c, D2d, D3, D4 · E1..E5 · F1..F7.
Any new G-plates from the gap list get appended to this queue (prompts written in `11` style: full description + ENV tail + ENV negative, no people, 1950 plates in colour → B&W in post).
