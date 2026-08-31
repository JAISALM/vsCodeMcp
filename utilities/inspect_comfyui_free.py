import os

COMFY = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI'

def show(path, pat, before=300, after=1400):
    if not os.path.exists(path):
        print(f'FILE NOT FOUND: {path}')
        return
    with open(path, encoding='utf-8', errors='replace') as f:
        c = f.read()
    i = c.find(pat)
    if i == -1:
        print(f'NOT FOUND: {pat!r} in {os.path.basename(path)}')
        return
    line = c[:i].count('\n') + 1
    print(f'=== {pat!r} @ {os.path.basename(path)}:{line} ===')
    print(c[max(0, i-before):i+after])
    print('\n' + '='*70 + '\n')

print('########## /free endpoint (top-level py) ##########')
for fn in sorted(os.listdir(COMFY)):
    if fn.endswith('.py'):
        p = os.path.join(COMFY, fn)
        try:
            with open(p, encoding='utf-8', errors='replace') as f:
                c = f.read()
        except Exception:
            continue
        if '/free' in c:
            show(p, '/free', 500, 1600)

print('########## model_management.py ##########')
mm = os.path.join(COMFY, 'comfy', 'model_management.py')
show(mm, 'def unload_all_models', 50, 1700)
show(mm, 'def free_memory', 50, 1700)
show(mm, 'lowvram', 300, 1000)
