import json, copy

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\Krea2_LanPaint_Inpaint_v1.json'
DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_inpaint_kf2_chair.json'

d = json.load(open(SRC, encoding='utf-8'))

def find(nid):
    for n in d['nodes']:
        if n['id'] == nid:
            return n
    return None

# 1) LoadImage (200) -> kf2
n200 = find(200)
n200['widgets_values'] = ['kf2_seated_v7.png', 'image']
if 'widgets_values_named' in n200:
    n200['widgets_values_named'] = {'image': 'kf2_seated_v7.png'}

# 2) SAM3Segment (454) -> segment the wooden chair
n454 = find(454)
w = list(n454['widgets_values'])
w[0] = 'wooden chair'          # prompt
n454['widgets_values'] = w
# keep model 'sam3' (index1), rest as-is

# 3) CLIPTextEncode (411) -> fill the masked region with the dark void
n411 = find(411)
n411['widgets_values'] = ['empty dark black void background, plain dark space, no objects, no furniture, no chair, no people, pure black background']

# 4) Add a SaveImage node (500) fed by the composite (487)
if find(500) is None:
    d['nodes'].append({
        "id": 500, "type": "SaveImage", "pos": [1400, 200], "size": [300, 200],
        "flags": {}, "order": 40, "mode": 0,
        "inputs": [{"localized_name": "images", "name": "images", "type": "IMAGE", "link": 900}],
        "outputs": [],
        "properties": {"Node name for S&R": "SaveImage"},
        "widgets_values": ["jaisal_kf2_inpaint"]
    })
    # link 487 -> 500
    if not any((l[0] == 900) for l in d['links']):
        d['links'].append([900, 487, 0, 500, 0, "IMAGE"])
    d['last_link_id'] = max(d.get('last_link_id', 0), 900)
    d['last_node_id'] = max(d.get('last_node_id', 0), 500)

json.dump(d, open(DST, 'w', encoding='utf-8'), ensure_ascii=False)
print("WROTE", DST)
print("node200:", find(200)['widgets_values'])
print("node454:", find(454)['widgets_values'])
print("node411:", find(411)['widgets_values'])
print("node500:", find(500)['widgets_values'] if find(500) else "MISSING")
