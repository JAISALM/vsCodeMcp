"""Extract full Note texts + Any Switch / Fast Groups Muter/Bypasser widget details.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_2pass_toggles.py"
"""
import json

WF = r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json"
wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}

print("=" * 80)
print("FULL NOTE TEXTS (workflow author's instructions):")
for nid, n in nodes.items():
    if n.get("type") == "Note":
        wv = n.get("widgets_values")
        print(f"\n--- Note node {nid} ---")
        if isinstance(wv, list):
            for w in wv:
                print(w)
        else:
            print(wv)

print("\n" + "=" * 80)
print("ANY SWITCH nodes (the mode selectors):")
for nid, n in nodes.items():
    if n.get("type") == "Any Switch (rgthree)":
        print(f"\n--- Any Switch node {nid} title={n.get('title')} ---")
        print("  widgets_values:", json.dumps(n.get("widgets_values")))
        print("  widgets_values_named:", json.dumps(n.get("widgets_values_named")))
        print("  inputs:", [(i.get("name"), i.get("type"), i.get("link")) for i in n.get("inputs", [])])

print("\n" + "=" * 80)
print("FAST GROUPS MUTER/BYPASSER nodes (the toggles):")
for nid, n in nodes.items():
    if "Fast Groups" in (n.get("type") or ""):
        print(f"\n--- {n.get('type')} node {nid} title={n.get('title')} ---")
        print("  widgets_values:", json.dumps(n.get("widgets_values")))
        print("  widgets_values_named:", json.dumps(n.get("widgets_values_named")))

print("\n" + "=" * 80)
print("Which groups each Fast Groups Muter/Bypasser controls (group ids):")
for nid, n in nodes.items():
    if "Fast Groups" in (n.get("type") or ""):
        print(f"  node {nid} ({n.get('title')}): widgets={json.dumps(n.get('widgets_values'))}")
