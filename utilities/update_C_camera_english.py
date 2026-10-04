import json, io, os

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
INPUT = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input'

# Verify the frontal start frame is available in the ComfyUI input folder
for name in ('jaisal_with_hand_on_table.png', 'jaisal_head_left_back_side.png', 'jaisal_head_180_dergree.png'):
    p = os.path.join(INPUT, name)
    print(("OK  " if os.path.exists(p) else "MISSING ") + name)

d = json.load(io.open(WF, encoding='utf-8'))

INSTRUCTION = (
    "As the camera orbits, the boy turns his head SLOWLY to the LEFT (toward his left shoulder), "
    "ending with his back to the camera and his face turned back over his shoulder. "
    "His BODY stays still and lit the same. "
    "In the second half of the shot, with his back to the camera, he speaks quietly with clear LIP MOVEMENT: "
    "<d>[English] <breath> I don't know what to say... <pause> I don't know where to start. "
    "<long pause> But... <inhale> this is where I start. <pause> So welcome to the Jaisal Kut. </d> "
    "His lips move naturally with each word. "
    "Natural ambient sound only - room tone, bulb hum, breath, his quiet voice. NO music."
)

changed = []
for n in d['nodes']:
    if n['id'] == 215 and n['type'] == 'LoadImage':
        n['widgets_values'][0] = 'jaisal_with_hand_on_table.png'
        changed.append('node 215 ref -> ' + n['widgets_values'][0])
    if n['id'] == 127 and n['type'] == 'H3LocalCameraEditor':
        n['widgets_values'][3] = INSTRUCTION
        changed.append('node 127 instruction -> ' + INSTRUCTION[:60] + '...')

json.dump(d, io.open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("Saved", WF)
for c in changed:
    print("  ", c)
