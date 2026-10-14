# Model Routing

Which local model handles which task. Created 2026-10-13 after the Ortenzya 2-hour file-creation failure incident.

## The incident (why this file exists)

Ortenzya 31B (writing-ortenzya @8107) was asked to create 5 project files. It failed for ~2 hours:
- Wrote bash syntax (`mkdir -p`, `&&`) into PowerShell (needs `New-Item`, `;`)
- Piped markdown through `echo` — PowerShell parses `- **Beat**:` as arithmetic (unary minus, multiply)
- Re-sent the **identical** failed command 6+ times without reading the error it was given
- A working `write` tool was available the whole time; never used
- ~20 tok/s (262K ctx, MTP off, D126 update 3 config)

Qwen 3.8 27B did the same task in 3 tool calls, ~200 tok/s.

**Root cause:** creative-writing finetunes are not agent models. They loop on tool errors instead of diagnosing them. This is a model-capability gap, not a harness bug — the harness returned correct errors and a working `write` tool both times.

**Hard rule: never route tool-heavy work (files, shell, MCP) to a Gemma writer model. If a writer model fails a tool call twice, stop it and switch to Qwen — do not let it loop.**

## Routing table

| Task | Model | Port | Notes |
|---|---|---|---|
| Tool use, coding, file ops, ComfyUI, workflows, memory updates | **Qwen 3.8 27B NVFP4-MTP** (`qwen-local`) | 8100 | ~199 tok/s with MTP. Always via `.bat`. Default, always-on. |
| Creative writing — default | **Gemma4-31B QAT HauhauCS** (`writing-gemma4`) | 8106 | `D:\models\Gemma\run-gemma4-31b-qat.bat`. QAT Q4_K_M base, "Balanced" finetune (no "not X, it's Y" tic), MTP shipped, vision. 185 likes. |
| Creative writing — backup / second opinion | **Ortenzya 31B** (`writing-ortenzya`) | 8107 | `D:\models\Gemma\run-ortenzya-31b-q5.bat`. Creative-writer finetune, en+ja+ara, vision, Q5_K_M. Heretic EOG quirks (D124). No MTP in repo. 81 likes. **Prose-only — no tool work.** |

## Writer bat modes (speed workaround, 32 GB VRAM)

MTP ceiling = ~84K ctx (D126 update 2). Two modes per writer bat:

- **Interactive mode** (chat back-and-forth, per-scene dialogue): `CONTEXT_SIZE=83200` + MTP line ON → ~53% faster (D125).
- **Bulk mode** (full script completion, long context): `CONTEXT_SIZE=262144` + `--cache-type-k/v q4_0` + MTP line OFF → ~20-30 tok/s.

Current bats are set to bulk mode (user priority: large context, D126 update 3). Flip to interactive mode for writing sessions; flip back for bulk completion runs.

## Research findings (2026-10-13, from user-shared threads + fetches)

**Gemma 4 31B tool calling is weak (confirmed):**
- LiveKit community thread: tool calls hallucinate frequently on large tool results (~50% in their test cases).
- Base model HAS native function calling (Google model card; July 2026 FA4/tool-calling update improved BFCL/TB2/Tau2), but **creative/RP finetunes degrade it** — trained on creative data, not tool data. This incident is the local proof.
- localbench: tool calling is the most quantization-resilient category (KL 0.078 at Q8_0) → the base's tool calling survives Q4/Q5 quants; the finetune layer is what breaks it.

**localbench KLD findings (53 quants vs BF16, ~250K tokens):**
- Non-Latin scripts degrade worst at EVERY quant — even Q8_0 shows KL 0.222. **Gemma 4 31B quants are weak at Malayalam even at 8-bit.** Keep Malayalam conversion in the separate Manglish→Malayalam workflow; never expect the writer model to emit Malayalam reliably.
- Long documents degrade fastest (KL 0.466 at Q8_0). 262K bulk-mode completion runs will drift in quality in the back half → prefer 83K interactive mode for dialogue work.
- Pareto frontier = unsloth + bartowski quants only; avoid lmstudio-community and ggml-org quants.

