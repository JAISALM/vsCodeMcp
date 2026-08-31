import json, shutil, os, sys

WF  = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json'
OUT = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output'
INP = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input'

# ---- 1. Copy the 7 images into input with clean names ----
src_names = [
    '1base_starting_sunny.png',
    '2 closeUp.png',
    '3 running medium.png',
    '4Bridge_middle medium.png',
    '5 Jump.png',
    '6UnderWater.png',
    '7title_thejaisalcut.png',
]
dst_names = [
    'jaisal_1_longshot.png',
    'jaisal_2_closeup.png',
    'jaisal_3_running.png',
    'jaisal_4_middle.png',
    'jaisal_5_jump.png',
    'jaisal_6_underwater.png',
    'jaisal_7_title.png',
]
for s, d in zip(src_names, dst_names):
    sp, dp = os.path.join(OUT, s), os.path.join(INP, d)
    if not os.path.exists(sp):
        print('MISSING SOURCE:', sp); sys.exit(1)
    shutil.copy(sp, dp)
    print('Copied', s, '->', d)

# ---- 2. Load workflow ----
d = json.load(open(WF, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

# ---- 3. Update existing LoadImage nodes ----
nodes[137]['widgets_values'] = ['jaisal_1_longshot.png', 'image']   # ref_image_0
nodes[139]['widgets_values'] = ['jaisal_2_closeup.png', 'image']    # ref_image_1

# ---- 4. Add new LoadImage nodes for images 3-7 ----
new_nodes = [
    (147, 'jaisal_3_running.png',     [-2421, 5300]),
    (148, 'jaisal_4_middle.png',      [-2421, 5660]),
    (149, 'jaisal_5_jump.png',        [-2421, 6020]),
    (150, 'jaisal_6_underwater.png',  [-2421, 6380]),
    (151, 'jaisal_7_title.png',       [-2421, 6740]),
]
for nid, fname, pos in new_nodes:
    node = {
        "id": nid, "type": "LoadImage", "pos": pos, "size": [290, 330],
        "flags": {}, "order": 0, "mode": 0,
        "inputs": [
            {"localized_name": "image", "name": "image", "type": "COMBO", "widget": {"name": "image"}, "link": None},
            {"localized_name": "choose file to upload", "name": "upload", "type": "IMAGEUPLOAD", "widget": {"name": "upload"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": []},
            {"localized_name": "MASK", "name": "MASK", "type": "MASK", "links": None},
        ],
        "properties": {"Node name for S&R": "LoadImage"},
        "widgets_values": [fname, "image"],
    }
    d['nodes'].append(node)
    nodes[nid] = node

# ---- 5. Rebuild node 136 inputs: 7 ref_image slots (3-9) + shifted rest ----
def refimg(i, link):
    return {"label": f"ref_image_{i}", "localized_name": f"ref_images.ref_image_{i}",
            "name": f"ref_images.ref_image_{i}", "shape": 7, "type": "IMAGE", "link": link}

new_inputs = [
    {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 272},
    {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 273},
    {"localized_name": "audio_vae", "name": "audio_vae", "type": "VAE", "link": 274},
    refimg(0, 278),
    refimg(1, 289),
    refimg(2, 290),
    refimg(3, 291),
    refimg(4, 292),
    refimg(5, 293),
    refimg(6, 294),
    {"label": "ref_video_0", "localized_name": "ref_videos.ref_video_0", "name": "ref_videos.ref_video_0", "shape": 7, "type": "IMAGE", "link": None},
    {"label": "ref_video_audio_0", "localized_name": "ref_video_audios.ref_video_audio_0", "name": "ref_video_audios.ref_video_audio_0", "shape": 7, "type": "AUDIO", "link": None},
    {"label": "ref_audio_0", "localized_name": "ref_audios.ref_audio_0", "name": "ref_audios.ref_audio_0", "shape": 7, "type": "AUDIO", "link": None},
    {"localized_name": "prompt", "name": "prompt", "type": "STRING", "widget": {"name": "prompt"}, "link": 279},
    {"localized_name": "width", "name": "width", "type": "INT", "widget": {"name": "width"}, "link": 276},
    {"localized_name": "height", "name": "height", "type": "INT", "widget": {"name": "height"}, "link": 277},
    {"localized_name": "length", "name": "length", "type": "INT", "widget": {"name": "length"}, "link": 275},
    {"localized_name": "ref_image_size", "name": "ref_image_size", "type": "COMBO", "widget": {"name": "ref_image_size"}, "link": None},
]
nodes[136]['inputs'] = new_inputs

# ---- 6. Shift downstream link to_slot values (prompt/width/height/length) ----
slot_shift = {279: 13, 276: 14, 277: 15, 275: 16}
for link in d['links']:
    if link[0] in slot_shift:
        link[4] = slot_shift[link[0]]

# ---- 7. Add new ref_image links + wire source IMAGE outputs ----
new_links = [
    (289, 139, 4),
    (290, 147, 5),
    (291, 148, 6),
    (292, 149, 7),
    (293, 150, 8),
    (294, 151, 9),
]
for lid, src_node, tgt_slot in new_links:
    d['links'].append([lid, src_node, 0, 136, tgt_slot, 'IMAGE'])
    nodes[src_node]['outputs'][0]['links'].append(lid)

# ---- 8. New 7-shot prompt (node 138) ----
PROMPT = """subject_definitions:
<Subject 1> is the young schoolboy in <Picture 1>, <Picture 2>, <Picture 3>, <Picture 4>, <Picture 5>, <Picture 6> - short dark hair, rose-pink collared shirt, full-length black trousers, a BLACK school bag, a normal school kid, no tie, no shorts.
<Subject 2> is the long straight traditional stone bridge with a low waist-height stone handrail crossing a wide open river.
<Picture 1> is the first frame of [Shot 1]: the wide long shot of the boy at the start of the bridge.
<Picture 2> is the first frame of [Shot 2]: the close-up of the boy's face.
<Picture 3> is the first frame of [Shot 3]: the boy running along the bridge.
<Picture 4> is the first frame of [Shot 4]: the boy standing in the middle of the bridge, full figure.
<Picture 5> is the first frame of [Shot 5]: the wide low-angle shot of the boy jumping off the bridge.
<Picture 6> is the first frame of [Shot 6]: the boy underwater.
<Picture 7> is the first frame of [Shot 7]: the title card.

summary:
[reference generation] A cinematic 7-shot sequence in a stylized angular 3D art style with thick visible brushstrokes and painterly color texture. The boy runs across a stone bridge as the weather turns from clear to heavy rain, then jumps into the river and sinks underwater, ending on the title. Every transition is smooth and organic.

retention_analysis:
<Subject 1> (appears in [Shot 1]-[Shot 6]): fully_preserved - the boy's face, short dark hair, rose-pink collared shirt, black trousers, and BLACK school bag are retained in every shot.
<Subject 2> (appears in [Shot 1]-[Shot 5]): fully_preserved - the long straight stone bridge with low handrail crossing the wide river is retained. The environment stays EXACTLY as in the references - same bridge, same trees, same river, no new objects.

detailed_description:
The target video is in a stylized angular 3D art style with thick visible brushstrokes, painterly color texture, matte finish, and angular geometric shapes - NOT photorealistic, NOT smooth CGI. All transitions between shots are smooth, organic, and cinematic.
[Shot 1] At 00:00.000, opens exactly on <Picture 1>: <Subject 1> at the start of <Subject 2>. The boy begins to RUN along the bridge. As he runs, the sky darkens from clear to moody overcast, the wind picks up, and rain begins to fall. Camera: a static wide shot that slowly pushes in.
[Shot 2] At 00:02.000, cuts to <Picture 2>: a close-up of <Subject 1>'s face. The camera moves slowly (a gentle push-in / subtle drift) and the wind blows his hair and shirt. Rain streaks are visible.
[Shot 3] At 00:04.000, cuts to <Picture 3>: <Subject 1> running along the middle of the bridge in the rain. Dynamic running motion, the camera tracks alongside him at running pace, wind and rain visible, water splashing on the bridge stones.
[Shot 4] At 00:06.000, cuts to <Picture 4>: <Subject 1> standing in the middle of the bridge, full figure, medium shot. Rain is now falling heavily (add the rainy effect). The camera holds steady with a subtle drift.
[Shot 5] At 00:08.000, cuts to <Picture 5>: a wide low-angle shot from the river surface. <Subject 1> jumps off the bridge and the camera completes his motion as he moves down into the river, a big splash.
[Shot 6] At 00:10.000, cuts to <Picture 6>: <Subject 1> underwater. The camera follows him as he sinks completely down into the dark open water, rising bubbles, his figure drifting down out of sight.
[Shot 7] At 00:12.000, cuts to <Picture 7>: the title card. The water is calm and dark, the title 'The Jaisal Cut' (formed from rising bubbles) is clearly visible and centered, held steady.

overall_soundscape:
Light wind building, rain intensifying, splashing water on the bridge stones, a big splash as the boy jumps in, then muffled underwater ambience.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles. The 'The Jaisal Cut' title is shown in the final shot and is NOT rendered by the model as a text overlay."""
nodes[138]['widgets_values'] = [PROMPT]

# ---- 9. Update last ids + save ----
d['last_node_id'] = 151
d['last_link_id'] = 294
json.dump(d, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Wrote', WF)
print('Chain: 7 LoadImage (137,139,147,148,149,150,151) -> MiniMaxH3ReferenceToVideo (136) ref_image_0..6')
print('Prompt updated (node 138): 7-shot sequence, black school bag, smooth organic transitions')
