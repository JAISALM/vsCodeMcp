"""Insert the MiniMax H3 Semantic Bridge (SenseNovaH3DistilledBridge) onto the
conditioning path of jaisal_single_shot.json (the SLA i2v workflow).

The i2v node (internal node 104, MiniMaxH3ImageToVideo) is inside a subgraph.
Its `positive` (CONDITIONING) output (link 187) feeds the BasicGuider (node 16)
entirely INSIDE the subgraph. We insert a standalone bridge node (id 300) on that
conditioning path:

    node 104 (positive) --[link 187]--> node 300 (SenseNovaH3DistilledBridge)
    node 300 (conditioning out) --[link 301]--> node 16 (BasicGuider conditioning)

This preserves the native i2v node, the SLA node (150), the turbo LoRA (121), and
all model/prompt settings. The bridge only transforms the CONDITIONING (orthogonal
to SLA's model path), so they coexist.

Idempotent: if node 300 already exists, it reports and exits without changes.
"""
import io
import json
import os
import shutil
import sys

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
BACKUP_DIR = r"d:\models\vsCodeMcp\workflow_backups"
BRIDGE_NODE_ID = 300
BRIDGE_LINK_ID = 301
COND_LINK_ID = 187          # existing 104 -> 16 conditioning link
I2V_NODE_ID = 104          # MiniMaxH3ImageToVideo (positive output)
GUIDER_NODE_ID = 16        # BasicGuider (conditioning input)
ADAPTER = "MiniMaxH3_SemanticBridge_v1.safetensors"
ALPHA = 0.10               # recommended starting point (0.15 = stronger, per A/B)
MAGNITUDE = "per_token"    # recommended mode


def main():
    # 1. Back up
    os.makedirs(BACKUP_DIR, exist_ok=True)
    bak = os.path.join(BACKUP_DIR, "jaisal_single_shot.pre_semantic_bridge.json")
    shutil.copy2(WF, bak)
    print("backed up ->", bak)

    with io.open(WF, encoding="utf-8") as f:
        d = json.load(f)

    sg = d["definitions"]["subgraphs"][0]
    nodes = sg["nodes"]
    links = sg["links"]

    # Idempotency check
    if any(n["id"] == BRIDGE_NODE_ID for n in nodes):
        print("bridge node 300 already present; no changes made.")
        return

    # Sanity: confirm the conditioning link we expect
    cond = next((L for L in links if L["id"] == COND_LINK_ID), None)
    assert cond is not None, "conditioning link 187 not found"
    assert cond["origin_id"] == I2V_NODE_ID and cond["target_id"] == GUIDER_NODE_ID, \
        f"unexpected conditioning link: {cond}"

    # 2. Reroute link 187: 104 -> 300 (bridge conditioning input, slot 0)
    cond["target_id"] = BRIDGE_NODE_ID
    cond["target_slot"] = 0

    # 3. Add new link 301: 300 -> 16 (bridge conditioning output -> BasicGuider)
    links.append({
        "id": BRIDGE_LINK_ID,
        "origin_id": BRIDGE_NODE_ID,
        "origin_slot": 0,
        "target_id": GUIDER_NODE_ID,
        "target_slot": 1,
        "type": "CONDITIONING",
    })

    # 4. Update node 16 (BasicGuider) conditioning input link: 187 -> 301
    guider = next(n for n in nodes if n["id"] == GUIDER_NODE_ID)
    for inp in guider["inputs"]:
        if inp["name"] == "conditioning":
            inp["link"] = BRIDGE_LINK_ID

    # 5. Add the bridge node (internal to the subgraph)
    bridge = {
        "id": BRIDGE_NODE_ID,
        "type": "SenseNovaH3DistilledBridge",
        "pos": [-650, 4740],
        "size": [360, 120],
        "flags": {},
        "order": 12,
        "mode": 0,
        "inputs": [
            {
                "localized_name": "conditioning",
                "name": "conditioning",
                "type": "CONDITIONING",
                "link": COND_LINK_ID,
            }
        ],
        "outputs": [
            {
                "localized_name": "conditioning",
                "name": "conditioning",
                "type": "CONDITIONING",
                "links": [BRIDGE_LINK_ID],
            }
        ],
        "properties": {
            "Node name for S&R": "SenseNovaH3DistilledBridge",
            "cnr_id": "minimax-h3-semantic-bridge",
            "ver": "1.0.0",
        },
        "widgets_values": [ADAPTER, ALPHA, MAGNITUDE],
        "widgets_values_named": {
            "distilled_adapter": ADAPTER,
            "alpha": ALPHA,
            "magnitude_match": MAGNITUDE,
        },
        "color": "#2a363b",
        "bgcolor": "#3f5159",
    }
    nodes.append(bridge)

    # 6. Save
    with io.open(WF, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print("inserted bridge node 300 on the conditioning path (104 -> 300 -> 16).")
    print(f"bridge widgets: adapter={ADAPTER}, alpha={ALPHA}, magnitude_match={MAGNITUDE}")
    print("saved ->", WF)


if __name__ == "__main__":
    main()
