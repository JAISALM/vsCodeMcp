"""G prompt v3: objects (mic, bat, ball) enter from BELOW/BEHIND, NOT from above.

User (2026-09-29): "the football, bat and mic has to come from below / behind the
person, not from above the frame. that's the only correction. the way he dissolves
is kind of ok now."

So: ONLY change the object-ENTRY DIRECTION for mic/bat/ball (below/behind, not
above). Do NOT touch the dissolve (it's OK now). Add a global entry-direction rule
+ negatives.
"""
import json, os

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
d = json.load(open(P, encoding="utf-8"))
n138 = [x for x in d["nodes"] if x["id"] == 138][0]
prompt = n138["widgets_values"][0]

repls = [
    # MIC beat: specify below/behind entry
    (
        "a SMALL COMPACT MICROPHONE on a SHORT stand suddenly emerges from the darkness and settles LOW on the table",
        "a SMALL COMPACT MICROPHONE on a SHORT stand suddenly rises up from BELOW the table, from the darkness behind and below Jaisal's lower body (NOT from above the frame, NOT falling from the top), and settles LOW on the table",
    ),
    # BAT beat: specify below/behind entry
    (
        "a CRICKET BAT (<Picture 3>) suddenly flies into the illuminated area and settles.",
        "a CRICKET BAT (<Picture 3>) rises up from BELOW the table, from the darkness behind and below Jaisal (NOT from above the frame, NOT falling from the top), and settles in the illuminated area.",
    ),
    # BALL beat: specify below/behind entry
    (
        "a round SOCCER BALL (<Picture 4>) rolls into the light and settles.",
        "a round SOCCER BALL (<Picture 4>) rolls in from BELOW, from the darkness behind and below Jaisal (NOT from above the frame, NOT falling from the top), and settles in the light.",
    ),
    # Global entry-direction rule (insert into OBJECT PHYSICS section)
    (
        "OBJECT PHYSICS (real, physically grounded)\nAll objects are REAL PHYSICAL OBJECTS",
        "OBJECT ENTRY DIRECTION (CRITICAL — below/behind, NEVER above)\nThe microphone, cricket bat and soccer ball ALL enter from BELOW the table and from the darkness BEHIND and BELOW Jaisal's lower body. They rise up / roll in from the lower part of the frame. They NEVER fall from above, NEVER drop from the top of the frame, NEVER float down from the ceiling or from above Jaisal's head. The papers drift in from behind Jaisal.\n\nOBJECT PHYSICS (real, physically grounded)\nAll objects are REAL PHYSICAL OBJECTS",
    ),
    # Negatives: forbid above-entry
    (
        "NEGATIVE\nmusic, soundtrack, score, melody, beat, rhythm, instruments",
        "NEGATIVE\nobjects falling from above, objects dropping from the top of the frame, objects entering from above, objects floating down from the ceiling, objects falling from above Jaisal's head, the microphone falling from above, the cricket bat falling from above, the soccer ball falling from above, music, soundtrack, score, melody, beat, rhythm, instruments",
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
print(f"applied {applied}/{len(repls)} replacements")
print(f"prompt length: {len(prompt)}")

# also save a reference copy
out = r"D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G_revolt_15s_v3_below_entry.txt"
open(out, "w", encoding="utf-8").write(prompt)
print("saved reference ->", out)
