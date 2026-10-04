"""Shot A: move the no-music constraint to the TOP of the prompt (user 2026-09-27:
"there is still music coming, we should add the prompt first not at the last buried,
check minimax prompt guide").

Per docs/MINIMAX_H3_R2V_PROMPTING_GUIDE.md (line ~190): H3 weights the FIRST FEW
LINES most; a constraint buried in the middle/end "gets treated as background and
ignored". So insert a MANDATORY AUDIO CONSTRAINT block at the VERY TOP of node 138
(before subject_definitions). The existing bottom sections stay as reinforcement.

Backup: workflow_backups/jaisal_intro_A_walkin.json.pre_nomusic_top.bak
"""
import json
import shutil

WF_A = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_intro_A_walkin.json.pre_nomusic_top.bak"

shutil.copy(WF_A, BAK)
wf = json.load(open(WF_A, encoding="utf-8"))
node = next(n for n in wf["nodes"] if n["id"] == 138)
p = node["widgets_values"][0]

TOP_BLOCK = (
    "MANDATORY AUDIO CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: the audio of this "
    "video is PURELY NATURAL AMBIENT SOUND ONLY. NO music of any kind. NO "
    "instruments. NO guitar, NO plucked strings, NO strumming, NO strings, NO "
    "piano, NO drums, NO melody, NO tune, NO beat, NO rhythm, NO humming, NO "
    "singing, NO voice, NO speech, NO musical tone of any kind. The ONLY sounds "
    "allowed are: low room tone, the faint electric hum of a bare bulb, a soft "
    "chair scrape on wood, a gentle breath, the quiet creak of the chair "
    "settling. This constraint OVERRIDES every other instruction in this prompt.\n\n"
)

anchor = "subject_definitions:"
assert anchor in p, "anchor not found"
assert "MANDATORY AUDIO CONSTRAINT" not in p, "top block already present"
p = p.replace(anchor, TOP_BLOCK + anchor, 1)

node["widgets_values"][0] = p
with open(WF_A, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=1)
print("No-music constraint moved to the TOP of the A prompt. Backup:", BAK)
print("--- first 700 chars now ---")
print(p[:700])
