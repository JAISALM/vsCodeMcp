# -*- coding: utf-8 -*-
import json
for key in ["A", "J"]:
    wf = {
        "A": "jaisal_intro_A_walkin.json",
        "J": "jaisal_intro_J_objects_join.json",
    }[key]
    d = json.load(open(
        r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\\" + wf,
        encoding="utf-8"))
    for n in d["nodes"]:
        if n["type"] == "PrimitiveStringMultiline":
            p = n["widgets_values"][0]
            print("==== %s (%d chars) ====" % (key, len(p)))
            print(p[:400])
            print("...")
            # check for the old bug
            print("has dup <Subject 1> is <Subject 1>:", "<Subject 1> is <Subject 1> is" in p)
            print()
