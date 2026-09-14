# INTRO VIDEO — PRODUCTION PLAN (Jaisal Kut)

Last Updated: 2026-09-10
Status: PLANNED — awaiting user go-ahead per task
Script: `docs/INTRO_SCRIPT.md` (Final Script v2, ~67s, B&W, no music, halal)

## 1. The script at a glance

7 shots, ~67s, **black & white cinematic**, high contrast, fine grain, 24fps.
Single practical bare bulb (top-down 45°), hard shadow, no fill.
**Diegetic sound only** (room tone, chair scrape, bulb hum, breath, sigh, paper
rustle) — **NO MUSIC** (D041). Two characters: **JAISAL** (the host) +
**CAMERA GUY** (off-screen, asks questions). Bilingual (Malayalam + English).

| # | Time | Shot | Lens | The VFX / cinematic challenge |
|---|------|------|------|-------------------------------|
| 1 | 0:00–0:05 | WIDE STATIC | 35mm | Bulb swings, chair scrape, Jaisal enters + sits, camera-guy silhouette |
| 2 | 0:05–0:08 | MEDIUM | 50mm | Slight low angle, "You ready?" |
| 3 | 0:08–0:18 | CLOSE UP | 85mm | **THE HEAD TWIST** — eyes shift, head rotates SLOWLY 180° toward camera, body stays still, camera rotates + pushes in at the same rate. Glitch + silence + cut to black. |
| 4 | 0:18–0:25 | MEDIUM REVERSE | 50mm | **PERFECT REVERSE** — everything plays backwards (chair, clothing, bulb, camera rotation), lands on ordinary seated Jaisal. |
| 5 | 0:25–0:38 | MEDIUM→CLOSE PUSH | 50→85mm | **PLANTS GROW** — a stem pushes through the table, another follows, a rose opens, plants populate the table. |
| 6 | 0:38–0:56 | CLOSE UP | 85mm | **PLANTS DIE SLOW** — leaf falls, plant bends, rose closes, room empties. |
| 7 | 0:56–1:07 | MEDIUM WIDE | 35mm | **OBJECTS AWAKEN** — page floats in, mic drops in, a cricket assembles (bat=body, stumps=hands, balancing on football, paper-smiley head, mic in front). Bulb flickers, cut to black. |

### The hard VFX items (ranked by difficulty)
1. **Shot 3 — 180° head twist + synced camera rotation/push-in.** The signature
   shot. H3 will struggle to hold a clean 180° rotation with the body locked.
   Options: (a) H3 i2v with a strong motion prompt + Shot Composer reference;
   (b) **2D post** (rotate the head region on a turntable / 3D head model);
   (c) Shot Composer 3D mannequin head-rotation → export → H3 i2v.
2. **Shot 7 — object assembly (cricket from props).** Multi-object physics in a
   dark space. H3 is weak at precise multi-object assembly. Options: (a) Shot
   Composer (primitives + keyframes) → export → H3; (b) H3 R2V with a
   Krea2-styled reference of the assembled cricket; (c) 2D compositing in post.
3. **Shot 4 — perfect reverse.** Easiest: generate the forward take, **reverse in
   post** (ffmpeg/DAW). Do NOT ask H3 to "reverse" — it can't.
4. **Shots 5/6 — plant growth / death.** H3 can do slow organic growth but it's
   unpredictable. Options: H3 i2v (seed-locked, iterate), or Shot Composer
   (scale keyframes on a plant primitive), or 2D.
5. **B&W look.** Apply in **post** (grayscale + contrast + grain) OR bake into
   the Krea2 keyframes (B&W prompt). Post is safer (consistent across shots).

## 2. Character consistency — Krea2 (user's decision)

**Decision (user, 2026-09-10):**
- **Intro video → Krea2 Identity Transfer workflow** (`krea2_identity_edit.json`,
  Identity Edit v1.2). Fast, no training.
- **Movies → Krea2 LoRA** (train a character LoRA for full consistency).

