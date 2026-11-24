# EPISODE 1 — QWEN CORE BIBLE (single file)

**You are the production assistant for Episode 1.** This file is the single source of truth. It contains 11 sections in this order: 00 rules, 12 story layer, 06 continuity map, 01 cast 2026, 02 cast 1950, 08 face matrix, 03 locations, 04 props and costumes, 05 sound and dialogue, 09 cinematic style, 11 location plates.

**HOW TO USE IT**
- Everything is keyed by ID: kids K01-K12 and Rockstar R01-R03; adults A01-A04, X01-X02; 1950 team P01-P11; supporting S01-S13; locations L01-L28; plates A0-F7; shots like 6-07 (shots are in a separate file when loaded).
- **Faces come from section 08. Costumes and kits from 01 and 02. Light, lens and sound from 09 and 11. Story meaning from 12. Continuity from 06.** Never invent features.
- **Hard rules (repeated at the end):** no music or instruments of any kind; every woman fully covered with no hair visible; every character's face must be distinct; 1950 images are generated in colour and graded B&W in post; leave [USER-SUPPLIED] fields blank; do not show legible text in generated images (text is added in post).
- When asked to assemble a prompt: take the template from section 00, the identity block by tone, the face from 08, and the kit from 01/02.

---


<!-- ===== FILE: 00_INDEX_AND_RULES.md ===== -->

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

## ADDED FILES (v3)
- `07_ASSEMBLED_PROMPTS_ALL_CHARACTERS.md` — character identity prompts (faces, kits).
- `08_FACE_FEATURE_MATRIX.md` — source of truth for faces.
- `09_CINEMATIC_STYLE_AND_LOCATIONS.md` — the two looks, the cinematic checklist, hard shots, and a wide plate plus a detail insert for every location.
- `10_SHOT_LIST_AND_VIDEO_PROMPTS.md` — 193 key shots in script order with lens, movement, length, references and a ready MiniMax video prompt; plus a coverage plan.
- `11_MAJOR_LOCATION_PLATES_RICH.md` — 34 story-driven plates (prompt, story job, must-see object, what to avoid); paste file `ep1_major_prompts_paste.txt`.
- `12_STORY_LAYER_AND_REFERENCES.md` — what the film says, motif meanings, the film in 12 frames, and reference slots R1 to R8 for *Sudani from Nigeria*.


<!-- ===== FILE: 12_STORY_LAYER_AND_REFERENCES.md ===== -->

# 12 — STORY LAYER FOR THE IMAGES + REFERENCE SLOTS

**Rule for every image in this film:** it must tell the story, not decorate it. Before generating or accepting any plate or shot, ask the **three-question test**:
1. **What does this image say?** (one sentence; each plate in `11` has a STORY JOB)
2. **What object proves it?** (one MUST-SEE object; if it is missing, the image is generic)
3. **Where are we in the arc?** (who is missing, what is at stake, what has just changed)
If an image fails any of the three, regenerate it or cut it.

## 1. WHAT THE FILM SAYS (my reading of your script; edit freely)
- **You cannot wait for the system to change. You adapt and build with what you have.** (the empty spray, the mud, the no-VAR ground)
- **Basics first, tactics on top.** Strength, grit and fundamentals carry a small game; skill and tactics win it. Neither alone is enough.
- **Do not bury the past badly.** The grave, the football under the cot, the semi-final: what you bury, you eventually dig up.
- **The people before us are still with us.** Grandpa, Sulaiman, the boy with the watch: memory is the real time machine.
- **Unseen work counts.** "A goal saved. Nobody counts that." The coir makers, the fisherman, the counter of coconuts.

## 2. MOTIFS AND WHAT THEY MEAN (keep them consistent in every image)
| Motif | Means | Where it appears |
|---|---|---|
| **The mud** | the ground truth; the same struggle at every scale | the paddy, the village ground, the Maracana (A0), the handshake (A3) |
| **The X** | two paths crossing without collision: unity, adaptation, the iconic image | arecanut palms (E3), the mast (D2d), the wingers in the matches |
| **The watch and its tick** | remembrance, not time travel; the film's heartbeat | F4, B1, D1, the fist at the return |
| **The open-hand banner** | the team's hope and unity at any size | C1, C5, B1, A0, A1 |
| **The empty centre circle (the dead rat)** | the truth everyone avoids | the training ground |
| **The sandal** | someone left in the middle of the game | B1, B2, C4's empty chair |
| **The grave and the pit** | burying the past | F5, F6 |
| **Coconuts** | home, food, football, and what is lost along the way | E1, D2, D2b, the voyage |
| **The ship's painted eyes** | the ship is watching; fate | D1, D1b, D4 |
| **The lantern** | the one warm light in the dark | D2a, D3, D4 |
| **Silence** | the loudest sound | S7, S16, S22 |

## 3. THE FILM IN 12 FRAMES (if only these twelve images survived, the story still reads)
| # | Frame | What it says | Plate |
|---|---|---|---|
| 1 | The minaret at dawn over a tiled-roof house | a quiet life of faith, before the day begins | F1 |
| 2 | A dusty football half-hidden under a cot | the passion he hid | F2 |
| 3 | A dead rat in the centre circle, a ball stopped beside it | the truth nobody wants to touch | C-set / 2-05 |
| 4 | A half-dug pit and a shovel | burying the past | F5 |
| 5 | Two fingers sliding a watch across a table | an old man passes memory on | F4 / 4-10 |
| 6 | A boy's face changing in the middle of a fight | what the fight does to him | 6-10 |
| 7 | One rubber sandal in glossy mud | everything stops | B1 / B2 |
| 8 | Two thin palms crossing in an X | the idea of the film | E3 |
| 9 | A child holding a watch to his ear | memory is the time machine | 11-07 |
| 10 | NOT burning off a form, leaving INDIA WILL... | the choice that changes things | 13-09 |
| 11 | Two hands over a muddy rail | admission and friendship | A3 / 23-02 |
| 12 | The watch ticking in a closed fist | back in the present, changed | 23-05 |

## 4. REFERENCE SLOTS — *SUDANI FROM NIGERIA* (2018)
**What I know:** it is a Malayalam film set in Malabar's football culture. I **cannot watch it** and I do not remember individual scenes reliably, so I will **not guess** its details. Please give me the specifics below and I will write them into the plates.
**How it will be used:** as an **atmosphere reference** (the feel of a Malabar football ground and its crowd), not to copy its compositions, characters or shots.

**What to send for each slot (stills, timestamps or a few lines are enough):**
| Slot | Applies to | What I need from you |
|---|---|---|
| **R1 The ground** | C1, C2, A1, B1 | the surface, the pitch edge, the posts, the boundary, the ground's size and shape |
| **R2 The gallery and crowd** | C1, C4, C5 | what the stands are made of, how people sit and stand, what they wear, how loud |
| **R3 Flags, banners, flex boards** | C1, C5 | how clubs and sponsors show themselves, colours, hanging style |
| **R4 The announcer / speaker** | C5, 23-06 | where he sits, his equipment, what he sounds like |
| **R5 Light and time of day** | C1, 6-01 to 6-14 | the match-time light, haze, dust, colours in the sky |
| **R6 Camera** | all of Part 1 | the angles and movements you liked (low, handheld, long lens from the gallery) |
| **R7 Houses and roads** | F1, F7, L06, L07 | roof, wall, veranda, road details of Malabar houses |
| **R8 The palette** | everything 2026 | the dominant colours and the grade |

**When you send them, label each item with the slot (R1 to R8).** I will update the matching plate prompts in `11` and the shot prompts in `10`, and re-run the same story check.

## 5. WHAT STILL NEEDS YOUR DECISION
- Nothing blocking. Send the reference details when ready; until then `11` stands on its own.


<!-- ===== FILE: 06_SCENE_CONTINUITY_MAP.md ===== -->

# 06 — SCENE CONTINUITY MAP (script v4)

Legend: **T** = time of day · **C** = colour state · **Mud** = state of dirt · **Tee** = T-shirt colour.
`[⊕]` = optional scene.

