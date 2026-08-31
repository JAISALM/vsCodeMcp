import json, os, shutil

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"

# 1) Copy the 5 images to input\ with clean names 1-5
mapping = {
    "1base1.png": "1.png",
    "2mid rain.png": "2.png",
    "3closeUp_drenched.png": "3.png",
    "4after rain.png": "4.png",
    "5ComfyUI-low_angle_00002_.png": "5.png",
}
print("=== Copying images to input\\ ===")
for src, dst in mapping.items():
    sp = os.path.join(SRC, src)
    dp = os.path.join(DST, dst)
    if os.path.exists(sp):
        shutil.copy2(sp, dp)
        print(f"   {src} -> {dst} ({os.path.getsize(dp)} bytes)")
    else:
        print(f"   *** MISSING: {src}")

# 2) Dump template links + MiniMax node inputs
print("\n=== TEMPLATE LINKS (video_minimax_h3_r2v+turbo.json) ===")
tp = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\video_minimax_h3_r2v+turbo.json"
wf = json.load(open(tp, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}
for l in wf["links"]:
    print(f"   link {l[0]}: {l[1]}.{l[2]} -> {l[3]}.{l[4]} ({l[5]})")

print("\n=== MiniMax node (136) inputs ===")
mm = nodes["136"]
for i in mm["inputs"]:
    print(f"   {i['name']:20} type={i['type']} link={i.get('link')}")

print("\n=== LoadImage nodes in template ===")
for n in wf["nodes"]:
    if n["type"] == "LoadImage":
        print(f"   id={n['id']} widgets={n['widgets_values']}")
        for o in n["outputs"]:
            print(f"      output {o['name']} links={o['links']}")