**Reference set:** `E:\ComfyUI_windows_portable\ComfyUI\output\Dataset\character_1`
= **20 PNGs** of the character.

**Identity Edit v1.2 key params (D023/D025):**
- `ref_boost` = 4.0 (fidelity dial; >10 over-copies, <1 suppresses the ref)
- KSampler 10 steps, cfg 1 (turbo)
- `grounding_px` 384–768 (lower if compositions double/split)
- 1MP output
- Style LoRA `Krea2_Cinematic_Artstyle.safetensors` @ 0.7 (node 95) for the
  moody/cinematic tone — for B&W, add a B&W/grain instruction.
- **Use a reference that's already in the target look** (B&W, moody) so the tone
  matches automatically (D025).

**Plan for the intro:**
1. Pick the best 3–5 of the 20 character_1 images (clearest face, varied angles).
2. Run Identity Edit v1.2 to generate the **keyframes** for each shot (Jaisal
   seated, the head-twist frame, the plant shots, the object-assembly frame) in
   the B&W cinematic look.
3. Feed 2–3 of those Krea2 keyframes to H3 (i2v / R2V) so the character + style
   hold across the video (D021).

**CAMERA GUY** is off-screen (voice only) — no character image needed, just a
voice (see audio).

## 3. Audio — RVC pipeline (D050, D055)

Two voices: **JAISAL** (host, main character) + **CAMERA GUY** (off-screen,
asks the questions). **The user dubs ALL lines** (they're the sole
writer/director/performer).

- **JAISAL = the USER'S OWN VOICE.** User dubs every JAISAL line (Malayalam +
  English) → `clean_audio.py` → used as-is (their real voice). NOT Midhun.
- **CAMERA GUY = MIDHUN'S VOICE.** User dubs the camera-guy lines (own voice)
  → `clean_audio.py` → RVC `midhun_v2_40k` → Midhun's timbre. **No second RVC
  model needed** (reuses `midhun_v2_40k`).
- **Pipeline:** user dubs each line (headset, quiet room) → `clean_audio.py`
  (openvoice venv) → JAISAL lines used directly; CAMERA GUY lines → RVC
  `infer.cli --model midhun_v2_40k.pth --input <dub> --output <out>
  --f0-method rmvpe --protect 0.33 --index-rate 0.75`.
- **Known issue:** RVC wording sounds "weird/quirky" on non-native sources —
  the user's own clean dub is the real test. If weak: `--index-rate 0.9`, or
  retrain with more data (`scripts\rvc_train.py`).
- **Sound design (diegetic only, NO MUSIC):** room tone, chair scrape, bulb hum,
  breath, sigh, paper rustle. Generate via ControlFoley (text-only mode) or a
  SFX library; mux in post. (ControlFoley was weak on 2D line-art — for this
  realistic B&W look it may work better; test.)

### Process order (D055 — dub-first)
Audio is the timing spine (each shot's length = its line's length). Order:
**dub all lines → lock shot durations from audio → generate keyframes + video
to match → SFX + assembly.** A quick B&W tone test (1-2 Krea2 keyframes) runs
in parallel to lock the look while dubs are recorded.

## 4. Qwen3-VL as the H3 prompt engine (user's idea)

**Model:** `D:\models\Writing\Qwen\Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf`
+ `...-mmproj-F32.gguf` (multimodal projector). This is a **VLM fine-tuned for
MiniMax H3** — it takes an image/description and emits an **H3-optimized prompt**.

**Goal:** wire it into the H3 ComfyUI pipeline so prompts are H3-tuned (better
adherence) instead of hand-written.

**Integration options (to verify):**
1. **ComfyUI custom node** that loads the GGUF (llama.cpp / GGUF loader) + the
   mmproj, takes a reference image (Krea2 keyframe) + a short intent, and outputs
   the H3 prompt → feed into the H3 node's prompt input.
