import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))

subs = d.get('definitions', {}).get('subgraphs', [])
print("num subgraphs:", len(subs))
for si, sub in enumerate(subs):
    print("\n=== SUBGRAPH", si, "===")
    print("internal nodes:")
    for n in sub.get('nodes', []):
        print("  ", n['id'], n['type'], "widgets:", (str(n.get('widgets_values'))[:80] if n.get('widgets_values') is not None else None))
    print("internal links:")
    for l in sub.get('links', []):
        print("   link", l[0], "from", l[1], "slot", l[2], "-> to", l[3], "slot", l[4], "type", l[5] if len(l) > 5 else '?')
