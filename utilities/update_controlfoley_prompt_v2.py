"""ControlFoley prompt v2: REMOVE the continuous water/wind beds.

The v1 timed prompt still came out as a continuous noise bed. Hypothesis (user):
the CONTINUOUS water/wind descriptions ("distant river water", "calm quiet water",
"flowing river water") make the model fill the whole timeline with a water-noise
bed that masks the discrete action sounds.

v2 keeps ONLY the discrete action sounds (footsteps, whistle+throw, plane plop,
jump whoosh, land thud+second jump, splash) and explicitly tells the model the
background is quiet (no continuous water/wind bed). Continuous water/wind is also
added to the NEGATIVE prompt to suppress it.

This is a clean A/B test of the "water = noise" hypothesis.
Idempotent: safe to re-run.
"""
import json

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_sketch_title_audio.json"

# DISCRETE action sounds only. No continuous water/wind bed. Gaps stay quiet.
PROMPT = (
    "Natural ambient sounds only, synced to the video. A stick figure walks on a "
    "stone bridge over a river. The background is QUIET - no continuous water "
    "sound, no continuous wind, no ambient bed.\n"
    "0-2s: soft footsteps on stone as he walks.\n"
    "2-3s: a soft low whistle and the whoosh of a paper plane being thrown.\n"
    "6s: a soft plop as the paper plane touches the water.\n"
    "6-7s: a soft whoosh as the figure jumps over the guardrail.\n"
    "7-8s: a soft thud as he lands, then a whoosh as he jumps toward the water.\n"
    "9s: a soft splash as he lands in the water."
)

# Suppress continuous water/wind beds + the usual NO-music exclusions.
NEGATIVE_PROMPT = (
    "music, instrumental music, musical instruments, melody, beat, rhythm, "
    "soundtrack, song, dialogue, speech, talking, voice, loud sounds, harsh noise, "
    "distortion, static, electronic sounds, beeps, alarms, continuous water, "
    "flowing water, river sound, water ambience, constant water, white noise, "
    "hiss, constant ambient, continuous wind, wind bed."
)

DURATION = 15.0  # upper limit; the 00011 video is 14.33s


def main() -> int:
    wf = json.load(open(WF, encoding="utf-8"))
    node = next(n for n in wf["nodes"] if n["id"] == 3)
    assert node["type"] == "ControlFoleyGenerate", f"node 3 is {node['type']}, not ControlFoleyGenerate"

    wv = node["widgets_values"]
    print("BEFORE prompt[0]:", repr(wv[0][:60]))
    print("BEFORE negative[1]:", repr(wv[1][:60]))

    wv[0] = PROMPT
    wv[1] = NEGATIVE_PROMPT
    wv[2] = DURATION

    json.dump(wf, open(WF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    wf2 = json.load(open(WF, encoding="utf-8"))
    n2 = next(n for n in wf2["nodes"] if n["id"] == 3)
    print("\nAFTER prompt[0]:")
    print(n2["widgets_values"][0])
    print("\nAFTER negative[1]:", n2["widgets_values"][1])
    print("\nduration:", n2["widgets_values"][2])
    print("\nOK - node 3 updated to the no-water v2 prompt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
