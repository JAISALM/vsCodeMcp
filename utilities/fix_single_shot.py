import json, shutil

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
shutil.copy(p, p + ".pre_named_fix.bak")
wf = json.load(open(p, encoding="utf-8"))

prompt = """A single continuous cinematic shot in an angular 3D art style with brush stroke color texture. The scene opens exactly on <Picture 1>: a young boy in a school uniform with a red school bag, standing at the start of a long traditional stone bridge with continuous stone handrails crossing a wide river.

The boy begins walking forward along the bridge. As he walks, the sky darkens, the wind picks up, and rain begins to fall. The boy starts running through the bridge as the rain intensifies. Midway across, the boy jumps into the river. The camera then dips down into the water, tilting to an underwater view with rising bubbles.

Keep the boy's character design, face, school uniform, and red school bag consistent throughout. Keep the angular 3D art style with brush stroke color texture throughout. No dialogue, no text, no subtitles. The 'The Jaisal Cut' title is composited in post over the underwater bubbles and is NOT rendered by the model.

Audio: light wind building, rain intensifying, a splash as the boy jumps in, then muffled underwater ambience."""

for n in wf["nodes"]:
    # Fix aspect ratio typo on ResolutionSelector
    if n["type"] == "ResolutionSelector":
        n["widgets_values"] = ["16:9 (Widescreen)", 0.98, 32]
        print("ResolutionSelector -> 16:9 (Widescreen) 0.98MP")

    # Fix the MiniMaxH3ImageToVideo node: update BOTH widgets_values and widgets_values_named
    if any(i.get("name") == "first_frame" for i in n.get("inputs", [])):
        w = n["widgets_values"]
        w[0] = prompt
        w[3] = 15
        w[9] = True
        w[10] = "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"
        w[12] = 4
        # Update the named dict (the converter prefers this)
        named = n.get("widgets_values_named")
        if isinstance(named, dict):
            named["prompt"] = prompt
            named["value_1"] = 15
            named["value"] = True
            named["lora_name"] = "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"
            named["value_2"] = 4
            print("Updated widgets_values_named (prompt, duration=15, turbo=True, lora=4step, steps=4)")
        else:
            print("WARNING: no widgets_values_named dict found")

json.dump(wf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Saved")
