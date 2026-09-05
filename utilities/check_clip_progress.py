import os, time, glob

hub = os.path.join(os.environ["USERPROFILE"], ".cache", "huggingface", "hub")
d = os.path.join(hub, "models--apple--DFN5B-CLIP-ViT-H-14-384")

def total_mb():
    if not os.path.isdir(d):
        return 0.0
    tot = 0
    for root, _, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f)
            try:
                tot += os.path.getsize(p)
            except OSError:
                pass
    return tot / (1024 * 1024)

a = total_mb()
print(f"CLIP total at t0: {a:.2f} MB")
time.sleep(20)
b = total_mb()
print(f"CLIP total at t+20s: {b:.2f} MB")
print(f"DELTA over 20s: {b - a:.2f} MB  ->  {'MOVING' if (b - a) > 0.5 else 'STUCK (no movement)'}")

print("\n=== incomplete files ===")
for root, _, files in os.walk(d):
    for f in files:
        if f.endswith(".incomplete"):
            p = os.path.join(root, f)
            print(f"  {os.path.getsize(p)/(1024*1024):10.2f} MB  {f}")
