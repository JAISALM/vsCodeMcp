"""Inspect the negpip-zimage pack + how ApplyKrea2NegPiP is wired in the 2-pass workflow.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\inspect_negpip.py"
"""
import os, re, json

PACK = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-negpip-zimage"
WF = r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json"

print("=== negpip-zimage pack .py files + node classes ===")
for dirpath, dirnames, filenames in os.walk(PACK):
    dirnames[:] = [x for x in dirnames if x != "__pycache__"]
    for fn in filenames:
        if fn.endswith(".py"):
            fp = os.path.join(dirpath, fn)
            src = open(fp, encoding="utf-8", errors="replace").read()
            m = re.findall(r"NODE_CLASS_MAPPINGS\s*=\s*\{(.*?)\}", src, re.S)
            cls = re.findall(r"^class\s+(\w+)", src, re.M)
            if m or cls:
                print("\n", fp)
                if m:
                    print("  NODE_CLASS_MAPPINGS:", m[0].strip()[:500])
                if cls:
                    print("  classes:", cls)

print("\n=== how ApplyKrea2NegPiP is wired in the workflow ===")
wf = json.load(open(WF, encoding="utf-8"))
for n in wf.get("nodes", []):
    if n.get("type") == "ApplyKrea2NegPiP":
        print("node id:", n.get("id"))
        print("title:", n.get("title"))
        print("widgets_values:", n.get("widgets_values"))
        print("widgets_values_named:", n.get("widgets_values_named"))
        print("inputs:", json.dumps(n.get("inputs"), indent=1))
        print("outputs:", json.dumps(n.get("outputs"), indent=1))
        # find links into this node
        nid = n.get("id")
        for l in wf.get("links", []):
            if l[4] == nid:
                print("  link in:", l)
        for l in wf.get("links", []):
            if l[0] == nid or (isinstance(l[0], list) and nid in l[0]):
                pass
        # outputs links
        for l in wf.get("links", []):
            if l[0] == nid:
                print("  link out:", l)
