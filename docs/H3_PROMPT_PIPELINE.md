# H3 R2V Prompt Pipeline — Jaisal Kut Intro

**Goal:** generate a proper MiniMax H3 R2V prompt for each of the 10 intro shots,
so the prompts describe OUR character (not a generic "school kid") and tag
`<Picture N>` to match the actual reference images. Then wire the prompts into the
10 workflows and run them.

---

## 1. The model — DIAGNOSIS (2026-09-14)

| File | Size | What it is |
|---|---|---|
| `Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-Q4_K_M.gguf` | 14.93 GB | A **pruned** vision-language model (layers 0-49, NO output head) |
| `Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49-mmproj-F32.gguf` | 2.38 GB | The vision projector (mmproj) |

**CRITICAL FINDING:** This model is **pruned** — it has 50 transformer layers
(0-49) but **NO `output_norm` and NO `lm_head`** (the output head). This means it's
a **text encoder only** (produces embeddings), NOT a **text generator** (produces
text). That's why llama.cpp fails with `tensor 'output_norm.weight' not found`.

The HF repo confirms this: "Pruned layers after 49 as they arent needed for use
with MiniMax H3" and "Can be used in ComfyUI with my fork of City96's
ComfyUI-GGUF. https://github.com/Nif00/ComfyUI-GGUF"

**CONCLUSION:** This specific model **CANNOT be used for prompt generation**
because it has no output head. It's meant to be used **in ComfyUI as a text
encoder** (via the `Nif00/ComfyUI-GGUF` fork), not as a standalone chat model.

