# Shot Language — Author's Cheat Sheet (2026-11-23)

**You do NOT need to learn cinematic language to direct. You give rough words or a
screenshot; the agent builds the blockout; you correct it visually; the agent
writes the "good prompt" (H3 / Krea2 / Blender spec) from the locked blockout.**

## The loop

```
your rough words (5 questions below, or a screenshot)
        ↓
agent builds GRAY BLOCKOUT in Blender (boxes + camera + light)
        ↓
thumbnail strip (4–8 frames / turntable)
        ↓
YOU CORRECT: "camera too low" · "grave closer" · "sky bigger" · "boy on the left"
        ↓
LOCKED blockout
        ↓
agent generates from it: H3 R2V prompt · Krea2 reference set · measured camera
```

**Correction beats description.** Saying "move the boy left" is easier than
describing the composition. The blockout is the shared language — boxes + camera
+ light carry scale/position/height/mood, which words are bad at.

## The 5-question shot brief (plain words are fine)

| # | Question | Examples |
|---|----------|----------|
| 1 | Who/what is in frame? | "the boy + the bandicoot" · "empty well" |
| 2 | Where? | "grave pit (L04)" · "bridge, early morning" |
| 3 | What are they doing? | "he looks down, holds it tight" · "nothing — it's empty" |
| 4 | How big / from where? | "wide, from above" · "close on his hands" · "low, looking up" |
| 5 | One feeling word? | heavy · lonely · warm · tense · quiet |

Can't answer #4 in words? **Send a screenshot** of any film frame / photo that's
"close to it" — the image answers #4 for you. Reference images are the
strongest channel you have (stronger than any prompt): Krea2/H3 can use them
directly (identity-edit, R2V refs); for blockouts the agent builds the
arrangement to match them.

## The 30 words that cover 95% of shots (optional — you never HAVE to use these)

**Shot size:** extreme close (eyes/hands) · close (face) · medium (waist up) ·
wide (full body + space) · very wide (world, tiny person)
**Camera height:** low (looking up = big/powerful) · eye level (neutral) ·
high (looking down = small/vulnerable) · bird's eye (map view)
**Movement:** still · slow push-in (feels closer to the emotion) · slow pull-back
(lets them go) · pan (follow sideways) · follow (walks with them)
**Light:** golden hour (warm, end of day) · overcast flat (1950s village default) ·
candle/lamp (night interior) · moon (cold night) · backlight silhouette
**Lens feel:** wide lens = space + exaggeration at edges · telephoto = compressed,
lonely, faces pushed together
**Scale trick:** small person in a big frame = loneliness; fill the frame with
the face = intimacy

## What the agent needs from you — nothing else

- The 5 answers (or a screenshot + "like this but our village")
- Which env card (L01–L08) · which character
- One word on pace: slow / sudden / quiet

Everything else (blockout, camera numbers, H3 6-section prompt, Krea2 ref
prompts, measured camera after generation) = agent-generated, you approve or
nudge. The "good prompt" is never your job to write.

## FaceFix note (2026-11-23)

`PixelAI_H3_FaceFix` = **fallback stage** — used for movie shots only when H3
doesn't nail the face properly (far-face melt, identity drift). First pass is
always the normal H3 shot; the face fix is the cheap post-fix (no re-render,
audio kept).
