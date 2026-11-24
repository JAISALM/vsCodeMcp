# 09 — CINEMATIC STYLE AND LOCATION PLATES

*This is the cinematic layer. The earlier character prompts are identity sheets on a grey backdrop (for faces only). This file and `10_SHOT_LIST_AND_VIDEO_PROMPTS.md` are what make it look like a film.*

## 1. DELIVERY
- **Aspect:** generate everything at **16:9** (your rig makes 2048x1152). **Frame everything inside a central safe frame (the middle 80% of the height) so you can decide the final crop in the edit.** Options, all possible from the same footage: **16:9 as shot** (maximum resolution, best for phones and YouTube), **2.0:1** (a mild cinema look, loses about 11% of the height), or **2.39:1** (the wide cinema look, loses about 25% of the height). Decide once and keep the same crop for both eras. See the explanation in the chat reply (and below) before choosing.
- **Frame rate:** 24 fps. **Clips:** 4 to 10 seconds per generation; the shot list is built to that length.
- **Text in shots (banners, forms, scoreboard, notebook, WhatsApp, newspaper):** generate the object **blank** and add the text in post. Image and video models garble lettering.
- **No music, no on-screen text from the model.** Every video prompt says so.
- **Colour grade:** 2026 stays in colour. 1950 is graded to black-and-white in post. Only the two T-shirts, fire and the watch keep colour (selective colourize).

## 2. THE TWO LOOKS
| | **2026 (Kerala)** | **1950 (the mind-trip)** |
|---|---|---|
| Camera | **handheld, slightly nervous**, close and sweaty; whip pans on action; nothing perfectly still | **locked-off or slow gliding**, dolly and crane, composed like paintings; the world feels remembered |
| Lens | 24, 28, 35 mm for action; 85 mm for faces | 24 and 35 mm for space; 50 and 85 mm for portraits; 100 mm macro for objects |
| Light | harsh noon white, wet green, red mud, hazy golden hour at 6 PM | golden-hour **bloom**, backlight, long shadows, soft vignette that dissolves the edges |
| Colour | saturated humid greens, red laterite, white sky, teal and mustard tees | graded to black and white; **gold only on fire, the watch, and the two tees** |
| Air | humid haze, heat shimmer, steam from mud, dust | woodsmoke, salt mist, dust shafts, pollen, rain |
| Motion language | chaos, noise, crowd, fast cuts | silence, long takes, slow push-ins, match cuts |
| Sound | handheld ambience: crowd, whistles, engines, birds | wind, surf, rigging, oars; the watch tick; **silence is the loudest sound** |

## 3. WHAT MAKES A SHOT CINEMATIC (the checklist)
1. **Foreground, midground and background** in every wide shot (a palm trunk, a rope, a basket).
2. **A light source you can point to** (window, sun, lantern, lamp).
3. **Atmosphere in the air** (dust, steam, mist, pollen, rain).
4. **One strong shape** (the X of the palms, the hands over the rail, the mountain of coconuts).
5. **Depth of field decisions:** shallow on faces and objects, deep on landscapes.
6. **Motion with a reason:** push-in for realisation, pull-back for loss, orbit only for the return.
7. **Repeated visual rhymes:** the paddy and the Maracana mud; the X of the palms and the X of the wingers; the watch tick as the film's heartbeat.

## 4. VIDEO PROMPT TEMPLATE (what the shot list assembles)
`{shot size}, {lens}, {camera movement}. {what happens}. Setting: {location}. Lighting: {light and atmosphere}. {era style}. Natural ambient sound only, no music, no on-screen text. Length: {n} seconds.`
Attach the **character sheets** named in `REFS` and the **location plate** from this file as references.

