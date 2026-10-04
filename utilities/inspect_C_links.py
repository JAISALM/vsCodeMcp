import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))
sub = d['definitions']['subgraphs'][0]

print("=== SUBGRAPH LINKS (dict form) ===")
for l in sub.get('links', []):
    print(l)

print("\n=== NODE 136 (sage patch) inputs/outputs ===")
for n in sub['nodes']:
    if n['id'] == 136:
        print("inputs:", n.get('inputs'))
        print("outputs:", n.get('outputs'))

print("\n=== NODE 138 (H3SLAAttention) inputs/outputs ===")
for n in sub['nodes']:
    if n['id'] == 138:
        print("inputs:", n.get('inputs'))
        print("outputs:", n.get('outputs'))

print("\n=== NODE 121 (LoraLoader) inputs/outputs ===")
for n in sub['nodes']:
    if n['id'] == 121:
        print("inputs:", n.get('inputs'))
        print("outputs:", n.get('outputs'))
