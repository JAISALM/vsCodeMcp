import json, shutil

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_inpaint_kf2_chair.json'
DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_inpaint_small_mic.json'

# Clone the PROVEN Krea2 inpaint workflow (differential diffusion + LanPaint + composite-back)
shutil.copyfile(SRC, DST)
wf = json.load(open(DST, encoding='utf-8'))

# Node 411 is the POSITIVE prompt (node 414 = ConditioningZeroOut = negative is zeroed).
# The SAM3 mask is the TALL big-mic silhouette, so the prompt must say the TOP of that
# region becomes black void (where the tall head used to be) and a SMALL mic sits LOW.
MIC_PROMPT = (
    "A SMALL compact studio microphone on a SHORT LOW stand, sitting low on the wooden "
    "table. The microphone head is small (like a compact studio mic), NOT a large "
    "broadcast mic. The area above the small microphone is pure black void background. "
    "Black-and-white high-contrast cinematic style, fine film grain, matching the "
    "surrounding scene exactly."
)

for n in wf['nodes']:
    if n['id'] == 200:  # LoadImage -> the mic+paper image
        n['widgets_values'] = ['mic+paper.png', 'image']
        if 'widgets_values_named' in n:
            n['widgets_values_named'] = {'image': 'mic+paper.png'}
    elif n['id'] == 454:  # SAM3Segment -> segment the microphone (not the chair)
        n['widgets_values'] = ['microphone', 'sam3', 'Auto', 0.5, 0, 0, False, False, 'Alpha', '#222222']
    elif n['id'] == 411:  # CLIPTextEncode -> the mic edit prompt (set BOTH positional + named)
        n['widgets_values'] = [MIC_PROMPT]
        if 'widgets_values_named' in n:
            n['widgets_values_named'] = {'text': MIC_PROMPT}
    elif n['id'] == 500:  # SaveImage -> output name
        n['widgets_values'] = ['jaisal_cut/mic_small']

json.dump(wf, open(DST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written:', DST)
print('changed: node 200 (LoadImage=mic+paper.png), 454 (SAM3=microphone), 411 (prompt), 500 (save)')
