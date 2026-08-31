import json, shutil, os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisalproduction1.json"
BAK = WF + ".pre_imgonly.bak"
if not os.path.exists(BAK):
    shutil.copy(WF, BAK)
    print("backup ->", BAK)

d = json.load(open(WF, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

# 1) length -> 15
n132 = nodes[132]
n132["widgets_values"] = [15]
if "widgets_values_named" in n132:
    n132["widgets_values_named"]["value"] = 15
print("132 ->", n132["widgets_values"])

# 2) remove node 149 (ref video loader)
d["nodes"] = [n for n in d["nodes"] if n["id"] != 149]
print("removed node 149")

# 3) remove links 303/304
before = len(d["links"])
d["links"] = [l for l in d["links"] if l[0] not in (303, 304)]
print("removed links:", before - len(d["links"]))

# 4) clear node 136 ref_video inputs (ref_video_0, ref_video_audio_0)
n136 = nodes[136]
for inp in n136["inputs"]:
    if inp["name"] in ("ref_videos.ref_video_0", "ref_video_audios.ref_video_audio_0"):
        inp["link"] = None
        print("cleared", inp["name"])

json.dump(d, open(WF, "w", encoding="utf-8"), indent=4)
print("saved. nodes:", len(d["nodes"]), "links:", len(d["links"]))
print("SLA still present:", any(n["type"] == "H3SLAAttention" for n in d["nodes"]))
