import sys
from PIL import Image, ImageFilter
import numpy as np

V7 = r'D:\models\vsCodeMcp\Jaisal-intro\v7'
orig = Image.open(V7 + r'\kf2_seated_v7_00001_.png').convert('RGB')

# --- Step 1: combine the two SAM3 masks (chair OR wall) into ONE starting mask ---
chair = np.array(Image.open(V7 + r'\kf2_mask_chair.png').convert('L'))
wall = np.array(Image.open(V7 + r'\kf2_mask_wall.png').convert('L'))
combined = np.maximum(chair, wall)
Image.fromarray(combined).save(V7 + r'\kf2_mask_combined.png')
print('combined mask (chair+wall) ->', V7 + r'\kf2_mask_combined.png')

# --- Step 2: apply a mask (white = replace) with a fill color ---
# usage: python apply_mask_fill.py [mask_path] [feather_px] [fill R,G,B] [out_path]
mask_path = sys.argv[1] if len(sys.argv) > 1 else V7 + r'\kf2_mask_combined.png'
feather = int(sys.argv[2]) if len(sys.argv) > 2 else 8
fill = tuple(int(x) for x in sys.argv[3].split(',')) if len(sys.argv) > 3 else (0, 0, 0)
out = sys.argv[4] if len(sys.argv) > 4 else V7 + r'\kf2_seated_v7_clean.png'

m = Image.open(mask_path).convert('L')
if m.size != orig.size:
    print('mask size', m.size, '!= image', orig.size, '-> resizing mask')
    m = m.resize(orig.size)
if feather > 0:
    m = m.filter(ImageFilter.GaussianBlur(feather))
arr = np.array(orig).astype(np.float32)
alpha = np.array(m).astype(np.float32) / 255.0
arr = arr * (1.0 - alpha[..., None]) + np.array(fill, dtype=np.float32) * alpha[..., None]
Image.fromarray(arr.astype(np.uint8)).save(out)
print('applied mask ->', out, '(fill', fill, 'feather', feather, 'px)')
