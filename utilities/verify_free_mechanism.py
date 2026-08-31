import os, re

COMFY = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI'

def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()

def section(path, start_pat, end_pat=None, maxchars=3000):
    c = read(path)
    i = c.find(start_pat)
    if i == -1:
        print(f'NOT FOUND: {start_pat!r} in {os.path.basename(path)}')
        return
    line = c[:i].count('\n') + 1
    j = c.find(end_pat, i) if end_pat else i + maxchars
    if j == -1:
        j = i + maxchars
    print(f'===== {os.path.basename(path)}:{line} ({start_pat!r}) =====')
    print(c[i:j][:maxchars])
    print('\n' + '='*70 + '\n')

# 1. PromptQueue.get — timeout units + idle behavior
section(os.path.join(COMFY, 'execution.py'), 'class PromptQueue', 'class ', 4000)

# 2. model_unload — does it release CPU RAM?
mm = os.path.join(COMFY, 'comfy', 'model_management.py')
c = read(mm)
i = c.find('def model_unload')
if i != -1:
    line = c[:i].count('\n') + 1
    print(f'===== model_management.py:{line} (def model_unload) =====')
    print(c[i:i+2500])
    print('\n' + '='*70 + '\n')
else:
    print('model_unload NOT FOUND as a def; searching for the method...')
    for m in re.finditer(r'def \w*unload\w*', c):
        print('  found:', m.group(0), 'at line', c[:m.start()].count('\n')+1)