## PART 1 (2026, COLOUR)
| Sc | Location | T | Who | Costume / state | Props | Notes |
|---|---|---|---|---|---|---|
| 1 | L01, L02, L03 | dawn | Jaisal, Grandpa | Jaisal O1 (vest + mundu); Grandpa white | watch on Grandpa, tea, football under cot, firecracker | Azan; no wall photographs |
| 1A ⊕ | L01 | dawn | Jaisal | O1 | football named "Jaisal – U13" | pushes it back harder |
| 2 | L04→L05 | morning | kids, Zidhan, Akhil | Zidhan mustard logo tee, whistle; kids' mismatched kits clean-dirty | notepad, rat, Activa, kaikkott | coconut-tree wipe; Activa 3-shot sequence |
| 2A ⊕ | L05 | morning | kids, Zidhan | same | six stones | quirk shots per kid |
| 3 | L05, L06 | near noon | Father, Akhil, Zidhan, injured boy (X03), Father's son | formal Father | spray can, notepad, "SPRAY: 0", car | Akhil: "Shafiq-ka's son... Rayyan" |
| 4 | L03, L04 | midday | Zidhan, Jaisal, Grandpa | Jaisal teal hibiscus tee, muddy hands | boar, shovel, watch | "Is Grandpa sleeping, or what?", "Naayle...", watch slid across |
| 5 | L07 | afternoon | Jaisal, Shafiq's wife, Rayyan | Rayyan in kit + sandals | phone | |
| 5A ⊕ | L07 | afternoon | Rayyan, Jaisal, mother | same | coconut | "Kaal keduvaratthanda..." |
| 6 | L08 | 6 PM golden | kids, Rockstar, Zidhan, Jaisal, referee, ticket boy, spectators | Winning Eleven kits (splashed); Rockstar black stars | ticket, banners, speaker, yellow card | **time shift at the fight**; Rayyan's foul; Jaisal adjusts the watch |

## PART 2 (1950, B&W + colour survivors)
| Sc | Location | T | Who | Tee state | Notes |
|---|---|---|---|---|---|
| 7 | L10 | amber | Jaisal, Zidhan | full colour | **one sandal in the mud**; Jaisal writes the letter with Zidhan's pen |
| 7A ⊕ | L10 | amber | Jaisal | full | the notebook pages |
| 8 | L11 | afternoon gold | Jaisal, Zidhan, villagers, constable | full colour | the only colour in the village |
| 9 | L12, L19 | late afternoon; night | Zidhan, Sulaiman, Muallim | full | Zidhan writes the telegraph form on the pathemari |
| 10 | L13–L17 | gold, noon | Jaisal + Gopalan, Antappan, Kuttappan, Karunan, Chandu, Velayudhan, Raghavan, constables, fishwife | full | recruitment: **five shots** |
| 11 | L12 | dusk | Jaisal, Sulaiman, Little Abu Bakar, the team line | full | **Jaisal gives the boy the watch**; Moosa, Pakru, Thomas, Bappu, the Vaidyar already in the line |
| 12 | L18 | dawn | team, Sulaiman + boy ashore | slightly muted | coconut mountains; the first coconut floats away |
| 13 | L20 | dawn | Zidhan, Postmaster, messenger | Zidhan salt-streaked | fire in gold; the **NOT** burns first |
| 14 | L21→L18 | morning | Zidhan, Muallim, team | muted | "Where are the other players?"; socks |
| 14A ⊕ | L18 cabin | night | Muallim, Zidhan | muted | route map |
| 15 | L22, L18 | all day / night | team, Muallim, the Vaidyar | **greying daily** | coconut stock shrinks; Bose silhouette one second; tactics board |
| 16 | L23, L24, L25 | misty dawn; day | team, officials, crowd | grey | the FIFA slip; the sung anthem |
| 17 | L26 | day | India vs Sweden | grey | the magic sequence, **the X**; 4–0 |
| 18 | L25/L27 | day | Italy, Paraguay | grey | Zidhan checks bruises |
| 19 | L26 | day | India vs Brazil | grey | the wingers' **X** splits the fullbacks; 3–2 |
| 20 | L28 | night | Jaisal, Zidhan | mostly grey | the quarrel; **"Rayyan made a tactical foul"** |
| 21 | L26 | day | India vs Spain | grey | one shot; Zidhan in the gallery |
| 22 | L26 | day, rain | India vs Uruguay | grey; **soaked mud** | slow-motion "NO / YES"; Jaisal's quiet line; 1–3 |
| 23 | L26 → L08 | rain → 6 PM golden | Jaisal, Zidhan, kids | **grey → colour floods** | handshake; 360° spin; **watch in Jaisal's fist**; scoreboard **WINNING ELEVEN 3 — ROCKSTAR BOYS 1**; commentator |
| 25 | L03 | night | Jaisal, Grandpa | full colour | Jaisal buckles the watch on Grandpa; sand falls; "Frequently." |

## ONE-LINE CHECKS FOR EVERY SHOT
1. Who is in frame, and is their tone/age/kit right for this scene's state?
2. Is the watch where the chain (`04` §1) says it should be?
3. Is the Tee colour right for the drain schedule?
4. Is the mud state right?
5. Is the coconut count right (Sc. 12, 15)?
6. Is the sound rule respected (no instruments)?
7. For spoken lines: is the mouth visible, and the shot long enough for the dub?


<!-- ===== FILE: 01_CAST_2026.md ===== -->

# 01 — CAST 2026 (COLOUR)

> **Faces:** FACE_DESC lines below are superseded by `08_FACE_FEATURE_MATRIX.md` (full 8-feature faces).

Format per entry: ID · NAME · AGE · COMMUNITY · TONE KEY · FACE_DESC · EXPRESSION · POSE · KIT · SIGNATURE · SCENES · CONTINUITY. Build prompts with templates T1–T4 in `00`.

## A. THE LEADS (LoRA-locked; no face sheets)
### J01 JAISAL
- **Age 28–29 · Muslim · tone `DARK`** (warm dark brown). Wavy black hair, slim build. **LoRA:** `krea2jaisal_v3`.
- **Arc:** left the academy after the semi-final; blames "the system"; digs the boar's grave; watches the final from the gallery; shifts time at the fight.
- **Outfits (outfit comes from the prompt, not the LoRA):**
  - `O1` Scene 1 morning/prayer **[PROPOSED]**: plain white cotton vest and white mundu, barefoot.
  - `O2` Scenes 4–8, 10–25: **teal tee with a large printed hibiscus** (`TEE_JAISAL_HIBISCUS` = `[USER-SUPPLIED]`, 3D-graphic style), dark jeans or trousers, plain trainers. In 1950 the tee drains toward grey over the voyage.
- **Props:** Grandpa's watch (from Scene 4), Zidhan's pen (from Scene 7), folded position list (Scene 10).
- **States:** `S4` mud to the knees and muddy hands (grave). `S10E` sweaty, carrying a basket of fish. `S23` tee fully grey, wrist bare, then the watch in his fist.

### Z01 ZIDHAN
- **Age ~28 · Muslim · tone `DARK`**. Black hair in a loose top bun, slim, **beard in every shot**. **LoRA:** `krea2zidhan_v3`.
- **Outfit:** **mustard tee with the team logo** (open hand in a ring; `TEE_ZIDHAN_LOGO` = `[USER-SUPPLIED]`), dark trousers, rubber slippers or old sports shoes. Whistle on a string around the neck.
- **Props:** notepad + pen (until Scene 7, when Jaisal borrows the pen), the empty spray cap in his pocket (Scene 3).
- **States:** `S2` dry; `S6` splashed; `S13` smelling of sea, tee salt-streaked; `S23` drenched.

## B. SUPPORTING ADULTS 2026 (t2i sheet + identity-edit; no LoRA)
### A01 GRANDPA ABU BAKAR
- **~81 · Muslim · tone `DARK`**, weathered, age-spotted. Thin frame, white beard, deep-set eyes, big ears, prominent nose, frail hands, a white prayer cap.
- **Outfit:** white half-sleeve shirt, white mundu. Sits in "stillness" in a chair facing the window. **The watch on his left wrist** (Scenes 1, 4 until he slides it; Scene 25 after Jaisal returns it).
- **Family rule:** Jaisal's features must read as his grandson's (same brow, same smile). **Little Abu Bakar (1950) and Sulaiman are generated FROM this face anchor.**
- Prompt DESC: `a thin elderly man, deep-set far-away eyes, large ears, prominent nose, white beard, white prayer cap, frail veined hands, completely still`.

### A02 AKHIL
- **18–20 · Hindu · tone `TAN`**. Slim, quick, friendly smile, short hair, light stubble.
- **Outfit:** faded checked shirt, a mundu folded up to the knee, rubber slippers.
- **Props:** **Activa** (dented scooter, mud on the wheels), **kaikkott** (Kerala shovel, worn wooden handle). Scenes 2, 3.

### A03 THE FATHER
- **~40 · Muslim · tone `WHEATISH`**. Tense, keeps checking his watch.
- **Outfit:** a crumpled formal white shirt, trousers, dusty sandals, a **wedding suit/dress on a hanger** in the car. Scene 3.

### A04 SHAFIQ'S WIFE
- **~35 · Muslim · tone `FAIR`**. Wary, practical, loving.
- **Outfit:** a long printed cotton house-dress, a soft-coloured **thattam (headscarf)**, hands wet from laundry. Scenes 5, 5A.
- **Shafiq (Jaisal's cousin, Rayyan's father)** is in the Gulf, **off-screen**; WhatsApp UI only (Scene 5).

