import json

P = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\minimax_h3_boar_grave_talking_r2v.json'
wf = json.load(open(P, encoding='utf-8'))
nodes = {n['id']: n for n in wf['nodes']}

# node -> (new name, named-key)
FIX = {
    127: ("minimax_h3_fl2va_pruned_int8_convrot.safetensors", "unet_name"),
    214: ("minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors", "lora_name"),
    119: ("minimax_h3_video_vae_fp16.safetensors", "vae_name"),
    120: ("minimax_h3_audio_vae_fp32.safetensors", "vae_name"),
    128: ("qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "clip_name"),
    223: ("minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors", "lora_name"),
}

for nid, (new_name, key) in FIX.items():
    n = nodes[nid]
    print(nid, n['type'], 'before:', json.dumps(n.get('widgets_values'))[:120])
    # positional: first widget is the model name
    n['widgets_values'][0] = new_name
    if 'widgets_values_named' in n and key in n['widgets_values_named']:
        n['widgets_values_named'][key] = new_name
    print('   after :', json.dumps(n.get('widgets_values'))[:120])

with open(P, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False)
print('saved', P)
