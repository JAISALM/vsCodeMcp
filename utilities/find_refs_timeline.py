"""Find reference filenames + SetNode 'optimized_model' + bundle source in the timeline workflow."""
import json, re

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))

print("== nodes with .png/.mp4/.flac in widgets (canvas + subgraphs) ==")
def scan(nodes, where):
    for n in nodes:
        w = n.get("widgets_values")
        if not w:
            continue
        for v in w:
            if isinstance(v, str) and re.search(r"\.(png|jpg|jpeg|mp4|flac|wav)$", v):
                print(f"  {where} node {n['id']} [{n['type']}]: {v!r}")
                break

scan(j["nodes"], "canvas")
for s in j.get("definitions", {}).get("subgraphs", []):
    scan(s.get("nodes", []), f"subgraph{len(s.get('nodes', []))}")

print()
print("== SetNode / GetNode widgets (canvas + subgraphs) ==")
def scan2(nodes, where):
    for n in nodes:
        if n["type"] in ("SetNode", "GetNode"):
            print(f"  {where} node {n['id']} [{n['type']}]: {n.get('widgets_values')}")
scan2(j["nodes"], "canvas")
for s in j.get("definitions", {}).get("subgraphs", []):
    scan2(s.get("nodes", []), "subgraph")

print()
print("== what feeds Unbundle 1390 and 1392 ==")
nodes = {n["id"]: n for n in j["nodes"]}
for L in j["links"]:
    a = list(L)
    if a[3] in (1390, 1392):
        src = nodes.get(a[1], {})
        print(f"  link {a[0]}: {a[1]} [{src.get('type')} w={str(src.get('widgets_values'))[:80]}] -> {a[3]}")

print()
print("== subgraph contents with LoadImagesCompose ==")
for s in j.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        if n["type"] in ("LoadImagesCompose", "LoadImages"):
            w = n.get("widgets_values")
            print(f"  subgraph node {n['id']} [{n['type']}]: {w}")
