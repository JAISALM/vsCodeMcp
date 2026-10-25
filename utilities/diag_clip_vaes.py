"""Diagnose the h3_clip_vaes Set/Get failure: check modes of 1373 chain + 752."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

for nid in (1373, 1374, 1376, 1379, 752):
    n = nodes.get(nid)
    if not n:
        print(f"{nid}: NOT FOUND")
        continue
    print(f"{nid} [{n['type']}] mode={n.get('mode',0)} w={str(n.get('widgets_values'))[:80]}")
    for i in n.get("inputs", []):
        print(f"    in: {i['name']} ({i['type']}) link={i.get('link')}")
    for L in j["links"]:
        a = list(L)
        if a[3] == nid:
            src = nodes.get(a[1], {})
            print(f"    <- link {a[0]}: {a[1]} [{src.get('type')} mode={src.get('mode',0)}]")
