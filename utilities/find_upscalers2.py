import json, re
s = open(r'd:\models\vsCodeMcp\data\object_info_cache.json', encoding='utf-8').read()
s = re.sub(r'"ClownOptions_Frameweights"', '"ClownOptions_Frameweights_dup"', s)
oi = json.loads(s)
names = [k for k in oi if re.search(r'Upscal|SuperRes|VSR|Topaz|RealESRGAN|VideoScale|VideoUpscale', k, re.I)]
print("=== upscaler-ish node classes ===")
for n in names:
    print(n)
print()
for n in names:
    info = oi[n]
    print("=== ", n, " ===")
    print("input:", json.dumps(info.get('input', {}))[:600])
    print("output:", info.get('output', None))
    print()
