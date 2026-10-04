"""Find the negative prompt source + Any Switch widget format + i2i chain node modes.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\find_2pass_negative.py"
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_2pass_bf16_turbo.json"
wf = json.load(open(WF, encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
links = wf.get("links", [])

def src_of(lid):
    for l in links:
        if l[0] == lid:
            return l[3], nodes.get(l[3], {}).get("type", f"?{l[3]}")
    return None, None

print("=== ALL CLIPTextEncode nodes + their text ===")
for nid, n in nodes.items():
    if n.get("type") == "CLIPTextEncode":
        wv = n.get("widgets_values")
        txt = wv[0] if isinstance(wv, list) and wv else wv
        print(f"\n--- CLIPTextEncode node {nid} (mode={n.get('mode')}) ---")
        print("  text:", (txt[:400] + "...") if isinstance(txt, str) and len(txt) > 400 else txt)

print("\n=== 1st pass KSampler (307) — trace each input's SOURCE (l[3]=dst, l[1]=src) ===")
n = nodes[307]
for i in n.get("inputs", []):
    lid = i.get("link")
    if lid:
        for l in links:
            if l[0] == lid:
                src_id = l[1]
                src_type = nodes.get(src_id, {}).get("type", f"?{src_id}")
                print(f"  {i.get('name'):<14} <- node {src_id} ({src_type})")

print("\n=== Any Switch widget format (node 271 Latent) ===")
n = nodes[271]
print("  widgets_values:", json.dumps(n.get("widgets_values")))
print("  widgets_values_named:", json.dumps(n.get("widgets_values_named")))
print("  full node:", json.dumps(n, indent=1)[:900])

print("\n=== i2i chain node modes ===")
for nid, label in [(265, "LoadImage"), (296, "ImageResizeKJv2"), (267, "InpaintModelConditioning"),
                    (271, "AnySwitch Latent"), (273, "AnySwitch Denoise"), (298, "AnySwitch MaskChoice"),
                    (254, "EmptyLatentImage"), (270, "PrimitiveFloat denoise"), (264, "mxSlider denoise")]:
    n = nodes.get(nid)
    if n:
        print(f"  {nid:>4} {label:<24} mode={n.get('mode')} ({'ACTIVE' if n.get('mode')==0 else 'BYPASSED' if n.get('mode')==4 else n.get('mode')}) widgets={json.dumps(n.get('widgets_values'))[:80]}")
