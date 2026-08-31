import urllib.request, os, json

LORA_DIR = r"E:\ComfyUI_windows_portable\ComfyUI\models\loras"

# Remove junk (error-page) files
for f in os.listdir(LORA_DIR):
    p = os.path.join(LORA_DIR, f)
    if os.path.isfile(p) and os.path.getsize(p) < 100_000 and f.endswith(".safetensors"):
        print(f"removing junk: {f} ({os.path.getsize(p)} bytes)")
        os.remove(p)

# Re-download with explicit file-type params (Civitai needs type=Model&format=SafeTensor)
targets = [
    ("https://civitai.com/api/download/models/3169623?type=Model&format=SafeTensor", "SimpleFineVector_Krea2_v1.safetensors"),
    ("https://civitai.com/api/download/models/3262188?type=Model&format=SafeTensor", "krea2_coloringbook_v1.safetensors"),
    ("https://civitai.com/api/download/models/3205841?type=Model&format=SafeTensor", "friendlysketch-v2_krea2.safetensors"),
]

def download(url, fname):
    dest = os.path.join(LORA_DIR, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 1_000_000:
        print(f"SKIP (exists): {fname} ({os.path.getsize(dest)//1024//1024} MB)")
        return
    print(f"DOWNLOADING {fname} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    tmp = dest + ".part"
    with urllib.request.urlopen(req, timeout=180) as r, open(tmp, "wb") as f:
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        while True:
            chunk = r.read(1024 * 256)
            if not chunk:
                break
            f.write(chunk)
            done += len(chunk)
            if total:
                print(f"\r  {done//1024//1024}/{total//1024//1024} MB ({done*100//total}%)", end="", flush=True)
    os.replace(tmp, dest)
    print(f"\nDONE: {fname} ({os.path.getsize(dest)//1024//1024} MB)")

for url, fname in targets:
    try:
        download(url, fname)
    except Exception as e:
        print(f"FAILED {fname}: {e}")

print("\n=== sketch/vector loras now ===")
for f in sorted(os.listdir(LORA_DIR)):
    if any(k in f.lower() for k in ("vector","lineart","coloring","sketch","friendly")):
        print(f"  {f}  ({os.path.getsize(os.path.join(LORA_DIR,f))//1024//1024} MB)")
