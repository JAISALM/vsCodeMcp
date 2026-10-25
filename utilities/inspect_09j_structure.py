#!/usr/bin/env python
"""Inspect 09j main-canvas structure: all nodes, which images exist, what feeds PE 555 + generator 459."""
import json

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json"
j = json.load(open(P, encoding="utf-8"))

print("== MAIN CANVAS NODES ==")
for n in j["nodes"]:
    wv = n.get("widgets_values")
    wvs = json.dumps(wv)[:160] if wv is not None else "None"
    print(f"node {n['id']:<4} {n['type'][:38]:<38} widgets={wvs}")
    for i, inp in enumerate(n.get("inputs") or []):
        if inp.get("link"):
            print(f"    in[{i}] {inp['name']} ({inp['type']}) <- link {inp['link']}")

print("\n== LINKS (id: from_node.out_slot -> to_node.in_slot) ==")
links = {l["id"]: l for l in j.get("links", [])}
for lid, l in sorted(links.items()):
    print(f"link {lid}: node {l['origin_id']}.out{l['origin_slot']} -> node {l['target_id']}.in{l['target_slot']}  [{l.get('type','?')}]")

# trace: find LoadImage nodes and what their output feeds
print("\n== LoadImage outputs ==")
for n in j["nodes"]:
    if n["type"] == "LoadImage":
        outs = n.get("outputs") or []
        for o in outs:
            for lk in (o.get("links") or []):
                t = links.get(lk, {})
                print(f"node {n['id']} ({n['widgets_values'][0]}) -> node {t.get('target_id')} (in{t.get('target_slot')})")

# PE 555 + generator 459 full widget lists
print("\n== 555 widgets:", json.dumps((next(n for n in j["nodes"] if n["id"]==555)["widgets_values"]), indent=1)[:800])
n459 = next(n for n in j["nodes"] if n["id"]==459)
print("== 459 widgets:", json.dumps(n459["widgets_values"]))
print("== 459 named:", json.dumps(n459.get("widgets_values_named")))
