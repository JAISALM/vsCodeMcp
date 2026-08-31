import json, copy

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = f"{BASE}\\video_minimax_h3_r2v+turbo.json"
DST = f"{BASE}\\jaisal_lowangle.json"

wf = json.load(open(SRC, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

# --- 1) Set the 3 existing LoadImage nodes to images 1, 2, 3 ---
nodes["137"]["widgets_values"] = ["1.png", "image"]
nodes["139"]["widgets_values"] = ["2.png", "image"]
nodes["143"]["widgets_values"] = ["3.png", "image"]

# --- 2) Add 2 new LoadImage nodes for images 4, 5 (native structure) ---
def make_loadimage(node_id, filename, pos):
    return {
        "id": node_id, "type": "LoadImage", "pos": pos, "size": [340, 180],
        "flags": {}, "order": 0, "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
            {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": []},
            {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": []},
        ],
        "properties": {"Node name for S&R": "LoadImage"},
        "widgets_values": [filename, "image"],
    }

# Find a free position (place them near the existing LoadImage nodes)
la4 = make_loadimage("LA4", "4.png", [1700, 0])
la5 = make_loadimage("LA5", "5.png", [1700, 200])
wf["nodes"].append(la4)
wf["nodes"].append(la5)
nodes["LA4"] = la4
nodes["LA5"] = la5

# --- 3) Add a ref_image_4 input to the MiniMax node (after ref_image_3) ---
mm = nodes["136"]
# Find the index of ref_image_3
ref3_idx = None
for i, inp in enumerate(mm["inputs"]):
    if inp["name"] == "ref_images.ref_image_3":
        ref3_idx = i
        break
# Insert ref_image_4 after ref_image_3
ref4_input = {
    "localized_name": "ref_image_4", "name": "ref_images.ref_image_4",
    "type": "IMAGE", "link": None,
}
mm["inputs"].insert(ref3_idx + 1, ref4_input)
ref4_idx = ref3_idx + 1

# --- 4) Wire all 5 images to the MiniMax node ---
# Existing links: 278 (137->136.3=ref_image_0), 282 (139->136.4=ref_image_1), 285 (143->136.5=ref_image_2)
# After inserting ref_image_4 at index 7, inputs after index 7 shift by +1:
#   prompt: 10->11, width: 11->12, height: 12->13, length: 13->14
for l in wf["links"]:
    if l[1] == "138" and l[3] == "136" and l[4] == 10:   # prompt
        l[4] = 11
    elif l[1] == "115" and l[3] == "136" and l[4] == 11:  # width
        l[4] = 12
    elif l[1] == "115" and l[3] == "136" and l[4] == 12:  # height
        l[4] = 13
    elif l[1] == "131" and l[3] == "136" and l[4] == 13:  # length
        l[4] = 14
# Add new links for LA4 -> ref_image_3 (index 6) and LA5 -> ref_image_4 (index 7)
max_link_id = max(l[0] for l in wf["links"])
link_la4 = max_link_id + 1
link_la5 = max_link_id + 2
wf["links"].append([link_la4, "LA4", 0, "136", 6, "IMAGE"])
wf["links"].append([link_la5, "LA5", 0, "136", 7, "IMAGE"])
la4["outputs"][0]["links"] = [link_la4]
la5["outputs"][0]["links"] = [link_la5]

# --- 5) Set the prompt (multi-shot, Jaisal Cut) ---
prompt = (
    "The Jaisal Cut - 15-second multi-shot sequence in an angular 3D art style with brush stroke color texture. "
    "Using the provided references: Image 1 = wide establishing shot of the stone bridge (base scene), "
    "Image 2 = mid-rain shot, Image 3 = close-up drenched shot, Image 4 = after-rain shot, "
    "Image 5 = low-angle ending (water, kid looking up at sky). "
    "Preserve the boy's exact character design, face, school uniform, red school bag, and the stone bridge environment from the references. "
    "Keep the angular 3D art style with brush stroke color texture throughout. "
    "Visual style: angular 3D art style, brush stroke color texture, moody cinematic atmosphere. "
    "The environment stays consistent - a long traditional stone bridge with continuous stone handrails crossing a wide river. "
    "Animation feel: smooth, natural motion, no jittery morphing. "
    "No dialogue, no text, no subtitles. The 'The Jaisal Cut' title is composited in post, NOT rendered by the model. "
    "Shot 1 (0s to 3s): Wide establishing shot. The boy stands on the long stone bridge, the base scene. Camera is wide, showing the bridge crossing the river. The sky is starting to darken. The boy is small in the frame. "
    "Shot 2 (3s to 6s): Mid-rain shot. Rain begins to fall. The boy is in the middle of the bridge as the rain hits. Camera medium shot. The rain is visible, the bridge stones getting wet. "
    "Shot 3 (6s to 9s): Close-up drenched shot. Close-up of the boy's face as he's fully drenched in the rain. Water on his face, hair, uniform. The rain is heavy. Camera close-up. "
    "Shot 4 (9s to 12s): After-rain shot. The rain stops. The boy after the rain, water dripping. Camera medium shot. The sky is clearing slightly. "
    "Shot 5 (12s to 15s): Low-angle ending (long shot). Low angle from the water level, looking up. The boy is drenched, looking up at the sky. The water is in the foreground. Long shot. The boy is small, looking up at the sky above. This is the ending shot where the 'The Jaisal Cut' title will be composited in post. "
    "Important constraints: Keep the whole video in the angular 3D art style with brush stroke color texture. "
    "No 3D-looking CGI (keep the angular 3D art style, not photorealistic). No character redesign. "
    "Keep all motion natural and consistent across shots. The 'The Jaisal Cut' title is composited in post, NOT rendered by the model."
)
# The prompt is in node 138 (PrimitiveStringMultiline)
nodes["138"]["widgets_values"] = [prompt]

# --- 6) Set the save prefix (includes 1, 2, 3, 4, 5) ---
nodes["92"]["widgets_values"] = ["video/Jaisal_LowAngle_1_2_3_4_5", "auto", "auto"]

# --- 7) Set the length to 15 seconds (node 132 = 15 -> 362 frames) ---
nodes["132"]["widgets_values"] = [15]

json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)
print("written:", DST)
print("nodes:", len(wf["nodes"]), "links:", len(wf["links"]))
print("MiniMax inputs:", [(i["name"], i.get("link")) for i in mm["inputs"]])
print("LA4 widgets:", la4["widgets_values"])
print("LA5 widgets:", la5["widgets_values"])
print("prompt length:", len(prompt))
