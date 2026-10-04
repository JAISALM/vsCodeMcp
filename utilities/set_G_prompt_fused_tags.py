"""G prompt: FUSE emotion tags INSIDE the <d> dialogue lines (guide Rule 2),
and remove the separate MICRO-EXPRESSIONS section (now redundant).

User (2026-09-29): "micro expression has to give within the dialogue... not as a
separate section right? which will work... update the prompt in the workflow, it
should be reflecting in ui so that i can run it in ui."

NO MUSIC (D041): only natural-speech tags (<breath>, <pause>, <sighs>, <i>, ...).
NO <humming>/melody tags.
"""
import json, os, re

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
d = json.load(open(P, encoding="utf-8"))
n138 = [x for x in d["nodes"] if x["id"] == 138][0]
prompt = n138["widgets_values"][0]

# --- 1) FUSE emotion tags inside the Jaisal dialogue lines ---
# (unique lines: exact-string replace)
dialogue = [
    # stories
    ("<d>[Malayalam] പറഞ്ഞപോലെ... കഥകൾ... </d>",
     "<d>[Malayalam] <breath> പറഞ്ഞപോലെ... <i>കഥകൾ</i>... </d>"),
    # politics
    ("<d>[Malayalam] രാഷ്ട്രീയം... </d>",
     "<d>[Malayalam] <pause> <i>രാഷ്ട്രീയം</i>... </d>"),
    # sports
    ("<d>[Malayalam] കായികം... </d>",
     "<d>[Malayalam] <breath> <i>കായികം</i>... </d>"),
    # then
    ("<d>[Malayalam] പിന്നെ... </d>",
     "<d>[Malayalam] <pause> പിന്നെ... </d>"),
    # fantasy
    ("<d>[Malayalam] അല്ലറ ചില്ലറ fantasy... </d>",
     "<d>[Malayalam] <breath> അല്ലറ ചില്ലറ <i>fantasy</i>... </d>"),
    # this is what I mean
    ("<d>[Malayalam] ഇതൊക്കെയാണ് ഉദ്ദേശിക്കുന്നത്. </d>",
     "<d>[Malayalam] <pause> ഇതൊക്കെയാണ് ഉദ്ദേശിക്കുന്നത്. </d>"),
    # I don't know if it'll work
    ("<d>[Malayalam] നടക്കുമോ എന്നറിയില്ല... </d>",
     "<d>[Malayalam] <sighs> നടക്കുമോ <i>എന്നറിയില്ല</i>... </d>"),
]
applied = 0
for old, new in dialogue:
    if old in prompt:
        prompt = prompt.replace(old, new, 1)
        applied += 1
    else:
        print(f"!! NOT FOUND: {old!r}")

# Jaisal's "നോക്കാം" (00:11-00:12) — context-anchored (the camera guy's line is
# identical but DUBBED IN POST, so leave it untagged).
jaisal_nokkam_old = "He says, <d>[Malayalam] നോക്കാം. </d>"
jaisal_nokkam_new = "He says, <d>[Malayalam] <breath> നോക്കാം. </d>"
if jaisal_nokkam_old in prompt:
    prompt = prompt.replace(jaisal_nokkam_old, jaisal_nokkam_new, 1)
    applied += 1
else:
    print("!! NOT FOUND: Jaisal നോക്കാം context")

# --- 2) Remove the separate MICRO-EXPRESSIONS section (now redundant) ---
# Remove from the "MICRO-EXPRESSIONS" header up to (not including) the next
# section header "AUDIO — FINAL HARD OVERRIDE".
pattern = re.compile(
    r"MICRO-EXPRESSIONS \(the performance that makes it feel real\).*?(?=AUDIO — FINAL HARD OVERRIDE)",
    re.DOTALL,
)
m = pattern.search(prompt)
if m:
    prompt = pattern.sub("", prompt, count=1)
    section_removed = True
else:
    section_removed = False
    print("!! MICRO-EXPRESSIONS section not found")

n138["widgets_values"] = [prompt]
json.dump(d, open(P, "w", encoding="utf-8"), indent=1)
print(f"dialogue tags applied: {applied}/{len(dialogue)+1}")
print(f"MICRO-EXPRESSIONS section removed: {section_removed}")
print(f"prompt length: {len(prompt)}")

out = r"D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G_revolt_15s_v4_fused_tags.txt"
open(out, "w", encoding="utf-8").write(prompt)
print("saved reference ->", out)
