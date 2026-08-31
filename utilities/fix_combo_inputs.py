import json, os, shutil

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
BACKUP = r"d:\models\vsCodeMcp\workflow_backups\pre_combo_fix"

MACHINE_BUILT = [
    "jaisal_shot1_t2i.json","jaisal_shot2_i2i.json","jaisal_shot3_i2i.json",
    "jaisal_sketch_shot1_i2i.json","jaisal_sketch_shot2_i2i.json","jaisal_sketch_shot3_i2i.json",
    "krea2_jaisal_aerial_v4.json","krea2_jaisal_aerial_v5.json","krea2_jaisal_continuity.json",
    "krea2_jaisal_face.json","krea2_jaisal_face_v2.json","krea2_jaisal_face_v3.json",
    "krea2_jaisal_final_aerial.json","krea2_jaisal_fix05_inpaint.json","krea2_jaisal_fix05_tie.json",
    "krea2_jaisal_longshot.json","krea2_jaisal_medium.json","krea2_jaisal_storysheet.json",
    "krea2_jaisal_storysheet_v2.json","krea2_jaisal_title_moody.json","jaisal_drone_optimized.json",
]

# The native LoadImage 'upload' input object (the file-picker button)
UPLOAD_INPUT = {
    "localized_name": "choose file to upload",
    "name": "upload",
    "type": "IMAGEUPLOAD",
    "widget": {"name": "upload"},
    "link": None,
}

os.makedirs(BACKUP, exist_ok=True)
print("=== FIXING COMBO INPUTS + LoadImage upload ===\n")
grand_combo = 0
grand_upload = 0
for fname in MACHINE_BUILT:
    p = os.path.join(BASE, fname)
    if not os.path.exists(p):
        print(f"*** MISSING: {fname}")
        continue
    shutil.copy2(p, os.path.join(BACKUP, fname))
    wf = json.load(open(p, encoding="utf-8"))
    combo_fixes = 0
    upload_fixes = 0
    for n in wf["nodes"]:
        # 1) Convert static-list combo inputs to type='COMBO'
        #    (only widget inputs — those have a 'widget' field; link inputs don't)
        for i in n.get("inputs", []):
            if isinstance(i.get("type"), list) and "widget" in i:
                i["type"] = "COMBO"
                combo_fixes += 1
        # 2) Ensure LoadImage has the 'upload' input (file-picker button)
        if n["type"] == "LoadImage":
            has_upload = any(i.get("name") == "upload" for i in n.get("inputs", []))
            if not has_upload:
                n["inputs"].append(dict(UPLOAD_INPUT))
                upload_fixes += 1
    json.dump(wf, open(p, "w", encoding="utf-8"), indent=1)
    grand_combo += combo_fixes
    grand_upload += upload_fixes
    print(f"### {fname}: {combo_fixes} combo->COMBO, {upload_fixes} upload added")

print(f"\n=== TOTAL: {grand_combo} combo fixes, {grand_upload} upload inputs added ===")
print(f"Backups in: {BACKUP}")
