import json, io

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
d = json.load(io.open(WF, encoding='utf-8'))

print("=== ALL NODES (id, type) ===")
for n in d['nodes']:
    print(n['id'], n['type'])

print("\n=== MODEL CHAIN (nodes feeding the video node) ===")
# find the video node
video_id = None
for n in d['nodes']:
    if n['type'] in ('MiniMaxH3ReferenceToVideo', 'CreateVideo', 'MiniMaxH3Video'):
        video_id = n['id']
        print("VIDEO NODE:", n['id'], n['type'])

# find KJNodes sage patch node
print("\n=== SAGE / SLA / model nodes ===")
for n in d['nodes']:
    if 'Sage' in n['type'] or 'SLA' in n['type'] or 'Attention' in n['type'] or 'UNET' in n['type'] or 'Lora' in n['type'] or 'Guider' in n['type'] or 'Sampler' in n['type']:
        print(n['id'], n['type'], "widgets:", n.get('widgets_values'))

print("\n=== LINKS involving model-type nodes ===")
for l in d.get('links', []):
    print("link", l[0], "from", l[1], "slot", l[2], "-> to", l[3], "slot", l[4], "type", l[5] if len(l) > 5 else '?')
