# 11 — MAJOR LOCATION PLATES (RICH, MERGED)

Merges your `10_MAJOR_LOCATIONS_RICH.md` with the cinematic layer in `09`/`10`. Every prompt keeps your **ENV tail** and uses your rig `krea2_t2i_env_cine.json` (2048x1152, 16:9, dual-LoRA: cinematic + realism). **1950 plates are generated in colour and graded B&W in post.** No plate contains people.

**ENV tail (appended to every prompt):** `empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

**ENV negative:** `people, humans, persons, faces, hands, crowds, players, text, watermark, logo, cartoon, 3d render, plastic smooth look, beauty retouching, brand logos, legible printed text`

## DECISIONS I MADE (change any)
1. **'hopuse' = the house** (Jaisal's house: exterior, bedroom, kitchen, Grandpa's room, backyard). The house is the opening location of the film, so it is section **F**.
2. **5-a-side confirmed by you.** Section C is a 5-a-side ground.
3. **The rhyme is confirmed:** same mud, same plank gallery, same rail and the open-hand banner at every scale (A0, B1, C1, A3, C4).

## FIXES MADE TO YOUR PROMPTS
- **Floodlights removed** from the Maracana (they are anachronistic for 1950).
- **B1 scoreboard now reads 0-0.** Scene 7 happens in the first half; 3-1 appears only at the return.
- **Sandal removed from the Maracana rain plate.** The single rubber sandal belongs to the 2026 ground (B1, B2).
- **Maracana kept as a real 1950 concrete bowl**, with the village echoes limited to the mud, the plank barrier and the small banner, so it does not become a hybrid.
- **Added** the Maracana tunnel, the pitch-edge rail (for the handshake), the gallery close-up, the cabin, the mast, the gangplank, and the whole house set.

## QUEUE ORDER (35 plates)
A0, A1, A2, A3 · B1, B2, B3 · C1 to C5 · D1, D1a, D1b, D2, D2a, D2b, D2c, D2d, D3, D4 · E1 to E5 · F1 to F7. Paste file: `utilities/ep1_major_prompts_paste.txt` (one prompt per line, same order).

---

## A0 — Maracana, rain hour (the Uruguay match) HERO
**Scenes:** S22, S23 first half · **Era:** 1950 (colour, grade B&W in post) · **Light:** heavy overcast, hours of rain, wet highlights · **Sound:** the roar of a huge crowd (claps only), rain on mud, a whistle

**PROMPT**
```
A vast 1950 concrete football stadium bowl under a heavy overcast sky, rising tiers of raw wet concrete stained dark with rain, stairways dividing the sections, an open upper rim against grey cloud, rain falling in thin silver sheets, the pitch a swamp of dark red-brown glossy mud exactly like a Kerala paddy field, the white lines vanishing under standing water, churned boot-marks and long puddles reflecting the grey sky, white-painted timber goalposts with rope nets, a low timber barrier and plank benches along the pitch edge echoing a village ground grown huge, a wooden scoreboard with sliding numbers at the far end, a hand-painted bedsheet banner on two bamboo poles at one corner with a small round open-hand emblem, wet concrete steps running with water, wide frame from the opposite gallery, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The paddy field has grown to the size of the world: the struggle is the same at every scale.
**MUST-SEE OBJECT:** a small hand-painted open-hand banner tied to a plank barrier
**AVOID (generic):** a glossy modern stadium, floodlights, a crowd of faces

**BRIEF / USE:** WHO: no one (plate). WHERE: A0. FEELING: the paddy field grown to the size of the world. USE FOR: 22-01, 22-03 to 22-10.

**NOTE:** NO floodlights (they are anachronistic for 1950). RHYME: mud texture, plank barrier and the open-hand banner must match C1 and B1.


## A1 — Maracana, dry overcast day (group matches, Brazil, Spain)
**Scenes:** S17-19, S21 · **Era:** 1950 · **Light:** flat overcast, dry, soft light · **Sound:** a crowd's roar, claps, a ref's whistle

