import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json'
d = json.load(open(WF, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

PROMPT = """subject_definitions:
<Subject 1> is the young schoolboy in <Picture 1>, <Picture 2>, <Picture 3> - short dark hair, rose-pink collared shirt, full-length black trousers, a BLACK school bag, a normal school kid, no tie, no shorts.
<Subject 2> is the long straight traditional stone bridge with a low waist-height stone handrail crossing a wide open river. The bridge is TALL - it is a high bridge over a wide river, NOT a shallow pool.
<Picture 1> is the first frame of [Shot 1]: the long wide shot of the boy at the start of the bridge.
<Picture 2> is the first frame of [Shot 2]: the close-up of the boy's face as he runs.
<Picture 3> is the first frame of [Shot 3]: the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, already running toward the handrail.

ORIENTATION (use the VIEWER's perspective for all left/right):
The boy's RIGHT side is the VIEWER'S LEFT side of the frame. When the boy turns toward his right, he turns toward the VIEWER'S LEFT. [Shot 3] is a side view from the VIEWER'S LEFT side, and the boy is on the VIEWER'S LEFT of the frame.

summary:
[reference generation] A cinematic 15-second run-up sequence in a stylized angular 3D art style with thick visible brushstrokes and painterly color texture. RAIN is present in every shot. The boy walks and slowly runs across a stone bridge as the sky turns moody and the rain builds, then stops and turns toward his right (the VIEWER'S LEFT), then runs toward the handrail and leaps over it. ALL THREE shots appear in this order, each getting its full time. Every transition is smooth and organic, and the color grade stays consistent across all shots.

retention_analysis:
<Subject 1> (appears in [Shot 1]-[Shot 3]): fully_preserved - the boy's face, short dark hair, rose-pink collared shirt, black trousers, and BLACK school bag are retained in every shot.
<Subject 2> (appears in [Shot 1]-[Shot 3]): fully_preserved - the long straight stone bridge with low handrail crossing the wide river is retained. The environment stays EXACTLY as in the references - same bridge, same trees, same river, no new objects.
The COLOR GRADE, lighting, and tone stay EXACTLY consistent across all shots - the same dark moody palette, the same dim grey overcast light, the same water color - so no shot looks like a different scene.

detailed_description:
The target video is in a stylized angular 3D art style with thick visible brushstrokes, painterly color texture, matte finish, and angular geometric shapes - NOT photorealistic, NOT smooth CGI. RAIN is present in EVERY shot - rain is falling in [Shot 1], [Shot 2], and [Shot 3]. All transitions between shots are smooth, organic, and cinematic. The color grade is consistent across every shot. ALL THREE SHOTS APPEAR IN THIS ORDER, EACH GETTING ITS FULL TIME. All left/right references use the VIEWER's perspective.
[Shot 1] At 00:00.000, a LONG WIDE static shot (the camera stays a FIXED wide view the whole time - it does NOT move closer, does NOT push in, does NOT cut to a close-up): <Subject 1> at the start of <Subject 2>, a small figure on the bridge. The boy WALKS and SLOWLY RUNS along the bridge with a natural gait - each foot clearly LIFTS and LANDS separately, visible leg movement, one step at a time (NOT a smooth slide, NOT a glide, NOT a blur). The MAIN PURPOSE of this shot is to ESTABLISH THE CLIMATE AND MOOD - the sky gradually darkens from clear to moody overcast, RAIN BEGINS TO FALL and builds, the wind picks up, and the whole landscape and environment shifts from clear to rainy. The camera stays a fixed wide shot the entire time. About 4 seconds.
[Shot 2] At 00:04.000, cuts to <Picture 2>: a close-up of <Subject 1>'s face and upper body as he RUNS. Dynamic running motion, the camera tracks with him, the wind blows his hair and shirt, rain streaks visible. Then the boy SLOWS and STOPS, and TURNS to look toward HIS RIGHT side, which is the VIEWER'S LEFT (toward the river) - the turn is clear and deliberate, his body rotates fully toward the VIEWER'S LEFT. About 6 seconds for the running, stopping, and turning.
[Shot 3] At 00:10.000, cuts to <Picture 3>: a SIDE view from the VIEWER'S LEFT of <Subject 1> at the middle of the bridge in HEAVY RAIN - the boy is on the VIEWER'S LEFT of the frame, on his right side. The boy is ALREADY RUNNING and IN MOTION at the start of this shot - he is NOT standing still, he is moving toward the handrail with momentum. The camera is positioned on the VIEWER'S LEFT side and TRACKS the boy (it stays anchored on the VIEWER'S LEFT, it does NOT sweep from left to right). The boy runs toward the low handrail, crouches, plants his feet, and then LEAPS over the handrail - his body fully airborne, a clear dynamic leap. The bridge is TALL, so this is a real leap from height over the wide river, NOT a shallow pool. The camera follows his leap and swings around to his BACK side as he is in the air. The shot ENDS with the camera at his BACK as he is in the air, BEFORE he reaches the water - the cut happens right here, so the next clip picks up the jump. About 5 seconds.

overall_soundscape:
Clear running footsteps on the stone bridge, RAIN THROUGHOUT the whole video (light rain building in [Shot 1], heavier rain in [Shot 2] and [Shot 3]), a building thunderstorm with distant thunder rumbles, splashing water on the bridge stones, then a rising tension as the boy runs and leaps.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles."""

nodes[138]['widgets_values'] = [PROMPT]
json.dump(d, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Updated jaisalproduction1.json node 138 prompt (v8)')
print('Length:', len(PROMPT), 'chars')
