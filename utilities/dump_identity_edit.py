"""Dump krea2_identity_edit_small_mic.json — the i2i identity-edit workflow (base image + instruction).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\dump_identity_edit.py"
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit_small_mic.json"
wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
links = wf.get("links", [])

MODE = {0: "ACTIVE", 4: "BYPASSED", 2: "MUTATED", 3: "ALWAYS"}

print("=== NODES ===")
for n in sorted(wf.get("nodes", []), key=lambda x: x.get("id", 0)):
    wv = n.get("widgets_values")
    wvs = json.dumps(wv)
    if len(wvs) > 400:
        wvs = wvs[:400] + "..."
    print(f"\n{n.get('id'):>4} {n.get('type'):<32} {MODE.get(n.get('mode',0),n.get('mode')):<9} title={n.get('title')}")
    print(f"     widgets: {wvs}")

print("\n=== FULL INSTRUCTION / PROMPT TEXTS (CLIPTextEncode + any text widgets) ===")
for n in wf.get("nodes", []):
    wv = n.get("widgets_values") or []
    for w in wv:
        if isinstance(w, str) and len(w) > 60:
            print(f"\n--- node {n.get('id')} ({n.get('type')}) ---")
            print(w)
