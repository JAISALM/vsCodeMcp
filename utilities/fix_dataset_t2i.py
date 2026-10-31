# -*- coding: utf-8 -*-
"""fix_dataset_t2i.py (2026-10-31)

Root cause of the 'fluke dataset' (11 identical outputs): the KSampler base
latent was the reference's OWN VAEEncode (link 73 -> KSampler slot 3) at
denoise 0.4 => every generation = 60% the reference composition
(frontal close-up, gray background) + seed noise. Prompt setting lines had
almost no power. All outputs looked like the reference shot.

Fix: t2i architecture —
  * new node 201 EmptyLatentImage (1024x1024, batch 1) -> KSampler latent
  * KSampler denoise 0.4 -> 1.0 (full prompt control of setting/pose)
  * reference identity path UNCHANGED: patch source_latent (73) +
    source_latent_b (92) + grounded encodes + identity-edit LoRA.

Applies to lora_dataset_jaisal.json + lora_dataset_zidhan.json.
Backs up originals as *.pre_t2i.bak. Idempotent (skips if node 201 exists).
"""
import json, shutil, sys

W = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

for name in ("jaisal", "zidhan"):
    p = W + "\\lora_dataset_%s.json" % name
    shutil.copyfile(p, p + ".pre_t2i.bak")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)

    # 1) rewire KSampler latent (to_node=53 slot=3 LATENT) from VAEEncode 73 -> new 201
    fixed = False
    for l in d["links"]:
        arr = l if isinstance(l, list) else l.get("value")
        if arr[3] == 53 and arr[4] == 3 and arr[5] == "LATENT":
            if arr[1] != 73:
                print("WARN %s: KSampler latent source is %s (expected 73) — rewiring anyway" % (name, arr[1]))
            if isinstance(l, list):
                l[1] = 201
            else:
                l["value"][1] = 201
            fixed = True
            print("%s: KSampler latent now <- node 201 (was %s)" % (name, 73))
    if not fixed:
        print("ERROR %s: KSampler latent link not found" % name); sys.exit(1)

    # 2) KSampler denoise -> 1.0 (widgets: [seed, control, steps, cfg, sampler, scheduler, denoise])
    for n in d["nodes"]:
        if n["id"] == 53:
            n["widgets_values"][6] = 1.0
            print("%s: KSampler denoise -> 1.0" % name)

    # 3) add EmptyLatentImage node 201 (native shape: no inputs, widgets [w,h,batch])
    if any(n["id"] == 201 for n in d["nodes"]):
        print("%s: node 201 already present — skipping add" % name)
    else:
        d["nodes"].append({
            "id": 201, "type": "EmptyLatentImage",
            "pos": [560.0, 420.0], "size": [220.0, 90.0],
            "flags": {}, "order": 1, "mode": 0,
            "inputs": [],
            "outputs": [{"localized_name": "LATENT", "name": "LATENT", "type": "LATENT", "links": [22]}],
            "properties": {"Node name for S&R": "EmptyLatentImage"},
            "widgets_values": [1024, 1024, 1]
        })
        print("%s: added node 201 EmptyLatentImage 1024x1024" % name)

    d["last_node_id"] = max(d["last_node_id"], 201)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print("%s: saved (last_node_id=%s)" % (name, d["last_node_id"]))

print("DONE")
