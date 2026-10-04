# MiniMax H3 — Micro-Expressions & Acting (prompting guide)

Source: r/StableDiffusion "Pushing AI emotions is possible through..." (2026) + the
official H3 R2V reference style. This is how to make Jaisal's face *act* — not just
pose — in the intro.

## The core idea: acting = VISUAL micro-expression + AUDIO emotion tags, fused

The post's key lesson: a good acting beat is **one fused sentence** that describes
the subtle facial movement *while* the line is delivered, with audio emotion tags
inside the dialogue. NOT a separate "he looks sad" note.

> "he starts to cry, desperately sobbing as he's delivering the next lines, his
> eyes watering a little bit. <Subject 1> (S1) says, <d>[English, crying] <pants>
> Maybe all you... <stutter> wa wanted is to to to break me! <catches breath> ...</d>"

Two channels working together:
1. **Visual** (in `detailed_description`): the eyes, the breath, the micro-movement.
2. **Audio** (inside the `<d>` dialogue): the emotion tags that shape the delivery.

## Rule 1 — LEAD WITH THE EYES

The eyes are the primary micro-expression channel. Always describe what the eyes do
*before* the bigger movement:
- "His eyes shift first. His head begins to rotate SLOWLY 180°..."
- "his gaze drops to the plant, then back up"
- "his eyes water a little"
- "his eyes follow the stem as it pushes through the table"

For our head-twist shot (C), the eyes leading the head IS the hook. Keep it.

## Rule 2 — FUSE the micro-expression with the action/dialogue

Don't write "he looks uncertain." Write the micro-expression *inside* the action:
- "a small breath catches as he sits, his eyes still wary"
- "he breathes out slowly, his shoulders dropping, as the plant bends"
- "a faint, wry half-smile as he looks at the strange objects"

## Rule 3 — Dialogue format: `<d>[Language] ... </d>`

Wrap spoken lines in `<d>` with a language tag. Emotion tags go INSIDE:

```
<Subject 1> (S1) says, <d>[English] <breath> I don't know what to say. <pause>
I don't know where to start. <long pause> But... this is where I start. <inhale>
So welcome to the Jaisal Kut. </d>
```

The language tag (`[English]`, `[Malayalam]`, `[English, crying]`, `[English,
singing]`) tells the model which voice/delivery to use.

## Rule 4 — Audio emotion tags (the working set)

| Tag | Effect | Example |
|---|---|---|
| `<pause>` | short pause | `Okay. <pause> This is just me talking.` |
| `<long pause>` | longer pause | `I mean... <long pause> I don't even know.` |
| `<breath>` | breathing sound | `And then... <breath> it just happened.` |
| `<inhale>` / `<exhale>` | in/out breath | `<inhale> Alright, let's do this.` |
| `<catches breath>` | out of breath | `Wait... <catches breath> hold on.` |
| `<deep breath>` | calming down | `<deep breath> Okay. I can do this.` |
| `<i>word</i>` | emphasize 1-4 words | `I was <i>not</i> expecting that.` |
| `<whisper>…</whisper>` | whisper delivery | `<whisper> Don't tell anyone.</whisper>` |
| `<humming>…</humming>` | humming a tune | `<humming> da-da-da.</humming>` |
| `<laughs>` / `<chuckle>` | laughing | `That's... <laughs> actually funny.` |
| `<sighs>` | sigh | `<sighs> I really tried.` |
| `<uh>` | filler / hesitation | `So, like... <uh> what was I saying?` |
| `<stutter>` | stutters the words | `<stutter> I ca can't believe that.` |
| `<gasp>` | sharp intake | `<gasp> Oh my God.` |
| `<coughs>` | cough | `<coughs> Sorry, one sec.` |
| `<clears throat>` | throat clear | `<clears throat> So anyway...` |
| `<sniff>` | sniffing | `<sniff> It's just... really sad.` |
| `<smacks lips></smacks lips>` | lip smack | `<smacks lips></smacks lips> Okay.` |
| `<pant>` / `<pants>` | panting | `Run... <pants> run now!` |
| `<softer>` | quieter delivery | `<softer> I don't think I can say it.` |
| `<mhm>` | agreement sound | `Yeah, <mhm> exactly.` |
| `<phew>` | relief | `<phew> That was close.` |

