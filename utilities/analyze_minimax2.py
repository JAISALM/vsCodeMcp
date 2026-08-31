import json

w = json.load(open(r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\mini-max-refrance-to-video-1.json', encoding='utf-8'))
nodes = {n['id']: n for n in w['nodes']}

print('=== LINKS (from -> to) ===')
for l in w['links']:
    lid, fn, fs, tn, ts, lt = l[0], l[1], l[2], l[3], l[4], (l[5] if len(l) > 5 else '?')
    ftype = nodes[fn]['type'] if fn in nodes else '?'
    ttype = nodes[tn]['type'] if tn in nodes else '?'
    print('link %s: %s(%s) -> %s(%s) slot %s [%s]' % (lid, fn, ftype, tn, ttype, ts, lt))

print()
print('=== What feeds key nodes ===')
for target in [46, 75, 37, 72, 74]:
    print('--- inputs to node %s (%s) ---' % (target, nodes[target]['type'] if target in nodes else '?'))
    for l in w['links']:
        if l[3] == target:
            fn = l[1]
            print('   from %s (%s) slot %s' % (fn, nodes[fn]['type'] if fn in nodes else '?', l[2]))

print()
print('=== MiniMaxH3ReferenceToVideo full widgets ===')
mm = nodes[75]
print(json.dumps(mm.get('widgets_values'), indent=2)[:2000])
