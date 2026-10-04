import io

p = r'd:\models\vsCodeMcp\project-memory\CURRENT_TASK.md'
s = io.open(p, encoding='utf-8').read()

marker = '## G1 issues fixed in prompt (2026-09-15, D094b)'
if marker in s:
    print('already present')
    raise SystemExit

block = """
## G1 issues fixed in prompt (2026-09-15, D094b)
G1 came out: (1) music instead of paper-blast sound, (2) Jaisal FADED (opacity) instead of bursting, (3) mic came WITH the paper burst.
Prompt fixes in shot_G_papers_v2_15s.txt (synced to workflow, validated clean):
- Paper-blast sound: LOUD natural PAPER BLAST (rustling/whooshing) + 'NOT music' on the burst.
- Burst not fade: Jaisal BURSTS INTO papers (body EXPLODES OUTWARD) + NEGATIVE 'fading/dissolving/opacity reducing'.
- Mic separate: emerges SEPARATELY from the dark at 00:07-00:09 + NEGATIVE 'mic appearing together with paper burst / before 00:07'.
"""

# Update the NEXT block's G line to mention the fixes
s = s.replace(
    'Run **G** (fresh tab) -> judge: plants shrink while he speaks? mic emerges separately? Jaisal bursts into papers (not fade)? paper-blast sound (not music)? -> clip_00008',
    'Run **G** (fresh tab) -> judge: plants shrink while he speaks? mic emerges SEPARATELY (not with paper burst)? Jaisal BURSTS into papers (not fade)? paper-blast sound (not music)? -> clip_00008'
)
s = s.rstrip() + '\n' + block
io.open(p, 'w', encoding='utf-8').write(s)
print('CURRENT_TASK updated')
