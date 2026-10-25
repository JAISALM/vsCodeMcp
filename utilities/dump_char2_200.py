#!/usr/bin/env python
import json
P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char2.json"
j = json.load(open(P, encoding="utf-8"))
for n in j["nodes"]:
    if n["id"] in (200, 300, 301):
        print(f"===== {n['id']} {n['type']} =====")
        print("widgets_values:")
        for i, w in enumerate(n.get("widgets_values", [])):
            print(f"  [{i}] {json.dumps(w, ensure_ascii=False)}")
        if "widgets_values_named" in n:
            print("widgets_values_named:")
            for k, v in n["widgets_values_named"].items():
                print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
        print()
# also check char1 for comparison
P1 = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1.json"
j1 = json.load(open(P1, encoding="utf-8"))
for n in j1["nodes"]:
    if n["type"] == "PixaromaPromptEach" or (n["type"] == "CLIPTextEncode" and n.get("widgets_values") and n["widgets_values"][0]):
        print(f"===== CHAR1 {n['id']} {n['type']} =====")
        for i, w in enumerate(n.get("widgets_values", [])):
            print(f"  [{i}] {json.dumps(w, ensure_ascii=False)[:600]}")
        print()