## 5. HARD SHOTS (plan these separately)
| Shot | Problem | Suggested solution |
|---|---|---|
| 6-14, 7-01 colour drain | animated grade | generate in colour, animate the saturation in post, radial from the watch |
| 13-08 fire | models vary | generate the fire as its own gold plate and composite |
| 17-05 pitch to chalkboard | morph | build as two plates and a dissolve in post |
| 23-03 the 360 orbit | models struggle with full rotation | generate 3 partial orbits (120 degrees each) and stitch with whip blurs; or a fast rotation with the rain streaks hiding the join |
| 19-01, 22-01 stadium crowds | thousands of faces | generate the empty bowl and add a crowd layer; keep faces tiny |
| 23-05 watch in the fist | tiny object | generate as an extreme close-up insert with the tick sound |
| 10-08 the X | must read clearly | generate on its own with a locked camera, then reuse the idea in the match shots |
| Any dialogue shot | mouth visible for dubbing | medium close-up, still camera, 20 to 30 percent extra length |

## 6. LOCATION PLATES (no foreground people; background figures only where described)
Each location has a **WIDE PLATE** and a **DETAIL INSERT**. Generate the plate first; use it as the scene reference for every shot in that location.

### L01 Jaisal's bedroom  (scenes 1, 1A)
**WIDE PLATE (16:9)**
```
A small Malabar bedroom at dawn: whitewashed walls with peeling lime, a red-oxide cement floor, a simple wooden cot with a thin mattress, a plastic chair, a barred window with wooden shutters half open, a stopped wall clock, muddy football socks drying on the window bar, the corner of an old football showing under the cot, no photographs on the walls. cold blue pre-dawn light through the window, slowly warming to pale gold, soft long shadows, a single beam on the floor. still air, a little floating dust. Shot on 35mm lens, eye level, slightly low. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of an old dusty football half-hidden under a wooden cot, a name in faded marker on the leather, dust motes drifting in a thin raking beam of window light. cold blue pre-dawn light through the window, slowly warming to pale gold, soft long shadows, a single beam on the floor. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L02 Kitchen  (scenes 1)
**WIDE PLATE (16:9)**
```
A small Kerala kitchen at dawn: a steel kettle on a two-burner gas stove, tiled counter, a shelf of steel glasses and plates, an old fridge, a barred window with a pale orange sunrise, steam rising. warm orange dawn from the window against cool blue room shadows. steam and a faint kitchen haze. Shot on 40mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of hands plucking fresh green mint leaves from a fridge shelf and dropping them into a steel glass of steaming water, steam curling in window light, shallow depth. warm orange dawn from the window against cool blue room shadows. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L03 Grandpa's room  (scenes 1, 4, 25)
**WIDE PLATE (16:9)**
```
A plain room with whitewashed walls, a wooden chair facing a window, a small wooden table with a steel tumbler, a ceiling fan turning slowly, a folded prayer mat on a shelf, nothing on the walls. soft side light from the window, dust drifting in the beam, deep gentle shadows. still, hushed, a slow fan. Shot on 50mm lens, locked-off, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Extreme close-up of a vintage gold-toned wristwatch with a cream dial on a frail, age-spotted wrist resting on a table, the second hand ticking, shallow depth of field. soft side light from the window, dust drifting in the beam, deep gentle shadows. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L04 Backyard (parambu)  (scenes 1-2, 4)
**WIDE PLATE (16:9)**
```
A Kerala homestead backyard (parambu) in the morning: tall coconut palms, wet red laterite earth, banana plants, a half-dug pit with fresh piles of red earth, a shovel standing in the soil, a tin-roofed shed, a washbasin against the back wall, morning mist between the trunks. soft diffused morning light with shafts through the palms, wet highlights on leaves. light ground mist, damp. Shot on 28mm lens, low angle. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a muddy shovel blade biting into wet red earth, soil falling, shallow depth with a palm trunk blurred behind. soft diffused morning light with shafts through the palms, wet highlights on leaves. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L05 Paddy training ground  (scenes 2, 2A, 3)
**WIDE PLATE (16:9)**
```
A harvested paddy field turned football ground in Kerala: churned red-brown mud with standing puddles, stubble at the edges, coconut palms on the horizon, six stones set out as markers, a muddy centre circle with a small dark shape lying in it that everyone avoids, farmers in palm-leaf hats at the far edge, hot humid late morning. hard late-morning sun, high contrast, steam rising from wet earth. hazy humid air, heat shimmer. Shot on 24mm lens, low and wide. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a football resting in a muddy puddle, mud splashed over the panels, a small dead bandicoot out of focus beside it. hard late-morning sun, high contrast, steam rising from wet earth. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L06 Field edge / road  (scenes 3)
**WIDE PLATE (16:9)**
```
A narrow red laterite road at the edge of a paddy field: a dented white Ambassador car with its back door open, a wedding outfit on a hanger in the rear window, coconut palms, dust. harsh near-noon sun, dust glowing. dusty, hot. Shot on 35mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a man's wristwatch and a sweating forearm as he checks the time, shallow focus. harsh near-noon sun, dust glowing. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L07 Shafiq's house  (scenes 5, 5A)
**WIDE PLATE (16:9)**
```
A modest Malabar house: a sloping Mangalore-tile roof, a small veranda with a grille, a clothesline of washed clothes, a dirt pathway to a green wooden gate, a coconut palm beside the gate, warm afternoon light. warm low-angle afternoon light, long soft shadows. dry dusty air, crows calling. Shot on 35mm lens, low angle. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Low close-up of a brown coconut rolling and wobbling along a dirt path toward the lens, soft focus house behind. warm low-angle afternoon light, long soft shadows. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L08 The match ground (5-a-side)  (scenes 6, 23)
**WIDE PLATE (16:9)**
```
A Kerala five-a-side match ground in a harvested paddy field at 6 PM: a plank-and-bamboo gallery crowded with villagers, a rope boundary, a hand-painted bedsheet banner on two bamboo poles (a round open-hand emblem, no legible text), a speaker on a stool, a hand-painted wooden scoreboard on a post, a churned muddy pitch, coconut palms in silhouette. low golden-hour backlight, long shadows, glowing dust and humidity in the air. golden haze. Shot on 28mm lens, slightly low. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a hand-painted wooden scoreboard with sliding number plates, flaking paint, in low golden light. low golden-hour backlight, long shadows, glowing dust and humidity in the air. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L10 Silent stadium (B&W)  (scenes 7, 7A)
**WIDE PLATE (16:9)**
```
The same paddy match ground completely empty at amber golden hour: the plank gallery empty, glossy black mud with scattered footprints, a single rubber sandal lying in the mud, the banner hanging still, long shadows, a glowing soft vignette dissolving the frame edges. amber golden-hour glow with a bloom and soft vignette. absolute stillness, a faint shimmer. Shot on 32mm lens, low, locked-off. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of one rubber sandal lying in glossy mud, footprints leading away, golden rim light. amber golden-hour glow with a bloom and soft vignette. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L11 Village road and fork  (scenes 8)
**WIDE PLATE (16:9)**
```
A 1950 Malabar village road at golden hour: red laterite road, a tin-roofed tea shop, a well, a tailor at a treadle sewing machine under a veranda, fence posts, a bullock cart, coconut palms, cooking-fire smoke, no modern objects, a fork where one road leads to the groves and the other to the sea. low golden light with bloom, backlit dust and smoke. woodsmoke haze. Shot on 35mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a tailor's hands working a treadle sewing machine, thread, a half-sewn shirt, warm light. low golden light with bloom, backlit dust and smoke. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L12 Shore  (scenes 9, 11)
**WIDE PLATE (16:9)**
```
A 1950 Malabar shore at late afternoon: pale sand, fishing boats pulled up, nets drying on poles like giant cobwebs, a huge three-deck wooden uru named MARJAN anchored offshore with painted eyes on its bow, surf, a long gangplank on the sand, long shadows. low sun, long shadows, glowing sea haze, rim light on the sails. salt haze, spray. Shot on 35mm lens, wide, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of the weathered painted eyes on the bow of a huge wooden ship, sea spray on the planks. low sun, long shadows, glowing sea haze, rim light on the sails. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L13 Coconut grove  (scenes 10A)
**WIDE PLATE (16:9)**
```
A coconut grove in shafts of golden light: leaning palms, fronds slicing the sun into bars, one branch heavy with twelve coconuts, dust and pollen floating in the beams. dramatic god-rays through fronds, high contrast. floating pollen and dust. Shot on 24mm lens, low angle. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a stone leaving a hand and seven coconuts falling through a shaft of light, tight and dynamic. dramatic god-rays through fronds, high contrast. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L14 Sea shallows  (scenes 10B)
**WIDE PLATE (16:9)**
```
Calm waist-deep shallows at midday glare: a fisherman standing perfectly still in the water with a short spear, silver fish glints below the surface, expanding ripples. bright specular glare, the sea a sheet of silver. still, tiny ripples. Shot on 85mm lens, water-level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Extreme close-up of a bare hand catching a leaping silver fish in mid-air, water droplets frozen. bright specular glare, the sea a sheet of silver. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L15 Arecanut grove (the X)  (scenes 10C)
**WIDE PLATE (16:9)**
```
Two very tall, impossibly thin arecanut palms side by side in a green grove, their tops bending toward each other and crossing in a clear X against a bright sky, golden light through the leaves. golden-hour backlight through the leaves, green glow. fresh, slight sway of the trunks. Shot on 24mm lens, low angle looking up. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of two climbers' bare feet and rope loops gripping a swaying trunk as they swing across. golden-hour backlight through the leaves, green glow. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L16 Coir beach  (scenes 10D)
**WIDE PLATE (16:9)**
```
A sandy beach with heaps of coconut husks and coir fibre, rows of men pounding husks with wooden mallets and bare feet, brown dust and fibres in the air. golden backlight, dust glowing. fibre and dust haze. Shot on 35mm lens, low. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of bare feet slamming a husk into the sand, fibres bursting upward in golden backlight. golden backlight, dust glowing. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L17 Market alley  (scenes 10E)
**WIDE PLATE (16:9)**
```
A crowded 1950 market alley at midday: baskets of fish and vegetables on wooden tables, cloth awnings, hawkers, a stray goat, cattle, hanging scales, cobblestones. hard midday sun cut by awnings into stripes. busy, dusty, fish-market haze. Shot on 28mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a basket of silver mackerel scattering across wet cobbles. hard midday sun cut by awnings into stripes. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L18 MARJAN deck and cabin  (scenes 11, 12, 14, 14A, 15, 20)
**WIDE PLATE (16:9)**
```
The deck of a huge 1950 wooden uru at dawn: a massive square sail, rope coils, mountains of coconuts in nets stacked against the mast, planks wet with dew, the painted eyes at the bow, a cabin door beside a hand-painted world map. soft pre-dawn light, cool blue to gold, sail glowing. sea mist, damp wood. Shot on 28mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a hand drawing a chalk pitch on wet deck planks, brown rubber seeds laid out as markers. soft pre-dawn light, cool blue to gold, sail glowing. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L19 Pathemari at night  (scenes 9)
**WIDE PLATE (16:9)**
```
A slim lateen-sailed wooden boat at night on a black sea, a single swinging lantern, a sky full of stars, glowing phosphorescence at the bow. single warm lantern against deep blue night, stars. cool night air, sea spray. Shot on 35mm lens, low. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a hand writing in block capitals on a page by swinging lantern light. single warm lantern against deep blue night, stars. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L20 Madras post office  (scenes 13)
**WIDE PLATE (16:9)**
```
A tall red-brick Madras post office interior at dawn: arched windows with dusty shafts of light, brass counters, rubber stamps, ceiling fans turning slowly, a queue of people, a telegraph key and strip machine, a high shelf with a small shrine, a garland and a brass oil lamp burning. warm dawn shafts through arched windows, the lamp flame the warmest point. dust in the light shafts, a stuffy heat. Shot on 35mm lens, eye level then tilting up. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up in slow motion of a brass oil lamp tipping, oil arcing out in a thin ribbon, the flame trailing. warm dawn shafts through arched windows, the lamp flame the warmest point. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L21 Madras bazaar and harbour  (scenes 14)
**WIDE PLATE (16:9)**
```
A busy Madras bazaar in the morning: stalls of shiny brown rubber seeds in heaps, stacks of paper, a barrow of striped woollen socks, crowds in white dhotis, black umbrellas, a harbour with masts and a huge wooden ship beyond. bright warm morning sun, bustling colour. busy dust, steam from tea stalls. Shot on 35mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a hand holding a palmful of glossy brown rubber seeds. bright warm morning sun, bustling colour. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L22 Open sea  (scenes 15)
**WIDE PLATE (16:9)**
```
An endless open sea under a vast sky, a lone huge wooden ship small in the frame, long swells, the deck piled with coconuts, golden dawn light. huge soft sky, a golden horizon line, deep blue water. salt mist, big swell. Shot on 24mm lens, wide, low over the water. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a single coconut floating away in the foaming wake, shrinking into the swell. huge soft sky, a golden horizon line, deep blue water. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L23 Rio harbour  (scenes 16)
**WIDE PLATE (16:9)**
```
Rio de Janeiro harbour at misty dawn in 1950: Sugarloaf mountain rising from the mist, the white Christ statue above low cloud, iron liners and steamers at anchor, a small wooden uru gliding among them like a ghost, gulls. cool pearly dawn, soft mist, a gleam on the water. heavy sea mist. Shot on 35mm lens, wide, slightly low. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a thick ship's rope on an iron quay bollard with mist behind. cool pearly dawn, soft mist, a gleam on the water. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L24 FIFA office  (scenes 16)
**WIDE PLATE (16:9)**
```
A cavernous 1950 stadium office: a long polished table with thirteen small national flags on stands, heavy glass ashtrays, a wire tray, tall windows with venetian blinds throwing stripes of light, cigarette haze. stripes of window light through blinds, warm dust and smoke. cigarette haze. Shot on 40mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a wire tray holding a single slip of paper beside a small flag. stripes of window light through blinds, warm dust and smoke. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L25 Stadium tunnel and pitch  (scenes 16, 17)
**WIDE PLATE (16:9)**
```
The mouth of a 1950 stadium tunnel opening onto an overcast pitch, a uniformed ceremonial party standing silent, a pole with a flag snapping in the wind, thirty thousand spectators in hats beyond. flat overcast light, bright opening at the tunnel mouth. wind, a hush. Shot on 28mm lens, low from inside the tunnel. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a flag snapping on its pole against a grey sky. flat overcast light, bright opening at the tunnel mouth. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L26 Maracana  (scenes 17-19, 21-23)
**WIDE PLATE (16:9)**
```
The Maracana in 1950: a vast concrete bowl of rising rings packed with a sea of hats and paper flags, a rail below the first row, a wide pitch (for the Uruguay match: hours of rain have turned it into a swamp of brown mud, the white lines vanishing, grey sky, rain streaks). day light for the group games; heavy overcast with rain for Uruguay, wet highlights. rain, mist, roar. Shot on 24mm lens, wide, low at pitch level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of boots and bare feet churning brown mud and rainwater on a swamped pitch, splashes in slow motion. day light for the group games; heavy overcast with rain for Uruguay, wet highlights. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L27 Dressing room  (scenes 18)
**WIDE PLATE (16:9)**
```
A bare 1950 stadium dressing room: wooden benches, coat hooks, a single hanging bulb, a bucket and a cloth, bruised bare shoulders in the half light. one overhead bulb, deep shadows, warm tungsten. quiet, a little steam. Shot on 35mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of a bruised ribcage on bare skin lit by a single bulb. one overhead bulb, deep shadows, warm tungsten. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```

### L28 Rio quay and night deck  (scenes 20)
**WIDE PLATE (16:9)**
```
The night deck of the moored wooden uru on the Rio quay: a single lantern, a rail, rope, Rio's lights across black water, a distant ship's horn. a single warm lantern against deep blue night, lights glittering on the water. cool night air, quiet water. Shot on 35mm lens, eye level. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
**DETAIL INSERT (16:9)**
```
Close-up of two men's hands on a ship's rail beside the lantern, one tightening his grip. a single warm lantern against deep blue night, lights glittering on the water. cinematic still, shot on 35mm film, natural light, subtle film grain, rich true-to-life colour, no close-up people, no text
```
