import io

p = r'd:\models\vsCodeMcp\project-memory\CURRENT_TASK.md'
s = io.open(p, encoding='utf-8').read()

s = s.replace(
    'Last Updated: 2026-09-28 (G split into G1 burst + G2 aftermath, both built + validated)',
    'Last Updated: 2026-09-28 (G = single 11s SEQUENTIAL take G_revolt, built + validated; G1/G2 split superseded)'
)

entry = '''- **2026-09-28 (LATEST) — G = SINGLE 11s SEQUENTIAL take `jaisal_intro_G_revolt.json` (D096) — BUILT + VALIDATED, AWAITING USER RUN:** user corrected the G1/G2 split: "the main idea is to do one action at a time. the burst should happen after the question is asked... the burst itself has 9 seconds, this is wrong... the bat has to come when we say one dialogue, the ball etc." **The real structure (user's pasted prompt): ONE continuous 11s take, SEQUENTIAL not simultaneous:** (1) camera guy asks the question FIRST (00:00–00:01, Malayalam "ഈ ചാനൽ നിന്ന് ആൾക്കാർക്ക് എന്തൊക്കെ എക്സ്പെക്ട് ചെയ്യാം?"); (2) each object triggered by its SPECIFIC WORD — PAPERS for "കഥകൾ" (stories, 00:02–00:03), MICROPHONE for "രാഷ്ട്രീയം" (politics, 00:03–00:04), CRICKET BAT + SOCCER BALL for "കായികം" (sports, 00:04–00:05), PAPER SMILEY on the bat for "fantasy" (00:06–00:07); (3) ONE ACTION AT A TIME — NOT a 9s paper explosion; the PAUSE after each word gives MiniMax time to physically appear + settle each object; (4) Jaisal REMAINS PRESENT through the whole object sequence (he watches them) and DISAPPEARS at ONE clean moment on "നോക്കാം" (00:09–00:10) — chair empty, objects remain; (5) camera guy answers "നോക്കാം" (00:10–00:11), bulb flickers, CUT TO BLACK. **BUILT `jaisal_intro_G_revolt.json` (11s/264f, 1344×768, 5 refs: kf7a_v4 start, mic+paper end, obj_cricket_bat, obj_soccer_ball, obj_paper_smiley; latent Load clip 7 → Save clip 8) via `utilities/build_G_revolt_11s.py` (clones G_papers, length 360→264, swaps prompt). Prompt: `Jaisal-intro/prompts/shot_G_revolt_11s.txt` (Malayalam dialogue, per-second timeline, OBJECT PHYSICS section, MICRO-EXPRESSIONS per beat, negatives: simultaneous object appearance / continuous paper explosion / Jaisal disappearing early / humanoid paper / camera movement). Validates clean (0 errors, 29 nodes, 2 harmless orphan-math warnings 131/132).** **Chain now A(1)→B(2)→C(3)→D(4)→E(5)→F1(6)→F2(7)→G(8).** **SUPERSEDED (do NOT run):** D095 G1/G2 split (`jaisal_intro_G1_burst.json`, `jaisal_intro_G2_aftermath.json`), `jaisal_intro_G_papers.json` (15s), `jaisal_intro_G_vanish_burst.json` (old 3s) — keep as backups. **NEXT (user, stop Qwen first, fresh tab):** (1) `Stop-Process -Name "llama-server" -Force`; (2) **stage F2's last frame** (if not already): `seedvr2_lastframe_2k.json` (LoadVideo = F2 take) → `output\\lastframe_2k_00001_.png` → copy to `input\\` (G's ref_image_0 is `kf7a_v4.png` — if F2's actual last frame looks better, set G node 137 to it); (3) run **G_revolt** (fresh tab) → judge: question first? objects appear ONE AT A TIME on their words (papers→mic→bat+ball→smiley)? Jaisal PRESENT through the sequence? clean disappearance on "നോക്കാം" (chair empty)? camera guy "നോക്കാം" + bulb flicker? → `clip_00008`; (4) `Start-Process "D:\\models\\qwen\\Qwen3.827BMTP.bat"`. **THEN FINAL ASSEMBLY:** concatenate A→B→C→D→E→F1→F2→G (Trim removes 22 pinned head frames) → single 2K upscale (4x-UltraSharp non-generative) → post audio (ambient + dubs, **NO MUSIC D041**). **RULES:** NO MUSIC (D041); user runs GPU jobs (I never stop Qwen); artifacts in `Jaisal-intro\\`; fresh tabs; check `Get-Process llama-server` before any run.

'''

marker = '## RESUME POINT (read this first)\n'
if marker in s:
    # demote the previous LATEST (G1/G2 split) entry
    s = s.replace(
        '- **2026-09-28 (LATEST) — G SPLIT INTO G1 (burst) + G2 (aftermath) (D095) — BUILT + VALIDATED, AWAITING USER RUNS:**',
        '- **2026-09-28 — G SPLIT INTO G1 (burst) + G2 (aftermath) (D095) — SUPERSEDED by single 11s G_revolt (D096):**'
    )
    s = s.replace(marker, marker + '\n' + entry)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('CURRENT_TASK updated with G_revolt')
else:
    print('marker not found')
