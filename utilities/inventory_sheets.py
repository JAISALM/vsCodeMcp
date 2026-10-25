#!/usr/bin/env python
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f'{path}[{i}]')
    elif isinstance(o,str):
        if 'JAISAL' in o or 'royal blue' in o.lower() or 'ZIDANE' in o or 'dark green' in o.lower():
            yield path, o[:90].replace('\n',' | ')
FILES = [
 r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json',
 r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\LEEBLAAB-QwenImage21-Character-SHEET - jaisal.json',
 r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\LEEBLAAB-QwenImage21-Character-SHEET - zidane.json',
]
out = io.StringIO()
for P in FILES:
    out.write('===== ' + P.split('\\')[-1] + '\n')
    j = json.load(open(P, encoding='utf-8'))
    for n in j['nodes']:
        wv = n.get('widgets_values')
        wvs = json.dumps(wv, ensure_ascii=False)[:80] if wv is not None else '-'
        out.write('  id=%-4s %-28s %s\n' % (n['id'], n['type'][:28], wvs))
    hits = list(walk(j))
    out.write('NAME/COLOR hits: %d\n' % len(hits))
    for p, s in hits:
        out.write('   %s :: %s\n' % (p, s))
    out.write('subgraphs: %d\n' % len(j.get('definitions', {}).get('subgraphs', [])))
open(r'D:\models\vsCodeMcp\data\09j_invent.txt', 'w', encoding='utf-8').write(out.getvalue())
print('ok', len(out.getvalue()))
