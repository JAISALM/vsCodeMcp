# MiniMax H3 — Reference-to-Video (R2V) Prompting Guide

Workspace reference for writing MiniMax H3 R2V prompts. Source: official MiniMax H3
docs (`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` + ComfyUI MiniMax H3 tutorial).

> ## ⚠️ HARD RULE — NO MUSIC (strict, all future scenes)
>
> **The user is Muslim and does NOT want instrumental music in any of their videos**
> (movies, title animations, etc.). This is a **strict, permanent guideline** for ALL
> future MiniMax H3 generations and ALL audio work in this project.
>
> **For every prompt, the `non_diegetic_music` section MUST state:**
> ```
> non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO
> melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only.
> ```
> **The `overall_soundscape` section MUST contain ONLY natural sounds** (footsteps,
> wind, water, birds, splashes, whooshes, ambient) — **never** a score, melody,
> instruments, or beat.
>
> **Do NOT write a cinematic score, piano, strings, or any musical description in
> any section.** If a prompt template or example shows music, replace it with the
> NO-music statement above.
>
> See **D041** in `project-memory/DECISIONS.md`.

## When to use R2V

Use the **ref2va** model (`minimax_h3_ref2va_pruned_int8_convrot.safetensors`) when
you have reference images/videos/audio to condition the generation. The
`MiniMaxH3ReferenceToVideo` node accepts up to **9 reference images**, **3 reference
videos**, and **3 reference audio** files.

- `ref_image_size`: `match` (scale down to fit) or `max` (2048px short edge).
- Turbo mode: add the turbo LoRA (`minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors`)
  for 4-step fast generation.
- Native stereo audio (dialogue/SFX/music in one MP4).
- Duration snaps to a 17-frame-per-block grid (17k+5) at 24fps.
- Native canvas: 768px short edge = 1344×768 at 16:9, rounded to a multiple of 32.

## The core R2V prompting idea

**Reference each input by a tag in connection order**, then **assign each reference a
job** (identity, style, motion, camera, voice, or frame anchor). The model reads the
tags and knows exactly which reference provides what.

### Reference labels

| Label | Meaning |
| --- | --- |
| `<Subject N>` | Reusable visible content (person, object, scene, style, pose) abstracted from references |
| `<Picture N>` | A reference image used as a concrete frame anchor (first/last/keyframe) or storyboard |
| `<Video N>` | A reference video providing editing source, continuation, or temporal structure |
| `<Audio N>` | An audio signal that is copied or referenced (timbre, music style, dialogue) |

**Numbering = connection order.** `<Picture 1>` is the image in `ref_image_0`,
`<Picture 2>` is `ref_image_1`, etc. Keep the same label meaning across all sections.

### Relationship markers

| Marker | Meaning |
| --- | --- |
| `fully_preserved` | The referenced content's role is fully preserved |
| `partially_preserved` | Still used, but some characteristics changed |
| `attribute_transfer` | Characteristics transferred to a different subject |
| `weak_reference` | Only broad similarity in style/composition/atmosphere |

Audio markers: `fully_copy`, `partially_copy`, `reference`, `weak_reference`.

## The 6-section structure

Write all six sections in English, in this order:

1. **`subject_definitions`** — define each referenced content unit and its label.
   One line per item. Name the source asset when provenance matters.
   ```
   <Subject 1> is the young boy in <Picture 1>, <Picture 2>, <Picture 3>, with short dark hair, a school uniform, and a red school bag.
   <Picture 1> is the first frame of [Shot 1], a wide establishing shot of the boy on the stone bridge.
   ```

2. **`summary`** — one short paragraph. Begin with a square-bracketed task-type prefix:
   `[reference generation]`, `[keyframe completion]`, `[video editing]`,
   `[video continuation]`, `[audio reuse]`, `[audio reference]` (combine with ` + `).
   ```
   [reference generation] The target video is a 15-second five-shot sequence. <Subject 1> and <Subject 2> are preserved across all shots. Each shot begins from its corresponding reference frame...
   ```

3. **`retention_analysis`** — one line per reference label, with a relationship marker.
   ```
   <Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the boy's face, hair, uniform, and red bag are retained.
   <Picture 1> ([Shot 1] first frame): fully_preserved - the wide base-scene composition is the opening frame.
   ```

4. **`detailed_description`** — the main body. Describe visuals, actions, shots, sound,
   and dialogue in playback order. Normally 350-500 English words.
   - `[Shot 1]` marks the opening shot (no timestamp).
   - Later shots: `[Shot N] At MM:SS.mmm, ...` to mark cut times.
   - Camera movement as natural English (type, amplitude, speed).
   - Dialogue as `<d>[Language] ...</d>`; speaker IDs `(S1)`, `(S2)`.
   - Cite `<Picture N>` at the shot it anchors: "the shot begins from <Picture 1>".
   ```
   The target video is in an angular 3D art style with brush stroke color texture.
   [Shot 1] A wide establishing shot opens on <Subject 2>, the long stone bridge. <Subject 1> stands small in the frame. The camera is static, then a slow push-in. The shot begins from <Picture 1>.
   [Shot 2] At 00:03.000, the shot cuts to a medium shot of <Subject 1> as rain begins. The shot begins from <Picture 2>.
   ```