**NO MUSIC rule (D041):** `<humming>` and any melody tag are MUSIC-adjacent — do NOT
use them in the intro (the user is Muslim, no music). Use only the natural-speech
tags (`<breath>`, `<pause>`, `<sighs>`, `<i>`, `<stutter>`, `<catches breath>`,
etc.).

## Rule 5 — Audio direction lines

Add a short direction for the voice's space/quality:
- "Quiet empty space around his voice."
- "in a low, tired voice, close to the mic"
- "his voice is small, almost to himself"

## Rule 6 — Melody / humming needs a REFERENCE AUDIO (not our case)

The post feeds a recorded melody via the `ref_audios` input (`<Audio 1>` tag) and
says "hums the melody of <Audio 1>". The R2V node has a `ref_audios` input for
this. **We do NOT use this** (no music, D041) — noted for completeness.

---

# Applying it to OUR intro (per-shot micro-expressions)

Our intro is B&W, Jaisal speaks Malayalam. The VISUAL micro-expressions below apply
regardless of the audio path. The `<d>` dialogue tags apply ONLY if we use MiniMax's
native audio (see the audio-path decision below).

| Shot | Jaisal's line | Micro-expression to prompt |
|---|---|---|
| **A** walk-in | "Let's start." | enters wary, eyes scanning the dark room; a small breath as he sits; a quiet, determined set to his jaw. |
| **B** setup | "Let's start." (EN placeholder) | **SMIRK only** (NOT a full smile) at one corner of the mouth as his hands rise to the table edge; eyes soften slightly; a quiet breath; then he says his line `<d>[English] <breath> Let's <i>start</i>. </d>`; the smirk fades to a calm settled look. |
| **C** the start | **ENGLISH** (dub Malayalam later) | **THE HOOK — "GENUINELY STARTING"** (`jaisal_intro_C_starting_2ref.json`, 2-ref R2V). **The 180° twist is DROPPED** (D086) — the opening is now awkwardly simple: Jaisal is seated (frontal, B's last frame), looks at the camera. **Camera = SMOOTH ROUND TRIP** (frontal → orbit left to ~90° → back to frontal); **FINAL FRAME = FIRST FRAME** (frontal) → seamless cut to shot D. Head follows the camera the whole way (body stays dead still). **CINEMATIC BLOCKING** (5 phases: STILL / ORBIT OUT / LEFT SIDE ~90° / ORBIT BACK / WELCOME) + **PER-SECOND TIMELINE** (10s): 0-1s still + eyes shift + "I don't know what to say"; 1-2s pause; 2-3s camera begins orbiting + "I don't know where to start"; 3-5s head slowly follows; 5-6s camera at his left side (~90°); 6-7s head ~90° into lens + "But... here we start"; 7-8s camera begins returning; 8-9s head follows back; 9-10s camera back at front + "Welcome to the Jaisal Kut" (final frame = first frame). **Micro-expressions:** eyes shift FIRST, gaze holds the lens, quiet natural delivery, clear LIP MOVEMENT. **Background = PURE BLACK VOID** (locked per-second). NO glitch, NO horror, NO 180° twist. 240 frames (10s). See D086. (180°-twist versions — 3-ref R2V, camera node, 2-step — kept as alternatives.) |
| **D** listening (reverse dropped, D089) | (camera guy OFF-SCREEN) | **4s take (96f).** The camera guy's line is an OFF-SCREEN male voice — MiniMax generates it: `<d>[English] <breath> What's the purpose of this channel? </d>` at [1-2s]. Jaisal does NOT speak — he only REACTS: eyes shift, small thoughtful expression, quiet breath, tiny natural head movement. Per-second timeline: [0-1s] still; [1-2s] off-screen question; [2-3s] listening reaction; [3-4s] quiet breath + subtle reaction. Camera COMPLETELY STILL. **Technique (v4, 2026-09-16): use a `<Subject 2>` tag for the off-screen voice ("calm adult male voice, NOT visible in the frame, only his voice is heard, NOT the boy") so H3 sees TWO distinct speakers — a custom `<Off-screen voice>` tag gets IGNORED and the line falls to the only visible person (the boy talks). Tie the `<d>` line to `<Subject 2>`, and HARD-lock the visible character's lips closed (visual description + negatives: `the boy speaking, the boy's mouth open, lip movement`). Keep reaction shots SHORT (4s) — idle time makes H3 hallucinate speech.** |
| **E** plants grow | "No real purpose. Just telling stories." | wonder — his eyes follow the stem as it pushes through; a slight, softening smile; a small breath of surprise. |
| **F** plants die | "Cinema... you need effort... I'm alone... limitations." | the weight of limitation — a slow breath, his gaze dropping to the plant, a subtle frown, shoulders dropping; the "you need effort" delivered with a `<pause>`. |
| **G** vanish | "stories, politics, sports... I don't know if it'll work... Let's see." | a faint, wry, honest half-smile as he looks at the strange objects; a small shrug; then he vanishes. |

## The audio-path decision (IMPORTANT)

Two ways to get Jaisal's voice in the intro:

**Path 1 — MiniMax NATIVE audio (the post's method):**
- Put the dialogue in the prompt as `<d>[Language] ... </d>` with emotion tags.
- MiniMax generates the voice + lip motion natively.
- **Pros:** simplest (no separate VC + lip-sync), the emotion tags work, the face
  and voice are synced by the model.
- **Cons:** the voice is a GENERIC MiniMax voice, NOT the user's voice. Malayalam is
  likely weak (MiniMax is English-leaning). For a Malayalam intro this is a real
  limitation.

**Path 2 — VC + LatentSync (our existing plan, D050):**
- The user dubs the Malayalam lines → RVC/OpenVoice converts to the target voice →
  LatentSync lip-syncs the H3 video to that audio.
- **Pros:** the user's ACTUAL voice, correct Malayalam pronunciation.
- **Cons:** more pipeline steps (dub → VC → LatentSync → DaVinci).

**Recommendation for the intro:** the VISUAL micro-expressions (Rules 1-2) apply in
BOTH paths — always prompt them. For the VOICE, decide per-shot:
- If a shot's line is short and English is acceptable → Path 1 (native `<d>` tags)
  is faster.
- If the line is Malayalam and must sound like the user → Path 2 (VC + LatentSync).

**DUB-PLACEHOLDER STRATEGY (user decision 2026-09-14):** the user will DUB the
dialogue in Malayalam later. So for now, prompt the lines in **ENGLISH** (the
script's English lines) via native `<d>[English] ... </d>` tags — this gives the
model mouth movement + timing to dub over. The English audio is a PLACEHOLDER; the
final Malayalam dub replaces it (Path 2: VC + LatentSync). Example (shot B):
`<d>[English] <breath> Let's <i>start</i>. </d>`.

**MALAYALAM NATIVE TEST (2026-09-14, shot B):** the user wants to test whether
MiniMax H3 can SPEAK Malayalam directly. Shot B now uses the Malayalam line
`<d>[Malayalam] <breath> തുടങ്ങട്ടെ </d>` ("Let's start"). **Judge the result:**
- If MiniMax speaks it cleanly → use native Malayalam audio directly (skip the dub).
- If it mangles it → fall back to the English placeholder + Malayalam dub (Path 2).

## Settings note (the post vs us)

The post uses: 30 steps, First Block Cache (0.08, 25% start), res_multistep
sampler, sage2++ attention, NO LoRA, 480p/720p, a custom FL2VA→REF2VA FP8 finetune.
We use: turbo 4-step LoRA + SLA (our speed stack, D014). The **prompting technique
is identical** — the acting comes from the prompt, not the settings. We keep our
speed stack; we adopt the prompting technique.
