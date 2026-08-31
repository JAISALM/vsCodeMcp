import os, json
wf = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'
cands = ['jaisal_shot2_i2i.json','jaisal_shot3_i2i.json','krea2_jaisal_medium.json',
         'krea2_jaisal_continuity.json','krea2_jaisal_face.json','krea2_jaisal_face_v2.json',
         'krea2_jaisal_face_v3.json','krea2_jaisal_title_moody.json','krea2_jaisal_base.json',
         'krea2_jaisal_refs.json','krea2_jaisal_fix05_inpaint.json','krea2_jaisal_fix05_tie.json']
for f in cands:
    p = os.path.join(wf, f)
    if not os.path.exists(p):
        print('===', f, '=== (missing)')
        continue
    d = json.load(open(p, encoding='utf-8', errors='ignore'))
    unet = [n.get('widgets_values') for n in d['nodes'] if n['type'] == 'UNETLoader']
    lora = [n.get('widgets_values') for n in d['nodes'] if 'Lora' in n['type']]
    loadimg = [n.get('widgets_values') for n in d['nodes'] if n['type'] == 'LoadImage']
    ks = [n.get('widgets_values') for n in d['nodes'] if n['type'] == 'KSampler']
    print('===', f, '===')
    print('  UNET:', unet)
    print('  LoRA:', lora)
    print('  LoadImage:', loadimg)
    print('  KSampler:', ks)
    print()
