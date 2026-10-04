import json

path = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
with open(path, "r", encoding="utf-8") as f:
    wf = json.load(f)

print("=== A NODES (sampler/decode/video chain) ===")
for n in wf["nodes"]:
    nid = n.get("id")
    ntype = n.get("type")
    if any(k in ntype for k in ("Sampler", "VAEDecode", "CreateVideo", "SaveVideo", "ReferenceToVideo", "ImageToVideo", "TextToVideo", "SaveLatent", "MotionContext")):
        wv = n.get("widgets_values")
        wvs = wv if not (isinstance(wv, list) and len(str(wv)) > 100) else str(wv)[:100] + "..."
        print(f"\n[{nid}] {ntype}  widgets={wvs}")
        for i in n.get("inputs", []):
            print(f"    in  {i.get('name'):26s} {i.get('type'):14s} link={i.get('link')}")
        for o in n.get("outputs", []):
            print(f"    out {o.get('name'):26s} {o.get('type'):14s} links={o.get('links')}")

print("\n=== A LINKS (sampler/decode/video) ===")
for l in wf.get("links", []):
    if isinstance(l, list) and len(l) >= 6:
        print(f"  link {l[0]}: node {l[1]} slot {l[2]} -> node {l[3]} slot {l[4]} ({l[5]})")