**PROMPT**
```
The same vast 1950 concrete stadium bowl on a dry overcast day, tiers of pale weathered concrete packed with a sea of small shapes of hats and paper flags in the distance, the pitch worn grass with patches of bare earth and fresh white lines, white-painted timber goalposts with rope nets, a low timber barrier along the pitch edge, the wooden scoreboard at the far end, a thin round open-hand emblem banner on two poles at one corner, soft grey light with no shadows, wide frame from the opposite gallery, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Scale: a tiny team before a sea of strangers.
**MUST-SEE OBJECT:** the small open-hand banner almost lost against the vast concrete
**AVOID (generic):** fireworks, triumphant glamour

**BRIEF / USE:** WHO: no one. FEELING: scale and hush before the whistle. USE FOR: 17-01, 19-01 to 19-06, 21-01, 21-02.

**NOTE:** Crowd is a separate layer added in post; keep faces tiny and far.


## A2 — Maracana tunnel (anthem, entrances)
**Scenes:** S16, S17 · **Era:** 1950 · **Light:** overcast daylight spilling in like a doorway · **Sound:** footsteps, a flag snapping, a hush

**PROMPT**
```
A long narrow concrete stadium tunnel in 1950 opening onto the pitch, wet brick walls, a single bare bulb on a cord, a low arched ceiling, puddles on the floor catching the overcast daylight, the bright rectangle of the pitch and the packed tiers beyond, a flagpole with a flag snapping in the wind at the opening, low frame at ankle height looking toward the opening, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The walk from shadow into light: the moment before everything is decided.
**MUST-SEE OBJECT:** a bare bulb above the dark and a blazing bright opening at the end of the tunnel
**AVOID (generic):** a grand hero entrance

**BRIEF / USE:** WHO: no one. FEELING: the walk out. USE FOR: 16-06 to 16-09.

**NOTE:** The band is optional; silent instruments only, or replace with a uniformed ceremonial party.


## A3 — Maracana pitch-edge rail (the handshake plate)
**Scenes:** S23 · **Era:** 1950 · **Light:** grey rain thinning to mist, wet highlights · **Sound:** rain dripping, distant echo, one tick far away

**PROMPT**
```
A low weathered timber and iron rail at the edge of a 1950 stadium pitch, wet with rain beads, the first row of plank benches behind it and the swamp of dark red-brown mud beyond, grey mist over the empty concrete tiers, puddles reflecting the sky, a single boot-print trail crossing the mud toward the rail, low frame at rail height, the rail in sharp foreground, the empty bowl soft behind, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Two friends, one rail between them: the quarrel and the reconciliation happen here.
**MUST-SEE OBJECT:** a single trail of boot-prints crossing the mud toward the rail
**AVOID (generic):** empty romantic mist

**BRIEF / USE:** WHO: Jaisal (below), Zidhan (above the rail) added in the character layer. WHERE: A3. HOW BIG: low two-shot over the rail, then the 360 orbit. FEELING: quiet admiration. USE FOR: 23-01 to 23-03.

**NOTE:** The same rail rhymes with C4 (the village gallery rail) so the 360 flip lands at the ground.


## B1 — The silent stadium (the 2026 ground, empty, amber)
**Scenes:** S7 · **Era:** 1950 mind-trip (colour, grade B&W) · **Light:** amber golden hour, low raking sun · **Sound:** one watch tick only

**PROMPT**
```
The same small village football ground in amber golden hour, completely empty, the plank-and-bamboo gallery seats all unoccupied, glossy red-brown mud with scattered footprints that glow in the raking light, one rubber sandal lying in the mud near the centre circle, the boundary rope sagging between posts, a hand-painted bedsheet banner on two bamboo poles with a round open-hand emblem, the wooden scoreboard reading 0-0, a portable speaker on a wooden stool silent, coconut palms in silhouette behind, long shadows, wide still frame, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Everything stops. Only a sandal and empty seats remain: someone has left something behind.
**MUST-SEE OBJECT:** one rubber sandal in the mud and an empty plank gallery
**AVOID (generic):** a crowd, any people

**BRIEF / USE:** WHO: Jaisal and Zidhan added later. FEELING: the world holds its breath. USE FOR: 7-01 to 7-07.

**NOTE:** DERIVE from C1 by image-to-image (same set, new light). The scoreboard reads **0-0**, not 3-1: the 3-1 appears only at the return (S23).


