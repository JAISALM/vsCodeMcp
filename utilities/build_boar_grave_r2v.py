import json, copy

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\minimax_h3_sam_r2v_2char_cinematic.json'
DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\minimax_h3_boar_grave_talking_r2v.json'

PROMPT = """How the reference video and pictures align with the target video — the target
video is an edited version of <Video 1>, replacing the blue silhouette with
<Subject 2>, and also replacing the red silhouette with <Subject 4>.

summary:
[video editing] The target video replaces two characters: the blue silhouette
<Subject 1> in <Video 1> is replaced with <Subject 2>, and the red silhouette
<Subject 3> in <Video 1> is replaced with <Subject 4>. The replacement
subjects perform the exact same motion, dialogue, positions and facial
expressions of the silhouettes they replace, while maintaining the original
camera movement and the scene environment.

<Subject 2> is a lean, fit Keralite man in his 30s with a full unkempt
beard, wearing a rose-pink shirt. He is crouched inside the small unfinished
grave hole, still digging with a shovel.
<Subject 4> is a lean Keralite man with a short dense beard, wearing a white
t-shirt, standing at the hole's edge. A third plain man in a plain shirt
stands right next to him, also listening.

Scene: a small unfinished grave hole in the black-soil backyard (parambu) of
a Keralite home, morning light around 9-10 AM. Two coconut trees, scattered
grass patches, a half-broken fence net at the yard boundary, and a dead wild
boar lying on the ground near the hole's edge. A crouching-digging pose
reference and a parambu environment reference are provided to keep the pose
and the environment consistent.

detailed_description:
[Shot 1] At 00:00.000 - A slow push-in from a high wide angle toward the
hole. <Subject 2> crouches inside the hole digging with a shovel;
<Subject 4> and the third man stand close at the rim, looking down at him.
[Shot 2] At 00:02.000 - The camera settles into a medium shot at the rim.
<Subject 2> looks up from the hole and speaks; the two men at the edge
listen. The dead boar lies on the ground near the rim.

overall_soundscape: natural sounds only — shovel scraping soil, low voices,
footsteps, distant birds, wind in the coconut leaves.
non_diegetic_music: NO music, NO instrumental music, NO musical instruments,
NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient
sounds only."""

wf = json.load(open(SRC, encoding='utf-8'))
nodes = {n['id']: n for n in wf['nodes']}


def set_widgets(nid, values, named):
    n = nodes[nid]
    n['widgets_values'] = values
    if 'widgets_values_named' in n:
        n['widgets_values_named'] = named


# --- 4 reference images (connection order = ref_image_0..3) ---
# ref_image_0 <- node 137, ref_image_1 <- 143, ref_image_2 <- 142, ref_image_3 <- 139
set_widgets(137, ['boar_char1_identity.png', 'image'], {'image': 'boar_char1_identity.png'})
set_widgets(143, ['boar_char2_identity.png', 'image'], {'image': 'boar_char2_identity.png'})
set_widgets(142, ['boar_char1_pose_digging.png', 'image'], {'image': 'boar_char1_pose_digging.png'})
set_widgets(139, ['boar_env_parambu.png', 'image'], {'image': 'boar_env_parambu.png'})

# --- reference video = blockout camera-motion clip ---
vw = {"video": "boar_grave_talking_camref.mp4", "force_rate": 24, "custom_width": 0,
      "custom_height": 0, "frame_load_cap": 0, "start_time": 0, "format": "AnimateDiff",
      "videopreview": None}
set_widgets(153, vw, dict(vw, **{"choose video to upload": None}))

# --- prompt ---
set_widgets(138, [PROMPT], {"value": PROMPT})

# --- output prefix ---
old305 = nodes[305]['widgets_values']
new305 = dict(old305)
new305['filename_prefix'] = 'boar_grave'
new305['videopreview'] = None
named305 = dict(nodes[305].get('widgets_values_named') or new305)
named305['filename_prefix'] = 'boar_grave'
named305['videopreview'] = None
nodes[305]['widgets_values'] = new305
nodes[305]['widgets_values_named'] = named305

with open(DST, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False)

print('saved:', DST)
# verify
wf2 = json.load(open(DST, encoding='utf-8'))
n2 = {n['id']: n for n in wf2['nodes']}
for nid in (137, 143, 142, 139, 153):
    print(nid, n2[nid]['type'], '->', json.dumps(n2[nid]['widgets_values'])[:150])
print('prompt starts:', n2[138]['widgets_values'][0][:80])
print('output prefix:', n2[305]['widgets_values']['filename_prefix'])
