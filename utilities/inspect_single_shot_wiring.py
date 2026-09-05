import json, os, datetime

wf = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json'
d = json.load(open(wf, encoding='utf-8'))

print('=== TOP-LEVEL NODES ===')
for n in d['nodes']:
    print(f"  id={n['id']} type={n['type']}")

print()
print('=== LINKS (from_node.from_slot -> to_node.to_slot) ===')
for l in d.get('links', []):
    ltype = l[5] if len(l) > 5 else ''
    print(f"  {l[1]}.{l[2]} -> {l[3]}.{l[4]}  ({ltype})")

print()
print('=== SUBGRAPH INTERNAL NODES ===')
for sg in d.get('definitions', {}).get('subgraphs', []):
    for n in sg['nodes']:
        print(f"  id={n['id']} type={n['type']}")

print()
print('=== RECENT OUTPUTS (video dir) ===')
out = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output'
vid = os.path.join(out, 'video')
if os.path.isdir(vid):
    files = sorted([(os.path.getmtime(os.path.join(vid, f)), f) for f in os.listdir(vid) if f.endswith(('.mp4', '.webm'))], reverse=True)
    for mt, f in files[:10]:
        print(f"  {datetime.datetime.fromtimestamp(mt):%Y-%m-%d %H:%M}  {f}")
else:
    print('  no video dir')

# Analyze the reference image for wood/mica texture
print()
print('=== REFERENCE IMAGE TEXTURE ANALYSIS (sketch_00008_.png) ===')
from PIL import Image
import numpy as np
p = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\sketch_00008_.png'
im = Image.open(p).convert('RGB')
arr = np.array(im, dtype=np.float32)
h, w, _ = arr.shape
print(f'  size: {w}x{h}')
# Sample background regions (corners + edges) and measure color variance
def region_stats(name, region):
    r = arr[region[0]:region[1], region[2]:region[3]]
    mean = r.mean(axis=(0, 1))
    std = r.std(axis=(0, 1))
    print(f'  {name}: mean RGB={mean.round(1)}, std={std.round(1)}')
region_stats('top-left corner', (0, 60, 0, 60))
region_stats('top-right corner', (0, 60, w-60, w))
region_stats('bottom-left corner', (h-60, h, 0, 60))
region_stats('bottom-right corner', (h-60, h, w-60, w))
region_stats('top strip', (0, 30, 0, w))
region_stats('center', (h//2-50, h//2+50, w//2-50, w//2+50))
# Check for warm/brown tones (wood) in the background regions
def warm_check(name, region):
    r = arr[region[0]:region[1], region[2]:region[3]]
    # warm = R > B by a margin
    warm_frac = ((r[:,:,0] - r[:,:,2]) > 8).mean()
    print(f'  {name}: warm-tone fraction (R-B>8) = {warm_frac:.3f}')
warm_check('top strip', (0, 30, 0, w))
warm_check('top-left corner', (0, 60, 0, 60))
warm_check('top-right corner', (0, 60, w-60, w))
# Overall image: fraction of non-white pixels
nonwhite = ((arr < 240).any(axis=2)).mean()
print(f'  overall non-white pixel fraction: {nonwhite:.3f}')
# Check if there's a paper/cream tint overall
bg_mask = (arr > 235).all(axis=2)
if bg_mask.sum() > 0:
    bg_mean = arr[bg_mask].mean(axis=0)
    print(f'  background (near-white) mean RGB: {bg_mean.round(1)}')
    print(f'  background tint: R-B = {bg_mean[0]-bg_mean[2]:.1f} (positive = warm/cream)')