## B2 — Silent stadium, the sandal (insert)
**Scenes:** S7 · **Era:** same · **Light:** amber rim light · **Sound:** a single tick

**PROMPT**
```
Close detail of one worn rubber sandal lying in glossy red-brown mud with footprints leading away, golden rim light on the wet mud, a blur of empty plank gallery behind, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Someone ran out of the middle of a game; the sandal is the evidence.
**MUST-SEE OBJECT:** a single worn sandal with footprints leading away
**AVOID (generic):** a pair of shoes, any person

**BRIEF / USE:** INSERT for 7-01.


## B3 — Silent stadium, gallery steps
**Scenes:** S7 · **Era:** same · **Light:** amber, long shadows · **Sound:** hollow wooden knocks as steps are descended

**PROMPT**
```
The empty plank-and-bamboo gallery steps of a village football ground in amber light, worn wooden planks and bamboo rails, long shadows across the steps, the muddy pitch beyond, shot from the top of the steps looking down, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The long walk down from the observer's seat into the game he has been avoiding.
**MUST-SEE OBJECT:** steps leading down from the gallery to the mud
**AVOID (generic):** a bright cheerful stand

**BRIEF / USE:** WHO: Jaisal runs down these steps (character layer). USE FOR: 7-04.


## C1 — The village ground, 6 PM (wide from the gallery)
**Scenes:** S6, S23 · **Era:** 2026 colour · **Light:** low golden hour backlight, 6 PM · **Sound:** crowd murmur, a speaker, whistle

**PROMPT**
```
A small village five-a-side football ground in a harvested paddy field at 6 PM in low golden light, a short muddy pitch with a rope boundary on bamboo posts and two small goals made of painted timber, a plank-and-bamboo gallery on one side crowded with empty seats and a few abandoned plastic chairs, a hand-painted bedsheet banner on two bamboo poles reading THE FINAL 6 PM in rough block letters, a second bedsheet banner with a round open-hand emblem, an empty ticket-booth post made of bamboo and a plank, a portable speaker on a wooden stool at the far touchline, a hand-painted wooden scoreboard on a post with sliding numbers, glossy churned mud in the last light, wet green paddy fields and coconut palms behind the gallery, glowing humid dust in the air, wide frame from the gallery end, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** A final at 6 PM: this small ground carries everything these kids have.
**MUST-SEE OBJECT:** two hand-painted banners (THE FINAL 6 PM and the open-hand emblem) over a plank gallery
**AVOID (generic):** a professional stadium, flood-lit pitch

**BRIEF / USE:** WHO: Winning Eleven and Rockstar Boys added by the lineup composite. FEELING: this small ground is the whole world. USE FOR: 6-01 to 6-14, 23-04 to 23-06.

**NOTE:** 5-a-side confirmed by you (matches the script).


## C2 — The ground from the pitch (reverse)
**Scenes:** S6 · **Era:** 2026 colour · **Light:** low golden backlight · **Sound:** a speaker, crowd murmur

**PROMPT**
```
The same village ground seen from the centre of the muddy pitch looking back at the plank-and-bamboo gallery, long shadows stretching toward the lens, the rope boundary and bamboo posts in the foreground, the two hand-painted banners on poles behind the gallery, the wet green paddy and coconut palms glowing behind, golden dust in the air, low wide frame, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The kids' view: a crowd of villagers has come to watch them.
**MUST-SEE OBJECT:** the plank gallery filling toward the lens
**AVOID (generic):** an empty grey ground

**BRIEF / USE:** USE FOR: 6-03, 6-04.


## C3 — The scoreboard (insert)
**Scenes:** S6, S23 · **Era:** 2026 colour · **Light:** low golden light · **Sound:** none

