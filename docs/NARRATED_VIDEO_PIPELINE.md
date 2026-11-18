# NARRATED VIDEO PIPELINE (captured 2026-11-18)

One series, three lanes — same engine, same audio rules, same distribution cuts.

| Lane | Video | Graphics | Motion |
|---|---|---|---|
| LINE-ART | Ubu al-Amal | Template B (PIL line art, 60 fps, v8 anti-lag) | programmatic |
| ANIMATION | Engineering-degree (allapinne-style) | USER supplies flat-2D assets per beat | asset compositing |
| ROBLOX | Football set | Template C / Blender low-poly 3D | 3D |

## Distribution standard (D241, user 2026-11-18)

**Target length 40 s.** Cuts:
- `part1` 0–20 s → WhatsApp status
- `part2` 20–40 s → WhatsApp status
- full 40 s → Instagram

Ubu proof: `utilities\build_ubu_al_amal.py` (D240) — one command: retime 48→40 s
(uniform 5/6, `rescale()`), render 2400 frames @60, encode, SFX at retimed beats,
cut + verify. Outputs `data\refanim\ubu_al_amal_40{,_sfx}.mp4` +
`ubu_40s_part{1,2}.mp4`.

## Stage 1 — Script → narration lines

- Script text from the USER (whisper garbles low-quality colloquial audio —
  `data\eng_degree\` shows turbo AND Systran large-v3 failing; demucs htdemucs
  vocals stem did NOT fix it).
- Lines → WAVs in **OmniVoice Studio** (user runs the app, D239): k2-fsa/OmniVoice
  + VoxCPM2 TTS; faster-whisper aligns line timing.
- Line WAVs land in `data\<video>\lines\line_NN.wav` with a timings list
  `lines\TIMINGS.json` (`[{"line": 0, "t0": 0.0, "t1": 3.2}, ...]`).

## Stage 2 — Assets

- ANIMATION lane: user drops per-beat assets into `data\<video>\assets\`
  (frames or short clips, any size — engine scales to 1080×1920).
- Asset list `assets\ASSETS.json`: `[{"id": "lead_walk", "file": "lead_walk.mp4"}, ...]`.

## Stage 3 — Composition (1080×1920 @ 60 fps)

Template B engine (v8: smoothstep ramps, crossfades, eased text, 2× supersample).
New spec block for asset beats:
```python
{"t0": 12.0, "t1": 24.0, "asset": "lead_walk",   # from ASSETS.json
 "layout": "full" | "card", "x": 0, "y": 0, "scale": 1.0,
 "fade": "x", "float": 0.0}
```
Text overlays use the locked fonts (caption=Constantia italic, labels=Arial Bold,
close=BASKVILL, handle=Arial). Palette: per-video from the palette set (A green /
B indigo / C amber / D slate — `data\refanim\palette_ab.png`).

## Stage 4 — Audio (D041 HARD: NO music, ever)

1. Narration lines placed at TIMINGS.json times (master bus, 0 dB).
2. Ambience bed (`synth_ambient.py`: crickets/room tone/whoosh — 100 % synthesized,
   zero copyright) ducked **~6 dB under narration**.
3. Action SFX at exact beats (`--door`, `--steps` flags) — only for actions that
   need them, mild, focus-friendly (user-confirmed 2026-11-18).
4. Mix → ffmpeg aac 160k.

## Stage 5 — Distribution cuts + verify

ffmpeg: part1 `-t 20 -c copy` (keyframe-tolerant for status), part2
`-ss 20 -c:v libx264 crf 19 -c:a aac` (exact boundary). ffprobe every file
(codec + duration) before delivery.

## Per-video checklist

1. `data\<video>\` created (script_original / assets / lines / out)
2. BEAT_BREAKDOWN.md (visual + timing map)
3. Content spec (`utilities\lesson_shorts_<video>.py`) with the timeline
4. Build script (`utilities\build_<video>.py`) — render → audio → cuts → verify
5. Memory: CURRENT_TASK + EXPERIMENTS + commit (D131)
