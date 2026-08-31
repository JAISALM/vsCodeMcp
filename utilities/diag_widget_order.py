import json, os

BASE = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# Native workflows = the ones the UI itself saved (named=False). Collect every
# node type's widgets_values from native files to learn the TRUE widget order
# (including hidden widgets like KSampler's control_after_generate).
native_files = [
    "krea2_jaisal_base.json",
    "05_Chained.json",
    "QWEN_click_multiple_character_angles-v1.0.json",
    "mini-max-refrance-to-video-1.json",
    "video_minimax_h3_t2v.json",
    "kerala_kid_2d_ref.json",
    "oneNode-Flux.json",
]

# node_type -> list of (widgets_values, source_file)
samples = {}
for f in native_files:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        continue
    wf = json.load(open(p, encoding="utf-8"))
    if not isinstance(wf.get("nodes"), list):
        continue
    for n in wf["nodes"]:
        t = n.get("type")
        wv = n.get("widgets_values")
        if wv is None:
            continue
        samples.setdefault(t, []).append((wv, f))

# The Krea2 chain node types we care about
focus = ["KSampler", "LoadImage", "CLIPTextEncode", "CLIPLoader", "UNETLoader",
         "VAELoader", "LoraLoaderModelOnly", "SaveImage", "PreviewImage",
         "VAEEncode", "VAEDecode", "EmptyLatentImage", "EmptyFlux2LatentImage"]

print("=== GROUND-TRUTH widget order from NATIVE workflows ===")
for t in focus:
    print(f"\n### {t} ###")
    seen = set()
    for wv, f in samples.get(t, []):
        key = json.dumps(wv, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        print(f"   len={len(wv)}  {wv}   [{os.path.basename(f)}]")
    if t not in samples:
        print("   (no native sample found)")
