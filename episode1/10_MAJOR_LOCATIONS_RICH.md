# 10 — MAJOR LOCATION RICH PROMPTS (world-building day, 2026-11-24)

**Author's 11-24 call:** the major factors are **the hopuse ⚠️ · the stadium · the 7s ground · the ship**,
plus the scenes where Jaisal searches for the players / does the recruitment.
This file = RICH prompts for each (review with Claude, refine, then we queue).

**Rig:** `krea2_t2i_env_cine.json` (2048×1152, dual-LoRA: cinematic + realism; famegrid zeroed) —
the env-batch rig (the one that made `ep1_env_00001..00008`).
**ERA rule:** 1950 locations generate IN COLOUR, graded B&W in post — never generate a black-and-white plate.
**ENV tail** (end of every env prompt):
`empty scene, no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`
**ENV negative** (already in the rig's negative node):
`people, humans, persons, faces, hands, crowds, players, text, watermark, logo, cartoon, 3d render, plastic smooth look, beauty retouching, brand logos, legible printed text`
**Prefixes:** `ep1_major_` (major plates) · `ep1_rec_` (recruitment env).

---

## DECISION POINTS (answer before we queue — 3 questions)

1. **The 7s ground:** L08 in `03_LOCATIONS.md` is currently a **5-a-side** ground. You said "the 7s ground" —
   does the village ground become **7-a-side**? If yes → L08 (2026), L10 (1950 silent) and the L26 rhyme
   all re-render with 7-a-side boundary (longer pitch, one extra pair of side posts).
2. **The hopuse:** this name is in NO project file (not the script, not the locations table, not the bible).
   Tell me in one line what it is → I draft its section next turn. Two candidate sketches are pre-drafted
   under **F** (harbour/quay vs coir hoober) in case one of them is it.
3. **The stadium rhyme:** the continuity rule (L08 = L10 = L26) says Maracanã must read as
   "the Kerala ground grown huge" — **same gallery proportions, same mud**. The rich prompt below keeps
   the gallery + mud + open-hand-ring banner motif so the rhyme survives at stadium scale. Confirmed?

---

## A. THE STADIUM — MARACANÃ (L26 · S17-19, 21-23) ⭐ the climax plate

**Era:** 1950 (colour → B&W grade) · **Light:** overcast day; the Uruguay match = hours of rain ·
**Camera:** wide → the mud close-up · **Sound (D041 — claps only, NO music):** the 190,000-voice roar,
clapping, the ball hitting a post, a ref's whistle, rain.

**Prompt (colour generation, grade B&W in post):**
`A vast 1950s South American concrete football stadium bowl under a heavy overcast sky, rain falling in
thin silver sheets, the pitch is dark glossy mud exactly like a Kerala paddy field with white lines
vanishing in the rain, a low timber-and-plank gallery ring around the bowl with simple bamboo-and-plank
seating sections echoing a small village ground grown huge, a hand-painted bedsheet banner on two poles
at one corner showing a round open-hand emblem, a single wooden scoreboard with sliding numbers,
tall steel floodlight frames with unlit bulbs at the corners, wet concrete steps in the stands,
puddles reflecting the grey sky, a boundary rope on one side where the concrete ends and the mud begins,
wide frame from the opposite gallery, empty scene, no people, no humans, no faces, no hands,
shot like a documentary still, natural textures with no smoothing, soft honest lighting,
shallow depth of field, subtle film grain, true-to-life colour`

**Variants (same set, re-render):**
- `V-A1 — rain hour (S21-22): the same bowl mid-storm, white sheets of rain, the mud pitch steaming in the cold, water running off the gallery in thin streams, one rubber sandal abandoned on the mud near the centre circle, wide frame, empty scene, ...tail`
- `V-A2 — tunnel (L25, S16-17): the long narrow concrete tunnel opening onto the pitch, wet brick, a single bare bulb, the overcast daylight spilling in like a doorway, low frame at ankle height, empty scene, ...tail`

**RHyme check (post-generation):** mud texture must match L08/L10 plates; gallery proportion = village ground; the open-hand-ring banner appears at every scale.

---

## B. THE SILENT STADIUM (L10 · S7, 7A) — the B&W twin of L08

**Era:** 1950 (colour → B&W) · **Light:** amber golden hour · **Sound:** a single watch tick.
**Must rhyme with L08 + L26** — same gallery proportions, same mud.

**Prompt (best: derive from the chosen L08 plate via identity/i2i — same set, different light + mood):**
`The same small village football ground in amber golden hour, completely EMPTY, the plank-and-bamboo
gallery seats all unoccupied, footprints glossy in the mud, ONE rubber sandal lying in the mud near the
centre circle, the boundary rope, the hand-painted bedsheet banner on two bamboo poles (round open-hand
emblem), the wooden scoreboard at 3-1, the portable speaker on its stool silent, low amber sun raking
across the mud and making every footprint glow, long shadows, wide still frame, empty scene, no people,
no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing,
soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

---

## C. THE 7s GROUND (L08 · S6, 23 — 6 PM, low golden light) — ⚠️ decision point 1

**If 7-a-side confirmed:** boundary rope stretched to 7-a-side length, one extra pair of side posts,
everything else unchanged. **This is the TEAM-SHOT backdrop** (lineup composite route) — the pick from
this batch becomes `input\env_L08_*.png`.

**Prompt (2026, colour, 6 PM):**
`A small village 7-a-side football ground at 6 PM in low golden light, a longer-than-usual muddy pitch
with a boundary rope around it and seven pairs of simple posts along the sides, plank-and-bamboo gallery
seating on one side, a hand-painted bedsheet banner on two bamboo poles reading THE FINAL 6 PM in rough
block letters, a second bedsheet banner with a round open-hand emblem, an empty ticket-booth post,
a portable speaker on a wooden stool, a wooden scoreboard with sliding numbers, wet green paddy fields
and coconut palms behind the gallery, the pitch mud glossy in the last light, wide frame, empty scene,
no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no
smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

**1950 twin = section B (L10).** After the pick: copy to `input\env_L08_*.png`.

---

## D. THE SHIP — MARJAN (Beypore-style wooden *uru*, painted bow eyes)

### D1. THE SHORE AT DUSK (L12 · S9, 11)
**Light:** late afternoon → dusk · **Sound:** surf, gulls, wood and rope.
`A Kerala fishing shore at dusk, drying fishing nets strung on wooden poles like cobwebs, a gangplank
laid from the sand to the water, the large Beypore-style wooden uru ship MARJAN anchored near, its hull
dark timber with painted eyes on the bow, a huge folded square sail, coconut palms at the far edge,
the sun low and amber on the water, long shadows on the wet sand, wide frame, empty scene, no people,
no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing,
soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`
**Variant:** `V-D1a — MARJAN anchored FAR (S9): the same shore, the ship small on the horizon line, nets in the foreground, dusk.`

### D2. DECK + CABIN AT SEA (L18 · S11, 12, 14, 14A, 15, 20) ⭐ the big one
**Light:** dawn / day / night variants · **Sound:** wind, rigging, wood creak.
`The deck of a large Beypore-style wooden uru ship at sea at dawn, a huge square sail half-set,
painted eyes on the bow, coils of rope on the deck, a pile of coconuts at the stern, a low wooden cabin
forward with a hand-painted route map on its wall and a swinging lantern, the endless dark-blue sea,
first gold light on the water, wide frame from the stern looking forward, empty scene, no people,
no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing,
soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`
**Variants:** `V-D2a — night (S20): the same deck at night under one lantern, star field, the Rio lights far on the horizon.` · `V-D2b — open sea (L22): the deck from above, the coconut pile smaller than before, endless water, midday glare.`

### D3. PATHEMARI AT NIGHT (L19 · S9)
`A slim lateen-sailed pathemari boat at night on dark water, a single swinging lantern at the stern
casting a warm pool of light, the lateen sail loose and still, stars reflected in the black water,
tight frame from the water level, empty scene, no people, no humans, no faces, no hands,
shot like a documentary still, natural textures with no smoothing, soft honest lighting,
shallow depth of field, subtle film grain, true-to-life colour`

### D4. RIO QUAY, NIGHT (L28 · S20 — the quarrel)
`A 1950s Rio harbour quay at night, the MARJAN moored alongside, its painted bow eyes in the dark,
the city lights and the hill silhouette above the clouds on the far shore, one lantern on the rail,
water reflecting the city lights in long streaks, wide frame from the rail looking out, empty scene,
no people, no humans, no faces, no hands, shot like a documentary still, natural textures with no
smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

---

## E. RECRUITMENT ENV — Scene 10 five-shot set (1950 · colour → B&W grade)

**Context (script S10 "The Life-IQ Selection", director note):** recruitment = five shots only —
midfielder (coconut counter), goalkeeper (wave-watcher), wingers (two arecanut climbers), defenders
(two coir makers), striker (the thief). Everyone else is revealed on the pitch through parallels.
Jaisal alone in the groves, a folded page with the position list, Zidhan's pen in his pocket.
**Env rule: plates are NO PEOPLE** — the character shots come from the blockout → H3 loop (D262)
using these plates as the environment refs.

### E1. L13 — COCONUT GROVE (10A · the coconut calculator) — gold, shafts of light
`A dense old coconut grove in golden afternoon light, leaning coconut palms with thick trunks,
one branch low with exactly twelve coconuts hanging from it, shafts of gold light cutting through
the fronds, dust and coconut husks on the dark earth, a stone at the grove edge, wide frame with the
twelve-coconut branch dead centre, warm gold light, empty scene, no people, no humans, no faces, no hands, shot like a
documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field,
subtle film grain, true-to-life colour`
**Sound:** thuds (the seven-then-eighth coconut). **Shot brief (character layer, for the blockout → H3
loop):** *who/what* Jaisal + Gopalan (wire spectacles, counting under a palm) · *where* L13 under the
twelve-coconut branch · *what are they doing* counting, throwing one stone, seven thuds, the eighth
falls on its own · *how big / from where* medium two-shot → close on the crossed-off list · *feeling*
quiet certainty.

### E2. L14 — SEA SHALLOWS (10B · the wave-watcher) — glare
`Waist-deep shallows over a sandy sea floor in hard glare, the water clear to the sand, a leaping fish
mid-arc above the surface, a long spear lying on the sand at the waterline, the horizon line dead level,
glare and whitecaps, wide frame from the beach looking out, empty scene, no people, no humans, no
faces, no hands, shot like a documentary still, natural textures with no smoothing, soft honest
lighting, shallow depth of field, subtle film grain, true-to-life colour`
**Sound:** splashes, the wave hush. **Shot brief:** *who/what* Jaisal + Antappan (fisherman, still as
stone, waist-deep) · *where* L14 · *doing* the spear skips, he catches the leaping fish bare-handed,
lets it go; Jaisal hurls a coconut husk at his face, he catches it without looking · *how big* wide →
close on the catch · *feeling* stillness.

### E3. L15 — ARECANUT GROVE — THE X SPOT (10C · the wingers) ⭐ set-piece
**THE X is reused in S17, S19, S22 and on the mast (S15) — this plate must be picked first; every later
X-shot rhymes to it.**
`Two tall, very thin arecanut palms side by side in a dry grove at golden hour, their trunks so
flexible they lean, bending and crossing in a perfect X shape at the top, shafts of gold light through
the sparse leaves, the dry grove floor with scattered arecanut husks, low sun raking across the trunks
making the crossing point glow, medium-wide frame with the X dead centre, empty scene, no people,
no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing,
soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`
**Sound:** the creak of bending trunks. **Shot brief:** *who/what* Jaisal + Kuttappan + Karunan
(two lean arecanut climbers) · *where* L15 · *doing* they scale the two palms, swing the trees toward
each other, the trunks cross in a perfect X mid-air, each lands on the other's tree, slide down, grin ·
*how big* wide full-body → the crossing moment medium · *feeling* the iconic one — clean, no hurry.

### E4. L16 — COIR BEACH (10D · the coir makers) — gold
`A Kerala coir beach in gold light, rows of men's workstations in a line — long wooden husk-pounding
boards, piles of coconut husks and loose fibre, the rhythmic work-stations empty, a few husks
half-pounded, the sand packed hard from years of pounding, the sea at the far edge, low gold sun,
wide frame along the rows, empty scene, no people, no humans, no faces, no hands, shot like a
documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of field,
subtle film grain, true-to-life colour`
**Sound (D041):** the foot-pounding as the beat — *thump, thump, thump* (natural, not an instrument).
**Shot brief:** *who/what* Jaisal + Chandu + Velayudhan (two enormous men) · *where* L16 · *doing*
rows pounding; Jaisal: "Kick that husk" — it sails over the palm tops and vanishes; "Can you kick it
softly?" — "What's soft?" · *how big* wide rows → medium on the kick · *feeling* comic power.

### E5. L17 — MARKET ALLEY (10E · the thief) — midday
`A narrow Kerala village market alley at midday, wooden market tables with fish baskets and mackerel,
a well at the corner, a tailor's stall, cattle and carts at the far end, hawkers' stalls with cloth
banners, hard midday glare and short shadows, the alley running straight to a vanishing point,
wide frame down the alley's length, empty scene, no people, no humans, no faces, no hands, shot
like a documentary still, natural textures with no smoothing, soft honest lighting, shallow depth of
field, subtle film grain, true-to-life colour`
**Sound:** shouts, the chase, a basket toppling. **Shot brief:** *who/what* Jaisal (2026 trainers —
the one anachronism) + Raghavan (lean, scar through the left brow) + two constables + the fishwife ·
*where* L17 · *doing* "STOP! THIEF!" — he pivots, leaps a fish basket, slides under a table, comes up
without breaking stride; Jaisal chases, knocks over the fishwife's basket, picks it up, keeps running
with the fish under his arm; cornered — "Are you police too?!" — "Nope. But you have the same feet
as a champion." · *how big* handheld wide chase → cornered medium two-shot · *feeling* the fastest
shot of the set.

**S10 opener (env already covered by E1):** Jaisal alone in the groves with the folded list —
*shot brief:* *who/what* Jaisal alone, folded page (GOALKEEPER / DEFENDERS / MIDFIELDER / WINGERS /
STRIKER), Zidhan's pen in pocket · *where* grove edge between L13 and L15 · *doing* muttering "Not the
strong. Not the fast. Patterns. Football is just life with a ball." · *how big* slow push-in to the
page · *feeling* the thesis of the scene.

---

## F. THE HOPUSE ⚠️ — NEEDS YOUR DEFINITION (not in any project file)

**One line from you = I finalise this section next turn.** Candidate sketches (delete the one that's
not it):

**F1 — if the hopuse = the harbour/quay itself (where MARJAN anchors, where the team boards in S11):**
`A small 1950s Kerala harbour at dusk, a low timber-and-coral-stone quay, the MARJAN at anchor with
its gangplank down to the wet sand, drying nets on poles like cobwebs along the quay wall, a small
wooden weighing-stone pit for fish, the sea long and open at the far end where the horizon is longest,
the last gold light on the water, wide frame from the quay's end looking out, empty scene, no people,
no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing,
soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`
**Note:** if this IS the hopuse, then D1 (the shore) merges into it — one location, two plates (dusk
anchor + the gangplank close).

**F2 — if the hopuse = the coir hoober (the great wooden coir-drawing frame hall):**
`The interior of a Kerala coir hoober hall in gold side-light, two enormous parallel wooden frames with
long rows of coir fibre being drawn and twisted, the timber posts worn smooth by years of rope,
bundles of golden coir stacked along the walls, shafts of dusty gold light through the open side,
the floor packed with fibre dust, wide frame down the length of the hall, empty scene, no people,
no humans, no faces, no hands, shot like a documentary still, natural textures with no smoothing,
soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

---

## QUEUE PLAN (after your Claude review)

1. You refine this file → tell me the 3 decision answers (7s? / hopuse = ? / rhyme OK?) + any prompt edits.
2. I build `utilities\ep1_major_prompts_paste.txt` (one prompt per line, in queue order) + update this
   file's numbering to the final queue order.
3. You queue from `krea2_t2i_env_cine.json` (fresh tab): **A, B, C, D1, D2, D3, D4, E1-E5, F** = ~14 plates.
4. Picks → `input\env_{L26,L10,L08,L12,L18,L19,L28,L13,L14,L15,L16,L17,HOPUSE}_*.png` → then the
   character layer (recruitment shots + the S11 shore line) goes through the blockout → H3 loop.
**No GPU work is queued by me (D192) — the rig is validated 0/0, fresh tab per run.**
