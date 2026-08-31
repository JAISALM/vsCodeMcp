import json

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json'
d = json.load(open(WF, encoding='utf-8'))
nodes = {n['id']: n for n in d['nodes']}

n115 = nodes[115]
print('ResolutionSelector before:', n115.get('widgets_values'))
# 1.0 MP @ 16:9 = 1344x768 (MiniMax H3 native canvas)
n115['widgets_values'] = ['16:9 (Widescreen)', 1.0, 32]
if 'widgets_values_named' in n115:
    n115['widgets_values_named'] = {'aspect_ratio': '16:9 (Widescreen)', 'megapixels': 1.0, 'multiple': 32}
print('ResolutionSelector after:', n115.get('widgets_values'))

json.dump(d, open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Set ResolutionSelector to 1.0 MP (1344x768 native). Reference video node 149 left wired.')
