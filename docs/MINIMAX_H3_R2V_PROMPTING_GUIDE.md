# MiniMax H3 — Reference-to-Video (R2V) Prompting Guide

Workspace reference for writing MiniMax H3 R2V prompts. Source: official MiniMax H3
docs (`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` + ComfyUI MiniMax H3 tutorial).

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

6. **`non_diegetic_music`** — background music audible only to the audience.
   ```
   non_diegetic_music: A restrained, slow cinematic score with soft piano and low strings.
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
