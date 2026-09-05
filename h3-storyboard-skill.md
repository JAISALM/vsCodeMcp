***

# H3 Storyboard & Performance SOP

**Name:** `h3-storyboard`
**Description:** Turn a script into MiniMax H3 shot lists with working emotional performance — beat tables, shot counts, expression direction, and the acting techniques that actually render.
**Use When:** Breaking a script or scene into H3 shots, writing beat timings, directing a character's face or emotion, fixing flat/wooden performance, deciding shot length, or writing prompts for episodic narrative work.
**Complements:** `minimax-h3` skill (covers prompt syntax and ComfyUI setup). This skill covers **performance logic** and **shot breakdown**.

---

## Core Philosophy

The `minimax-h3` skill teaches you **how to write what you've already figured out in H3 format**.
This skill teaches you **how to think** — how to break down a script into shots, and how to turn emotions into actions the model can actually perform.

Official and community skills stop at the "translation layer." This SOP covers the missing gap: **performance direction**. All rules below are extrapolated from real production tests (isolated variables, fixed seeds) and are marked with their verification status.

---

## I. 🔴 First Law: One Shot Cannot Hold Too Many Beats

**Rule:** Stuffing too many facial expression beats into a single shot makes the model converge toward "average motion," flattening everything out. You write eyes opening, eyebrows raising, lip biting — and nothing happens on screen. No error message, no warning.

### Evidence (Controlled Experiment)
Same shock scene, same seed, same facial beats:

| Version | Shot Structure | Dialogue | PSNR at Emotional Peak | Result |
| :--- | :--- | :--- | :--- | :--- |
| **A** | One 7-second close-up, 9 beats | None | **37–42 dB** | Face completely still (Failure) |
| **B** | Split into three 2–3 second shots, one main beat each | None | **22–23 dB** | **All expressions landed** |
| **C** | Same as B | Added `<d>` | **19 dB** | Performance slightly stronger |

*(Note: PSNR lower = more visual change. 42 dB is effectively a frozen frame.)*

**Key Insights:**
1.  **A → B is the main factor: Splitting shots.** Most of the effect comes from breaking long shots into short ones.
2.  **B → C is a bonus: Dialogue.** Helpful, but not the primary mechanism.

### Action Plan
```
① Count the beats. More than 2–3 facial beats per shot → split it.
② Split into 2–3 second short shots, one main beat each.
③ Write dialogue if there is any (see below), but it works without it too.
```

**The cut itself is performance** — the audience automatically re-reads the character's state at the cut point. So splitting isn't just so the model can execute; it's also so the audience can see it.

> **Verification:** 2026-08-26, Ref2VA 243 frames, three-way comparison, seed fixed. This was isolated: A→B changed only the shot structure; B→C changed only one line of dialogue.

### The Role of `<d>`: It Steals Time
Shots with dialogue have stronger performance, but the mechanism isn't "dialogue makes the face move" — **H3 redistributes the entire video's time budget, giving more to the shot that has dialogue.**

**Data (243-frame video, 4 shots):**
*   **No Dialogue:** The emotional peak shot was compressed to 55 frames (spec was 74). The emotion cut off mid-performance.
*   **With Dialogue:** The peak shot got 84 frames. Facial change was stronger (28.5 dB vs. 30.2 dB for no-dialogue).

**The Cost:** The extra frames are taken from other shots.
*   *Example:* In a 4-shot sequence, adding dialogue to Shot 3 squeezed Shot 4. The background character in Shot 4 disappeared because the shot was too short to establish continuity.

