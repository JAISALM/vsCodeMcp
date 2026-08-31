import json, os
from collections import Counter

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
broken = [
    "jaisal_shot1_t2i.json", "jaisal_shot2_i2i.json", "jaisal_shot3_i2i.json",
    "jaisal_sketch_shot1_i2i.json", "jaisal_sketch_shot2_i2i.json", "jaisal_sketch_shot3_i2i.json",
    "krea2_jaisal_aerial_v4.json", "krea2_jaisal_aerial_v5.json", "krea2_jaisal_continuity.json",
    "krea2_jaisal_face.json", "krea2_jaisal_face_v2.json", "krea2_jaisal_face_v3.json",
    "krea2_jaisal_final_aerial.json", "krea2_jaisal_fix05_inpaint.json", "krea2_jaisal_fix05_tie.json",
    "krea2_jaisal_longshot.json", "krea2_jaisal_medium.json", "krea2_jaisal_storysheet.json",
    "krea2_jaisal_storysheet_v2.json",
]
alltypes = Counter()
for fn in broken:
    wf = json.load(open(os.path.join(W, fn), encoding="utf-8"))
    if isinstance(wf.get("nodes"), list):
        print(fn, "-> already UI, skipping")
        continue
    types = Counter(v["class_type"] for v in wf.values())
    alltypes.update(types)
    for nid, nd in wf.items():
        for k, v in nd["inputs"].items():
            if isinstance(v, dict):
                print("  %s %s (%s) dict-input %s = %s" % (fn, nid, nd["class_type"], k, json.dumps(v)[:150]))

print()
print("=== all class types across broken files ===")
for t, c in alltypes.most_common():
    print("  ", t, c)
