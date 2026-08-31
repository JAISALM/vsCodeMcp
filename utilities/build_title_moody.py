import json

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_medium.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_title_moody.json"

wf = json.load(open(SRC, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

# --- LoadImage: source = the existing title scene (kid on bridge) ---
n = nodes["FKI2I:img"]
n["widgets_values"] = ["jaisal_title_scene.png"]
n["widgets_values_named"] = {"image": "jaisal_title_scene.png"}

# --- Positive prompt: SAME scene/structure, ONLY moody climate ---
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
n = nodes["6"]
n["widgets_values"] = [moody_prompt]
n["widgets_values_named"] = {"text": moody_prompt}

# --- Negative: keep the existing identity/structure negative (already good) ---
# (node 13 unchanged)

# --- KSampler: low denoise 0.4 = atmosphere-only change, structure preserved ---
n = nodes["3"]
n["widgets_values"] = [424242, 8, 1.0, "euler", "simple", 0.4]
n["widgets_values_named"] = {
    "seed": 424242, "steps": 8, "cfg": 1.0,
    "sampler_name": "euler", "scheduler": "simple", "denoise": 0.4,
}

# --- SaveImage: new prefix ---
n = nodes["29"]
n["widgets_values"] = ["jaisal_cut/title_moody"]
n["widgets_values_named"] = {"filename_prefix": "jaisal_cut/title_moody"}

# --- reposition nodes into a clean grid ---
for idx, n in enumerate(wf["nodes"]):
    col, row = idx % 4, idx // 4
    n["pos"] = [col * 420, row * 320]

json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)
print("written:", DST)
print("nodes:", len(wf["nodes"]), "links:", len(wf["links"]))
for nid in ("FKI2I:img", "6", "3", "29"):
    print(f"  id={nid} {nodes[nid]['type']} widgets={nodes[nid]['widgets_values']}")
