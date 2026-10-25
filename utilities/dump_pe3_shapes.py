#!/user/bin/env python
"""Dump the exact node shapes needed to convert krea2_t2i_char1_pe3.json into a plain-t2i
frontal-face workflow: CLIPTE 300/301/313/318 (inputs + widgets), latent 82, KSampler 53/314/319,
SaveImage 29/317/322, and the TG nodes to remove (310/311/312 + their links)."""
import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char1_pe3.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}
for nid in (300, 301, 313, 318, 82, 53, 314, 319, 29, 317, 322, 310, 311, 312):
    n = nodes.get(nid)
    if not n:
        print(f"--- {nid}: MISSING"); continue
    print(f"--- {nid} {n['type']}")
    print("   widgets:", str(n.get("widgets_values"))[:160])
    for i, inp in enumerate(n.get("inputs", [])):
        print(f"   in[{i}] {inp.get('name')} ({inp.get('type')}) link={inp.get('link')}")
    for o, out in enumerate(n.get("outputs", [])):
        print(f"   out[{o}] {out.get('name')} links={out.get('links')}")
print("=== links touching 310/311/312 ===")
for l in j["links"]:
    if l[1] in (310, 311, 312) or l[3] in (310, 311, 312):
        print(l)
print("last_link_id:", j.get("last_link_id"), "last_node_id:", j.get("last_node_id"))
