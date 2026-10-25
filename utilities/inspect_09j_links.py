#!/usr/bin/env python
"""Dump 09j links in UI array format + trace the image branches."""
import json
P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json"
j = json.load(open(P, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

def nm(i):
    n = nodes.get(i)
    if not n:
        return f"<{i}?>"
    wv = json.dumps(n.get("widgets_values"))[:40]
    return f"{n['type'][:22]}(w={wv})"

print("== LINKS [id, from, from_slot, to, to_slot, type] ==")
for l in j["links"]:
    lid, a, asl, b, bsl, typ = l[0], l[1], l[2], l[3], l[4], l[5]
    print(f"{lid:>4}: {a:>3}.out{asl} -> {b:>3}.in{bsl} [{typ}]   {nm(a)} -> {nm(b)}")

# what feeds key inputs
print("\n== trace: who feeds 555.image (link 959), 459.images.image_1 (747), 485.image (743), 569.image1/2 (989/992) ==")
for l in j["links"]:
    if l[0] in (959, 747, 743, 989, 992, 969, 985, 670, 671, 672, 981, 993):
        print(f"link {l[0]}: node {l[1]} -> node {l[3]} in{l[4]}  [{nm(l[1])}]")

# 555 full widgets_values_named
n555 = nodes[555]
print("\n== 555 named keys:", list((n555.get("widgets_values_named") or {}).keys()))
print("== 459 named keys:", list((nodes[459].get("widgets_values_named") or {}).keys()))
print("== 481 widget:", nodes[481].get("widgets_values"))
# does 485 output connect to anything?
print("\n== node 485 outputs:", nodes[485].get("outputs"))
print("== node 569 outputs:", nodes[569].get("outputs"))
print("== node 470 outputs:", nodes[470].get("outputs"))
