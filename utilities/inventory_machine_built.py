import json, os

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# Machine-built workflows (built/converted by us, NOT native UI-saved)
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
    "jaisal_drone_optimized.json",
]

# Expected NATIVE widgets_values length per node type (verified from native UI files)
EXPECTED_LEN = {
    "KSampler": 7,
    "LoadImage": 2,
    "CLIPTextEncode": 1,
    "CLIPLoader": 3,
    "UNETLoader": 2,
    "VAELoader": 1,
    "LoraLoaderModelOnly": 2,
    "SaveImage": 1,
    "VAEDecode": 0,
    "EmptyLatentImage": 3,
    "EmptyFlux2LatentImage": 3,
    "PreviewImage": 0,
    "VAEEncode": 0,
}

print("=== DRY-RUN INVENTORY (no writes) ===\n")
all_types = set()
for fname in MACHINE_BUILT:
    p = os.path.join(BASE, fname)
    if not os.path.exists(p):
        print(f"*** MISSING: {fname}")
        continue
    wf = json.load(open(p, encoding="utf-8"))
    print(f"### {fname} ({len(wf['nodes'])} nodes) ###")
    for n in wf["nodes"]:
        t = n["type"]
        all_types.add(t)
        wv = n.get("widgets_values")
        wlen = len(wv) if wv is not None else None
        has_named = "widgets_values_named" in n
        exp = EXPECTED_LEN.get(t)
        flag = ""
        if exp is None:
            flag = "  << NO-NATIVE-REF (verify manually)"
        elif wlen != exp:
            flag = f"  << LEN MISMATCH (got {wlen}, want {exp})"
        print(f"   {t:28} id={str(n['id']):10} wlen={wlen} named={has_named}{flag}")
    print()

print("=== ALL NODE TYPES SEEN ===")
for t in sorted(all_types):
    exp = EXPECTED_LEN.get(t)
    print(f"   {t:28} expected_len={exp if exp is not None else '???' }")
