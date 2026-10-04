"""Show group membership (which nodes are in each group) for the 2-pass workflow.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_2pass_groups.py"
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_2pass_bf16_turbo.json"
wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
groups = wf.get("groups", [])

for g in groups:
    b = g.get("bounding") or [0, 0, 0, 0]
    bx, by, bw, bh = (list(b) + [0, 0, 0, 0])[:4]
    members = []
    for nid, n in nodes.items():
        pos = n.get("pos", [0, 0])
        if bx <= pos[0] <= bx + bw and by <= pos[1] <= by + bh:
            members.append(f"{nid}:{n.get('type')}({'A' if n.get('mode')==0 else 'B' if n.get('mode')==4 else n.get('mode')})")
    print(f"\n=== GROUP [{g.get('id')}] {g.get('title')} (box {bx},{by} {bw}x{bh}) ===")
    for m in members:
        print("   ", m)
