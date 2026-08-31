import json, os, shutil

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
BACKUP = r"d:\models\vsCodeMcp\workflow_backups\pre_widget_fix"

# All machine-built workflows (built/converted by us, NOT native UI-saved)
MACHINE_BUILT = [
    "jaisal_shot1_t2i.json",
    "jaisal_shot2_i2i.json",
    "jaisal_shot3_i2i.json",
    "jaisal_sketch_shot1_i2i.json",
    "jaisal_sketch_shot2_i2i.json",
    "jaisal_sketch_shot3_i2i.json",
    "krea2_jaisal_aerial_v4.json",
    "krea2_jaisal_aerial_v5.json",
    "krea2_jaisal_continuity.json",
    "krea2_jaisal_face.json",
    "krea2_jaisal_face_v2.json",
    "krea2_jaisal_face_v3.json",
    "krea2_jaisal_final_aerial.json",
    "krea2_jaisal_fix05_inpaint.json",
    "krea2_jaisal_fix05_tie.json",
    "krea2_jaisal_longshot.json",
    "krea2_jaisal_medium.json",
    "krea2_jaisal_storysheet.json",
    "krea2_jaisal_storysheet_v2.json",
    "krea2_jaisal_title_moody.json",
    "jaisal_drone_optimized.json",
]

os.makedirs(BACKUP, exist_ok=True)

print("=== APPLYING NATIVE WIDGET SHAPE FIX ===\n")
grand = 0
for fname in MACHINE_BUILT:
    p = os.path.join(BASE, fname)
    if not os.path.exists(p):
        print(f"*** MISSING: {fname}")
        continue
    # backup original
    shutil.copy2(p, os.path.join(BACKUP, fname))
    wf = json.load(open(p, encoding="utf-8"))
    changes = []
    for n in wf["nodes"]:
        t = n["type"]
        wv = n.get("widgets_values")
        # KSampler: 6 -> 7 (insert hidden control_after_generate at index 1)
        if t == "KSampler" and isinstance(wv, list) and len(wv) == 6:
            wv.insert(1, "randomize")
            changes.append(f"KSampler[{n['id']}]: 6->7")
        # LoadImage: 1 -> 2 (append literal 'image')
        if t == "LoadImage" and isinstance(wv, list) and len(wv) == 1:
            wv.append("image")
            changes.append(f"LoadImage[{n['id']}]: 1->2")
        # remove widgets_values_named (native files don't have it)
        if "widgets_values_named" in n:
            del n["widgets_values_named"]
            changes.append(f"{t}[{n['id']}]: -named")
    json.dump(wf, open(p, "w", encoding="utf-8"), indent=1)
    grand += len(changes)
    print(f"### {fname} ({len(wf['nodes'])} nodes) -> {len(changes)} changes")
    for c in changes:
        print(f"     {c}")
    print()

print(f"=== TOTAL: {grand} changes across {len(MACHINE_BUILT)} files ===")
print(f"Backups in: {BACKUP}")
