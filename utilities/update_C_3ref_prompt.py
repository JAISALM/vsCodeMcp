import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headturn_3ref.json'
TXT = r'D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_C_3ref.txt'

PROMPT = """subject_definitions:
<Subject 1> is the young boy in <Picture 1>, <Picture 2> and <Picture 3> - short dark hair, rose-pink collared shirt, black trousers. His face, hair, clothing and build come from the reference images, NOT from this text description.
<Picture 1> is the FIRST frame: the boy seated at the wooden table, facing the camera, hands resting on the table edge.
<Picture 2> is the MIDDLE frame: the same boy seen from his left-back side, head turned about 90 degrees to the left.
<Picture 3> is the LAST frame: the boy with his back to the camera, face turned back over his shoulder.

summary:
[reference generation] A 10-second single continuous shot with a LOCKED, completely static camera. <Subject 1> slowly turns his head 180 degrees to the left in the first half, passing through <Picture 2>, then holds the <Picture 3> pose while speaking English with clear lip movement in the second half.

retention_analysis:
<Subject 1> (all frames): fully_preserved - the face, hair, rose-pink shirt and black trousers stay identical in every frame.
<Picture 1> (first frame): fully_preserved - the opening frame is exactly this image.
<Picture 2> (middle frame): fully_preserved - the head passes through this exact pose at about 2.5 seconds.
<Picture 3> (last frame): fully_preserved - the final frame is exactly this image.

detailed_description:
MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: the camera is completely static and locked - NO camera movement, NO pan, NO orbit, NO zoom, for the entire 10 seconds.
Black & white, high contrast, fine film grain. A single young boy sits at a wooden table in a dark room. A single bare bulb hangs directly above his head, the only light source. The room, table, chair and bulb stay EXACTLY the same throughout - the background is locked to the reference images; do not change, add, remove or reposition anything. ONLY ONE boy, no duplicates.
[Shot 1] The shot begins from <Picture 1>. The boy faces the camera, hands on the table edge. His eyes shift first - his gaze turns toward the lens before anything else moves.
[Shot 2] At 00:01.000, his head begins to rotate SLOWLY and deliberately to the LEFT (toward his left shoulder), at a constant slow rate, while his body stays completely still and lit the same.
[Shot 3] At 00:02.500, his head passes through the exact pose of <Picture 2> - seen from the left-back side, about 90 degrees turned.
[Shot 4] At 00:05.000, his head completes the turn and reaches the exact pose of <Picture 3> - back to the camera, face turned back over his shoulder. He holds this pose for the rest of the shot.
[Shot 5] At 00:05.500, with his back to the camera, he speaks quietly with clear LIP MOVEMENT: (S1) says, <d>[English] <breath> I don't know what to say... <pause> I don't know where to start. <long pause> But... <inhale> this is where I start. <pause> So welcome to the Jaisal Kut. </d> His lips move naturally with each word.

overall_soundscape:
Continuous natural ambient sound from edge to edge - quiet room tone, faint bare-bulb hum, the boy's breathing, his quiet voice in the second half. No other sounds.

non_diegetic_music:
NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only."""

d = json.load(io.open(WF, encoding='utf-8'))

done = []
for n in d['nodes']:
    if n['id'] == 138 and n['type'] == 'PrimitiveStringMultiline':
        n['widgets_values'][0] = PROMPT
        done.append('node 138 prompt -> guide-based 6-section (locked camera, 3 anchors, English dialogue)')
    if n['id'] == 136 and n['type'] == 'MiniMaxH3ReferenceToVideo':
        # confirm refs + length
        print("R2V widgets:", n['widgets_values'])
        for inp in n.get('inputs', []):
            if inp.get('name', '').startswith('ref_image'):
                print("  ", inp['name'], "link=", inp.get('link'))

assert done, "node 138 not found"
json.dump(d, io.open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("Saved", WF)

io.open(TXT, 'w', encoding='utf-8').write(
    "# Shot C — THE HOOK — 3-REF R2V (jaisal_intro_C_headturn_3ref.json, node 138)\n"
    "# refs: ref_image_0=jaisal_with_hand_on_table.png (frontal START)\n"
    "#       ref_image_1=jaisal_head_left_back_side.png (90deg MIDDLE anchor)\n"
    "#       ref_image_2=jaisal_head_180_dergree.png (180deg END)\n"
    "# 240 frames (10s), 1344x768, LOCKED camera, head does the twist.\n"
    "# Camera node abandoned (D085): colors/face drifted over 10s.\n\n"
    + PROMPT
)
print("Saved", TXT)
