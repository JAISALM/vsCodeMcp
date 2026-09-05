"""Build the ControlFoley audio workflow for the locked Jaisal Sketch Title video.

Pipeline (TC-V2A: video + text-guided natural sounds):
  LoadControlFoleyModel -> ControlFoleyGenerate <- LoadControlFoleyVideo
        |                        |
        |                        v
        |               SaveControlFoleyAudio
        v                        (WAV)
  MuxControlFoleyAudioToVideo  (replace original audio -> final MP4)

First run auto-fetches the ControlFoley source tree (pinned) and downloads the
~16 GB weights from Hugging Face. Subsequent runs reuse the cache.
"""
import json
import shutil
from pathlib import Path

INPUT_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input")
WORKFLOWS_DIR = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows")
SRC_VIDEO = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\video\Jaisal_Sketch_Title_00010_.mp4")
DST_VIDEO_NAME = "jaisal_sketch_title_00010.mp4"

# 1. Stage the locked video into the input dir so LoadControlFoleyVideo finds it by name.
dst_video = INPUT_DIR / DST_VIDEO_NAME
shutil.copy2(SRC_VIDEO, dst_video)
print(f"[1] Copied video -> {dst_video}")

# 2. TC-V2A text prompt: the exact natural sounds the user asked for, in story order.
#    HARD RULE (D041): natural sounds ONLY, NO instrumental music.
PROMPT = (
    "Natural ambient sounds only. A stick figure walks slowly on a stone bridge over a river. "
    "Soft footsteps on stone as he walks. A gentle continuous wind in the background. "
    "A soft low whistle. Soft flowing river water below the bridge. "
    "A few birds chirping softly in the distance. "
    "A soft whoosh as a small paper plane is thrown. "
    "A soft plop as the paper plane lands on the water. "
    "A soft whoosh as the figure jumps. "
    "A soft splash as the figure lands in the water. "
    "Then calm quiet water with a few low birds chirping. "
    "NO music, NO instrumental music, NO musical instruments, NO melody, NO beat, NO soundtrack, NO dialogue."
)

workflow = {
    "last_node_id": 5,
    "last_link_id": 6,
    "version": 0.4,
    "nodes": [
        {
            "id": 1,
            "type": "LoadControlFoleyModel",
            "pos": [80, 80],
            "size": [360, 220],
            "flags": {},
            "order": 0,
            "mode": 0,
            "inputs": [],
            "outputs": [
                {"name": "controlfoley_model", "type": "CONTROLFOLEY_MODEL", "links": [1, 4]}
            ],
            "properties": {"Node name for S&R": "LoadControlFoleyModel"},
            # [controlfoley_source_dir, model_weights_dir, variant, device, precision, low_vram, compile_encoders, auto_fetch_source]
            "widgets_values": ["controlfoley", "path/to/model_weights", "large_44k", "auto", "bf16", False, False, True]
        },
        {
            "id": 2,
            "type": "LoadControlFoleyVideo",
            "pos": [80, 360],
            "size": [340, 200],
            "flags": {},
            "order": 1,
            "mode": 0,
            "inputs": [],
            "outputs": [
                {"name": "controlfoley_video", "type": "CONTROLFOLEY_VIDEO", "links": [2, 5]},
                {"name": "video_output", "type": "VIDEO", "links": None}
            ],
            "properties": {"Node name for S&R": "LoadControlFoleyVideo"},
            # [video_path, duration]
            "widgets_values": [DST_VIDEO_NAME, 12.5]
        },
        {
            "id": 3,
            "type": "ControlFoleyGenerate",
            "pos": [520, 130],
            "size": [440, 300],
            "flags": {},
            "order": 2,
            "mode": 0,
            "inputs": [
                {"name": "controlfoley_model", "type": "CONTROLFOLEY_MODEL", "link": 1},
                {"name": "video", "type": "CONTROLFOLEY_VIDEO", "link": 2},
                {"name": "video_input", "type": "VIDEO", "link": None},
                {"name": "images", "type": "IMAGE", "link": None}
            ],
            "outputs": [
                {"name": "audio", "type": "AUDIO", "links": [3, 6]},
                {"name": "sample_rate", "type": "INT", "links": None},
                {"name": "inference_time_sec", "type": "FLOAT", "links": None},
                {"name": "peak_vram_gb", "type": "FLOAT", "links": None}
            ],
            "properties": {"Node name for S&R": "ControlFoleyGenerate"},
            # [prompt, negative_prompt, duration, seed, num_inference_steps, guidance_scale,
            #  mask_away_clip, cache_video_features, staged_offload, clip_batch_size_multiplier,
            #  sync_batch_size_multiplier, reference_audio_path, image_fps]
            "widgets_values": [PROMPT, "", 12.5, 42, "fixed", 4.5, False, True, True, "40", "40", "", 24.0]
        },
        {
            "id": 4,
            "type": "SaveControlFoleyAudio",
            "pos": [1040, 120],
            "size": [340, 160],
            "flags": {},
            "order": 3,
            "mode": 0,
            "inputs": [
                {"name": "audio", "type": "AUDIO", "link": 3}
            ],
            "outputs": [
                {"name": "audio", "type": "AUDIO", "links": None},
                {"name": "audio_file", "type": "CONTROLFOLEY_AUDIO_FILE", "links": None},
                {"name": "audio_path", "type": "STRING", "links": None}
            ],
            "properties": {"Node name for S&R": "SaveControlFoleyAudio"},
            # [filename_prefix, format]
            "widgets_values": ["controlfoley/jaisal_sketch_title", "wav"]
        },
        {
            "id": 5,
            "type": "MuxControlFoleyAudioToVideo",
            "pos": [1040, 360],
            "size": [360, 200],
            "flags": {},
            "order": 4,
            "mode": 0,
            "inputs": [
                {"name": "controlfoley_model", "type": "CONTROLFOLEY_MODEL", "link": 4},
                {"name": "video", "type": "CONTROLFOLEY_VIDEO", "link": 5},
                {"name": "audio", "type": "AUDIO", "link": 6}
            ],
            "outputs": [
                {"name": "video_file", "type": "CONTROLFOLEY_VIDEO_FILE", "links": None},
                {"name": "video_path", "type": "STRING", "links": None}
            ],
            "properties": {"Node name for S&R": "MuxControlFoleyAudioToVideo"},
            # [output_filename, mode]
            "widgets_values": ["controlfoley/jaisal_sketch_title.mp4", "replace"]
        }
    ],
    "links": [
        [1, 1, 0, 3, 0, "CONTROLFOLEY_MODEL"],
        [2, 2, 0, 3, 1, "CONTROLFOLEY_VIDEO"],
        [3, 3, 0, 4, 0, "AUDIO"],
        [4, 1, 0, 5, 0, "CONTROLFOLEY_MODEL"],
        [5, 2, 0, 5, 1, "CONTROLFOLEY_VIDEO"],
        [6, 3, 0, 5, 2, "AUDIO"]
    ]
}

out = WORKFLOWS_DIR / "jaisal_sketch_title_audio.json"
out.write_text(json.dumps(workflow, indent=2), encoding="utf-8")
print(f"[2] Wrote workflow -> {out}")
print("[3] Done. Open jaisal_sketch_title_audio.json in a FRESH tab and run.")
