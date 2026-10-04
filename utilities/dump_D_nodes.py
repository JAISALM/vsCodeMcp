import json
wf = json.load(open(r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_D_reverse.json', encoding='utf-8'))
for n in wf['nodes']:
    wv = n.get('widgets_values', [])
    print(f"{n['id']} | {n['type']} | {str(wv)[:150]}")
