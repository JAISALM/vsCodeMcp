import json, os, shutil

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
BAK_DIR = r"d:\models\vsCodeMcp\workflow_backups"
os.makedirs(BAK_DIR, exist_ok=True)

FILES = ["jaisal_intro_E_plants.json", "jaisal_intro_F_plants_die.json", "jaisal_intro_G_papers.json"]

for fname in FILES:
    path = os.path.join(BASE, fname)
    with open(path, "r", encoding="utf-8") as f:
        wf = json.load(f)
    shutil.copy(path, os.path.join(BAK_DIR, fname + ".pre_rewire_ref1.bak"))

    def find(nid):
        for n in wf["nodes"]:
            if n["id"] == nid: return n
        raise KeyError(nid)

    n136 = find(136)
    n139 = find(139)

    # 1. un-bypass node 139
    n139["mode"] = 0

    # 2. new link id above the REAL max
    max_lid = max(l[0] for l in wf["links"])
    new_lid = max_lid + 1

    # 3. wire 139 IMAGE -> 136 slot 4 (ref_image_1)
    slot4 = n136["inputs"][4]
    assert slot4["name"] == "ref_images.ref_image_1", slot4["name"]
    slot4["link"] = new_lid
    n139["outputs"][0]["links"] = [new_lid]
    wf["links"].append([new_lid, 139, 0, 136, 4, "IMAGE"])
    wf["last_link_id"] = max(wf.get("last_link_id", 0), new_lid)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False)
    print(fname, "-> node 139 un-bypassed, link", new_lid, "139->136.ref_image_1")

print("DONE. Backups in", BAK_DIR)
