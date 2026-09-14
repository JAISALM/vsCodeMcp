import json
path = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2T2iI2iInpaint2pass_v15.json'
d = json.load(open(path, encoding='utf-8'))
print("=== NODES ===")
for n in d['nodes']:
    print(f"  {n['id']:>4} {n['type']:<32} widgets={n.get('widgets_values')}")
print("=== LINKS ===")
for l in d['links']:
    if isinstance(l, dict):
        print(f"  {l['id']:>4}: {l['origin_id']} -> {l['target_id']}  to_slot={l['to_slot']}")
    else:
        print(f"  {l[0]:>4}: {l[1]} -> {l[3]}  to_slot={l[4]}  type={l[5] if len(l)>5 else '?'}")
