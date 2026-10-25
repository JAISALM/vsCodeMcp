"""
Build Krea 2 PE (Prompt Expansion) workflows for char1 and char2.

Inserts a TextGenerate node between PixaromaPromptEach and CLIPTextEncode.
The TextGenerate node uses the text encoder (Qwen3VL 4B) as an LLM to expand
the prompt, adding variance via the PE seed.

Wiring:
  PixaromaPromptEach.prompt → TextGenerate.prompt
  CLIPLoader.CLIP → TextGenerate.clip
  TextGenerate.generated_text → CLIPTextEncode.text (replaces direct link)

Two nobs for variance:
  - PE seed (inside TextGenerate sampling_mode): extreme changes
  - KSampler seed: fine-grained changes
"""
import json
import copy
import os

WORKFLOWS_DIR = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"

def build_pe_workflow(src_name, dst_name, pe_seed=42):
    src_path = os.path.join(WORKFLOWS_DIR, src_name)
    dst_path = os.path.join(WORKFLOWS_DIR, dst_name)
    
    with open(src_path, encoding="utf-8-sig") as f:
        wf = json.load(f)
    
    # Find key nodes
    node_map = {n["id"]: n for n in wf["nodes"]}
    
    # Find PixaromaPromptEach, CLIPLoader, CLIPTextEncode (positive)
    pixaroma = None
    clip_loader = None
    clip_pos = None
    clip_neg = None
    for n in wf["nodes"]:
        if n["type"] == "PixaromaPromptEach":
            pixaroma = n
        elif n["type"] == "CLIPLoader":
            clip_loader = n
        elif n["type"] == "CLIPTextEncode":
            # The positive one has its text input linked from PixaromaPromptEach
            for inp in n.get("inputs", []):
                if inp["name"] == "text" and inp.get("link") is not None:
                    # Check if this link comes from PixaromaPromptEach
                    link_id = inp["link"]
                    for link in wf["links"]:
                        if link[0] == link_id and link[1] == pixaroma["id"]:
                            clip_pos = n
                            break
                if inp["name"] == "text" and inp.get("link") is None:
                    clip_neg = n
            if clip_pos and clip_neg:
                break
    
    if not pixaroma or not clip_loader or not clip_pos:
        raise ValueError(f"Could not find required nodes in {src_name}")
    
    print(f"Found: PixaromaPromptEach={pixaroma['id']}, CLIPLoader={clip_loader['id']}, CLIPTextEncode(pos)={clip_pos['id']}")
    
    # Get the current link from PixaromaPromptEach to CLIPTextEncode
    old_link_id = None
    for link in wf["links"]:
        if link[1] == pixaroma["id"] and link[3] == clip_pos["id"]:
            old_link_id = link[0]
            break
    
    if old_link_id is None:
        raise ValueError(f"Could not find link from PixaromaPromptEach to CLIPTextEncode")
    
    print(f"Old link {old_link_id}: {pixaroma['id']} → {clip_pos['id']}")
    
    # Remove the old link
    wf["links"] = [l for l in wf["links"] if l[0] != old_link_id]
    
    # Update the CLIPTextEncode text input to have no link (will be re-linked)
    for inp in clip_pos["inputs"]:
        if inp["name"] == "text":
            inp["link"] = None
    
    # Update the PixaromaPromptEach prompt output links
    for out in pixaroma["outputs"]:
        if out["name"] == "prompt":
            out["links"] = [l for l in (out.get("links") or []) if l != old_link_id]
    
    # Update the CLIPLoader CLIP output links (remove the one going to clip_pos text)
    # Actually, the CLIPLoader links go to clip_pos and clip_neg clip inputs, not text.
    # We need to add a NEW link from CLIPLoader to TextGenerate.
    
    # Create the TextGenerate node
    new_node_id = 303
    # Make sure 303 doesn't already exist
    while new_node_id in node_map:
        new_node_id += 1
    
    # Get the prompt text from PixaromaPromptEach for the TextGenerate prompt widget
    # The TextGenerate prompt widget should contain the PE instruction
    pe_prompt = (
        "Expand this prompt into a detailed, vivid image generation prompt. "
        "Add specific visual details: lighting, textures, materials, environment, "
        "atmosphere, camera angle, and mood. Keep the core subject and action intact. "
        "Output only the expanded prompt, no explanations."
    )
    
    text_gen_node = {
        "id": new_node_id,
        "type": "TextGenerate",
        "pos": [pixaroma["pos"][0], pixaroma["pos"][1] + 400],
        "size": [420, 200],
        "flags": {},
        "order": pixaroma["order"] + 1,
        "mode": 0,
        "inputs": [
            {
                "localized_name": "clip",
                "name": "clip",
                "type": "CLIP",
                "link": None  # Will be set below
            },
            {
                "localized_name": "image",
                "name": "image",
                "shape": 7,
                "type": "IMAGE",
                "link": None
            },
            {
                "localized_name": "video",
                "name": "video",
                "shape": 7,
                "type": "IMAGE",
                "link": None
            },
            {
                "localized_name": "audio",
                "name": "audio",
                "shape": 7,
                "type": "AUDIO",
                "link": None
            },
            {
                "localized_name": "prompt",
                "name": "prompt",
                "type": "STRING",
                "widget": {"name": "prompt"},
                "link": None  # Will be set below
            },
            {
                "localized_name": "max_length",
                "name": "max_length",
                "type": "INT",
                "widget": {"name": "max_length"},
                "link": None
            },
            {
                "localized_name": "Sampling Mode",
                "name": "sampling_mode",
                "type": "COMFY_DYNAMICCOMBO_V3",
                "widget": {"name": "sampling_mode"},
                "link": None
            },
            {
                "localized_name": "thinking",
                "name": "thinking",
                "shape": 7,
                "type": "BOOLEAN",
                "widget": {"name": "thinking"},
                "link": None
            },
            {
                "localized_name": "use_default_template",
                "name": "use_default_template",
                "shape": 7,
                "type": "BOOLEAN",
                "widget": {"name": "use_default_template"},
                "link": None
            }
        ],
        "outputs": [
            {
                "localized_name": "generated_text",
                "name": "generated_text",
                "type": "STRING",
                "links": None  # Will be set below
            },
            {
                "localized_name": "thinking",
                "name": "thinking",
                "type": "STRING",
                "links": None
            }
        ],
        "properties": {
            "Node name for S&R": "TextGenerate"
        },
        "widgets_values": [
            pe_prompt,
            512,
            "on",
            False,
            True
        ],
        "widgets_values_named": {
            "prompt": pe_prompt,
            "max_length": 512,
            "sampling_mode": {
                "sampling_mode": "on",
                "temperature": 0.7,
                "top_k": 64,
                "top_p": 0.95,
                "min_p": 0.05,
                "repetition_penalty": 1.05,
                "seed": pe_seed
            },
            "thinking": False,
            "use_default_template": True
        }
    }
    
    wf["nodes"].append(text_gen_node)
    
    # Create new links
    # Link A: PixaromaPromptEach.prompt → TextGenerate.prompt
    link_a_id = wf["last_link_id"] + 1
    link_a = [link_a_id, pixaroma["id"], 0, new_node_id, 4, "STRING"]
    wf["links"].append(link_a)
    
    # Update PixaromaPromptEach prompt output
    for out in pixaroma["outputs"]:
        if out["name"] == "prompt":
            if out["links"] is None:
                out["links"] = []
            out["links"].append(link_a_id)
    
    # Update TextGenerate prompt input
    for inp in text_gen_node["inputs"]:
        if inp["name"] == "prompt":
            inp["link"] = link_a_id
    
    # Link B: CLIPLoader.CLIP → TextGenerate.clip
    link_b_id = wf["last_link_id"] + 2
    link_b = [link_b_id, clip_loader["id"], 0, new_node_id, 0, "CLIP"]
    wf["links"].append(link_b)
    
    # Update CLIPLoader CLIP output
    for out in clip_loader["outputs"]:
        if out["name"] == "CLIP":
            if out["links"] is None:
                out["links"] = []
            out["links"].append(link_b_id)
    
    # Update TextGenerate clip input
    for inp in text_gen_node["inputs"]:
        if inp["name"] == "clip":
            inp["link"] = link_b_id
    
    # Link C: TextGenerate.generated_text → CLIPTextEncode.text
    link_c_id = wf["last_link_id"] + 3
    link_c = [link_c_id, new_node_id, 0, clip_pos["id"], 1, "STRING"]
    wf["links"].append(link_c)
    
    # Update TextGenerate generated_text output
    for out in text_gen_node["outputs"]:
        if out["name"] == "generated_text":
            out["links"] = [link_c_id]
    
    # Update CLIPTextEncode text input
    for inp in clip_pos["inputs"]:
        if inp["name"] == "text":
            inp["link"] = link_c_id
    
    # Update last_link_id
    wf["last_link_id"] = link_c_id
    
    # Update last_node_id
    wf["last_node_id"] = max(wf.get("last_node_id", 0), new_node_id)
    
    # Update the workflow id
    wf["id"] = dst_name.replace(".json", "")
    
    # Save
    with open(dst_path, "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=2)
    
    print(f"Saved {dst_name}")
    print(f"  New node: TextGenerate (id={new_node_id})")
    print(f"  Link A: {pixaroma['id']}.prompt → {new_node_id}.prompt (id={link_a_id})")
    print(f"  Link B: {clip_loader['id']}.CLIP → {new_node_id}.clip (id={link_b_id})")
    print(f"  Link C: {new_node_id}.generated_text → {clip_pos['id']}.text (id={link_c_id})")
    print(f"  PE seed: {pe_seed}")
    print(f"  KSampler seed: (unchanged - change for fine-grained variance)")
    return dst_path

if __name__ == "__main__":
    # Build PE versions of both character workflows
    p1 = build_pe_workflow("krea2_t2i_char1.json", "krea2_t2i_char1_pe.json", pe_seed=42)
    p2 = build_pe_workflow("krea2_t2i_char2.json", "krea2_t2i_char2_pe.json", pe_seed=42)
    print(f"\nDone. Workflows saved to:\n  {p1}\n  {p2}")
