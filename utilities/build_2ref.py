import json, shutil

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json"
shutil.copy(p, p + ".pre_2ref.bak")
wf = json.load(open(p, encoding="utf-8"))

# --- 1. Delete the 3 unused LoadImage nodes (143=3.png, LA4=4.png, LA5=5.png) ---
delete_ids = {"143", "LA4", "LA5"}
wf["nodes"] = [n for n in wf["nodes"] if str(n["id"]) not in delete_ids]
deleted_nodes = len(delete_ids)

# --- 2. Delete their links (285: 143->136.5, 289: LA4->136.6, 290: LA5->136.7) ---
delete_links = {285, 289, 290}
wf["links"] = [l for l in wf["links"] if l[0] not in delete_links]

# --- 3. MiniMax node: clear link fields on ref_image_2/3/4 ---
for n in wf["nodes"]:
    if n["type"] == "MiniMaxH3ReferenceToVideo":
        for i in n["inputs"]:
            if i["name"] in ("ref_images.ref_image_2", "ref_images.ref_image_3", "ref_images.ref_image_4"):
                i["link"] = None
        print("MiniMax node: ref_image_2/3/4 link fields cleared")

# --- 4. New simple 2-image prompt (clear 1-to-1 mapping) ---
prompt = """subject_definitions:
<Subject 1> is the young boy in <Picture 1> and <Picture 2>, with short dark hair, a school uniform, and a red school bag.
<Subject 2> is the long traditional stone bridge with continuous stone handrails crossing a wide river, in <Picture 1> and <Picture 2>.
<Picture 1> is the first frame of [Shot 1]: the boy at the start of the bridge.
<Picture 2> is the first frame of [Shot 2]: the boy in the middle of the bridge.

summary:
[reference generation] A 15-second two-shot sequence in an angular 3D art style with brush stroke color texture. [Shot 1] begins from <Picture 1> (the boy at the start of the bridge) and [Shot 2] begins from <Picture 2> (the boy in the middle of the bridge). The boy walks, the weather turns, and he runs through the rain.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the boy's face, short dark hair, school uniform, and red school bag are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the long stone bridge with continuous handrails crossing the wide river is retained.
<Picture 1> ([Shot 1] first frame): fully_preserved - the boy at the start of the bridge is the opening frame.
<Picture 2> ([Shot 2] first frame): fully_preserved - the boy in the middle of the bridge is the opening frame of Shot 2.

detailed_description:
The target video is in an angular 3D art style with brush stroke color texture, cinematic lighting, and a moody rain palette.
[Shot 1] A wide shot opens exactly on <Picture 1>: <Subject 1>, the young boy in a school uniform with a red school bag, stands at the start of <Subject 2>, the long stone bridge. The boy begins walking forward along the bridge. As he walks, the sky darkens, the wind picks up, and rain begins to fall. The boy starts running as the rain intensifies.
[Shot 2] At 00:07.000, the shot cuts to <Picture 2>: <Subject 1> in the middle of the bridge, running through the heavy rain, fully drenched. Water splashes on the bridge stones. The camera follows the boy as he runs.

overall_soundscape:
Light wind building, rain intensifying, and splashing water on the bridge stones.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles. The 'The Jaisal Cut' title is composited in post and is NOT rendered by the model."""

for n in wf["nodes"]:
    if str(n["id"]) == "138":
        n["widgets_values"] = [prompt]
        print("Prompt updated on node 138 (2-image, simple)")
    if n["type"] == "SaveVideo":
        n["widgets_values"][0] = "video/Jaisal_2Ref_1_2"
        print("SaveVideo -> video/Jaisal_2Ref_1_2")

json.dump(wf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Saved. Deleted nodes:", deleted_nodes)
