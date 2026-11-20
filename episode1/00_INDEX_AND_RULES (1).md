# EPISODE 1 BIBLE — 00 INDEX AND GLOBAL RULES

**Source of truth:** `episode1_full_script_FINAL_v4.md` (names updated, spray payoff removed, faces-echo removed).
**This bible supersedes:** the earlier Cast + Location Bible (2026-11-18) and `episode1_kids_prompts_and_gap_review.md` (old kid names).
**Reader:** a local LLM (Qwen via MCP) assembling prompts for ComfyUI (Krea2 / Qwen-Image / MiniMax H3). Every field is explicit. If a field says `[USER-SUPPLIED]`, do not invent it; wait for the asset.

## FILES
| File | Contents |
|---|---|
| `00_INDEX_AND_RULES.md` | this file: global rules, identity blocks, prompt templates, QA |
| `01_CAST_2026.md` | Jaisal, Zidhan, adults, extras, the 12 Winning Eleven kids, the Rockstar Boys |
| `02_CAST_1950.md` | the 11 India-team players, supporting cast, opposing players, extras |
| `03_LOCATIONS.md` | every location with time of day, light, set dressing, sound, colour state |
| `04_PROPS_COSTUMES.md` | props, kits, T-shirts, the watch, continuity counts |
| `05_SOUND_AND_DIALOGUE.md` | instrument-free sound rules, humming policy, English → Malayalam pipeline |
| `06_SCENE_CONTINUITY_MAP.md` | per scene: place, time, who, costume/mud/colour state, props, sound |

## DECISIONS LOCKED (do not reopen)
1. **Teams:** Zidhan's 2026 five-a-side team = **Winning Eleven**. Jaisal's 1950 team = **India** (the national team). Opponents 2026 = **Rockstar Boys**.
2. **Names:** every 2026 kid has a realistic Malabar name for a child born around 2014–2015. **No nicknames as names.** A 2026 kid keeps the **same religious identity** as his 1950 counterpart, with a different name. The first letter echoes the 1950 name where natural (exceptions: Pakru/Sinan, Chandu/Sreehari).
3. **Faces:** the 1950 men are **completely different people** from the 2026 kids. Echo lives only in the initials, the religious identity and the theme.
4. **Skin tones (Malabar diversity):** the 12 Winning Eleven kids are **6 fair, 4 wheatish/light brown, 2 tanned**. Never generate all kids dark. Fair means a warm wheat undertone, **not pale, not pink, not European.**
5. **T-shirts:** Jaisal = teal tee with a printed **hibiscus** (3D-graphic style; design `[USER-SUPPLIED]`). Zidhan = mustard tee with the Winning Eleven logo, an **open hand in a ring** (design `[USER-SUPPLIED]`). The same logo goes on the team's bedsheet banner.
6. **Spray:** no spray payoff scene. "SPRAY: 0" remains only as ground reality in Part 1.
7. **Vaidyar:** a **background physio**, never a coach and never a recruitment scene. Optional one shot: he is pulled from an ayurvedic shop.
8. **Sound:** no instruments, no score. Voices (Azan, sung anthem, humming) and natural sound only. See `05`.
9. **Language:** dialogue generated in **English** with MiniMax (one consistent voice per character). Malayalam via later dubbing with lip-sync correction.
10. **Hardware:** everything local (RTX 5090, 64 GB RAM).

## ERA RULES
| | **2026** | **1950** |
|---|---|---|
| Colour | full colour, wet green, red mud, harsh noon | **black & white** + golden-hour bloom + soft vignette, graded in post; character sheets stay in COLOUR |
| Look | modern t-shirts, rubber sandals, Activa | period 1950s Kerala: simple cotton shirts, mundus, 1950s hair, weathered |
| Team | 5-a-side | 11-a-side |
| Colour survivors in 1950 | | only **(a) Jaisal's and Zidhan's T-shirts** (drain a little each day of the voyage), **(b) fire** (gold), **(c) the watch** (faint gold glint). Done by selective colourize in post |

## IDENTITY BLOCKS (use ONE per character; never the old "warm dark brown" default for everyone)
**Constants (append to every block):** `dark brown eyes, thick black hair, ordinary village features, Malayali (Kerala, South Indian) face, no European features, no East-Asian features, no blond or brown hair`

| Tone key | Text |
|---|---|
| `FAIR` | fair skin with a warm wheat undertone, natural texture and tiny blemishes, not pale, not pink |
| `WHEATISH` | light-brown wheatish skin, natural texture and tiny blemishes |
| `TAN` | tanned medium-brown skin from outdoor play, natural texture and tiny blemishes |
| `DARK` | warm dark brown skin, natural texture, weathered where relevant |

**Kid block:** `A real {AGE}-year-old Malayali boy from Malabar, Kerala, {TONE TEXT}, a child's proportions, no adult face, {CONSTANTS}.`
**Adult block:** `A real {AGE}-year-old Malayali {man|woman} from Kerala, {TONE TEXT}, {CONSTANTS}.`
**1950 block:** `A real {AGE}-year-old Malayali man of the 1950s from Kerala, {TONE TEXT}, weathered by sun and work, 1950s haircut, period cotton clothing, {CONSTANTS}.`