**Naughty/RP finetune ecosystem (SillyTavern thread context):**
- The Gemma 4 31B creative finetune scene (Gembrain/Gemsicle/GarnetV2/SDFT-RP/heretic-ara) is built around "unhinged narratives," adult RP, dark fantasy. "Uncensored" there ≈ "won't stop writing naughty stuff."
- **Style-mismatch risk for the clean family football project:** prose drifts edgy. Uncensoring itself isn't needed for a football script (no refusals to remove).
- Implication: for clean family prose, prefer **base `unsloth`/`bartowski` Gemma 4 31B it** (Q5_K_M/Q6_K, Pareto-frontier, no RP skew, native tool calling) or **HauhauCS QAT "Balanced"** (less edgy, community-verified character work). Ortenzya demoted to edgy-only — NOT for this project.

**Writer session protocol (standing rule, D128.5):** writer models NEVER write files. Every writer-session prompt ends with: *"Return the entire document as text in your response. Do NOT use any tools. Do NOT create or write any files."* Workflow: writer session produces text → user copies/saves it → Qwen archives to `scripts/` (e.g. `episode1_structure_qat.md`) when the user is back. Not "absolutely needed" for pure writing tasks (the model replies with text anyway) — it's free insurance that removes the loop failure mode entirely.

**Iterative development protocol (D128.6):** the script is developed IN the writer session, round by round. The model drives: after every version it must ask the director for the next input and wait. The director (user) is the ONLY source of truth for plot details — the model must NEVER invent plot; missing detail = ask, don't fill. Every round returns the FULL document (labeled v1, v2, ...), not a diff. The loop continues until the user declares the script FINAL and FIXED. Checkpoint habit: every time a section feels settled, save that round's output to `scripts/episode1_structure_vN.md` (user copies, or pastes back and Qwen archives) — if the session dies or the model drifts, the latest saved version is the restart point (restart = synopsis + latest saved doc + "continue, ask me for the next input").

**Malayalam caveat for writer models (localbench KLD):** non-Latin scripts are the WORST category at every quant (KL 0.222 even at Q8_0). Judge any Malayalam section from a Gemma writer STRICTLY — expect broken/mixed output. Fallback route if it fails: English/Manglish from the writer → Malayalam via the established Manglish→Malayalam conversion (`prompts\manglish_to_malayalam.txt`, D116) or via Qwen.

**Tone test (2026-10-13, D128.1):** user CONFIRMED **HauhauCS QAT Q4_K_M as default writer** (no base-model A/B). The test IS the real task, not a toy scene: paste-ready prompt at `scripts/episode1_structure_prompt.txt` — Episode 1 structure document (structure + meaning + aim), English AND Malayalam, NO dialogues yet, text-only response. User runs it in a FRESH DSH session on the QAT provider (stop Qwen 8100 → `D:\models\Gemma\run-gemma4-31b-qat.bat` → wait for "listening on 8106"). Judge: (1) meaning section shows real grasp of the story, (2) clean family tone / no edgy drift, (3) Malayalam section clean or broken, (4) structure is useful or vague. If prose drifts edgy → fallback = base `unsloth`/`bartowski` Q5 (download required, not yet on disk).

## Switching protocol (one writer at a time + Qwen)

1. Stop Qwen 8100 (Ctrl+C in its console)
2. Run the writer bat: `D:\models\Gemma\run-gemma4-31b-qat.bat` (or ortenzya)
3. Wait for `listening on 8106` / `listening on 8107`
4. When done: stop the writer, restart Qwen 8100 via `always.bat`
5. DSH writing profile (port 3081) has both writer providers registered — select the active one per session

## Football project (Episode 1) plan

- **Qwen 8100**: script file creation, memory updates, any ComfyUI/workflow work, dialogue structure
- **QAT 8106 (default writer)**: scene prose, dialogue polishing (Jaisal = short emotional lines; Zidhan = clipped practical; Abu Bakar = slow circular), magical-realist description
- **Ortenzya 8107 (backup)**: second-opinion prose drafts if QAT's voice disappoints; text-only tasks
- Verify QAT on a small tool task before fully trusting it as an agent (its HF tags claim agentic/coding — unverified)
