import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json'
d = json.load(open(WF, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

PROMPT = """subject_definitions:
<Subject 1> is the young schoolboy in <Picture 1>, <Picture 2>, <Picture 3> - short dark hair, rose-pink collared shirt, full-length black trousers, a BLACK school bag, a normal school kid, no tie, no shorts.
<Subject 2> is the long straight traditional stone bridge with a low waist-height stone handrail crossing a wide open river.
<Picture 1> is the first frame of [Shot 1]: the wide long shot of the boy at the start of the bridge.
<Picture 2> is the first frame of [Shot 2]: the close-up of the boy's face as he runs.
<Picture 3> is the first frame of [Shot 3]: the boy at the middle of the bridge, a side view, gathering himself to leap into the river.

summary:
[reference generation] A cinematic 15-second run-up sequence in a stylized angular 3D art style with thick visible brushstrokes and painterly color texture. The boy runs slowly and deliberately across a stone bridge as the weather turns from clear to heavy rain, then stops, turns toward the river, and gathers himself to leap. Every transition is smooth and organic, and the color grade stays consistent across all shots.

retention_analysis:
<Subject 1> (appears in [Shot 1]-[Shot 3]): fully_preserved - the boy's face, short dark hair, rose-pink collared shirt, black trousers, and BLACK school bag are retained in every shot.
<Subject 2> (appears in [Shot 1]-[Shot 3]): fully_preserved - the long straight stone bridge with low handrail crossing the wide river is retained. The environment stays EXACTLY as in the references - same bridge, same trees, same river, no new objects.
The COLOR GRADE, lighting, and tone stay EXACTLY consistent across all shots - the same dark moody palette, the same dim grey overcast light, the same water color - so no shot looks like a different scene.

detailed_description:
The target video is in a stylized angular 3D art style with thick visible brushstrokes, painterly color texture, matte finish, and angular geometric shapes - NOT photorealistic, NOT smooth CGI. All transitions between shots are smooth, organic, and cinematic. The color grade is consistent across every shot.
[Shot 1] At 00:00.000, opens exactly on <Picture 1>: <Subject 1> at the start of <Subject 2>. The boy runs SLOWLY and DELIBERATELY along the bridge at a natural, unhurried pace - each step clearly visible, one foot at a time, his feet landing one after the other on the bridge stones in a clear step-by-step rhythm (NOT rushing, NOT a fast blur, NOT sliding, NOT a smooth glide - real running with distinct steps). As he runs, the sky darkens from clear to moody overcast, the wind picks up, and rain begins to fall. Camera: a static wide shot that slowly pushes in. This shot runs for about 7 seconds.
[Shot 2] At 00:07.000, cuts to <Picture 2>: a close-up of <Subject 1>'s face and upper body as he RUNS. Dynamic running motion, the camera tracks with him, the wind blows his hair and shirt, rain streaks visible. NOT a static shot - the boy is clearly running. Toward the end of the shot, the boy SLOWS and STOPS, then TURNS toward the river side, and the camera PANS to follow him into the next view. About 3 seconds.
[Shot 3] At 00:10.000, cuts to <Picture 3>: a SIDE view of <Subject 1> at the middle of the bridge in HEAVY RAIN. The boy is IN MOTION the whole time - he has just stopped and turned toward the river, he looks down at the water, takes a few steps toward the edge, crouches, and gathers himself to leap, a dynamic pre-jump build. The camera slowly ROTATES around him as he moves. He is NEVER standing still - every moment he is doing something (turning, stepping, looking down, crouching). The shot ENDS with him pushing off the edge, mid-launch, so the next clip can pick up his leap. About 5 seconds.

overall_soundscape:
Light wind building, rain intensifying, splashing water on the bridge stones, the boy's running footsteps on the stone, then a rising tension as he gathers to leap.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles."""

nodes[138]['widgets_values'] = [PROMPT]
json.dump(d, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Updated jaisalproduction1.json node 138 prompt')
print('Length:', len(PROMPT), 'chars')
