# verify_pe_conversion.py — run the real comfy_cli UI->API converter on the PE
# workflows and print the resulting API prompt for the TextGenerate + CLIPTextEncode
# nodes, proving the sampling_mode dict (with seed) survives conversion.
import json
import sys
import urllib.request

import comfy_cli.workflow_to_api as w2a

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
API = "http://127.0.0.1:8188/object_info/{}"

for name in (sys.argv[1:] or ["krea2_t2i_char1_pe.json"]):
    wf = json.load(open(f"{WF_DIR}\\{name}", encoding="utf-8"))
    types = sorted({n["type"] for n in wf["nodes"]})
    object_info = {}
    for t in types:
        raw = urllib.request.urlopen(API.format(t), timeout=15).read().decode("utf-8")
        object_info[t] = json.loads(raw)
    api = w2a.convert_ui_to_api(wf, object_info)
    print("===", name, "===")
    for nid, spec in sorted(api.items(), key=lambda kv: int(kv[0])):
        cls = spec["class_type"]
        if cls in ("TextGenerate", "CLIPTextEncode", "KSampler"):
            print(f"node {nid} [{cls}]:")
            print("  ", json.dumps(spec["inputs"], ensure_ascii=False)[:900])
