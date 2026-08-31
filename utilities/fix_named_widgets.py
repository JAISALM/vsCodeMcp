import json

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_drone_optimized.json"
wf = json.load(open(P, encoding="utf-8"))
nodes = {x["id"]: x for x in wf["nodes"]}

# --- Node 136 MiniMaxH3ReferenceToVideo: width/height/length ---
n = nodes[136]
n["widgets_values_named"] = {
    "prompt": "",
    "width": 864,
    "height": 480,
    "length": 362,
    "ref_image_size": "match",
}

# --- Node 127 UNETLoader: fl2va ---
n = nodes[127]
n["widgets_values_named"] = {
    "unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
    "weight_dtype": "default",
}
# also fix stale properties.models metadata
n["properties"]["models"] = [{
    "name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
    "url": "https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors",
    "directory": "diffusion_models",
}]

# --- Node 146 LoraLoaderModelOnly: fl2v turbo 4step ---
n = nodes[146]
n["widgets_values_named"] = {
    "lora_name": "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors",
    "strength_model": 1,
}

# --- Node 137 LoadImage: start frame ---
n = nodes[137]
n["widgets_values_named"] = {"image": "jaisal_mm_start.png", "upload": "image"}

# --- Node 139 LoadImage: final frame ---
n = nodes[139]
n["widgets_values_named"] = {"image": "jaisal_mm_final.png", "upload": "image"}

# --- Node 138 PrimitiveStringMultiline: drone prompt ---
n = nodes[138]
drone_prompt = (
    "Cinematic aerial drone shot over a Kerala backwater river, an angular 3d art style with brush stroke color texture. "
    "A single young Indian schoolboy, around ten years old, in a neat school uniform with a red school bag, drenched and wet from the rain, "
    "stands in the center of a single long traditional stone bridge over a single wide river. "
    "The camera starts at a medium high angle above the boy, who looks up at the camera. "
    "Then the camera rises smoothly and continuously straight upward, like a drone ascending, gradually revealing the full length of the bridge, "
    "the wide river on both sides, and the surrounding environment. The boy becomes smaller and smaller until he is a tiny dot in the center of the bridge. "
    "Water droplets fall from the boy. Moody overcast sky. "
    "ONE single smooth continuous upward camera movement, no panning sideways, no camera tilt, no cuts, no new characters appearing, exactly one boy the entire time. "
    "The same angular 3d brush-stroke artstyle throughout. "
    "Audio: soft rain ambience, gentle river water, light wind."
)
n["widgets_values_named"] = {"value": drone_prompt}

# --- Node 92 SaveVideo: prefix ---
n = nodes[92]
n["widgets_values_named"] = {"filename_prefix": "video/Jaisal_Drone", "format": "auto", "codec": "auto"}

json.dump(wf, open(P, "w", encoding="utf-8"), indent=1)
print("fixed widgets_values_named for nodes 136,127,146,137,139,138,92")
# verify
for nid in (136, 127, 146, 137, 139, 92):
    print(f"  id={nid} {nodes[nid]['type']} named={nodes[nid].get('widgets_values_named')}")
