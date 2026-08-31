import json, os, datetime

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

print("=== ALL WORKFLOWS (name, size, mtime, has_nodes_list, has_widgets_values_named) ===")
rows = []
for f in sorted(os.listdir(BASE)):
    if not f.endswith(".json"):
        continue
    p = os.path.join(BASE, f)
    sz = os.path.getsize(p)
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")
    try:
        wf = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(f"  {f:45} {sz:>8} {mt}  PARSE-ERROR {e}")
        continue
    is_ui = isinstance(wf.get("nodes"), list)
    # does any node have widgets_values_named?
    has_named = False
    ntypes = set()
    if is_ui:
        for n in wf["nodes"]:
            ntypes.add(n.get("type"))
            if n.get("widgets_values_named") is not None:
                has_named = True
    tag = "UI " if is_ui else "API"
    print(f"  {f:45} {sz:>8} {mt}  {tag} named={has_named} types={sorted(ntypes)[:4]}")
