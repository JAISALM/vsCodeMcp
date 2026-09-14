import json, os, shutil, copy

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json'
WF_DIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'
INPUT_DIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input'
# Anchor = the PERFECT back-view (kf3a v7) - body already in back view, only the head rotates
ANCHOR_SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut\kf3a_headnormal_v7_00001_.png'
STAGED_REF = 'kf3a_v7_back_ref.png'

shutil.copy(ANCHOR_SRC, os.path.join(INPUT_DIR, STAGED_REF))
print('STAGED', STAGED_REF)

d = json.load(open(SRC, encoding='utf-8'))

SCENE = ("The same young man, same face, same identity, dark wavy hair, dark complexion, black shirt, "
         "seated at the same wooden table on the same wooden chair, same single bare bulb hanging above, "
         "same pure black void background, same black and white high-contrast cinematic look. "
         "The camera is a BACK VIEW - we see his back, his shoulders, and the back of his head. ")
ONE_PERSON = ("ONLY ONE single person in the entire frame, a single young man, NO second person, NO duplicate, "
              "NO twin, NO mirror image, NO reflection, exactly one figure, one man only. ")
NEG_COMMON = ("extra chair, wall, bright background, white background, color, multiple people, duplicate, "
              "two people, two men, three people, three men, second person, twin, mirror image, reflection of a person, "
              "different face, different person, tilted camera, dutch angle, objects on the table, clutter, grain, speckles")

frames = [
    {
        'file': 'krea2_kf3b_head180.json',
        'save': 'jaisal_cut/kf3b_head180',
        'seed': 501,
        'pos': (ONE_PERSON + SCENE +
            "HORROR GHOST LOOK: his head is rotated a FULL 180 degrees, so his FACE is turned all the way around "
            "over his shoulder and is looking STRAIGHT AT THE CAMERA. His face is FULLY VISIBLE and FACING THE CAMERA "
            "(not a side profile, not turned to the left or right side) - his eyes are staring directly at the viewer, "
            "a creepy unsettling horror look, like a ghost turning around to look at you. "
            "We see his back and shoulders (still in the back view, facing away), but his face is turned completely around "
            "over his shoulder, facing the camera head-on. "
            "His body and shoulders do NOT turn - they stay in the back view, facing away. ONLY the head is rotated 180 degrees. "
            "Everything else remains EXACTLY the same as the reference - same table, same chair, same bulb, same void, same lighting. "
            "There is ONLY ONE man in this frame. Do NOT show two men. Do NOT show a front view of the body."),
        'neg': (NEG_COMMON + ", body turned around, shoulders turned around, front view of body, face not visible, back of head only, two men, "
                "face in profile, side of face, face pointing sideways, face turned to the side, face looking to the left, face looking to the right, "
                "face looking away from camera, 270 degree rotation, head over-rotated"),
    },
    {
        'file': 'krea2_kf3c_head90.json',
        'save': 'jaisal_cut/kf3c_head90',
        'seed': 502,
        'pos': (ONE_PERSON + SCENE +
            "IN-BETWEEN FRAME: his head is rotated about 90 degrees to the side, so we see the SIDE of his face in profile "
            "(his nose pointing to the side of the frame). This is the mid-point of a slow head twist. "
            "His body and shoulders do NOT turn - they stay in the back view, facing away. ONLY the head is rotated to the side. "
            "Everything else remains EXACTLY the same as the reference - same table, same chair, same bulb, same void, same lighting. "
            "There is ONLY ONE man in this frame. Do NOT show two men. Do NOT show a front view of the body."),
        'neg': (NEG_COMMON + ", body turned around, shoulders turned around, front view of body, face fully visible front, two men"),
    },
]

for f in frames:
    dd = copy.deepcopy(d)
    nn = {n['id']: n for n in dd['nodes']}
    nn[72]['widgets_values'][0] = STAGED_REF
    nn[82]['widgets_values'] = [1928, 1088, 1]
    nn[84]['widgets_values'][0] = f['pos']
    nn[84]['widgets_values'][1] = 768
    nn[85]['widgets_values'][0] = f['neg']
    nn[85]['widgets_values'][1] = 768
    nn[29]['widgets_values'][0] = f['save']
    nn[53]['widgets_values'][0] = f['seed']
    nn[79]['widgets_values'] = [4, 1, 'fit']
    for n in dd['nodes']:
        if n['type'] == 'Image Comparer (rgthree)':
            n['mode'] = 4
    out = os.path.join(WF_DIR, f['file'])
    json.dump(dd, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('WROTE', out)
print('DONE')
