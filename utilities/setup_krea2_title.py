import json, shutil, os

# 1. Copy FINAL_TITLE_REFERENCE.png to input\
src = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut\FINAL_TITLE_REFERENCE.png'
dst = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\FINAL_TITLE_REFERENCE.png'
shutil.copy2(src, dst)
print('Copied FINAL_TITLE_REFERENCE.png to input\\')
print('  exists:', os.path.exists(dst), f'({os.path.getsize(dst)} bytes)')

# 2. Update the identity-edit workflow
wf = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json'
d = json.load(open(wf, encoding='utf-8'))

# Node 72 (LoadImage) -> point at FINAL_TITLE_REFERENCE.png
n72 = [n for n in d['nodes'] if n['id'] == 72][0]
n72['widgets_values'][0] = 'FINAL_TITLE_REFERENCE.png'
if 'widgets_values_named' in n72:
    n72['widgets_values_named']['image'] = 'FINAL_TITLE_REFERENCE.png'
print('Node 72 (LoadImage) ->', n72['widgets_values'][0])

# Node 84 (positive instruction) -> title instruction
n84 = [n for n in d['nodes'] if n['id'] == 84][0]
title_instruction = open(r'd:\models\vsCodeMcp\prompts\jaisal_title_instruction.txt', encoding='utf-8').read().strip()
n84['widgets_values'][0] = title_instruction
if 'widgets_values_named' in n84:
    # find the instruction key
    for k in n84['widgets_values_named']:
        if 'instruction' in k.lower() or 'prompt' in k.lower() or 'text' in k.lower():
            n84['widgets_values_named'][k] = title_instruction
print('Node 84 (positive instruction) set, length:', len(title_instruction))

# Node 85 (negative instruction) -> title-specific negative
n85 = [n for n in d['nodes'] if n['id'] == 85][0]
title_negative = ("stick figure, person, character, figure, human, kid, face, body, "
                  "filled letters, solid letters, colored letters, garbled text, "
                  "misspelled text, unreadable text, distorted letters, "
                  "multiple titles, duplicate title, extra text, watermark, logo")
n85['widgets_values'][0] = title_negative
if 'widgets_values_named' in n85:
    for k in n85['widgets_values_named']:
        if 'instruction' in k.lower() or 'prompt' in k.lower() or 'text' in k.lower():
            n85['widgets_values_named'][k] = title_negative
print('Node 85 (negative instruction) set')

# Node 29 (SaveImage) -> prefix for the title output
n29 = [n for n in d['nodes'] if n['id'] == 29][0]
n29['widgets_values'][0] = 'jaisal_cut/title_final'
if 'widgets_values_named' in n29:
    for k in n29['widgets_values_named']:
        if 'prefix' in k.lower() or 'filename' in k.lower():
            n29['widgets_values_named'][k] = 'jaisal_cut/title_final'
print('Node 29 (SaveImage) prefix ->', n29['widgets_values'][0])

json.dump(d, open(wf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('Workflow saved.')
