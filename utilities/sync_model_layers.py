#!/usr/bin/env python
"""Sync ALL widget layers (positional + named + instance) of the 4 sheet workflows to
the models actually on this machine (both copies). Muted LoRA (05d node 22) left alone.
09j: 451 named->bf16, 453 named->fp8_scaled, 459 instance widgets+named -> bare on-disk names.
05d/05e: named layers <- each node's own positional value (proven working values)."""
import json

BASES = [r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows",
         r"D:\models\vsCodeMcp\challenge\consistent-short\workflows"]

for base in BASES:
    # ---- 09j ----
    p = f"{base}\\09j_QWEN21_JAISAL_sheet.json"
    j = json.load(open(p, encoding="utf-8"))
    for sg in j["definitions"]["subgraphs"]:
        for n in sg["nodes"]:
            if n["id"] == 451:
                assert n["widgets_values"][0] == "qwen_image_2.1_bf16.safetensors", n["widgets_values"]
                n["widgets_values_named"]["unet_name"] = "qwen_image_2.1_bf16.safetensors"
            if n["id"] == 453:
                assert n["widgets_values"][0] == "qwen3vl_8b_fp8_scaled.safetensors", n["widgets_values"]
                n["widgets_values_named"]["clip_name"] = "qwen3vl_8b_fp8_scaled.safetensors"
            if n["id"] == 454:
                assert n["widgets_values"][0] == "qwen_image_2.1_vae_bf16.safetensors", n["widgets_values"]
                n["widgets_values_named"]["vae_name"] = "qwen_image_2.1_vae_bf16.safetensors"
    for n in j["nodes"]:
        if n["id"] == 459:
            assert n["widgets_values"][8] == "qwen/qwen_image_2.1_int8_convrot.safetensors", n["widgets_values"][8]
            assert n["widgets_values"][9] == "qwen/qwen3vl_8b_bf16.safetensors", n["widgets_values"][9]
            assert n["widgets_values"][10] == "qwen/qwen_image_2.1_vae_bf16.safetensors", n["widgets_values"][10]
            n["widgets_values"][8] = "qwen_image_2.1_bf16.safetensors"
            n["widgets_values"][9] = "qwen3vl_8b_fp8_scaled.safetensors"
            n["widgets_values"][10] = "qwen_image_2.1_vae_bf16.safetensors"
            n["widgets_values_named"]["unet_name"] = "qwen_image_2.1_bf16.safetensors"
            n["widgets_values_named"]["clip_name"] = "qwen3vl_8b_fp8_scaled.safetensors"
            n["widgets_values_named"]["vae_name"] = "qwen_image_2.1_vae_bf16.safetensors"
    json.dump(j, open(p, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    print("synced 09j", p)

    # ---- 05d / 05e: named layer <- positional layer (proven values) ----
    for f, loader_nodes in [("05d_charsheet_H3_wide_jaisal.json", {10: "unet_name", 11: "clip_name", 2: "vae_name", 3: "vae_name"}),
                            ("05e_charsheet_H3_fizgig_jaisal.json", {71: "unet_name", 72: "clip_name"})]:
        p = f"{base}\\{f}"
        j = json.load(open(p, encoding="utf-8"))
        for n in j["nodes"]:
            if n["id"] in loader_nodes:
                key = loader_nodes[n["id"]]
                pos0 = n["widgets_values"][0]
                old = n["widgets_values_named"].get(key)
                n["widgets_values_named"][key] = pos0
                print(f"  {f} node {n['id']} {key}: {old!r} -> {pos0!r}")
        json.dump(j, open(p, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        print("synced", p)
print("all synced")