## STYLE TAIL (end of every prompt)
`shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

## NEGATIVE (if the workflow accepts one)
`blonde, European features, pale skin, pink skin, plastic smooth skin, beauty retouching, glamour lighting, text, watermark, extra fingers, distorted hands, adult proportions on children, heavy makeup, cartoon, 3d render, brand logos, legible printed text`

## PROMPT TEMPLATES
**T1 FACE ANCHOR** (3:4): `{IDENTITY BLOCK} {FACE_DESC}. Portrait, head and shoulders, plain white round-neck T-shirt, {EXPRESSION}, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light, no hat, no props. {STYLE TAIL}`
**T2 FULL-BODY KIT SHEET** (2:3): `{IDENTITY BLOCK} {FACE_SHORT}. Full body, head to feet, front view, {POSE}, wearing {KIT}. Plain light-grey seamless backdrop, flat even soft light. {STYLE TAIL}`
**T3 THREE-QUARTER:** T1 + `, head turned three-quarters to the left, same lighting, same backdrop`
**T4 MUD STATE:** T2 + `, shins, knees, forearms and the front of the jersey splashed with wet red-brown paddy mud, mud in the hair at the temples, a smear on one cheek, slightly out of breath, kit soaked and clinging`
**T5 PERIOD (1950 sheets):** same as T1/T2 but swap the white tee for the `VILLAGE` costume and add a `KIT` sheet for Brazil scenes. Sheets stay colour.

**Worked example (RAYYAN, T1):**
`A real 11-year-old Malayali boy from Malabar, Kerala, light-brown wheatish skin, natural texture and tiny blemishes, a child's proportions, no adult face, dark brown eyes, thick black hair, ordinary village features, Malayali (Kerala, South Indian) face, no European features, no East-Asian features, no blond or brown hair. A tall, lean boy, taller than his age, long neck, sharp angular features, high cheekbones, narrow chin, thick straight eyebrows, wide shy eyes, short black hair cut unevenly at home with a small cowlick at the crown. Portrait, head and shoulders, plain white round-neck T-shirt, shy hopeful expression, looking straight at the camera, plain light-grey seamless backdrop, flat even soft light, no hat, no props. shot like a documentary still, natural skin texture with no smoothing, soft honest lighting, shallow depth of field, subtle film grain, true-to-life colour`

## PER-MODEL NOTES
- **Krea2 / Qwen-Image:** use the prompts as written; keep sentences, avoid keyword spam. If skin drifts, strengthen the TONE text and repeat "not pale, not pink".
- **MiniMax H3 (video):** I could not verify its limits. Test first: how many reference images, clip length, whether it holds identity. Feed each character: face anchor, 3/4, full-body clean, and mud-state if the scene needs it.
- **Identity-edit step:** Face Anchor → identity-edit lock → kit sheet. Do **Rayyan first**.

## GENERATION ORDER
1. Rayyan → Alan → Govind → Bilal → Rishi (starters). 2. Rockstar Hashim, Abhijith, Jerin. 3. Adults (Grandpa, Akhil, Father, Shafiq's wife). 4. 1950 players, Sulaiman, little Abu Bakar (from Grandpa's anchor). 5. Bench kids only when a shot needs them.

## QA CHECKLIST (run on every anchor)
- Skin tone matches the key for that character (not drifting dark or pale).
- Face reads Malayali, not European, not East-Asian.
- Child looks 11–12 (no adult jaw or stubble). Rayyan reads as tall but still a child.
- Kit matches the entry (colour, wear, props). No black on a Winning Eleven kid.
- No printed legible text or brand logos.
- Hands normal; no extra fingers.
- 1950 men look different from every 2026 kid.
- Family resemblance rule met (see `02`).

## SCRIPT RENAME MAP (already applied in v4)
Adam→**Rayyan** · Anto→**Alan** · Gopu→**Govind** · Babu→**Bilal** · Ragu→**Rishi** · Pachu→**Sinan** · Velu→**Vihaan** · Kutti→**Kailas** · Karu→**Kiran** · Chandru→**Sreehari** · Musthu→**Muhsin** · Tomy→**Tobin**.

## ADDED RULES (v2)
1. **MODESTY RULE (every woman, every era, every shot):** no hair is ever visible. **2026:** a modern hijab covering the head, ears, neck and chest, loose long-sleeved clothing; only the face and hands visible. **1950:** a head cloth (thattam) covering all hair, ears and neck, a long-sleeved blouse and a mundu to the ankles; only the face and the front of the hands visible. Add to the negative prompt: `visible hair on women, bare arms on women, low neckline on women`.
2. **FACES:** `08_FACE_FEATURE_MATRIX.md` is the source of truth for faces. Every character has 8 features (head shape, hairline/hair, eyebrows, eyes, nose, lips, jaw/chin, ears). No two characters in a group share more than 2 of the 8, and never the same nose + jaw + ears. The FACE_DESC lines in `01` and `02` are superseded.
3. **ADULT SKIN:** adults get a visible-skin sentence (pores, fine lines, sun marks, wrinkles by age). Kids keep clean child skin.
4. **Optional men's toggle:** bare-chested village costumes (Chandu, Velayudhan, Kuttappan, Karunan) can take `a plain cotton vest`.
5. **Prompts:** `07_ASSEMBLED_PROMPTS_ALL_CHARACTERS.md` is regenerated from the matrix; use it, not any earlier prompt file.
