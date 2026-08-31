import json, re
s = open(r'd:\models\vsCodeMcp\data\object_info_cache.json', encoding='utf-8').read()
# fix duplicate key that breaks json.loads
s = re.sub(r'"ClownOptions_Frameweights"', '"ClownOptions_Frameweights_dup"', s)
oi = json.loads(s)
names = [k for k in oi if re.search(r'Upscal|SuperRes|Upscale|VSR|Hunyuan|Topaz|RealESRGAN|LatentUpscale|VideoUpscale|VideoScale', k, re.I)]
print("=== upscaler-ish node classes ===")
for n in names:
    print(n)
print()
# Show details for the most relevant ones
for n in names:
    if re.search(r'RTX|Hunyuan|Topaz|VideoUpscale|LatentUpscale|UpscaleImage', n, re.I):
        info = oi[n]
        print("=== ", n, " ===")
        print("input:", json.dumps(info.get('input', {}), indent=1)[:800])
        print("output:", info.get('output', None))
        print()
