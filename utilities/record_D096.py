import io

# ---- DECISIONS.md ----
p = r'd:\models\vsCodeMcp\project-memory\DECISIONS.md'
s = io.open(p, encoding='utf-8').read()
add = '''
### D096 — G = SINGLE 11s SEQUENTIAL take (supersedes D095 G1/G2 split) (2026-09-28)
- **User correction:** the G1/G2 split was overcomplicating it. The real structure (from the user's pasted prompt) is ONE continuous 11s take where the transformation is SEQUENTIAL, not simultaneous:
  1. Camera guy asks the question FIRST (00:00–00:01).
  2. Each object is triggered by its SPECIFIC WORD: PAPERS for "കഥകൾ" (stories, 00:02–00:03), MICROPHONE for "രാഷ്ട്രീയം" (politics, 00:03–00:04), CRICKET BAT + SOCCER BALL for "കായികം" (sports, 00:04–00:05), PAPER SMILEY on the bat for "fantasy" (00:06–00:07).
  3. ONE ACTION AT A TIME — NOT a 9-second paper explosion. The PAUSE after each word gives MiniMax time to physically appear + settle each object.
  4. Jaisal REMAINS PRESENT through the whole object sequence and DISAPPEARS at ONE clean moment on "നോക്കാം" (00:09–00:10) — chair empty, objects remain.
  5. Camera guy answers "നോക്കാം" (00:10–00:11), bulb flickers, CUT TO BLACK.
- **Why the split was wrong:** splitting into G1 (burst) + G2 (aftermath) put the object-entrances in G2 with NO character, but the user wants the character PRESENT while the objects appear (he watches them), and the disappearance is ONE clean beat, not a "burst". The sequential single take keeps the character in frame for the whole object sequence.
- **Built:** `jaisal_intro_G_revolt.json` (11s/264f, 1344×768, 5 refs: kf7a_v4 start, mic+paper end, obj_cricket_bat, obj_soccer_ball, obj_paper_smiley). Latent: Load clip 7 (F2 tail) → Save clip 8. Prompt: `Jaisal-intro/prompts/shot_G_revolt_11s.txt`. Built via `utilities/build_G_revolt_11s.py` (clones G_papers, length 360→264, swaps prompt). Validates clean (0 errors, 29 nodes).
- **Chain now A(1)→B(2)→C(3)→D(4)→E(5)→F1(6)→F2(7)→G(8).** (G = single 11s take, NOT G1+G2.)
- **SUPERSEDED:** D095 G1/G2 split (`jaisal_intro_G1_burst.json`, `jaisal_intro_G2_aftermath.json`) — keep as backups, do NOT run. `jaisal_intro_G_papers.json` (15s) + `jaisal_intro_G_vanish_burst.json` (old 3s) also superseded.
- **KEY LESSON:** for a shot where a character watches a SEQUENCE of objects appear, keep it ONE continuous take with the character PRESENT, trigger each object by its specific word, use pauses + micro-expressions to give MiniMax time per object, and make the disappearance ONE clean beat (not a burst). Do NOT split into character-present + character-absent shots.
'''
if 'D096' not in s:
    s = s.rstrip() + '\n' + add
    io.open(p, 'w', encoding='utf-8').write(s)
    print('DECISIONS D096 added')
else:
    print('D096 already present')
