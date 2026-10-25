"""Map the engine -> save topology: instance outputs, 1216/1434/1457 inputs, subgraph port mappings."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

def show(nid):
    n = nodes.get(nid)
    if not n:
        print(f"  {nid}: NOT FOUND")
        return
    print(f"  {nid} [{n['type']} mode={n.get('mode',0)}] w={str(n.get('widgets_values'))[:100]}")
    for i in n.get("inputs", []):
        print(f"     in[{i['name']}] link={i.get('link')}")
    for o in n.get("outputs", []):
        print(f"     out[{o['name']}] links={o.get('links')}")

for nid in (1359, 1488, 1457, 1216, 1434, 1463, 1475):
    show(nid)
    print()

print("== links feeding 1216 and 1434 ==")
links = {list(L)[0]: list(L) for L in j["links"]}
for L in j["links"]:
    a = list(L)
    if a[3] in (1216, 1434, 1457):
        src = nodes.get(a[1], {})
        print(f"  link {a[0]}: {a[1]} [{src.get('type','?')} w={str(src.get('widgets_values'))[:60]}] -> {a[3]} slot {a[4]}")

print()
print("== subgraph defs: inputs/outputs ports ==")
for s in j.get("definitions", {}).get("subgraphs", []):
    sgid = str(s.get("id", "?"))[:8]
    ins = s.get("inputs", [])
    outs = s.get("outputs", [])
    if ins or outs:
        print(f"  subgraph {sgid}: {len(ins)} inputs, {len(outs)} outputs, {len(s.get('links', []))} internal links")
        for i in ins[:10]:
            print(f"     in: {i.get('name')} type={i.get('type')}")
        for o in outs[:10]:
            print(f"     out: {o.get('name')} type={o.get('type')}")