**PROMPT**
```
A hand-painted wooden scoreboard on a bamboo post, sliding number plates in flaking white and red paint, a plank frame stained by rain, a coconut palm blurred behind, low golden light raking across the paint, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The score is the story: blank plates waiting to be set.
**MUST-SEE OBJECT:** sliding number plates in flaking paint
**AVOID (generic):** a digital scoreboard

**BRIEF / USE:** USE FOR: 23-06 (show 3 and 1 added in post) and a 0-0 version for S6.

**NOTE:** Generate with BLANK plates; set the numbers in post.


## C4 — The gallery and rail (close)
**Scenes:** S6, S23 · **Era:** 2026 colour · **Light:** low golden light · **Sound:** creak of planks

**PROMPT**
```
A close view of the plank-and-bamboo gallery of a village football ground, rough worn planks lashed to bamboo uprights with coir rope, a low bamboo rail at the front, a few red and white plastic chairs, mud on the lowest plank, golden light raking along the grain, the pitch soft behind, one empty plastic chair at the very front of the gallery, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The observer's seat, where Jaisal sits apart from the game.
**MUST-SEE OBJECT:** one empty plastic chair at the very front of the gallery
**AVOID (generic):** a packed crowd

**BRIEF / USE:** USE FOR: 6-05, 6-11, 23-04 (the mirrored handshake).

**NOTE:** RHYME with A3 (the Maracana rail).


## C5 — The sideline corner (bench, speaker, banner)
**Scenes:** S6 · **Era:** 2026 colour · **Light:** low golden light · **Sound:** speaker hum, banter

**PROMPT**
```
The sideline corner of a village football ground: a bedsheet banner with a round open-hand emblem on two bamboo poles, a plank bench with mismatched water bottles and a school bag, a portable speaker on a wooden stool a short distance away, muddy boot-marks everywhere, coconut palms and wet paddy behind, low golden light, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Poverty and pride: the bench, mismatched bottles, and the rock-band speaker across the way.
**MUST-SEE OBJECT:** mismatched water bottles on a plank bench
**AVOID (generic):** a team dugout with branded gear

**BRIEF / USE:** USE FOR: 6-02, 6-03, 20-04.


## D1 — The shore at dusk (MARJAN anchored near)
**Scenes:** S9, S11 · **Era:** 1950 · **Light:** late afternoon to dusk, amber · **Sound:** surf, gulls, wood and rope

**PROMPT**
```
A Kerala fishing shore at dusk in 1950, drying fishing nets strung on wooden poles like giant cobwebs, a long wooden gangplank laid from the sand toward the water, the huge three-deck Beypore-style wooden uru MARJAN anchored near with a dark timber hull, big painted eyes on the bow, a vast folded square sail, thick coir rigging, coconut palms at the far edge, the sun low and amber on the water, long shadows on the wet sand, upturned fishing boats, tidal pools, wide frame, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** A promise at sea: the ship waits for those who dare to board.
**MUST-SEE OBJECT:** a gangplank leading from the sand to the ship's dark hull and its painted eyes
**AVOID (generic):** a tourist harbour

**BRIEF / USE:** WHO: Sulaiman, Zidhan, the team added later. FEELING: the sea is long and the ship is a promise. USE FOR: 9-01, 9-02, 11-01 to 11-08.


## D1a — The shore, MARJAN far (Sulaiman alone)
**Scenes:** S9 · **Era:** 1950 · **Light:** late afternoon · **Sound:** surf, a single gull

**PROMPT**
```
The same Kerala fishing shore with the huge wooden uru MARJAN small and distant near the horizon line, nets on poles in the foreground, wet sand with a single trail of footprints leading down to the water, long amber shadows, wide still frame, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The dream is far; one man's footprints lead to it.
**MUST-SEE OBJECT:** a single trail of footprints leading down to the water
**AVOID (generic):** a crowded beach

**BRIEF / USE:** USE FOR: 9-01.


## D1b — The gangplank (close)
**Scenes:** S11 · **Era:** 1950 · **Light:** dusk · **Sound:** wood creak, surf

**PROMPT**
```
A long wooden gangplank worn smooth by feet and rope, laid from wet sand up to the dark timber hull of the wooden uru MARJAN, painted eyes on the bow above, coir ropes and wooden pegs, low dusk light on the planks, low frame looking up the gangplank at the deck, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Boarding is a decision: the gangplank is the threshold.
**MUST-SEE OBJECT:** a worn gangplank rising to the hull
**AVOID (generic):** a modern ramp

**BRIEF / USE:** USE FOR: 11-03, 11-08 (boarding).


## D2 — MARJAN deck at dawn
**Scenes:** S12, S14, S15 · **Era:** 1950 · **Light:** first gold light, cool blue shadows · **Sound:** wind in the canvas, rigging, wood creak

