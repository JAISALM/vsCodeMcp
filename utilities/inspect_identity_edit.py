import json

wf = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json'
d = json.load(open(wf, encoding='utf-8'))

print('=== TOP-LEVEL NODES ===')
for n in d['nodes']:
    wv = n.get('widgets_values', [])
    # show a short preview of widgets
    preview = []
    for v in wv:
        s = str(v)
        if len(s) > 50:
            s = s[:50] + '...'
        preview.append(s)
    print(f"  id={n['id']} type={n['type']}")
    if preview:
        print(f"      widgets: {preview}")

print()
print('=== LINKS ===')
for l in d.get('links', []):
    ltype = l[5] if len(l) > 5 else ''
    print(f"  {l[1]}.{l[2]} -> {l[3]}.{l[4]}  ({ltype})")
