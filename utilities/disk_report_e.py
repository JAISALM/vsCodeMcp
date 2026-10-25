"""Top files per ComfyUI model category + D:\\models deep dirs + recycle-bin structure."""
import os

def top_files(path, n=15):
    rows = []
    total = 0
    count = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            p = os.path.join(root, f)
            try:
                sz = os.path.getsize(p)
                total += sz
                count += 1
                rows.append((sz, os.path.relpath(p, path)))
            except OSError:
                pass
    rows.sort(reverse=True)
    print("\n### {}  (total {:.1f} GB, {} files)".format(path, total / 1e9, count))
    for sz, rel in rows[:n]:
        print("  {:9.1f} GB  {}".format(sz / 1e9, rel))

MP = r"E:\ComfyUI_windows_portable\ComfyUI\models"
print("=" * 80)
print("MAIN MODELS PATH — top files per category")
print("=" * 80)
for cat in ("diffusion_models", "text_encoders", "loras", "unet", "checkpoints",
            "clip", "vae", "SEEDVR2", "LLM", "controlnet"):
    p = os.path.join(MP, cat)
    if os.path.isdir(p):
        top_files(p)

print()
print("=" * 80)
print("D:\\models deep dirs")
print("=" * 80)
for sub in ("Writing", "ai-movie", "blobs", "SeedVR2-TensorRT-Studio"):
    p = os.path.join(r"D:\models", sub)
    if os.path.isdir(p):
        top_files(p, n=12)

print()
print("=" * 80)
print("D:\\$RECYCLE.BIN — structure (top-level + sizes, errors shown)")
print("=" * 80)
rb = r"D:\$RECYCLE.BIN"
try:
    for name in os.listdir(rb):
        p = os.path.join(rb, name)
        try:
            if os.path.isdir(p):
                tot = 0
                errs = [0]
                def onerr(e):
                    errs[0] += 1
                for root, dirs, files in os.walk(p, onerror=onerr):
                    for f in files:
                        try:
                            tot += os.path.getsize(os.path.join(root, f))
                        except OSError:
                            errs[0] += 1
                print("{:<40} {:9.1f} GB  (unreadable files: {})".format(name, tot / 1e9, errs[0]))
            else:
                print("{:<40} {:9.1f} MB".format(name, os.path.getsize(p) / 1e6))
        except OSError as e:
            print("{:<40} READ-ERROR: {}".format(name, e))
except PermissionError as e:
    print("TOP-LEVEL READ ERROR:", e)