### EXTRAS 2026 (generic, no sheets; build as needed)
| ID | Who | Detail |
|---|---|---|
| X01 | **The referee** (Sc. 6) | ~40, worn local man, grey shirt, whistle, **yellow card** |
| X02 | **Ticket boy** (Sc. 6) | ~10, school shirt, school notebook, plastic bucket |
| X03 | **Father's son** and **injured boy "Nidhin"** (Sc. 3) | two 11–12-year-olds (not in the 12); Nidhin has a twisted ankle |
| X04 | Paddy farmers (Sc. 2, 6) | 3–4 men with palm-leaf umbrellas |
| X05 | Gallery spectators (Sc. 6) | 30–40 mixed villagers on the plank gallery |
| X06 | The commentator (Sc. 23) | **voice only**, no face |

## C. THE WINNING ELEVEN KIDS (11–12 years old; 5-a-side)

**Tone split:** FAIR (6): Alan, Govind, Bilal, Rishi, Vihaan, Tobin · WHEATISH (4): Rayyan, Sinan, Kailas, Muhsin · TAN (2): Kiran, Sreehari.
**Religion split (matches 1950 counterpart):** Muslim: Bilal, Sinan, Muhsin (+ Rayyan) · Hindu: Govind, Rishi, Vihaan, Kailas, Kiran, Sreehari · Christian: Alan, Tobin.

### STARTERS (on the pitch)
#### K01 RAYYAN (formerly Adam)
- **11 · Muslim · `WHEATISH`** · **Shafiq's son, Jaisal's nephew**; calls his mother **Umma**. The tallest, a head above the others; shy, desperate to play. **The tactical foul and the fight (Sc. 6). The most important kid.**
- **FACE_DESC:** a tall, lean boy, long neck, sharp angular features, high cheekbones, narrow chin, thick straight eyebrows, wide shy eyes, short black hair cut unevenly at home with a small cowlick at the crown, a touch of Jaisal's brow line.
- **EXPRESSION:** shy hope. **POSE:** standing straight, oversized hands and feet.
- **KIT:** faded red football jersey a size too big, grey cotton shorts, thin socks over **shin guards made of folded newspaper**, worn **rubber sandals (no boots)**.
- **SCENES:** 5, 5A, 6, 7 (one sandal left in the mud), 20, 23.

#### K02 ALAN (GK) — echoes Antappan
- **11 · Christian · `FAIR`.** Stocky, sturdy, calm, unbothered.
- **FACE_DESC:** round solid face, full cheeks, broad flat nose, small steady eyes, thick short neck, close-cropped hair. **EXPRESSION:** calm. **POSE:** planted, feet apart.
- **KIT:** oversized faded green goalkeeper jersey, long grey shorts, plain socks, worn canvas shoes, **no gloves**, dusty palms.

#### K03 GOVIND (captain) — echoes Gopalan
- **11 · Hindu · `FAIR`.** Confident, strong jaw.
- **FACE_DESC:** square face, strong jaw, straight nose, thick dark eyebrows, steady direct eyes, short side-parted hair with a little oil sheen, a small mole beside the right eyebrow. **EXPRESSION:** calm authority, lips pressed. **POSE:** upright, shoulders back.
- **KIT:** faded yellow jersey, a **strip of torn white cloth tied round the left upper arm as an armband**, navy shorts, scuffed boots.

#### K04 BILAL (long passer) — echoes Bappu
- **11 · Muslim · `FAIR`.** Lean, long-legged (second tallest), dreamy and focused.
- **FACE_DESC:** narrow face, long straight nose, deep-set thoughtful eyes, slightly prominent ears, wavy black hair falling over the forehead. **POSE:** weight on one leg, relaxed.
- **KIT:** white jersey with a torn collar, faded blue shorts, socks of two different shades, worn boots.

#### K05 RISHI (striker) — echoes Raghavan
- **11 · Hindu · `FAIR`.** Small, wiry, fast, mischievous.
- **FACE_DESC:** sharp cheekbones, bright darting eyes, thin eyebrows, a lopsided half-grin with a chipped front tooth, close-cropped hair with a faint shaved line above the left ear. **POSE:** on the balls of his feet, knees bent.
- **KIT:** faded orange jersey, short green shorts, thin socks, light worn boots.

### BENCH (generate only if a shot needs them)
#### K06 SINAN — "the stubborn one" — echoes Pakru
- **11 · Muslim · `WHEATISH`.** **FACE_DESC:** rounded determined face, heavy low eyebrows, set jaw, lips pressed into a stubborn line, short tightly curled hair. **POSE:** **arms folded across the chest.** **KIT:** faded maroon jersey, grey shorts, plain socks, scuffed boots.

#### K07 VIHAAN — the loud little defender — echoes Velayudhan
- **11 · Hindu · `FAIR`.** The smallest. **FACE_DESC:** wide mouth, a missing front baby tooth, big ears, round bright eyes, shaggy hair, always mid-shout. **POSE:** chest puffed, fists on hips. **KIT:** striped blue-and-white jersey hanging almost to his knees, dark shorts, mismatched socks, boots slightly too big.

#### K08 KAILAS — the fast one — echoes Kuttappan
- **11 · Hindu · `WHEATISH`.** **FACE_DESC:** lean, long-limbed, high forehead, angular face, easy quick eyes, buzz cut. **POSE:** loose and springy. **KIT:** faded light-grey jersey with green sleeves, light shorts, ankle socks, light boots.

#### K09 KIRAN — the jumpy one — echoes Karunan
- **11 · Hindu · `TAN`.** **FACE_DESC:** wiry, restless, unruly curly hair, big bright eyes, a quick mischievous grin, thin arms, a healing scab on one elbow. **POSE:** bouncing on his toes. **KIT:** faded purple jersey, brown shorts, socks sliding down; optional pose: one boot on, one off.

#### K10 SREEHARI — the biggest, a gentle giant — echoes Chandu
- **11 · Hindu · `TAN`.** **FACE_DESC:** broad wide-jawed face, thick neck, round chin, big hands, short hair, gentle soft eyes that contrast with his size. **POSE:** solid, feet apart. **KIT:** stretched grey jersey, long dark shorts, thick socks, large worn boots.

#### K11 MUHSIN — the organiser — echoes Moosa
- **11 · Muslim · `WHEATISH`.** **FACE_DESC:** narrow face, small neat features, a tidy side parting, careful watchful eyes. **POSE:** **one hand half-raised, two fingers pointing as if directing someone.** **KIT:** faded sky-blue jersey tucked in neatly, light shorts, clean socks, plain boots.

#### K12 TOBIN — the quiet one who always knows — echoes Thomas
- **11 · Christian · `FAIR`.** **FACE_DESC:** oval face, hooded calm eyes, **one eyebrow slightly higher than the other**, a closed-mouth half-smile, neatly combed hair. **POSE:** still, hands loose. **KIT:** faded white-and-red striped jersey, grey shorts, plain socks, worn boots.

## D. THE ROCKSTAR BOYS (12–13; bigger and broader but clearly children)
**Shared kit:** matching **black football jersey with a cluster of printed silver stars on the chest**, black shorts, black socks, clean boots. A **speaker on a stool** on their sideline. They look like a rock band: neat, matching, a little too proud.
**Kid block variant:** `A real 12-year-old Malayali boy from Kerala, {TONE}, bigger and broader than the average boy his age but still clearly a child, {CONSTANTS}.`

