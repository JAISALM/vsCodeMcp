r"""Dump exact widget order for the SeedVR2 image workflow nodes.

Writes ordered input lists (widget inputs first, then link inputs) to a file so
the workflow builder can set widgets_values in the correct positional order.
"""
import urllib.request, json

r = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=30))
out = open(r"d:\models\vsCodeMcp\data\seedvr_schema.txt", "w")

for name in ["SeedVR2LoadDiTModel", "SeedVR2LoadVAEModel", "SeedVR2VideoUpscaler", "LoadImage", "SaveImage"]:
    if name not in r:
        out.write("== %s MISSING ==\n" % name)
        continue
    info = r[name]
    out.write("== %s ==\n" % name)
    out.write("INPUTS (ordered, required then optional):\n")
    inp = info.get("input", {})
    for section in ["required", "optional"]:
        for k, v in inp.get(section, {}).items():
            if isinstance(v, list):
                opts = v
                if len(opts) > 8:
                    opts = opts[:4] + ["...%d total" % len(v)]
                out.write("  %-24s %s\n" % (k, opts))
            else:
                out.write("  %-24s %s\n" % (k, v))
    outo = info.get("output", {})
    if isinstance(outo, dict):
        out.write("OUTPUTS: %s\n\n" % list(outo.keys()))
    else:
        out.write("OUTPUTS: %s\n\n" % outo)
out.close()
print(open(r"d:\models\vsCodeMcp\data\seedvr_schema.txt").read())
