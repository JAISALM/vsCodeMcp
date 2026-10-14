# EPISODE 1 — Project Hub

**The one-stop folder for everything Episode 1.** When creating workflows, prompts,
keyframes, or resuming work on Episode 1, read here first.

## Files

| File | What it is |
|---|---|
| `DECISIONS_EPISODE1.md` | **Story-specific decisions** (metaphors, characters, tone, scene-level choices). Read this BEFORE building any workflow for a scene. |
| `narrative_map.md` | Characters, plot arc, cinematic motifs (the map of the whole episode). |
| `episode1_script_part1.md` | **Current full script** — Part 1 / first half. Ends at the B&W transition. **Second half NOT written yet.** |
| `episode1_first_half.md` | First-half sequence summary (scene beats). |
| `first_script.md` | The earlier full outline (Acts I–III) — the structural skeleton the current script grew from. |
| `episode1_structure_prompt.txt` | The Gemma4-31B QAT structure-document prompt (run fresh at port 8106) — the director's synopsis verbatim + what to produce. |
| `workflows/` | Reusable ComfyUI workflow JSONs for Episode 1 (see `workflows/README.md`). |

## The three acts (current understanding)

1. **Present — Kerala 2026:** muddy paddy field / academy ground. Jaisal (tactics/IQ) vs
   Zidhan (Kaalappoott/physicality). Stakes: saving the academy, winning the fives final.
2. **Mind-trip — 1950 World Cup:** the watch triggers the jump. Jaisal applies 2026
   tactical IQ to a 1950 India team in Brazil.
3. **The lesson + return:** India loses 3-1 to Brazil → IQ dominates the game,
   Physicality wins the final → Jaisal returns to 2026 and accepts reality → the 5s team wins.

## Rules that apply to ALL Episode 1 work

- **NO MUSIC** (D041, permanent): no score/instruments/melody/beat anywhere — natural
  ambient sounds only (see AGENTS.md).
- Working models: Gemma4-31B writer @8106 · Qwen3.8-27B agent @8100 · RTX 5090 (32 GB).
- Resume state: `project-memory\CURRENT_TASK.md` (milestones + pending technicals).