5. **`overall_soundscape`** — ambience and physical sounds across the full video.
   ```
   overall_soundscape: Rain sounds throughout - light rain building in [Shot 2], heavy rain in [Shot 3], dripping in [Shot 4], quiet stillness in [Shot 5].
   ```

6. **`non_diegetic_music`** — **MUST state NO MUSIC** (see the HARD RULE at the top).
   Never describe a score, melody, instruments, or beat. Use natural sounds only.
   ```
   non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO
   melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only.
   ```

## Practical tips for our Jaisal Cut use case

- **Assign each reference image a job.** Don't just list them — say what each provides
  (identity, frame anchor, style, motion).
- **Use `<Picture N>` as frame anchors.** "the shot begins from <Picture N>" tells the
  model exactly which reference is the opening frame of which shot.
- **Partition into `[Shot N]` with camera angles.** Each shot: camera angle + what's
  happening + which `<Picture N>` it anchors to.
- **Keep the style consistent.** State the art style once in the `detailed_description`
  opening, then let it carry through.
- **Title is composited in post.** If a title is added in post, say so explicitly:
  "The title is composited in post and is NOT rendered by the model." Leave negative
  space in the final shot for it.
- **No dialogue/text** if not wanted: state "No dialogue, no text, no subtitles."

## Forcing a specific camera angle (the H3 camera-correction problem)

H3 has a strong internal prior to "correct" the camera toward a flattering eye-level
view, especially when a face is in frame. If you ask for a strong angle (overhead,
low-angle, etc.), the model may silently move the camera back to eye level to make
the subject look better. The common cheat: keep the camera at eye level and just tilt
the subject's head. To force a specific camera angle:

1. **Put the camera constraint at the absolute top.** H3 weights the first few lines
   most. Open the prompt with a `MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE
   ALL ELSE: ...` line that names the exact angle. Don't bury the camera instruction
   in the middle — it gets treated as background and ignored.

2. **Explicitly accept the natural distortion that angle causes.** A strong angle
   distorts the subject (larger forehead, compressed lower face, foreshortening).
   The model's face-enhancement tendency will try to "fix" this by moving the camera.
   Tell it the distortion is CORRECT and must not be removed:
   "ACCEPT NATURAL [ANGLE] PERSPECTIVE DISTORTION."

3. **Explicitly forbid moving the camera to fix the subject.** Prohibit the cheat
   directly: "DO NOT CORRECT CAMERA TO EYE-LEVEL TO FIX [SUBJECT] PROPORTION",
   "DO NOT auto-adjust camera perspective", "REJECT flat eye-level frontal camera".

4. **Use short hard negative commands.** Long explanatory reasoning is less reliable
   than short prohibitions. "NO eye-level shot", "NO camera at face height",
   "FORBIDDEN: flat frontal camera". Short `DO NOT` / `NO` / `FORBIDDEN` commands
   read as hard constraints.

5. **Keep the reference's identity, discard its camera.** The reference image should
   provide identity/appearance only. Add "COMPLETELY DISCARD <Picture N> original
   camera angle, framing, background, lighting, and pose" so the reference doesn't
   drag the camera back to its original position. Keep the person, replace the scene
   and camera.

### Reusable camera-lock block

```
MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: [name the exact angle,
e.g. "FORCE a 45-55 degree high-down overhead shot, 30-60 cm above the subject's
head"]. ACCEPT NATURAL [ANGLE] PERSPECTIVE DISTORTION. DO NOT CORRECT CAMERA TO
EYE-LEVEL TO FIX [SUBJECT] PROPORTION. DO NOT auto-adjust camera perspective.
REJECT flat eye-level frontal camera.
```

Then repeat the angle lock per `[Shot N]` and add a `CAMERA LOCK` section that
restates the angle for every shot + the forbidden camera behaviors. For a STATIC
shot, the lock is the inverse: "the camera is locked and does NOT move, does NOT
push in, does NOT drift, does NOT tilt, does NOT pan, does NOT zoom."

### Be specific about what the subject does AND does not

