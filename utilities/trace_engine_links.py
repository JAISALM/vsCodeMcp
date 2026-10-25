"""Trace the source of engine-internal in-links 2795, 2289, 2838, 2684."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))

def find_link(lid):
    # canvas links
    for L in j["links"]:
        a = list(L)
        if a[0] == lid:
            return "canvas", a
    for s in j.get("definitions", {}).get("subgraphs", []):
        for L in s.get("links", []):
            a = list(L)
            if a[0] == lid:
                return f"subgraph[{s.get('id','?')[:8]}]", a
    return None, None

def describe(nid, where):
    if where == "canvas":
        for n in j["nodes"]:
            if n["id"] == nid:
                return f"{nid}[{n['type']} w={str(n.get('widgets_values'))[:80]} mode={n.get('mode',0)}]"
    for s in j.get("definitions", {}).get("subgraphs", []):
        for n in s.get("nodes", []):
            if n["id"] == nid:
                return f"{nid}[{n['type']} w={str(n.get('widgets_values'))[:80]} mode={n.get('mode',0)}]"
    return f"?{nid}"

for lid in (2795, 2289, 2838, 2684):
    where, a = find_link(lid)
    if a:
        print(f"link {lid} ({where}): {describe(a[1], where)} -> {describe(a[3], where)}")
    else:
        print(f"link {lid}: NOT FOUND")

print()
print("== ValuePresets 1290 full widgets ==")
for n in j["nodes"]:
    if n["id"] == 1290:
        for i, v in enumerate(n.get("widgets_values") or []):
            print(f"  w[{i}]: {str(v)[:150]}")
        print("  inputs:", ", ".join(f"{i['name']} link={i.get('link')}" for i in n.get("inputs", [])))
        print("  outputs:", ", ".join(f"{o['name']} links={o.get('links')}" for o in n.get("outputs", [])))
