import json, shutil

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_single_shot.json"
shutil.copy(p, p + ".pre_build.bak")
wf = json.load(open(p, encoding="utf-8"))

# --- Simple single-shot prompt (R2V style, <Picture 1> = first frame) ---
prompt = """A single continuous cinematic shot in an angular 3D art style with brush stroke color texture. The scene opens exactly on <Picture 1>: a young boy in a school uniform with a red school bag, standing at the start of a long traditional stone bridge with continuous stone handrails crossing a wide river.

The boy begins walking forward along the bridge. As he walks, the sky darkens, the wind picks up, and rain begins to fall. The boy starts running through the bridge as the rain intensifies. Midway across, the boy jumps into the river. The camera then dips down into the water, tilting to an underwater view with rising bubbles.

Keep the boy's character design, face, school uniform, and red school bag consistent throughout. Keep the angular 3D art style with brush stroke color texture throughout. No dialogue, no text, no subtitles. The 'The Jaisal Cut' title is composited in post over the underwater bubbles and is NOT rendered by the model.

Audio: light wind building, rain intensifying, a splash as the boy jumps in, then muffled underwater ambience."""

for n in wf["nodes"]:
    # 1. LoadImage -> 1.png (wide base scene = the first frame)
    if n["type"] == "LoadImage":
        n["widgets_values"] = ["1.png", "image"]
        print("LoadImage -> 1.png")

    # 2. MiniMaxH3ImageToVideo (UUID type) -> prompt, duration, turbo 4-step
    if any(i.get("name") == "first_frame" for i in n.get("inputs", [])):
        w = n["widgets_values"]
        # w[0]=prompt, w[1]=width, w[2]=height, w[3]=duration, w[4]=seed,
        # w[5]=unet, w[6]=clip, w[7]=vae, w[8]=audio_vae, w[9]=turbo_mode,
        # w[10]=turbo_model, w[11]=turbo_strength, w[12]=turbo_steps
        w[0] = prompt
        w[3] = 15          # 15s (max) for the full walk->rain->run->jump->underwater arc
        w[9] = True        # enable turbo
        w[10] = "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors"
        w[12] = 4          # 4-step turbo
        print("MiniMaxH3ImageToVideo -> prompt + 15s + turbo 4-step")

    # 3. ResolutionSelector -> 16:9 768p (1344x768)
    if n["type"] == "ResolutionSelector":
        n["widgets_values"] = ["16:9 (Widescreeen)", 0.98, 32]
        print("ResolutionSelector -> 16:9 0.98MP (1344x768)")

    # 4. SaveVideo -> our prefix
    if n["type"] == "SaveVideo":
        n["widgets_values"][0] = "video/Jaisal_SingleShot"
        print("SaveVideo -> video/Jaisal_SingleShot")

json.dump(wf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Saved")
