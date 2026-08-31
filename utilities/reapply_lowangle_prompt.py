import json, shutil

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_lowangle.json"
shutil.copy(p, p + ".pre_prompt_reapply.bak")
wf = json.load(open(p, encoding="utf-8"))

prompt = """subject_definitions:
<Subject 1> is the young boy in <Picture 1>, <Picture 2>, <Picture 3>, <Picture 4>, and <Picture 5>, with short dark hair, a school uniform, and a red school bag.
<Subject 2> is the long traditional stone bridge environment in <Picture 1>, <Picture 2>, <Picture 4>, and <Picture 5>, with continuous stone handrails crossing a wide river.
<Picture 1> is the first frame of [Shot 1], a wide establishing shot of the boy on the stone bridge in the base scene.
<Picture 2> is the first frame of [Shot 2], a medium shot of the boy in the middle of the bridge as rain begins.
<Picture 3> is the first frame of [Shot 3], a close-up of the boy's face fully drenched in heavy rain.
<Picture 4> is the first frame of [Shot 4], a medium shot of the boy after the rain stops, water dripping.
<Picture 5> is the first frame of [Shot 5], a low-angle long shot from water level looking up at the boy looking at the sky.

summary:
[reference generation] The target video is a 15-second five-shot cinematic sequence in an angular 3D art style with brush stroke color texture. <Subject 1> (the boy) and <Subject 2> (the stone bridge) are preserved across all shots. Each shot begins from its corresponding reference frame: <Picture 1> for [Shot 1], <Picture 2> for [Shot 2], <Picture 3> for [Shot 3], <Picture 4> for [Shot 4], and <Picture 5> for [Shot 5]. The sequence follows the boy across a rain event on the bridge, ending on a low-angle shot with negative space for a title.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5]): fully_preserved - the boy's face, short dark hair, school uniform, and red school bag are retained in every shot.
<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 4], [Shot 5]): fully_preserved - the long stone bridge with continuous handrails crossing the wide river is retained.
<Picture 1> ([Shot 1] first frame): fully_preserved - the wide base-scene composition is the opening frame.
<Picture 2> ([Shot 2] first frame): fully_preserved - the medium mid-rain composition is the opening frame of Shot 2.
<Picture 3> ([Shot 3] first frame): fully_preserved - the close-up drenched composition is the opening frame of Shot 3.
<Picture 4> ([Shot 4] first frame): fully_preserved - the after-rain composition is the opening frame of Shot 4.
<Picture 5> ([Shot 5] first frame): fully_preserved - the low-angle long-shot composition is the opening frame of Shot 5.

detailed_description:
The target video is in an angular 3D art style with brush stroke color texture, cinematic lighting, and a moody rain palette.
[Shot 1] A wide establishing shot opens on <Subject 2>, the long traditional stone bridge with continuous stone handrails crossing a wide river. <Subject 1>, the young boy in a school uniform with a red school bag, stands small in the frame on the bridge. The sky is darkening. The camera is static, then begins a slow push-in. The shot begins from <Picture 1>.
[Shot 2] At 00:03.000, the shot cuts to a medium shot of <Subject 1> in the middle of the bridge as rain begins. Rain streaks fall across the frame and the stone handrails get wet. The camera holds steady with a slight handheld drift. The shot begins from <Picture 2>.
[Shot 3] At 00:06.000, the shot cuts to a close-up of <Subject 1>'s face, fully drenched in heavy rain. Water runs down his face and hair. The camera is tight and static, emphasizing the drenched expression. The shot begins from <Picture 3>.
[Shot 4] At 00:09.000, the shot cuts to a medium shot of <Subject 1> after the rain stops. Water drips from his hair and the bridge stones. The sky begins to clear. The camera slowly pulls back. The shot begins from <Picture 4>.
[Shot 5] At 00:12.000, the shot cuts to a low-angle long shot from water level, looking up at <Subject 1> who is drenched and looking up at the sky. Water is in the foreground. The camera is static, holding the low angle with generous negative space above the boy for a title. The shot begins from <Picture 5>.

overall_soundscape:
Rain sounds throughout the sequence - light rain building in [Shot 2], heavy rain in [Shot 3], dripping water in [Shot 4], and a quiet after-rain stillness in [Shot 5].

non_diegetic_music:
A restrained, slow cinematic score with soft piano and low strings, building gently through the rain and resolving quietly on the final low-angle shot. No dialogue, no text, no subtitles. The title is composited in post and is NOT rendered by the model."""

found = False
for n in wf["nodes"]:
    if str(n["id"]) == "138":
        n["widgets_values"] = [prompt]
        found = True
        print("Prompt re-applied to node 138 (len=%d)" % len(prompt))

if not found:
    print("ERROR: node 138 not found!")
else:
    json.dump(wf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Saved")
