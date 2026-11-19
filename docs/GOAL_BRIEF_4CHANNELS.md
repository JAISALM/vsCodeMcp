# PROJECT GOAL — 4-Channel Video Content Engine (brief for external LLM consultation)

**Date:** 2026-11-19 · **Owner:** single content creator (Kerala, India; Muslim) ·
**Status:** production-ready engine exists; 1 video shipped; 3 pipelines designed;
daily publishing planned from **2026-11-25**.

This brief is self-contained: it contains all context an external LLM needs.

---

## 1. Who & what

A solo Muslim content creator wants a **daily short-video publishing operation**
across four channels, on Instagram, YouTube, Facebook, and X — in **English and
Malayalam** (Channel 1 has two language versions of everything; others start in
one language). He is both the creator and the only human operator; an AI agent
runs the entire production pipeline on his PC (Windows + RTX 5090 + ComfyUI +
local LLMs + a local TTS app).

His framing of the four channels (his own words):

> 1. Islamic daily learning — "for becoming better muslim"
> 2. pradhana prashnam (issue explainers) — "for revenue"
> 3. Football Talkies — "for revenue"
> 4. Jaisal Cut — "where as artist I perform"

---

## 2. The four channels

### Channel 1 — `learnhadithAndQuranDaily` (handle spelling pending: "Dialy"? "Daily"?)

