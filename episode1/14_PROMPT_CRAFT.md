# 14 — PROMPT CRAFT & NATURALITY SYSTEM (2026-11-28)

**Author diagnosis (11-28):** naturality in our clips will be lost **due to lack of prompts,
not technicality**. Correct — the tech is proven (pose test moved the body, FaceRefine
held the face; `k2f_*` multi-pass was rejected for drift = under-specification, see
PENDING_ITEMS DO-NOT-RUN). An AI video model fills every UNSPECIFIED slot with its prior:
generic "AI look", one-shot robotic action, stock compositions, characters stacked or
duplicated. **Naturality = specificity discipline, not more nodes.** This doc is the
standing craft standard for every character shot (Krea2 character images AND H3 R2V).

---

## THE SIX RULES (naturality system)

1. **ONE physical action chain per shot — body parts + object + direction + tempo.**
   Never "he looks thoughtful" (abstraction → stock freeze). Instead:
   "he lifts his wrist, glances at the watch, holds it for a beat, lets the arm drop."
   Models animate concrete physical chains; they cannot animate adjectives.
2. **BEAT STRUCTURE — action → hold → follow-through.** Natural performance has micro-beats.
   A single action reads as a robot; a chain with a hold reads as a person.
   `[action]` → `[1–2 s hold with a micro-detail]` → `[reaction / follow-through]`.
3. **COUPLE character to environment IN THE SAME SENTENCE.** Behaviour tied to the world:
   "footprints sinking into the red mud" · "wind lifting the hair" · "mud speckling the kit"
   · "breath faintly visible in the dawn cold". One shared sentence = one scene, not a composite.
4. **SPECIFY THE NEGATIVE SPACE — what the character is NOT doing.**
   "eyes on the field, not the camera" · "hands in pockets" · "no one looks at the camera."
   Prevents the default-pose prior.
5. **EXPLICIT SPATIAL LAYOUT for every multi-character shot.**
   "Zidhan left of frame facing right, Jaisal centre with his back half-turned, the boy
   right of frame, two paces apart." H3 needs the layout stated per reference — otherwise
   it stacks, merges or duplicates figures. (Krea2 duplication quirk: character images
   always say "ONLY ONE character, no other people, no duplicates.")
6. **HUMAN IMPERFECTION BLOCK — standard closer for every character shot:**
   "weight shifting, a glance down, mid-blink, uneven natural gait, small wasted motions —
   real people, not a posed photograph." + the D041 audio block (natural ambience ONLY,
   no music/instruments/melody/beat).

## WHAT NOT TO DO (our own failure history)

- **500-word essays confuse the model (D020).** Specificity ≠ length. Target **60–120 words**
  of action/craft per shot, on top of the verbatim environment block (3-layer rule, `13` doc).
- **Never describe a pose as a fresh action** ("looking at the sky" makes the model re-pose)
  — anchor to the reference: "EXACTLY matching the reference pose" (D020 / pose-test lesson).
- **Climate consistency (D024):** once rain starts, ONE moody tone across all rain/water
  shots; light never jumps between shots of the same beat.
- **Multi-pass K2F is dead (DO-NOT-RUN).** Multi-character = ONE H3 R2V pass with up to
  9 reference slots (`ref_image_0…8`) + rule 5 layout — not chained identity passes.
- **Identity lock is per-character, pre-generation:** character IMAGES (below) carry identity;
  the H3 ref slots carry them into the shot. The identity-edit workflow is for single-character
  images only — it cannot lock 3 faces in one frame (that is H3's job).

---

## TEMPLATES

### Character shot (H3 R2V, single character)

```
<Subject 1> = [one line from continuity: age/build/hair/costume/props].
[Beat 1: physical action chain] → [hold: micro-detail] → [Beat 2: follow-through].
[Coupling line: character × environment, one sentence.]
[Negative space: what he is not doing; where the eyes go.]
[Camera: angle + movement, one line — handheld / slow push / static wide.]
[Light: from the scene's T column, one line.]
[Imperfection block — rule 6.]
[AUDIO: natural ambience only — NO music, NO instruments, NO melody, NO beat (D041).]
```

### Multi-character shot (3+ in one frame — the "three characters" case)

```
[Layout: X left of frame facing right; Y centre; Z right; distances in paces.]
[Per character, in spatial order: one-line identity + ONE action beat each.]
[One shared coupling line for the group × environment.]
[Camera + light + imperfection + D041 audio blocks.]
Rule: each character gets exactly ONE beat — group naturality comes from the shared
coupling line + staggered beats (X acts, Y reacts half a beat later, Z stays).
```

---

## CHARACTER IMAGE LAYER (what we were behind on — author 11-28: env + character images
BEFORE identity/multi-character workflows)

Per recurring named character, **two single-view Krea2 images** (NOT sheets — one H3 ref
slot = one anchor, D021), built with **identity-edit v1.2** (ref_boost 4.0, style LoRA
0.7, D023/D025) from the character's face ref so the face is LOCKED, costume from the
continuity map (`06`), era-correct background, "ONLY ONE character":

- **(a) identity view** — full-body, 3/4 standing, scene costume, neutral era-appropriate
  background, no other people.
- **(b) behaviour anchor** — full-body mid-signature-action, same costume (the pose that
  character is known for in this film).

### Teaser-cast image set (Dec 6 scenes only)

| Character | Scene(s) | Costume / state (from `06`) | Face ref |
|---|---|---|---|
| Jaisal-2026 dawn | Sc 1 | vest + mundu (O1), dawn light | char1 face ref |
| Jaisal-2026 match | Sc 6 | plain black tee, **watch on his wrist** ("Jaisal adjusts the watch") | char1 face ref |
| Zidhan-2026 | Sc 6 | **mustard logo tee + whistle** | char2 face ref |
| Jaisal-1950 | Sc 22–23 | 1950 Kerala (mundu + shirt), grey-drained colour | char1 face ref |
| Zidhan-1950 | Sc 22–23 | 1950 Kerala, grey-drained | char2 face ref |
| Grandpa | Sc 1 (·25) | white, ~70s, thin | t2i face ref first (new), then identity-edit |
| Rockstar | Sc 6 | black stars jersey | t2i (recurring enough for a face ref later) |
| kids | Sc 6, 23 | mismatched kits | generic, IN-SCENE (no identity lock) |
| referee | Sc 6 | referee kit | generic, IN-SCENE |

**Watch chain (prop continuity, `04` §1):** Sc 1 = on Grandpa's wrist · Sc 6 = on Jaisal's
wrist · Sc 23 = "watch in Jaisal's fist". Every shot prompt states the watch position.

### Execution order (REVISED 11-28 12:10 — author: env + characters first)

1. **Tonight (author queue):** 35 location plates (`krea2_t2i_env_cine.json` +
   `utilities\ep1_major_prompts_paste.txt`) — the environment layer.
2. **11-29 (author queue):** teaser character image set above (agent builds the
   identity-edit workflow + paste file).
3. **11-30 (author queue):** THREE-CHARACTER composition test at the Sc 6 ground
   (3 ref slots + rule-5 layout prompt) = the gate for "three characters in one image".
4. **Only then:** behaviour tests (`h3_behavior_test_*.json` — built, waiting),
   identity / face-refine workflows, and the Dec 6 teaser shots (11-30 → 12-02).
