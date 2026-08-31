import json

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = f"{BASE}\\krea2_jaisal_medium.json"
DST = f"{BASE}\\krea2_jaisal_title_moody.json"

# Ground-truth widget order per node type (confirmed from /object_info widget inputs,
# i.e. the required inputs that are NOT link types).
WIDGET_ORDER = {
    "UNETLoader": ["model_name", "weight_dtype"],
    "CLIPLoader": ["clip_name", "type", "device"],
    "VAELoader": ["vae_name"],
    "LoadImage": ["image"],
    "CLIPTextEncode": ["text"],
    "LoraLoaderModelOnly": ["lora_name", "strength"],
    "SaveImage": ["filename_prefix"],
    "PreviewImage": [],
    "VAEDecode": [],
    "VAEEncode": [],
    "KSampler": ["seed", "steps", "cfg", "sampler_name", "scheduler", "denoise"],
}

# Rebuild title_moody from the clean medium template
wf = json.load(open(SRC, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

moody_prompt = (
    "An angular, 3d art style, with brush stroke color texture. "
    "The exact same scene and composition as the reference image: a wide aerial view of a long traditional stone bridge "
    "with continuous stone handrails crossing a wide river, a small young Indian schoolboy in a neat school uniform "
    "with a red school bag standing in the MIDDLE of the bridge. "
    "Keep the bridge structure, the river, the banks, and the boy's position (center of the bridge) EXACTLY the same as the reference. "
    "ONLY change the climate and atmosphere to MOODY: heavy dark overcast storm clouds filling the sky, dim cold grey light, "
    "low hanging mist over the water, light rain, wet glistening bridge stones, moody cinematic atmosphere, "
    "muted desaturated colors, dramatic moody lighting. "
    "The same angular 3d brush-stroke artstyle throughout. "
    "Exactly one boy, single character, no duplicate, no second kid."
)

# --- set the 4 moody values with CLEAN widget arrays (matching medium's shape) ---
nodes["FKI2I:img"]["widgets_values"] = ["jaisal_title_scene.png"]
nodes["FKI2I:img"]["widgets_values_named"] = {"image": "jaisal_title_scene.png"}

nodes["6"]["widgets_values"] = [moody_prompt]
nodes["6"]["widgets_values_named"] = {"text": moody_prompt}

nodes["3"]["widgets_values"] = [424242, 8, 1.0, "euler", "simple", 0.4]
nodes["3"]["widgets_values_named"] = {"seed": 424242, "steps": 8, "cfg": 1.0,
                                      "sampler_name": "euler", "scheduler": "simple", "denoise": 0.4}

nodes["29"]["widgets_values"] = ["jaisal_cut/title_moody"]
nodes["29"]["widgets_values_named"] = {"filename_prefix": "jaisal_cut/title_moody"}

# --- reposition into a clean grid ---
for idx, n in enumerate(wf["nodes"]):
    col, row = idx % 4, idx // 4
    n["pos"] = [col * 420, row * 320]

json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)
print("rewritten:", DST)

# --- VERIFY every node's widgets_values length against ground-truth widget order ---
print("\n=== VERIFICATION (widgets_values length vs expected widget order) ===")
ok = True
for n in wf["nodes"]:
    t = n["type"]
    expected = WIDGET_ORDER.get(t, ["<unknown type>"])
    vals = n.get("widgets_values")
    named = n.get("widgets_values_named")
    match = (vals is not None) and (len(vals) == len(expected))
    flag = "OK " if match else "BAD"
    if not match:
        ok = False
    print(f"  [{flag}] {t:22} expected={len(expected)} got={len(vals) if vals is not None else None} named={'yes' if named else 'None'}")
    if not match:
        print(f"        expected order: {expected}")
        print(f"        got values:     {vals}")
print("\nALL NODES CLEAN" if ok else "\n*** SOME NODES STILL BAD ***")
