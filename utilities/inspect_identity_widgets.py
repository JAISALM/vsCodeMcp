import json
d = json.load(open(r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_identity_edit.json', encoding='utf-8'))
for nid in (72, 84, 85, 29):
    n = [x for x in d['nodes'] if x['id'] == nid][0]
    print(f'=== node {nid} ({n["type"]}) ===')
    print('  widgets_values:', n['widgets_values'])
    if 'widgets_values_named' in n:
        print('  widgets_values_named keys:', list(n['widgets_values_named'].keys()))
        for k, v in n['widgets_values_named'].items():
            s = str(v)
            print(f'    {k} = {s[:60]!r}')
    print()
