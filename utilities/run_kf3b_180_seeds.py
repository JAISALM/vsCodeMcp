import json, os, copy, subprocess, time

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json'
WF_DIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'
SUBMIT = r'd:\models\vsCodeMcp\utilities\submit_krea2_workflow.py'
PY = r'E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe'
STAGED_REF = 'kf3a_v7_back_ref.png'

d = json.load(open(SRC, encoding='utf-8'))

SCENE = ("The same young man, same face, same identity, dark wavy hair, dark complexion, black shirt, "
         "seated at the same wooden table on the same wooden chair, same single bare bulb hanging above, "
         "same pure black void background, same black and white high-contrast cinematic look. "
         "The camera is a BACK VIEW - we see his back, his shoulders, and the back of his head. ")
ONE_PERSON = ("ONLY ONE single person in the entire frame, a single young man, NO second person, NO duplicate, "
              "NO twin, NO mirror image, NO reflection, exactly one figure, one man only. ")
POS = (ONE_PERSON + SCENE +
    "HORROR GHOST LOOK: his head is rotated a FULL 180 degrees, so his FACE is turned all the way around "
    "over his shoulder and is looking STRAIGHT AT THE CAMERA. His face is FULLY VISIBLE and FACING THE CAMERA "
    "(not a side profile, not turned to the left or right side) - his eyes are staring directly at the viewer, "
    "a creepy unsettling horror look, like a ghost turning around to look at you. "
    "We see his back and shoulders (still in the back view, facing away), but his face is turned completely around "
    "over his shoulder, facing the camera head-on. "
    "His body and shoulders do NOT turn - they stay in the back view, facing away. ONLY the head is rotated 180 degrees. "
    "Everything else remains EXACTLY the same as the reference - same table, same chair, same bulb, same void, same lighting. "
    "There is ONLY ONE man in this frame. Do NOT show two men. Do NOT show a front view of the body.")
NEG = ("extra chair, wall, bright background, white background, color, multiple people, duplicate, "
       "two people, two men, three people, three men, second person, twin, mirror image, reflection of a person, "
       "different face, different person, tilted camera, dutch angle, objects on the table, clutter, grain, speckles, "
       "body turned around, shoulders turned around, front view of body, face not visible, back of head only, two men, "
       "face in profile, side of face, face pointing sideways, face turned to the side, face looking to the left, "
       "face looking to the right, face looking away from camera, 270 degree rotation, head over-rotated")

seeds = [601, 602]
for s in seeds:
    dd = copy.deepcopy(d)
    nn = {n['id']: n for n in dd['nodes']}
    nn[72]['widgets_values'][0] = STAGED_REF
    nn[82]['widgets_values'] = [1928, 1088, 1]
    nn[84]['widgets_values'][0] = POS
    nn[84]['widgets_values'][1] = 768
    nn[85]['widgets_values'][0] = NEG
    nn[85]['widgets_values'][1] = 768
    nn[29]['widgets_values'][0] = 'jaisal_cut/kf3b_head180'
    nn[53]['widgets_values'][0] = s
    nn[79]['widgets_values'] = [4, 1, 'fit']
    for n in dd['nodes']:
        if n['type'] == 'Image Comparer (rgthree)':
            n['mode'] = 4
    out = os.path.join(WF_DIR, 'krea2_kf3b_head180.json')
    json.dump(dd, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    r = subprocess.run([PY, SUBMIT, out, '300'], capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if 'prompt_id' in l]
    print('seed', s, line[0] if line else r.stdout[-200:])
    time.sleep(2)
print('SUBMITTED kf3b 2 seeds')
