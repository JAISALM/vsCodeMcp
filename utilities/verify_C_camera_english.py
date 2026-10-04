import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))

for n in d['nodes']:
    if n['id'] == 215:
        print("REF (node 215):", n['widgets_values'][0])
    if n['id'] == 127:
        print("\nTRAJECTORY:", n['widgets_values'][0])
        print("PROFILE:", n['widgets_values'][1])
        print("ORBIT_DIR:", n['widgets_values'][13] if len(n['widgets_values']) > 13 else '?')
        print("\nINSTRUCTION:\n", n['widgets_values'][3])
        # checks
        ins = n['widgets_values'][3]
        print("\n--- CHECKS ---")
        print("head turns LEFT:", 'to the LEFT' in ins)
        print("English dialogue:", '[English]' in ins)
        print("lip movement:", 'LIP MOVEMENT' in ins or 'lips move' in ins)
        print("NO music:", 'NO music' in ins)
        print("back to camera:", 'back to the camera' in ins)
