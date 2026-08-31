import json

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
DST = f"{BASE}\\krea2_jaisal_title_moody.json"

wf = json.load(open(DST, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

# --- KSampler: native shape = 7 values [seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise] ---
nodes["3"]["widgets_values"] = [424242, "randomize", 8, 1.0, "euler", "simple", 0.4]
# remove widgets_values_named (native files don't have it)
nodes["3"].pop("widgets_values_named", None)

# --- LoadImage: native shape = 2 values [filename, 'image'] ---
nodes["FKI2I:img"]["widgets_values"] = ["jaisal_title_scene.png", "image"]
nodes["FKI2I:img"].pop("widgets_values_named", None)

# --- Remove widgets_values_named from ALL nodes (match native format exactly) ---
for n in wf["nodes"]:
    n.pop("widgets_values_named", None)

json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)
print("fixed:", DST)

# --- Verify: compare KSampler + LoadImage against a native file ---
native = json.load(open(f"{BASE}\\krea2_jaisal_base.json", encoding="utf-8"))
def get(wf, t):
    for n in wf["nodes"]:
        if n["type"] == t:
            return n
    return None

print("\n=== VERIFY against native krea2_jaisal_base.json ===")
for t in ("KSampler", "LoadImage"):
    nn = get(native, t)
    mm = get(wf, t)
    print(f"{t}:")
    print(f"  native   widgets_values len={len(nn['widgets_values'])} has_named={'widgets_values_named' in nn}")
    print(f"  fixed    widgets_values len={len(mm['widgets_values'])} has_named={'widgets_values_named' in mm}")
    print(f"  fixed    widgets_values = {mm['widgets_values']}")
    print()

# Confirm no node has widgets_values_named anymore
named_left = [n["type"] for n in wf["nodes"] if "widgets_values_named" in n]
print("nodes still with widgets_values_named:", named_left if named_left else "NONE (clean)")
