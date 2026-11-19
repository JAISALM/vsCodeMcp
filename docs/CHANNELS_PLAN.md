# CHANNELS PLAN — 4 channels, daily from 2026-11-25 (user 2026-11-19, "thinking big")

## The four channels (user's words, mapped)

| # | Channel | Purpose (user) | Language | Cadence | Pipeline |
|---|---|---|---|---|---|
| 1 | **learnhadithAndQuranDaily** (handle = **Daily** — user-confirmed 2026-11-19: "daily only, dialy is different meaning") | "for becoming better muslim" | **EN + ML** (separate pages) | Daily from **2026-11-25** | Islamic explainers (Ubu-style, D250) + narration |
| 2 | **pradhaana_prashnam** ("main issue") | revenue | **ML (final, D254)** | weekly/daily (news-driven) | punchline-first issue explainers; **Kerala/Malayalam-specific news** source; social issues + simple-yet-effective humor |
| 3 | **Football Talkies** | revenue | **EN (final, D254 — "football must be in english, not in malayalam")** | per major match | tactical-lite animation + XG/shot data |
| 4 | **Jaisal Cut** | "where as artist i perform" | — | — | user's own art (Krea2/ComfyUI character lane already exists) |

## Channel 1 — learnhadithAndQuranDaily

**FORMAT PIVOT (user 2026-11-19: copyright on recitation recordings):**
- **NO recitation audio** — a reciter's recording is a copyrighted performance
  (the Quran/hadith TEXT is fine; the audio is not). Channel 1 **explains**
  hadith & Quran via NARRATION (Voice Studio), never recitation.
- **Daily 40 s** videos, each covering **important details with respect to
  CURRENT AFFAIRS & SCENARIOS** (today's news/event → the hadith/verse that
  speaks to it).
- **ALWAYS carries a WARNING** — because it is the word of God: reverence +
  cite the source + "always verify from the original".

**Daily format spec (40 s):**
| t | Beat |
|---|---|
| 0–5 s | TODAY'S SCENARIO — current affairs / everyday situation, one line (hook) |
| 5–13 s | THE WORD — hadith text / Quran verse + source card (e.g. SAHIH AL-BUKHARI 1) |
| 13–32 s | THE EXPLANATION — meaning, lesson, how it applies to the scenario |
| 32–40 s | THE WARNING — "this is the word of God — verify from the original" + @handle |

