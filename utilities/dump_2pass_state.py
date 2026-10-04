"""Dump current state of the configured 2-pass workflow: key node modes + values + group membership.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_2pass_state.py"
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_2pass_bf16_turbo.json"
wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
groups = wf.get("groups", [])

MODE = {0: "ACTIVE", 4: "BYPASSED", 2: "MUTATED", 3: "ALWAYS"}

def group_at(x, y):
    for g in groups:
        b = g.get("bounding") or [0, 0, 0, 0]
        bx, by, bw, bh = (list(b) + [0, 0, 0, 0])[:4]
        if bx <= x <= bx + bw and by <= y <= by + bh:
            return g.get("title")
    return None

print("=== KEY NODES (mode + value + group) ===")
for nid in (247, 9, 265, 267, 296, 254, 255, 300, 301, 270, 264, 275, 259, 37, 25, 279, 281, 285, 219, 237, 238, 307, 186):
    n = nodes.get(nid)
    if not n:
        continue
    pos = n.get("pos", [0, 0])
    grp = group_at(pos[0], pos[1])
    wv = n.get("widgets_values")
    wvs = json.dumps(wv)
    if len(wvs) > 160:
        wvs = wvs[:160] + "..."
    print(f"\n{nid:>4} {n.get('type'):<34} {MODE.get(n.get('mode',0),n.get('mode')):<9} grp={grp}")
    print(f"     widgets: {wvs}")

print("\n=== GROUPS (title + bounding box) ===")
for g in groups:
    print(f"  [{g.get('id')}] {g.get('title'):<40} pos={g.get('pos')} size={g.get('size')}")
