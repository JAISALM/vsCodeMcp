# -*- coding: utf-8 -*-
"""add_realism_lora.py (2026-10-31)

Insert node 202 LoraLoaderModelOnly (Krea2-realism-V2 @0.8) between the
identity-edit LoRA (71) and the Krea2EditModelPatch (79) in both dataset
workflows — the detail layer (proven 2026-10-08 face-candidate work).

Chain becomes: 55 UNET -> 71 identity LoRA -> 202 realism LoRA -> 79 patch -> 53 KSampler.
Backs up originals as *.pre_realism.bak. Idempotent.
"""
import json, shutil, copy, sys

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

for name in ("jaisal", "zidhan"):
    p = W + "\\lora_dataset_%s.json" % name
    shutil.copyfile(p, p + ".pre_realism.bak")
    d = json.load(open(p, encoding="utf-8"))

    # find the 71 -> 79 MODEL link (link id 2)
    link = None
    for l in d["links"]:
        arr = l if isinstance(l, list) else l.get("value")
        if arr[1] == 71 and arr[3] == 79 and arr[5] == "MODEL":
            link = arr
            break
    assert link is not None, name + ": 71->79 link not found"
    link_id = link[0]

    # node 71 model output now feeds 202
    n71 = next(n for n in d["nodes"] if n["id"] == 71)
    n71["outputs"][0]["links"] = [link_id] if False else [101]

    # relink: 202 -> 79
    link[1] = 202

    # new link 71 -> 202
    if not any((l if isinstance(l, list) else l.get("value"))[0] == 101 for l in d["links"]):
        d["links"].append([101, 71, 0, 202, 0, "MODEL"])

    # clone node 71 shape -> 202 (native shape, no widgets_values_named)
    n202 = copy.deepcopy(n71)
    n202["id"] = 202
    n202["pos"] = [60.0, 520.0]
    n202["order"] = 15
    n202["inputs"][0]["link"] = 101
    n202["outputs"][0]["links"] = [link_id]
    n202["widgets_values"] = ["Krea2-realism-V2.safetensors", 0.8]
    d["nodes"] = [n for n in d["nodes"] if n["id"] != 202]
    d["nodes"].append(n202)

    d["last_node_id"] = max(d["last_node_id"], 202)
    d["last_link_id"] = max(d["last_link_id"], 101)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print("%s: 55 -> 71 identity -> 202 realism (Krea2-realism-V2 @0.8) -> 79 patch -> 53" % name)

print("DONE")
