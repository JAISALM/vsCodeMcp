import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json"
wf = json.load(open(p, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

print("=== LoadImage nodes (which image each loads) ===")
for n in wf["nodes"]:
    if n["type"] == "LoadImage":
        print(f"   id={n['id']:8} widgets={n['widgets_values']}  IMAGE output links={n['outputs'][0]['links']}")

print("\n=== MiniMax node (136) ref_image inputs + their links ===")
mm = nodes["136"]
for i in mm["inputs"]:
    if "ref_image" in i["name"]:
        print(f"   {i['name']:24} link={i.get('link')}")

print("\n=== All links touching node 136 ===")
for l in wf["links"]:
    if l[3] == "136" or l[1] == "136":
        print(f"   link {l[0]}: {l[1]}.{l[2]} -> {l[3]}.{l[4]} ({l[5]})")

# Trace: for each ref_image_N, which LoadImage feeds it?
print("\n=== ref_image -> LoadImage trace ===")
link_map = {l[0]: l for l in wf["links"]}
for i in mm["inputs"]:
    if "ref_image" in i["name"]:
        lid = i.get("link")
        if lid:
            l = link_map.get(lid)
            src_node = l[1]
            src = nodes.get(str(src_node), {})
            print(f"   {i['name']:24} <- link {lid} <- node {src_node} ({src.get('type')}) {src.get('widgets_values')}")
        else:
            print(f"   {i['name']:24} <- NO LINK (unwired)")
