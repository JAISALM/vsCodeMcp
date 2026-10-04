import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headturn_3ref.json'
d = json.load(io.open(WF, encoding='utf-8'))

print("=== TOP-LEVEL NODES ===")
for n in d['nodes']:
    t = n['type']
    if t in ('MiniMaxH3ReferenceToVideo', 'PrimitiveStringMultiline', 'LoadImage', 'SaveVideo', 'ResolutionSelector'):
        wv = n.get('widgets_values')
        s = str(wv)
        if len(s) > 300:
            s = s[:300] + " ...[+%d]" % (len(str(wv)) - 300)
        print("\n--- node", n['id'], t, "---")
        print("  widgets:", s)
        for inp in n.get('inputs', []):
            print("  IN:", inp.get('name'), "link=", inp.get('link'))
