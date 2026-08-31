import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_title_moody.json"
wf = json.load(open(p, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

# --- Positive (node 6): anchor pose to reference, don't re-interpret it ---
positive = (
    "An angular, 3d art style, with brush stroke color texture. "
    "The exact same scene, composition, and character pose as the reference image: a wide aerial view of a long traditional stone bridge "
    "with continuous stone handrails crossing a wide river, a small young Indian schoolboy in a neat school uniform with a red school bag "
    "standing in the MIDDLE of the bridge, head tilted back with face and gaze turned upward toward the sky, "
    "EXACTLY matching the reference pose and head angle. "
    "Keep the bridge structure, the river, the banks, the boy's position, body pose, and head angle EXACTLY the same as the reference. "
    "ONLY change the climate and atmosphere to MOODY: heavy dark overcast storm clouds filling the sky, dim cold light, "
    "low hanging mist over the water, light rain, wet glistening bridge stones, moody cinematic atmosphere, "
    "muted desaturated colors, dramatic moody rainy lighting. "
    "The same angular 3d brush-stroke artstyle throughout. "
    "Exactly one boy, single character, no duplicate, no second kid."
)
nodes["6"]["widgets_values"] = [positive]

# --- Negative (node 13): keep identity/structure negatives, replace weak pose ones with concrete pose-locking ---
negative = (
    "houses, buildings, structures, different character, different face, different boy, "
    "very pale skin, white skin, dusky skin, dark skin, shorts, short pants, bare legs, side view, "
    "rounded handrail, rounded railing, decorative railing, exotic railing, ornate railing, curved railing, fancy railing, "
    "close trees, close paddy fields, foreground trees, blurry, low quality, deformed, watermark, text, logo, "
    "cartoon, flat vector, photorealistic, photo, "
    "changed pose, different pose, different body position, head facing forward, head turned to the side, "
    "looking down, looking at camera, turned away, different head angle, different body angle, "
    "shifted position, moved position"
)
nodes["13"]["widgets_values"] = [negative]

# --- KSampler (node 3): denoise 0.4 -> 0.3 (index 6 in the 7-value native shape) ---
ks = nodes["3"]["widgets_values"]
print("KSampler before:", ks)
ks[6] = 0.3
print("KSampler after: ", ks)

json.dump(wf, open(p, "w", encoding="utf-8"), indent=1)
print("\nsaved.")
print("\n=== VERIFY ===")
wf2 = json.load(open(p, encoding="utf-8"))
for n in wf2["nodes"]:
    if n["type"] == "CLIPTextEncode":
        print(f"CLIPTextEncode id={n['id']}: {n['widgets_values'][0][:80]}...")
    if n["type"] == "KSampler":
        print(f"KSampler id={n['id']}: {n['widgets_values']}")
