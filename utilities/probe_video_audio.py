"""Probe a video file for audio streams (ffprobe).

Usage:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\probe_video_audio.py" <path-to-mp4>
"""
import json
import subprocess
import sys


def probe(path: str) -> None:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", path],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("ffprobe failed:", r.stderr[:500])
        return
    data = json.loads(r.stdout)
    streams = data.get("streams", [])
    print(f"File: {path}")
    print(f"Total streams: {len(streams)}")
    for i, s in enumerate(streams):
        print(f"  stream {i}: codec={s.get('codec_name')}, type={s.get('codec_type')}, "
              f"duration={s.get('duration', '?')}s, channels={s.get('channels', '-')}")
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    print(f"Has audio stream: {has_audio}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: probe_video_audio.py <path-to-mp4>")
        raise SystemExit(1)
    probe(sys.argv[1])
