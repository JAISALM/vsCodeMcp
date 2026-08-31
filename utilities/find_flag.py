import os
COMFY = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI'
targets = ['unload_models', 'set_flag', 'get_flag', 'free_memory(', 'class PromptQueue', 'def process']
hits = {}
for dp, dn, fn in os.walk(COMFY):
    if 'site-packages' in dp or 'node_modules' in dp or 'web' in dp:
        continue
    for f in fn:
        if not f.endswith('.py'):
            continue
        p = os.path.join(dp, f)
        try:
            with open(p, encoding='utf-8', errors='replace') as fh:
                lines = fh.readlines()
        except Exception:
            continue
        for idx, line in enumerate(lines):
            for t in targets:
                if t in line:
                    hits.setdefault(t, []).append((p, idx+1, line.strip()[:120]))
for t in targets:
    print(f'===== {t} =====')
    for p, ln, txt in hits.get(t, [])[:12]:
        print(f'  {os.path.relpath(p, COMFY)}:{ln}: {txt}')
    print()
