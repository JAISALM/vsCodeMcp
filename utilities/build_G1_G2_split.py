import json, io, copy

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_papers.json'
OUTDIR = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows'
G1_PROMPT = r'd:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G1_burst_10s.txt'
G2_PROMPT = r'd:\models\vsCodeMcp\Jaisal-intro\prompts\shot_G2_aftermath_10s.txt'

src = json.load(open(SRC, encoding='utf-8'))
g1_prompt = io.open(G1_PROMPT, encoding='utf-8').read().strip()
g2_prompt = io.open(G2_PROMPT, encoding='utf-8').read().strip()

def find(wf, nid):
    for n in wf['nodes']:
        if n['id'] == nid:
            return n
    return None

def set_widgets(wf, nid, widgets):
    n = find(wf, nid)
    n['widgets_values'] = widgets

def remove_nodes(wf, ids):
    wf['nodes'] = [n for n in wf['nodes'] if n['id'] not in ids]
    wf['links'] = [l for l in wf['links'] if l[0] not in ids]

def clear_link_on_input(wf, nid, input_names):
    n = find(wf, nid)
    for i in n.get('inputs', []):
        if i.get('name') in input_names:
            i['link'] = None

# ============ G1 — burst (character present -> bursts -> gone) ============
g1 = copy.deepcopy(src)
set_widgets(g1, 137, ['kf7a_v4.png', 'image'])                       # ref_image_0 = start (character at table)
set_widgets(g1, 139, ['jaisal_gone_papers_alone.png', 'image'])      # ref_image_1 = end (papers only, no character)
set_widgets(g1, 136, ['', 1344, 768, 240, 'match'])                  # length 240 = 10s
set_widgets(g1, 138, [g1_prompt])
set_widgets(g1, 161, ['h3_context', 7])                              # load F2 tail (clip 7)
set_widgets(g1, 164, ['h3_context/clip', 8])                         # save as clip 8
# remove the 3 object-ref nodes + their links; clear their ref slots on node 136
remove_nodes(g1, {165, 166, 167, 318, 319, 320})
clear_link_on_input(g1, 136, {'ref_images.ref_image_2', 'ref_images.ref_image_3', 'ref_images.ref_image_4'})
json.dump(g1, open(OUTDIR + r'\jaisal_intro_G1_burst.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('G1 written: jaisal_intro_G1_burst.json  (2 refs, 10s, load7->save8)')

# ============ G2 — aftermath (papers only start, no character, voices + objects) ============
g2 = copy.deepcopy(src)
set_widgets(g2, 137, ['jaisal_gone_papers_alone.png', 'image'])      # ref_image_0 = start (papers only)
set_widgets(g2, 139, ['mic+paper.png', 'image'])                     # ref_image_1 = end (papers + mic)
# keep 165/166/167 object refs (cricket bat, soccer ball, smiley paper) as-is
set_widgets(g2, 136, ['', 1344, 768, 240, 'match'])                  # length 240 = 10s
set_widgets(g2, 138, [g2_prompt])
set_widgets(g2, 161, ['h3_context', 8])                              # load G1 tail (clip 8)
set_widgets(g2, 164, ['h3_context/clip', 9])                         # save as clip 9
json.dump(g2, open(OUTDIR + r'\jaisal_intro_G2_aftermath.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('G2 written: jaisal_intro_G2_aftermath.json  (5 refs, 10s, load8->save9)')

# ============ verify ============
for name, f in [('G1', 'jaisal_intro_G1_burst.json'), ('G2', 'jaisal_intro_G2_aftermath.json')]:
    wf = json.load(open(OUTDIR + '\\' + f, encoding='utf-8'))
    h3 = find(wf, 136)
    print(f'--- {name} ---')
    print('  H3 widgets:', h3['widgets_values'])
    for n in wf['nodes']:
        if n['type'] == 'LoadImage':
            print('  LoadImage', n['id'], '->', n['widgets_values'][0])
    for n in wf['nodes']:
        if n['id'] in (161, 164):
            print('  node', n['id'], n['type'], '->', n['widgets_values'])
    # confirm ref slots on 136
    for i in h3['inputs']:
        if i['name'].startswith('ref_images.'):
            print('  ', i['name'], 'link=', i['link'])
