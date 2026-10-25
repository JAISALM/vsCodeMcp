"""Dump the key canvas nodes of the obvpm timeline workflow for setup inspection."""
import json, sys

p = r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\04_h3_timeline_r2v.json"
j = json.load(open(p, encoding="utf-8"))
keep = {"LoadImage", "LoadImages", "LoadAudio", "MiniMaxH3Timeline", "H3Timeline",
        "CLIPTextEncode", "MiniMaxH3ReferenceToVideo", "SaveVideo", "VHS_VideoCombine",
        "H3ContextWindows", "ResolutionSelector", "Text", "Note",
        "PrimitiveInt", "PrimitiveFloat", "PrimitiveString", "PrimitiveStringMultiline",
        "PrimitiveCombo", "KSamplerSelect", "BasicScheduler", "SamplerCustomAdvanced"}
for n in j["nodes"]:
    if n["type"] and len(n["type"]) > 30:
        continue
    if n["type"] in keep:
        w = n.get("widgets_values")
        ws = str(w)[:140] if w is not None else ""
        print(f"{n['id']} [{n['type']}] mode={n.get('mode',0)} w={ws}")
        for inp in n.get("inputs", []):
            print(f"    in: {inp['name']} ({inp['type']}) link={inp.get('link')}")
        for out in n.get("outputs", []):
            print(f"    out: {out['name']} ({out['type']}) links={out.get('links')}")
