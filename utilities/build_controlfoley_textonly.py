"""Build the TEXT-ONLY ControlFoley SFX workflow.

Transforms jaisal_sketch_title_audio.json from VIDEO-mode (video conditions the
SFX) to TEXT-ONLY mode (SFX generated purely from the text prompt). This is the
clean, reusable production path for line-art video where ControlFoley's video
mode produces a noise bed.

Design (reusable):
  Node 1 [LoadControlFoleyModel]   -> loads the model
  Node 2 [LoadControlFoleyVideo]   -> loads the SOUNDLESS video (for the mux ONLY)
  Node 3 [ControlFoleyGenerate]    -> TEXT-ONLY SFX (NO video input)
  Node 4 [SaveControlFoleyAudio]   -> saves the SFX as WAV
  Node 5 [MuxControlFoleyAudioToVideo] -> muxes SFX into the video (replace mode)

Wiring:
  Node 1 -> Node 3 (model)
  Node 1 -> Node 5 (model)
  Node 2 -> Node 5 (video, for mux)   [Node 2 does NOT feed Node 3]
  Node 3 -> Node 4 (audio)
  Node 3 -> Node 5 (audio)

To reuse on a new video:
  1. Strip the video's audio (ffmpeg -an) and copy it to input\ with a simple name.
  2. Set Node 2's video_path to that filename.
  3. Edit Node 3's prompt to describe the SFX timeline.
  4. Run -> get the muxed video with the new SFX.

Idempotent: safe to re-run (it detects if already text-only).
"""
import json
import shutil
from pathlib import Path

WF = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_sketch_title_audio.json")
BACKUP = Path(r"d:\models\vsCodeMcp\workflow_backups\jaisal_sketch_title_audio_video_mode.json")

# Clean TEXT-ONLY SFX prompt (no "synced to the video" — there's no video input now).
PROMPT = (
    "Natural ambient sound effects only. A stick figure walks on a stone bridge "
    "over a river.\n"
    "0-2s: soft footsteps on stone as he walks.\n"
    "2-3s: a soft low whistle and the whoosh of a paper plane being thrown.\n"
    "6s: a soft plop as the paper plane touches the water.\n"
    "6-7s: a soft whoosh as the figure jumps over the guardrail.\n"
    "7-8s: a soft thud as he lands, then a whoosh as he jumps toward the water.\n"
    "9s: a soft splash as he lands in the water.\n"
    "9-14s: gentle flowing river water."
)

NEGATIVE_PROMPT = (
    "music, instrumental music, musical instruments, melody, beat, rhythm, "
    "soundtrack, song, dialogue, speech, talking, voice, loud sounds, harsh noise, "
    "distortion, static, electronic sounds, beeps, alarms."
)

DURATION = 14.5  # text-only generation length (video is 14.375s; mux truncates cleanly)


def main() -> int:
    # Back up the video-mode version (only if the backup doesn't already exist).
    if not BACKUP.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(WF, BACKUP)
        print(f"Backed up video-mode workflow -> {BACKUP.name}")
    else:
        print(f"Backup already exists: {BACKUP.name} (not overwriting)")

    wf = json.load(open(WF, encoding="utf-8"))
    links = wf["links"]
    nodes = {n["id"]: n for n in wf["nodes"]}

    # 1. Remove the link from Node 2 (video) -> Node 3 (generator).
    #    This makes Node 3 text-only (no video input).
    removed = []
    for l in links:
        # link = [link_id, from_node, from_slot, to_node, to_slot, type]
        if l[1] == 2 and l[3] == 3:
            removed.append(l[0])
    links[:] = [l for l in links if l[0] not in removed]
    print(f"Removed link(s) {removed} (Node 2 -> Node 3)")

    # 2. Set Node 3's 'video' input link to None (it's now text-only).
    n3 = nodes[3]
    for inp in n3["inputs"]:
        if inp["name"] == "video":
            inp["link"] = None
            print(f"Set Node 3 'video' input link -> None (text-only mode)")

    # 3. Update Node 3's prompt, negative, and duration.
    wv = n3["widgets_values"]
    wv[0] = PROMPT
    wv[1] = NEGATIVE_PROMPT
    wv[2] = DURATION
    print(f"Updated Node 3: prompt (text-only SFX), negative, duration={DURATION}")

    # 4. Verify Node 2 still feeds Node 5 (the mux).
    mux_video_link = [l for l in links if l[1] == 2 and l[3] == 5]
    if not mux_video_link:
        print("WARNING: Node 2 -> Node 5 (mux video) link is missing!")
    else:
        print(f"Node 2 -> Node 5 (mux video) link {mux_video_link[0][0]} intact")

    json.dump(wf, open(WF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nSaved text-only workflow -> {WF.name}")
    print("\nFinal wiring:")
    for l in wf["links"]:
        print(f"  link {l[0]}: node {l[1]} slot {l[2]} -> node {l[3]} slot {l[4]} ({l[5]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
