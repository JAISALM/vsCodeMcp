import os

COMFY = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI'

def show(path, pat, before=200, after=1400, label=None):
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
    print(f'=== {label or pat!r} @ {os.path.basename(path)}:{line} ===')
    print(c[max(0, i-before):i+after])
    print('\n' + '='*70 + '\n')

# How is the unload_models flag consumed?
pq = os.path.join(COMFY, 'comfy', 'queue.py')
show(pq, 'unload_models', 400, 1200, 'queue.py unload_models consumption')
show(pq, 'def set_flag', 50, 500, 'queue.py set_flag')
show(pq, 'def get_flag', 50, 500, 'queue.py get_flag')
show(pq, 'def process', 50, 1600, 'queue.py process (worker loop)')

# Where is free_memory called from the queue?
show(pq, 'free_memory', 400, 800, 'queue.py free_memory call')
