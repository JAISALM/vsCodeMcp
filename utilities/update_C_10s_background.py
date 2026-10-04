import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))

INSTRUCTION = (
    "SCENE: A single young boy (short dark hair, rose-pink collared shirt, black trousers) "
    "is seated at a wooden table in a dark room, hands resting on the table edge. A single bare "
    "bulb hangs directly above his head, the only light source. Black & white, high contrast, "
    "fine film grain. The room, table, chair and the single bare bulb stay EXACTLY the same "
    "throughout the entire shot - do NOT change, add, remove or reposition any background "
    "element; the background is locked to the reference image. "
    "HEAD: his EYES shift first (his gaze turns toward the lens). Then his head rotates SLOWLY "
    "and deliberately to the LEFT (toward his left shoulder), in sync with the camera orbit, "
    "ending with his back to the camera and his face turned back over his shoulder. His BODY "
    "stays still and lit the same the whole time. "
    "DIALOGUE: in the second half of the shot, with his back to the camera, he speaks quietly "
    "with clear LIP MOVEMENT: <d>[English] <breath> I don't know what to say... <pause> I don't "
    "know where to start. <long pause> But... <inhale> this is where I start. <pause> So "
    "welcome to the Jaisal Kut. </d> His lips move naturally with each word. "
    "SOUND: natural ambient only - room tone, bulb hum, breath, his quiet voice. NO music. "
    "ONLY ONE boy, no duplicates."
)

changed = []
for n in d['nodes']:
    if n['id'] == 127 and n['type'] == 'H3LocalCameraEditor':
        old_profile = n['widgets_values'][1]
        n['widgets_values'][1] = '243 frames (~10.13s)'
        changed.append('profile: %s -> %s' % (old_profile, n['widgets_values'][1]))
        n['widgets_values'][3] = INSTRUCTION
        changed.append('instruction -> enriched (scene + background lock + head turn + English dialogue)')

json.dump(d, io.open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("Saved", WF)
for c in changed:
    print("  ", c)
