import urllib.request, os

url = "https://huggingface.co/RudySen/Krea2-Realism-Checkpoint/resolve/main/Krea2Realism_V1.safetensors"
dest_dir = r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models"
os.makedirs(dest_dir, exist_ok=True)
dest = os.path.join(dest_dir, "Krea2Realism_V1.safetensors")
tmp = dest + ".part"

def hook(blocks, block_size, total):
    done = blocks * block_size
    if total > 0:
        pct = done * 100.0 / total
        print(f"\r{done/1e9:.2f}/{total/1e9:.2f} GB ({pct:.1f}%)", end="", flush=True)

print("Downloading Krea2Realism_V1 (FP8) to:", dest, flush=True)
urllib.request.urlretrieve(url, tmp, reporthook=hook)
os.replace(tmp, dest)
print("\nDONE:", dest, os.path.getsize(dest)/1e9, "GB", flush=True)
