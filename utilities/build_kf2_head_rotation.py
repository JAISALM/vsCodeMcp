import json, shutil, os

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json'
WF_DIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'
INPUT_DIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input'
OUT_00004 = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_kf2_manual_inpaint_00004_.png'
STAGED_REF = 'kf2_00004_ref.png'

# 1. Stage 00004 into input as the reference
dst_ref = os.path.join(INPUT_DIR, STAGED_REF)
shutil.copy(OUT_00004, dst_ref)
print('STAGED', dst_ref)

# 2. Load the identity-edit workflow
d = json.load(open(SRC, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

# Shared scene lock (everything that must stay EXACTLY as 00004)
SCENE = ("The same young man, same face, same identity, same black shirt unbuttoned over a white t-shirt, "
         "seated at the same wooden table, same single bare bulb hanging above, same pure black void background, "
         "same black and white high-contrast cinematic look. ")

NEG_COMMON = ("extra chair, wall, bright background, white background, color, multiple people, duplicate, "
              "two people, two men, second person, twin, mirror image, reflection of a person, "
              "different face, different person, tilted camera, dutch angle, objects on the table, clutter, grain, speckles")

ONE_PERSON = ("ONLY ONE single person in the entire frame, a single young man, NO second person, NO duplicate, "
              "NO twin, NO mirror image, NO reflection, exactly one figure. ")

frames = [
    {
        'file': 'krea2_kf2_hands_table.json',
        'save': 'jaisal_cut/kf2_hands_table',
        'seed': 42,
        'pos': (ONE_PERSON + SCENE +
            "SAME straight-on centered symmetric eye-level static camera as the reference. "
            "ONLY CHANGE: both of his hands are now placed flat on the table surface in front of him, "
            "palms down, fingers relaxed, as if he is ready to talk to the camera. "
            "He is looking directly at the camera with a calm, ready expression, a subtle natural motion "
            "as if he just sat down and is about to speak. "
            "Everything else remains EXACTLY the same as the reference - same face, same body, same table, "
            "same bulb, same void, same lighting, same composition, same camera angle. "
            "Do NOT change the camera angle. Do NOT rotate the head. Do NOT add any objects."),
        'neg': (NEG_COMMON + ", head turned, head rotated, camera rotated, side view, back view"),
    },
    {
        'file': 'krea2_kf2_head90.json',
        'save': 'jaisal_cut/kf2_head90',
        'seed': 43,
        'pos': (ONE_PERSON + SCENE +
            "Both of his hands placed flat on the table surface in front of him. "
            "This is a SIDE VIEW: the camera is positioned to the side of the table, so we see the single young man in PROFILE (his side face, nose pointing to the side of the frame). "
            "His head is turned to the side (a 90 degree profile). "
            "His body and shoulders stay seated at the table. "
            "Everything else remains EXACTLY the same as the reference - same face, same body, same table, same bulb, same void, same lighting. "
            "There is ONLY ONE man in this frame, seen from the side. Do NOT show two men. Do NOT show a front view."),
        'neg': (NEG_COMMON + ", body turned, shoulders turned, front view, back view, two men side by side, facing each other"),
    },
    {
        'file': 'krea2_kf2_head180.json',
        'save': 'jaisal_cut/kf2_head180',
        'seed': 44,
        'pos': (ONE_PERSON + SCENE +
            "Both of his hands placed flat on the table surface in front of him. "
            "This is a BACK VIEW: the camera is positioned BEHIND the single young man, so we see his back, his shoulders, and the back of his head. "
            "BUT his head is turned all the way around (rotated 180 degrees) so his FACE is visible, turned over his shoulder looking back at the camera - a creepy horror look. "
            "His body and shoulders stay in the back view (facing away from the camera). "
            "Everything else remains EXACTLY the same as the reference - same face, same body, same table, same bulb, same void, same lighting. "
            "There is ONLY ONE man in this frame, seen from behind with his face turned around over his shoulder. Do NOT show two men. Do NOT show a front view."),
        'neg': (NEG_COMMON + ", body turned around, shoulders turned around, front view, side view, two men, back of head only, face not visible"),
    },
]

for f in frames:
    # deep copy the workflow
    import copy
    dd = copy.deepcopy(d)
    nn = {n['id']: n for n in dd['nodes']}
    # reference image
    nn[72]['widgets_values'][0] = STAGED_REF
    # output size = match 00004 (1928x1088)
    nn[82]['widgets_values'] = [1928, 1088, 1]
    # positive instruction
    nn[84]['widgets_values'][0] = f['pos']
    # grounding_px = 768 (safe, avoids composition split)
    nn[84]['widgets_values'][1] = 768
    # negative
    nn[85]['widgets_values'][0] = f['neg']
    nn[85]['widgets_values'][1] = 768
    # save prefix
    nn[29]['widgets_values'][0] = f['save']
    # fixed seed
    nn[53]['widgets_values'][0] = f['seed']
    # ref_boost stays 4 (face lock)
    nn[79]['widgets_values'] = [4, 1, 'fit']
    out = os.path.join(WF_DIR, f['file'])
    json.dump(dd, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('WROTE', out)

print('DONE')