**PROMPT**
```
The deck of a large Beypore-style wooden uru ship at sea at dawn, a huge square sail half-set and glowing, big painted eyes on the bow, coils of coir rope on the planks wet with dew, mountains of coconuts in nets and baskets stacked against the mast and heaped at the stern, a low wooden cabin forward with a hand-painted route map on its wall and a swinging lantern, the endless dark-blue sea, first gold light on the water, wide frame from the stern looking forward, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** A village afloat: everything they own is coconuts and rope.
**MUST-SEE OBJECT:** mountains of coconuts against the mast
**AVOID (generic):** a clean yacht deck

**BRIEF / USE:** WHO: the team, Jaisal, Zidhan (character layer). FEELING: a village afloat. USE FOR: 12-01 to 12-06, 14-03, 15-02 to 15-06.

**NOTE:** COCONUT COUNT: mountains here; smaller in later shots (see 04).


## D2a — MARJAN deck at night (the quarrel)
**Scenes:** S20, S15 night · **Era:** 1950 · **Light:** one lantern, deep blue night · **Sound:** water on the hull, a far ship's horn

**PROMPT**
```
The same large wooden uru deck at night under one swinging lantern, a field of stars, the lights of a far city glittering low on the horizon, rope coils, the dark mast and furled sail, the planks glowing warm around the lantern and falling into blue shadow, the painted eyes at the bow barely visible, wide frame from the stern, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Night: the quarrel under the stars.
**MUST-SEE OBJECT:** one swinging lantern as the only light
**AVOID (generic):** moonlit romance

**BRIEF / USE:** USE FOR: 15-08 (Bose silhouette), 20-01 to 20-06.


## D2b — Open sea from above (the coconut pile, day 20)
**Scenes:** S15 · **Era:** 1950 · **Light:** midday glare · **Sound:** waves, wind

**PROMPT**
```
The deck of a wooden uru seen from above at midday on an endless open sea, the pile of coconuts now small and low against the mast, rope coils, the shadow of the sail across the planks, glare on the water, a long wake behind, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Time has passed: the coconuts are fewer, the sea is endless.
**MUST-SEE OBJECT:** a small low pile of coconuts
**AVOID (generic):** a luxury cruise

**BRIEF / USE:** USE FOR: 15-01, 15-07.

**NOTE:** COCONUT COUNT: a low pile (about 80).


## D2c — The cabin interior (route map)
**Scenes:** S14A · **Era:** 1950 · **Light:** a swinging kerosene lantern, warm · **Sound:** creak, lantern squeak, the sea

**PROMPT**
```
The interior of a small wooden ship's cabin at night, a hand-painted world map on the wall with a chalk route line from Madras to Rio, a low table, rolled charts, a swinging kerosene lantern throwing warm moving light, rough planks, brass fittings, a round porthole with black water beyond, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The way is drawn by hand: faith in a chalk line.
**MUST-SEE OBJECT:** a hand-painted route line from Madras to Rio
**AVOID (generic):** a digital map

**BRIEF / USE:** USE FOR: 14A (route scene).


## D2d — The mast looking up (the X on the mast)
**Scenes:** S15 · **Era:** 1950 · **Light:** dawn gold · **Sound:** wind, rope creak

**PROMPT**
```
The tall wooden mast of a large uru seen from the deck looking straight up, a huge square sail edged with gold dawn light, coir rigging crossing like a net against the sky, a gull far above, the planks wet with dew at the bottom of the frame, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Looking up: the X waits at the top of the mast.
**MUST-SEE OBJECT:** rigging crossing like an X above
**AVOID (generic):** a plain mast

**BRIEF / USE:** USE FOR: 15-03 (the two climbers cross in an X at the top).

**NOTE:** The X motif reappears here: build the climbers' shot on this plate.


## D3 — Pathemari at night
**Scenes:** S9 · **Era:** 1950 · **Light:** a single swinging lantern, stars · **Sound:** water, rope, wind in a loose sail

**PROMPT**
```
A slim lateen-sailed pathemari boat at night on dark water, a single swinging lantern at the stern casting a warm pool of light on bare planks, the lateen sail loose and still, stars reflected in the black water, soft phosphorescence at the bow, tight frame from water level, a folded blank form on the plank beside the lantern, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Zidhan alone with a message that must become true.
**MUST-SEE OBJECT:** a folded blank form on the plank beside the lantern
**AVOID (generic):** a pirate ship

