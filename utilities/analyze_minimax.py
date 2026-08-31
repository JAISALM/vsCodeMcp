import json
from collections import Counter

w = json.load(open(r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\mini-max-refrance-to-video-1.json', encoding='utf-8'))
types = Counter(n['type'] for n in w['nodes'])
print('=== NODE TYPES ===')
for t, c in types.most_common():
    print('%3d  %s' % (c, t))
print()
print('=== KEY NODES (widgets) ===')
for n in w['nodes']:
    t = n['type']
    if any(k in t.lower() for k in ['loadimage', 'prompt', 'text', 'video', 'save', 'preview', 'ref', 'minimax', 'krea', 'sampler', 'latent', 'empty', 'image']):
        wv = n.get('widgets_values')
        print('id=%s type=%s' % (n['id'], t))
        print('   widgets=%s' % str(wv)[:200])
print()
print('=== LINKS INTO/OUT OF key nodes ===')
# find LoadImage nodes and what they connect to
for n in w['nodes']:
    if n['type'] == 'LoadImage':
        print('LoadImage id=%s image=%s' % (n['id'], n.get('widgets_values')))
        for out in n.get('outputs', []):
            for link_id in (out.get('links') or []):
                for l in w['links']:
                    if l['id'] == link_id:
                        tgt = next((x for x in w['nodes'] if x['id'] == l['to']), None)
                        print('   -> link %s to node id=%s type=%s slot=%s' % (link_id, l['to'], tgt['type'] if tgt else '?', l['slot']))
