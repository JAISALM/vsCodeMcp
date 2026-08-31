import json, os

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

def classify(path):
    with open(path, encoding="utf-8") as f:
        wf = json.load(f)
    nodes = wf.get("nodes")
    if isinstance(nodes, dict):
        # API/prompt format: nodes keyed by string id, each has class_type
        sample = next(iter(nodes.values()))
        fmt = "API"
        has_pos = False
        has_class_type = "class_type" in sample
    elif isinstance(nodes, list):
        # UI format: nodes is a list of objects with id/type/pos/size
        fmt = "UI"
        sample = nodes[0] if nodes else {}
        has_pos = "pos" in sample
        has_class_type = "class_type" in sample
    else:
        fmt = "UNKNOWN"
        has_pos = False
        has_class_type = False
    return fmt, has_pos, has_class_type, len(nodes) if nodes else 0

print(f"{'FILE':45s} {'FMT':6s} {'pos':5s} {'class_type':10s} {'#nodes':>6s}")
print("-" * 80)
for fn in sorted(os.listdir(W)):
    if not fn.endswith(".json") or fn == ".index.json":
        continue
    p = os.path.join(W, fn)
    try:
        fmt, has_pos, has_ct, n = classify(p)
        flag = ""
        if fmt == "API":
            flag = "  <-- API format (UI shows EMPTY)"
        print(f"{fn:45s} {fmt:6s} {str(has_pos):5s} {str(has_ct):10s} {n:6d}{flag}")
    except Exception as e:
        print(f"{fn:45s} ERROR: {e}")