**BRIEF / USE:** USE FOR: 9-07, 9-08.


## D4 — Rio quay at night
**Scenes:** S20 · **Era:** 1950 · **Light:** one lantern, city lights · **Sound:** water, a far horn

**PROMPT**
```
A 1950 Rio harbour quay at night, the MARJAN moored alongside with its painted bow eyes in the dark, the city lights and the hill silhouette above the clouds on the far shore, one lantern on the rail, black water reflecting the city lights in long streaks, wet stone, iron bollards and coiled rope, wide frame from the rail looking out, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Rio's lights, the far dream, indifferent to the quarrel on the deck.
**MUST-SEE OBJECT:** one lantern on the rail and the moored ship's painted eyes
**AVOID (generic):** a postcard skyline

**BRIEF / USE:** USE FOR: 20-01, 20-06.


## E1 — Coconut grove (10A: the coconut calculator)
**Scenes:** S10 · **Era:** 1950 · **Light:** gold, shafts of light · **Sound:** thuds of falling coconuts

**PROMPT**
```
A dense old coconut grove in golden afternoon light, leaning coconut palms with thick ringed trunks, one low branch with exactly twelve coconuts hanging from it, shafts of gold light cutting through the fronds, dust and pollen floating in the beams, coconut husks and dark earth on the ground, a stone at the grove edge, wide frame with the twelve-coconut branch dead centre, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Counting is a skill nobody paid for.
**MUST-SEE OBJECT:** exactly twelve coconuts on one low branch
**AVOID (generic):** a generic palm grove

**BRIEF / USE:** WHO: Jaisal + Gopalan (wire spectacles, counting). WHERE: E1. DOING: counting, one stone, seven thuds, the eighth falls on its own. HOW BIG: medium two-shot, close on the crossed-off list. FEELING: quiet certainty. USE FOR: 10-01 to 10-04.


## E2 — Sea shallows (10B: the wave-watcher)
**Scenes:** S10 · **Era:** 1950 · **Light:** hard glare · **Sound:** splashes, the hush of the wave

**PROMPT**
```
Waist-deep shallows over a sandy sea floor in hard midday glare, the water clear to the sand, a silver fish mid-arc above the surface, a long spear lying on the sand at the waterline, the horizon dead level, glare and small whitecaps, wide frame from the beach looking out, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Stillness is a skill: the sea can be read.
**MUST-SEE OBJECT:** a long spear lying on the sand at the waterline
**AVOID (generic):** a tropical beach resort

**BRIEF / USE:** WHO: Jaisal + Antappan (still as stone, waist-deep). DOING: spear skips, bare-hand catch, lets it go; Jaisal hurls a husk; he catches it without looking. HOW BIG: wide to close on the catch. FEELING: stillness. USE FOR: 10-05 to 10-07.


## E3 — Arecanut grove, THE X (10C: the wingers) SET-PIECE
**Scenes:** S10, S15, S17, S19, S22 · **Era:** 1950 · **Light:** golden hour backlight · **Sound:** the creak of bending trunks

**PROMPT**
```
Two tall, very thin arecanut palms side by side in a dry grove at golden hour, their trunks so flexible that they lean, bending toward each other and crossing in a perfect X at the top against a bright sky, shafts of gold light through the sparse leaves, the dry grove floor scattered with arecanut husks and fallen fronds, low sun raking across the trunks so the crossing point glows, medium-wide frame with the X dead centre, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Two paths cross and nobody collides: the film's central image.
**MUST-SEE OBJECT:** two thin palms crossing in a perfect X
**AVOID (generic):** two palms that merely lean

**BRIEF / USE:** WHO: Jaisal + Kuttappan + Karunan. DOING: they scale the palms, swing them toward each other, the trunks cross in an X, each lands on the other's tree, slide down, grin. HOW BIG: wide full-body to the crossing in medium. FEELING: the iconic image, clean and unhurried. USE FOR: 10-08.

**NOTE:** PICK THIS PLATE FIRST: every later X shot (mast, matches) rhymes to it.


