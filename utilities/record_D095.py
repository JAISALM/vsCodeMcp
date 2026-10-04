import io

# ---- DECISIONS.md ----
p = r'd:\models\vsCodeMcp\project-memory\DECISIONS.md'
s = io.open(p, encoding='utf-8').read()
add = '''
### D095 — G split into G1 (burst) + G2 (aftermath) (2026-09-28)
- **Problem:** single 15s G kept the character "staying" — as soon as the paper burst happened the character should be GONE, but MiniMax left him in frame.
- **Decision:** split G into TWO chained shots so the hard "disappear" moment is isolated and the aftermath has NO character reference at all:
  - **G1 `jaisal_intro_G1_burst.json`** (10s/240f): ref_image_0=`kf7a_v4.png` (character at table), ref_image_1=`jaisal_gone_papers_alone.png` (papers only, empty chair). Character present -> speaks -> **BURSTS INTO papers -> GONE** by 00:08-00:10. End ref anchors "character gone". Load clip 7 (F2 tail) -> save clip 8.
  - **G2 `jaisal_intro_G2_aftermath.json`** (10s/240f): ref_image_0=`jaisal_gone_papers_alone.png` (papers only, NO character), ref_image_1=`mic+paper.png` (papers+mic), + object refs cricket bat/soccer ball/smiley paper. **NO character at all** — camera guy's off-screen voice "Let's see." + mic emerges + objects enter. Load clip 8 (G1 tail) -> save clip 9.
- **Why it works:** G2 has no character reference, so the character CANNOT "stay" — MiniMax only has papers+objects to track. The burst is isolated into G1 where the end ref (papers only) forces the character out.
- **Latent chain now:** A(1)->B(2)->C(3)->D(4)->E(5)->F1(6)->F2(7)->G1(8)->G2(9).
- **Old files superseded:** `jaisal_intro_G_papers.json` (15s single) and `jaisal_intro_G_vanish_burst.json` (old 3s) are now superseded by G1+G2.
- **Prompts:** `Jaisal-intro/prompts/shot_G1_burst_10s.txt`, `Jaisal-intro/prompts/shot_G2_aftermath_10s.txt`.
- **Build script:** `utilities/build_G1_G2_split.py` (clones G_papers, swaps refs/prompt/length/latent, removes object-ref nodes for G1).
'''
if 'D095' not in s:
    s = s.rstrip() + '\n' + add
    io.open(p, 'w', encoding='utf-8').write(s)
    print('DECISIONS D095 added')
else:
    print('D095 already present')
