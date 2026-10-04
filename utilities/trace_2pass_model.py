"""Trace the model chain into both samplers (1st pass KSampler 307, 2nd pass subgraph 186).

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\trace_2pass_model.py"
"""
import json

wf = json.load(open(r"E:\Krea2\krea2T2iI2iInpaint2pass_v15.json", encoding="utf-8"))
nodes = {n.get("id"): n for n in wf.get("nodes", [])}
links = wf.get("links", [])

def src_of_link(lid):
    for l in links:
        if l[0] == lid:
            return nodes.get(l[3], {}).get("type", f"?{l[3]}")
    return None

def model_input(nid):
    n = nodes.get(nid)
    if not n:
        return None
    for i in n.get("inputs", []):
        if i.get("name") == "model":
            lid = i.get("link")
            return f"{src_of_link(lid)} (link {lid})" if lid else "none"
    return "no model input"

print("1st pass KSampler (307) model <-", model_input(307))
print("2nd pass subgraph (186) model <-", model_input(186))

# What feeds the Power Lora Loader (279) and where does it go?
print("\nPower Lora Loader (279):")
n = nodes[279]
for i in n.get("inputs", []):
    if i.get("name") == "model":
        print("  model in <-", src_of_link(i.get("link")))
for o in n.get("outputs", []):
    for lid in (o.get("links") or []):
        for l in links:
            if l[0] == lid:
                print(f"  model out -> {nodes.get(l[3],{}).get('type')} (node {l[3]})")

# What feeds the 1st pass KSampler's latent + conditioning
print("\n1st pass KSampler (307) inputs:")
for i in nodes[307].get("inputs", []):
    print(f"  {i.get('name')} <- {src_of_link(i.get('link'))} (link {i.get('link')})")

# The 2nd pass subgraph inputs
print("\n2nd pass subgraph (186) inputs:")
for i in nodes[186].get("inputs", []):
    print(f"  {i.get('name')} <- {src_of_link(i.get('link'))} (link {i.get('link')})")
