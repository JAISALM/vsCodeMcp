import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json'
d = json.load(open(WF, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

PROMPT = """subject_definitions:
<Subject 1> is the young schoolboy in <Picture 1>, <Picture 2>, <Picture 3> - short dark hair, rose-pink collared shirt, full-length black trousers, a BLACK school bag, a normal school kid, no tie, no shorts.
<Subject 2> is the long straight traditional stone bridge with a low waist-height stone handrail crossing a wide open river.
<Picture 1> is the first frame of [Shot 1]: the long wide shot of the boy at the start of the bridge.
<Picture 2> is the first frame of [Shot 2]: the close-up of the boy's face as he runs.
<Picture 3> is the first frame of [Shot 3]: the boy at the middle of the bridge, a side view from the VIEWER'S LEFT, about to climb over the handrail and leap into the river.

ORIENTATION (important - use the VIEWER's perspective for all left/right):
The boy's RIGHT side is the VIEWER'S LEFT side of the frame. When the boy turns toward his right, he turns toward the VIEWER'S LEFT. [Shot 3] is a side view from the VIEWER'S LEFT side, and the boy is on the VIEWER'S LEFT of the frame.

summary:
[reference generation] A cinematic 15-second run-up sequence in a stylized angular 3D art style with thick visible brushstrokes and painterly color texture. The boy runs slowly across a stone bridge as the sky slowly turns moody, then stops and turns toward his right (the VIEWER'S LEFT), then climbs over the handrail and leaps. ALL THREE shots must appear in this order, each getting its full time - [Shot 1] MUST be a LONG WIDE establishing shot that shows the landscape and the climate change, [Shot 3] MUST appear. Every transition is smooth and organic, and the color grade stays consistent across all shots.

retention_analysis:
<Subject 1> (appears in [Shot 1]-[Shot 3]): fully_preserved - the boy's face, short dark hair, rose-pink collared shirt, black trousers, and BLACK school bag are retained in every shot.
<Subject 2> (appears in [Shot 1]-[Shot 3]): fully_preserved - the long straight stone bridge with low handrail crossing the wide river is retained. The environment stays EXACTLY as in the references - same bridge, same trees, same river, no new objects.
The COLOR GRADE, lighting, and tone stay EXACTLY consistent across all shots - the same dark moody palette, the same dim grey overcast light, the same water color - so no shot looks like a different scene.

detailed_description:
The target video is in a stylized angular 3D art style with thick visible brushstrokes, painterly color texture, matte finish, and angular geometric shapes - NOT photorealistic, NOT smooth CGI. All transitions between shots are smooth, organic, and cinematic. The color grade is consistent across every shot. ALL THREE SHOTS MUST APPEAR IN THIS ORDER, EACH GETTING ITS FULL TIME - do not skip, compress, or drop any shot. [Shot 1] MUST be a LONG WIDE establishing shot (a hard requirement - it must NOT be cut short, NOT turned into a close-up, NOT skipped) that shows the landscape and the climate change. [Shot 3] MUST appear. All left/right references use the VIEWER's perspective.
[Shot 1] At 00:00.000, a LONG WIDE static shot (a HARD REQUIREMENT - the camera does NOT move closer, does NOT push in, does NOT cut to a close-up - it stays a FIXED wide view the whole time): <Subject 1> at the start of <Subject 2>, a small figure on the bridge. The boy runs SLOWLY and DELIBERATELY along the bridge with a REAL running gait - each foot clearly LIFTS and LANDS separately, visible leg movement, one step at a time (NOT a smooth slide, NOT a glide, NOT a blur, NOT a keyframe slide, NOT fast). The MAIN PURPOSE of this shot is to ESTABLISH THE CLIMATE CHANGE - the sky gradually darkens from clear to moody overcast, the wind picks up, and rain begins to fall, the whole landscape and environment shifting from clear to rainy. The camera stays a fixed wide shot the entire time. About 5 seconds.
[Shot 2] At 00:05.000, cuts to <Picture 2>: a close-up of <Subject 1>'s face and upper body as he RUNS. Dynamic running motion, the camera tracks with him, the wind blows his hair and shirt, rain streaks visible. Then the boy SLOWS and STOPS, and TURNS to look toward HIS RIGHT side, which is the VIEWER'S LEFT (toward the river). About 5 seconds for the running, stopping, and turning.
[Shot 3] At 00:10.000, cuts to <Picture 3>: a SIDE view from the VIEWER'S LEFT of <Subject 1> at the middle of the bridge in HEAVY RAIN - the boy is on the VIEWER'S LEFT of the frame, on his right side. The camera is positioned on the VIEWER'S LEFT side and TRACKS the boy (it stays anchored on the VIEWER'S LEFT, it does NOT sweep from left to right) as the boy climbs over the low handrail. Then as he JUMPS, the camera swings around to his BACK side. The shot ENDS with the camera at his BACK as he is in the air, mid-leap, so the next clip can pick up his jump. About 5 seconds.

overall_soundscape:
Clear running footsteps on the stone bridge, heavy rain, a building thunderstorm with distant thunder rumbles, splashing water on the bridge stones, then a rising tension as the boy climbs and leaps.

non_diegetic_music:
Only natural sounds, no musical instruments. No dialogue, no text, no subtitles."""

nodes[138]['widgets_values'] = [PROMPT]
json.dump(d, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Updated jaisalproduction1.json node 138 prompt (v5)')
print('Length:', len(PROMPT), 'chars')
