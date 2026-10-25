"""Find h3_upscale_engine_settings / h3_gen_engine_settings setters + inspect subgraph 1488 internals."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))

def scan(nodes_list, where, sg_id=None):
    for n in nodes_list:
        w = n.get("widgets_values") or []
        hit = None
        for v in w:
            if isinstance(v, str) and ("h3_upscale_engine_settings" in v or "h3_gen_engine_settings" in v):
                hit = v
                break
        if hit:
            print(f"  {where} node {n['id']} [{n['type']} mode={n.get('mode',0)}]: {str(w)[:110]}")
            return True
    return False

print("== setters (canvas + subgraphs) ==")
found = scan(j["nodes"], "canvas")
for s in j.get("definitions", {}).get("subgraphs", []):
    if scan(s.get("nodes", []), f"subgraph[{s.get('id','?')[:8]}]"):
        found = True

print()
print("== subgraph 1488 internals (upscale engine) ==")
for s in j.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        if n["id"] in (1481, 1482, 1483, 1484, 1485, 1486):
            w = str(n.get("widgets_values"))[:90]
            ins = ", ".join(f"{i['name']} link={i.get('link')}" for i in n.get("inputs", []))
            outs = ", ".join(f"{o['name']} links={o.get('links')}" for o in n.get("outputs", []))
            print(f"  {n['id']} [{n['type']} mode={n.get('mode',0)}] w={w}\n    in: {ins}\n    out: {outs}")

print()
print("== subgraph 1359 internals (generator engine) Unbundle check ==")
for s in j.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        if n["type"] == "Unbundle (obvpm)":
            w = str(n.get("widgets_values"))[:90]
            ins = ", ".join(f"{i['name']} link={i.get('link')}" for i in n.get("inputs", []))
            print(f"  {n['id']} [{n['type']}] w={w}\n    in: {ins}")
