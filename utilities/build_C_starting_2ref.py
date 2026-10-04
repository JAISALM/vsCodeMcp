import json, io, os, shutil

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headturn_3ref.json'
DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_starting_2ref.json'
TXT = r'D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_C_starting.txt'

PROMPT = """subject_definitions:
<Subject 1> is the boy in <Picture 1> and <Picture 2>. His identity, face, hair, clothing and build come ENTIRELY from the reference images - do not alter his appearance in any way.
<Picture 1> is the FIRST frame: the boy seated at the table, facing the camera, hands resting on the table edge.
<Picture 2> is the LAST frame: the boy seen from his left side, head turned about 90 degrees to the left, face looking directly into the camera.

summary:
[reference generation] A 10-second single continuous shot. <Subject 1> is seated, facing the camera. He speaks, then the camera performs ONE slow 90-degree orbit to his left while his head slowly follows the camera (turning left) to keep looking at the lens. His body stays completely still the whole time. The shot ends with the camera at his left side and his face looking directly into the lens.

retention_analysis:
<Subject 1> (all frames): fully_preserved - his appearance is identical in every frame, exactly as in the reference images.
<Picture 1> (first frame): fully_preserved - the opening frame is exactly this image.
<Picture 2> (last frame): fully_preserved - the final frame is exactly this image.

detailed_description:
MANDATORY SHOT CONSTRAINT, HIGHEST PRIORITY ABOVE ALL ELSE: ONE single continuous shot - NO cuts, NO jump cuts, NO morphing, NO pose-to-pose jumps. The camera performs ONE slow 90-degree orbit to the boy's LEFT (counter-clockwise seen from above), starting exactly at <Picture 1> and ending exactly at <Picture 2>. The camera does NOT orbit 180 degrees, does NOT complete a full circle, does NOT return to the start, does NOT continue past the 90-degree endpoint. The boy's BODY (shoulders, torso, arms, hands, chair, table) stays COMPLETELY STILL and fixed the entire time - ONLY his head moves. His head slowly follows the camera, turning to the LEFT, so he keeps looking at the lens.
Black & white cinematic photography, high contrast, subtle fine film grain, 85mm close-up feel. A single bare bulb hangs directly above the boy, the only light source. The background is a PURE BLACK VOID - featureless darkness. NO room, NO wall, NO door, NO ceiling, NO furniture, NO architecture, NO objects, NO environmental details. As the camera orbits, the background STAYS a pure black void - DO NOT reveal anything behind the boy, DO NOT generate a door or wall at the side angle. ONLY ONE boy, no duplicates.
[0.00-1.00s] The boy is seated, facing the camera, hands on the table edge. Almost completely still. His eyes shift subtly toward the lens. He says, quiet and natural, with clear lip movement: (S1) <d>[English] I don't know what to say. </d>
[1.00-2.00s] A small pause. He is still, looking at the camera. His eyes hold the lens.
[2.00-3.00s] The camera begins a slow orbit to his LEFT. He says: (S1) <d>[English] I don't know where to start. </d>
[3.00-4.00s] The camera continues orbiting left. His head begins to slowly follow, turning to the LEFT, keeping his gaze on the lens.
[4.00-5.00s] The camera continues. His head continues turning left, smoothly, at the same slow rate as the camera.
[5.00-6.00s] The camera approaches his left side. His head keeps following.
[6.00-7.00s] The camera reaches his left side (about 90 degrees). A pause.
[7.00-8.00s] He looks directly at the camera - his head is now turned about 90 degrees to the left, face into the lens. He says: (S1) <d>[English] But... here we start. </d>
[8.00-9.00s] A beat. He holds the pose, looking at the camera.
[9.00-10.00s] He says: (S1) <d>[English] Welcome to the Jaisal Kut. </d> He holds the final pose, matching <Picture 2>.

overall_soundscape:
Continuous natural ambient sound from edge to edge - quiet room tone, faint bare-bulb hum, the boy's breathing, his quiet voice. No other sounds.

non_diegetic_music:
NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only."""

# Load the 3-ref workflow as the base
d = json.load(io.open(SRC, encoding='utf-8'))

# 1. Remove the 3rd ref (node 152 = jaisal_head_180_dergree.png) + its link (307)
removed_nodes = []
d['nodes'] = [n for n in d['nodes'] if not (n['id'] == 152)]
removed_nodes.append('node 152 (180deg LoadImage)')

# 2. Remove link 307 (152 -> ref_image_2)
before = len(d['links'])
d['links'] = [l for l in d['links'] if l[0] != 307]
print("Removed links:", before - len(d['links']))

# 3. Clear the ref_image_2 input on the R2V node (136)
for n in d['nodes']:
    if n['id'] == 136 and n['type'] == 'MiniMaxH3ReferenceToVideo':
        for inp in n.get('inputs', []):
            if inp.get('name') == 'ref_images.ref_image_2':
                inp['link'] = None
                print("Cleared ref_image_2 link on node 136")
        # confirm refs
        print("R2V widgets:", n['widgets_values'])
        for inp in n.get('inputs', []):
            if inp.get('name', '').startswith('ref_image'):
                print("  ", inp['name'], "link=", inp.get('link'))

# 4. Update the prompt (node 138)
done = False
for n in d['nodes']:
    if n['id'] == 138 and n['type'] == 'PrimitiveStringMultiline':
        n['widgets_values'][0] = PROMPT
        done = True
assert done, "node 138 not found"

# 5. Update SaveVideo prefix (node 92)
for n in d['nodes']:
    if n['id'] == 92 and n['type'] == 'SaveVideo':
        n['widgets_values'][0] = 'jaisal_intro_C_starting_2ref'
        print("SaveVideo prefix -> jaisal_intro_C_starting_2ref")

json.dump(d, io.open(DST, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("Saved", DST)

io.open(TXT, 'w', encoding='utf-8').write(
    "# Shot C — THE HOOK (genuinely starting) — 2-REF R2V\n"
    "# File: jaisal_intro_C_starting_2ref.json (node 138 = prompt)\n"
    "# refs: ref_image_0=jaisal_with_hand_on_table.png (frontal START, B's last frame)\n"
    "#       ref_image_1=jaisal_head_left_back_side.png (90deg left, head into lens, END)\n"
    "# 240 frames (10s), 1344x768. Camera = ONE slow 90deg orbit to his LEFT (counter-clockwise\n"
    "# from above); head follows the camera; body stays dead still. Pure black void background.\n"
    "# English dialogue (dub Malayalam later). NO 180deg twist, NO glitch, NO horror.\n"
    "# RULE: NO appearance text - identity comes ENTIRELY from the refs.\n\n"
    + PROMPT
)
print("Saved", TXT)
