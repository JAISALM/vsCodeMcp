# -*- coding: utf-8 -*-
"""Drive the RUNNING Fizgig web app via its REST API (D170) to set up the
krea2chars_v3 dual-subject LoRA-Isolation training (2026-10-31, D209).

Why the API: the app holds its state in memory and re-saves it — editing
user_data\*.json while the app is running gets clobbered. The API is the
app's own state store, so the browser UI reflects it too.

Steps: token from the served page -> GET /api/state -> merge the krea2
family patch -> POST /api/state (model_values + image_folder + prep) ->
verify with a second GET.
"""
import json, re, urllib.request

BASE = "http://127.0.0.1:8081"

html = urllib.request.urlopen(BASE + "/", timeout=10).read().decode("utf-8", "replace")
m = re.search(r'name="fizgig-token"\s+content="([^"]+)"', html) or \
     re.search(r'content="([^"]+)"\s+name="fizgig-token"', html)
token = m.group(1) if m else ""
print("token found:", bool(token), "(%s)" % (token[:8] + "..." if token else "n/a"))
assert token, "no fizgig-token meta on the served page — is the app at 127.0.0.1:8081?"

def api(path, body=None):
    req = urllib.request.Request(BASE + path, headers={"X-Fizgig-Token": token})
    if body is not None:
        req.data = json.dumps(body).encode()
        req.headers["Content-Type"] = "application/json"
    return json.load(urllib.request.urlopen(req, timeout=30))

st = api("/api/state")
vals = st.get("values") or {}
k = dict(vals.get("krea2") or {})
print("before: image_folder=%s LORA_NAME=%s rank=%s ep=%s MP=%s subject2=%s" % (
    st.get("image_folder"), k.get("LORA_NAME"), k.get("NETWORK_DIM"),
    k.get("MAX_TRAIN_EPOCHS"), k.get("DATASET_MEGAPIXELS"), k.get("FAMILY_CONCEPT_DIR")))

PATCH = {
    "LORA_NAME": "krea2chars_v3",
    "NETWORK_DIM": 16,
    "NETWORK_ALPHA": 16,
    "MAX_TRAIN_EPOCHS": 20,
    "DATASET_MEGAPIXELS": "0.5",
    "SAVE_EVERY_N_EPOCHS": 1,
    "FAMILY_CONCEPT_DIR": r"D:\lora_training\zidane_3110",
    "SAMPLE_EVERY_N_EPOCHS": "2",
}
k.update(PATCH)
vals["krea2"] = k
st["values"] = vals

prep = dict(st.get("prep") or {})
prep["mp"] = "0.5"

res = api("/api/state", {
    "model_values": {"family": "krea2", "values": k},
    "family": "krea2",
    "image_folder": r"D:\lora_training\jaisal_3110",
    "prep": prep,
})
print("POST:", res)

st2 = api("/api/state")
v2 = (st2.get("values") or {}).get("krea2") or {}
print(json.dumps({
    "image_folder": st2.get("image_folder"),
    "LORA_NAME": v2.get("LORA_NAME"),
    "rank_alpha": "%s/%s" % (v2.get("NETWORK_DIM"), v2.get("NETWORK_ALPHA")),
    "epochs": v2.get("MAX_TRAIN_EPOCHS"),
    "MP": v2.get("DATASET_MEGAPIXELS"),
    "subject2": v2.get("FAMILY_CONCEPT_DIR"),
    "mode": v2.get("FAMILY_PEOPLE_MODE"),
    "DOP": v2.get("FAMILY_DOP"),
    "multi_person": v2.get("FAMILY_MULTI_PERSON"),
    "samples_q": v2.get("SAMPLE_EVERY_N_EPOCHS"),
    "prep": st2.get("prep"),
}, indent=1))
