# Lesson-Shorts Template-Factory Pipeline (2026-11-18)

Status: **pipeline CHECK session — Template B renderer built + demo rendered (local, D192-compliant).**
References: 3 user-sent shorts re-analyzed this session (frames + spectral audio classification, `data\refanim\`).

## What we're building

Template-factory shorts (per LIFE_PLAN content backlog): the **da'wah line** (lesson/Quran shorts) +
**football line** + **kids' line**. Each line = ONE reusable template (scene layout + style set +
text style + audio bed) filled with new content per video. NOT bespoke AI video generation —
that's the cinema line (Jaisal). This is the cheap/batchable background line.

### Reference videos (re-verified 2026-11-18, frames in `data\refanim\`)

| Ref | Content | Style | Format | Audio (spectral estimate) |
|-----|---------|-------|--------|---------------------------|
| v1 `ZkdWP-OJTWbaIw` (2:50) | "Your First Night in the Grave" — hadith-based | **Template A** flat 2D vector: faceless silhouettes, purple/pink night gradient, moon, rounded "stage" | 720×1280 9:16 30fps | **narration over ambient bed** (syllabic modulation 0.43 + continuous floor; no music) |
| v2 `549UNr7yalVugw` (2:00) | @aiishadahir — WITH/WITHOUT contrast series (BARAKAH, TAWAKKUL…), Quran citations | **Template B** neon single-stroke line-art on dark green, gold glow, card layout, series numbers | 1080×1920 9:16 30fps | **narration** (voiceband ratio 0.92, tonal flatness 0.17) |
| v3 `jD6cSpz5JLQx4g` (1:18) | @thefinalthird football debate | **Template C** low-poly 3D pitch + faceless kit figures | 576×1024 9:16 30fps | **natural sound** (crowd ambient; env std only 2.2 dB = continuous, no speech pauses) |

Spectral method: 50 ms hop / 0.5 s win — activity ratio, envelope std (burstiness), median
spectral centroid, median spectral flatness (0 = tonal, 1 = noise-like), voiceband (100–3000 Hz)
energy ratio, 3–8 Hz envelope modulation (syllabic rate). **User to confirm by ear which bucket
each video lands in** (narration-only vs text+natural-sound) — estimates above.

## THE TWO AUDIO MODES (user-specified 2026-11-18)

Both modes obey the **D041 HARD RULE: NO music / NO instruments / NO beat — ever.**

### Mode A — narration only (no music)
Voice track carries the content; audio = voice alone (or voice over a very quiet natural ambient
bed, ducked ~25–30 dB below voice).
- **Voice sources:** (1) user's own dub (headset → `clean_audio.py`, openvoice venv — best for a
  personal da'wah brand) (2) **IndicF5** (Malayalam-native TTS — parked+working,
  `D:\models\ai-movie\scripts\indicf5_*`, venv `envs\indicf5ml`) (3) **Fish S2 Pro** (80+ langs
  incl. English — parked+working, venv `envs\fishs2`).
- **Post:** `clean_audio.py` → 16 kHz mono → loudnorm −16 LUFS.
- Reference: v2 (clean voice over calm visuals = the respectful da'wah format).

### Mode B — text on screen + natural sound (no narration)
No voice at all; the on-screen caption IS the content; audio = natural ambience matching the
scene (night = distant crickets/wind; stadium = crowd murmur; home = room tone + clock tick).
- **Ambient sources:** (1) **ControlFoley TC-V2A** (PROVEN 2026-09-03, P5 — video + text-guided
  natural sounds; prompt = exact sounds in story order + the D041 NO-music statement;
  `guidance_scale 4.5`, steps `fixed`, seed 42; workflow + `utilities\submit_controlfoley.py`
  exist; **user queues** per D192) (2) H3-native natural audio (any H3 clip generates natural
  sound — but H3 clips drift stylistically, so only for Template A stills with i2v) (3) a
  synthesized ambient bed (last resort — ffmpeg-generated noise shapes; weakest).
- **Mix:** ffmpeg — ambient only (Mode B) or ambient ducked under voice (Mode A with bed).
- Reference: v3 (crowd ambient, zero narration).

**D041 statement to paste in every ControlFoley/TTS-adjacent audio prompt:**
`NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO
soundtrack, NO song. Natural ambient sounds only.`

## Toolchain per template line

| Line | Visual engine | Text overlay | Motion |
|------|---------------|--------------|--------|
| **B — neon line-art** (da'wah contrast series) | **Programmatic renderer** `utilities\lesson_shorts_template_b.py` (Python PIL, data-driven scene spec → 30 fps PNG sequence → ffmpeg). Clean single-stroke geometry = AI generation would wobble; drawing it is exact. | same renderer (serif caption + gold accent words + typewriter + citation + series number) | line draw-on, star twinkle, glow pulse, progress ring, typewriter caption |
| **A — flat 2D vector** (hadith scenes) | **Krea2 t2i** stills in the flat-vector style set (faceless silhouettes, gradient night, gold accents) — user queues 2–3 at a time (D192) | ffmpeg drawtext / PIL overlay | ffmpeg `zoompan` slow push-in + text animation |
| **C — low-poly football** | **Blender** (MCP, local — agent-runnable): reusable pitch + crowd + faceless kit-figure template; swap kit colors/figures/text per video | Blender text objects / PIL overlay | camera push/arc, figure walk cycles |
| **Kids' cartoon** (future) | Krea2 t2i — SECOND style set (bright/flat primaries, high contrast — the kids' attention palette) | PIL overlay | ffmpeg zoompan |

**Shared:** assembly = ffmpeg (concat + audio mix + loudnorm) · voice = user dub or parked TTS ·
audio bed = ControlFoley (Mode B) or ambient bed (Mode A) · **no music (D041)**.

### Why programmatic for Template B
The style is pure geometry (single-stroke lines, circles, rects, dots, one gold accent).
Data-driven drawing = pixel-identical brand consistency across every video in the series
(exact the brand), zero style drift, free batch generation, fully offline. AI's job shrinks
to: script/quote selection (local LLM drafts) + optional Template A scene stills.

## Content-integrity spec (non-negotiable, da'wah line)
1. **Verified citation on-screen in every video** (hadith = collection + number; or surah +
   ayah). **LLM drafts the script; the HUMAN verifies the source** — the citation is the
   credibility layer.
2. **Non-depictive:** faceless figures only; NEVER depict the Prophet ﷺ, Allah, or the Quran as
   a character. Animate lessons/stories/calligraphy around the text, not around figures of the
   sacred.
3. **No music (D041).** Voiceover + natural ambient = the respectful format — "music-free,
   respectfully told" IS the brand.

## Format spec
- Master 1080×1920 9:16 @ 30 fps, H.264 yuv420p crf 19 (refs also ship 720×1280 / 576×1024).
- Structure: hook 0–3 s → 3–6 scene cards (WITH/WITHOUT contrast or sequential story) →
  closing (series number + handle). Total 1.3–3 min.
- Text: serif caption (Georgia — Cambria on this machine is `.ttc`-only, so the renderer
  uses `georgia.ttf`), gold accent words (#D4A94E), all-caps letter-spaced labels (Arial),
  typewriter cursor on active caption line.

## Pipeline stages (per video)
1. **Content:** topic → local LLM drafts script + candidate citations → user verifies citations.
2. **Scene spec:** JSON of primitives per card (lines/circles/rects/dots/labels) — or a Krea2
   still for Template A.
3. **Render:** Template B = `lesson_shorts_template_b.py` (sequence → ffmpeg). Template A =
   ffmpeg zoompan on the still.
4. **Audio:** Mode A = dub/TTS → `clean_audio.py`; Mode B = ControlFoley (user queues).
5. **Mix + encode:** ffmpeg (voice/ambient + video → final mp4, loudnorm −16 LUFS).
6. **QA:** watch 0–3 s hook + one full pass; check citation legibility + no-music.

## Status / next
- **DONE 11-18:** ref re-analysis (frames + spectral audio classification) · Template B
  renderer built + 9 s demo rendered (`data\refanim\template_b_demo.mp4`) · this doc.
- **NEXT:** (1) user confirms audio-mode buckets by ear (which refs are narration vs
  natural-sound) (2) pick line #1 to batch (da'wah B series = cheapest: pure renderer, zero
  ComfyUI) (3) topic list → LLM-drafted scripts → user verifies citations (4) Mode A: first
  TTS pass (IndicF5 ML or Fish EN) or user's dub (5) Mode B: ControlFoley ambient on one
  rendered scene (user queues) (6) end-to-end first video.
- **OPEN:** voiceover language (English? Malayalam? Arabic?) · channel handle for the bottom
  watermark (demo uses `@yourhandle`) · series numbering scheme.
