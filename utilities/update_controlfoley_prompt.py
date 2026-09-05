"""Update the ControlFoley generate node (node 3) in jaisal_sketch_title_audio.json.

Fixes the "static noise" output by:
  1. Replacing the flat, un-timed sound list with a CLEAN TIMED sound design
     that matches the video beat-by-beat (footsteps -> whistle/throw -> plane
     touches water -> jump -> land -> splash -> title water).
  2. Moving the NO-music / NO-noise exclusions OUT of the positive prompt and
     INTO the negative_prompt widget (that is what it is for).
  3. Aligning the duration widget to the actual video length (14.33s -> 15.0
     upper limit) so the tail (title at ~11s) is not cut / misaligned.

Idempotent: safe to re-run.
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_sketch_title_audio.json"

# Clean, TIMED, video-synced sound design (matches the user's beat-by-beat).
PROMPT = (
    "Natural ambient sounds only, synced to the video. A stick figure walks on a "
    "stone bridge over a river.\n"
    "0-2s: soft footsteps on stone as he walks.\n"
    "2-3s: a soft low whistle and the soft whoosh of a paper plane being thrown, "
    "nothing else.\n"
    "3-6s: quiet, just gentle wind and distant river water.\n"
    "6s: a soft plop as the paper plane touches the water.\n"
    "6-7s: a soft whoosh as the figure jumps over the guardrail.\n"
    "7-8s: a soft thud as he lands, then another whoosh as he jumps toward the water.\n"
    "9s: a soft splash as he lands in the water.\n"
    "9-11s: calm, quiet water.\n"
    "11s onward: gentle flowing river water only, as the title appears."
)

# Exclusions live in the NEGATIVE prompt (keeps the positive prompt clean/focused).
NEGATIVE_PROMPT = (
    "music, instrumental music, musical instruments, melody, beat, rhythm, "
    "soundtrack, song, dialogue, speech, talking, voice, loud sounds, harsh noise, "
    "distortion, static, electronic sounds, beeps, alarms."
)

DURATION = 15.0  # upper limit; the 00011 video is 14.33s so output follows input length


def main() -> int:
    wf = json.load(open(WF, encoding="utf-8"))
    node = next(n for n in wf["nodes"] if n["id"] == 3)
    assert node["type"] == "ControlFoleyGenerate", f"node 3 is {node['type']}, not ControlFoleyGenerate"

    wv = node["widgets_values"]
    print("BEFORE:")
    print("  prompt[0]:", repr(wv[0][:60]))
    print("  negative[1]:", repr(wv[1]))
    print("  duration[2]:", wv[2])

    wv[0] = PROMPT
    wv[1] = NEGATIVE_PROMPT
    wv[2] = DURATION

    json.dump(wf, open(WF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # Re-read to confirm.
    wf2 = json.load(open(WF, encoding="utf-8"))
    n2 = next(n for n in wf2["nodes"] if n["id"] == 3)
    print("\nAFTER:")
    print("  prompt[0]:", repr(n2["widgets_values"][0][:60]))
    print("  negative[1]:", repr(n2["widgets_values"][1][:60]))
    print("  duration[2]:", n2["widgets_values"][2])
    print("\nOK - node 3 updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
