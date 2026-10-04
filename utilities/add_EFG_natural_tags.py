import json, os, shutil

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
BAK_DIR = r"d:\models\vsCodeMcp\workflow_backups"
PROMPT_DIR = r"d:\models\vsCodeMcp\Jaisal-intro\prompts"
os.makedirs(BAK_DIR, exist_ok=True)

# (workflow, prompt_file, [(old, new), ...])
EDITS = [
    ("jaisal_intro_E_plants.json", "shot_E_plants_grow_v4_micro.txt", [
        # beat 1: throat-clear before the first line
        ("<Subject 1> (S1) says, <d>[English] <breath> No real purpose. <pause> Just telling stories. <pause> Sharing stories. </d>",
         "<Subject 1> (S1) says, <d>[English] <clears throat> No real purpose. <pause> Just telling stories. <breath> Sharing stories. </d>"),
        # beat 2: a small hesitation
        ("He continues speaking, <d>[English] The stories happening around us, <pause> the ones we lived, <breath> the ones we know by hearsay. </d>",
         "He continues speaking, <d>[English] <uh> The stories happening around us, <pause> the ones we lived, <breath> the ones we know by hearsay. </d>"),
    ]),
    ("jaisal_intro_F_plants_die.json", "shot_F_plants_die_v2_micro.txt", [
        # Jaisal's first line: gathers his words with a throat-clear
        ("<Subject 1> (S1) says, <d>[English] <long pause> Cinema... <pause> or if you want to tell a story... </d>",
         "<Subject 1> (S1) says, <d>[English] <long pause> <clears throat> Cinema... <pause> or if you want to tell a story... </d>"),
        # the lonely beat: a sigh
        ("<Subject 1> (S1) says, <d>[English] I'm alone right now. <long pause> So there are some limitations to what I can do. </d>",
         "<Subject 1> (S1) says, <d>[English] <sighs> I'm alone right now. <long pause> So there are some limitations to what I can do. </d>"),
    ]),
    ("jaisal_intro_G_papers.json", "shot_G_papers_v2_micro.txt", [
        # Jaisal's first line: throat-clear
        ("<Subject 1> (S1) says, <d>[English] As I said... <pause> stories, politics, sports, <pause> and a little bit of fantasy. </d>",
         "<Subject 1> (S1) says, <d>[English] <clears throat> As I said... <pause> stories, politics, sports, <pause> and a little bit of fantasy. </d>"),
        # the uncertain beat: a sigh
        ("<Subject 1> (S1) says, <d>[English] I don't know if it'll work... <long pause> Let's see. </d>",
         "<Subject 1> (S1) says, <d>[English] <sighs> I don't know if it'll work... <long pause> Let's see. </d>"),
    ]),
]

for fname, pfile, pairs in EDITS:
    path = os.path.join(BASE, fname)
    with open(path, "r", encoding="utf-8") as f:
        wf = json.load(f)
    shutil.copy(path, os.path.join(BAK_DIR, fname + ".pre_natural_tags.bak"))
    for n in wf["nodes"]:
        if n["id"] == 138:
            p = n["widgets_values"][0]
            for old, new in pairs:
                if old not in p:
                    print("!! NOT FOUND in", fname, ":", old[:60])
                else:
                    p = p.replace(old, new)
            n["widgets_values"] = [p]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False)
    with open(os.path.join(PROMPT_DIR, pfile), "w", encoding="utf-8") as f:
        f.write(p)
    print("Updated", fname, "->", pfile)

print("DONE. Backups in", BAK_DIR)
