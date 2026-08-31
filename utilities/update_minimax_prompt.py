import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json'
d = json.load(open(WF, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

PROMPT = """subject_definitions:
<Subject 1> is the young schoolboy in <Picture 1>, <Picture 2>, <Picture 3>, <Picture 4>, <Picture 5>, <Picture 6> - short dark hair, rose-pink collared shirt, full-length black trousers, a BLACK school bag, a normal school kid, no tie, no shorts.
<Subject 2> is the long straight traditional stone bridge with a low waist-height stone handrail crossing a wide open river.
<Picture 1> is the first frame of [Shot 1]: the wide long shot of the boy at the start of the bridge.
<Picture 2> is the first frame of [Shot 2]: the close-up of the boy's face as he runs.
<Picture 3> is the first frame of [Shot 3]: the boy running along the bridge (a brief transitional stitch).
<Picture 4> is the first frame of [Shot 4]: the boy at the middle of the bridge, a side shot, gathering effort to leap into the river.
<Picture 5> is the first frame of [Shot 5]: the boy leaping off the bridge into the river.
<Picture 6> is the first frame of [Shot 6]: the boy underwater.
<Picture 7> is the first frame of [Shot 7]: the title card.

summary:
[reference generation] A cinematic 7-shot sequence in a stylized angular 3D art style with thick visible brushstrokes and painterly color texture. The boy runs across a stone bridge as the weather turns from clear to heavy rain, then leaps into the river and sinks underwater, ending on the title. Every transition is smooth and organic, and the color grade stays consistent across all shots.

retention_analysis:
<Subject 1> (appears in [Shot 1]-[Shot 6]): fully_preserved - the boy's face, short dark hair, rose-pink collared shirt, black trousers, and BLACK school bag are retained in every shot.
<Subject 2> (appears in [Shot 1]-[Shot 5]): fully_preserved - the long straight stone bridge with low handrail crossing the wide river is retained. The environment stays EXACTLY as in the references - same bridge, same trees, same river, no new objects.
The COLOR GRADE, lighting, and tone stay EXACTLY consistent across all shots - the same dark moody palette, the same dim grey overcast light, the same water color - so no shot looks like a different scene.

detailed_description:
The target video is in a stylized angular 3D art style with thick visible brushstrokes, painterly color texture, matte finish, and angular geometric shapes - NOT photorealistic, NOT smooth CGI. All transitions between shots are smooth, organic, and cinematic. The color grade is consistent across every shot.
[Shot 1] At 00:00.000, opens exactly on <Picture 1>: <Subject 1> at the start of <Subject 2>. The boy begins to RUN along the bridge. As he runs, the sky darkens from clear to moody overcast, the wind picks up, and rain begins to fall. Camera: a static wide shot that slowly pushes in.
[Shot 2] At 00:02.000, cuts to <Picture 2>: a close-up of <Subject 1>'s face and upper body as he RUNS. Dynamic running motion, the camera tracks with him, the wind blows his hair and shirt, rain streaks visible. NOT a static shot - the boy is clearly running.
[Shot 3] At 00:04.000, a brief transitional stitch to <Picture 3>: <Subject 1> running along the middle of the bridge in the rain, a short bridge between the close-up and the next shot, the camera tracking alongside him, wind and rain visible.
[Shot 4] At 00:06.000, cuts to <Picture 4>: a SIDE shot of <Subject 1> at the middle of the bridge in HEAVY RAIN, crouching and gathering effort to leap into the river, a dynamic pre-jump pose (NOT standing still, NOT static), the camera at his level from the side. Rain is falling heavily.
[Shot 5] At 00:08.000, cuts to <Picture 5>: <Subject 1> makes a SHORT, natural leap off the near edge of the bridge, dropping into the water CLOSE to the bridge (NOT a long throw, NOT flung far away, NOT like a stone being thrown) - a small, believable jump, a splash where he lands.
[Shot 6] At 00:10.000, cuts to <Picture 6>: <Subject 1> underwater. The camera follows him as he sinks completely down into the dark open water, rising bubbles, his figure drifting down out of sight.
[Shot 7] At 00:12.000, cuts to <Picture 7>: the title card. The water is calm and dark, the title 'The Jaisal Cut' (formed from rising bubbles) is clearly visible and centered, held steady. The COLOR GRADE, lighting, and tone EXACTLY match the previous underwater shot (Shot 6) - the same dark moody palette, the same dim grey light, the same water color - so it reads as a CONTINUATION of the underwater shot, NOT a separate shot.

overall_soundscape:
Light wind building, rain intensifying, splashing water on the bridge stones, a splash as the boy leaps in, then muffled underwater ambience.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles. The 'The Jaisal Cut' title is shown in the final shot and is NOT rendered by the model as a text overlay."""

nodes[138]['widgets_values'] = [PROMPT]
json.dump(d, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Updated node 138 prompt in', WF)
print('Length:', len(PROMPT), 'chars')
