#!/usr/bin/env python
"""Trace wiring of the 4 problematic stage-2 nodes (111/125/126/127) + save nodes 106/13."""
import json

j = json.load(open(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\2BZ_H3_character_sheet_2stage - jaisal.json", encoding="utf-8", errors="ignore"))
nodes = {n["id"]: n for n in j["nodes"]}
# link map: [link_id, origin_id, origin_slot, target_id, target_slot, type]
links = j["links"]

def inputs_of(nid):
    return [(l[0], l[1], l[2], l[5]) for l in links if l[3] == nid]

def outputs_of(nid):
    return [(l[0], l[3], l[4], l[5]) for l in links if l[1] == nid]

for nid in (106, 13, 111, 125, 126, 127, 115):
    n = nodes.get(nid)
    print(f"=== node {nid} {n['type'] if n else '?'} ===")
    print("  inputs :", [(f"from {o} slot {oslot} type {t}") for (_, o, oslot, t) in inputs_of(nid)])
    print("  outputs:", [(f"to {t} slot {tslot} type {ty}") for (_, t, tslot, ty) in outputs_of(nid)])
    # also print node inputs array (link fields)
    if n:
        for i, inp in enumerate(n.get("inputs", [])):
            print(f"    in[{i}] {inp.get('name')} type={inp.get('type')} link={inp.get('link')}")
    print()
