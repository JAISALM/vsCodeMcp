"""G prompt v5: (1) first 2s = WAITING beat with breath in the space;
(2) word->object LOCK (objects appear exactly ON the word, same breath).

User (2026-09-29): "we are not waiting in the first 2 second... we need that
breath in space... the items are not coming as he speaks, lets try this one last
time."
"""
import json, os

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
d = json.load(open(P, encoding="utf-8"))
n138 = [x for x in d["nodes"] if x["id"] == 138][0]
prompt = n138["widgets_values"][0]

repls = [
    # (1) FIRST 2 SECONDS = WAITING BEAT with breath in the space
    (
        "[Shot 1] 00:00–00:03 — Jaisal is SILENT, his mouth COMPLETELY CLOSED, he only LISTENS. His eyes are toward the camera, a small thoughtful look, a quiet heavy expression. (The camera guy's question is DUBBED IN POST — it is NOT spoken in this video.) NO objects appear during this beat.",
        "[Shot 1] 00:00–00:02 — a WAITING BEAT. Jaisal sits completely still at the table, his mouth COMPLETELY CLOSED, his eyes toward the camera, a small thoughtful look, a quiet heavy expression. He is LISTENING to an off-screen voice (the camera guy's question — DUBBED IN POST, NOT spoken in this video, Jaisal does NOT speak it). In the space of this beat, one quiet <breath> — a slow, natural inhale as he listens, his shoulders barely moving. NOTHING appears. NO objects, NO papers, NO movement except the breath. The stillness holds.\n[Shot 1] 00:02–00:03 — the listening continues, his eyes shift slightly, a small nod of understanding, still SILENT, mouth closed. NO objects appear during this beat.",
    ),
    # (2) WORD->OBJECT LOCK: papers appear EXACTLY on the word, same breath
    (
        "As he says \"കഥകൾ\", ONLY 4-6 loose paper sheets TOTAL in the entire shot (NOT 20, NOT papers everywhere, NOT a paper explosion) suddenly appear from the darkness BEHIND Jaisal and drift physically toward the table.",
        "The papers appear EXACTLY ON the word \"കഥകൾ\" — in the SAME BREATH as he speaks it, NOT before, NOT after: ONLY 4-6 loose paper sheets TOTAL in the entire shot (NOT 20, NOT papers everywhere, NOT a paper explosion) suddenly appear from the darkness BEHIND Jaisal at the exact moment the word lands, and drift physically toward the table.",
    ),
    # (2) mic appears EXACTLY on the word
    (
        "THIS WORD TRIGGERS THE SECOND VISUAL EVENT: a SMALL COMPACT MICROPHONE on a SHORT stand suddenly rises up from BELOW the table",
        "THE MICROPHONE APPEARS EXACTLY ON THE WORD \"രാഷ്ട്രീയം\" — in the SAME BREATH as he speaks it, NOT before, NOT after: a SMALL COMPACT MICROPHONE on a SHORT stand suddenly rises up from BELOW the table",
    ),
    # (2) bat + ball appear EXACTLY on the word
    (
        "THIS WORD TRIGGERS THE THIRD VISUAL EVENT: a CRICKET BAT (<Picture 3>) rises up from BELOW the table",
        "THE CRICKET BAT APPEARS EXACTLY ON THE WORD \"കായികം\" — in the SAME BREATH as he speaks it, NOT before, NOT after: a CRICKET BAT (<Picture 3>) rises up from BELOW the table",
    ),
    # (2) smiley paper appears EXACTLY on the word
    (
        "THIS IS THE FANTASY MOMENT: one sheet of PAPER with a simple curved smile line (<Picture 5>) moves upward and gently settles on top of the cricket bat",
        "THIS IS THE FANTASY MOMENT — the smiley paper appears EXACTLY ON THE WORD \"fantasy\", in the SAME BREATH as he speaks it, NOT before, NOT after: one sheet of PAPER with a simple curved smile line (<Picture 5>) moves upward and gently settles on top of the cricket bat",
    ),
    # Global word->object lock rule (insert before OBJECT ENTRY DIRECTION)
    (
        "OBJECT ENTRY DIRECTION (CRITICAL — below/behind, NEVER above)",
        "WORD-TO-OBJECT LOCK (CRITICAL — objects appear EXACTLY on the word)\nEvery object appears in the SAME BREATH as the word that triggers it — NOT before the word, NOT after the word, NOT during the pause. The word lands, and in that exact moment the object appears. There is a clear PAUSE between each word and the next object. If an object appears before its word or during a silent beat, it is WRONG.\n\nOBJECT ENTRY DIRECTION (CRITICAL — below/behind, NEVER above)",
    ),
    # Negatives: objects before their word / during the waiting beat
    (
        "objects appearing before 00:03, microphone before politics, cricket bat before sports, soccer ball before sports",
        "objects appearing before 00:03, objects appearing during the 00:00-00:02 waiting beat, objects appearing before their word, objects appearing after their word, objects appearing during a pause, papers before the word കഥകൾ, microphone before the word രാഷ്ട്രീയം, cricket bat before the word കായികം, soccer ball before the word കായികം, smiley paper before the word fantasy, microphone before politics, cricket bat before sports, soccer ball before sports",
    ),
]

applied = 0
for old, new in repls:
    if old in prompt:
        prompt = prompt.replace(old, new, 1)
        applied += 1
    else:
        print(f"!! NOT FOUND: {old[:70]!r}")

n138["widgets_values"] = [prompt]
json.dump(d, open(P, "w", encoding="utf-8"), indent=1)
print(f"applied {applied}/{len(repls)}")
print(f"prompt length: {len(prompt)}")

out = r"D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G_revolt_15s_v5_waiting_wordlock.txt"
open(out, "w", encoding="utf-8").write(prompt)
print("saved reference ->", out)
