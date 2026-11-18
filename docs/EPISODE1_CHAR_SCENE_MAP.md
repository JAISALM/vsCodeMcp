# EPISODE 1 — CHARACTER + SCENE → ASSET MAP (2026-11-18, agent-prepared; updated to v3 FINAL)

Source: **`episode1\episode1_full_script_FINAL_v3.md` — USER-CONFIRMED FINAL (2026-11-18, "i have made few changes, that will be our final one")** (817-line class, v3 07:13 IST; supersedes v2 + v1). Prepared for the workflow-prep gate (D227).

## Script overview (for the asset pipeline)

- **Two timelines:** 2026 Kerala village — the final (Jaisal in the gallery, Zidhan on the
  touchline) + a 1950 mind-trip (B&W, golden-hour bloom; the village's 1950 selves sail on
  the Beypore *uru* **MARJAN** to Brazil for the 1950 World Cup; Maracanã mud; 360° spin
  return in Scene 23).
- **Magical-realism rules (visual):** colour survives in only three things in 1950 — the two
  graphic T-shirts (they DRAIN slowly over the voyage), fire (gold), the watch (faint gold
  glint). Anachronism rule: Jaisal/Zidhan keep modern words; villagers translate them.
- **Faces echo:** the 1950 players are played by the same faces as the 2026 kids (Anto→
  Antappan, Gopu→Gopalan, Pachu→Pakru, Babu→Bappu, Ragu→Raghavan, Velu→Velayudhan,
  Kutti→Kuttappan, Karu→Karunan, Chandru→Chandu, Musthu→Moosa, Tomy→Thomas).
- **SOUND BIBLE = D041-COMPLIANT already:** "no score, no needle-drop. Only what exists in
  the world: the Azan, the watch tick, wind, surf, oars, rigging, bare feet, coconut thuds,
  crowd claps, voices. The anthem is sung, never played." → every R2V
  `non_diegetic_music` block = the standard no-music statement; `overall_soundscape` =
  these natural sounds only.
- **Key prop:** Grandpa's watch (glint, tick, the tool of remembering — Scene 1, 4, 25, 30).

## Character table → asset routes

### 2026 leads (LoRA-locked)
| Character | Age | Look (script) | Props | Asset route |
|---|---|---|---|---|
| **Jaisal** | 28–29 | left the academy after the semi-final; blames "the system" | Grandpa's watch (from Scene 4), muddy hands/feet, the graphic T-shirt that drains in 1950 | `krea2jaisal_v3` ✓ (D137 look: wavy black hair, slim, plain black tee) |
| **Zidhan** | ~28 | the coach who stayed; always carries a **notepad + pen** ("SPRAY: 0", injury log) | notepad & pen, whistle on a string, drenched shirt in 1950 | `krea2zidhan_v3` ✓ (D137 look: top bun, white tee, **beard in every shot**) |

### 2026 supporting adults
| Character | Age | Script role | Asset route |
|---|---|---|---|
| **Akhil** | 18–20 | rides an **Activa**, carries a *kaikkott* (shovel), groundsman / first-aid man (Scene 3) | **char3 slot = `krea2jaisal_v2`** (young-man fit is approximate — confirm look with user; rename in prompts) |
| **The Father** | ~40s | rushes to a wedding in another district (Scene 3) | **char4 slot = `krea2zidhan_v2`** (middle-aged fit approximate — confirm with user) |
| **Shafiq's wife** | ~35 | skeptical mother; hanging washing (Scenes 5, 5A) | **NEW — no female LoRA**: t2i concept sheet (Kerala housewife, 3 angles) → pick → identity-edit v1.2 (ref_boost 4.0) for scene stills. Small role (2 scenes). |
| **Shafiq** | — | Gulf, WhatsApp only — OFF-SCREEN (phone screen in Scene 5) | none (phone UI only) |
| **Grandpa Abu Bakar** | ~81 | sits in "stillness", dreams of his father's ship, calls Jaisal "Jaisalu", the watch (Scenes 1, 4, 25, 30) | **char5 = identity-edit FIRST** (D227 confirmed by script — he is CORE). 1 clean reference (user photo of an 80s Malayali grandpa, or t2i concept) → identity-edit v1.2. **Watch = set-piece prop, must be consistent (glint/tick).** |

