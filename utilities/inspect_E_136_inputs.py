import json
base = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
f = "jaisal_intro_E_plants.json"
wf = json.load(open(base + "\\" + f, encoding="utf-8"))
n136 = [n for n in wf["nodes"] if n["id"] == 136][0]
print("136 inputs:")
for i, inp in enumerate(n136["inputs"]):
    print("  slot", i, "name=", inp.get("name"), "type=", inp.get("type"), "link=", inp.get("link"))
print()
print("139 outputs:", n139_out := [n for n in wf["nodes"] if n["id"] == 139][0]["outputs"])
print()
print("max link id:", max(l[0] for l in wf["links"]))
print("last_link_id:", wf.get("last_link_id"))
print()
print("all links:")
for l in wf["links"]:
    print("  ", l)
