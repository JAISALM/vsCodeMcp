import json

d = json.load(open(r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_t2i_char2.json', encoding='utf-8-sig'))
for n in d['nodes']:
    if n['type'] == 'PixaromaPromptEach':
        rows = n['properties']['promptEachState']['rows']
        print('char2 has', len(rows), 'prompt rows')
        for i, r in enumerate(rows):
            print('--- row %d (enabled=%s) ---' % (i, r['enabled']))
            print(r['text'][:220])
        print()
        print('promptEachState keys:', list(n['properties']['promptEachState'].keys()))
        print('split/expand/trim/cap:', n['properties']['promptEachState'].get('split'), n['properties']['promptEachState'].get('expand'), n['properties']['promptEachState'].get('trim'), n['properties']['promptEachState'].get('cap'))
    if n['type'] == 'SaveImage':
        print('char2 SaveImage prefix:', n['widgets_values'])
    if n['type'] == 'KSampler':
        print('char2 KSampler widgets:', n['widgets_values'])
    if n['type'] == 'EmptySD3LatentImage':
        print('char2 latent widgets:', n['widgets_values'])
    if n['type'] == 'LoraLoaderModelOnly':
        print('char2 LoRA', n['id'], n['widgets_values'])