**Rules for Dialogue:**
1.  **Performance Shots:** Write dialogue (even internal monologue/voiceover).
2.  **Continuity Shots:** Do **not** put them in the same video as dialogue shots if you need background continuity. Render two versions (with/without dialogue) and cut between them if needed.
3.  **Internal Monologue Format:**
    ```text
    the young woman, in a small unsteady voice that catches once partway through (S1),
    says in an off-screen voiceover: <d>[Chinese]……</d>
    while her lips remain completely closed.
    ```
    *   **Emotion** goes in the `delivery` field, **not** inside `<d>`.
    *   **Do not force dialogue** just for performance. If the character is designed to be silent (listening, avoiding, sulking), splitting into short shots is enough.

### Silent Characters: Use Large Body Movements
For characters without dialogue, **facial beats can still be written**, but **large body movements are safer**:

| Facial (Riskier) | Large Body Movement (Solid) |
| :--- | :--- |
| Jaw muscle bulges once | Nose exhales long, shoulders drop |
| Blink, gaze drops to floor | Hand wipes down pants → grabs back of neck → head tips forward |
| Upper eyelids fully open | Head pulls back three centimeters |
| Lower lip tucks inward | Object in grip loosens, tilts downward |

**Locomotion** (sitting up, standing, walking somewhere) almost never fails — it's the most reliable category.

---

## II. ⛔ Do Not Write "Nothing Changes"

**Rule:** Never write "nothing changes" or "stays still" in a prompt.
```text
❌  From 00:04.800 to 00:05.300 nothing about her changes:
    her eyes stay where they are, her mouth stays where it is, her head does not move.
```
**Result:** This is a strong "don't move" instruction that **leaks into the entire shot** — resulting in things that *should* move also not moving.

**Solution:** Leave that "not yet reacted" pause as an **edit point**:
```text
Shot A ends on "movement stops"
── cut ──                       ← pause happens here, freeze frame in post for as long as needed
Shot B starts on "reaction begins"
```
**Pauses are the editor's job, not the generator's.** Leave it to post-production — 100% controllable.

> ⚠️ **Note:** This rule is **not isolated** in testing (it was paired with the "9 beats in one shot" problem). Thus, "don't write it" is the safe practice, but whether it's the *primary* cause of flatness is uncertain. However, pauses are inherently more controllable in editing, so there is no reason to take the risk.

---

## III. Dialogue Length is a Hard Constraint (For External Audio)

When H3 generates its own voice, it speaks faster to fit the dialogue in.
**Once you plan to discard its audio track and use real voiceover, time becomes a hard constraint** — you can't change a real voice's speaking speed significantly (`atempo` > 5% becomes audible).

### Calculation
1.  Measure your voice actor's speaking speed: `Total Characters / Total Seconds`.
    *(Example: 4.30 characters/second, including within-sentence pauses.)*
2.  **Character count ÷ speaking speed = seconds needed.**
3.  **Compare that to the duration of the shot containing the dialogue.**

⚠️ **Critical Warning:**
Do not compare dialogue length to the "distance to the next beat."
Real production proves: dialogue is marked at 3.400s, next beat at 4.000s, but the mouth starts moving at 2.17s and keeps moving until the video ends at 5.12s.
**H3 treats the entire shot as the person speaking; it doesn't close the mouth at the next beat.**

### What Actually Causes Problems
Putting beats in the same shot that conflict with speaking:
```text
❌ At 00:03.200  dialogue starts
   At 00:04.600  she finishes speaking   ← forces H3 to close mouth here
   At 00:05.200  blink
   At 00:05.800  swallow                  ← impossible mid-sentence
```
**Fix:** Put post-dialogue beats in the **next shot**.
That shot is entirely "he is speaking" — the mouth movement fills the whole shot, and time is naturally sufficient.

**Voiceover (VO) Exception:**
VO is unrestricted — post-production can make it as long as needed, spanning shots or even videos.

---

## IV. ⛔ Do Not Film Collisions, or Liquid Volume

H3 cannot do **contact-driven causality**, nor maintain **liquid volume**.

