import json

p = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\minimax_h3_sam_r2v_2char_cinematic.json'
wf = json.load(open(p, encoding='utf-8'))
nodes = {n['id']: n for n in wf['nodes']}
lk = {l[0]: l for l in wf['links']}

print('--- R2V node 136 inputs -> source nodes ---')
n136 = nodes[136]
for i in n136.get('inputs', []):
    if i.get('link') is not None:
        t = lk[i['link']]
        print('  input %-28s <- node %s (%s)' % (i['name'], t[1], nodes[t[1]]['type']))

print()
print('--- node 247 (SAM3 image source) ---')
print('type:', nodes[247]['type'])
print('widgets:', json.dumps(nodes[247].get('widgets_values'))[:400])
for i in nodes[247].get('inputs', []):
    if i.get('link') is not None:
        t = lk[i['link']]
        print('  input %s <- node %s (%s)' % (i['name'], t[1], nodes[t[1]]['type']))
print('outputs ->')
for o in nodes[247].get('outputs', []):
    for lid in (o.get('links') or []):
        t = lk[lid]
        print('  -> node %s (%s) slot %s' % (t[3], nodes[t[3]]['type'], t[4]))

print()
print('--- SAM3 290/291 outputs -> ---')
for nid in (290, 291):
    for o in nodes[nid].get('outputs', []):
        for lid in (o.get('links') or []):
            t = lk[lid]
            print('SAM3 %s -> node %s (%s) slot %s' % (nid, t[3], nodes[t[3]]['type'], t[4]))

print()
print('--- composite/resize chain toward R2V refs ---')
for n in wf['nodes']:
    if n['type'] in ('ImageCompositeMasked', 'ImageResizeKJv2', 'ImageAddNoise', 'ImageConcatMulti', 'ImageBlend', 'ImageCropMask'):
        for o in n.get('outputs', []):
            for lid in (o.get('links') or []):
                t = lk[lid]
                print('%s %s -> node %s (%s) slot %s' % (n['type'], n['id'], t[3], nodes[t[3]]['type'], t[4]))

print()
print('--- SetNode widgets (value overrides) ---')
for n in wf['nodes']:
    if n['type'] == 'SetNode':
        print('node %s: %s' % (n['id'], json.dumps(n.get('widgets_values'))[:250]))

print()
print('--- GetNode widgets ---')
for n in wf['nodes']:
    if n['type'] == 'GetNode':
        print('node %s: %s' % (n['id'], json.dumps(n.get('widgets_values'))[:250]))
