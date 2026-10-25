"""Map every Set/Get + Unbundle(constant) usage in the timeline workflow."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
links = {list(L)[0]: list(L) for L in j["links"]}

def desc(nid):
    n = nodes.get(nid)
    if not n:
        return f"?{nid}"
    return f"{nid}[{n['type']} w={str(n.get('widgets_values'))[:60]}]"

print("== SetNodes (constant <- source) ==")
for n in j["nodes"]:
    if n["type"] == "SetNode":
        for i in n.get("inputs", []):
            lid = i.get("link")
            if lid and lid in links:
                L = links[lid]
                print(f"  {n['id']} sets {n['widgets_values'][0]!r} <- link {lid}: {desc(L[1])} slot {L[2]}")
            else:
                print(f"  {n['id']} sets {n['widgets_values'][0]!r} <- NO INPUT LINK")

print()
print("== Unbundle nodes (in-link + get widget) ==")
for n in j["nodes"]:
    if n["type"] == "Unbundle (obvpm)":
        w = n.get("widgets_values") or []
        names = w[0] if len(w) > 0 else None
        get = w[1] if len(w) > 1 else None
        in_link = None
        for i in n.get("inputs", []):
            if i.get("name") == "in":
                in_link = i.get("link")
        src = desc(links[in_link][1]) if in_link and in_link in links else "NO IN LINK"
        print(f"  {n['id']}: names={str(names)[:40]!r} get={str(get)[:20]!r} in={in_link} <- {src}")

print()
print("== Bundle nodes with set widget ==")
for n in j["nodes"]:
    if n["type"] == "Bundle (obvpm)":
        w = n.get("widgets_values") or []
        print(f"  {n['id']}: w={str(w)[:80]}")

print()
print("== consumers of SetNode outputs (links INTO the SetNode's output slot) ==")
set_ids = {n["id"] for n in j["nodes"] if n["type"] == "SetNode"}
for L in j["links"]:
    a = list(L)
    if a[1] in set_ids:
        print(f"  link {a[0]}: {desc(a[1])} -> {desc(a[3])}")
