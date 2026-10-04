"""Find the i2i workflow that made the paper/mic/obj refs (LoadImage base + save prefix).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\find_i2i_ref_workflow.py"
"""
import json, os, glob

WFDIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
PREFIXES = ("obj_cricket_bat", "obj_soccer_ball", "obj_paper_smiley", "paper+mic", "mic+paper", "jaisal_gone_papers", "mic_small")

for fp in glob.glob(os.path.join(WFDIR, "*.json")):
    try:
        wf = json.load(open(fp, encoding="utf-8"))
    except Exception:
        continue
    nodes = wf.get("nodes", [])
    load_images = []
    empty_latents = 0
    saves = []
    unets = []
    for n in nodes:
        t = n.get("type")
        wv = n.get("widgets_values") or []
        if t == "LoadImage":
            load_images.append(wv[0] if wv else None)
        elif t in ("EmptyLatentImage", "EmptySD3LatentImage", "EmptyQwenImageLayeredLatentImage"):
            empty_latents += 1
        elif t in ("SaveImage", "Image Saver Simple"):
            if wv:
                saves.append(wv[0])
        elif t in ("UNETLoader", "UnetLoaderGGUF"):
            if wv:
                unets.append(wv[0])
    # only show workflows that save to our prefixes
    relevant = [s for s in saves if any(p in str(s) for p in PREFIXES)]
    if relevant:
        name = os.path.basename(fp)
        print(f"\n=== {name} ===")
        print(f"  LoadImage bases: {load_images}")
        print(f"  EmptyLatent count: {empty_latents}")
        print(f"  saves: {relevant}")
        print(f"  unet: {unets}")
