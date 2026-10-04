import io

p = r'd:\models\vsCodeMcp\project-memory\CURRENT_TASK.md'
s = io.open(p, encoding='utf-8').read()

# Update the "Last Updated" line
s = s.replace(
    'Last Updated: 2026-09-28 (late — G v2 built, ready to run)',
    'Last Updated: 2026-09-28 (G split into G1 burst + G2 aftermath, both built + validated)'
)

entry = '''- **2026-09-28 (LATEST) — G SPLIT INTO G1 (burst) + G2 (aftermath) (D095) — BUILT + VALIDATED, AWAITING USER RUNS:** user ran the single 15s G (`jaisal_intro_G_papers.json`) → **character STAYED** (as soon as the paper burst happened the character should be GONE). **DIAGNOSIS:** one 15s shot asks MiniMax to hold the character, shrink plants, emerge a mic, enter 3 objects AND burst the character into papers — too many simultaneous events; the character-identity prior wins and he "stays". **FIX (user's idea, adopted): SPLIT G into TWO chained shots:**
  - **G1 = `jaisal_intro_G1_burst.json` (10s/240f):** ref_image_0=`kf7a_v4.png` (character at table, dead plants), ref_image_1=`jaisal_gone_papers_alone.png` (**papers only, empty chair — NO character**). Character present → camera-guy question → Jaisal speaks ("As I said... stories, politics, sports, fantasy" + "I don't know if it'll work... Let's see.") + plants shrink → **00:08–00:10 JAISAL BURSTS INTO papers** (body EXPLODES OUTWARD, NOT a fade) → chair EMPTY, ends on <Picture 2> (papers only). **2 refs only** (object-ref nodes 165/166/167 removed). Load clip 7 (F2 tail) → Save clip 8.
  - **G2 = `jaisal_intro_G2_aftermath.json` (10s/240f):** ref_image_0=`jaisal_gone_papers_alone.png` (**papers only — NO character at all**), ref_image_1=`mic+paper.png` (papers+mic), + object refs cricket bat/soccer ball/smiley paper (nodes 165/166/167). **NO character in the shot at any point** — camera guy's OFF-SCREEN voice "Let's see." (00:02–00:04) → mic emerges SEPARATELY (00:04–00:06) → cricket bat flies in (00:06–00:08) → soccer ball rolls in + smiley paper settles on bat (00:08–00:10) → ends on <Picture 2>. Load clip 8 (G1 tail) → Save clip 9.
  - **WHY IT WORKS:** G2 has NO character reference, so the character CANNOT "stay" — MiniMax only has papers+objects to track. The hard "disappear" moment is isolated into G1 where the END ref (papers only, empty chair) forces the character out.
  - **Built via `utilities/build_G1_G2_split.py`** (clones G_papers, swaps refs/prompt/length/latent, removes object-ref nodes for G1). **Both validate clean (0 errors; G1 26 nodes, G2 29 nodes; 2 harmless orphan-math warnings 131/132).** **Prompts:** `Jaisal-intro/prompts/shot_G1_burst_10s.txt` + `shot_G2_aftermath_10s.txt`.
  - **Latent chain now: A(1)→B(2)→C(3)→D(4)→E(5)→F1(6)→F2(7)→G1(8)→G2(9).**
  - **SUPERSEDED:** `jaisal_intro_G_papers.json` (15s single) + `jaisal_intro_G_vanish_burst.json` (old 3s) — do NOT run these.
  - **NEXT (user, stop Qwen first, fresh tabs):** (1) `Stop-Process -Name "llama-server" -Force`; (2) **stage F2's last frame** (if not already): `seedvr2_lastframe_2k.json` (LoadVideo = F2 take) → `output\\lastframe_2k_00001_.png` → copy to `input\\` (G1's ref_image_0 is `kf7a_v4.png` — the F2 last frame should match it; if F2's actual last frame differs, set G1 node 137 to that file); (3) run **G1** (fresh tab) → judge: starts on F2's ending? plants shrink while he speaks? **character BURSTS into papers and is GONE by the end (chair empty)?** paper-blast sound (not music)? → `clip_00008`; (4) **stage G1's last frame**: `seedvr2_lastframe_2k.json` (LoadVideo = G1 take) → `output\\lastframe_2k_00001_.png` → copy to `input\\` (G2's ref_image_0 is `jaisal_gone_papers_alone.png` — if G1's actual last frame is better, set G2 node 137 to it); (5) run **G2** (fresh tab) → judge: **NO character at any point?** mic emerges separately? objects enter one at a time? off-screen "Let's see."? → `clip_00009`; (6) `Start-Process "D:\\models\\qwen\\Qwen3.827BMTP.bat"`.
  - **THEN FINAL ASSEMBLY:** concatenate A→B→C→D→E→F1→F2→G1→G2 (Trim removes 22 pinned head frames) → single 2K upscale (4x-UltraSharp non-generative) → post audio (ambient + dubs, **NO MUSIC D041**).
  - **RULES:** NO MUSIC (D041); user runs GPU jobs (I never stop Qwen); artifacts in `Jaisal-intro\\`; fresh tabs; check `Get-Process llama-server` before any run.

'''

# Insert the new entry right after the "## RESUME POINT (read this first)" header
marker = '## RESUME POINT (read this first)\n'
if marker in s:
    # remove any previous copy of this entry (idempotent)
    s = s.replace(entry, '')
    # demote the old G v2 entry's LATEST tag so only one LATEST remains
    s = s.replace(
        '- **2026-09-28 (LATEST) — G v2 BUILT (15s + 5 refs + plant-shrinking) — READY TO RUN (D094 update):**',
        '- **2026-09-28 — G v2 BUILT (15s + 5 refs + plant-shrinking) — SUPERSEDED by G1+G2 split (D095):**'
    )
    s = s.replace(marker, marker + '\n' + entry)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('CURRENT_TASK updated with G1/G2 split')
else:
    print('marker not found')
