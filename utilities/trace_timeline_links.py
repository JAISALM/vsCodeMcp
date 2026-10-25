"""Trace link sources in the timeline workflow: refs, prompt, length, model chain."""
import json

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
nodes = {n["id"]: n for n in j["nodes"]}

def node_desc(nid):
    n = nodes.get(nid)
    if not n:
        return f"?{nid}"
    w = n.get("widgets_values")
    return f"{n['id']}[{n['type']}] w={str(w)[:100]}"

# links feeding node 797 (the R2V node)
targets = {2314: "ref_image_0", 2315: "ref_image_1", 2316: "ref_image_2",
           2317: "ref_image_3", 2611: "ref_video_0", 2584: "prompt",
           2585: "width", 2586: "height", 3036: "length", 2612: "ref_video_audio_0",
           2318: "ref_audio_0", 2319: "ref_audio_1"}
print("== links into R2V node 797 ==")
for L in j["links"]:
    a = list(L)
    if a[3] == 797 and a[0] in targets:
        print(f"  {targets[a[0]]}: link {a[0]} <- {node_desc(a[1])}")

print()
print("== LoadImagesCompose nodes ==")
for n in j["nodes"]:
    if n["type"] == "LoadImagesCompose":
        print(f"  {node_desc(n['id'])}  inputs: " +
              ", ".join(f"{i['name']} link={i.get('link')}" for i in n.get("inputs", [])))

print()
print("== model chain: node 1400 ==")
n = nodes.get(1400)
print(f"  {node_desc(1400) if n else '1400 not found'}")
if n:
    for i in n.get("inputs", []):
        print(f"    in: {i['name']} ({i['type']}) link={i.get('link')}")
    for L in j["links"]:
        a = list(L)
        if a[3] == 1400:
            print(f"    <- link {a[0]}: {node_desc(a[1])}")

print()
print("== model loaders on canvas (UNETLoader/CLIPLoader/VAELoader outside subgraphs) ==")
for n in j["nodes"]:
    if n["type"] in ("UNETLoader", "CLIPLoader", "VAELoader", "LoraLoaderModelOnly", "MiniMaxH3TurboLoRA"):
        print(f"  {node_desc(n['id'])}")

print()
print("== length widget source: link 3036 target slot ==")
for L in j["links"]:
    a = list(L)
    if a[0] == 3036:
        print(f"  link 3036: {node_desc(a[1])} -> 797 slot {a[4]}")