### Evidence
Prompting "hand knocks over coffee cup, coffee spreads and floods the small object on the table" resulted in:
*   **Hand never touches the cup:** Cup spins and falls in mid-air; no contact in any frame.
*   **Coffee volume > one cup:** Fills half the table in two seconds, keeps flowing after "done."
*   **Liquid doesn't behave like liquid:** Hard scalloped edges like a sticker, doesn't follow wood grain.
*   **Key beat didn't happen:** Liquid never touched the small object.

Writing more detailed prompts doesn't help — it didn't misread; it just can't do it.

### Solution: Don't Film the Moment
```text
Shot 1  Arm sweeps across the frame from the edge, filling the entire frame as it comes close
Shot 2  Cut — the thing has already happened. Cup is lying down, spill has spread and stopped
        H3 only needs to "continue an existing state," not "initiate a collision"
Impact sound on the audio track; audience fills in the causality
```
The arm sweeping across the frame is a natural cut point, and it's locomotion — the most reliable category.

### Define Liquid Amount with Hard Boundaries
```text
✅ spread about as far as the width of a hand and no further, its leading edge
   a few centimetres short of the base
❌ runs out across the wood in a widening dark sheet
```
"Widening," "spreading" — words without endpoints let H3 keep growing it.
**Principle:** Describe observable boundaries, not abstract processes.

---

## V. Size: Describe Cropping Relationships, Not Fractions

**Rule:** Fractions get ignored. Real test: `wrote about two thirds as tall as the frame` → output was 45–52%.

**Solution:** Change to describing the **composition itself**, which the model can't avoid:
```text
✅  tips of its ears are only a palm's width from the top edge of the frame
✅  its base spills off both left and right edges — no complete bottom visible on either side
✅  the bottom of the frame cuts through just below the front edge of its base
✅  it's by far the largest thing in the frame; everything else is just small detail around it
```
**Result:** 45% → 52% → **69%** (target: two-thirds) in one go.

### Control Secondary Subject Size
To control the size of a secondary subject, "limiting what enters the frame" is more reliable than specifying dimensions:
```text
❌  her open palm is about as wide as the distance between its two ears   → actual was 1.66x
✅  only fingers and the front of her palm are in frame; wrist and back of palm remain outside
```
Show less, and the subject naturally appears larger.

### Vertical Format Has a Geometric Size Ceiling
A subject with **width ≈ height**, fully in frame in 9:16 vertical:
```text
Filling the width → height = 768 ÷ (aspect ratio) ≈ 50–60% of frame height
```
Real tests: 52%, 61%, 61%. **This isn't a prompting issue; it's the aspect ratio limit.**

To go bigger, you **must crop part of it out**. Usually the bottom (base, lower body), since the upper part is narrower and can sit higher in frame:
```text
✅ only its upper part is in the picture: its cheeks reach out past both the left
   and the right edge of the frame, the tips of its ears sit just under the top edge,
   and the bottom edge of the frame cuts straight across its glowing belly so that
   its base is entirely out of shot below
```
**Rule:** "Full body in frame" and "big" are mutually exclusive in vertical format.

### Distance Works the Same Way — Don't Write Units
Fractions get ignored; **distances with units get ignored too.**
```text
❌ a hand's width short of its base
❌ stops about five centimetres away
✅ between the near edge of the pool and its base there is a band of bare dry wood
   as wide as the figurine is tall
```
Same principle: the model can't calculate abstract quantities, but it understands "there's a gap between A and B that's as wide as C."

### Overhead Shots Destroy Characters
From directly above, a character's face, ears, silhouette all disappear, leaving only a color blob; and **without depth reference, size relationships break** (e.g., a coffee mug rendered bigger than a 16cm figurine).

