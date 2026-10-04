"""Make krea2T2iI2iInpaint2pass_v15 runnable by swapping the 2 missing model files
to proven available equivalents. Preserves the original; writes a _fixed copy.

Swaps:
  VAE  krea2RealVae_v10.safetensors            -> qwen_image_vae.safetensors
  UNet Krea2_Turbo_convrot_int8mixed.safetensors -> krea2_turbo_fp8_scaled.safetensors

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\fix_2pass_models.py"
"""
import json, os, shutil

SRC = r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2T2iI2iInpaint2pass_v15_fixed.json"

VAE_OLD, VAE_NEW = "krea2RealVae_v10.safetensors", "qwen_image_vae.safetensors"
UNET_OLD, UNET_NEW = "Krea2_Turbo_convrot_int8mixed.safetensors", "krea2_turbo_fp8_scaled.safetensors"

wf = json.load(open(SRC, encoding="utf-8"))

def swap_in_node(n):
    changed = []
    # widgets_values (positional list)
    wv = n.get("widgets_values")
    if isinstance(wv, list):
        for i, v in enumerate(wv):
            if v == VAE_OLD:
                wv[i] = VAE_NEW; changed.append(("widgets_values", VAE_OLD, VAE_NEW))
            elif v == UNET_OLD:
                wv[i] = UNET_NEW; changed.append(("widgets_values", UNET_OLD, UNET_NEW))
    # widgets_values_named (dict)
    wvn = n.get("widgets_values_named")
    if isinstance(wvn, dict):
        for k, v in list(wvn.items()):
            if v == VAE_OLD:
                wvn[k] = VAE_NEW; changed.append(("widgets_values_named.%s" % k, VAE_OLD, VAE_NEW))
            elif v == UNET_OLD:
                wvn[k] = UNET_NEW; changed.append(("widgets_values_named.%s" % k, UNET_OLD, UNET_NEW))
    return changed

all_changes = []
for n in wf.get("nodes", []):
    c = swap_in_node(n)
    if c:
        all_changes.append((n.get("id"), n.get("type"), c))
for s in wf.get("definitions", {}).get("subgraphs", []):
    for n in s.get("nodes", []):
        c = swap_in_node(n)
        if c:
            all_changes.append((n.get("id"), n.get("type"), c))

os.makedirs(os.path.dirname(DST), exist_ok=True)
json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)

print("=== changes applied ===")
for nid, ntype, c in all_changes:
    print(f"node {nid} ({ntype}):")
    for loc, old, new in c:
        print(f"   {loc}: {old} -> {new}")
print("\nwrote:", DST)
print("total nodes changed:", len(all_changes))
