import json, shutil

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json'
DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit_small_mic.json'

shutil.copyfile(SRC, DST)
wf = json.load(open(DST, encoding='utf-8'))

POS = (
    "Make the microphone SMALL and COMPACT, on a SHORT LOW stand, sitting low on the "
    "table. ONLY ONE microphone in the image. Its top stays well below the height of "
    "a tall broadcast mic. Keep EVERYTHING ELSE exactly the same: the loose sheets of "
    "paper floating in the air, the wooden table, the empty wooden chair, the single "
    "bare bulb hanging above, the pure black void background, and the black-and-white "
    "high-contrast cinematic style with fine film grain. Preserve the entire original "
    "image exactly. No other changes. No people."
)
NEG = (
    "large microphone, big microphone, tall microphone stand, broadcast microphone, "
    "two microphones, multiple microphones, duplicate mic, extra mic, color, any "
    "color, people, a person, a boy, extra objects, text, watermark, glowing "
    "effects, holograms, fire, smoke"
)

for n in wf['nodes']:
    if n['id'] == 72:   # LoadImage -> the base scene
        n['widgets_values'] = ['mic+paper.png', 'image']
    elif n['id'] == 84:  # positive instruction
        n['widgets_values'] = [POS, 768, '']
    elif n['id'] == 85:  # negative
        n['widgets_values'] = [NEG, 768, '']
    elif n['id'] == 29:  # SaveImage
        n['widgets_values'] = ['jaisal_cut/mic_small_id']
    elif n['id'] == 95:  # Typnosis typography LoRA -> bypass (not needed for mic edit)
        n['mode'] = 4

json.dump(wf, open(DST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written:', DST)
print('changed: 72 (LoadImage=mic+paper.png), 84 (instruction), 85 (negative), 29 (save), 95 (Typnosis bypassed)')
print('kept: 79 ref_boost=4 fit, 83 16:9 2MP, 53 10 steps cfg 1 denoise 1, 71 identity LoRA v1.2 @1.0')