**Fix:** To shoot things on a table, **put the camera at table height looking forward, not looking down.** The face stays, liquid range is foreshortened (doesn't look like a lake), and proportions have reference.

### Three Size Techniques — Use All Three
1.  **Compare to a known object** — about the same size as a woman's hand from wrist to fingertips.
2.  **Absolute dimension** — roughly 16 centimetres tall.
3.  **How much it occupies in frame** — use cropping relationships (see above).

First two ensure **physical correctness**, the third controls **perception**. Using only the first two, the object will be "proportionally correct but looks small."

---

## VI. Shape and Proportions Go to Reference Images

Textual proportions fail consistently.
*   *Test:* Wanted 1.75:1 ratio. Got 0.96 (square).

**Solution:** Feed one reference image; solves it in one go.
```text
Need a specific shape (light panel, screen, display)
  → Make a "blank" reference image: correct shape, rounded corners, edge glow, with empty content
  → Composite content in post
```
**Advantage of blank version:** The model gets **pure geometry, with no content to mess up.**

⛔ **Don't feed images with actual content** (e.g., tarot cards, UI screenshots) — symbols and text will always render as gibberish.

---

## VII. ⛔ Brand Characters Must Not Be Dirty, Broken, or Deformed

Shooting a "ceramic figurine flooded by knocked-over coffee" shot, prompt had `coffee glistening around its base` and `the amber light glowing through the wet film`.
H3 executed, and it **spread upward all over the face** — turning the figurine into a muddy-tear mess.

If that character is a product/brand asset, that shot is unusable, no exceptions.

**The problem isn't the model; it's the prompt.** Any sentence that ties liquid to the character's surface (`on`, `around`, `through`, `soaks into`, `film`) will paint it there, and it will overdo it.

### Fix: Preserve Tension, Sever Contact
```text
❌ coffee glistening around its base, the light glowing through the wet film
✅ a dark pool lies on the wood behind it, a hand's width back from its base,
   holding the amber light as a long reflection across its surface
   (add a positive statement: its cream-white surface is dry and matte all over)
```
Liquid is still in frame, the looming tension remains, the character is clean — and reflections look better than wet film.

**General Rule:** Don't use prepositions that tie "things that stain" and "surfaces that must stay clean" in the same noun phrase. Give them a clear spatial distance.

---

## VIII. ⭐ Decide Camera Position First, Then Write Expression

**Rule:** When the character's object of attention is off-screen, H3 makes them look at the camera.

This is the most common form of the same problem, with two symptoms:
```text
No gaze direction written    →   character talks directly to camera, stage-play style
Gaze direction written       →   but it conflicts with "needing to see the face," model picks one
```

### Three Examples, Same Solution

| Scenario | ❌ Bad Approach | ✅ Good Approach |
| :--- | :--- | :--- |
| **Character looking down at a small object on the table** | Add "lifts head to face camera" — conflicts with "looking at that thing"; lifting head means she can't see it. | **Put the camera at table height, next to the object, looking up.** She looks down at it = looking toward the camera; looking down and showing face are no longer mutually exclusive. |
| **Character talking to someone crouched on the floor** | Write nothing — she faces camera directly, stage-play feeling. | **Put the camera at the crouching person's eye level, looking up.** He's in the foreground, back to camera; she's behind him, looking down at him. |
| **Character watching a TV on the side** | In close-up, no TV visible, gaze not written — looks at camera. | **Put the camera [next to] the TV;** she looks at screen = looking slightly to one side of camera. This is standard interview framing. |

**Same solution in all three: move the camera to where the character is looking.**

### Why "Add an Action" Fails
To show the face, the instinct is to tell the character to turn, lift, face camera. But **the character's posture is usually locked in by the story** — she must look at that thing; that's the point of the scene. Adding a conflicting action creates a contradiction, and the model picks the story one (which is correct) when faced with ambiguity.

> **Rule: When the character's posture is locked by the story, move the camera, not the character.**

### The Writing Order
```
1. What is the character looking at in this shot?
2. Is that thing in frame?
     Yes → write normally
     No → decide camera position first (put it in that direction), write it into the shot description
3. Only then write the expression
```
If step 2 is skipped, everything written later will be ruined by "she's looking at the camera."

⚠️ **Also:** Once the camera position is clear, explicitly state **do not look at camera.** "Looking slightly next to camera" and "looking at camera" are very close to the model; block the latter.

---

## IX. Don't Name Objects That Shouldn't Appear in the Prompt

**Rule:** If H3 mentions it, it tends to render it (phantom objects).

```text
❌  a tall upright rectangle with the proportions of a phone screen held vertically
                                              ^^^^^^^^^^^^ might actually render a phone
✅  use frame boundaries to lock width and height, don't name the object
✅  or feed a reference image (see above)
```
Similarly, metaphors and references must be careful — "like a tarot card proportion" may tempt the model to draw card symbols.

---

## X. The Physiological Order of Emotion

Once beat density is right, facial beats become meaningful. Wrong order produces fake expression:

```text
Genuine smile     Eyes smile first (lower lids push up, crow's feet) → mouth follows
Social fake smile Mouth smiles first, eyes don't move           ← reversing this gives exactly that
Relief            Brow relaxes → exhale → shoulders drop → eyes focus → corners of mouth lift
Suppression       Brows and eyes already leak, mouth holds (delay mouth reaction 0.3–0.5s)
```

**The three layers of micro-expression: brows (first, smallest movement) → eyes → mouth (last, most controllable).**

### Filmable Actions per Emotion

| Emotion | ⛔ Don't Write | ✅ Write (Physical Action) |
| :--- | :--- | :--- |
| **Confused** | confused | inner brows draw down and together, head tilts ~10° to one side, gaze flicks between two points once |
| **Uneasy** | uneasy | blinks slow and heavy, swallows once (jawline pulls), shoulders rise 1cm then drop |
| **Shocked** | shocked | head pulls back 3cm, upper eyelids fully open, inhale leaves shoulders high |
| **Holding back tears** | holding back tears | lower lip tucks in, blinks faster, gaze drifts upward away from the other's face |
| **Conflicted** | conflicted | gaze jumps between three fixed points with different dwell times each, fingers open/close repeatedly, breathing switches nose→mouth |
| **Relieved** | relieved | shoulders drop in one motion, held breath exhales through the mouth corner |
| **Tender** | tender | eyes smile first, mouth slowly follows |
| **Irritated** | irritated | exhale through nose drops shoulders, palm wipes on pants, grabs back of neck |

**Breath is the underlying beat of emotion.** Every emotional segment should have one visible breath — and **holding breath (shoulders stopped high) conveys tension more than any expression**, and the model does it most easily — it's just "not moving."

**Hands are more honest than the face**, but write only the action and contact, not detailed finger shapes (hands are high-risk for extra fingers).

---

## XI. ⛔ Emotional Transition: Don't Let It Happen Continuously On-Screen

Writing "brow relaxes," "smile fades" — **going from state A to state B** — gives the model a start and an end, and it crossfades between them — **the face morphs like rubber.** This is the most common source of "unnatural expression."

### ① Hide the Change Behind Occlusion
Blinking, looking down, a hand covering, a cut — all count. The change happens during the unseen period; when we see the face again, it's already in the new state — the model had no chance to interpolate.

```text
❌ At 00:03.000 the crease between her eyebrows smooths out and releases.

✅ At 00:02.900 her eyes close and stay closed, and her head tips forward
   about five degrees.
   At 00:03.500, with her eyes still closed, her eyebrows come apart and the
   skin between them goes flat.
   [cut]
   At 00:04.300 her eyes open, and they open onto a face that is already loose.
```
This is what real actors do too.

### Even "Design" Can Change, Not Just Expression
Previously, character **design elements** (eyes drawn differently, appearance pinned by a different reference image) were thought to require a cut.
**Real production disproved this.** Within the same shot:
```text
2.25s  eyelids close, each eye becomes a single smooth curved line
3.75s  open — already in a different eye design pinned by a different reference image
       no cut in between
```
So the rule becomes: **it's not that you can't change within a shot; you just can't let it be seen morphing.** With enough occlusion, even design changes work. This saves many shots.

⚠️ **But be careful with writing eye closure.** If the reference image has a "half-closed" variant, writing `its eyelids come down again` might pull toward half-closed, not fully closed. Write the **shape** of closed eyes directly:
```text
❌ its eyelids come down again, slowly this time, and close all the way
✅ its eyes narrow slowly and evenly until each one is a single smooth curved
   line with no part of the eye showing behind it
```

### ② Write a Counter-Move First
Before relaxing, tighten more; before tears, hold them back. **A turn without resistance looks like a switch flipped.**
```text
✅ At 00:02.300 her chin pulls in toward her throat and her lower lip presses up
   hard against the upper one, so that the whole lower half of her face tightens
   further than it already was.
```
The counter-move has another advantage: it's an **action**, not a state change — the model executes it more reliably.

### ③ The Trigger Must Be in the Same Shot or the Immediately Adjacent Shot
If the character turns because of something seen/heard, and the trigger is in Shot 1, but the turn is already complete at the start of Shot 2 — with no beat of her "receiving" it in between — the audience feels the emotion came out of nowhere.

Leave a beat for processing — usually the eye-close or head-drop from ①.

---

## XII. Shot Breakdown Process

```text
Script
 ↓  ① Emotional skeleton      List all turns; mark which is the peak and which is the valley
 ↓  ② Segment                 One segment = one scene or one emotional unit, 5–13 seconds
 ↓  ③ Beat table              Timeline for each segment, one thing per beat
 ↓  ④ Check beat density  ⭐  More than 2–3 facial beats per shot → split; write dialogue if available
 ↓  ⑤ Frame count             Sum of beats + 1.3–1.5s tail room → snap to 17n+5 grid points
 ↓  ⑥ Write prompt
```

**Step ④ is the core of this skill — do not skip it.**
A shot with too many beats will flatten no matter how detailed the expressions are.

### How to Specify Frame Count

| Scenario | Frames | Seconds |
| :--- | :--- | :--- |
| One action, static shot | 124 | 5.17 |
| One action + one camera move | 158 | 6.58 |
| Enter, approach, walk into frame | 192 | 8.00 |
| Action → Reaction → Settle | 209 | 8.71 |
| With cuts | 243+ | 10.13+ |

⚠️ **Always leave 1.3–1.5s tail room.** H3 often degrades into noise blocks in the last 1.2–1.7s, and it's easy to miss in dark scenes. **Check the final frames of every render.**

⚠️ **Enter duration as "slightly below the target seconds with one decimal"** so it gets snapped to the target grid point. Entering the exact desired seconds gives you extra frames — and those extra frames have no prompt → tail degradation.

### Cut Count Trade-Off

> **Cut Count Trade-Off:**
> *   **More cuts** → Higher risk of tail degradation.
> *   **But performance requires cuts** (see §I).
> *   **Decision:** Cut for emotional scenes to gain performance accuracy; keep establishing shots/transitions as single shots.

---

## XIII. Validation: Use Numbers, Not Eyes

Human eyes are fooled by expectation. Extract frames and calculate PSNR — fast and objective.

```bash
# Did the expression happen: extract "before" and "after" frames
ffmpeg -ss 5.2 -i out.mp4 -frames:v 1 a.png
ffmpeg -ss 5.9 -i out.mp4 -frames:v 1 b.png
ffmpeg -i a.png -i b.png -lavfi "[0:v][1:v]psnr" -f null -
```

| PSNR | Meaning |
| :--- | :--- |
| **> 45 dB** | Completely still (frozen frame 60–65 dB) |
| 30–40 dB | Only breathing-level micro-movement ← if this is where emotion should be, it's a fail |
| 18–28 dB | Clear action |
| < 15 dB | Cut or dramatic change |

**Scan PSNR of adjacent frames 0.2s apart; see where the curve's low points are.** Low points should land on emotional beats; if the emotional beat is instead a high point (stillest), that render failed.

### Check Displacement (For Shots That Need Compositing)
```bash
ffmpeg -i a.png -i b.png -filter_complex \
  "[0:v][1:v]blend=all_mode=difference,eq=contrast=7" diff.png
# All black in the area = perfectly still, safe to composite
```

### Measure Coordinates by Printing Profiles, Not Auto-Detection
When there are other glowing elements around the subject, fixed thresholds and gradient detection will misread — **and won't tell you it's wrong.**
```python
cx = 383                              # target horizontal center
for y in range(0, 800, 10):
    print(y, px[cx, y])
```
Features are easy to identify: **the body is a long flat plateau, with one sharp drop at each end; glow is a gradual slope; other glowing elements are isolated narrow peaks.**

---

## XIV. What Audio Reference (`ref_audio_0`) Can Do

H3 can ingest an audio clip as reference, tagged `<Audio 1>`, with the reserved marker `reference`:
```text
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).
<Audio 1>: reference - only the timbre, pitch and delivery are referenced;
           none of its original wording is carried across.
```

⚠️ **The audio waveform does NOT go into the text encoder** — only the `<Audio 1>:` tag does; the waveform goes directly to the DiT. So **describing that audio in the prompt does nothing**; it's just a pointer. Emotion still goes in the `delivery` field.

### Real Test: Can Drive Performance, But Not a Sound Source
Using a 6-second real voice timbre reference to generate a new line:
*   **Voice was generated ✅** Mouth shape, breath, head rhythm all correct.
*   **Reference was absorbed ✅** When connected correctly, pitch moves toward reference.
*   **Pitch still high ❌** Reference 192.8 Hz, generated 222.2 Hz — about two semitones off.
*   **Range still too narrow ❌** Reference span 175 Hz, generated only 117 Hz.
*   **Accent drift ❌** Reference had Taiwanese accent, output still mainland-accented.
*   **Audio quality ❌** Noticeable electronic/synthetic texture.

⚠️ **Connections are easy to get wrong:** Standalone audio goes to `ref_audio_0`, **not `ref_video_audio_0`** (that's for audio from a reference video). Connect wrong and timbre transfer won't happen at all, **with no error message.**

**So the positioning is "performance scaffolding":** Makes mouth shape and breath rhythm more accurate, **but the final track is still recorded separately.**

⚠️ **Accent drift is common across generated speech, not limited to H3.** Whenever the model has creative freedom, accent drifts toward the training data's majority dialect. For a specific accent, use real recordings, or use real recordings for voice cloning.

---

## XV. ⭐ The Final Mile of Performance Is in Editing, Not Prompt Iteration

You'll reach a point where: beats, occlusion, counter-moves — all done correctly, the character actually performs as instructed, **but it still looks fake.**

At that point, stop tweaking prompts. Start editing.

### Why Prompts Can't Save It
**H3 treats each timestamp as a state to "reach."**
It will faithfully place the character in the "shocked" state at 1.700 — but a real human's shock is **anticipatory** (the body is 0.2s faster than the conscious mind), and emotional turns are **discontinuous** (a sudden release), not smooth interpolation.

These two things are exactly what performance needs, and H3's architecture doesn't do them.

### Two Symptoms, Two Cuts

**Symptom 1: Reaction is half a beat slow**
The stimulus appears; the character reacts a second later. That one-second blank is what reads as "fake."
```text
Cut: Remove the blank; cover it with an insert shot

  A  Calm, stimulus just appeared
  B  ★ Cut to insert shot (close-up of that stimulus)
  C  Cut back, character is 【already reacting】

The audience never sees the "start of reaction" moment; their brain fills it in —
and what they fill in is faster and more real than anything acted.
```

**Symptom 2: Turn is too smooth**
Both ends of the emotion are actually rendered, but the middle is a continuous gradient, and the audience **has no comparison point** — they only feel "the expression slowly changed."
```text
Cut: Bring the two ends closer; insert one cut in between

  A  One end of the emotion (peak of tension)
  B  ★ A short insert shot
  C  The other end (already released)

A 3.7s gradient becomes just a 1s insert apart.
Same footage, completely different reading.
```

### What to Film to Leave Room
```text
✅ Shoot longer              Gives editors room to trim blanks
✅ Must have insert shots    That's the material for cuts; without them, can't cut
✅ Film both ends of the emotion fully   The middle can be discarded; the ends cannot be skimped
❌ Don't keep tweaking prompts for rhythm
```
Insert shots are already needed (to establish space, give audience breathing room), so "leaving room for editing" has almost no extra cost.

⚠️ **Real example:** Two shots from one scene went through four prompt revisions each without fixing the issue; on the same day, applying both cuts above solved each in one try. **Four revisions cost far more than one edit.**

---

## XVI. Division of Labor with Post-Production

Some things **should never be given to H3**:

| Item | Why |
| :--- | :--- |
| Screen content (phone, TV, tablet) | UI text will always be garbled |
| Brand assets (cards, logos, packaging) | Symbols will be corrupted |
| Anything requiring precise text | Same as above |
| Pauses and freeze frames | Generation is uncontrollable; editing is 100% controllable |

**Screens: "give brightness only, no content"** — write "even cool white light," composite content in post.

⚠️ **ffmpeg alpha fade for still images MUST use `-loop 1`;** otherwise, a single-frame image's PTS stays at 0, alpha stays at its starting value forever, **entirely transparent with no error.** This silent failure is the hardest to debug.

```bash
# ❌ Overlay never appears, no error
ffmpeg -i base.mp4 -i card.jpg -filter_complex \
  "[1:v]scale=W:H,format=rgba,fade=t=in:st=2:d=0.7:alpha=1[c];[0:v][c]overlay=X:Y"

# ✅
ffmpeg -i base.mp4 -loop 1 -framerate 24 -t <duration> -i card.jpg -filter_complex \
  "[1:v]scale=W:H,format=rgba,fade=t=in:st=2:d=0.7:alpha=1[c];[0:v][c]overlay=X:Y"
```

---

## XVII. Reuse Across Episodes

For series with fixed rituals or transitions, **shoot them as reusable assets**:
```text
No episode-specific elements (props, card faces, dialogue)
No protagonist's full face (only hands)
Leave room for post-production compositing
```
Shoot once, reuse every episode. It saves not just compute but **consistency** — the same ritual looks identical every time, which is branding in itself.

---

## XVIII. 🚑 Diagnosing Flat/Wooden Performance (Checklist)

If the character looks stiff or the performance is flat, check in this order:

1.  **Beat Density Check** → More than 2-3 facial beats per shot? *(Most common cause)*
2.  **Gaze Direction Check** → Is the character looking off-screen without camera repositioning?
3.  **Breath Check** → Did you include a visible breath in the emotional segment?
4.  **Transition Check** → Did you write "A changes to B" instead of hiding the morph?
5.  **Dialogue Check** → Did you put physical beats inside a dialogue shot?

**Fix in this order:**
`Beat density` → `Camera position` → `Breath` → `Occlusion` → `Dialogue placement`

---

## XIX. Official `<d>` Spec Warning

**Official Spec Reminder:**
*   Identifier, ID, action, and delivery are all **outside** `<d>`.
*   `<d>` contains **ONLY**: language tag + verbatim dialogue.
*   Emotion goes in the **delivery field**, not inside `<d>`.

Example Structure:
```text
[Identifier] [ID] [Action], [Delivery], says in [Language]: <d>[Language Tag] [Verbatim Dialogue]</d>
```