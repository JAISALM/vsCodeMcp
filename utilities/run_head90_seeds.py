import json, os, copy, time, urllib.request

WF_DIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'
SRC = os.path.join(WF_DIR, 'krea2_kf2_head90.json')
SUBMIT = r'd:\models\vsCodeMcp\utilities\submit_krea2_workflow.py'
PY = r'E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe'

d = json.load(open(SRC, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

SCENE = ("The same young man, same face, same identity, same black shirt unbuttoned over a white t-shirt, "
         "seated at the same wooden table, same single bare bulb hanging above, same pure black void background, "
         "same black and white high-contrast cinematic look. ")
ONE_PERSON = ("ONLY ONE single person in the entire frame, a single young man, NO second person, NO duplicate, "
              "NO twin, NO mirror image, NO reflection, exactly one figure, one man only. ")
POS = (ONE_PERSON + SCENE +
    "A single young man seen from the SIDE in PROFILE, seated at the wooden table. "
    "The camera is positioned to the side of the table, so we see his face in a clean side profile (nose pointing to the side of the frame). "
    "Both of his hands are placed flat on the table surface in front of him. "
    "His body and shoulders stay seated at the table. "
    "Everything else remains EXACTLY the same as the reference - same face, same body, same table, same bulb, same void, same lighting. "
    "There is ONLY ONE man in this frame, seen from the side in profile. Do NOT show two men. Do NOT show three men. Do NOT show a front view.")
NEG = ("extra chair, wall, bright background, white background, color, multiple people, duplicate, "
       "two people, two men, three people, three men, second person, twin, mirror image, reflection of a person, "
       "different face, different person, tilted camera, dutch angle, objects on the table, clutter, grain, speckles, "
       "body turned, shoulders turned, front view, back view, two men side by side, facing each other")

seeds = [101, 202, 303]
pids = []
for s in seeds:
    dd = copy.deepcopy(d)
    nn = {n['id']: n for n in dd['nodes']}
    nn[72]['widgets_values'][0] = 'kf2_00004_ref.png'
    nn[82]['widgets_values'] = [1928, 1088, 1]
    nn[84]['widgets_values'][0] = POS
    nn[84]['widgets_values'][1] = 768
    nn[85]['widgets_values'][0] = NEG
    nn[85]['widgets_values'][1] = 768
    nn[29]['widgets_values'][0] = 'jaisal_cut/kf2_head90'
    nn[53]['widgets_values'][0] = s
    nn[79]['widgets_values'] = [4, 1, 'fit']
    for n in dd['nodes']:
        if n['type'] == 'Image Comparer (rgthree)':
            n['mode'] = 4
    out = os.path.join(WF_DIR, 'krea2_kf2_head90.json')
    json.dump(dd, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    import subprocess
    r = subprocess.run([PY, SUBMIT, out, '300'], capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if 'prompt_id' in l]
    print('seed', s, line[0] if line else r.stdout[-200:])
    time.sleep(2)
print('SUBMITTED all 3 seeds')
