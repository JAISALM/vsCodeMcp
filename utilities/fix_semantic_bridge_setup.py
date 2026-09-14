"""Fix the Semantic Bridge setup:
1. Restore the working jaisal_single_shot.json from the clean backup.
2. Create a SEPARATE jaisal_single_shot_semantic.json (copy of the clean backup).
3. Copy the adapter into the RUNNING ComfyUI's models dir (comfyUi_latest).
4. Insert the bridge node onto the conditioning path of the NEW semantic workflow.
"""
import io
import json
import os
import shutil

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
ORIG = os.path.join(WF_DIR, "jaisal_single_shot.json")
NEW = os.path.join(WF_DIR, "jaisal_single_shot_semantic.json")
BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_single_shot.pre_semantic_bridge.json"

ADAPTER = "MiniMaxH3_SemanticBridge_v1.safetensors"
ALPHA = 0.10
MAGNITUDE = "per_token"
BRIDGE_NODE_ID = 300
BRIDGE_LINK_ID = 301
COND_LINK_ID = 187
I2V_NODE_ID = 104
GUIDER_NODE_ID = 16

# 1. Restore the working original
shutil.copy2(BAK, ORIG)
print("1. restored working original ->", ORIG)

# 2. Create the new semantic workflow from the SAME clean backup
shutil.copy2(BAK, NEW)
print("2. created new semantic workflow ->", NEW)

# 3. Copy the adapter into the RUNNING ComfyUI's models dir (comfyUi_latest)
ad_dir = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\models\semantic_bridge"
os.makedirs(ad_dir, exist_ok=True)
src = os.path.join(r"E:\ComfyUI_windows_portable\ComfyUI\models\semantic_bridge", ADAPTER)
dst = os.path.join(ad_dir, ADAPTER)
shutil.copy2(src, dst)
print("3. adapter copied to running instance ->", dst, os.path.getsize(dst), "bytes")

# 4. Insert the bridge node onto the conditioning path of the NEW workflow
with io.open(NEW, encoding="utf-8") as f:
    d = json.load(f)
sg = d["definitions"]["subgraphs"][0]
nodes = sg["nodes"]
links = sg["links"]

if any(n["id"] == BRIDGE_NODE_ID for n in nodes):
    print("4. bridge node already present in new workflow; skipping insertion.")
else:
    cond = next((L for L in links if L["id"] == COND_LINK_ID), None)
    assert cond is not None and cond["origin_id"] == I2V_NODE_ID and cond["target_id"] == GUIDER_NODE_ID, \
        f"unexpected conditioning link: {cond}"
    # reroute 187: 104 -> 300
    cond["target_id"] = BRIDGE_NODE_ID
    cond["target_slot"] = 0
    # new link 301: 300 -> 16
    links.append({"id": BRIDGE_LINK_ID, "origin_id": BRIDGE_NODE_ID, "origin_slot": 0,
                  "target_id": GUIDER_NODE_ID, "target_slot": 1, "type": "CONDITIONING"})
    # node 16 conditioning input -> 301
    guider = next(n for n in nodes if n["id"] == GUIDER_NODE_ID)
    for inp in guider["inputs"]:
        if inp["name"] == "conditioning":
            inp["link"] = BRIDGE_LINK_ID
    # add bridge node
    nodes.append({
        "id": BRIDGE_NODE_ID, "type": "SenseNovaH3DistilledBridge",
        "pos": [-650, 4740], "size": [360, 120], "flags": {}, "order": 12, "mode": 0,
        "inputs": [{"localized_name": "conditioning", "name": "conditioning",
                    "type": "CONDITIONING", "link": COND_LINK_ID}],
        "outputs": [{"localized_name": "conditioning", "name": "conditioning",
                     "type": "CONDITIONING", "links": [BRIDGE_LINK_ID]}],
        "properties": {"Node name for S&R": "SenseNovaH3DistilledBridge",
                       "cnr_id": "minimax-h3-semantic-bridge", "ver": "1.0.0"},
        "widgets_values": [ADAPTER, ALPHA, MAGNITUDE],
        "widgets_values_named": {"distilled_adapter": ADAPTER, "alpha": ALPHA,
                                 "magnitude_match": MAGNITUDE},
        "color": "#2a363b", "bgcolor": "#3f5159",
    })
    with io.open(NEW, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print("4. inserted bridge node 300 into the NEW semantic workflow (104 -> 300 -> 16).")

print("done.")
