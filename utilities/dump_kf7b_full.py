import json, os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
f = os.path.join(WF, "krea2_intro_kf7b_page_mic_v8.json")
d = json.load(open(f, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

for nid in [84, 85]:
    n = nodes[nid]
    print("=" * 80)
    print(f"NODE {nid}  {n['type']}  title={n.get('title')}")
    print("-" * 80)
    for i, w in enumerate(n.get("widgets_values") or []):
        if isinstance(w, str) and len(w) > 60:
            print(f"[widget {i}]:")
            print(w)
        else:
            print(f"[widget {i}]: {w!r}")
    print()

# reference image + key params
print("=" * 80)
print("KEY PARAMS")
print("LoadImage(72):", nodes[72].get("widgets_values"))
print("Krea2EditModelPatch(79):", nodes[79].get("widgets_values"))
print("KSampler(53):", nodes[53].get("widgets_values"))
print("EmptySD3Latent(82):", nodes[82].get("widgets_values"))
print("ResolutionSelector(83):", nodes[83].get("widgets_values"))
print("UNET(55):", nodes[55].get("widgets_values"))
print("CLIP(56):", nodes[56].get("widgets_values"))
print("VAE(57):", nodes[57].get("widgets_values"))
print("LoRA(71):", nodes[71].get("widgets_values"))
print("SaveImage(29):", nodes[29].get("widgets_values"))
