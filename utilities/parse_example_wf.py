r"""Parse the numz example image workflow to extract native widget shapes."""
import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\seedvr2_videoupscaler\example_workflows\SeedVR2_simple_image_upscale.json"
d = json.load(open(p, encoding="utf-8"))
out = open(r"d:\models\vsCodeMcp\data\example_wf.txt", "w")
out.write("TOP KEYS: %s\n\n" % list(d.keys()))
for n in d["nodes"]:
    out.write("NODE id=%s type=%s mode=%s\n" % (n["id"], n["type"], n.get("mode")))
    out.write("  widgets_values: %s\n" % json.dumps(n.get("widgets_values")))
    out.write("  inputs: %s\n" % json.dumps([(i["name"], i["type"], i.get("link")) for i in n.get("inputs", [])]))
    out.write("  outputs: %s\n\n" % json.dumps([(o["name"], o["type"], o.get("links")) for o in n.get("outputs", [])]))
out.write("LINKS:\n")
for l in d.get("links", []):
    out.write("  link id=%s from_node=%s from_slot=%s to_node=%s to_slot=%s\n" % (l[0], l[1], l[2], l[3], l[4]))
out.close()
print(open(r"d:\models\vsCodeMcp\data\example_wf.txt").read())
