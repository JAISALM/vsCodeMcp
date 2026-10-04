"""Dump krea2_object_refs.json structure — how the bat/ball/paper refs were made.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_object_refs.py"
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_object_refs.json"
wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
links = wf.get("links", [])

MODE = {0: "ACTIVE", 4: "BYPASSED", 2: "MUTATED", 3: "ALWAYS"}

print("=== NODES ===")
for n in sorted(wf.get("nodes", []), key=lambda x: x.get("id", 0)):
    wv = n.get("widgets_values")
    wvs = json.dumps(wv)
    if len(wvs) > 300:
        wvs = wvs[:300] + "..."
    print(f"\n{n.get('id'):>4} {n.get('type'):<30} {MODE.get(n.get('mode',0),n.get('mode')):<9} title={n.get('title')}")
    print(f"     widgets: {wvs}")
    print(f"     inputs: {[(i.get('name'), i.get('link')) for i in n.get('inputs', [])]}")

print("\n=== LINKS ===")
for l in links:
    lid, src, sslot, dst, dslot, ltype = l[0], l[1], l[2], l[3], l[4], l[5]
    sn = nodes.get(src, {}).get("type", f"?{src}")
    dn = nodes.get(dst, {}).get("type", f"?{dst}")
    print(f"  {lid:>5}: {sn:<28} s{sslot} -> {dn:<28} s{dslot} [{ltype}]")
