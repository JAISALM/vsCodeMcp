import json, shutil, os

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json'
SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\video\Jaisal_Production_1_00011_.mp4'
DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\jaisal_prod1_ref.mp4'

# 1) Copy the good output video into the input dir (where the loader node scans)
shutil.copyfile(SRC, DST)
print('Copied', os.path.basename(SRC), '->', os.path.basename(DST))

d = json.load(open(WF, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

# 2) Pick new unique ids
max_node_id = max(n['id'] for n in d['nodes'])
max_link_id = max(l[0] for l in d['links'])
new_node_id = max_node_id + 1
new_link_img = max_link_id + 1
new_link_aud = max_link_id + 2
print('new_node_id', new_node_id, 'new_link_img', new_link_img, 'new_link_aud', new_link_aud)

# 3) Find node 136 input indices for ref_videos.ref_video_0 and ref_video_audios.ref_video_audio_0
n136 = nodes[136]
idx_refvideo = None
idx_refvideo_audio = None
for i, inp in enumerate(n136['inputs']):
    if inp.get('name') == 'ref_videos.ref_video_0':
        idx_refvideo = i
    if inp.get('name') == 'ref_video_audios.ref_video_audio_0':
        idx_refvideo_audio = i
print('idx_refvideo', idx_refvideo, 'idx_refvideo_audio', idx_refvideo_audio)
assert idx_refvideo is not None and idx_refvideo_audio is not None

# 4) Create the MiniMaxH3ReferenceVideoLoadStar7 node
#    outputs: [IMAGE, AUDIO, INT, STRING] -> slot 0 = IMAGE, slot 1 = AUDIO
#    widgets: [video, max_long_edge, allow_upscale]
pos136 = n136.get('pos', [0, 0])
new_node = {
    "id": new_node_id,
    "type": "MiniMaxH3ReferenceVideoLoadStar7",
    "pos": [pos136[0] - 420, pos136[1] + 40],
    "size": [320, 120],
    "flags": {},
    "order": 0,
    "mode": 0,
    "inputs": [],
    "outputs": [
        {"localized_name": "IMAGE", "name": "IMAGE", "type": "IMAGE", "links": [new_link_img]},
        {"localized_name": "AUDIO", "name": "AUDIO", "type": "AUDIO", "links": [new_link_aud]},
        {"localized_name": "INT", "name": "INT", "type": "INT", "links": []},
        {"localized_name": "STRING", "name": "STRING", "type": "STRING", "links": []},
    ],
    "title": "RefVideo (motion anchor)",
    "properties": {"Node name for S&R": "MiniMaxH3ReferenceVideoLoadStar7"},
    "widgets_values": ["jaisal_prod1_ref.mp4", 1344, False],
}
d['nodes'].append(new_node)

# 5) Add the two links: [id, from_node, from_slot, to_node, to_slot, type]
d['links'].append([new_link_img, new_node_id, 0, 136, idx_refvideo, 'IMAGE'])
d['links'].append([new_link_aud, new_node_id, 1, 136, idx_refvideo_audio, 'AUDIO'])

# 6) Set node 136 input link fields
n136['inputs'][idx_refvideo]['link'] = new_link_img
n136['inputs'][idx_refvideo_audio]['link'] = new_link_aud

# 7) Set ResolutionSelector (node 115) to 2K: ['16:9 (Widescreen)', 2.4 MP, 32] -> ~2048x1152
n115 = nodes[115]
print('ResolutionSelector before:', n115.get('widgets_values'))
n115['widgets_values'] = ['16:9 (Widescreen)', 2.4, 32]
if 'widgets_values_named' in n115:
    n115['widgets_values_named'] = {'aspect_ratio': '16:9 (Widescreen)', 'megapixels': 2.4, 'multiple': 32}
print('ResolutionSelector after:', n115.get('widgets_values'))

json.dump(d, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Saved. Added node', new_node_id, '(MiniMaxH3ReferenceVideoLoadStar7) -> ref_videos.ref_video_0 + ref_video_audios.ref_video_audio_0')
print('Resolution set to 2K (2.4 MP @ 16:9 ~ 2048x1152)')