- **Content:** daily Islamic learning — **EXPLAINER videos on hadith & Quran**
  (narration, in the creator's language). **NO recitation audio** — a reciter's
  recording is a copyrighted performance (the Quran/hadith text is fine; the
  audio is not).
- **Daily 40 s format (creator's spec):** each video covers important details
  **with respect to current affairs & scenarios** (today's event/situation →
  the hadith/verse that speaks to it), and **ALWAYS carries a warning** —
  because it is the word of God (reverence + source citation + "verify from
  the original").
- **Daily beat structure:** 0–5 s today's scenario (hook) · 5–13 s the word
  (text + source card, e.g. SAHIH AL-BUKHARI 1) · 13–32 s the explanation ·
  32–40 s the warning + handle.
- **Scenario source:** the project's daily news-RAG store (shared with
  Channel 2 — one news fetch, two lenses: Islamic perspective / issue lens).
- **Languages:** English + Malayalam (separate social pages per language; 4
  platforms × 2 languages = 8 accounts, all on a fresh Gmail — creator's action).
- **Cadence:** daily from 2026-11-25.
- **Layout reference (provided by creator, analyzed):** a 104 s "Surah At-Takwir"
  video, 720×1280 — per-verse text stack (header + calligraphy verse +
  translation line) over a clean matching background. Used as a LAYOUT/style
  reference only; its recitation audio is OUT per the copyright rule above.
- **First piece shipped:** "Ubu al-Amal" — a 40 s line-art (stick-figures +
  lantern) explainer of the famous hadith "Innamal a'malu bin niyyat" (Sahih
  al-Bukhari 1), with a synthesized cricket-night ambience + action SFX. Done,
  verified, in a warm amber palette.

### Channel 2 — `pradhaana_prashnam` ("the main question")

- **Content:** one issue / society issue / political issue / idea per video.
- **Format (creator's exact spec):** the **punchline comes FIRST** — the main
  issue stated in one line as a cold open — then the video explains the issue.
- **Language:** Malayalam, narrated.
- **Automation idea (creator's):** source topics by **scraping news from the
  internet** — weekly top story or daily story. (The project already has a
  daily news-RAG scraper that fetches Reddit/X/Civitai/news into a local store —
  this is the natural source.)
- **Cadence:** daily or weekly (unspecified).

### Channel 3 — Football Talkies

- **Content:** football explained with **animation**, simple tactical terms.
  Reference channel: YouTube "Football Made Simple".
- **Creator's exact scope:** NOT a tactical masterclass. Pick a major match
  (Real Madrid / Barcelona / Champions League), then take **best player + a
  fan-favorite + the goal scorer** and explain how each contributes, using
  engagement narratives the public already agrees with, e.g.:
  "why Arda Güler is the modern No.10 football needs" · "why Mbappé is not a
  traditional No.9" · "why Vini Jr. is not a regular winger" · "why Pedri is
  essential in midfield" · "Yamal is a new Messi generation".
- **Data (creator asked "do we have any such data?") — answer: yes:**
  - XG + shot locations (→ simple heatmaps): **understat.com** (top-5 leagues,
    ~3 seasons, JSON endpoints) and **fbref.com** (XG, shot maps per match).
  - Player stats/ratings: FotMob / Who-style pages (scrapable).
  - Full player-tracking heatmaps = paid (Opta) — **out of scope** ("we don't
    need to go in depth").
- **Format:** shorts first (40–60 s); longer-form later. Language: English
  first (unconfirmed).
- **Cadence:** per major match.

### Channel 4 — Jaisal Cut

- The creator's **own art** channel (character art / short films). No production
  pipeline is needed from the agent beyond the existing ComfyUI character-art
  stack (two adult male characters, Krea2 face-locked references, identity-edit
  workflows). This brief does not cover it further.

---

## 3. What is already BUILT and PROVEN (the production stack)

All of this runs on the creator's PC and is version-controlled:

1. **Template B — a 1080×1920 @ 60 fps line-art video engine (Python/PIL).**
   Programmatic stick-figure scenes: eased text (no pops), smoothstep crossfades,
   2× supersampling, star fields, gold accents. Renders a 40 s video in ~35 min.
   A 10-second single-frame `preview()` exists for fast A/B checks.
2. **7-palette registry** (one per weekday for the daily series):
   A deep green · B midnight indigo · **C lantern amber (in use)** · D slate+gold ·
   E deep teal · F warm clay · G twilight plum. Any video picks one by a spec key.
3. **The 40-second standard:** every video is timed to 40 s, then cut into
   `part1` (0–20 s) and `part2` (20–40 s) for **WhatsApp status** + the full 40 s
   for **Instagram**. Every build script ffprobe-verifies every output.
4. **Synthesized SFX/ambience (100 % generated, zero copyright):** cricket-night
   beds, whooshes, footsteps, door sounds, placed at exact beat times.
5. **A one-command pipeline builder** (pattern: retime → render → SFX → cuts →
   verify). Reproduced the whole Ubu deliverable set in one run.
6. **A daily news-RAG pipeline** (scheduled Windows task, browser-head fetch tier
   for walled sources) — the future source for Channel 2 topics.
7. **TTS app (user's own open-source "OmniVoice Studio"):** k2-fsa OmniVoice +
   VoxCPM2 voices, faster-whisper for alignment. **Used for narration ONLY** —
   Quran recitation is a human reciter, never TTS.
8. **ComfyUI + MiniMax H3 + Krea2 lane** (character art / hybrid video) and a
   **Blender lane** (3D low-poly, for a football-set idea) — agent prepares
   workflows; **the human queues them** (hard rule: agent never queues ComfyUI).
9. **Transcription toolchain:** faster-whisper (large-v3) + demucs on GPU —
   verified working; note it garbles low-quality colloquial Malayalam audio.

### Shipped so far

- `Ubu al-Amal` 40 s (palette C, with SFX) + 2×20 s WhatsApp cuts — verified.
- A "engineering-degree" Malayalam explainer (third-party reference video,
  74 s, allapinne-style flat 2D): fully analyzed (beat map, audio forensics),
  **blocked on creator inputs**: the script text (auto-transcription failed on
  the music-heavy source audio) and per-beat graphics (creator is obtaining them).

---

## 4. Hard constraints (non-negotiable)

1. **NO music, ever** (creator is Muslim): no instrumental music, melody, beat,
   or soundtrack in ANY video. Natural sounds only (footsteps, wind, water,
   crickets, ambient). Applies to all pipelines including AI-video prompts.
2. **Narration = OmniVoice Studio only** (the creator's TTS app). Agent places
   line WAVs at beat times; ambience ducks ~6 dB under dialogue.
3. **SFX = synthesized only** (copyright-safe). A proper AI-SFX model
   (ControlFoley) is planned after 2026-11-24.
4. **Offline window: no model downloads until 2026-11-24** (fonts/models must
   come from the creator or wait; web scraping is allowed — the daily news job
   still runs).
5. **Agent never queues ComfyUI/MiniMax renders** — it prepares workflow JSONs;
   the creator queues them in his UI (shared GPU, no VRAM-release mechanism).
6. **Fonts (locked by creator):** captions = Constantia italic, labels = Arial
   Bold, closing = BASKVILL, handle = Arial. Malayalam = Nirmala (verified).
   **Arabic calligraphy font = MISSING** (none on machine; needs an Amiri-style
   font supplied, or a download after 2026-11-24).
7. **Creative choices belong to the creator** (palette picks, topic picks,
   scripts) — the agent builds and shows options; the human chooses.
8. **Distribution:** 40 s → 2×20 s WhatsApp + 40 s Instagram (all platforms).
9. **Citations must be verifiable** (e.g., the Ubu hadith = Sahih al-Bukhari 1).

---

## 5. Pipeline per channel (inputs → outputs)

| Channel | Inputs (who) | Steps (agent) | Outputs |
|---|---|---|---|
| Islamic | Topic (creator) · recitation/narration WAVs (creator/omnivoice) · backgrounds (creator or MiniMax after 11-24) · Arabic font (creator, pending) | verse/beat timeline → text stack (Arabic + translation) over backgrounds → ambience/SFX (no music) → 40 s + 2×20 s cuts → ffprobe verify | 40 s IG + 2×20 s WA, EN + ML versions |
| pradhana prashnam | News store (RAG scraper, automated) · topic pick (creator) · script approval (creator) | issue pick → **punchline-first** script → Voice Studio narration (ML) → line-art animation → SFX → cuts | 40–60 s ML short |
| Football | Match pick (creator) · understat/fbref data (agent fetches) · player picks (best + fan-fave + scorer) | data → 3-player narrative script → pitch-diagram + stat callouts (line-art) → narration → cuts | 40–60 s short, per major match |
| (ref) engineering-degree | Script text (creator) · per-beat graphics (creator) | asset compositing + narration + cuts | 40 s short (template: `docs\NARRATED_VIDEO_PIPELINE.md` 5-stage pattern) |

---

## 6. Open questions / decision points (what to consult)

1. **Handle spelling:** `learnhadithAndQuranDialy` — is it `…Daily`? (8 accounts
   to register: IG/YT/FB/X × EN+ML, on a fresh Gmail — creator's action.)
2. **Channel-1 content queue** from 2026-11-25: day 1 = Ubu (ready, not
   scenario-tied). Day 2+ = the daily 40 s explainers (scenario → word →
   explanation → warning) — first scenario-tied topic? (The news store can
   auto-suggest candidates.)
3. **Channel-2 cadence** (daily vs weekly) and the **script-approval loop** —
   how much does the creator review before publish?
4. **Channel-3 language** (English first?) and **first match**; confirm
   understat/fbref data is acceptable quality for "simple heatmaps".
5. **The engineering-degree video**: creator to supply script text + graphics;
   or convert it to the in-house line-art style (agent can fully own that)?
6. **Longer-form football videos** (creator: "a possibility") — when?
7. Any **revenue-model specifics** (branding, end cards, monetization timing)
   the creator wants baked into the pipeline (e.g., handle watermark is currently
   a `@yourhandle` placeholder).

---

## 7. Known risks / gotchas (learned the hard way)

- **Whisper transcription fails on music-bedded colloquial Malayalam**
  (hallucinated English / character-garble even after demucs vocal separation).
  Rule: script text comes from the creator, not the transcript.
- **PIL + Arabic** needs a calligraphy font + verified text shaping (libraqm) —
  not yet rendered; first render must be verified.
- **Static-frame lag** killed an earlier version of the engine (v8 = eased
  motion, smoothstep crossfades); any new scene type must use the same easing
  standards or it looks "jittery".
- **ffmpeg mjpeg encoder** on this build fails on non-full-range YUV — use PNG
  for frame extraction.
- **Console encoding** (cp1252) corrupts Malayalam/Arabic stdout — always write
  to UTF-8 files.
- **Keyframe cuts:** `-t 20 -c copy` can overshoot to the next keyframe
  (20.033 s) — acceptable for WhatsApp; part 2 is a re-encode for an exact
  boundary.

---

## 8. Immediate next actions (agent's queue)

1. Creator: create the Gmail → agent prepares 8-account bios (EN+ML).
2. Creator: drop an Arabic calligraphy font into `fonts\`.
3. Creator: supply Takvir recitation (or approve split from the reference audio)
   + 18 verse backgrounds (or "MiniMax after 11-24").
4. Creator: confirm handle spelling + first-match/language for Football.
5. Agent: build understat/fbref fetcher + a sample pitch-diagram short.
6. Agent: build pradhana-prashnam spec from the RAG news store (first topic
   pick for creator approval).
7. Engineering-degree: wait for script + assets, then build.