For each `[Shot N]`, list the concrete actions in order (walk → stop → turn head →
whistle) AND the forbidden actions ("does NOT run, does NOT jump yet, does NOT leave
the bridge, is NOT duplicated"). Vague "the character moves" reads as dead; a clear
action chain + explicit NOT-list gives much tighter control.

### Lock the background (no out-of-space hallucinations)

H3 will hallucinate background elements that are not in the reference (a wooden
floor, a room, a table) if the background is not explicitly locked. A line-art
reference with a warm *paper/cream* background is especially prone to a "wooden
table" hallucination — the model reads "paper" and adds wood. Add a top priority
`BACKGROUND LOCK` that names the EXACT background AND explicitly forbids the
warm/wood family: "the background is PURE WHITE (a clean empty white void),
EXACTLY like the reference image. NOT cream, NOT beige, NOT tan, NOT paper, NOT
wooden. NO wooden overlay, NO wooden floor, NO wooden table, NO wood grain, NO
brown tones, NO warm tones, NO table, NO room, NO wall, NO scene, NO environment,
NO color, NO shading, NO additional background elements, NO out-of-space objects."
Restate it in the `detailed_description` global line. Saying "plain white" alone is
NOT enough — you must also say "NOT cream/paper/wooden" or the warm paper tone
drifts into a wooden overlay.

### A single continuous take anchors the WHOLE shot to the reference (phase-based state locks)

In a single continuous take (i2v from one image), the reference image anchors the
ENTIRE shot — not just the first frame. So if the reference shows the figure on the
bridge, the model's prior is "figure on the bridge" for the whole take, and it will
KEEP the figure on the bridge even after you say "then he jumps" (it can't cleanly
*remove* the figure from the bridge context). Two fixes:
1. **Use PHASE-based language, not Shot-based.** "Shot 1/2/3" implies cuts, but a
   continuous take has no cuts — it confuses the model. Use "PHASE 1 - WALK /
   PHASE 2 - THROW / PHASE 3 - JUMP / PHASE 4 - PLANE FILLS SCREEN / PHASE 5 -
   TITLE" in one continuous take.
2. **Give each phase an explicit STATE lock** (ON the bridge / in the AIR / GONE)
   and a hard rule for the transition: "AFTER THE JUMP (PHASE 3), the figure is NO
   LONGER on the bridge - he does NOT walk on the bridge after jumping, he does NOT
   return to the bridge, he does NOT reappear on the bridge." The explicit
   "does NOT [old state] after [new state]" is what breaks the reference anchor.

### Ambiguous gestures get misread (whistle → drinking)

A vague gesture like "whistles (one line arm raised to his head)" was rendered as
the character DRINKING from a cup. Use CONCRETE physical actions (throw a paper
plane, jump) instead of ambiguous gestures, and add a NOT-list for the misread
("does NOT drink, does NOT hold a cup, does NOT hold a bottle, does NOT hold any
object to his mouth").

### Split the video into per-second parts (the timeline technique)

H3 compresses a long sequence if you only describe the actions in order without
timing — e.g. a 15s take where the figure "walks, throws a plane, jumps, the plane
fills the screen" will have the jump done by ~6s and the plane back by ~7s, because
the model front-loads the action. The fix (from the high-overhead camera workflow):
**split the video into at least one part per second** and instruct what happens in
each second explicitly. For a 15s take, write 15 timeline segments
(`0.00-1.00 second: ...`, `1.00-2.00 second: ...`, ... `14.00-15.00 second: ...`),
each naming the figure's exact state + action + the background lock. This forces the
model to spread the action across the full duration instead of compressing it.

Two rules for the per-second timeline:
1. **One state per second.** Each segment names the figure's exact state (ON the
   bridge / in the AIR / in the water) and the one action happening in that second.
   Don't cram two actions into one second.
2. **Lock the background in EVERY segment.** Restate "the background is pure white,
   black ink lines only" in each second — a single background lock at the top is not
   enough; the model drifts to a wooden/mica overlay mid-take if the lock isn't
   repeated per segment.

Also add a **sound-to-action beat map** (a table: time → natural sound → visual
action) at the end of the prompt to sync the action to the audio (NO music — natural
sounds only, per the HARD RULE), and a **NOT-list** that forbids the failure modes
("the figure does NOT jump before the plane has floated", "the plane does NOT come
back", "the plane does NOT fill the screen").

## Jaisal Cut low-angle workflow — reference mapping

Connection order in `jaisal_lowangle.json` (ref_image_0..4):

| Tag | File | Content | Anchors |
| --- | --- | --- | --- |
| `<Picture 1>` | 1.png | wide establishing / base scene | [Shot 1] |
| `<Picture 2>` | 2.png | mid-rain medium shot | [Shot 2] |
| `<Picture 3>` | 3.png | close-up drenched | [Shot 3] |
| `<Picture 4>` | 4.png | after-rain medium shot | [Shot 4] |
| `<Picture 5>` | 5.png | low-angle ending (water, kid looking up) | [Shot 5] |

`<Subject 1>` = the boy (all 5 pictures). `<Subject 2>` = the stone bridge environment
(pictures 1, 2, 4, 5).

## Source

- Official R2V guide: `https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`
- Base guide (T2VA/I2VA/FL2VA/L2VA): `https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md`
- ComfyUI MiniMax H3 tutorial: `https://docs.comfy.org/tutorials/video/minimax/minimax-h3`
