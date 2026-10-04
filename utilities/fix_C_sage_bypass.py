import json, io, os, shutil

WF = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json'
BAK = WF + '.bak_sage'

if not os.path.exists(BAK):
    shutil.copyfile(WF, BAK)
    print("Backed up ->", BAK)

d = json.load(io.open(WF, encoding='utf-8'))
sub = d['definitions']['subgraphs'][0]

# 1. Retarget link 404 (origin 6 UNET) from node 136 -> node 137 (ModelAttentionBackend)
retargeted = False
for l in sub['links']:
    if l['id'] == 404:
        assert l['origin_id'] == 6, "link 404 origin is not UNET(6): %r" % l
        l['target_id'] = 137
        l['target_slot'] = 0
        retargeted = True
        print("Retargeted link 404: 6 -> 137 (was 136)")
assert retargeted, "link 404 not found"

# 2. Remove link 269 (136 -> 137)
before = len(sub['links'])
sub['links'] = [l for l in sub['links'] if l['id'] != 269]
print("Removed link 269 (136->137):", before - len(sub['links']), "link(s) removed")

# 3. Remove node 136 (the sage patch)
before = len(sub['nodes'])
sub['nodes'] = [n for n in sub['nodes'] if n['id'] != 136]
print("Removed node 136 (SagePatch):", before - len(sub['nodes']), "node(s) removed")

# 4. Update node 137's model input link field: 269 -> 404
for n in sub['nodes']:
    if n['id'] == 137:
        for inp in n.get('inputs', []):
            if inp.get('name') == 'model' and inp.get('link') == 269:
                inp['link'] = 404
                print("Node 137 model input link: 269 -> 404")

# 5. Verify the new chain is intact
print("\n=== VERIFY new model chain ===")
for l in sub['links']:
    if l['type'] == 'MODEL':
        print("  MODEL link", l['id'], ":", l['origin_id'], "->", l['target_id'], "slot", l['target_slot'])

json.dump(d, io.open(WF, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("\nSaved", WF)
