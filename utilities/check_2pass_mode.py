"""Check current VAE availability + the i2i/inpaint mode mechanism (Any Switch + groups).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\check_2pass_mode.py"
"""
import json, urllib.request

# 1. Current VAE list from live server
raw = urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60).read().decode("utf-8", "replace")
d = json.loads(raw)

def combo_options(node, field):
    info = d.get(node, {})
    inp = info.get("input", {})
    for section in ("required", "optional"):
        if field in inp.get(section, {}):
            spec = inp[section][field]
            if isinstance(spec, list) and len(spec) >= 2 and isinstance(spec[1], dict):
                return spec[1].get("choices", spec[1])
            return spec
    return None

vae_opts = combo_options("VAELoader", "vae_name")
print("=== current VAE options (live server) ===")
print(vae_opts)
print("krea2RealVae_v10 available:", "krea2RealVae_v10.safetensors" in (vae_opts or []))
print("qwen_image_vae available:", "qwen_image_vae.safetensors" in (vae_opts or []))

# 2. UNet options
unet_opts = combo_options("UNETLoader", "unet_name")
print("\n=== krea2 UNet options ===")
print([u for u in (unet_opts or []) if "krea" in str(u).lower()])

# 3. The i2i/inpaint mode mechanism: Any Switch nodes + which groups the muters control
wf = json.load(open(r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json", encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
links = wf.get("links", [])

def trace(nid, label):
    n = nodes.get(nid)
    print(f"\n=== {label} (node {nid}) ===")
    for i in n.get("inputs", []):
        lid = i.get("link")
        if lid:
            for l in links:
                if l[0] == lid:
                    src = nodes.get(l[3], {}).get("type", f"?{l[3]}")
                    print(f"    {i.get('name')} <- link {lid} <- {src}")

trace(271, "Any Switch 'Latent' — T2I vs i2i latent")
trace(273, "Any Switch 'Denoise'")
trace(298, "Any Switch 'MaskChoice' — SolidMask vs painted mask")

# 4. The Fast Groups Muter/Bypasser raw JSON (to see how they store group refs)
print("\n=== Fast Groups Muter/Bypasser raw JSON ===")
for nid in (299, 304, 272, 286, 287):
    n = nodes.get(nid)
    if n:
        print(f"\n--- node {nid} ({n.get('type')}) title={n.get('title')} ---")
        print(json.dumps(n, indent=1)[:1200])
