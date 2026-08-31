import json, copy

BASE = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json'
OUTDIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'

# LoadImage node -> image
LI = {137:'jaisal_1_longshot.png', 139:'jaisal_2_closeup.png', 147:'jaisal_3_running.png',
      148:'jaisal_4_middle.png', 149:'jaisal_5_jump.png', 150:'jaisal_6_underwater.png',
      151:'jaisal_7_title.png'}

# Non-ref links (the model/VAE/CLIP/sampler chain) - keep as-is
NONREF_LINKS = {250,251,253,254,255,256,258,259,260,261,270,271,272,273,274,275,276,277,279,280,281,286,287,288}
REF_LINK_IDS = {278,289,290,291,292,293,294}

def refimg(i, link):
    return {"label": f"ref_image_{i}", "localized_name": f"ref_images.ref_image_{i}",
            "name": f"ref_images.ref_image_{i}", "shape": 7, "type": "IMAGE", "link": link}

def build_pipeline(fname, keep_li, slot_map, prompt, length_s, save_prefix, new_link_ids):
    """keep_li: list of LoadImage node ids to keep.
       slot_map: {loadimage_node_id: target_slot_index} (3,4,5 for ref_image_0,1,2)
       new_link_ids: {loadimage_node_id: new_link_id}
    """
    d = json.load(open(BASE, encoding='utf-8'))
    nodes = {n['id']: n for n in d['nodes']}

    # 1. Keep only the needed LoadImage nodes + all non-LoadImage nodes
    d['nodes'] = [n for n in d['nodes'] if n['type'] != 'LoadImage' or n['id'] in keep_li]
    nodes = {n['id']: n for n in d['nodes']}

    # 2. Rebuild node 136 inputs: 3 ref slots (3,4,5) + rest
    n136 = nodes[136]
    new_inputs = [
        {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 272},
        {"localized_name": "vae", "name": "vae", "type": "VAE", "link": 273},
        {"localized_name": "audio_vae", "name": "audio_vae", "type": "VAE", "link": 274},
        refimg(0, None), refimg(1, None), refimg(2, None), refimg(3, None), refimg(4, None), refimg(5, None),
        {"label": "ref_video_0", "localized_name": "ref_videos.ref_video_0", "name": "ref_videos.ref_video_0", "shape": 7, "type": "IMAGE", "link": None},
        {"label": "ref_video_audio_0", "localized_name": "ref_video_audios.ref_video_audio_0", "name": "ref_video_audios.ref_video_audio_0", "shape": 7, "type": "AUDIO", "link": None},
        {"label": "ref_audio_0", "localized_name": "ref_audios.ref_audio_0", "name": "ref_audios.ref_audio_0", "shape": 7, "type": "AUDIO", "link": None},
        {"localized_name": "prompt", "name": "prompt", "type": "STRING", "widget": {"name": "prompt"}, "link": 279},
        {"localized_name": "width", "name": "width", "type": "INT", "widget": {"name": "width"}, "link": 276},
        {"localized_name": "height", "name": "height", "type": "INT", "widget": {"name": "height"}, "link": 277},
        {"localized_name": "length", "name": "length", "type": "INT", "widget": {"name": "length"}, "link": 275},
        {"localized_name": "ref_image_size", "name": "ref_image_size", "type": "COMBO", "widget": {"name": "ref_image_size"}, "link": None},
    ]
    # wire the 3 ref slots
    for li_id, slot in slot_map.items():
        new_inputs[slot]["link"] = new_link_ids[li_id]
    n136['inputs'] = new_inputs

    # 3. Rebuild links: keep non-ref links, add new ref links
    d['links'] = [l for l in d['links'] if l[0] in NONREF_LINKS]
    for li_id, slot in slot_map.items():
        lid = new_link_ids[li_id]
        d['links'].append([lid, li_id, 0, 136, slot, 'IMAGE'])
        # set the LoadImage node's IMAGE output link
        nodes[li_id]['outputs'][0]['links'] = [lid]

    # 4. Update prompt (node 138)
    nodes[138]['widgets_values'] = [prompt]

    # 5. Update length (node 132) + save prefix (node 92)
    nodes[132]['widgets_values'] = [length_s]
    nodes[92]['widgets_values'] = [save_prefix, 'auto', 'auto']

    # 6. Update last ids
    d['last_node_id'] = max(n['id'] for n in d['nodes'])
    d['last_link_id'] = max(l[0] for l in d['links'])

    path = OUTDIR + '\\' + fname
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'Wrote {fname}: refs={[LI[i] for i in keep_li]}, length={length_s}s, save={save_prefix}')
    return path

