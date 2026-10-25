import json, io

base_path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_fair_test.json"
out_path  = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_raw_qtest.json"
hard = json.load(open(r"D:\models\vsCodeMcp\utilities\hard_test_prompts.json", encoding="utf-8"))

# 3 comparison prompts = same as turbo hard test: [2] close-up, [1] profile, [8] both football
prompts = [hard[1], hard[0], hard[7]]
assert prompts[0].startswith("jeskvman,") and "EXTREME CLOSE-UP" in prompts[0]
assert "EXTREME LEFT PROFILE" in prompts[1]
assert prompts[2].startswith("jeskvman and dlorman")

w = json.load(open(base_path, encoding="utf-8"))
state = {"version":2, "prompts":prompts, "text":"", "split":"line", "expand":True, "trim":True, "skipEmpty":True, "cap":200, "wiredAt":"after"}
blob = json.dumps(state, separators=(",", ":"))

for n in w["nodes"]:
    if n["id"] == 55:
        n["widgets_values"] = ["krea2_raw_bf16.safetensors", "default"]
    elif n["id"] == 53:
        n["widgets_values"] = [42, "randomize", 40, 3.5, "euler", "simple", 1]
    elif n["id"] == 200:
        n["widgets_values"] = [blob]
        n["widgets_values_named"] = {"prompteach": blob}
    elif n["id"] == 29:
        n["widgets_values"] = ["krea2_raw_qtest"]

with io.open(out_path, "w", encoding="utf-8") as f:
    f.write(json.dumps(w, indent=1))
print("WROTE", out_path)
print("unet=raw, steps=40, cfg=3.5, 3 prompts (close-up, profile, both-football), prefix=krea2_raw_qtest")
