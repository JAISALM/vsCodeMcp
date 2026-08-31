import urllib.request, os, sys

LORA_DIR = r"E:\ComfyUI_windows_portable\ComfyUI\models\loras"

# Best candidates for a 2D vector / line-art / stick-figure style on Krea 2
# (Civitai model-version download endpoints)
targets = [
    # (url, filename)
    ("https://civitai.com/api/download/models/3169623", "SimpleFineVector_Krea2_v1.safetensors"),
    ("https://civitai.com/api/download/models/3146526", "krea2_lineart_v1_fp16.safetensors"),
    ("https://civitai.com/api/download/models/3262188", "krea2_coloringbook_v1.safetensors"),
    ("https://civitai.com/api/download/models/3205841", "friendlysketch-v2_krea2.safetensors"),
]

os.makedirs(LORA_DIR, exist_ok=True)

def download(url, fname):
    dest = os.path.join(LORA_DIR, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 1_000_000:
        print(f"SKIP (exists): {fname} ({os.path.getsize(dest)//1024//1024} MB)")
        return
    print(f"DOWNLOADING {fname} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    tmp = dest + ".part"
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        while True:
            chunk = r.read(1024 * 256)
            if not chunk:
                break
            f.write(chunk)
            done += len(chunk)
            if total:
                pct = done * 100 // total
                print(f"\r  {done//1024//1024}/{total//1024//1024} MB ({pct}%)", end="", flush=True)
    os.replace(tmp, dest)
    print(f"\nDONE: {fname} ({os.path.getsize(dest)//1024//1024} MB)")

for url, fname in targets:
    try:
        download(url, fname)
    except Exception as e:
        print(f"FAILED {fname}: {e}")

print("\n=== loras dir now ===")
for f in sorted(os.listdir(LORA_DIR)):
    if "vector" in f.lower() or "lineart" in f.lower() or "coloring" in f.lower() or "sketch" in f.lower() or "friendly" in f.lower():
        print(f"  {f}  ({os.path.getsize(os.path.join(LORA_DIR,f))//1024//1024} MB)")