### 2026 kids (11–12) — 12 characters (team name: **the Winning Eleven**, v3 — named after the
football-game series, "with a wink at the eleven men of 1950"; a **bedsheet banner hand-painted
WINNING ELEVEN** hangs from two bamboo poles behind their bench, Scene 6)
**Adam** (tall, Shafiq's son — **CONFIRMED v3: Shafiq is Jaisal's cousin, so Adam = Jaisal's
NEPHEW** — calls her Umma, newspaper shin guards, rubber sandals, the tactical foul — the most
important kid), **Anto** (GK), **Gopu** (captain), **Pachu** (stubborn), **Babu** (long
passer), **Ragu** (striker), **Velu**, **Kutti**, **Karu**, **Chandru**, **Musthu**, **Tomy**.

**Route (no kid LoRAs exist):** per-kid t2i concept (12 face sheets, 3 angles each via the
identity-edit chain from ONE chosen sheet per kid) → each kid's face locks the 1950 adult
echo too. **Batch plan:** 12 kids × Klein t2i (fast) → user picks 1 sheet/kid → 12
identity-locks. Adam first (most scenes + the echo with the 1950 "little Abu Bakar" beat is
actually the ABU BAKAR line, not Adam's — Adam stays 2026-only).

### 1950 players (same faces as the 2026 kids)
Antappan (GK, fisherman, salt-bleached brows), Chandu (RB, husk beater), Moosa (CB, market
manager, tilted cap), "Illa" Pakru (CB, heavy brows, folded arms), Velayudhan (LB, barrel
chest, gap tooth), Thomas (DM, 28-card player, ink thumb), Gopalan (CM, coconut calculator,
wire spectacles), Bappu (AM, tea master, tea-cloth on shoulder), Kuttappan (RW, arecanut
climber, rope loop at ankles), Karunan (LW, the X-cross climber), Raghavan "Kallan" (ST,
the thief, scar through left brow).

**Route:** each = identity-edit AGE-UP of the locked 2026 kid face ("same face, now a
weathered 1950 adult of the same village, 1950 clothes") + the per-player look above
(spectacles, cap, scar, tea-cloth…). B&W grade applied at the H3 R2V stage (1950 =
high-contrast B&W + golden-hour bloom + vignette).

### 1950 supporting
| Character | Role | Route |
|---|---|---|
| **Sulaiman** | great-grandfather, ship master, stays ashore (Scenes 10, 11) | identity-edit from t2i concept (another old Malayali man — distinct from Abu Bakar: bearded, ship-master's bearing) |
| **Little Abu Bakar (5)** | 5-year-old in a tiny mundu, "VAAPPAAAA!", gets the watch (Scene 11) | t2i concept (5yo Kerala boy) + identity-edit — the emotional core of the trip |
| **Muallim Moideen** | navigator | t2i concept + identity-edit (small role) |
| **Vaidyar Madhavan** | village healer, "third coach" (Scenes 7–9, 21) | identity-edit from concept (cloth bag) |
| **Madras Postmaster** | "Mistakes need Form 7B" (Scene 13) | concept + identity-edit (1 scene) |
| **Varela** (Uruguay captain) | "You play the way my grandchildren will" (Scene 22, subtitled) | concept + identity-edit (1 scene, Western 1950 look) |
| **Federation messenger** | drops the "INDIA WILL NOT PARTICIPATE" envelope (Scene 13) | background character (generic 1950 clerk) |

### The vessel
**MARJAN** — Beypore-style wooden *uru* (pathemari), painted eyes on the bow, huge square
sail, gangplank, mountains of coconuts on deck (Scenes 10–12, 14–16). **Key new asset** —
blockout: hull + square sail + bow eyes + deck coconut stacks.

## Scene table → blockout status

| Script scene | Title | Timeline | Blockout status |
|---|---|---|---|
| 1 + 1A | The Sacred Morning (kitchen, Grandpa's stillness, watch glint, mint tea) + the Room He Doesn't Look At (football under the bed) | 2026 | **S3 inside-house** = base ✓ (bed + table + doorway) → extend: Grandpa's room corner (chair + table + watch) + kitchen corner (mint-tea pot) |
| 2 + 2A | The Transition & The Muddy Field (kids playing, Zidhan on touchline, Activa arrival) + The Stone Drill | 2026 | **S1 paddy** = base ✓ (paddy + farmers) → adjust: touchline + 5–8 kids + Zidhan + Activa at edge |
| 3 | The Father's Anxiety & The First-Aid Fail | 2026 | **S6 village** = base ✓ → Father rushing out + Akhil with kaikkott |
| 4 | The Conversation of Dreams (**boar grave**, dead boar, watch slide beat) | 2026 | **S2 behind-house** = base ✓ + **boar-grave blockout (D106) = EXACTLY this scene** (2 angles enough) |
| 5 + 5A | The House of Shafiq (wife + Adam in mismatched kit) + The Header (coconut on the pathway) | 2026 | **S6 village** houses = base → one house front + pathway + coconut palm |
| 6 | The Tournament — First Half (gallery, ticket boy, "THE FINAL — 6 PM" banner, 5-a-side, Rockstar Boys, speaker, **v3: WINNING ELEVEN bedsheet banner behind the bench**) | 2026 | **S5 7's ground** = base ✓ → extend: plank-and-bamboo **gallery** + boundary rope + banners (THE FINAL — 6 PM title card + WINNING ELEVEN bedsheet) + ticket boy + **wooden scoreboard** (it carries the Scene 23 return: "WINNING ELEVEN 3 — ROCKSTAR BOYS 1") |
| 7–9 | (1950 selection — Life-IQ vignettes: fisherman/husk-beater/market manager/etc.; **v3: the arecanut climbers' X is now THE iconic parallel — two climbers crossing between bending palms in an X, shown again in the matches (Sc. 17, 19) and clipped by Uruguay (Sc. 22)**) | 1950 | **NEW blockout**: village ground at golden hour + Life-IQ vignette spots (coconut tree, husk floor, market) + **THE X SPOT: two arecanut trees crossing in an X** (the set-piece location for the 3 match-cuts) |
| 10–11 | Beypore shore (MARJAN at anchor, gangplank, team line, "VAAPPAAAA!") | 1950 | **NEW blockout**: shore + MARJAN + beach line |
| 12 | Casting Off — The Coconut Ball (dawn, sail unfurls, coconut mountains on deck) | 1950 | **NEW blockout**: ship deck + coconut stacks + square sail |
| 13 | The Madras Post Office (**v3: it is now a TELEGRAM counter** — Zidhan queues with his own telegraph form inside his shirt; the Federation's form goes to the **brass key**; close-up reads block capitals in a printed box: "INDIA WILL NOT PARTICIPATE"; the lamp oil arcs onto the FORM; the postmaster taps it out on the key — "Tap, tap, tap. Sent."; Rio: a **telegraph strip chatters out of a machine**. Fact-anchored: a telegram was the standard fast official international message in 1950.) | 1950 | **NEW blockout**: post-office interior — queue, **telegram counter + brass key + telegraph form boxes + strip machine**, counter 11 (closed until Thursday), outgoing area, brass lamp shrine over the counter |
| 14–16 | At sea (the voyage, T-shirt colour drain) | 1950 | **NEW blockout**: open sea + ship deck (reuse 12 + sea backdrop) |
| 17 | Brazil arrival (the port) | 1950 | **NEW blockout**: port + MARJAN at berth |
| 18–20 | Maracanã — Brazil vs Sweden, India vs Spain (pre-match, gallery; **v3: THE X runs again here — "the wingers cross in their X and split Brazil's fullbacks"**) | 1950 | **NEW blockout (BIG)**: Maracanã gallery + rail + mud pitch (the mud pitch = "exactly like the paddy field in Kerala" — the visual echo with S1) |
| 21 | India vs Spain — Hardening (Jaisal alone on touchline, Vaidyar, seed board) | 1950 | reuse 18–20 blockout (touchline angle) |
| 22 | India vs Uruguay — The Mud (**v3: the X is attempted and CLIPPED — "a boot clips Karunan mid-run"; + NEW Jaisal solo touchline monologue: "Tactics alone can't win this. No referee on our side. No VAR. You adapt. Strength, physicality, a little skill. The basics." DIRECTOR NOTE: the Uruguay match = the 2026 five-a-side final in disguise**) | 1950 | reuse 18–20 (mud angle) + Jaisal-alone touchline angle |
| 23 | **The Handshake, The 360° Spin & The Return** (v3: the return now CARRIES the payoff — colour floods back, **the watch in Jaisal's closed fist, ticking, glinting gold** (proving he's in the present), **wooden scoreboard "WINNING ELEVEN 3 — ROCKSTAR BOYS 1"**, kids' mud heap, the **commentator's loudspeaker line** (English + Malayalam original kept for dubbing), OPTIONAL single background frame: Akhil with the full first-aid spray) | 1950→2026 | **S5/S1 ground** (the 2026 muddy ground — the return lands on the match ground, NOT the Maracanã) — the 360° spin = R2V camera directive, not a blockout. **NEW SET-DRESS: the wooden scoreboard + WINNING ELEVEN bedsheet banner.** |
| ~~24~~ | ~~The 2026 Payoff~~ — **REMOVED in v3** ("the 360° return now carries the payoff"; no replay of the new game) | — | — |
| 25 | The Watch (v3: Grandpa's wrist BARE at the start — the watch came back in Jaisal's fist in Sc. 23; **Jaisal fastens it on the old man's wrist**; the strap carries a thin crust of sea-salt; a grain of wet sand drops from the buckle) | 2026 | **S3 inside-house** reuse (Grandpa's room corner). **WATCH = continuity-critical prop, full chain: table slide (Sc. 4) → boy Abu Bakar (Sc. 11) → Jaisal's fist w/ salt crust (Sc. 23) → Grandpa's wrist (Sc. 25).** |

**Blockout gap list (prioritized, v3):**
1. **Maracanã gallery + rail + mud pitch** (scenes 18–23 — the climax; highest blockout value)
2. **Shore + MARJAN** (10–11) + **deck with coconut stacks + square sail** (12)
3. **Madras post office interior — TELEGRAPH counter + brass key + form boxes + strip machine** (13, v3)
4. **S5 extension**: gallery + boundary rope + "THE FINAL — 6 PM" title-card banner + **WINNING ELEVEN bedsheet banner** (v3) + ticket boy + **wooden scoreboard** (it carries the Scene 23 return: "WINNING ELEVEN 3 — ROCKSTAR BOYS 1")
5. **S1 adjustment**: touchline + kids + Activa (existing blockout is a base; S1 = the match ground itself — the 2026 muddy ground the Scene 23 return lands on)
6. **Village ground at golden hour** (7–9 Life-IQ vignette spots) + **THE X SPOT: two arecanut trees crossing in an X** (the set-piece location for the 3 match-cuts, v3)
7. S3 extensions: Grandpa's room corner + kitchen corner
All 7 = the same graybox recipe (EXPERIMENTS 2026-11-17) — ~5–10 min each locally.

## Open items for the user (v3-confirmed status)

1. **char3/char4 fits:** `krea2jaisal_v2` → **Akhil**? `krea2zidhan_v2` → **The Father**? (the v2 looks are "older Jaisal"/"older Zidhan" — close-ish; if the script's Akhil/Father looks are very different, a t2i concept + identity-edit may beat the LoRA fit for those two)
2. **Grandpa Abu Bakar reference:** a real photo of an 80s Malayali grandpa you have in mind, or I t2i-generate the concept (stillness, thin, white beard, watch) and you pick?
3. ~~Adam's relation to Jaisal~~ — **RESOLVED v3: Adam = Jaisal's NEPHEW** (Shafiq = Jaisal's cousin; Adam = Shafiq's son). Scene 1 kitchen blocking = uncle/nephew framing.
4. **The P4 deadline (Nov 22) is re-scoped** — the script is a full episode (v3: 24 core scenes, Scene 24 removed; Part 2 CORE ≈ 21:55). Propose: **2026 scenes first** (1, 2, 3, 4, 5, 6, 23-return, 25 = our 6 blockouts + scoreboard set-dress, ~2 weeks), **1950 part second** (needs the 7 new blockouts + the B&W grade pipeline).
5. **12-kid face batch:** the script is now FINAL — OK to start the 12×3 t2i concept batch (Klein, fast, user queues 2–3 at a time)?
6. **New (v3):** the **commentator's line has its Malayalam original kept for dubbing** — it is a P1 dubbing target (record it with the dubs; the line is in the script).

## v2 → v3 change log (user's final pass, 2026-11-18 07:13 — diffed, all hunks processed)

1. **Scene 24 REMOVED** — "The 2026 Payoff" deleted; the Scene 23 360° return now carries the
   payoff (watch in Jaisal's fist, wooden scoreboard WINNING ELEVEN 3 — ROCKSTAR BOYS 1,
   kids' heap, commentator). No replay of the 2026 match. Part 2 CORE ≈ 21:55 (was 22:40).
2. **Letter → TELEGRAPH CABLE everywhere** — Sc. 9 (Muallim draws the telegraph-form boxes;
   Zidhan writes "INDIA WILL PARTICIPATE" into them), Sc. 13 (telegram counter, brass key,
   form, strip machine; dialogue "cable", "Tap tap tap. Sent."), Sc. 16 (FIFA: "a cable from
   Madras"), dialogue "How do I stop a cable?". Fact anchor added: telegram = standard fast
   official international message in 1950.
3. **THE X = iconic parallel** — the arecanut climbers' X (Sc. 7–9/10C) now runs as the
   wingers' match move in Sc. 17/19 ("cross in the middle, each making the run behind the
   other's marker") and is CLIPPED by Uruguay in Sc. 22 ("a boot clips Karunan mid-run").
4. **Scene 23 rewritten** — Jaisal's wrist BARE + the watch in his closed fist (ticking,
   glinting gold = "He is in the present"); "admiration in both directions"; the tick
   "grows until it fills the frame"; + the commentator's loudspeaker line (English) with the
   Malayalam original kept for dubbing; Akhil's full-spray = now an OPTIONAL background frame.
5. **Scene 25 adjusted** — Grandpa's wrist bare at the start; Jaisal fastens the (sea-salt
   crusted) watch on his wrist himself.
6. **Team name + banner** — Zidhan's kids = **the Winning Eleven** (a wink at the game series
   + the eleven men of 1950); bedsheet banner behind the bench (Sc. 6).
7. **Adam = Jaisal's nephew** — Shafiq is Jaisal's cousin (relation confirmed; the old
   "still to confirm" item is closed).
8. **Timing/dialogue** — Sc. 13 73 words (was 67), Sc. 16 77 (was 84), Sc. 22 36 (was 7,
   the new Jaisal monologue), Sc. 23 1:45/72 words (was 1:00/8).