2. **Standalone script** (llama.cpp server or `llama-cpp-python`) that runs the
   VLM on each keyframe → writes the prompt → the H3 workflow reads it.
3. **Check for an existing node** (e.g. a GGUF/VLM caption node in
   `custom_nodes`) that already loads GGUF VLMs — reuse it.

**First step:** confirm how to load a GGUF VLM + mmproj in ComfyUI (which node
pack), then build the prompt-enhancer node/script. **NOT yet set up** (the GGUF
is not in the ComfyUI models dir).

## 5. Shot Composer (open-media) — the "Blender way" (user's idea)

**Repo:** `https://github.com/Anujatk1999/open-media` = **"Shot Composer"** — a
free, browser-based, **local** 3D shot composer (React + three.js + mannequin.js).
No backend, no account, data stays in `localStorage`.

**What it does (relevant to us):**
- Add characters (Male/Female/Child) + primitives (cube, sphere, cylinder, etc.).
- **Pose** characters (joint gizmos, pose library).
- **Camera** control: shot size (wide/full/medium/MCU/close-up), angle (front,
  3/4, profile, back, OTS), elevation, composition.
- **Motion mode:** keyframe characters/objects/cameras over a timeline; camera
  rigs (follow/orbit/shot); Motion Shot Sequence (chain framings).
- **Export:** Capture Shot → PNG reference; **Export MP4** → the full motion
  timeline as a video.
- **MCP server** (`mcp/` dir): `cd mcp; npm install; npm start` — lets an AI
  agent drive the composer (build scenes, pose, keyframe, save).

**Setup (needs Node.js 18+):**
```
git clone https://github.com/Anujatk1999/open-media.git
cd open-media
npm install
npm run dev        # → http://localhost:5173
```

**How it helps the intro (the "Blender way"):**
- Previsualize the **hard shots** (3 head-twist, 5/6 plants, 7 object assembly)
  as a 3D mannequin + primitives with keyframed motion.
- **Export MP4** of the motion → feed to H3 as a **motion/pose reference** (i2v
  or R2V) so H3 follows the exact movement instead of guessing.
- **Export PNG** of a posed frame → use as the H3 first-frame / Krea2 reference.

**Plan:** set up Shot Composer, build the Shot 3 (head twist) + Shot 7 (object
assembly) motions, export, and test whether H3 follows the reference better than
a text prompt alone.

## 6. Video — MiniMax H3

- **Speed stack:** SLA (D042) — 1MP H3 under 240 s.
- **Per-shot approach:**
  - Simple shots (1, 2, 4, 6): H3 i2v from a Krea2 keyframe + a clear motion
    prompt.
  - Hard shots (3, 5, 7): H3 i2v/R2V **with a Shot Composer motion reference**
    (if it helps) + a Krea2-styled first frame.
- **R2V rules (D017/D020):** 2–3 Krea2-styled refs max, each an explicit frame
  anchor for one shot, SHORT prompt, 6-section structure, `<Picture N>` tags in
  connection order.
- **B&W:** bake into the Krea2 keyframes + confirm in post.
- **NO MUSIC (D041):** diegetic sound only.
- **D045:** stop Qwen before H3 generation (heavy GPU job).

## 7. Assembly

- Video editor (or ffmpeg): mux the RVC voice track + H3 video + diegetic SFX.
- Apply the B&W + grain + contrast grade consistently across all shots.
- Upscale if needed: SeedVR2 TensorRT Studio (2K, ~8 min/8 s on the 5090).
- Title card: "JAISAL KUT" (name lock) — Krea2 or a simple text overlay.

## 8. Task list (do one by one)

- [ ] **T1 — Character keyframes (Krea2 Identity Edit v1.2):** pick best 3–5 of
      the 20 character_1 images → generate B&W cinematic keyframes for each shot
      (Jaisal seated, head-twist frame, plant shots, object-assembly frame).
