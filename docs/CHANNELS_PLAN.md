# CHANNELS PLAN — 4 channels, daily from 2026-11-25 (user 2026-11-19, "thinking big")

## The four channels (user's words, mapped)

| # | Channel | Purpose (user) | Language | Cadence | Pipeline |
|---|---|---|---|---|---|
| 1 | **learnhadithAndQuranDaily** (handle spelling TBD — "Dialy"? ) | "for becoming better muslim" | **EN + ML** (separate pages) | Daily from **2026-11-25** | Islamic line-art (Ubu-style) + recitation/narration |
| 2 | **pradhaana_prashnam** ("main issue") | revenue | ML | weekly/daily (news-driven) | punchline-first issue explainers, news-scraper automated |
| 3 | **Football Talkies** | revenue | EN (ML later?) | per major match | tactical-lite animation + XG/shot data |
| 4 | **Jaisal Cut** | "where as artist i perform" | — | — | user's own art (Krea2/ComfyUI character lane already exists) |

## Channel 1 — learnhadithAndQuranDaily

**Style reference (attached 2026-11-19, `data\quran_ref\`):** Surah At-Takwir recitation video, 720×1280, 103.8 s:
per verse = cinematic background matching the imagery (sun setting, stars darkening,
volcanic sea, fire, buried-alive mound) + Arabic calligraphy verse + English
translation + surah/verse header; audio = recitation (Arabic, ~3.4 s/verse).
Beat map: `data\quran_ref\BEAT_BREAKDOWN.md`.

**Pipeline:**
- Audio: recitation WAV per verse (user supplies / reciter — Quran is recited by a
  human, NEVER TTS; narration/explanation can be TTS via Voice Studio).
- Text: Arabic (calligraphy font — **NOT on this machine yet; no Amiri/Sakkal in
  C:\Windows\Fonts, D228 offline until 11-24** — user drops `fonts\amiri\` or we
  download after 11-24. PIL shaping: Windows wheels carry libraqm — verify first
  render). Malayalam = `Nirmala.ttc` (verified rendering ✓).
- Backgrounds: per-verse stills/clips (user supplies, or MiniMax hybrid after 11-24,
  D041 no-music always).
- Compose: Template B engine (1080×1920 @60, v8, 7 palettes), 40 s cuts (D241).
- Ubu al-Amal = first Channel-1 piece (done, palette C).
**Platforms:** Instagram + YouTube + Facebook + X, EN page + ML page = **8 accounts**,
fresh Gmail (USER action — agent cannot create the account). Handle spelling to
confirm: `learnhadithAndQuranDialy` vs `…Daily`.

## Channel 2 — pradhaana_prashnam

**Format (user):** punchline FIRST — "pradhaana prashnam" (the main issue) as the
cold open in one line → then explain the issue/idea. Topics: issue, society,
politics, ideas.
**Pipeline:**
- Source: **our RAG daily news** (`rag\daily.py` already fetches news every day) →
  weekly-top or daily issue pick.
- Script: one-line punchline + 3-4 supporting beats (40 s).
- Narration: Voice Studio (D239) or clone — ML.
- Animation: Template B line-art (issue visual metaphor) or user graphics.
- SFX: light (D041 no music).
- Automation level: news pick is automatable; script approval = user (it's opinion
  content — user's voice/face, not agent's).
**Open:** first topic, script approval loop.

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
Template B animation (pitch diagram + stat callouts — line-art fits tactical
explainers well) → 40–60 s short.
**Open:** first match, EN vs ML.

## Channel 4 — Jaisal Cut

User's own art channel — no pipeline needed from the agent beyond the existing
Krea2/ComfyUI character work (D137 char1/char2, face refs, identity-edit v1.2).

## Shared standards (all channels)

- 1080×1920 @60 · Template B v8 engine · 7 palettes rotate by weekday (D244)
- 40 s → 2×20 s WhatsApp + 40 s Instagram (D241)
- D041 HARD: no music, ever (natural sounds only)
- Fonts: caption=constani, labels=arialbd, close=BASKVILL, handle=arial (D237);
  Malayalam=Nirmala.ttc; Arabic=pending (font + libraqm verify)
- Narration = Voice Studio (D239); SFX = synthesized (D236)
- Distribution cuts + ffprobe verify in every build script (D240 pattern)

## Open questions (user)

1. Handle spelling: `learnhadithAndQuranDialy` or `learnhadithAndQuranDaily`?
2. Channel 2 name on platforms: `pradhaana_prashnam` exactly?
3. Football language: EN first?
4. First daily content (25th): Ubu in C (ready) — then what? (Takwir-style verse
   video? need recitation + backgrounds)
5. Gmail: user creates the account(s) — then agent preps bio/profile copy per
   platform (EN + ML).
