import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_title_moody.json"
wf = json.load(open(p, encoding="utf-8"))
print("top keys:", list(wf.keys()))
print("node count:", len(wf["nodes"]))
print("\n=== ALL NODES ===")
for n in wf["nodes"]:
    print(f"  id={n['id']:12} type={n['type']:20} pos={n.get('pos')}")
    if n["type"] == "LoadImage":
        print("    --- LoadImage full ---")
        print("    widgets_values:", n.get("widgets_values"))
        print("    has widgets_values_named:", "widgets_values_named" in n)
        for i in n.get("inputs", []):
            t = i.get("type")
            tshow = f"LIST(len={len(t)})" if isinstance(t, list) else repr(t)
            print(f"      input {i.get('name'):12} type={tshow} widget={i.get('widget')} link={i.get('link')}")
        for o in n.get("outputs", []):
            print(f"      output {o.get('name'):12} type={o.get('type')} links={o.get('links')}")
        print("    properties:", n.get("properties"))