# ---------------- Pipeline 1: images 1, 2, 4 (run-up) ----------------
P1 = """subject_definitions:
<Subject 1> is the young schoolboy in <Picture 1>, <Picture 2>, <Picture 3> - short dark hair, rose-pink collared shirt, full-length black trousers, a BLACK school bag, a normal school kid, no tie, no shorts.
<Subject 2> is the long straight traditional stone bridge with a low waist-height stone handrail crossing a wide open river.
<Picture 1> is the first frame of [Shot 1]: the wide long shot of the boy at the start of the bridge.
<Picture 2> is the first frame of [Shot 2]: the close-up of the boy's face as he runs.
<Picture 3> is the first frame of [Shot 3]: the boy at the middle of the bridge, a side view, gathering himself to leap into the river.

summary:
[reference generation] A cinematic 15-second run-up sequence in a stylized angular 3D art style with thick visible brushstrokes and painterly color texture. The boy runs across a stone bridge as the weather turns from clear to heavy rain, then gathers himself at the middle of the bridge and pushes off toward the river. Every transition is smooth and organic, and the color grade stays consistent across all shots.

retention_analysis:
<Subject 1> (appears in [Shot 1]-[Shot 3]): fully_preserved - the boy's face, short dark hair, rose-pink collared shirt, black trousers, and BLACK school bag are retained in every shot.
<Subject 2> (appears in [Shot 1]-[Shot 3]): fully_preserved - the long straight stone bridge with low handrail crossing the wide river is retained. The environment stays EXACTLY as in the references - same bridge, same trees, same river, no new objects.
The COLOR GRADE, lighting, and tone stay EXACTLY consistent across all shots - the same dark moody palette, the same dim grey overcast light, the same water color - so no shot looks like a different scene.

detailed_description:
The target video is in a stylized angular 3D art style with thick visible brushstrokes, painterly color texture, matte finish, and angular geometric shapes - NOT photorealistic, NOT smooth CGI. All transitions between shots are smooth, organic, and cinematic. The color grade is consistent across every shot.
[Shot 1] At 00:00.000, opens exactly on <Picture 1>: <Subject 1> at the start of <Subject 2>. The boy RUNS along the bridge for a good stretch. As he runs, the sky darkens from clear to moody overcast, the wind picks up, and rain begins to fall. Camera: a static wide shot that slowly pushes in. This shot runs for about 7 seconds - give the boy plenty of time to run.
[Shot 2] At 00:07.000, cuts to <Picture 2>: a close-up of <Subject 1>'s face and upper body as he RUNS. Dynamic running motion, the camera tracks with him, the wind blows his hair and shirt, rain streaks visible. NOT a static shot - the boy is clearly running. About 3 seconds.
[Shot 3] At 00:10.000, cuts to <Picture 3>: a SIDE view of <Subject 1> at the middle of the bridge in HEAVY RAIN. He gathers himself, crouches, and the camera slowly ROTATES around him as he climbs over the low handrail and pushes off toward the river, a dynamic pre-jump build. The shot ENDS with him pushing off the edge, mid-launch, so the next clip can pick up his leap. About 5 seconds.

overall_soundscape:
Light wind building, rain intensifying, splashing water on the bridge stones, the boy's running footsteps on the stone, then a rising tension as he gathers to leap.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles."""

