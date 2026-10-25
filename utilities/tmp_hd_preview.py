from PIL import Image
import os
out = r"D:\models\vsCodeMcp\data\refset_v7_preview"
os.makedirs(out, exist_ok=True)
src = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\refset_v7"
for name in ["jaisal_portrait_HD_00001_.png", "zidane_portrait_HD_00001_.png"]:
    p = os.path.join(src, name)
    im = Image.open(p)
    print(name, "orig:", im.size)
    im = im.convert("RGB")
    im.thumbnail((1400, 1400))
    dst = os.path.join(out, name.replace(".png", ".jpg"))
    im.save(dst, "JPEG", quality=88)
    print("  ->", dst, im.size)
