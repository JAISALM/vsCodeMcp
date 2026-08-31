import urllib.request, os, sys

url = "https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"
dest_dir = r"E:\ComfyUI_windows_portable\ComfyUI\models\loras"
os.makedirs(dest_dir, exist_ok=True)
dest = os.path.join(dest_dir, "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors")
tmp = dest + ".part"

def hook(blocks, block_size, total):
    done = blocks * block_size
    if total > 0:
        pct = done * 100.0 / total
        print(f"\r{done/1e9:.2f}/{total/1e9:.2f} GB ({pct:.1f}%)", end="", flush=True)

print("Downloading turbo 4-step LoRA to:", dest, flush=True)
urllib.request.urlretrieve(url, tmp, reporthook=hook)
os.replace(tmp, dest)
print("\nDONE:", dest, os.path.getsize(dest)/1e9, "GB", flush=True)
