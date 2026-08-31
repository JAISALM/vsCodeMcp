import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_title_moody.json"
wf = json.load(open(p, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

native = nodes["31"]      # user-added native LoadImage (working image selector)
ours = nodes["FKI2I:img"] # our converted LoadImage

print("=== FULL JSON: native node 31 (user-added, working) ===")
print(json.dumps(native, indent=1, ensure_ascii=False))
print("\n=== FULL JSON: our FKI2I:img ===")
print(json.dumps(ours, indent=1, ensure_ascii=False))

# Field-by-field diff
print("\n=== FIELD-BY-FIELD DIFF ===")
allkeys = set(native.keys()) | set(ours.keys())
for k in sorted(allkeys):
    nv = native.get(k, "<MISSING>")
    ov = ours.get(k, "<MISSING>")
    same = (nv == ov)
    if not same:
        print(f"  DIFF {k}:")
        print(f"     native={json.dumps(nv, ensure_ascii=False)}")
        print(f"     ours  ={json.dumps(ov, ensure_ascii=False)}")
    else:
        print(f"  same {k}")
