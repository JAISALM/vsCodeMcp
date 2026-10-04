"""Dump the keyframe-generation workflows (v9 latest + kf7b_page_mic) to find the trick.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_kf_workflows.py"
"""
import json, os

WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
TARGETS = ["krea2_intro_kf6_plants_dead_v9.json", "krea2_intro_kf7b_page_mic_v8.json"]

for name in TARGETS:
    fp = os.path.join(WFDIR, name)
    if not os.path.isfile(fp):
        print(f"MISSING: {name}")
        continue
    wf = json.load(open(fp, encoding="utf-8"))
    nodes = {n.get("id"): n for n in wf.get("nodes", [])}
    links = wf.get("links", [])
    MODE = {0: "ACTIVE", 4: "BYPASSED", 2: "MUTATED", 3: "ALWAYS"}
    print("=" * 90)
    print(f"### {name}  ({len(nodes)} nodes)")
    print("=" * 90)
    for n in sorted(wf.get("nodes", []), key=lambda x: x.get("id", 0)):
        wv = n.get("widgets_values")
        wvs = json.dumps(wv)
        if len(wvs) > 500:
            wvs = wvs[:500] + "..."
        print(f"\n{n.get('id'):>4} {n.get('type'):<32} {MODE.get(n.get('mode',0),n.get('mode')):<9} title={n.get('title')}")
        print(f"     widgets: {wvs}")
    print("\n--- LINKS ---")
    for l in links:
        lid, src, sslot, dst, dslot, ltype = l[0], l[1], l[2], l[3], l[4], l[5]
        sn = nodes.get(src, {}).get("type", f"?{src}")
        dn = nodes.get(dst, {}).get("type", f"?{dst}")
        print(f"  {lid:>5}: {sn:<28} s{sslot} -> {dn:<28} s{dslot} [{ltype}]")
