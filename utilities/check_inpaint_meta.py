import json, re
d = json.load(open(r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\Krea2_LanPaint_Inpaint_v1.json', encoding='utf-8'))
print('TOP KEYS:', list(d.keys()))
print('extra:', {k: v for k, v in d.items() if k not in ('nodes', 'links')})
s = json.dumps(d)
print('cnr_id hints:', sorted(set(re.findall(r'cnr_id["\']?\s*:\s*["\']([^"\']+)', s))))
# also look for any 'pack' or 'repo' strings
print('repo hints:', sorted(set(re.findall(r'(?:repo|pack|source)["\']?\s*:\s*["\']([^"\']+)', s)))[:20])
