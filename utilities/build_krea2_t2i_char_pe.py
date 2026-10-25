# build_krea2_t2i_char_pe.py
#
# Builds the Krea 2 single-prompt PE (prompt-expansion) variance workflows:
#   krea2_t2i_char1_pe.json  (Character 1: round face, wavy hair, full beard, dark tee)
#   krea2_t2i_char2_pe.json  (Character 2: angular face, man-bun, short patchy beard, white tee)
#
# Technique (Reddit PSA r/StableDiffusion 1wwlo18, author ref workflow pastebin S6ziW7yZ):
#   the built-in TextGenerate node (comfy_extras/nodes_textgen.py) with the Qwen3VL 4B
#   text encoder (qwen3vl_4b_fp8_scaled.safetensors, krea2 type) acts as an LLM that
#   expands ONE strong prompt into a rich description. Variance comes from two nobs:
#     1. PE seed  = sampling_mode.seed inside TextGenerate (drastic changes)
#     2. KSampler seed = "randomize" control_after_generate (fine changes, fresh seed each run)
#
# Design (single-prompt PE):
#   CLIPLoader(56) --clip--> TextGenerate(310) [prompt widget = one strong prompt per
#   character, sampling_mode = on/seed=42]
#   TextGenerate(310).generated_text --STRING--> CLIPTextEncode(300).text (positive)
#   The old PixaromaPromptEach(200) 6-row loop is REMOVED (TextGenerate is single-prompt).
#   Everything else (UNET 55, VAE 57, LoRA 96 Krea2-realism-V2 @1.0 -> LoRA 97
#   famegrid_spicy @0.7, latent 82, KSampler 53, VAEDecode 54, FameGridColorFinish 302,
#   SaveImage 29) is kept AS-IS from the char1/char2 originals.
#
# Node shape = the author's native ON-mode save (pastebin S6ziW7yZ nodes 56/64,
# frontend 1.53.10, core 0.37.0 — same core as our live 1.53.6/0.37.0 server):
#   inputs:  clip, image, video, audio, system_prompt, prompt (widget), sampling_mode.seed (widget INT)
#   outputs: generated_text, thinking
#   widgets_values (13 slots, expanded dynamic-combo form):
#     [prompt, max_length, "on", temperature, top_k, top_p, min_p, repetition_penalty,
#      seed, presence_penalty, thinking, use_default_template, mtp]
#   The sampling_mode slot holds the SELECTOR key "on"; the selected option's sub-values
#   follow positionally in schema order. The comfy_cli UI->API converter reconstructs
#   the API dict {"sampling_mode":"on", "temperature":..., "seed":42, ...} from these
#   slots (verified: a plain dict in that slot is REJECTED — validator reports
#   "required dynamic-combo input 'sampling_mode' is missing").
#
# Run:
#   & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\build_krea2_t2i_char_pe.py"

import json
import os

WF_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

# --- PE knobs (the two variance nobs: PE seed here; KSampler seed kept as "randomize") ---
PE_SEED = 42          # <- DRAMATIC variance knob (PE seed)
PE_MAX_LENGTH = 1024
PE_TEMPERATURE = 0.7
PE_TOP_K = 64
PE_TOP_P = 0.95
PE_MIN_P = 0.05
PE_REPETITION_PENALTY = 1.05
PE_PRESENCE_PENALTY = 0.0
PE_THINKING = False
PE_USE_DEFAULT_TEMPLATE = True
PE_MTP = "off"