**Sources:** the RAG daily news store feeds the scenario beat (same store as
Channel 2 — one news fetch, two lenses: Islamic perspective / issue perspective).
Ubu al-Amal = launch piece (done, palette C — not scenario-tied, acceptable as
day 1). Takvir reference (`data\quran_ref\`, beat map saved) = LAYOUT reference
only (header + text stack + clean background) — its recitation audio is OUT.

**Pipeline:**
- Audio: narration WAVs per beat (Voice Studio, EN + ML versions — D239).
- Text: Arabic verse text shown as TEXT (calligraphy font — **NOT on machine
  yet; no Amiri/Sakkal in C:\Windows\Fonts, D228 until 11-24** — user drops
  `fonts\amiri\` or we fetch after 11-24; verify libraqm shaping first).
  Malayalam = `Nirmala.ttc` ✓.
- Visuals: Template B line-art scenes for the scenario beat (our style); the
  warning beat = text card + source.
- Compose: Template B engine (1080×1920 @60, v8, 7 palettes), 40 s + 2×20 s
  cuts (D241).
**Platforms:** Instagram + YouTube + Facebook + X, EN page + ML page = **8 accounts**,
fresh Gmail (USER action — agent cannot create the account). **Handle =
`learnhadithAndQuranDaily`** (user-confirmed 2026-11-19 — "dialy" is a different
word).

## Channel 2 — pradhaana_prashnam

**Format (user):** punchline FIRST — "pradhaana prashnam" (the main issue) as the
cold open in one line → then explain the issue/idea. Topics: issue, society,
politics, ideas.
**THE FORMULA (user, D257):** a **simple solution** to a problem people might
consider — **that is not that easy in practice**. The punchline IS the gap:
`[problem people think about] + [assumed simple solution] + [why practice makes
it hard]`. Domains: **corruption, study, culture, etc.** — evergreen problems,
news is OPTIONAL seasoning (the hot layer from D256 adds the "people are already
talking" spice when it fits).
**Language: MALAYALAM (final, D254).** **Tone (user, D254):** interesting Kerala
news + social issues + **simple yet effective humor**. **First script = user
structures it, then we pick it up** (compose/narrate/cut — OPEN_ITEMS 2.2).

**Pipeline:**
- Source: **Kerala/Malayalam-specific news, pulled DAILY** (D254 — the current RAG
  store is general news; a Malayalam source must be ADDED to the daily job —
  OPEN_ITEMS 2.1; web scraping allowed even during D228).
- Script: one-line punchline + 3-4 supporting beats (40 s).
- Narration: Voice Studio (D239) or clone — ML.
- Animation: Layer 1 (Template B punchline cards + visual metaphor — D253).
- SFX: light (D041 no music).
- Automation level: news pick is automatable; script approval = user (it's opinion
  content — user's voice/face, not agent's).
**Open:** Malayalam news source (2.1) · first script (2.2) · platform name spelling (2.3).

## Channel 3 — Football Talkies

**Scope (user):** shorts-first (longer later). Pick a major match (Madrid/Barça/
CL) → best player + fan-fave + goal scorer → explain contribution with SIMPLE
tactical terms + engaging narratives ("why Arda Güler is the modern No.10",
"why Mbappé is not a traditional 9", "why Vini is not a regular winger",
"why Pedri is essential", "Yamal is a new Messi generation"). Reference channel:
"Football Made Simple" (YouTube) — animated tactical explainers, shallow.
**Data (user: "do we have any such data?") — YES, public sources:**
- **XG + shot locations** (simple heatmaps): `understat.com` (top-5 leagues,
  last ~3 seasons, JSON endpoints) + `fbref.com` (XG, shot maps per match).
- Player stats/ratings: FotMob/Who-style pages (scrape).
- **Full tracking heatmaps = paid (Opta) — skip** ("we dont need to go in depth").
- Scraping is web (allowed — RAG runs daily); only MODEL downloads are blocked
  until 11-24 (D228).
**Pipeline:** match pick → data fetch (XG/shot map) → 3-player narrative script →
Layer-1 animation (PIL tactics board from the data + stat callouts — D253) →
40–60 s short. **Language: ENGLISH (final, D254 — "football must be in english,
not in malayalam").**
**Open:** first match (OPEN_ITEMS 3.1) → data fetch (3.2) → PIL board renderer (3.3).

## Channel 4 — Jaisal Cut

User's own art channel — no pipeline needed from the agent beyond the existing
Krea2/ComfyUI character work (D137 char1/char2, face refs, identity-edit v1.2).

**POSITIONING (D258, 11-19):** Jaisal Cut = **CINEMA channel** — aim = better
growth, art + **film festival if needed** → **slow-burn, its own timeline**
("lets give some time for that") — **NOT in the December 3-channel target**
(D258). No daily/weekly cadence pressure; production + festival cycle.

## ANIMATION STRATEGY — two layers, NOT "ComfyUI only" (2026-11-19, user asked "hwo we are going to animate? using comfyui only right?")

**Layer 1 — the workhorse: Template B + procedural 2D (PIL, no GPU, seconds per
video). This is what every daily/weekly video is made of.**
- **Channel 1:** text cards + line-art (existing Ubu system) — done.
- **Channel 2 (pradhana):** punchline-first text cards + a visual metaphor per
  issue (Template B line-art or user graphics). Same engine, new palette
  treatment. Fast enough for daily.
- **Channel 3 (football):** **data-driven tactics board, auto-drawn in PIL** —
  pitch (green rect + lines + boxes), player dots, movement arrows, shot
  markers + XG callouts — generated FROM the understat/fbref JSON. This IS the
  "Football Made Simple" aesthetic: clean flat 2D diagrams, NOT cinematic.
  No GPU, no user per-beat art — the board is code from data.
- Narration on both = Voice Studio / clone (D239); SFX synthesized (D041).

**Layer 2 — the spice: ComfyUI (GPU, user queues — D192). HERO SHOTS ONLY.**
- Krea2 ref → MiniMax H3 R2V (the film pipeline) for 1–2 cinematic beats per
  video max: a player-story moment (Güler close-up), a goal moment, an issue's
  hero visual when a text card can't carry it.
- Why not ComfyUI-only: minutes per shot + shared GPU (D192 queue discipline) +
  daily content doesn't need cinema. ComfyUI is the accent, Template B +
  data-2D is the meal.

## Shared standards (all channels)

- 1080×1920 @60 · Template B v8 engine · 7 palettes rotate by weekday (D244)
- 40 s → 2×20 s WhatsApp + 40 s Instagram (D241)
- D041 HARD: no music, ever (natural sounds only)
- Fonts: caption=constani, labels=arialbd, close=BASKVILL, handle=arial (D237);
  Malayalam=Nirmala.ttc; Arabic=pending (font + libraqm verify)
- Narration = Voice Studio (D239); SFX = synthesized (D236)
- Distribution cuts + ffprobe verify in every build script (D240 pattern)

## Open items → single sheet

**`docs/OPEN_ITEMS.md`** (D254) is the ONE open-items sheet — per channel, with
owners. Resolved-so-far: ① handle = `learnhadithAndQuranDaily` (2026-11-19) ②
football language = **EN** (D254) ③ pradhana language = **ML** (D254).
Remaining: pradhana platform-name spelling · first football match · day-2 topic ·
Gmail (author) → 8-account bios (agent) · Malayalam news source (agent) ·
eng-degree script text + beat graphics (author).
