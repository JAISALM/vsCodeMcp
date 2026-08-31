import json

src = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\mini-max-refrance-to-video-1.json'
dst = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\mini-max-jaisal-test.json'

w = json.load(open(src, encoding='utf-8'))

PROMPT = (
    "Cinematic aerial drone shot over a Kerala backwater river, an angular 3d art style with brush stroke color texture. "
    "A single young Indian schoolboy, around ten years old, in a neat school uniform with a red school bag, drenched and wet from the rain, "
    "stands in the center of a single long traditional stone bridge over a single wide river. "
    "The camera starts at a medium high angle above the boy, who looks up at the camera. "
    "Then the camera rises smoothly and continuously straight upward, like a drone ascending, "
    "gradually revealing the full length of the bridge, the wide river on both sides, and the surrounding environment. "
    "The boy becomes smaller and smaller until he is a tiny dot in the center of the bridge. "
    "Water droplets fall from the boy. Moody overcast sky. "
    "ONE single smooth continuous upward camera movement, no panning sideways, no camera tilt, no cuts, no new characters appearing, exactly one boy the entire time. "
    "The same angular 3d brush-stroke artstyle throughout."
)

for n in w['nodes']:
    if n['id'] == 76:
        n['widgets_values'] = ['jaisal_mm_start.png', 'image']
    elif n['id'] == 97:
        n['widgets_values'] = ['jaisal_mm_final.png', 'image']
    elif n['id'] == 75:
        wv = list(n['widgets_values'])
        wv[0] = PROMPT
        n['widgets_values'] = wv

json.dump(w, open(dst, 'w', encoding='utf-8'), indent=1)
print('written:', dst)

# verify
w2 = json.load(open(dst, encoding='utf-8'))
for n in w2['nodes']:
    if n['id'] in (75, 76, 97):
        print('id=%s type=%s widgets=%s' % (n['id'], n['type'], str(n.get('widgets_values'))[:100]))
