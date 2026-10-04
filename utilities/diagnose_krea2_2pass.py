"""Diagnose krea2T2iI2iInpaint2pass_v15.json: which node packs are missing and where they live.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\diagnose_krea2_2pass.py"
"""
import json, re, os, urllib.request, glob

WF = r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json"
CUSTOM = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes"
CORE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI"

# 1. Load workflow, collect all node types (top-level + subgraph internals)
wf = json.load(open(WF, encoding="utf-8"))
types = set(n.get("type") for n in wf.get("nodes", []))
for s in wf.get("definitions", {}).get("subgraphs", []):
    types |= set(n.get("type") for n in s.get("nodes", []))
types.discard(None)

# 2. Live server object_info
raw = urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60).read().decode("utf-8", "replace")
d = json.loads(raw)
print("=== object_info: %d nodes, raw len %d ===" % (len(d), len(raw)))

print("\n=== workflow node types vs live server ===")
missing = []
for t in sorted(types):
    ok = t in d
    if not ok:
        missing.append(t)
    print(("OK   " if ok else "MISS ") + t)

print("\n=== MISSING: %s ===" % missing)

# 3. For each missing node, search installed packs + core for the class name
print("\n=== where each missing node is defined (search .py files) ===")
all_py = []
for root in (CUSTOM, CORE):
    for dirpath, dirnames, filenames in os.walk(root):
        # skip heavy dirs
        dirnames[:] = [x for x in dirnames if x not in ("__pycache__", "node_modules", ".git", "venv", "models")]
        for fn in filenames:
            if fn.endswith(".py"):
                all_py.append(os.path.join(dirpath, fn))
print("scanned %d .py files" % len(all_py))

for t in missing:
    # the class name is usually the part before ' (' for display names
    cls = t.split(" (")[0].strip()
    hits = []
    for p in all_py:
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                src = f.read()
        except Exception:
            continue
        # look for the class definition or a NODE_CLASS_MAPPINGS entry
        if re.search(r"NODE_CLASS_MAPPINGS\s*\[?\s*[\"']%s[\"']" % re.escape(cls), src) or \
           re.search(r"class\s+%s\b" % re.escape(cls), src) or \
           re.search(r"[\"']%s[\"']\s*:" % re.escape(cls), src):
            hits.append(p)
    print("\n--- %r (class %r) ---" % (t, cls))
    if hits:
        for h in hits[:8]:
            print("   ", h)
    else:
        print("    NOT FOUND in any installed .py -> needs install")