# ---------------- Pipeline 2: images 5, 6, 7 (jump + drown + title) ----------------
P2 = """subject_definitions:
<Subject 1> is the young schoolboy in <Picture 1>, <Picture 2> - short dark hair, rose-pink collared shirt, full-length black trousers, a BLACK school bag, a normal school kid, no tie, no shorts.
<Subject 2> is the long straight traditional stone bridge with a low waist-height stone handrail crossing a wide open river.
<Picture 1> is the first frame of [Shot 1]: the boy leaping off the bridge into the river.
<Picture 2> is the first frame of [Shot 2]: the boy underwater.
<Picture 3> is the first frame of [Shot 3]: the title card.

summary:
[reference generation] A cinematic 11-second sequence in a stylized angular 3D art style with thick visible brushstrokes and painterly color texture. The boy makes a short leap into the river, sinks underwater, and the scene resolves into the title. Every transition is smooth and organic, and the color grade stays consistent across all shots.

retention_analysis:
<Subject 1> (appears in [Shot 1]-[Shot 2]): fully_preserved - the boy's face, short dark hair, rose-pink collared shirt, black trousers, and BLACK school bag are retained.
<Subject 2> (appears in [Shot 1]): fully_preserved - the long straight stone bridge with low handrail crossing the wide river is retained. The environment stays EXACTLY as in the references - same bridge, same trees, same river, no new objects.
The COLOR GRADE, lighting, and tone stay EXACTLY consistent across all shots - the same dark moody palette, the same dim grey overcast light, the same water color - so no shot looks like a different scene.

detailed_description:
The target video is in a stylized angular 3D art style with thick visible brushstrokes, painterly color texture, matte finish, and angular geometric shapes - NOT photorealistic, NOT smooth CGI. All transitions between shots are smooth, organic, and cinematic. The color grade is consistent across every shot.
[Shot 1] At 00:00.000, opens exactly on <Picture 1>: <Subject 1> makes a SHORT, natural leap off the near edge of the bridge, dropping into the water CLOSE to the bridge (NOT a long throw, NOT flung far away, NOT like a stone being thrown) - a small, believable jump, a splash where he lands. About 2 seconds.
[Shot 2] At 00:02.000, cuts to <Picture 2>: <Subject 1> underwater. The camera follows him as he sinks completely down into the dark open water, rising bubbles, his figure drifting down out of sight. About 4.5 seconds.
[Shot 3] At 00:07.000, cuts to <Picture 3>: the title card. The water is calm and dark, bubbles foam up, and the title 'The Jaisal Cut' (formed from rising bubbles) slowly becomes visible and centered, held steady. The COLOR GRADE, lighting, and tone EXACTLY match the previous underwater shot (Shot 2) - the same dark moody palette, the same dim grey light, the same water color - so it reads as a CONTINUATION of the underwater shot, NOT a separate shot. About 4 seconds.

overall_soundscape:
A splash as the boy lands, then muffled underwater ambience, rising bubbles, then a calm, quiet underwater hush as the title appears.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles. The 'The Jaisal Cut' title is shown in the final shot and is NOT rendered by the model as a text overlay."""

# Build pipeline 1: images 1 (137), 2 (139), 4 (148) -> slots 3,4,5
build_pipeline(
    'jaisalproduction1.json',
    keep_li=[137, 139, 148],
    slot_map={137:3, 139:4, 148:5},
    prompt=P1, length_s=15, save_prefix='video/Jaisal_Production_1',
    new_link_ids={137:300, 139:301, 148:302},
)

# Build pipeline 2: images 5 (149), 6 (150), 7 (151) -> slots 3,4,5
build_pipeline(
    'jaisalproduction2.json',
    keep_li=[149, 150, 151],
    slot_map={149:3, 150:4, 151:5},
    prompt=P2, length_s=11, save_prefix='video/Jaisal_Production_2',
    new_link_ids={149:300, 150:301, 151:302},
)
print('Done.')
