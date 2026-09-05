import os

hub = os.path.join(os.environ["USERPROFILE"], ".cache", "huggingface", "hub")

repos = [
    "models--apple--DFN5B-CLIP-ViT-H-14-384",
    "models--nvidia--bigvgan_v2_44khz_128band_512x",
    "models--facebook--musicgen-style",
    "models--m-a-p--MERT-v1-95M",
    "models--roberta-base",
    "models--facebook--bart-base",
    "models--bert-base-uncased",
]

def repo_size_mb(name):
    d = os.path.join(hub, name)
    if not os.path.isdir(d):
        return None
    tot = 0
    for root, _, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f)
            try:
                tot += os.path.getsize(p)
            except OSError:
                pass
    return tot / (1024 * 1024)

print("=== 7 dependency repos (HF cache) ===")
total = 0.0
for r in repos:
    sz = repo_size_mb(r)
    if sz is None:
        print(f"  {'ABSENT':>10}   {r}")
    else:
        total += sz
        print(f"  {sz:10.1f} MB  {r}")
print(f"\n  TOTAL deps: {total:.1f} MB")

# Show the big CLIP files specifically
clip = os.path.join(hub, "models--apple--DFN5B-CLIP-ViT-H-14-384")
print("\n=== CLIP big files (>100MB) ===")
if os.path.isdir(clip):
    for root, _, files in os.walk(clip):
        for f in files:
            p = os.path.join(root, f)
            try:
                s = os.path.getsize(p)
            except OSError:
                continue
            if s > 100 * 1024 * 1024:
                print(f"  {s/(1024*1024):10.1f} MB  {f}")
else:
    print("  (CLIP dir not present)")
