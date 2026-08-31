import json, copy

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\video_minimax_h3_r2v+turbo.json"
DST = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_drone_optimized.json"

wf = json.load(open(SRC, encoding="utf-8"))
nodes = {x["id"]: x for x in wf["nodes"]}
links = wf["links"]

def find_link(lid):
    for l in links:
        if l[0] == lid:
            return l
    return None

# ---------- 1. UNET -> fl2va (first-last frame model for drone ascent) ----------
nodes[127]["widgets_values"] = ["minimax_h3_fl2va_pruned_int8_convrot.safetensors", "default"]

# ---------- 2. LoRA -> turbo 4-step ----------
nodes[146]["widgets_values"] = ["minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors", 1]

# ---------- 3. Insert Star7 node (Comfy Kitchen INT8 attention + chunking) ----------
star7 = {
    "id": 200,
    "type": "MiniMaxH3ActivationChunkStar7",
    "mode": 0,
    "pos": [400, 200],
    "size": [320, 260],
    "inputs": [
        {"name": "model", "type": "MODEL", "link": 300},
        {"name": "chunk_tokens", "type": "INT", "widget": {"name": "chunk_tokens"}, "link": None},
        {"name": "auto_halve_on_oom", "type": "BOOLEAN", "widget": {"name": "auto_halve_on_oom"}, "link": None},
        {"name": "verbose", "type": "BOOLEAN", "widget": {"name": "verbose"}, "link": None},
        {"name": "mlp_chunk_tokens", "type": "INT", "widget": {"name": "mlp_chunk_tokens"}, "link": None},
        {"name": "disable_dynamic_prefetch", "type": "STRING", "widget": {"name": "disable_dynamic_prefetch"}, "link": None},
        {"name": "qkv_chunk_tokens", "type": "INT", "widget": {"name": "qkv_chunk_tokens"}, "link": None},
        {"name": "reuse_mlp_weights", "type": "BOOLEAN", "widget": {"name": "reuse_mlp_weights"}, "link": None},
        {"name": "attention_backend", "type": "COMBO", "widget": {"name": "attention_backend"}, "link": None},
    ],
    "outputs": [{"name": "model", "type": "MODEL", "links": [301, 302]}],
    "widgets_values": [8192, True, True, 8192, "experimental-removed", 4096, True, "comfy_kitchen_int8"],
}
wf["nodes"].append(star7)
nodes[200] = star7

# ---------- 4. Rewire model chain: LoRA(146) -> Star7(200) -> Scheduler(124)+Guider(126) ----------
# Remove old links 287 (LoRA->Scheduler) and 288 (LoRA->Guider)
wf["links"] = [l for l in wf["links"] if l[0] not in (287, 288)]
# LoRA(146) outputs -> only link 300 now
nodes[146]["outputs"][0]["links"] = [300]
# New links
wf["links"].append([300, 146, 0, 200, 0, "MODEL"])   # LoRA -> Star7
wf["links"].append([301, 200, 0, 124, 0, "MODEL"])   # Star7 -> Scheduler
wf["links"].append([302, 200, 0, 126, 0, "MODEL"])   # Star7 -> Guider
# Scheduler(124) model input -> 301
for inp in nodes[124]["inputs"]:
    if inp["name"] == "model":
        inp["link"] = 301
# Guider(126) model input -> 302
for inp in nodes[126]["inputs"]:
    if inp["name"] == "model":
        inp["link"] = 302

# ---------- 5. Ref images -> jaisal start + final ----------
nodes[137]["widgets_values"] = ["jaisal_mm_start.png", "image"]   # ref_image_0 (first frame)
nodes[139]["widgets_values"] = ["jaisal_mm_final.png", "image"]   # ref_image_1 (last frame)
# Remove ref_image_2 (node 143) and its link
for inp in nodes[136]["inputs"]:
    if inp["name"] == "ref_images.ref_image_2":
        inp["link"] = None
wf["nodes"] = [x for x in wf["nodes"] if x["id"] != 143]
# remove link 285 (143 -> MiniMax ref_image_2)
wf["links"] = [l for l in wf["links"] if l[0] != 285]
# node 143 output links cleared (node removed)

# ---------- 6. MiniMax node: 0.4MP (864x480), 15s (362 frames), drone prompt ----------
# width/height/length -> use widgets (remove ResolutionSelector + math expression wiring)
for inp in nodes[136]["inputs"]:
    if inp["name"] in ("width", "height", "length"):
        inp["link"] = None
nodes[136]["widgets_values"] = ["", 864, 480, 362, "match"]
# Remove ResolutionSelector (115), ComfyMathExpression (131), PrimitiveFloat (132)
for nid in (115, 131, 132):
    wf["nodes"] = [x for x in wf["nodes"] if x["id"] != nid]
# Remove their links (276, 277 from ResolutionSelector; 275 from math; 261 from float)
wf["links"] = [l for l in wf["links"] if l[0] not in (276, 277, 275, 261)]

# ---------- 7. Prompt -> drone ascent ----------
nodes[138]["widgets_values"] = [
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
]

# ---------- 8. RTX upscaler (2x ULTRA) between VAEDecode and CreateVideo ----------
rtx = {
    "id": 201,
    "type": "RTXVideoSuperResolution",
    "mode": 0,
    "pos": [800, 400],
    "size": [320, 180],
    "inputs": [
        {"name": "images", "type": "IMAGE", "link": 303},
        {"name": "resize_type", "type": "COMFY_DYNAMICCOMBO_V3", "widget": {"name": "resize_type"}, "link": None},
        {"name": "resize_type.scale", "type": "FLOAT", "widget": {"name": "resize_type.scale"}, "link": None},
        {"name": "quality", "type": "COMBO", "widget": {"name": "quality"}, "link": None},
    ],
    "outputs": [{"name": "upscaled_images", "type": "IMAGE", "links": [304]}],
    "widgets_values": ["scale by multiplier", 2.0, "ULTRA"],
}
wf["nodes"].append(rtx)
nodes[201] = rtx
# VAEDecode(122) output -> RTX(201) instead of CreateVideo(130)
nodes[122]["outputs"][0]["links"] = [303]
wf["links"].append([303, 122, 0, 201, 0, "IMAGE"])   # VAEDecode -> RTX
wf["links"].append([304, 201, 0, 130, 0, "IMAGE"])   # RTX -> CreateVideo
# CreateVideo(130) images input -> 304
for inp in nodes[130]["inputs"]:
    if inp["name"] == "images":
        inp["link"] = 304
# Remove old link 258 (VAEDecode -> CreateVideo)
wf["links"] = [l for l in wf["links"] if l[0] != 258]

# ---------- 9. Save prefix ----------
nodes[92]["widgets_values"] = ["video/Jaisal_Drone", "auto", "auto"]

json.dump(wf, open(DST, "w", encoding="utf-8"), indent=1)
print("written:", DST)
print("nodes:", len(wf["nodes"]), "links:", len(wf["links"]))
# sanity: verify key nodes
for nid in (127, 146, 200, 136, 137, 139, 201, 92):
    n = nodes.get(nid)
    if n:
        print(f"  id={nid} {n['type']} widgets={n.get('widgets_values')}")