## E4 — Coir beach (10D: the coir makers)
**Scenes:** S10 · **Era:** 1950 · **Light:** gold, low sun · **Sound:** thump, thump, thump (natural, no instrument)

**PROMPT**
```
A Kerala coir beach in gold light, long rows of wooden husk-pounding boards in a line, piles of coconut husks and loose golden fibre, half-pounded husks, the sand packed hard from years of pounding, a few coir ropes drying on poles, the sea at the far edge, low gold sun, wide frame along the rows, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Strength is work, done every day without applause.
**MUST-SEE OBJECT:** rows of wooden husk-pounding boards on hard-packed sand
**AVOID (generic):** a leisure beach

**BRIEF / USE:** WHO: Jaisal + Chandu + Velayudhan (two enormous men). DOING: rows pounding; 'Kick that husk': it sails over the palm tops; 'What's soft?'. HOW BIG: wide rows to medium on the kick. FEELING: comic power. USE FOR: 10-09, 10-10.


## E5 — Market alley (10E: the thief)
**Scenes:** S10 · **Era:** 1950 · **Light:** hard midday glare · **Sound:** shouts, a basket toppling, running feet

**PROMPT**
```
A narrow Kerala village market alley at midday, wooden market tables with baskets of silver mackerel and vegetables, a well at the corner, a tailor's stall with a treadle machine, cattle and carts at the far end, hawkers' stalls with cloth awnings, hard midday glare and short crisp shadows, the alley running straight to a vanishing point, wide frame down the alley, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Speed is survival: the thief runs because he has to.
**MUST-SEE OBJECT:** a basket of silver mackerel at the table's edge
**AVOID (generic):** a tidy tourist market

**BRIEF / USE:** WHO: Jaisal (2026 trainers, the one anachronism) + Raghavan + two constables + the fishwife. DOING: 'STOP! THIEF!'; he pivots, leaps a fish basket, slides under a table; Jaisal chases and knocks over the fishwife's basket, picks it up, keeps running; cornered: 'Are you police too?!'. HOW BIG: handheld wide chase to cornered medium two-shot. FEELING: the fastest shot of the set. USE FOR: 10-11 to 10-13.


## F1 — The house, exterior at dawn (the Azan)
**Scenes:** S1 · **Era:** 2026 colour · **Light:** blue-grey pre-dawn warming to pale gold · **Sound:** the Azan, a distant crow, a rooster

**PROMPT**
```
A modest Malabar family house at dawn, whitewashed walls streaked with green monsoon algae, a sloping Mangalore-tile roof with moss and a few cracked tiles, a small front veranda with a low parapet and two plain concrete pillars, a dark-brown wooden front door, barred windows with half-open wooden shutters, a plastic chair on the veranda, a concrete water tank on a pillar, an electric meter box on the wall, coconut palms and a mango tree beside the house, a damp dirt yard with puddles and red laterite earth, a rope clothesline, a distant mosque minaret in silhouette against a blue-grey sky with the first pale gold on the horizon, wide frame from the yard, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** A house of faith and silence at dawn: the first sound is the call to prayer.
**MUST-SEE OBJECT:** the distant minaret silhouette and the first pale gold
**AVOID (generic):** a suburban villa

**BRIEF / USE:** USE FOR: 1-01.


## F2 — Jaisal's bedroom
**Scenes:** S1, S1A · **Era:** 2026 colour · **Light:** cold blue pre-dawn through the window, warming to gold · **Sound:** the watch tick, the Azan, a ceiling fan off

**PROMPT**
```
A small bedroom in a Malabar house at dawn, limewashed pale green walls with damp patches near the ceiling, a red-oxide cement floor, a simple wooden cot with a thin striped mattress and a folded cotton sheet, a folded prayer mat at the end of the cot, a plastic chair holding folded clothes, a steel almirah in the corner, a wall clock stopped at the wrong time, a barred window with half-open wooden shutters letting in cold blue light, muddy football socks drying on the window bar, the dusty corner of an old football under the cot, no photographs or pictures on any wall, a switched-off ceiling fan, wide frame from the doorway, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** A man who stopped playing: the ball hidden, the socks still muddy.
**MUST-SEE OBJECT:** a football half-hidden under the cot
**AVOID (generic):** framed photographs, a messy teen room

