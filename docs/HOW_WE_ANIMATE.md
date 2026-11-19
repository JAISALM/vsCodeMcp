# HOW OUR VIDEOS ARE MADE — plain-language version (D254, so it can be explained to people who don't use AI)

**The one-line version:** we do NOT use a video editor at all — no After Effects,
no Blender, no HTML, no timeline. A small **Python program draws every frame of
the video with code**, and a standard tool (**ffmpeg**) stitches the frames into
an MP4. AI is used for only two optional things: cinematic "hero shots" (ComfyUI)
and the spoken narration (OmniVoice Studio). Everything else is plain,
deterministic code.

## What is actually running (four standard tools, no exotic software)

1. **Python + PIL (Pillow) = the "hands".** For every 1/60th of a second, code
   computes where each element is — position, size, opacity — and draws the frame
   as a picture (cards, text, lines, circles, stars, gradients). 40 s of video =
   2400 pictures, drawn one by one.
2. **Formulas instead of keyframes = the "animation".** In After Effects a person
   drags a dot along a timeline (keyframes). Here the motion is *written as
   math* — e.g. "this line slides up 40 px and fades in over 0.6 s with a
   slow-out curve" (easing functions: ease-out, smoothstep). The computer then
   draws all 2400 frames from those formulas. Think of it as a **flipbook where
   a program draws every page** — same principle as stop-motion, but the hands
   are code. That is what "procedural animation" means.
3. **NumPy = the sounds.** The whooshes, door creaks and footsteps are
   *synthesized* — mathematically generated tones (low-frequency sines, filtered
   noise), not recorded samples. No audio files are ever imported (and no music,
   ever — natural sounds only).
4. **FFmpeg = the projector.** It stitches the 2400 pictures into an H.264 MP4,
   mixes the synthesized audio in, and makes the 2×20 s distribution cuts.
   FFmpeg is the industry-standard open video tool (used by YouTube itself).

## Where AI actually sits (two optional layers — everything else is code)

| Layer | What | Who runs it |
|---|---|---|
| **Procedural core (always)** | PIL frame-drawing + formulas + numpy sounds + ffmpeg | the build script, one command, seconds–minutes, no GPU |
| **Narration (per video)** | spoken voice per beat | OmniVoice Studio (the author's own app) — human-approved text |
| **Hero shots (rare, optional)** | 1–2 cinematic moments per video: an AI image (Krea2) turned into AI video (MiniMax H3) | ComfyUI — **the author queues it** (shared GPU) |

The AI layer is *spice on top of a code-determined video*: if a hero shot is
skipped, the video is still complete (text cards + procedural motion carry it).

## Why built this way (the engineering reasons)

- **Daily content needs a one-command pipeline.** A day's video is a JSON table
  of beats (times + text); the machine draws everything from that table. No
  hand-keyframing, no editor licenses, no manual timeline work.
- **Reproducible:** same input table → identical video, every time. A day's
  deliverable (40 s + 2×20 s) is produced and ffprobe-verified by ONE command.
- **Cheap & parallel:** the procedural core uses the CPU only (no GPU), so it
  never fights the shared GPU (ComfyUI / local LLM) — which is exactly why the
  AI layer is rare and manually queued.
- **The football channel is data-driven**: the tactics board (pitch, player
  dots, arrows, shot/XG markers) is DRAWN BY CODE from scraped match data
  (understat/fbref JSON) — the same "program draws the frame" principle, with
  numbers from the real match.

## What each channel uses

| Channel | Procedural (code) | Narration | AI hero shots |
|---|---|---|---|
| 1 — Islamic daily | Template B text cards + line-art | OmniVoice (EN+ML) | none planned |
| 2 — pradhana | punchline cards + visual metaphor | OmniVoice (ML) | optional, rare |
| 3 — football | **data-drawn tactics board** + stat callouts | author's voice / OmniVoice | optional player-story moment |
| 4 — Jaisal Cut | (artist lane) | — | Krea2/ComfyUI is the main tool here |
| Film (episode 1) | — | — | Krea2 refs → MiniMax H3 R2V is the main tool (bespoke cinematic film) |

**Bottom line for the non-AI explainer:** "It's mostly a program that draws
2400 pictures with math and ffmpeg joins them — like stop-motion where a
computer draws each page. AI only paints one or two fancy background shots and
speaks the narration."
