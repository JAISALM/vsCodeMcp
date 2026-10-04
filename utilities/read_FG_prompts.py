import json
base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
for f in ["jaisal_intro_F_plants_die.json", "jaisal_intro_G_papers.json"]:
    wf = json.load(open(base + "\\" + f, encoding="utf-8"))
    p = [n for n in wf["nodes"] if n["id"] == 138][0]["widgets_values"][0]
    print("=====", f, "=====")
    print(p)
    print()
