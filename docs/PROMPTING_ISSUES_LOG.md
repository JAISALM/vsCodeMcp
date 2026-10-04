# H3 R2V — Prompting Issues Log

A running log of the **prompting problems** we hit with MiniMax H3 (ref2va) on the
Jaisal Cut intro, **why they happened**, and **how we overcame them**. Re-read this
before writing a new H3 prompt so we correct ourselves instead of repeating the
same mistakes.

> Scope: MiniMax H3 R2V (`MiniMaxH3ReferenceToVideo`, ref2va model). The general
> 6-section structure + reference-tag rules live in
> `docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md`. This file is the **lessons-learned**
> layer on top of it.

---

## Issue 1 — Off-screen voice gets attributed to the visible character (character starts talking)

**Symptom:** an off-screen line (e.g. the camera guy asking a question) made the
ONLY visible person start TALKING.

**Root cause:** the prompt used a **custom** `<Off-screen voice>` tag. H3 does NOT
recognize custom subject tags, so the single `<d>` line fell to the only visible
person in frame.

**Fix:**
1. Define the off-screen voice as a proper **`<Subject 2>`**: "a calm adult male
   voice (the camera guy). NOT visible in the frame - only his voice is heard,
   coming from OFF-SCREEN. NOT the boy."
2. Define the visible character as **`<Subject 1>`**: "the ONLY person VISIBLE in
   the frame. does NOT speak - his lips stay CLOSED the entire shot."
3. Tie the `<d>` line to `<Subject 2>`.
4. HARD-lock the visible character's lips in the visual description + per-second
   timeline.
5. Negatives: `the boy speaking, the boy's mouth open, the boy's lips moving, ...`.

**Rule:** for an off-screen voice, use a `<Subject 2>` tag (two distinct speakers)
+ tie the `<d>` line to it + hard-lock the visible character's lips. A custom tag
gets ignored.

**BUT — see Issue 2: this was NOT enough.**

---

## Issue 2 — H3 animates the visible person's mouth whenever ANY dialogue line is present

**Symptom:** even with the `<Subject 2>` off-screen voice + "lips stay CLOSED"
lip-lock, H3 STILL animated the visible boy's mouth (take
`jaisal_intro_D_reverse_00004_` = lip-sync / the boy appears to talk).

**Root cause:** H3 moves the **visible** person's lips whenever ANY `<d>` line is
in the prompt. An off-screen `<Subject 2>` tag + lip-lock wording does NOT hold
the only visible person's lips closed — the model sees a dialogue line and animates
the person it can see.

**Fix:** **REMOVE the in-video dialogue entirely** (no `<d>`, no `<Subject 2>`).
The character becomes a pure silent listener/reactor. The line is **dubbed in
post** (Midhun voice, D055/D089/D090).

**Rule:** when the visible character must NOT talk, REMOVE the dialogue from the
video (pure silent reaction) and DUB the line in post — do NOT rely on an
off-screen-voice tag or lip-lock wording to hold the visible person's lips closed.

**BUT — see Issue 3: removing the dialogue was STILL not enough.**

---

## Issue 3 — H3's audio prior leaks speech-like GIBBERISH even with NO dialogue

**Symptom:** with the dialogue removed (pure silent reaction), H3 still produced
**speech-like gibberish** (not our line — just mouth-sound / talking-like audio).

**Root cause:** H3 has an **audio prior** — a person facing the camera = talking.
So even a "silent" shot leaks speech-like audio. A prompt-only silent lock helps
but is NOT guaranteed.

