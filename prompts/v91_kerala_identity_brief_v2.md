# v91 Dataset — KERALA IDENTITY BRIEF v2 (corrected — for the rewriting model)

## WHY v1 CAME OUT BLONDE / EUROPEAN (root cause — read first)

The reference images are CORRECT (dark-skinned Indian men, black hair — verified). The failure came from THREE gaps:

1. **NO absolute identity words in the prompts.** v1's description was "Man, 26 years old, ... black hair ... skin EXACTLY the same as the reference image". That is a RELATIVE instruction — image models follow absolute words ("warm dark brown skin", "Kerala/South Indian") far better than relative ones ("same as reference"). With no absolute ethnicity/skin words, the model fell back to its own prior for "man, 26 years old" = a white European man. Black hair was stated, so hair stayed dark; skin and face-type drifted European.
2. **Weak identity anchor (workflow side — ALREADY FIXED).** The workflow's identity patch was at ref_boost 2.0 (the author's value, tuned for his blonde character whose prompts also said blonde). It is now raised to 4.0/1.0 (our proven strong-identity values), so the reference face+skin dominate. The prompts must ADD absolute identity words on top of that — both anchors together.
3. **European editorial framing.** v1 kept the author's Western scene/vibe set (luxury penthouse, cashmere sweater, antique bookstore, Rembrandt lighting, silk scarf) — even with a correct face, the WORLD reads European. The character's root is KERALA — scenes, clothing and mood must be rooted in South India.

## CHARACTER IDENTITY BLOCKS (put this at the START of EVERY line — verbatim, absolute words)

### Jaisal (char1 — PRIMARY)
```
Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural texture, medium wavy black hair falling to eyebrow length, slightly crooked naturally bent nose, dark brown almond eyes, thin lips, clean-shaven with faint stubble, lean slim build.
```

### Zidhan (char2)
```
Kerala (South Indian) man, about 26 years old, warm dark brown skin with natural texture, short neat black hair, full short dense black beard, dark brown eyes, lean slim build.
```

Rules:
- The identity block is the FIRST clause of every single line, before the scene. Never the relative "skin same as the reference".
- Hair must match the block EXACTLY (the face is locked by identity conditioning — describing hair consistently helps; contradicting it hurts).
- NEVER describe blonde/fair/white skin anywhere. If a line needs a skin word, use "warm dark brown skin" or "dark brown skin".

## CLOTHING (character canon)
- Jaisal: plain BLACK t-shirt is the base outfit. For scene lines, natural Indian casuals fit the root: open-collar white shirt, simple kurta, black t-shirt with jeans, rolled sleeves. No Western model-glamour clothing (no silk scarves, no cashmere, no jewelry stacks).
- Zidhan: plain WHITE t-shirt is the base outfit. Same natural casuals.

## SCENES — KERALA ROOT (this is the big change from v1)
Replace the author's European scene set with Kerala-rooted settings. Mix of three tiers:
- **Rural Kerala:** paddy fields, backwaters and houseboats, coconut groves, laterite stone paths, fishing boats on the lagoon, monsoon rain on a village street, temple-town courtyard, banana-leaf and clay-pot details, red laterite walls.
- **Urban Kerala:** Kochi old-city streets, Marine Drive promenade, monsoon over a city road, old veranda with brass and wood, filter-coffee moment, bus stand, rain-slicked market lane.
- **Domestic/natural:** home veranda in the rain, courtyard with a neem tree, morning light through a wooden window, rooftop in the monsoon, evening light on a backwater.

Lighting vocabulary: golden hour over water, soft monsoon overcast, rim light through rain, warm tungsten veranda light, dappled shade under coconut palms. Keep the photographic CRAFT from v1 (85mm f/1.8, shallow DOF, dutch angle, pov, creamy bokeh, high-detail skin texture with natural pores, film grain) — that part was good.

## FRAMING / MOOD (kill the "European male model" look)
- Grounded, natural, documentary/editorial South Indian look — NOT glossy Western male-model glamour. No "seductive look", no mirror-selfie vanity framing, no jewelry.
- Expressions: calm, thoughtful, faint smile, looking away at the water, working, waiting in rain — everyday real moments.
- If a v1 line's SHOT TYPE is worth keeping (profile, rear view, close-up beauty shot, dutch angle, pov), keep the shot type and re-root the scene/clothing/mood as above.

## LINE RULES (same as v1)
1. SAME line counts per list as the author's lists (20/20/25/25/25/20/25/7), same order, each line a complete standalone prompt.
2. EVERY line ends with: `ONLY ONE character, no other people, no duplicates.` (Krea2 duplication quirk — hard rule).
3. EVERY line includes the global suffix: `ignore original clothing completely, photorealistic, high-detail natural skin texture with pores, soft natural lighting, sharp focus,` (wired in the workflow too — keep both).
4. Write ALL 8 lists for Jaisal AND all 8 for Zidhan (16 blocks total), same labels as before (`LIST n — node <id> (Jaisal/Zidhan)`).
5. One prompt per line, no blank lines inside a block.

## OUTPUT FORMAT
16 fenced blocks, same order and labels as the v1 file. Paste-ready for the CR Prompt List nodes.
