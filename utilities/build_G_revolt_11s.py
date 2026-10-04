import json, io, copy

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_papers.json'
OUT = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json'
PROMPT = r'd:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G_revolt_11s.txt'

src = json.load(open(SRC, encoding='utf-8'))
prompt = io.open(PROMPT, encoding='utf-8').read().strip()

def find(wf, nid):
    for n in wf['nodes']:
        if n['id'] == nid:
            return n
    return None

g = copy.deepcopy(src)

# length 360 (15s) -> 264 (11s @ 24fps)
h3 = find(g, 136)
h3['widgets_values'] = ['', 1344, 768, 264, 'match']

# swap prompt
find(g, 138)['widgets_values'] = [prompt]

# latent: load clip 7 (F2 tail) -> save clip 8 (unchanged from G_papers)
find(g, 161)['widgets_values'] = ['h3_context', 7]
find(g, 164)['widgets_values'] = ['h3_context/clip', 8]

json.dump(g, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written:', OUT)

# verify
wf = json.load(open(OUT, encoding='utf-8'))
h3 = find(wf, 136)
print('H3 widgets:', h3['widgets_values'])
for n in wf['nodes']:
    if n['type'] == 'LoadImage':
        print('  LoadImage', n['id'], '->', n['widgets_values'][0])
for n in wf['nodes']:
    if n['id'] in (161, 164):
        print('  node', n['id'], n['type'], '->', n['widgets_values'])
print('prompt len:', len(find(wf, 138)['widgets_values'][0]))
print('total nodes:', len(wf['nodes']))
