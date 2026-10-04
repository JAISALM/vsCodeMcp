import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))

for n in d['nodes']:
    if n['id'] == 127:
        print("PROFILE (idx1):", n['widgets_values'][1])
        print("TRAJ (idx0):", n['widgets_values'][0])
        print("\nINSTRUCTION (idx3):\n", n['widgets_values'][3])
