#!/usr/bin/env python
"""Fix 09j node 549 (ThinkingLLM_QwenVL_GGUF_Advanced, subgraph-2 internal):
the author's file carried a 33-value widgets_values from a DIFFERENT pack version than the
installed v2.5.8 (29 widgets). Rebuild the array in the INSTALLED order (object_info
input_order), preserving the author's values where they map 1:1 and using installed
defaults where the author's value was a version artifact.

Installed order (v2.5.8):
[0] model_name  [1] device  [2] preset_prompt  [3] custom_prompt  [4] max_tokens
[5] temperature [6] top_p   [7] repetition_penalty [8] frame_count [9] ctx
[10] n_batch   [11] gpu_layers [12] image_max_tokens [13] top_k   [14] pool_size
[15] keep_model_loaded [16] seed [17] legacy_seed_mode [18] legacy_unload_after_run
[19] n_ubatch  [20] n_threads [21] n_threads_batch [22] flash_attn [23] offload_kqv
[24] ctx_checkpoints [25] stream_tokens_to_terminal [26] enable_thinking
[27] auto_finalization_retry [28] hf_token
"""
import json

PATHS = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\09j_QWEN21_JAISAL_sheet.json",
    r"D:\models\vsCodeMcp\challenge\consistent-short\workflows\09j_QWEN21_JAISAL_sheet.json",
]

NEW = [
    "[local] Qwen-Image-2.1-PE-I2I.Q4_K_M.gguf",  # model_name (author)
    "auto",                                        # device (author)
    "\U0001f4ac Custom prompt + image (no preset)",  # preset_prompt (author)
    "",                                            # custom_prompt (link 953 overrides at runtime)
    32768,                                         # max_tokens (author idx4)
    1,                                             # temperature (author idx5)
    0.9,                                           # top_p (author idx6; link 949 -> 0.95 at runtime)
    1,                                             # repetition_penalty (author idx7)
    10,                                            # frame_count (author idx8)
    32768,                                         # ctx (author idx9)
    512,                                           # n_batch (author idx10)
    26,                                            # gpu_layers (author idx11)
    4096,                                          # image_max_tokens (author idx12)
    20,                                            # top_k (author idx13)
    4194304,                                       # pool_size (author idx14)
    False,                                         # keep_model_loaded (author idx15)
    1,                                             # seed (author idx16)
    "fixed",                                       # legacy_seed_mode (author idx17)
    False,                                         # legacy_unload_after_run (installed default)
    512,                                           # n_ubatch (installed default)
    0,                                             # n_threads (auto; author's 512 exceeded max 256)
    0,                                             # n_threads_batch
    True,                                          # flash_attn
    True,                                          # offload_kqv
    0,                                             # ctx_checkpoints
    False,                                         # stream_tokens_to_terminal
    True,                                          # enable_thinking (author idx26)
    True,                                          # auto_finalization_retry (author idx27)
    "",                                            # hf_token
]

for path in PATHS:
    j = json.load(open(path, encoding="utf-8"))
    fixed = False
    for sg in j["definitions"]["subgraphs"]:
        for n in sg["nodes"]:
            if n["id"] == 549:
                assert n["type"] == "ThinkingLLM_QwenVL_GGUF_Advanced", n["type"]
                old = n["widgets_values"]
                n["widgets_values"] = list(NEW)
                n.pop("widgets_values_named", None)  # native UI files carry no named dict;
                # the converter then maps positional widgets_values cleanly
                print(f"549 widgets: {len(old)} -> {len(NEW)} values ({path.split(chr(92))[-1]})")
                fixed = True
        if fixed:
            break
    assert fixed, "node 549 not found"
    json.dump(j, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("saved", path)
print("DONE")
