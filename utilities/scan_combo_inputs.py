import json, os

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
MACHINE_BUILT = [
    "jaisal_shot1_t2i.json","jaisal_shot2_i2i.json","jaisal_shot3_i2i.json",
    "jaisal_sketch_shot1_i2i.json","jaisal_sketch_shot2_i2i.json","jaisal_sketch_shot3_i2i.json",
    "krea2_jaisal_aerial_v4.json","krea2_jaisal_aerial_v5.json","krea2_jaisal_continuity.json",
    "krea2_jaisal_face.json","krea2_jaisal_face_v2.json","krea2_jaisal_face_v3.json",
    "krea2_jaisal_final_aerial.json","krea2_jaisal_fix05_inpaint.json","krea2_jaisal_fix05_tie.json",
    "krea2_jaisal_longshot.json","krea2_jaisal_medium.json","krea2_jaisal_storysheet.json",
    "krea2_jaisal_storysheet_v2.json","krea2_jaisal_title_moody.json","jaisal_drone_optimized.json",
]

# For each node type, collect the set of input names whose type is a LIST (static combo dump)
# vs 'COMBO' (correct). Report which (node_type, input_name) pairs are static-lists.
from collections import defaultdict
static = defaultdict(set)   # (type, input_name) -> count
combo = defaultdict(set)
for fname in MACHINE_BUILT:
    p = os.path.join(BASE, fname)
    if not os.path.exists(p):
        continue
    wf = json.load(open(p, encoding="utf-8"))
    for n in wf["nodes"]:
        for i in n.get("inputs", []):
            t = i.get("type")
            if isinstance(t, list):
                static[(n["type"], i.get("name"))].add(fname)
            elif t == "COMBO":
                combo[(n["type"], i.get("name"))].add(fname)

print("=== INPUTS WITH STATIC LIST type (should be 'COMBO') ===")
for (ntype, iname), files in sorted(static.items()):
    print(f"   {ntype:28} {iname:16} in {len(files)} file(s)")

print("\n=== INPUTS ALREADY 'COMBO' (correct) ===")
for (ntype, iname), files in sorted(combo.items()):
    print(f"   {ntype:28} {iname:16} in {len(files)} file(s)")
