"""Full structural dump of krea2T2iI2iInpaint2pass_v15.json for explanation.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_2pass_full.py"
"""
import json

WF = r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json"
wf = json.load(open(WF, encoding="utf-8"))

MODE = {0: "active", 4: "BYPASSED", 2: "mutated", 3: "always"}

print("=" * 80)
print("GROUPS (section labels):")
for g in wf.get("groups", []):
    t = g.get("title", "")
    print(f"  [{g.get('id')}] {t}")

print("=" * 80)
print("NODES (id | type | mode | title | widgets):")
for n in sorted(wf.get("nodes", []), key=lambda x: (x.get("pos", [0, 0])[1], x.get("pos", [0, 0])[0])):
    mode = MODE.get(n.get("mode", 0), str(n.get("mode")))
    wv = n.get("widgets_values")
    wvs = json.dumps(wv)
    if len(wvs) > 220:
        wvs = wvs[:220] + "..."
    print(f"  {n.get('id'):>4} | {n.get('type'):<38} | {mode:<9} | {str(n.get('title'))[:30]:<30} | {wvs}")

print("=" * 80)
print("SUBGRAPH internals:")
for s in wf.get("definitions", {}).get("subgraphs", []):
    print(f"  subgraph id={s.get('id')} name={s.get('name')}")
    print("  inputs:", [(i.get("name"), i.get("type")) for i in s.get("inputs", [])])
    print("  outputs:", [(o.get("name"), o.get("type")) for o in s.get("outputs", [])])
    for n in s.get("nodes", []):
        print(f"    internal {n.get('id')} | {n.get('type')} | mode={n.get('mode')} | widgets={json.dumps(n.get('widgets_values'))[:200]}")

print("=" * 80)
print("LINKS (link_id: from_node.from_slot -> to_node.to_slot):")
node_by_id = {n.get("id"): n for n in wf.get("nodes", [])}
for l in wf.get("links", []):
    lid, src, sslot, dst, dslot, ltype = l[0], l[1], l[2], l[3], l[4], l[5]
    sn = node_by_id.get(src, {}).get("type", f"?{src}")
    dn = node_by_id.get(dst, {}).get("type", f"?{dst}")
    print(f"  {lid:>5}: {sn:<30} slot{sslot} -> {dn:<30} slot{dslot}  [{ltype}]")
