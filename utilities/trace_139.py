#!/usr/bin/env python
"""Check node 139, 109, 5, 49 + node 127 widgets in the A variant."""
import json

j = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\2BZ_H3_character_sheet_2stage - jaisal.json", encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}
links = j["links"]

def inputs_of(nid):
    return [(l[0], l[1], l[2], l[5]) for l in links if l[3] == nid]

def outputs_of(nid):
    return [(l[0], l[3], l[4], l[5]) for l in links if l[1] == nid]

for nid in (139, 109, 5, 49, 127):
    n = nodes.get(nid)
    print(f"=== node {nid} {n['type'] if n else 'MISSING'} ===")
    if n:
        print("  widgets:", [str(w)[:80] for w in n.get("widgets_values", [])])
    print("  inputs :", [(f"from {o} slot {oslot} type {t}") for (_, o, oslot, t) in inputs_of(nid)])
    print("  outputs:", [(f"to {t} slot {tslot} type {ty}") for (_, t, tslot, ty) in outputs_of(nid)])
    print()

# what consumes 139's output chain — walk forward from 139
def forward(nid, depth=3, seen=None):
    if seen is None:
        seen = set()
    if depth == 0 or nid in seen:
        return
    seen.add(nid)
    for (_, t, tslot, ty) in outputs_of(nid):
        print(f"    {nid} -> {t} ({nodes[t]['type'] if t in nodes else '?'}) slot {tslot}")
        forward(t, depth - 1, seen)

print("=== forward chain from 139 ===")
forward(139, 4)
print("=== forward chain from 49 ===")
forward(49, 4)
