import json

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# Check the full native LoadImage input objects across a few native files
for f in ("mini-max-refrance-to-video-1.json", "QWEN_click_multiple_character_angles-v1.0.json"):
    wf = json.load(open(f"{BASE}\\{f}", encoding="utf-8"))
    for n in wf["nodes"]:
        if n["type"] == "LoadImage":
            print(f"### {f} id={n['id']} ###")
            print("inputs (full):")
            for i in n.get("inputs", []):
                t = i.get("type")
                tshow = f"LIST(len={len(t)})" if isinstance(t, list) else repr(t)
                print(f"   {json.dumps(i, ensure_ascii=False)}")
            print("outputs (full):")
            for o in n.get("outputs", []):
                print(f"   {json.dumps(o, ensure_ascii=False)}")
            print("widgets_values:", n.get("widgets_values"))
            print()
            break  # first LoadImage per file
