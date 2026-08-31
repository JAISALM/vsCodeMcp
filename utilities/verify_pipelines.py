import json
WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'
for f in ('jaisalproduction1.json', 'jaisalproduction2.json'):
    d = json.load(open(WF + '\\' + f, encoding='utf-8'))
    nodes = {n['id']: n for n in d['nodes']}
    print('===', f, '===')
    print('  length (node 132):', nodes[132]['widgets_values'])
    print('  save prefix (node 92):', nodes[92]['widgets_values'][0])
    print('  LoadImages:', [(n['id'], n['widgets_values'][0]) for n in d['nodes'] if n['type'] == 'LoadImage'])
    print('  ref links:', [l for l in d['links'] if l[0] in (300, 301, 302)])
    print('  prompt starts:', nodes[138]['widgets_values'][0][:80].replace('\n', ' '))
    print()
