# Build a VDN-H3 text-to-video benchmark workflow from the pack's example.
# Adapts vdn_h3_t2v_8step.json to OUR models + 1MP (1344x768) + NO-music prompt.
#
# Chain: UNETLoader -> ApplyVDNH3Advanced -> MiniMaxChunkFeedForward -> BasicGuider -> SamplerCustomAdvanced
#        (BasicScheduler also takes the model from MiniMaxChunkFeedForward)
#        MiniMaxH3ImageToVideo (t2v mode, no frames) -> VAEDecode/VAEDecodeAudio -> CreateVideo -> SaveVideo
#
# Run: & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\build_vdn_t2v.py"

import io, json, shutil, os

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\ComfyUI-VDN-H3\example_workflows\vdn_h3_t2v_8step.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\vdn_h3_t2v_benchmark.json"

# Our actual model files (verified present)
UNET   = "minimax_h3_fl2va_pruned_int8_convrot.safetensors"
CLIP   = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
V_VAE  = "minimax_h3_video_vae_fp16.safetensors"
A_VAE  = "minimax_h3_audio_vae_fp32.safetensors"
CKPT   = "vdn-minimax-h3-int8-convrot-comfyui"

# 1MP (matches our SLA baseline), 124 frames (17*7+5 grid), 8 steps
W, H, LEN = 1344, 768, 124

PROMPT = (
    "integrated_multimodal_description: [Shot 1] A young schoolboy with short dark hair, "
    "wearing a rose-pink collared shirt and black trousers, walks slowly along a long straight "
    "stone bridge over a wide open river. The sky is dark and moody, heavy overcast post-rain "
    "clouds, dim diffused light. Light rain begins to fall. The camera is a static eye-level "
    "medium shot, deep focus, the boy a small figure on the bridge.\n\n"
    "overall_soundscape: Soft footsteps on the wet stone bridge, gentle continuous wind, soft "
    "flowing river water, a few birds chirping in the distance.\n\n"
    "non_diegetic_music: NO music, NO instrumental music, NO musical instruments, NO melody, "
    "NO beat, NO rhythm, NO soundtrack, NO song. Natural ambient sounds only."
)

d = json.load(io.open(SRC, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}

# 1. UNETLoader (node 1) -> our pruned int8 base
nodes[1]["widgets_values"] = [UNET, "default"]
nodes[1]["widgets_values_named"] = {"unet_name": UNET, "weight_dtype": "default"}

# 2. VAELoader video (node 4) -> our fp16 video VAE
nodes[4]["widgets_values"] = [V_VAE]
nodes[4]["widgets_values_named"] = {"vae_name": V_VAE}

# 3. VAELoader audio (node 5) -> our audio VAE (already correct, set explicitly)
nodes[5]["widgets_values"] = [A_VAE]
nodes[5]["widgets_values_named"] = {"vae_name": A_VAE}

# 4. CLIPLoader (node 2) -> our CLIP (already correct, set explicitly)
nodes[2]["widgets_values"] = [CLIP, "minimax", "default"]
nodes[2]["widgets_values_named"] = {"clip_name": CLIP, "type": "minimax", "device": "default"}

# 5. ApplyVDNH3Advanced (node 32) -> our checkpoint, turbo ON, merge, grouped, fast_kernels OFF
#    (fast_kernels OFF: README warns it drifts on 8-step DMD stages)
#    widget order: vdn_checkpoint, apply_turbo_adapter, stage_b_strength, turbo_strength,
#                  lora_mode, branch_weights, retain_buffers, verbose, attention_backend,
#                  window_radius, window_chunk, anchor_frames, text_state, linear_branch, fast_kernels
nodes[32]["widgets_values"] = [CKPT, True, 1, 1, "merge", "auto", "auto", True, "grouped", 1, 5, "both", True, True, False]
nodes[32]["widgets_values_named"] = {
    "vdn_checkpoint": CKPT, "apply_turbo_adapter": True, "stage_b_strength": 1, "turbo_strength": 1,
    "lora_mode": "merge", "branch_weights": "auto", "retain_buffers": "auto", "verbose": True,
    "attention_backend": "grouped", "window_radius": 1, "window_chunk": 5, "anchor_frames": "both",
    "text_state": True, "linear_branch": True, "fast_kernels": False,
}

# 6. MiniMaxH3ImageToVideo (node 6) -> 1MP + our NO-music t2v prompt, no frames (t2v mode)
nodes[6]["widgets_values"] = [PROMPT, W, H, LEN]
nodes[6]["widgets_values_named"] = {"prompt": PROMPT, "width": W, "height": H, "length": LEN}

# 7. SaveVideo (node 16) -> our prefix
nodes[16]["widgets_values"] = ["vdn_h3_bench", "auto", "auto", "auto"]
nodes[16]["widgets_values_named"] = {"filename_prefix": "vdn_h3_bench", "format": "auto", "format.codec": "auto", "codec": "auto"}

# 8. Drop ModelPreviewOverrideKJ (node 17) to avoid the taeh3 preview-VAE dependency.
#    Rewire link 38 (was 17->11) to come from node 27 (MiniMaxChunkFeedForward) instead,
#    and remove link 75 (27->17).
links = d["links"]
new_links = []
for l in links:
    if l[0] == 38:
        new_links.append([38, 27, 0, 11, 0, "MODEL"])   # 27 -> 11 (BasicGuider)
    elif l[0] == 75:
        continue                                          # drop 27 -> 17
    else:
        new_links.append(l)
d["links"] = new_links
nodes[27]["outputs"][0]["links"] = [38, 76]              # node 27 now feeds 38 (guider) + 76 (scheduler)
d["nodes"] = [n for n in d["nodes"] if n["id"] != 17]

# Backup any existing target, then write
if os.path.exists(DST):
    shutil.copy(DST, DST + ".bak")
with io.open(DST, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("WROTE", DST)
print("nodes:", len(d["nodes"]), "links:", len(d["links"]))
print("chain: UNET(1) -> ApplyVDNH3Advanced(32) -> MiniMaxChunkFeedForward(27) -> BasicGuider(11) -> SamplerCustomAdvanced(12)")
print("res:", W, "x", H, "frames:", LEN, "ckpt:", CKPT)
