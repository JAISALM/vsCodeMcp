"""Fix F1: remove ref_image_1 (dead plant) + update prompt to face-camera version.
- Remove node 139 (LoadImage kf6_plants_dead_v9)
- Remove link 317 (139 -> 136.4)
- Clear node 136 ref_image_1 input link
- Update node 138 prompt
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_F1_plants_listen.json"
PROMPT = r"d:\models\vsCodeMcp\Jaisal-intro\prompts\shot_F1_plants_listen.txt"

with open(WF, "r", encoding="utf-8") as f:
    wf = json.load(f)

# Remove node 139
wf["nodes"] = [n for n in wf["nodes"] if n["id"] != 139]
print(f"Removed node 139. Nodes now: {len(wf['nodes'])}")

# Remove link 317
wf["links"] = [l for l in wf["links"] if l[0] != 317]
print(f"Removed link 317. Links now: {len(wf['links'])}")

# Clear node 136 ref_image_1 input link
for n in wf["nodes"]:
    if n["id"] == 136:
        for inp in n["inputs"]:
            if inp["name"] == "ref_images.ref_image_1":
                inp["link"] = None
                print("Cleared node 136 ref_image_1 link")

# Update node 138 prompt
with open(PROMPT, "r", encoding="utf-8") as f:
    new_prompt = f.read().strip()
for n in wf["nodes"]:
    if n["id"] == 138:
        n["widgets_values"] = [new_prompt]
        print(f"Updated node 138 prompt ({len(new_prompt)} chars)")

with open(WF, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=1)
print("Saved F1")