def build(src_name, dst_name, wf_id):
    src = os.path.join(WF_DIR, src_name)
    dst = os.path.join(WF_DIR, dst_name)
    with open(src, "r", encoding="utf-8") as f:
        wf = json.load(f)

    nodes = wf["nodes"]
    by_id = {n["id"]: n for n in nodes}

    # --- sanity: source workflow must have the expected pieces ---
    assert by_id[200]["type"] == "PixaromaPromptEach", "node 200 is not PixaromaPromptEach"
    assert by_id[300]["type"] == "CLIPTextEncode", "node 300 is not CLIPTextEncode"
    assert by_id[301]["type"] == "CLIPTextEncode", "node 301 is not CLIPTextEncode"
    assert by_id[96]["widgets_values"] == ["Krea2-realism-V2.safetensors", 1.0]
    assert by_id[97]["widgets_values"] == ["famegrid_spicy_3167060.safetensors", 0.7]
    assert by_id[53]["widgets_values"] == [42, "randomize", 10, 1, "euler", "simple", 1]

    # --- one strong prompt per character = first row of the existing 6 ---
    strong_prompt = by_id[200]["properties"]["promptEachState"]["rows"][0]["text"]

    # --- remove the 6-row loop node + its link (11) ---
    nodes.remove(by_id[200])
    wf["links"] = [l for l in wf["links"] if l[0] != 11]

    # --- new TextGenerate node (id 310) at the old prompt-source position ---
    tg = {
        "id": 310,
        "type": "TextGenerate",
        "pos": [400, 470],
        "size": [420, 560],
        "flags": {},
        "order": 6,
        "mode": 0,
        "title": "PE: change seed = dramatic variance",
        "inputs": [
            {"localized_name": "clip", "name": "clip", "type": "CLIP", "link": 14},
            {"localized_name": "image", "name": "image", "shape": 7, "type": "IMAGE", "link": None},
            {"localized_name": "video", "name": "video", "shape": 7, "type": "IMAGE", "link": None},
            {"localized_name": "audio", "name": "audio", "shape": 7, "type": "AUDIO", "link": None},
            {"localized_name": "system_prompt", "name": "system_prompt", "shape": 7, "type": "STRING", "link": None},
            {"localized_name": "prompt", "name": "prompt", "type": "STRING", "widget": {"name": "prompt"}, "link": None},
            {"localized_name": "sampling_mode.seed", "name": "sampling_mode.seed", "type": "INT", "widget": {"name": "sampling_mode.seed"}, "link": None},
        ],
        "outputs": [
            {"localized_name": "generated_text", "name": "generated_text", "type": "STRING", "links": [15]},
            {"localized_name": "thinking", "name": "thinking", "type": "STRING", "links": None},
        ],
        "properties": {"Node name for S&R": "TextGenerate"},
        "widgets_values": [
            strong_prompt,
            PE_MAX_LENGTH,
            "on",
            PE_TEMPERATURE,
            PE_TOP_K,
            PE_TOP_P,
            PE_MIN_P,
            PE_REPETITION_PENALTY,
            PE_SEED,
            PE_PRESENCE_PENALTY,
            PE_THINKING,
            PE_USE_DEFAULT_TEMPLATE,
            PE_MTP,
        ],
        "widgets_values_named": {
            "prompt": strong_prompt,
            "max_length": PE_MAX_LENGTH,
            "sampling_mode": "on",
            "sampling_mode.temperature": PE_TEMPERATURE,
            "sampling_mode.top_k": PE_TOP_K,
            "sampling_mode.top_p": PE_TOP_P,
            "sampling_mode.min_p": PE_MIN_P,
            "sampling_mode.repetition_penalty": PE_REPETITION_PENALTY,
            "sampling_mode.seed": PE_SEED,
            "sampling_mode.presence_penalty": PE_PRESENCE_PENALTY,
            "thinking": PE_THINKING,
            "use_default_template": PE_USE_DEFAULT_TEMPLATE,
            "mtp": PE_MTP,
        },
    }
    nodes.append(tg)

    # --- rewire: CLIPLoader(56) gains link 14 -> TextGenerate(310) clip ---
    by_id[56]["outputs"][0]["links"] = [2, 3, 14]

    # --- positive CLIPTextEncode(300).text now comes from the PE link 15 ---
    for inp in by_id[300]["inputs"]:
        if inp["name"] == "text":
            inp["link"] = 15

    # --- new links ---
    wf["links"].append([14, 56, 0, 310, 0, "CLIP"])
    wf["links"].append([15, 310, 0, 300, 1, "STRING"])

    # --- metadata ---
    wf["id"] = wf_id
    wf["last_node_id"] = 310
    wf["last_link_id"] = 15

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)

    print(f"built {dst}")
    print(f"  nodes: {len(wf['nodes'])}  links: {len(wf['links'])}")
    print(f"  PE seed: {PE_SEED}  max_length: {PE_MAX_LENGTH}  prompt chars: {len(strong_prompt)}")


build("krea2_t2i_char1.json", "krea2_t2i_char1_pe.json", "krea2_t2i_char1_pe")
build("krea2_t2i_char2.json", "krea2_t2i_char2_pe.json", "krea2_t2i_char2_pe")
print("done")
