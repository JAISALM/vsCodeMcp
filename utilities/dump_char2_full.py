#!/usr/bin/env python
import json
P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char2.json"
j = json.load(open(P, encoding="utf-8"))
print("id:", j.get("id"))
for n in j["nodes"]:
    wv = n.get("widgets_values")
    print(f"== {n['id']} {n['type']} {json.dumps(wv, ensure_ascii=False)[:160]}")
    for inp in n.get("inputs", []):
        print(f"   in: {inp.get('name')} link={inp.get('link')}")
    for out in n.get("outputs", []):
        print(f"   out: {out.get('name')} links={out.get('links')}")
print("links:", json.dumps(j.get("links")))
