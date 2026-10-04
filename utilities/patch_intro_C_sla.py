# -*- coding: utf-8 -*-
"""
Patch jaisal_intro_C_headtwist_180.json (the camera-node shot) so it runs on OUR
stack instead of the shared template's missing pieces:

  1. Internal node 138  EastMoeSolAttn  ->  H3SLAAttention
     (EastMoeSolAttn comes from the uninstalled eastmoe/ComfyUI-Sol-Attn pack;
      H3SLAAttention is our proven SLA speed stack, already in every production wf)
  2. Internal node 121  LoraLoaderModelOnly
     minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors  (NOT installed)
       -> minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors (we HAVE this)

Both nodes live inside definitions.subgraphs[0].nodes (the subgraph instance is
top-level node 105). The model link wiring (270 in / 272 out) is unchanged.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "D:\\models\\vsCodeMcp\\utilities\\patch_intro_C_sla.py"
"""
import json, os

PATH = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json"

# H3SLAAttention widget order (from live /object_info, model is the link input):
#   sparsity_ratio, block_size, min_seq_len, dense_last_steps, protect_audio,
#   enabled, dense_steps, dense_backend, disable_fp16_accum, stabilize_motion,
#   reference_protection
SLA_WIDGETS = [0.9, "32", 8192, 1, True, True, "0", "comfy_kitchen", True, False, False]
SLA_NAMED = {
    "sparsity_ratio": 0.9, "block_size": "32", "min_seq_len": 8192,
    "dense_last_steps": 1, "protect_audio": True, "enabled": True,
    "dense_steps": "0", "dense_backend": "comfy_kitchen",
    "disable_fp16_accum": True, "stabilize_motion": False,
    "reference_protection": False,
}
NEW_LORA = "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"

def main():
    with open(PATH, "r", encoding="utf-8") as f:
        wf = json.load(f)
    sg = wf["definitions"]["subgraphs"][0]
    nodes = {n["id"]: n for n in sg["nodes"]}

    # 1. swap EastMoeSolAttn -> H3SLAAttention
    n138 = nodes[138]
    assert n138["type"] == "EastMoeSolAttn", "node 138 is not EastMoeSolAttn: " + n138["type"]
    n138["type"] = "H3SLAAttention"
    n138["widgets_values"] = list(SLA_WIDGETS)
    n138["widgets_values_named"] = dict(SLA_NAMED)
    if "properties" in n138:
        n138["properties"]["Node name for S&R"] = "H3SLAAttention"
    if "title" in n138:
        n138["title"] = "H3 SLA Attention"
    print("node 138 -> H3SLAAttention, widgets =", n138["widgets_values"])

    # 2. fix the LoRA filename
    n121 = nodes[121]
    assert n121["type"] == "LoraLoaderModelOnly", "node 121 is not LoraLoader: " + n121["type"]
    n121["widgets_values"][0] = NEW_LORA
    if "widgets_values_named" in n121:
        n121["widgets_values_named"]["lora_name"] = NEW_LORA
    print("node 121 lora ->", NEW_LORA)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, separators=(",", ":"))
    print("patched:", PATH)

if __name__ == "__main__":
    main()
