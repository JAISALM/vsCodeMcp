import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))

print("=== NODES (camera / prompt / video / save) ===")
for n in d['nodes']:
    if n['type'] in ('H3LocalCameraEditor', 'PrimitiveStringMultiline', 'MiniMaxH3ReferenceToVideo', 'SaveVideo', 'LoadImage'):
        print("\n--- node", n['id'], n['type'], "---")
        wv = n.get('widgets_values')
        if isinstance(wv, list):
            for i, v in enumerate(wv):
                s = str(v)
                if len(s) > 400:
                    s = s[:400] + " ...[+%d]" % (len(str(v)) - 400)
                print("  [%d] %s" % (i, s))
        # inputs
        for inp in n.get('inputs', []):
            print("  IN:", inp.get('name'), "link=", inp.get('link'))

print("\n=== LINKS (to camera node 127 / prompt / video) ===")
for l in d.get('links', []):
    print("link", l[0], "from node", l[1], "slot", l[2], "-> to node", l[3], "slot", l[4], "type", l[5] if len(l) > 5 else '?')
