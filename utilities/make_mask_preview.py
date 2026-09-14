from PIL import Image
import numpy as np

V7 = r'D:\models\vsCodeMcp\Jaisal-intro\v7'
orig = np.array(Image.open(V7 + r'\kf2_seated_v7_00001_.png').convert('RGB')).astype(np.float32)
m = np.array(Image.open(V7 + r'\kf2_mask_combined.png').convert('L')).astype(np.float32) / 255.0
# tint the masked region red (50% blend) so it's clearly visible
red = np.array([255, 0, 0], dtype=np.float32)
overlay = orig * (1.0 - 0.5 * m[..., None]) + red * (0.5 * m[..., None])
Image.fromarray(overlay.astype(np.uint8)).save(V7 + r'\kf2_mask_preview_red.png')
print('preview ->', V7 + r'\kf2_mask_preview_red.png')
