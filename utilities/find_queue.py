import os
COMFY = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI'
for dp, dn, fn in os.walk(COMFY):
    if 'site-packages' in dp or 'node_modules' in dp:
        continue
    for f in fn:
        if 'queue' in f.lower() and f.endswith('.py'):
            print(os.path.join(dp, f))
