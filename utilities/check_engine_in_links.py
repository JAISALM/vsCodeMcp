"""Check canvas links 2717, 2729, 2820 + anything feeding the engine 'in' ports."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
links = {list(L)[0]: list(L) for L in j["links"]}

def desc(nid):
    n = nodes.get(nid)
    return f"{nid}[{n['type']} w={str(n.get('widgets_values'))[:70]} mode={n.get('mode',0)}]" if n else f"?{nid}"

for lid in (2717, 2729, 2820, 2726, 2730, 2808, 2733, 2734, 2504, 2524, 2716):
    L = links.get(lid)
    if L:
        print(f"link {lid}: {desc(L[1])} slot {L[2]} -> {desc(L[3])} slot {L[4]}")
    else:
        print(f"link {lid}: *** MISSING ***")

print()
print("== consumers of 1457 (LazyCaseSwitch) and 1531/1533 ==")
for L in j["links"]:
    a = list(L)
    if a[1] in (1457, 1531, 1533, 1290, 1335):
        print(f"  link {a[0]}: {desc(a[1])} -> {desc(a[3])} slot {a[4]}")

print()
print("== ValuePresets 1335 widgets (set name?) ==")
for n in j["nodes"]:
    if n["id"] == 1335:
        for i, v in enumerate(n.get("widgets_values") or []):
            print(f"  w[{i}]: {str(v)[:120]}")
        print("  outputs:", ", ".join(f"{o['name']} links={o.get('links')}" for o in n.get("outputs", [])))