**BRIEF / USE:** USE FOR: 1-02, 1-03, 1A-01.

**NOTE:** No framed photographs anywhere in the house.


## F3 — The kitchen
**Scenes:** S1 · **Era:** 2026 colour · **Light:** orange sunrise against cool blue shadows · **Sound:** a kettle hiss, steam

**PROMPT**
```
A small Kerala kitchen at dawn, a two-burner gas stove on a tiled counter, a dented steel kettle with steam rising, a steel rack of glasses and plates, a plastic bucket and a brass pot, a white single-door fridge with a few fresh mint stems standing in a glass, a window with an iron grille showing orange sunrise, a stone grinder in the corner, a hanging bundle of curry leaves, a wet floor, wide frame from the doorway, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** Care is the first act of the day: mint tea for Grandpa.
**MUST-SEE OBJECT:** fresh mint stems standing in a glass
**AVOID (generic):** a modern kitchen

**BRIEF / USE:** USE FOR: 1-04.


## F4 — Grandpa's room (day and night)
**Scenes:** S1, S4, S25 · **Era:** 2026 colour · **Light:** soft side light through the window; at night one yellow bulb · **Sound:** a slow fan, the watch tick

**PROMPT**
```
A plain room in a Malabar house with limewashed white walls, a wooden easy chair with long arms facing a barred window with white curtains stirring, a small wooden side table with a steel tumbler and a pair of spectacles, a ceiling fan turning slowly, a bed with a white sheet in the corner, a folded prayer mat on a shelf, a pair of leather sandals under the chair, dust floating in the window light, nothing on the walls, wide frame from the doorway, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** A man in stillness with a ticking watch: the heart of the film.
**MUST-SEE OBJECT:** an empty wooden easy chair facing the window and a steel tumbler
**AVOID (generic):** a hospital feel

**BRIEF / USE:** WHO: Grandpa (still), Jaisal. USE FOR: 1-05 to 1-07, 4-01, 4-09 to 4-11, 25-01 to 25-05.

**NOTE:** NIGHT VARIANT (S25): the same room with one yellow bulb, the fan spinning, a dark window, moths around the bulb.


## F5 — The backyard (parambu) and the grave pit
**Scenes:** S1-S2, S4 · **Era:** 2026 colour · **Light:** soft diffused morning light with shafts through palms · **Sound:** scraping shovel, dogs barking far away

**PROMPT**
```
A Kerala homestead backyard in morning mist, tall coconut palms with thick wet trunks, banana plants with torn leaves, wet red laterite earth, a half-dug pit with fresh red-brown soil heaped beside it, a shovel standing upright in the earth, a long shape under a torn sack beside the pit, a tin-roofed shed, a washbasin with a steel tap and a bucket against the back wall, a coir-rope clothesline, light mist between the trunks, wide frame from the back door, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** A man digging a grave for the past.
**MUST-SEE OBJECT:** a half-dug pit with fresh red soil
**AVOID (generic):** a tidy garden

**BRIEF / USE:** USE FOR: 1-08, 2-01, 4-02 to 4-07.


## F6 — The washbasin (insert)
**Scenes:** S4 · **Era:** 2026 colour · **Light:** morning · **Sound:** running water

**PROMPT**
```
A concrete washbasin with a steel tap against a limewashed back wall, brown muddy water swirling toward the drain, a bar of green soap, a towel on a nail, morning light, close frame, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** He washes off the mud, but not the past.
**MUST-SEE OBJECT:** brown water swirling toward the drain
**AVOID (generic):** clean clear water

**BRIEF / USE:** USE FOR: 4-08.


## F7 — The veranda (Zidhan at the window)
**Scenes:** S4 · **Era:** 2026 colour · **Light:** late morning · **Sound:** a rooster, a fan

**PROMPT**
```
The side of a modest Malabar house with a barred window and half-open wooden shutters at eye level, a view through the bars into a dim room with a chair facing the light, a coconut palm and a plastic chair beside the wall, dappled late-morning sun, wide frame from outside the window, empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour
```

**STORY JOB:** The watcher at the window sees the stillness.
**MUST-SEE OBJECT:** a barred window with a view of the chair
**AVOID (generic):** an open modern window

**BRIEF / USE:** USE FOR: 4-01.

