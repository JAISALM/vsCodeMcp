import json

base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
for fname in ("krea2_jaisal_medium.json", "krea2_jaisal_title_moody.json"):
    wf = json.load(open(f"{base}\\{fname}", encoding="utf-8"))
    print(f"########## {fname} ##########")
    for n in wf["nodes"]:
        if n["type"] in ("KSampler", "LoadImage"):
            print(f"  node {n['id']} {n['type']}:")
            print(f"    widgets_values       = {n.get('widgets_values')}")
            print(f"    widgets_values_named = {n.get('widgets_values_named')}")
            print(f"    has 'widgets' key    = {'widgets' in n}")
            if "widgets" in n:
                print(f"    widgets (new fmt)    = {n.get('widgets')}")
    print()
