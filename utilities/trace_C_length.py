import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))
sub = d['definitions']['subgraphs'][0]

print("=== SUBGRAPH INPUTS (instance slot -> internal -10 slot) ===")
for inp in sub.get('inputs', []):
    print("  ", inp)

print("\n=== SUBGRAPH OUTPUTS ===")
for out in sub.get('outputs', []):
    print("  ", out)

print("\n=== VIDEO NODE 201 (MiniMaxH3ImageToVideo) ===")
for n in sub['nodes']:
    if n['id'] == 201:
        print("widgets:", n.get('widgets_values'))
        for i, inp in enumerate(n.get('inputs', [])):
            print("  input slot", i, "name", inp.get('name'), "type", inp.get('type'), "link", inp.get('link'))

print("\n=== LINKS feeding -10 slot 12 (video length source) ===")
for l in sub['links']:
    if l['target_id'] == 201 and l['target_slot'] == 7:
        print("  video length <- origin", l['origin_id'], "slot", l['origin_slot'], "type", l['type'])

print("\n=== What is -10 slot 12? (subgraph input mapping) ===")
# find which instance slot maps to -10 slot 12
for inp in sub.get('inputs', []):
    # inputs may be dicts with 'id' (instance slot) and 'name'
    print("  input entry:", inp)
