from PIL import Image, ImageFilter, ImageDraw
import numpy as np

src = r'D:\models\vsCodeMcp\Jaisal-intro\v7\kf2_seated_v7_00001_.png'
img = Image.open(src).convert('RGB')
W, H = img.size
print('size', W, H)

g = np.array(img.convert('L'))
# The extra chair sits in the bottom-LEFT, on a pure black void.
# Restrict the search to that region so we never touch the table/character (center).
x_max = int(0.40 * W)
y_min = int(0.45 * H)
region = g[y_min:, :x_max]
ys, xs = np.where(region > 35)
if len(xs) == 0:
    print('NO bright pixels in bottom-left region; chair not found by threshold')
else:
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()) + y_min, int(ys.max()) + y_min
    print('chair bbox:', x0, y0, x1, y1, 'of', W, H)
    mx = int(0.025 * W); my = int(0.025 * H)
    x0 = max(0, x0 - mx); y0 = max(0, y0 - my)
    x1 = min(W - 1, x1 + mx); y1 = min(H - 1, y1 + my)
    print('painted box (with margin):', x0, y0, x1, y1)
    mask = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.rectangle([x0, y0, x1, y1], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(30))
    arr = np.array(img).astype(np.float32)
    m = np.array(mask).astype(np.float32) / 255.0
    arr = arr * (1.0 - m[..., None])  # -> black where mask=1
    out = Image.fromarray(arr.astype(np.uint8))
    out1 = r'D:\models\vsCodeMcp\Jaisal-intro\v7\kf2_seated_v7_nochair.png'
    out2 = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\kf2_seated_v7_nochair.png'
    out.save(out1)
    out.save(out2)
    print('saved', out1)
    print('saved', out2)
