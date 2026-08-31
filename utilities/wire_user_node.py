import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_jaisal_title_moody.json"
wf = json.load(open(p, encoding="utf-8"))
nodes = {str(n["id"]): n for n in wf["nodes"]}

# 1) Point the user's native node 31 at the correct source image
n31 = nodes["31"]
n31["widgets_values"] = ["jaisal_title_scene.png", "image"]

# 2) Rewire link 4: source FKI2I:img -> 31
for l in wf["links"]:
    if l[0] == 4:
        l[1] = "31"
        print("link 4 now:", l)

# 3) Update node 31 IMAGE output links to [4]
for o in n31["outputs"]:
    if o["name"] == "IMAGE":
        o["links"] = [4]
    if o["name"] == "MASK":
        o["links"] = []

# 4) Remove the redundant FKI2I:img node
wf["nodes"] = [n for n in wf["nodes"] if str(n["id"]) != "FKI2I:img"]
print("removed FKI2I:img; node count now:", len(wf["nodes"]))

# 5) Tidy node 31 position (place it where FKI2I:img was)
n31["pos"] = [1260, 0]
n31["size"] = [340, 180]

json.dump(wf, open(p, "w", encoding="utf-8"), indent=1)
print("saved.")

# Verify
wf2 = json.load(open(p, encoding="utf-8"))
print("\n=== VERIFY ===")
for n in wf2["nodes"]:
    if n["type"] == "LoadImage":
        print("LoadImage id:", n["id"], "widgets:", n["widgets_values"])
        for o in n["outputs"]:
            print("   output", o["name"], "links:", o["links"])
print("links:", [l for l in wf2["links"] if l[0] == 4])
