"""Add Krea2-realism-V2 LoRA node (id 97) into 02's chain: 55 -> 97 -> 71 -> 79.
Idempotent. Also copies the two user-picked face refs into input/.
"""
import json, shutil, os

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\02_identity_refset.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

if 97 in nodes:
    print("node 97 already present")
else:
    # remove existing 55->71 link
    before = len(j["links"])
    j["links"] = [l for l in j["links"] if not (l[1] == 55 and l[2] == 0 and l[3] == 71)]
    print(f"removed {before - len(j['links'])} link(s) 55->71")
    # 71's model input now fed by 97
    for inp in nodes[71]["inputs"]:
        if inp.get("name") == "model":
            inp["link"] = 101
    # 55's single output now feeds 97
    nodes[55]["outputs"][0]["links"] = [100]
    # mirror existing link tuple length
    ltype = j["links"][0][5] if len(j["links"][0]) > 5 else None
    newl = [100, 55, 0, 97, 0]
    newl2 = [101, 97, 0, 71, 0]
    if ltype is not None:
        newl.append(ltype); newl2.append(ltype)
    j["links"] += [newl, newl2]
    nodes[97] = {
        "id": 97, "type": "LoraLoaderModelOnly",
        "pos": [660.0, 260.0], "size": [320.0, 80.0], "flags": {}, "order": 0, "mode": 0,
        "inputs": [{"localized_name": "model", "name": "model", "type": "MODEL", "link": 100}],
        "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": [101]}],
        "properties": {"Node name for S&R": "LoraLoaderModelOnly"},
        "widgets_values": ["Krea2-realism-V2.safetensors", 0.0],
    }
    j["nodes"].append(nodes[97])
    print("node 97 added (V2 LoRA, strength starts 0.0)")

json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved 02")

# copy user-picked face refs
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"
inp = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
shutil.copy(os.path.join(out, "krea2_abtest_char1", "char1_NEW_realism_s6_00001_.png"), os.path.join(inp, "jaisal_ref.png"))
shutil.copy(os.path.join(out, "krea2_char1_face_c_00001_.png"), os.path.join(inp, "zidane_ref.png"))
print("refs copied: jaisal_ref.png (A/B NEW base), zidane_ref.png (char1_face_c_00001)")
