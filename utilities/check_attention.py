import os

base = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI'
targets = [
    'use-pytorch-cross-attention',
    'use_pytorch_cross_attention',
    'cache-none',
    'cache_none',
    'use-split-cross-attention',
    'use_split_cross_attention',
    'disable-pinned-memory',
    'disable_pinned_memory',
    'attention_mode',
    'pytorch_attention',
    'sageattention',
    'sdpa',
]
hits = {t: [] for t in targets}
for dp, dn, fn in os.walk(base):
    if any(s in dp for s in ['node_modules', '.git', 'custom_nodes', 'models', 'venv', 'python_embeded']):
        continue
    for f in fn:
        if f.endswith('.py'):
            p = os.path.join(dp, f)
            try:
                with open(p, encoding='utf-8', errors='ignore') as fh:
                    for i, line in enumerate(fh, 1):
                        for t in targets:
                            if t in line:
                                hits[t].append((os.path.relpath(p, base), i, line.strip()[:130]))
            except Exception:
                pass
for t in targets:
    print('===', t, '(', len(hits[t]), 'hits) ===')
    for h in hits[t][:12]:
        print('  ', h[0], ':', h[1], '|', h[2])
    print()
