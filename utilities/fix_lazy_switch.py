"""Fix 1457 (LazyCaseSwitch) dead-GetNode inputs:
- 2695 (1457.in): 1466 (GetNode h3_timeline_outputs) -> 1449 slot 0 (Bundle timeline outputs)
- 2818 (1457.on_false): 1529 (GetNode h3_gen_engine_settings) -> 1290 slot 0 (ValuePresets gen)
- 2819 (1457.on_true): 1530 (GetNode h3_upscale_engine_settings) -> 1335 slot 0 (ValuePresets upscale)
"""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
links = {list(L)[0]: L for L in j["links"]}

def repoint(lid, new_src, new_slot):
    L = links[lid]
    old_src = L[1]
    for out in nodes[old_src].get("outputs", []):
        if out.get("links"):
            out["links"] = [x for x in out["links"] if x != lid]
    L[1], L[2] = new_src, new_slot
    for out in nodes[new_src].get("outputs", []):
        out["links"] = (out.get("links") or []) + [lid]
    print(f"link {lid}: {old_src} -> {new_src} slot {new_slot}")

repoint(2695, 1449, 0)
repoint(2818, 1290, 0)
repoint(2819, 1335, 0)

json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False)
print("saved")
