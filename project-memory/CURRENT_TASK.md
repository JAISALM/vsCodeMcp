# Current Task

## 🔴 PRIMARY GOAL: Scripting Episode 1
**Phase:** Moving from the "Red Card/Fight" of the first half into the 1950 Mind-Trip.

**Writer entry point (D132):** `episode1\CONTINUE_SCRIPT.md` — self-contained brief.
The writer model (Gemma) reads it and writes **only** the new file it names
(`episode1\episode1_script_part2.md`) — it must NOT edit existing files; the agent
model (Qwen) updates memory + commits afterwards.

**Next Milestones:**
1. **The Humorous Selection:** Define the IQ-based players (The Mathematician, The Lazy Genius, etc.).
2. **The Ship Journey:** Script the la lloC (Cura la lloC) journey to Brazil, including coconut practice and the "Fax" fix.
3. **The Brazil Final:** Detailed clash between Jaisal's Tactical India and Zidhan's Physical Brazil.
4. **The 360 Return:** Transition back to 2026 and the final handshake.

**Pending Technicals:**
- Verify MTP (Speculative Decoding) is active for Gemma writers.
- Maintain the 262K context window for long-term reasoning.

## Krea2 Realism V1 A/B test (2026-10-17, D133) — IN PROGRESS
- User downloads `Krea2Realism_V1.safetensors` (13.14 GB FP8, HF `RudySen/Krea2-Realism-Checkpoint`) **via browser** (agent download aborted per user) and drops it into `E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\`.
- A/B workflow prepared: `data\krea2_abtest_realism.json` — old `krea2_turbo_fp8_scaled` @10 steps vs new `Krea2Realism_V1` @6 steps (author's sweet spot), same seed 42, euler/simple, cfg 1, 1152×1792 (2MP).
- **Next steps:** (1) verify model visible: `GET http://127.0.0.1:8188/models/diffusion_models` (server restart may be needed for the UNETLoader combo list); (2) run the A/B via MCP `run_workflow` (API format); (3) user judges realism; (4) if good → swap Krea2 base in workflows (keep old files).
- **Reddit recipe:** redlib mirror `safereddit.com` works for blocked reddit posts (see D133).

**Project files (read these when resuming) — Episode 1 hub = `episode1\`:**
- `episode1\DECISIONS_EPISODE1.md` — **story decisions** (characters, metaphors, scene beats) — read first
- `episode1\episode1_script_part1.md` — full Episode 1 script (Part 1 / first half; ends at the B&W transition — **second half NOT written yet** = the work above)
- `episode1\episode1_first_half.md` — first-half sequence summary
- `episode1\narrative_map.md` — characters, symbols, concept map
- `episode1\first_script.md` + `episode1\episode1_structure_prompt.txt` — earlier outline + the Gemma structure prompt (@8106)
- `episode1\workflows\` — reusable Episode 1 workflow JSONs (see its README)
- `docs\` — pipeline guides; `utilities\commit_md.ps1` — daily .md safety-commit (D131)
