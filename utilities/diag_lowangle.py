import json, os, re, urllib.request

# 1) Find the 1-5 images in jaisal_cut
d = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut"
print("=== 1-5 files in jaisal_cut ===")
found = []
for f in sorted(os.listdir(d)):
    if os.path.isfile(os.path.join(d, f)) and re.match(r"^[1-5][._-]?", f):
        found.append(f)
        print(f"   {f}  ({os.path.getsize(os.path.join(d,f))} bytes)")
if not found:
    print("   (none found with ^[1-5] pattern — listing all recent files instead)")
    files = [(f, os.path.getmtime(os.path.join(d, f))) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
    files.sort(key=lambda x: -x[1])
    for f, m in files[:15]:
        print(f"   {f}")

# 2) Dump the ref+turbo template structure
print("\n=== TEMPLATE: video_minimax_h3_r2v+turbo.json ===")
tp = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\video_minimax_h3_r2v+turbo.json"
wf = json.load(open(tp, encoding="utf-8"))
for n in wf["nodes"]:
    wv = n.get("widgets_values")
    wvshow = wv if wv is not None and len(str(wv)) < 120 else (str(wv)[:100] + "..." if wv is not None else None)
    print(f"   id={str(n['id']):10} type={n['type']:32} widgets={wvshow}")

# 3) Dump MiniMaxH3ReferenceToVideo schema
print("\n=== MiniMaxH3ReferenceToVideo schema ===")
info = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=30))
mm = info.get("MiniMaxH3ReferenceToVideo", {})
print("required inputs:")
for k, v in mm.get("input", {}).get("required", {}).items():
    print(f"   {k}: {v[0] if isinstance(v, list) else v}")
print("optional inputs:")
for k, v in mm.get("input", {}).get("optional", {}).items():
    print(f"   {k}: {v[0] if isinstance(v, list) else v}")
