"""G prompt: strengthen paper COUNT (explicit total + negatives).

The end reference anchors the paper count (~20 papers), so the prompt's
"approximately 4-6" loses. Strengthen the count in the beat + add count
negatives. (The real fix is regenerating the reference with fewer papers —
see krea2_small_mic_ref_v2.json — but this makes the prompt push too.)
"""
import json, os

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
d = json.load(open(P, encoding="utf-8"))
n138 = [x for x in d["nodes"] if x["id"] == 138][0]
prompt = n138["widgets_values"][0]

repls = [
    # Strengthen the paper beat with an explicit TOTAL count
    (
        "a small number of loose paper sheets (approximately 4-6) suddenly appear from the darkness BEHIND Jaisal and drift physically toward the table.",
        "ONLY 4-6 loose paper sheets TOTAL in the entire shot (NOT 20, NOT papers everywhere, NOT a paper explosion) suddenly appear from the darkness BEHIND Jaisal and drift physically toward the table.",
    ),
    # Add paper-count negatives (append to the existing above-entry negatives block)
    (
        "the soccer ball falling from above, music, soundtrack, score, melody, beat, rhythm, instruments",
        "the soccer ball falling from above, 20 papers, 30 papers, dozens of papers, papers everywhere, papers filling the frame, papers covering the wall, a large number of papers, many papers, a paper explosion, music, soundtrack, score, melody, beat, rhythm, instruments",
    ),
]

applied = 0
for old, new in repls:
    if old in prompt:
        prompt = prompt.replace(old, new, 1)
        applied += 1
    else:
        print(f"!! NOT FOUND: {old[:60]!r}")

n138["widgets_values"] = [prompt]
json.dump(d, open(P, "w", encoding="utf-8"), indent=1)
print(f"applied {applied}/{len(repls)}")
print(f"prompt length: {len(prompt)}")

out = r"D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G_revolt_15s_v3_below_entry.txt"
open(out, "w", encoding="utf-8").write(prompt)
print("saved reference ->", out)
