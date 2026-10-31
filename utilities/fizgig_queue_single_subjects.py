# -*- coding: utf-8 -*-
"""Queue two SINGLE-SUBJECT Krea2 LoRA runs in the running Fizgig app (D170 API).

Why single-subject (user call, 2026-11-01): the dual-subject v3 run came out
weak (generic faces, triggers worked but identity diluted). Separate LoRAs =
each face gets the full network capacity, no merge mechanism at all. In
ComfyUI both LoRAs chain for two-character shots.

Settings = the OLD run's PROVEN face-quality config (krea2fp_V2's rank 32 @
1.0 MP produced 0.45-0.55 likeness) but only 15 epochs each (the v3 loss
peaked mid-run and rose at e20; every epoch is saved so we pick the best).
DOP mode "Leave the rest of the model alone" = stranger-safe single subject.
"""
import json, re, urllib.request

BASE = "http://127.0.0.1:8081"
html = urllib.request.urlopen(BASE + "/", timeout=10).read().decode("utf-8", "replace")
m = re.search(r'name="fizgig-token"\s+content="([^"]+)"', html) or \
    re.search(r'content="([^"]+)"\s+name="fizgig-token"', html)
token = m.group(1)
assert token, "no token"

def api(path, body=None):
    req = urllib.request.Request(BASE + path, headers={"X-Fizgig-Token": token})
    if body is not None:
        req.data = json.dumps(body).encode()
        req.headers["Content-Type"] = "application/json"
    return json.load(urllib.request.urlopen(req, timeout=60))

st = api("/api/state")
base_vals = dict((st.get("values") or {}).get("krea2") or {})
print("base krea2 values loaded: %d fields" % len(base_vals))

RUNS = [
    {"image_folder": r"D:\lora_training\jaisal_3110", "name": "krea2jaisal_v1",
     "sample": "jeskvman"},
    {"image_folder": r"D:\lora_training\zidane_3110", "name": "krea2zidhan_v1",
     "sample": "dloroman"},
]

for r in RUNS:
    vals = dict(base_vals)
    vals.update({
        "LORA_NAME": r["name"],
        "NETWORK_DIM": 32,
        "NETWORK_ALPHA": 32,
        "DATASET_MEGAPIXELS": "1.0",
        "MAX_TRAIN_EPOCHS": 15,
        "SAVE_EVERY_N_EPOCHS": 1,
        "FAMILY_SUBJECTS": "1 subject",
        "FAMILY_CONCEPT_COUNT": "1 subject",
        "FAMILY_MULTICONCEPT": False,
        "FAMILY_PEOPLE_MODE": "Leave the rest of the model alone",   # DOP on, multi off
        "FAMILY_DOP": True,
        "FAMILY_MULTI_PERSON": False,
        "FAMILY_CONCEPT_DIR": "",
        "SAMPLE_ENABLED": True,
        "SAMPLE_EVERY_N_EPOCHS": "1",
        "SAMPLE_PROMPT": r["sample"],
    })
    res = api("/api/queue/add", {
        "family": "krea2",
        "values": vals,
        "image_folder": r["image_folder"],
    })
    print(r["name"], "->", res)
    if res.get("problems") or res.get("error"):
        print("ABORTING second run on problem/error")
        break

q = api("/api/runs")
items = q if isinstance(q, list) else (q.get("runs") or q.get("items") or [q])
for i in items[:4]:
    print("run:", json.dumps(i)[:400])