| ID | Name | Role | Community · Tone | FACE_DESC |
|---|---|---|---|---|
| R01 | **Hashim** | striker (breaks clear; grabs Rayyan's shirt) | Muslim · `FAIR` | taller than the others, athletic, a smirk, sharp jaw, trendy hair with faded sides and the top swept up, confident eyes |
| R02 | **Abhijith** | big defender (the tallest and widest) | Hindu · `WHEATISH` | tall and heavy-set, thick neck, broad flat face, heavy-lidded eyes, short cropped hair, a bored intimidating look |
| R03 | **Jerin** | captain | Christian · `FAIR` | medium height, neat features, self-satisfied, perfectly combed hair, a thin black armband |
| R04–R05 | two unnamed teammates | filler | mixed | generic, same kit |

**Team shot prompt:** `Five boys aged 12 to 13 in Kerala lined up on a muddy paddy-field pitch in matching black football jerseys with printed silver stars, black shorts and clean boots, standing like a rock band, a bigger and broader group than ordinary kids their age, a speaker box on a stool on the sideline behind them, wet green paddy and coconut palms behind, harsh late-afternoon light, {STYLE TAIL}`


<!-- ===== FILE: 02_CAST_1950.md ===== -->

# 02 — CAST 1950 (generate in COLOUR; B&W grade is applied in post)

> **Faces:** FACE_DESC lines below are superseded by `08_FACE_FEATURE_MATRIX.md` (full 8-feature faces).

**Rule:** completely different people from the 2026 kids. Period look: simple cotton shirts, mundus, 1950s haircuts, sun-worn skin. Ages are adult and varied (22–45), so they read as men, not as grown-up kids.
**Block:** use the 1950 block from `00`. Tone is set per entry.
**Costumes:** each man has `VILLAGE` (Scene 8–10 selection) and `KIT` (Scenes 16–23).

## THE INDIA KIT (Brazil, Scenes 16–23)
Shirts sewn by Sulaiman's sailmakers from **off-white sailcloth dyed with turmeric (golden ochre) and indigo trim**, hand-stitched numbers, a **small hand-stitched tricolour patch** on the chest, mismatched socks (some wear the striped socks Zidhan bought), some **barefoot**, some in **borrowed leather boots tied with rope**. No printed text, no brands. They look like the poorest team in the world.

## A. THE 11 PLAYERS
| # | ID · Name | Age · Community · Tone | Role (Life-IQ) | FACE_DESC / BUILD | VILLAGE costume | KIT footwear |
|---|---|---|---|---|---|---|
| 1 | **P01 Antappan** (GK) | 38 · Christian · `DARK` | fisherman: "I look where the fish will be afraid" | tall, narrow shoulders, salt-bleached brows and hair, half-closed eyes against glare, net-rope scars on the forearms | faded checked lungi, sleeveless vest | rope-tied canvas shoes, bare hands |
| 2 | **P02 Chandu** (RB) | 26 · Hindu · `DARK` | coir maker (husk beater) | wide jaw, thick neck, calves like coconut trunks, rope-burned palms | mundu folded high, bare chest, towel on shoulder | barefoot |
| 3 | **P03 Moosa** (CB) | 40 · Muslim · `WHEATISH` | market manager who conducts a crowd with two fingers | tall, lean, beaky nose, long fingers, a white crochet cap tilted | white shirt, checked lungi | borrowed leather boots tied with rope |
| 4 | **P04 "Illa" Pakru** (CB) | 34 · Muslim · `WHEATISH` | the man who says "no" | heavy brows, jutting jaw, one folded ear, permanently folded arms | faded half-sleeve shirt, mundu | scuffed boots |
| 5 | **P05 Velayudhan** (LB) | 28 · Hindu · `DARK` | coir maker | short, barrel chest, shaved sunburnt head, a gap in the teeth | bare chest, towel, mundu | barefoot |
| 6 | **P06 Thomas** (DM) | 43 · Christian · `FAIR` | twenty-eight card player | hooded eyes, one eyebrow higher, ink-stained thumb, grey temples | white half-sleeve shirt, mundu, a deck of cards tucked in the waist | plain shoes with the striped socks |
| 7 | **P07 Gopalan** (CM) | 45 · Hindu · `WHEATISH` | coconut counter | thin, wire spectacles, high forehead, lips move when counting | crisp white shirt, immaculately folded mundu | plain leather shoes, socks |
| 8 | **P08 Bappu** (AM) | 30 · Muslim · `WHEATISH` | tea master (the long pour) | lean forearms with tiny burn marks, long fingers | sleeves rolled, lungi, **tea-cloth over one shoulder** | striped socks, rope-tied boots |
| 9 | **P09 Kuttappan** (RW) | 24 · Hindu · `TAN` | arecanut climber | lean, **rope loop at the ankles**, bare calloused soles | short mundu, bare chest | barefoot |
| 10 | **P10 Karunan** (LW) | 22 · Hindu · `TAN` | arecanut climber | wiry, quick knife-thin grin, bark-scarred forearms | short mundu, bare chest | barefoot |
| 11 | **P11 Raghavan "Kallan"** (ST) | 25 · Hindu · `WHEATISH` | the thief | lean, sharp cheekbones, **scar through the left brow**, toes that grip | torn shirt, patched mundu | striped socks |

**Prompt assembly (example, P07 Gopalan T1):** 1950 block (45, `WHEATISH`) + `thin face, wire spectacles, high forehead, lips slightly moving as if counting` + T1 tail; costume: `crisp white half-sleeve shirt and immaculately folded white mundu`; EXPRESSION: `quietly calculating`.

## B. SUPPORTING CAST 1950
| ID | Name / role | Age · Community · Tone | Look (key) | Rule |
|---|---|---|---|---|
| S01 | **Sulaiman** (great-grandfather, ship master; stays ashore) | ~55 · Muslim · `DARK` | broad, white-streaked beard, dark waistcoat, thick leather belt, lungi, white cap, **no watch on his wrist**, a ship-master's bearing | **Same bone structure as Grandpa Abu Bakar (his son)**: generate FROM A01's anchor, 25 years younger, broader |
| S02 | **Little Abu Bakar** (age 5) | 5 · Muslim · `DARK` | tiny white mundu, no shirt, big ears, wide eyes | **Generate FROM Grandpa's face anchor age-regressed**; he must look like the old man in the chair |
| S03 | **Muallim Moideen** (navigator) | ~70 · Muslim · `DARK` | white skull-cap, **milky eyes**, rolled chart under the arm, a calm stare | sails on the pathemari and the MARJAN |
| S04 | **Vaidyar Madhavan** (village healer, **background physio**) | ~65 · Hindu · `WHEATISH` | white mundu, faint sandal-paste mark, a cloth bag of oil bottles | **Never a coach.** Voyage montage: kneads calves at sunset. Optional single shot: pulled from an ayurvedic shop |
| S05 | **Madras Postmaster** | ~50 | stout, handlebar moustache, spectacles on a string | Scene 13 |
| S06 | **Federation messenger** | ~30 | neat uniform, satchel, hurried | Scene 13; hands over the telegraph form |
| S07 | **Madras post-office extras** | — | a fat man, clerks, a clerk with a tray of stamps | Scene 13 |
| S08 | **The two constables** | ~35 | khaki, belts, one friendly | Scenes 8, 10E; one tips his cap at Jaisal |
| S09 | **The tailor** | ~50 | at a treadle sewing machine, tape round the neck | Scenes 8, 12 |
| S10 | **The boy who touches the T-shirt** | 6 | bare chest, shorts | Scene 8 |
| S11 | **Two women at the well** | ~40 | cotton saris/mundus, brass pots | Scene 8 |
| S12 | **Man on a bicycle** | ~35 | rides into the fence post | Scene 8 |
| S13 | **The fishwife** | ~45 | basket of mackerel | Scene 10E |
| S14 | **MARJAN crew + cook** | — | 6–8 sailors, a cook | Scenes 11, 12, 15 |
| S15 | **FIFA official, journalist, clerk, band leader** | — | 1950 Brazilian offices, pinstripe suit, flat cap | Scene 16 |
| S16 | **Opposing players** | — | Sweden: tall, fair, **yellow** · Italy: dark blue, grave, captain who stares at the sea · Brazil: **white** shirts · Spain: red · Paraguay: check references · **Uruguay: sky-blue, hard, a quiet captain** and a striker who says "YES" | Real people are **not to be depicted**: build generic 1950 footballers |
| S17 | **Bose silhouette** | — | tall figure in a long dark coat, round-rimmed spectacles, a cap, seen against the stars | Scene 15, one second. A fictional silhouette only, no face |
| S18 | **Maracanã crowd** | — | thousands in 1950 hats and paper flags | plate/crowd tool, no individual faces |

**Uruguay captain (script: "Varela"):** the script names a real person. Render a **fictional** quiet captain with a closed-door face, in sky blue; do not seek a likeness.

## C. FAMILY RESEMBLANCE (rules for the identity-edit step)
- **Grandpa (A01) → Sulaiman (S01) → Little Abu Bakar (S02)** share the same brow, ears and nose.
- **Jaisal (J01) → Rayyan (K01):** a subtle shared brow line and smile (nephew).
- Do not link any 1950 player to any 2026 kid by face.


<!-- ===== FILE: 08_FACE_FEATURE_MATRIX.md ===== -->

# 08 — FACE FEATURE MATRIX (source of truth for faces)

**Purpose:** guarantees that characters do not look alike. `01_CAST_2026.md` and `02_CAST_1950.md` hold role, age, community, kit; **this file overrides their FACE_DESC lines.**

**Rules for any new or edited character (the MCP model must follow them):**
1. Every character needs all 8 categories: **head shape, hairline and hair, eyebrows, eyes, nose, lips, jaw and chin, ears.**
2. Within a group, **no two characters may share more than 2 of the 8 categories**, and **never the same nose + jaw + ears together.**
3. Add marks, facial hair and (for adults) visible skin detail as separate sentences.
4. Women: follow the modesty rule in `00` (all hair covered, only face and hands visible); for them hairline and ears are listed as covered.
5. Family resemblance exceptions (intended): Grandpa, Sulaiman and Little Abu Bakar share large ears, a prominent nose and deep-set eyes.


## Winning Eleven and Rockstar kids (2026)

| ID | Name | Head | Hair / hairline | Brows | Eyes | Nose | Lips | Jaw / chin | Ears | Extra |
|---|---|---|---|---|---|---|---|---|---|---|
| K01 | RAYYAN | long and narrow | an uneven home-cut: longer on top with a loose side-swept fringe falling across the right side of the forehead and ragged edges, a small cowlick sticking up at the crown, about half the forehead covered | thick, straight and set low over the eyes | wide-set, large and almond-shaped, with a shy gaze | straight and narrow with a slightly pointed tip | small and full | narrow, with a soft jawline and a small chin | medium-sized and slightly protruding | He has a long neck and slightly oversized hands. |
| K02 | ALAN | round and full | short thick hair brushed forward into a stubby flat fringe covering the top third of the forehead, a low straight hairline, a small forehead | light and sparse | small, round and deep-set | short, broad and flat with wide nostrils | thick and full | wide and soft, with a short thick neck | small and close to the head, with attached lobes | He has full cheeks. |
| K03 | GOVIND | square, with a broad forehead | a neat school-boy side parting on the left, hair combed flat and oiled to a shine, a clean straight hairline with a small widow's peak, the forehead fully exposed | dark, thick and strongly defined, level | steady, direct and almond-shaped | medium in length with a straight bridge and a blunt squared tip | firm and medium | strong and square, with a faint dimple in the chin | medium-sized and lying flat against the head | He has a small mole beside the right eyebrow. |
| K04 | BILAL | narrow across the forehead and slightly wider at the jaw | longer wavy hair in a centre parting, curtain locks hanging over both temples down to the ears, the forehead partly covered, a low hairline in the middle | thin and softly arched | deep-set and hooded, with slightly downturned outer corners, thoughtful | long and straight with a faintly hooked tip | thin | narrow with a pointed chin | large and clearly sticking out | He is lean and long-legged. |
| K05 | RISHI | small and heart-shaped, broad across the forehead and narrow at the chin | a short spiky gelled top standing up, shaved short sides with a faint shaved line above the left ear, an M-shaped hairline, the forehead fully exposed | thin and sharply angled upward | large, bright and slightly upturned, always darting | small and upturned | thin, in a lopsided grin showing a chipped front tooth | a small sharp chin with prominent cheekbones | small and neat, slightly pointed at the top | He is small and wiry. |
| K06 | SINAN | wide and round with a flat top | short dense tight curls forming a rounded cap, the hairline so low the curls nearly touch the eyebrows, only a narrow strip of forehead showing | heavy, low and nearly meeting | narrow and deep-set, with a stubborn glare | broad with a bulbous tip and a low bridge | pressed together, with a full lower lip | a set, square jaw | small and set tight against the head | He has a thick stubborn neck. |
| K07 | VIHAAN | small and round | a shaggy straight bowl cut with a thick blunt fringe cut straight across just above the eyebrows, hair covering the tops of the ears | light and high-arched, giving a permanently surprised look | round, big and bright | a tiny button nose | wide, with a missing front baby tooth | a tiny soft chin | big and flaring | He is the smallest boy in the team. |
| K08 | KAILAS | a long oval with a high forehead | a very short buzz cut of uniform length, the skull shape clearly visible, a high rounded hairline and a tall forehead fully exposed | straight and medium-thick | narrow, relaxed almond eyes | long with a high straight bridge and narrow nostrils | medium and relaxed | an angular, narrow jaw | small and set high on the head | He is lean and long-limbed. |
| K09 | KIRAN | wide, with prominent cheekbones | a wild, thick, springy curly mop, longer on top and around the ears, uneven tufts, a ragged hairline low on the forehead, hair partly covering the ears | bushy and irregular | big, round, bright and wide-set | wide, with the tip tilted slightly to the left | wide in a quick grin, with a thin upper lip | a small chin | medium-sized and low-set | He has thin arms, a thin neck and a healing scab on one elbow. |
| K10 | SREEHARI | large, heavy and broad | short, thick, straight hair cut evenly all round like a helmet, the front edge a low straight line across a small forehead, no parting | thick and level | small, soft and heavy-lidded | broad across the bridge with a soft rounded tip | full | wide, with a round chin and a slight double chin | large with long lobes, low-set | He has a thick neck and big hands. |
| K11 | MUHSIN | small and egg-shaped | hair combed straight back and held tight with a glossy finish, a high clean hairline, the forehead fully exposed, sides trimmed close | thin, neat and slightly arched | small, close-set and watchful | small and straight with narrow nostrils | thin and composed | a small delicate chin and a light jaw | small and close to the head | He keeps one hand half-raised, as if directing someone. |
| K12 | TOBIN | a smooth oval | soft fine slightly wavy hair grown out a little long, brushed up and back from the forehead in a loose quiff, a smooth rounded hairline | medium, one eyebrow sitting slightly higher than the other | hooded, calm and almond-shaped | medium and slightly aquiline, with a narrow tip | medium, in a closed-mouth half-smile | a soft oval chin | medium, with slightly pointed tops | He is quiet and still. |
| R01 | HASHIM | long | a high skin fade with the sides almost bald and the top longer, swept up and back in a styled pompadour, a high sharp hairline | thick and slanted, giving a confident look | sharp, narrow and slightly upturned | straight with a high bridge and a sharp tip | thin, in a permanent smirk | a sharp, angular jaw | small and neat, lying flat | He is taller than the others and athletic. |
| R02 | ABHIJITH | broad and heavy, block-shaped | short cropped hair of even length all over, a low, straight, slightly uneven hairline and a heavy forehead | heavy and straight | small and heavy-lidded | wide, with a slightly crooked bridge, as if once knocked | wide and flat | a very wide square jaw above a thick neck | thick and lobeless | He is the tallest and widest of the Rockstar boys. |
| R03 | JERIN | a refined oval | a stylish textured crop: tapered sides, the top brushed forward into a sharp gelled fringe touching the eyebrows | neatly shaped and arched | large almond eyes with long lashes | slim and straight with a slightly upturned tip | thin and smug | a tapered chin | small | He wears a thin black captain's armband. |

## Adults and extras (2026)

| ID | Name | Head | Hair / hairline | Brows | Eyes | Nose | Lips | Jaw / chin | Ears | Extra |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | Grandpa Abu Bakar | long and thin | a high forehead, thin white hair under a prayer cap | long, wispy and white | deep-set, with drooping lids and a cloudy far-away gaze | long, prominent and beaked | thin, mostly hidden in the beard | gaunt, under a full white beard | large, with long drooping lobes | He has deep wrinkles, age spots and hollow cheeks. Deep wrinkles, age spots and loose skin. |
| A02 | Akhil | a long oval | a widow's peak, short thick wavy black hair | thick, straight and dark | warm almond-shaped, crinkling when he smiles | medium and straight with slightly wide nostrils | full, in a wide open smile | a defined jaw with light stubble | medium-sized and slightly protruding | He has thin sideburns. Visible pores and a few blemishes. |
| A03 | The Father | broad and square | a receding M-shaped hairline, short black hair going grey at the temples | thick and drawn together in worry | tired and heavy-lidded, with bags and slightly downturned corners | broad and straight with a fleshy tip | thin and pressed | square, with slight jowls | large with fleshy lobes | He has a trimmed moustache and worry lines across the forehead. Visible pores, fine lines and uneven sun-marked skin. |
| A04 | Shafiq's wife | a soft oval face framed by the hijab | all hair, ears, neck and chest fully covered by a modern pastel hijab | thick and arched | large, dark and almond-shaped | small and straight | full | a soft jaw with a small dimple in the chin | covered by the hijab | Only her face is visible. |
| X01 | Referee | long and narrow | a high receding hairline and a bald crown, short grey-black hair at the sides | bushy and grey-flecked | small, creased and tired | large and hooked, with a bump on the bridge | thin | lean, with hollow cheeks | large, with prominent cartilage | He has a grey-flecked moustache. Visible pores, fine lines and uneven sun-marked skin. |
| X02 | Ticket boy | small and round | hair shaved close at the sides, a short top with a small tuft at the front, the forehead mostly bare | thin and straight | small, sharp and watchful | small and straight | thin and businesslike | a small pointed chin | small |  |

## India team (1950)

| ID | Name | Head | Hair / hairline | Brows | Eyes | Nose | Lips | Jaw / chin | Ears | Extra |
|---|---|---|---|---|---|---|---|---|---|---|
| P01 | ANTAPPAN (GK) | long and narrow, weathered | a hairline receding at the temples, short salt-bleached hair | pale, bleached and sparse | narrow, deep-set and half-closed, with deep crow's feet | long and aquiline with a bump on the bridge, the skin sunburnt and peeling | thin and cracked | a lean angular jaw with stubble | pointed and sun-darkened | He has net-rope scars on his forearms and sun-creased skin. Visible pores and lightly sun-marked skin. |
| P02 | CHANDU (RB) | big and square | a close-shaved head with a stubble shadow on the scalp and a low straight hairline | thick and level | small and calm | broad and flat with wide nostrils | thick | a massive square jaw | thick and small, close to the head | He has a thick neck and rope-burned palms. Visible pores and lightly sun-marked skin. |
| P03 | MOOSA (CB) | long and narrow | hair mostly hidden under a tilted white crochet cap | thin and high-arched, amused | bright, large, wide-set and slightly upturned | very prominent and beaky | thin and wide, often smiling | a narrow, pointed chin | large and sticking out beside the cap | He has a thin moustache. Visible pores, fine lines and uneven sun-marked skin. |
| P04 | "ILLA" PAKRU (CB) | wide and heavy-browed | a short, coarse, spiky salt-and-pepper crop with a low hairline | heavy and overhanging | deep-set and narrow | broad, with the bridge bent to one side as if once broken | tight and unimpressed | a jutting, underbitten jaw | one ear folded over | He is stern and unmoving. Visible pores and lightly sun-marked skin. |
| P05 | VELAYUDHAN (LB) | round, shaved and sunburnt | a shaved scalp | short and thick | small, bright and crinkled | short and wide, snub | wide and full, grinning with a gap between the front teeth | a round, wide jaw | small and flat | He has a barrel chest and a thick neck. Visible pores and lightly sun-marked skin. |
| P06 | THOMAS (DM) | a long oval | a high hairline receding at the temples, neatly combed black hair greying at the sides | thin, one eyebrow higher than the other | hooded and calm | thin and straight with a high bridge | thin, in a half-smile that gives nothing away | a soft jaw with a slight jowl | medium-sized | He is clean-shaven, with fine lines on his fair skin and an ink-stained thumb. Visible pores, fine lines and uneven sun-marked skin. |
| P07 | GOPALAN (CM) | narrow, with a high domed forehead | thin oiled hair receding from a high forehead | faint and thin | small and precise behind round wire-rimmed spectacles | long and pinched | thin and pursed, as if counting | a small receding chin | sticking out slightly at the top | He has a thin neck with a prominent Adam's apple. Visible pores, fine lines and uneven sun-marked skin. |
| P08 | BAPPU (AM) | oval | a low neat hairline, short wavy black hair | thick and expressive | warm almond-shaped, with laugh lines | medium and straight with a rounded tip | full, in an easy wide smile | a soft jaw with light stubble | medium-sized and lying flat | He has small burn marks on his forearms. Visible pores and lightly sun-marked skin. |
| P09 | KUTTAPPAN (RW) | narrow and sun-browned | hair grown a little long and tied in a small knot at the back of the head, a low hairline | thin and straight | bright, alert and narrow | straight and narrow with a high bridge | medium | a lean angular jaw | small and flat | He has a wiry neck and calloused hands. Visible pores and a few blemishes. |
| P10 | KARUNAN (LW) | small and angular | a low hairline, unruly wiry black hair | thin and sharply slanted | restless, bright and slightly upturned | small and upturned | thin, in a quick knife-thin grin | a pointed chin | small and pointed | He has bark-scarred forearms. Visible pores and a few blemishes. |
| P11 | RAGHAVAN "KALLAN" (ST) | heart-shaped, with a broad forehead and a narrow chin | a sharp widow's peak, hair oiled and combed straight back | one eyebrow split by a scar | quick, wary, close-set and narrow | straight and sharp, the tip bent slightly | thin, in a wary half-smile | a narrow jaw with sharp cheekbones and hollow cheeks | small and close | He has a scar running through the left eyebrow. Visible pores and lightly sun-marked skin. |

## Supporting cast (1950)

| ID | Name | Head | Hair / hairline | Brows | Eyes | Nose | Lips | Jaw / chin | Ears | Extra |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | Sulaiman | large and broad | a white cap over short grey-black hair | thick, bushy and dark | deep-set and steady | prominent, with a straight bridge and a broad base | thin, mostly hidden in the beard | a strong square jaw under the beard | large, like his son's | He has a white-streaked full beard. Visible pores, fine lines and uneven sun-marked skin. |
| S02 | Little Abu Bakar | round and small | soft, fine, baby-like hair, a little long, falling in loose curls over the forehead and ears, a soft low hairline | faint and soft | wide, round and curious | small, with the first hint of a beaked bridge | small, in a gap-toothed grin | a tiny round chin | big, just like his father's and his grandson's |  |
| S03 | Muallim Moideen | long and narrow | a bald crown under a white skull-cap, white hair at the sides | bushy and white | milky and clouded, calm | broad and flat | thin | a small chin under a short white beard | big | He has deep lines in his face. Deep wrinkles, age spots and loose skin. |
| S04 | Vaidyar Madhavan | round and gentle | a high hairline with a short white crop | soft and white | kind and round | medium and rounded | soft | a soft round jaw with a small double chin | with long lobes | He has a faint sandal-paste mark on the forehead. Deep wrinkles, age spots and loose skin. |
| S05 | Postmaster | wide and round | a balding top with a few combed strands | thick and black | small, behind spectacles hanging on a string | bulbous with a red tip | thin | jowly | small | He has a handlebar moustache and a sweating forehead. Visible pores, fine lines and uneven sun-marked skin. |
| S06 | Messenger | a narrow oval | oiled hair with a sharp side parting | thin and neat | large and alert | straight | neat | narrow | slightly protruding | He has a thin neat moustache. Visible pores and lightly sun-marked skin. |
| S08 | Constable | round | short hair under a khaki cap | thick | kind, small and tired | broad | full | round | small | He has a thick moustache. Visible pores and lightly sun-marked skin. |
| S09 | Tailor | long and narrow | thin greying hair, a high hairline | sparse | small and patient behind thin spectacles | thin and long | thin | narrow | large | He has a tape measure round his neck. Visible pores, fine lines and uneven sun-marked skin. |
| S13 | Fishwife | a square face with high cheekbones | all hair, ears and neck fully covered by a white thattam (head cloth) | thick | sharp and bright | strong and straight | full | a strong jaw | covered by the head cloth | Only her face is visible. |

<!-- ===== FILE: 03_LOCATIONS.md ===== -->

# 03 — LOCATIONS

Columns: ID · name · scenes · time/light · key set dressing · camera note · sound · colour · blockout status.
**Blockout status:** `READY` (in the graybox set), `EXTEND`, `NEW`.

## 2026 (COLOUR)
| ID | Location | Scenes | Time / light | Set dressing | Camera / sound | Blockout |
|---|---|---|---|---|---|---|
| L01 | **Jaisal's bedroom** | 1, 1A | dawn, blue to pale gold | a cot, a plastic chair, a stopped wall clock, muddy football socks on the window bar, **a football half-hidden under the cot** (name written on it), **no wall photographs** | low handheld; the Azan, the watch tick | EXTEND (S3) |
| L02 | **Kitchen** | 1 | dawn | fridge with fresh mint, a steel kettle, glasses | close, steam; kettle hiss | EXTEND (S3) |
| L03 | **Grandpa's room** | 1, 4, 25 | dawn; late afternoon; night | a chair facing a window, a small table (the tea, the watch), a ceiling fan | still frames; the watch tick | READY (S3) |
| L04 | **Backyard (parambu)** | 1→2, 4 | morning | coconut palms, wet earth, the **boar grave pit**, dead boar, cracker trap, a washbasin | wide, cluttered; scraping shovel, dogs barking far | READY (S2) + boar grave |
| L05 | **Paddy training ground** | 2, 2A, 3 | late morning, hard sun | muddy paddy, farmers at the edges, **dead bandicoot in the centre circle ("no-go")**, six stones for the drill | handheld; coconut-leaf wind, bird calls | READY (S1) → EXTEND |
| L06 | **Field edge / road (Father's car)** | 3 | near noon | a dented white Ambassador car at the edge | wide; engine idle | READY (S6 village) |
| L07 | **Shafiq's house + pathway** | 5, 5A | afternoon | a house front, a clothes line, a path, a coconut palm | medium; crows, a dropped coconut | READY (S6 village) → EXTEND |
| L08 | **The match ground (5-a-side)** | 6, 23 | **6 PM, low golden light** | plank-and-bamboo **gallery**, a boundary rope, a banner reading **"THE FINAL — 6 PM"**, the **WINNING ELEVEN bedsheet banner** (open hand in a ring) on two bamboo poles, a **ticket booth boy**, the Rockstar **speaker on a stool**, a **wooden scoreboard** (sliding numbers, ends at 3–1) | handheld; crowd murmur, whistle | READY (S5) → EXTEND |

## 1950 (B&W; sheets in colour)
| ID | Location | Scenes | Time / light | Set dressing | Sound | Blockout |
|---|---|---|---|---|---|---|
| L10 | **Silent stadium (the same ground, B&W)** | 7, 7A | amber golden hour | the ground, empty gallery, footprints glossy in the mud, **one rubber sandal** in the mud | a single watch tick | READY (S5) |
| L11 | **Village road and fork** | 8 | afternoon gold | tin-roofed tea shop, a well, a tailor, fence posts, the road forks to groves/sea | chickens, a hammer, a bullock cart | NEW |
| L12 | **Shore** | 9, 11 | late afternoon → dusk | nets on poles like cobwebs, **MARJAN** anchored far then near, a gangplank | surf, gulls | NEW |
| L13 | **Coconut grove** | 10A | gold, shafts of light | leaning palms, one branch with twelve coconuts | thuds | NEW |
| L14 | **Sea shallows** | 10B | glare | waist-deep water, spear, leaping fish | splash | NEW |
| L15 | **Arecanut grove — THE X SPOT** | 10C | gold | two tall, thin arecanut palms side by side that bend and cross in an **X** | creak of bending trunks | NEW (set-piece) |
| L16 | **Coir beach** | 10D | gold | rows of men pounding husks, piles of fibre | rhythmic pounding (no instruments) | NEW |
| L17 | **Market alley** | 10E | midday | fish baskets, wooden tables, cattle, hawkers | shouts, chase | NEW |
| L18 | **MARJAN deck + cabin** | 11, 12, 14, 14A, 15, 20 | dawn; day; night | huge square sail, painted bow eyes, **coconut mountains** (count in `04`), rope coils, chalk pitch, a cabin with a hand-painted route map and a swinging lantern | wind, rigging, wood creak | NEW |
| L19 | **Pathemari at sea** | 9 | night, lantern | slim lateen-sailed boat, a swinging lantern, Zidhan writing the cable | water, rope | NEW |
| L20 | **Madras post office (telegram counter)** | 13 | dawn | red brick, brass counters, **telegraph key, strip machine, form boxes**, a **shrine shelf with a brass lamp**, ledgers, ceiling fans, a queue | fans, stamps, a tapping key, fire | NEW |
| L21 | **Madras bazaar and harbour** | 14 | morning | rubber-seed stall, paper stall, a sock barrow, the MARJAN | crowd | NEW |
| L22 | **Open sea** | 15 | all day, night | endless water, deck pile of coconuts shrinking | waves, wind | NEW |
| L23 | **Rio harbour** | 16 | misty dawn | Sugarloaf, the Christ statue above clouds, iron liners | foghorns, gulls | NEW |
| L24 | **FIFA office** | 16 | day | long table, **thirteen little flags**, ashtrays, a tray marked "Pending" | murmurs | NEW |
| L25 | **Stadium tunnel and pitch (anthem)** | 16, 17 | overcast | a band that has no music for India | the sung anthem | NEW |
| L26 | **Maracanã** | 17–19, 21–23 | day; **hours of rain for Uruguay** | gallery, rail, **mud pitch that looks exactly like the Kerala paddy**, white lines vanishing | 190,000-voice roar (claps only) | NEW (BIG) |
| L27 | **Dressing room** | 18 | day | benches, bruises, Zidhan checks them | — | NEW |
| L28 | **Rio quay + night deck (quarrel)** | 20 | night, one lantern | the MARJAN moored, rail, Rio lights | water, a ship's horn far off | NEW |

**Set-piece reuse:** L15's X is reused in the match shots (Scenes 17, 19, 22) and on the mast (Scene 15).
**Camera continuity:** L08 and L10 and L26 must visually rhyme: **same gallery proportions, same mud**, so the Maracanã reads as the Kerala ground grown huge.


<!-- ===== FILE: 04_PROPS_COSTUMES.md ===== -->

# 04 — PROPS AND COSTUMES (continuity-critical)

## 1. THE WATCH (hero prop)
- **Design (lock once):** a vintage round wristwatch, gold-toned case, cream dial, thin worn brown leather strap, a small scratch on the glass. It must read identically in every shot. In 1950 it keeps a **faint gold glint** (colour survivor).
- **Chain of custody:** Sc. 1 on Grandpa's left wrist → Sc. 4 Grandpa slides it across the table with two fingers; Jaisal buckles it on → Sc. 6 Jaisal adjusts the dial and whispers "Let's change the history" → Sc. 11 Jaisal fastens it on the 5-year-old Abu Bakar (it hangs like a bracelet; the boy holds it to his ear) → Sc. 23 it appears **in Jaisal's closed fist** as the 360° spin ends (**salt crust on the strap**) → Sc. 25 Jaisal buckles it on Grandpa; a **grain of wet sand** drops from the buckle.
- **Sound:** a clear tick; louder in Sc. 1, 7, 23.
- **Rule:** the watch is a tool of remembering, **not** a time machine.

## 2. THE T-SHIRTS (the colour survivors)
| Prop | Spec | Asset |
|---|---|---|
| `TEE_JAISAL` | **teal** cotton tee with a large printed **hibiscus** in a glossy 3D-graphic style | `TEE_JAISAL_HIBISCUS` = `[USER-SUPPLIED]` |
| `TEE_ZIDHAN` | **mustard** cotton tee with the **Winning Eleven logo** (an open hand in a ring) | `TEE_ZIDHAN_LOGO` = `[USER-SUPPLIED]` |
- **Drain schedule (1950):** Sc. 8 full colour (faded) → Sc. 12 slightly muted → Sc. 15 each day greyer → Sc. 20 mostly grey → Sc. 23 fully grey; colour returns with the 360° spin.
- Do **not** put legible text on shirts; the logo is a shape only.

## 3. KITS
**Winning Eleven (2026):** mismatched faded jerseys, no black, no numbers; per-kid kit in `01`. Hand-painted bedsheet banner with the logo.
**Rockstar Boys:** matching black jerseys with printed silver stars; speaker on a stool.
**India (1950):** turmeric/indigo sailcloth shirts, hand-stitched numbers, tiny tricolour patch, mismatched socks, some barefoot, some rope-tied borrowed boots (see `02`).
**Opposition (1950, generic, no real likenesses):** Sweden yellow · Italy dark blue · Brazil white · Spain red · Uruguay sky blue · Paraguay (check references).

## 4. PROPS LIST
| ID | Prop | Detail / state | Scenes |
|---|---|---|---|
| PR01 | Football under the cot | old, dusty, name in marker | 1A |
| PR02 | Mint tea | steel kettle, glass, fresh mint leaves | 1 |
| PR03 | Firecracker / cracker trap | the crack that starts Sc. 1→2; the trap that killed the boar | 1, 4 |
| PR04 | Dead bandicoot rat | centre circle, then buried | 2, 3 |
| PR05 | Activa | dented, mud on the tyres | 2, 3 |
| PR06 | Kaikkott | worn wooden handle | 2, 3 |
| PR07 | **Notepad + pen** | Zidhan's; "SPRAY: 0", injury log, drills; the pen goes to Jaisal in Sc. 7 | 2, 3, 7, 7A |
| PR08 | Whistle on a string | Zidhan | 2, 6 |
| PR09 | **Empty spray can + cap** | sputters; Zidhan pockets the cap | 3 |
| PR10 | Wild boar, grave pit, shovel | dead boar; the pit made deeper | 4 |
| PR11 | Washbasin + towel | muddy hands/feet | 4 |
| PR12 | Phone | WhatsApp: "all set! He's waiting for u!" | 5 |
| PR13 | Coconut (road) | rolls down the path; Rayyan kicks it in sandals | 5A |
| PR14 | Matchbox-label ticket | ₹10 | 6 |
| PR15 | **Wooden scoreboard** | hand-painted sliding numbers; **WINNING ELEVEN 3 — ROCKSTAR BOYS 1** at the end | 6, 23 |
| PR16 | Yellow card, whistle | referee | 6 |
| PR17 | Bamboo-and-bedsheet banners | "THE FINAL — 6 PM" and the team banner | 6 |
| PR18 | Folded position list | GOALKEEPER, DEFENDERS, MIDFIELDER, WINGERS, STRIKER; crossed off with Zidhan's pen | 10 |
| PR19 | Coconuts, stones, husks | grove, throw, kick | 10A, 10D, 12 |
| PR20 | Spear, fish | Antappan | 10B |
| PR21 | Fish basket + mackerel | Jaisal carries it, Sc. 10E; Raghavan still holds it at the ship | 10E, 11 |
| PR22 | Tea glasses, tea-cloth, card deck | Bappu, Thomas (on the pitch parallels) | 17 |
| PR23 | Sulaiman's coin pouch | Zidhan uses it at the bazaar | 9, 14 |
| PR24 | Hand-drawn telegraph forms (x2) | the Federation's: **INDIA WILL NOT PARTICIPATE**; Zidhan's: **INDIA WILL PARTICIPATE**, boxes drawn by Muallim | 9, 13 |
| PR25 | Brass lamp, ledgers, wet sacking | the lamp tips and the fire starts | 13 |
| PR26 | Rubber seeds, paper, 15 pairs of striped socks | Zidhan's bazaar haul | 14, 15 |
| PR27 | Chalk, route map, lantern | on deck and in the cabin | 14A, 15 |
| PR28 | Sailcloth ball, soaked in seawater | wet-leather feel | 15 |
| PR29 | **Coconut stock on deck** | see §5 | 12, 15 |
| PR30 | Thirteen small flags, "Pending" tray | FIFA office | 16 |
| PR31 | Uruguay time-wasting prop | none; the captain's raised hand | 22 |
| PR32 | Plastic chair (gallery) | red; Jaisal sits at the end of the spin | 23 |
| PR33 | Grandpa's chair and window | | 1, 4, 25 |

## 5. COCONUT STOCK (continuity count on MARJAN)
| Moment | Quantity (visual) |
|---|---|
| Sc. 12 casting off | **mountains** against the mast: nets, baskets, sacks (~300) |
| Sc. 15 early days | still a big heap (~200), one more lost with every wild kick |
| Sc. 15 mid voyage | a low pile (~80) |
| Sc. 15 day 40 | **a handful** in one net (~12) |
Each kick that goes overboard: the coconut **floats away astern and is never fetched**.

## 6. COSTUME STATES (mud / wet / dirt)
- **Clean:** all of Part 1 before the match (except Jaisal after the grave).
- **Splashed:** Winning Eleven kids at the Sc. 6 fight.
- **Soaked mud:** the 1950 India team in the Uruguay match (Sc. 22) and Jaisal/Zidhan at the handshake (Sc. 23).
- **Salt:** Zidhan after the sea (Sc. 13); the watch strap in Sc. 23.


<!-- ===== FILE: 05_SOUND_AND_DIALOGUE.md ===== -->

# 05 — SOUND AND DIALOGUE

## A. SOUND POLICY (non-musical, instrument-free film)
- **No score, no needle-drop, no instruments of any kind** (no drums, strings, pads, stingers, risers).
- **Allowed:** the human voice (the **Azan** at the opening, the **sung anthem**, **humming**, calls, chants), plus natural and diegetic sound: wind, surf, gulls, rain, oars, rigging, wood, rope, bare feet, coconut thuds, husks pounded rhythmically, tea poured, ledgers falling, fire, a telegraph key tapping, a ship's horn, a crowd's clapping and roar, a loudspeaker voice.
- **Humming policy:** voice-only and **diegetic** (someone doing a task: coir workers, a mother hanging washing, a sailor on watch). It is never a score and never underlies emotion in a cue. Keep it sparse. Use it only if you are comfortable with it; a stricter choice is to keep the sung anthem and no humming at all.
- **Rhythm without instruments:** the husk pounding (Sc. 10D), the oars, the coconut bounces, and **crowd claps** carry rhythm. Do not add drum samples. Describe the Brazilian "samba" as **claps and feet** only.
- **Silence is a tool:** Sc. 7 (one watch tick), Sc. 16 (the anthem, a hushed stadium), Sc. 22 (the whistle).
- **Azan:** use your own recording or a licence-free recitation; it is voice only.

## B. SOUND PER SCENE (short)
| Sc | Sound |
|---|---|
| 1 | Azan, steam, kettle, loud watch tick, a firecracker CRACK |
| 2–3 | handheld field, Activa engine, whistle, spray *pssst, psss* |
| 4 | scraping shovel, dogs, a murmured "Naayle...", the slide of the watch |
| 5–5A | WhatsApp ping, crows, a coconut bang against a wall |
| 6 | crowd murmur, speaker, whistle, the fight thinning to a single tick |
| 7 | **silence + one tick**, wind in fronds |
| 8–9 | chickens, a hammer, a bullock cart, surf, gulls |
| 10 | stone and coconut thuds, spear, husk pounding, chase footsteps |
| 11–12 | gangplank, the sail unfurling like a wing, a coconut splash |
| 13 | fans, stamps, key tapping, the whoosh of fire, a fire-cart bell |
| 14–15 | bazaar crowd, rope, laps on wet planks, chalk, sea |
| 16 | foghorns, the **sung anthem** (no instruments), a flag snapping |
| 17–19 | the crowd's claps and roar, the watch tick in the magic sequence |
| 20 | water on the hull, a far ship's horn, the quarrel |
| 21–22 | rain, mud, whistle, a hushed stadium |
| 23 | the tick grows → a village crowd shouting in Malayalam → a loudspeaker commentator |
| 25 | the fan, the watch tick |

## C. LANGUAGE AND VOICE PIPELINE
1. **Generate in English (MiniMax).** Keep **one voice per character** (use MiniMax's consistent-voice workflow). Record the voice ID in the table in §E.
2. **Dub into Malayalam later** with lip-sync correction. Candidate: **LongCat-Video-Avatar 1.6** (I could not verify it; test on one clip first). Voices: **different voice actors** or a voice clone / OmniChar, never a clone of the English voice.
3. **Write for dubbing:** keep English lines short and plain; Malayalam usually runs longer, so give each dialogue shot **20–30% extra duration**; keep mouths visible (medium or close-up, not backs or deep profile) on every spoken line; avoid fast cuts during a line.
4. **Keep the script's Malayalam words in both tracks:** *Naayle, Kaal keduvaratthanda, Oraalayi, Randaalayi, Vaappaa, Nokkaam, Umma, Illa*, and Shafiq's wife's line *"Aarelum kayyo kaalo odichu ennum paranjond ingott vannaal athre ullu"*.
5. **Subtitle track:** English subtitles on the Malayalam version; Spanish (Uruguay captain) subtitled in both.
6. **Commentator (Sc. 23):** voice only, English in the first cut; Malayalam original kept for the dub: *"2026 il modern tactics ange attam etthi nilkunna velayilum chila gameukal jayikka tactics maathram pora kurach protiens venam, tholod thol cherth maatturach kaarirumbinte karutthum, kaalappoottinte kuthippum kond athaa winning eleven boys cup adichirikkuka aan."*

## D. LIP-SYNC SHOT RULES
- Dialogue in **medium close-up or close-up**, camera still or slow.
- One speaker per shot where possible; two-shots only when both are visible and the second speaks after a clean cut.
- No dialogue over water spray or hands covering the mouth.
- Keep the **1950 selection scenes** (Sc. 10) as short exchanges, each under ~8 seconds of speech.

## E. SPEAKING CHARACTERS (assign one voice ID each)
| Character | Speaks in | Voice ID | Notes |
|---|---|---|---|
| Jaisal | 1, 4–8, 10, 11, 14, 15, 17, 19, 20, 22, 23, 25 | `[ASSIGN]` | soft → intense → quiet |
| Zidhan | 2, 3, 4, 6, 7, 9, 13, 14, 15, 20, 23 | `[ASSIGN]` | dry, patient |
| Grandpa | 4, 25 | `[ASSIGN]` | slow, clear |
| Akhil, the Father | 2, 3 | `[ASSIGN]` | |
| Shafiq's wife | 5, 5A | `[ASSIGN]` | skeptical |
| Rayyan | 5 | `[ASSIGN]` | boy, excited |
| Referee | 6 | `[ASSIGN]` | one word |
| Gopalan, Antappan, Moosa, Pakru, Raghavan | 10, 15 | `[ASSIGN]` | one voice each |
| Thomas, Bappu | 15 | `[ASSIGN]` | |
| Sulaiman, Little Abu Bakar | 9, 11 | `[ASSIGN]` | the boy's voice should rhyme with Grandpa's |
| Muallim | 9 | `[ASSIGN]` | |
| Madras Postmaster | 13 | `[ASSIGN]` | |
| FIFA official, journalist | 16 | `[ASSIGN]` | |
| Uruguay captain | 22 | `[ASSIGN]` | Spanish, subtitled |
| Commentator | 23 | `[ASSIGN]` | cracking with emotion |


<!-- ===== FILE: 09_CINEMATIC_STYLE_AND_LOCATIONS.md ===== -->

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


<!-- ===== FILE: 11_MAJOR_LOCATION_PLATES_RICH.md ===== -->

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


---
## HARD RULES (repeat)
1. **No music, no instruments, no score.** Natural sound and voices only.
2. **Every woman fully covered; no hair visible.** 2026 hijab over head, neck and chest; 1950 head cloth, long sleeves; only face and hands visible.
3. **Every face distinct:** no two characters in a group share more than 2 of 8 features (head, hair, brows, eyes, nose, lips, jaw, ears).
4. **Skin tones:** the 12 Winning Eleven kids are 6 fair, 4 wheatish, 2 tanned; fair means warm wheat undertone, not pale, not pink.
5. **1950 = colour sheets, B&W in post;** only the two tees, fire and the watch keep colour.
6. **Every image has a story job and a must-see object** (section 12).
7. **Text in shots is generated blank and added in post.**
8. **[USER-SUPPLIED]** = leave blank: hibiscus tee, Winning Eleven logo, voice IDs, Sudani references R1-R8.