**REVISED PLAN:** Use the pruned H3 model **in ComfyUI** as a text encoder:
1. Install the `Nif00/ComfyUI-GGUF` fork (https://github.com/Nif00/ComfyUI-GGUF)
2. Wire the pruned H3 model + mmproj into the ComfyUI workflow as a text encoder
3. The model will encode the reference images + shot description into embeddings
4. Use those embeddings to condition the MiniMax H3 R2V generation

**ALTERNATIVE:** If we want to generate prompts (not just encode them), we need a
**full vision-language model** (with an output head). Options:
- Download a full Qwen3-VL model from HuggingFace (e.g., `unsloth/Qwen3-VL-32B-Instruct-GGUF`)
- Use a different vision-language model that's already installed
- Go back to hand-crafted prompts, but fix the structure issues (character description, `<Picture N>` tags, 6-section structure)

---

## 2. VRAM reality (why we stop Qwen)

- The H3 model is ~15 GB. Qwen is also large (~17–20 GB VRAM).
- Running both at once risks **OOM on the 32 GB RTX 5090**.
- So the safe procedure is: **stop Qwen → run H3 model → generate prompts (quick,
  ~5–10 min) → stop H3 model → restart Qwen.**
- The prompt generation is a *quick* job (10 shots × ~30–60 s), so Qwen is only
  down for ~10 minutes.

> **I never stop Qwen myself** (I run on it). You run every command below.

---

## 3. The procedure (you run these)

### Step 0 — Prereqs (already done)
- [x] 10 shot workflows built + validated (`jaisal_intro_A…J.json`).
- [x] 14 keyframes in `D:\models\vsCodeMcp\Jaisal-intro\keyframes\`.
- [x] Per-shot descriptions in `D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_descriptions.txt`.
- [x] `utilities\gen_h3_prompt.py` (single shot) + `utilities\gen_all_h3_prompts.py` (batch).

### Step 1 — Stop Qwen (your terminal)
```powershell
Stop-Process -Name "llama-server" -Force
```
> The chat cuts off. Expected. You're now doing this manually.

### Step 2 — Launch the H3 prompt model (your terminal)
```powershell
D:\models\Writing\Qwen\run-minimax-h3-heretic.bat
```
Wait until it prints that the server is listening on **port 8104** (it loads the
15 GB model first — give it a minute or two). **Leave this terminal open.**

### Step 3 — Verify it's up (a SECOND terminal)
```powershell
Invoke-RestMethod http://127.0.0.1:8104/v1/models
```
Should return the model name. If it errors "connection refused", the model isn't
ready yet — wait and retry.

### Step 4 — Test ONE shot first (recommended)
```powershell
& "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "D:\models\vsCodeMcp\utilities\gen_all_h3_prompts.py" A
```
This generates **only shot A** and saves it to
`D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_A.txt`. Open it and check:
- Does it describe **our** character (rose shirt, black trousers, black bag) — not a generic "school kid"?
- Do the `<Picture N>` tags match the actual refs (A = `table empty.png` → `jaisal_hand_under_the_table.png`)?
- Is the 6-section structure correct?

If it's good, proceed. If not, tweak the description in `shot_descriptions.txt`
and re-run just that shot.

### Step 5 — Generate ALL 10 prompts
```powershell
& "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "D:\models\vsCodeMcp\utilities\gen_all_h3_prompts.py"
```
Saves `shot_A.txt` … `shot_J.txt` in `Jaisal-intro\prompts\`. Takes ~5–10 min.

### Step 6 — Stop the H3 model
```powershell
Stop-Process -Name "llama-server" -Force
```
> Qwen is already stopped, so this stops only the H3 model. (If you ever have
> both running, `Get-Process -Name "llama-server" | Select Id,StartTime` shows
> which is which.)

### Step 7 — Restart Qwen
```powershell
Start-Process "D:\models\qwen\Qwen3.827BMTP.bat"
```
> Chat comes back. Tell me the prompts are ready.

### Step 8 — Review + wire (me)
- I review the 10 prompts with you.
- I paste each `shot_X.txt` into the matching workflow's prompt node.
- I validate all 10.

### Step 9 — Run the workflows (you)
- Stop Qwen again (the actual video generation is the heavy GPU job).
- Run **A → J** in the UI (now at correct per-shot lengths: A=5.2s, B=3s, …).
- Restart Qwen.

---

## 4. What we give the model per shot

For each shot, the model receives:
1. A **short shot description** (action + camera + look) — from
   `shot_descriptions.txt` (derived from the intro MD, one block per shot).
2. The **actual reference images** for that shot (from the keyframes folder), in
   `<Picture N>` order (first = start frame, last = end frame).

The model writes a proper 6-section H3 R2V prompt that matches what's *really* in
the images.

**Why not give the whole intro MD?** The model needs to focus on ONE shot at a
time. Giving the whole 67 s script would make it try to describe all 7 shots at
once. So we give the per-shot description + the reference images. The B&W /
no-music / 24 fps / one-character rules are baked into the system prompt.

### Per-shot reference mapping (refs ONLY from the keyframes folder)
| Shot | Refs (in `<Picture N>` order) |
|---|---|
| A | `table empty.png` → `jaisal_hand_under_the_table.png` |
| B | `jaisal_hand_under_the_table.png` → `jaisal_with_hand_on_table.png` |
| C | `jaisal_head_left_back_side.png` (camera node) |
| D | `jaisal_head_180_dergree.png` → `jaisal_with_hand_on_table.png` |
| E | `jaisal_with_hand_on_table.png` → `plants_Alive.png` |
| F | `plants_Alive.png` → `plants_dead.png` |
| G | `plants_dead.png` → `jaisal_gone_papers_alone.png` |
| H | `jaisal_gone_papers_alone.png` → `mic+paper_2k.png` |
| I | `mic+paper_2k.png` → `mic_without paper_final scene.png` |
| J | `mic_without paper_final scene.png` + `obj_cricket_bat_00002_.png` + `obj_soccer_ball_00002_.png` + `obj_paper_smiley_00002_.png` |

---

## 5. The character sheet (optional, for identity consistency)

The MiniMax H3 character-sheet node family **is installed**:
`DecodeH3CharacterSheet`, `TextEncodeH3Edit`, `AddH3EditReference`,
`H3EditOptions`, `Conditioning Recast FP64`, `Sigmas Recast`.

- Use it to generate a **consistent multi-angle character sheet** from our
  character (front / side / back / close-up), then use that sheet as the identity
  anchor for all shots.
- **When you need it:** if we want NEW angles/poses we don't have keyframes for,
  or if the character's face drifts between shots.
- **When you don't:** since we already have a keyframe for each shot (which shows
  our character), the R2V prompts can use those directly. The character sheet is
  a belt-and-suspenders identity lock, not a prerequisite.

---

## 6. Troubleshooting

| Symptom | Fix |
|---|---|
| `connection refused` on port 8104 | The model isn't loaded yet — wait, re-check Step 3. |
| OOM crash when launching the H3 model | Make sure Qwen is fully stopped (Step 1). Check `Get-Process -Name "llama-server"`. |
| Prompt describes a generic character | The model didn't get the images — check the `--refs` paths exist and are in the keyframes folder. |
| `<Picture N>` tags wrong | Make sure the refs are passed in the correct order (start frame first). |
| Prompt too long / bloaty | Lower `--max-tokens` in `gen_h3_prompt.py` or tighten the shot description. |
| One shot is off | Re-run just that shot: `python gen_all_h3_prompts.py <X>` after editing its description. |

---

## 7. Files

| File | Purpose |
|---|---|
| `D:\models\Writing\Qwen\run-minimax-h3-heretic.bat` | Launches the H3 prompt model on port 8104 |
| `utilities\gen_h3_prompt.py` | Generate one shot's prompt (`--desc` + `--refs`) |
| `utilities\gen_all_h3_prompts.py` | Batch-generate all 10 prompts |
| `Jaisal-intro\prompts\shot_descriptions.txt` | Per-shot descriptions (from the intro MD) |
| `Jaisal-intro\prompts\shot_X.txt` | Generated prompts (output) |
| `Jaisal-intro\keyframes\` | The 14 reference images (source of truth) |