- [ ] **T2 — Audio (RVC):** user dubs JAISAL + CAMERA GUY lines → `clean_audio.py`
      → RVC (`midhun_v2_40k` for JAISAL; a ref voice for CAMERA GUY) → listen.
- [ ] **T3 — Qwen3-VL prompt engine:** confirm how to load the GGUF VLM + mmproj
      in ComfyUI (node pack or standalone script) → build the H3 prompt-enhancer.
- [ ] **T4 — Shot Composer setup:** `git clone` + `npm install` + `npm run dev`
      → build Shot 3 (head twist) + Shot 7 (object assembly) motions → export
      MP4/PNG → test as H3 references.
- [ ] **T5 — H3 generation:** per-shot i2v/R2V (SLA stack), B&W, NO MUSIC, stop
      Qwen first.
- [ ] **T6 — Sound design:** diegetic SFX (room tone, chair scrape, bulb hum,
      breath, paper rustle) — ControlFoley text-only or SFX library.
- [ ] **T7 — Assembly:** mux audio + video + SFX, B&W/grain grade, title card,
      optional SeedVR2 2K upscale.
- [ ] **T8 — Review + iterate.**

## 9. Rules that apply
- **NO MUSIC** (D041) — diegetic sound only.
- **D045** — stop Qwen before H3 generation (heavy GPU). RVC small jobs OK alongside.
- **D051** — I never stop Qwen myself; user runs stop/restart commands.
- **Character consistency** — Krea2 Identity Edit v1.2 for the intro (D023/D025);
  Krea2 LoRA for movies.
- **Climate/look consistency** — ONE B&W moody tone across all shots.
- **CAMERA (user hard rule, 2026-09-11):** STATIC, CENTERED, SYMMETRIC framing for
  emotional/in-depth shots — the subject is centered, the camera is straight-on and
  static. Asymmetric positions or different camera angles are used ONLY when there is
  no emotional story to hold (StudioBinder principle). No extreme close-ups (face
  filling the frame) — keep MEDIUM, straight, centered.
- **LIGHT-POOL DARKNESS (user hard rule, 2026-09-11):** the bulb's light is a small
  pool; everything OUTSIDE it is pure black (NO visible walls/pillars/columns). This
  is what makes the 180° head-twist (shot 3) a clean cut — no wall to rotate/expose.
- **CONSISTENCY LOCK (user hard rule, 2026-09-11):** the character (black full-sleeve
  shirt, unbuttoned halfway), the table (consistent size/color/position), and the
  plants (consistent design) must stay IDENTICAL across all shots — MiniMax drifts if
  they change between frames.

## 10. Open questions (for the user)
1. **CAMERA GUY voice** — do you have a reference, or should I dub + RVC a second
   character model?
2. **B&W in Krea2 vs post** — bake B&W into the keyframes, or generate in color
   and grade in post? (Recommend: test both on Shot 1.)
3. **Shot 3 head-twist** — try H3 i2v first, or go straight to Shot Composer /
   2D post? (Recommend: H3 i2v first, fall back to Shot Composer.)
4. **Qwen3-VL** — is there a specific ComfyUI node you've seen for GGUF VLMs, or
   should I research the best loader?

---

## 10b. User decisions (2026-09-10) — all 4 open questions answered

1. **VOICE ASSIGNMENT (superseded 2026-09-11, see D055)** -> originally:
   CAMERA GUY = a new 26-yo male model, JAISAL = `midhun_v2_40k`. **NOW:
   JAISAL = the USER'S OWN VOICE** (user dubs all JAISAL lines, cleaned, used
   as-is); **CAMERA GUY = MIDHUN** (user dubs camera-guy lines → RVC
   `midhun_v2_40k`). No second RVC model needed. The user dubs ALL lines.
2. **B&W** -> **bake it into Krea2** — the keyframes themselves are generated in
   the B&W tone, so H3 inherits it (easier for MiniMax). The character_1 refs are
   color, so the Identity Edit instruction must force the B&W look.
