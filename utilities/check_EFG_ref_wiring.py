import json
base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
for f in ["jaisal_intro_E_plants.json", "jaisal_intro_F_plants_die.json", "jaisal_intro_G_papers.json"]:
    wf = json.load(open(base + "\\" + f, encoding="utf-8"))
    print("=====", f, "=====")
    for n in wf["nodes"]:
        if n["id"] in (136, 137, 139):
            print(" node", n["id"], n["type"], "mode=", n.get("mode"), "widgets=", n.get("widgets_values"))
            for i in n.get("inputs", []):
                if i.get("name") in ("ref_image_0", "ref_image_1", "ref_image_2", "image"):
                    print("   input", i["name"], "link=", i.get("link"))
    # links touching 137/139
    for l in wf["links"]:
        if l[1] in (137, 139) or l[3] in (137, 139):
            print("   link", l)
    print()
