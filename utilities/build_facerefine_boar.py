import json

SRC = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\H3_Face_Refine_Auto_Select.json'
DST = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\H3_FaceRefine_boar_grave.json'

# R2V output of the boar-grave talking scene (VHS_VideoCombine prefix 'boar_grave')
R2V_OUTPUT = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\boar_grave_00001.mp4'

FACE_PROMPT = """A lean, fit Keralite man in his 30s with a full unkempt beard,
wearing a rose-pink shirt, crouched inside a small unfinished grave hole in
a black-soil Kerala backyard, digging with a shovel. Morning light, natural
skin tone. Refine only the face — keep the pose, costume and scene identical."""

wf = json.load(open(SRC, encoding='utf-8'))
nodes = {n['id']: n for n in wf['nodes']}

# --- fix model names to installed ones ---
FIX = {
    4: ("vae_name", "minimax_h3_video_vae_fp16.safetensors"),
    5: ("vae_name", "minimax_h3_audio_vae_fp32.safetensors"),
    12: ("lora_name", "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"),
}
for nid, (key, new_name) in FIX.items():
    n = nodes[nid]
    print(nid, n['type'], 'before:', json.dumps(n.get('widgets_values'))[:100])
    if isinstance(n['widgets_values'], list):
        n['widgets_values'][0] = new_name
    if 'widgets_values_named' in n and key in n['widgets_values_named']:
        n['widgets_values_named'][key] = new_name
    print('   after :', json.dumps(n['widgets_values'])[:100])

# --- reference images ---
n6 = nodes[6]
n6['widgets_values'][0] = 'boar_char1_identity.png'
n7 = nodes[7]
n7['widgets_values'][0] = 'boar_char2_identity.png'
print('refs:', n6['widgets_values'], n7['widgets_values'])

# --- input video = R2V output ---
n1 = nodes[1]
n1['widgets_values']['video'] = R2V_OUTPUT
if 'videopreview' in n1['widgets_values']:
    n1['widgets_values']['videopreview'] = None
print('video:', n1['widgets_values']['video'])

# --- R2V node prompt (identity prompt for the subject) ---
n9 = nodes[9]
if isinstance(n9['widgets_values'], list) and n9['widgets_values']:
    n9['widgets_values'][0] = FACE_PROMPT
    print('prompt set (len %d)' % len(FACE_PROMPT))

with open(DST, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False)
print('saved:', DST)