**Fix (two layers):**
1. **HARD SILENT-AUDIO LOCK** in the prompt (per the guide's "No dialogue/text if
   not wanted" rule): `overall_soundscape` = "COMPLETE SILENCE except a faint
   ambient bed… NO human voice, NO speech, NO talking, NO words, NO gibberish";
   `non_diegetic_music` + negatives forbid ALL voice/speech/words/gibberish/vocalization.
2. **GUARANTEED — strip the H3 audio in post.** The line is dubbed in post anyway,
   so the H3 audio is throwaway:
   ```
   ffmpeg -i <take>.mp4 -an -c:v copy <take>_silent.mp4
   ```
   then build the audio track in post (ambient bed + Midhun dub).

**Rule:** a prompt-only silent lock helps but is NOT guaranteed to stop H3's speech
prior — for a silent-character shot, **STRIP the H3 audio in post** and build the
audio track in post.

---

## Issue 4 — The NARRATIVE CONCEPT of "listening/reaction" triggers speech-like facial motion

**Symptom:** even with no dialogue + a hard silent-audio lock, the boy's mouth
still moved. The prompt said "He is LISTENING to an off-screen question" and
"the question is NOT heard in this take" and "his mouth stays CLOSED" — that
*should* work, but H3 is a video-generation model and **speech-like facial motion
can be triggered by the narrative concept of "listening/reaction."**

**Root cause:** (a) the *concept* of listening/reacting to a question primes the
model toward a talking face; (b) if the **reference image** has the mouth slightly
open/neutral, H3 animates it.

**Fix (GPT's diagnosis, adopted 2026-09-20):**
1. **Remove the off-screen-question concept ENTIRELY.** Since the dialogue is
   added in post anyway, there is no reason for the model to know he's answering
   anything. The shot is just "a quiet natural moment."
2. **Make the shot AGGRESSIVELY non-speaking** — a dedicated `CRITICAL PERFORMANCE
   RULE` block (mouth FULLY CLOSED first-to-last frame, lips/jaw completely still,
   teeth never visible, no lip-sync, no mouth words, no whisper, no speech sounds,
   no talking-like facial movement) + a comprehensive speech-movement negative.
3. **Do NOT use "young boy"** if the character is an adult/young man — "young boy"
   can cause undesirable facial behavior and identity drift. Use **`<Subject 1>`**
   and let the **reference image** define the person.

**Rule:** for a silent shot, remove the listening/reacting-to-a-question concept
entirely, make the non-speaking instruction AGGRESSIVE (dedicated rule block +
strong negative), and define the person via `<Subject 1>` + the reference image
(not a "young boy" descriptor).

**Applied:** `jaisal_intro_D_reverse.json` node 138, via
`utilities/fix_shot_D_silent_v3.py` (validates clean 0 errors).

---

## Issue 5 — Idle time in a take = hallucinated speech

**Symptom:** a 7.3s reaction shot had too much idle time → MiniMax hallucinated
speech ("gibberish out of nowhere").

**Root cause:** idle time gives the model nothing to do, so it fills the gap with
speech.

**Fix:** keep reaction shots **SHORT (4s)** and give the model an explicit
per-second timeline so it has nothing to fill.

**Rule:** keep reaction/listening shots short (4s) + a per-second timeline.

---

## Issue 6 — Asking H3 to render TEXT in a face shot distorts the face

**Symptom:** the in-video white "The Jaisal Kut" title flash DISTORTED THE FACE
(shot C).

**Root cause:** asking MiniMax to render text + hold a face + speak at once is too
much pressure; the face suffers first (model attention goes to the text).

**Fix:** keep the video **TEXT-FREE**; add any title in **POST** (take the last
frame → add text in a new image → post effect over the clean video).

**Rule:** do NOT ask MiniMax to render text in a face shot — it distorts the face.
Keep the video text-free; add any title in POST.

---

## Issue 7 — H3 "corrects" the camera back to a flattering eye-level view

**Symptom:** a strong camera angle (overhead/low-angle) silently reverts to
eye-level; the common cheat is to keep the camera at eye level and just tilt the
subject's head.

**Root cause:** H3 has a strong internal prior to "correct" the camera toward a
flattering eye-level view, especially when a face is in frame.

**Fix:**
1. Put the camera constraint at the **absolute top** (`MANDATORY SHOT CONSTRAINT,
   HIGHEST PRIORITY ABOVE ALL ELSE: ...`).
2. **Accept the natural distortion** that angle causes ("ACCEPT NATURAL [ANGLE]
   PERSPECTIVE DISTORTION").
3. **Forbid the camera cheat** with short hard negatives (`NO eye-level shot`,
   `FORBIDDEN: flat frontal camera`).
4. Keep the reference's identity but **discard its camera**.

**Rule:** to force a camera angle in H3, put the constraint at the top, accept the
natural distortion, forbid the camera cheat with hard negatives, discard the
reference's camera, and give the subject an explicit action chain + NOT-list.

---

## Issue 8 — H3 DROPS the last shot of a multi-shot R2V

**Symptom:** in a 3-shot R2V, MiniMax DROPPED Shot 3 entirely.

**Root cause:** without an explicit demand, the model compresses/drops the final
shot.

**Fix:** add a hard line in BOTH the summary and the per-shot line: "ALL THREE
shots must appear in this order, each getting its full time - do not skip,
compress, or drop any shot, especially [Shot 3]."

**Rule:** when a shot has a specific job, state it as a HARD REQUIREMENT in BOTH
the summary and the per-shot line, and explicitly forbid the failure modes
(cut short / turned into a close-up / skipped).

---

## Issue 9 — "runs" look like a sliding keyframe

**Symptom:** a running character looks like a smooth slide/glide, not a real run.

**Root cause:** without an explicit gait description, H3 interpolates a slide.

**Fix:** specify **SLOW + DELIBERATE + step-by-step** ("each foot clearly LIFTS
and LANDS separately, visible leg movement, one step at a time, NOT a smooth
slide, NOT a glide, NOT a blur").

**Rule:** MiniMax "runs" look like a sliding keyframe unless you specify SLOW +
step-by-step + distinct footfalls.

---

## Issue 10 — Left/right ambiguity

**Symptom:** "he turns to his right" made MiniMax pick the wrong side.

**Root cause:** ambiguous "his right" — the model doesn't know whose perspective.

**Fix:** ALWAYS specify left/right from the **VIEWER's perspective** ("the boy's
RIGHT side is the VIEWER'S LEFT side of the frame"). Anchor the camera to a fixed
side and say it TRACKS the subject.

**Rule:** always specify left/right from the VIEWER's perspective in R2V prompts.

---

## Issue 11 — Object duplication / unwanted items persist

**Symptom:** the model duplicates objects (2 bats, 2 balls) or keeps items you
want gone (extra papers).

**Fix (three levers):**
1. **Explicit counts** in the prompt: "exactly ONE cricket bat", "exactly ONE
   round soccer ball".
2. **Lead with the removal**: "REMOVE ALL the floating papers EXCEPT ONE single
   sheet. There must be exactly ONE sheet of paper left."
3. **Duplicates in the negative**: `second bat, two bats, multiple bats, ...`.
4. **Pin positions explicitly** ("the ball rests on the table", "the bat stands
   vertically, balanced on top of the ball").
5. If it still duplicates after a correct prompt → **re-roll the seed** (sampling
   variance, not a prompt problem).

**Rule:** unnamed counts get duplicated; lead with the removal; pin positions;
re-roll the seed if it's sampling variance.

---

## Issue 12 — Character-vanish shots: the identity prior keeps the person

**Symptom:** describing "papers behind the man" / "the man sits still" kept the
man as the permanent subject — the character STAYS.

**Root cause:** the identity/reference workflow is strongly biased toward
**preserving the person**.

**Fix (ABSENCE-FIRST):**
- **Open with the absence**: "Remove the man completely. There is NO PERSON
  remaining in the final image."
- **Keep the scene identical** (same table/chair/room/bulb/camera/lighting; the
  chair is now EMPTY).
- **Describe a PHYSICAL burst, not a dissolve** ("papers violently erupt from the
  exact space where the man was sitting").
- **End with a hard FINAL STATE line**: "empty chair + explosive cloud of loose
  papers. Absolutely no human figure."
- **Negative lists the person explicitly**: `man, person, human, face, head, body,
  ...`.
- If the man still appears: drop `ref_boost` to ~2-3 (or ~1.5) and/or re-roll the
  seed.

**Rule:** for a character-free frame, make the ABSENCE the primary instruction
(open with it, keep the scene identical, physical burst not dissolve, hard final
state, person in the negative).

---

## Issue 13 — Continuation/listening shots drift INTO the anchor pose

**Symptom:** a continuation shot DRIFTED TOWARD the reference (the boy moved into
the pose over the shot) instead of STARTING on it.

**Root cause:** the prompt said "settles into" / "moves to" the pose, so H3
animated a transition INTO the anchor.

**Fix:** the prompt must say the subject is **ALREADY in the pose from frame 1**
("ALREADY seated in the FIRST frame, exactly as in <Picture 1>; he does NOT move
into this pose"). Same-frame start+end anchors lock the pose.

**Rule:** for a continuation/listening shot, the subject is ALREADY in the pose
from frame 1 (not "settles into" it) — otherwise H3 animates a transition into the
anchor.

---

## Issue 14 — Locking the last frame to the SAME image reads as frozen

**Symptom:** locking the last frame to the same image (ref_image_0 = ref_image_1)
made the shot read as a frozen "same old image."

**Fix:** use **FIRST REF ONLY** (the previous shot's last frame as `ref_image_0`
only) + subtle micro-expressions + a **NATURAL ending** (not locked to the same
frame). Then grab the natural last frame with `seedvr2_lastframe_2k.json` for the
next shot.

**Rule:** for a continuation shot, use FIRST REF ONLY + micro-expressions + a
NATURAL ending — do NOT lock the last frame to the same image (feels frozen).

---

## Issue 15 — Idle/neutral reference mouth gets animated

**Symptom:** if the **reference image** has the mouth in a slightly open/neutral
state, H3 animates it (even in a "silent" shot).

**Fix:** pick a reference where the mouth is clearly CLOSED; reinforce "mouth
completely closed, lips completely still" in the prompt + negative.

**Rule:** check the reference image's mouth state — a slightly open/neutral mouth
in the ref gets animated by H3.

---

## Quick checklist for a SILENT-character shot (no talking)

1. **No `<d>` line, no `<Subject 2>`** — remove the dialogue from the video
   entirely (dub in post).
2. **Remove the listening/reacting-to-a-question concept** — the shot is just "a
   quiet natural moment."
3. **Define the person via `<Subject 1>` + the reference image** (not "young boy").
4. **AGGRESSIVE non-speaking block** (mouth FULLY CLOSED first-to-last, lips/jaw
   still, teeth never visible, no lip-sync/whisper/speech sounds) + comprehensive
   speech-movement negative.
5. **HARD SILENT-AUDIO LOCK** (`overall_soundscape` = ambient only, NO voice/speech/
   words/gibberish; `non_diegetic_music` + negatives forbid all voice).
6. **Check the reference image's mouth** is clearly closed.
7. **Keep it SHORT (4s)** + a per-second timeline.
8. **GUARANTEED: strip the H3 audio in post** (`ffmpeg -an`) and build the audio
   track in post (ambient + dub).

---

## Quick checklist for a SPEAKING-character shot

1. Use `<d>[Language] ... </d>` with emotion tags (`<breath>`, `<pause>`, `<i>`).
2. Assign the line to the correct `<Subject N>` (the VISIBLE speaker).
3. Lead with the eyes; fuse the micro-expression with the action/dialogue.
4. Keep the shot long enough for the line but not so long that idle time
   hallucinates extra speech.
5. NO MUSIC (D041) — `non_diegetic_music` = natural sounds only.
