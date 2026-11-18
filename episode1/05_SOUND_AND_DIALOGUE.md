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