3. **Shot 3 head-twist** -> **try H3 i2v 2-3 times first**; if it doesn't get the
   180-degree rotation clean, **fall back to Shot Composer** (the 3D setup).
4. **Qwen3-VL** -> **analyze the user's found model** (`Qwen3-VL-32B-Instruct-
   MiniMax-H3-L0-49`); use a better one if found. (It's H3-specific — likely the
   right choice; verify the ComfyUI loader.)

### VFX approach (user, 2026-09-10)
- **The object-assembly VFX (Shot 7: cricket = bat + stumps + ball + page + mic)
  should be done in 3D** so the motion is clean and H3 can follow it. Same for the
  page-with-mic.
- **Shot Composer vs Blender:** Shot Composer (open-media) is a **browser-based
  3D** tool (three.js + mannequin.js) — NOT Blender, but the same idea (pose +
  keyframe + export). It's lighter (no install, runs in the browser) and has an
  MCP server. **Blender is NOT installed** on this machine. **Decision: use Shot
  Composer first** (no install); install Blender only if Shot Composer can't do a
  specific VFX cleanly.
- **Shot 4 (perfect reverse):** generate the **forward** take in H3, then
  **reverse in post** (DaVinci Resolve or ffmpeg) — do NOT ask H3 to reverse.

### Tooling status (checked 2026-09-10)
| Tool | Status |
|------|--------|
| DaVinci Resolve | installed (`C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe`) |
| Node.js | v25.6.1 (use `npm.cmd` — PowerShell blocks `npm.ps1`) |
| ffmpeg | `D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe` |
| Blender | NOT installed (Shot Composer is the 3D tool of choice) |
| Qwen3-VL GGUF | `D:\models\Writing\Qwen\` (Q4_K_M + mmproj-F32) — not yet in ComfyUI models dir |
| **Shot Composer (open-media)** | **INSTALLED 2026-09-11** at `D:\models\open-media` (cloned + `npm install`, 90 pkgs). Run: `cd D:\models\open-media; npm.cmd run dev` → http://localhost:5173. MCP: `cd mcp; npm.cmd install; npm.cmd start`. |

### B&W keyframe technique (verified 2026-09-11)
- **v3 KEYFRAME SET (current, 2026-09-11):** `krea2_intro_kf1_empty.json`,
  `krea2_intro_kf2_seated.json`, `krea2_intro_kf3a_headnormal.json`,
  `krea2_intro_kf3b_headtwisted.json`, `krea2_intro_kf5_plants_grown.json`,
  `krea2_intro_kf6_plants_dead.json`, `krea2_intro_kf7_cricket.json` (native UI format,
  openable + re-runnable in the ComfyUI UI). Build script:
  `utilities/build_intro_keyframes_v3.py`. Each = copy of `krea2_identity_edit.json` with
  node 84 (instruction) + node 29 (save prefix) changed; node 72 = grayscale ref
  `intro_char_ref_bw.png`; node 114 (rgthree comparer) bypassed. All validate `valid: true`.
- **LIGHT-POOL DARKNESS (the real wall-fix):** "the bulb's light forms a small pool;
  everything OUTSIDE that pool is pure black darkness, NO visible walls/pillars/columns/
  concrete, the room fades into complete blackness on ALL sides." Baked into every prompt.
  (v1/v2 "no walls" wording still hallucinated walls/pillars — the light-pool framing is
  what actually kills them.)
- **CONSISTENCY LOCK (shared blocks in every prompt):** CHARACTER (dark wavy hair, dark
  complexion, black full-sleeve shirt UNBUTTONED HALFWAY/open collar), TABLE (simple
  wooden table + chair, consistent size/color/position), CAMERA (straight-on, centered,
  symmetric, eye-level, static, subject centered). NO extreme close-ups (all MEDIUM).
- **7 UNIQUE KEYFRAMES (all 1928×1088, pure B&W):** kf1_empty, kf2_seated,
  kf3a_headnormal, kf3b_headtwisted (backside, head twisted 180° over shoulder — the
  signature frame), kf5_plants_grown, kf6_plants_dead (re-ran as _00002_ after a concrete
  pillar + pot broke through _00001_), kf7_cricket (soccer ball + smiley-on-written-paper
  + mics + bat body).
- **MOTION PAIRS for MiniMax (first→last):** shot1 walk-in = kf1→kf2; shot3 twist =
  kf3a→kf3b; shot5 growth = kf2→kf5; shot6 dying = kf5→kf6; shot7 assembly = kf2→kf7;
  shot4 reverse = kf2 (reversed in post). **ALL MOTION IS MINIMAX'S JOB** — keyframes are
  just anchors.
- **HARD RULE (user): STATIC, CENTERED, SYMMETRIC camera for emotional/in-depth shots —
  asymmetric/different angles only when there's no emotional story (StudioBinder principle).**
- **Reusable per-shot workflows (v1, superseded by v3):** `krea2_intro_shot1.json` …
  `krea2_intro_shot7.json` (build script `utilities/build_intro_keyframes_all.py`).
- **KEY (D025):** pre-convert the character ref to **grayscale** (`input\intro_char_ref_bw.png`
  from `character_1\Image_00001_.png`) AND demand B&W in the instruction → output is **pure
  monochrome** (measured colorfulness 0-1). The Identity Edit inherits the ref's tone, so a
  grayscale ref forces clean B&W.
- **ALL 7 KEYFRAMES GENERATED (2026-09-11):** `output\jaisal_cut\intro_shot1_00001_.png` …
  `intro_shot7_00001_.png` (all 1928×1088, pure B&W). Quality: Shot 1 (wide seated) ✅, Shot 3
  (extreme close-up, bulb above, head-twist anchor) ✅, Shot 5 (plants/rose growing on table)
  ✅, Shot 7 (object assembly: cricket-bat body + smiley paper head + football + mic + floating
  page) ✅. Character consistent across all 7. **User to review in ComfyUI; re-run any shot via
  its `krea2_intro_shotN.json` (or tweak node 84 + re-run).**

### Character reference picks (character_1, 20 PNGs)
- **Identity lock refs:** `Image_00001` (frontal close-up, clean) + `Image_00020`
  (profile). Consistent young man, dark wavy hair, dark shirt.
- **B&W:** refs are color -> the Identity Edit instruction must force the B&W
  cinematic look (high contrast, fine grain) so the keyframes come out B&W.

### Reversing the 180-degree head twist (user asked: "is it possible in DaVinci Resolve?")
- **Shot 4 (perfect reverse)** is the easy one: generate the FORWARD take in H3,
  then **reverse the clip** — DaVinci Resolve: select the clip in the Edit page ->
  right-click -> **Reverse** (or `Ctrl+R`); it renders the clip backwards. ffmpeg
  equivalent: `ffmpeg -i forward.mp4 -vf reverse -af areverse out.mp4`.
- **Shot 3 (the 180-degree head twist itself)** is NOT a simple reverse — it's a
  live 180-degree rotation of the head while the body stays still. That's a
  **generation** problem (H3 i2v) or a **3D** problem (Shot Composer / Blender
  head turntable), not a post reverse. If H3 can't hold it clean, the 3D route
  (Shot Composer mannequin head-rotation keyframes -> export -> H3 reference) is
  the clean path.
- **DaVinci Resolve is installed** and is the right tool for: reversing Shot 4,
  the B&W + grain + contrast grade, glitch effect (Shot 3 cut), and final assembly.

## 11. Open questions (remaining)
1. **CAMERA GUY dub** — when will you record the 26-yo male reference? (Need ~1-2
   min clean audio to train the second RVC model.)
2. **Shot Composer install** — OK to `git clone` + `npm install` now (needs
   Node.js, which is present)?
3. **Qwen3-VL loader** — should I research the best ComfyUI node for GGUF VLMs, or
   do you have one in mind?
