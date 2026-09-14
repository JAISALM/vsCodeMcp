"""
Update krea2_kf3b_head180.json:
- node 84 positive prompt -> the user's WORKING head-replacement prompt
  (frames it as a head REPLACEMENT, not a rotation, + B&W scene context).
- node 113 (2nd ref) is already pointed at jaisal_face_mono_closeup.png.
- node 79 stays [3, 1, fit] (face ref boosted at 3, scene at 1).
"""
import json

wf = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\krea2_kf3b_head180.json"
j = json.load(open(wf, encoding="utf-8"))

new_prompt = (
    "Replace only the head with a frontal view of the same man's face. "
    "The face is looking directly into the camera. "
    "Keep the head attached to the same neck position and keep the body, "
    "shoulders and torso facing completely away from the camera. "
    "The man's back remains toward the camera; only his face is visible "
    "because his head has rotated fully around. "
    "The front of the face is perfectly centered and parallel to the camera. "
    "Both eyes are clearly visible and symmetrical. "
    "Preserve the original body, clothing, table, chair, bulb, lighting, "
    "composition and background exactly. "
    "Black and white high-contrast cinematic photograph, a single bare bulb "
    "hanging above, a pure black void background. "
    "There is ONLY ONE man in the frame."
)

for n in j["nodes"]:
    if n["id"] == 84:
        print("BEFORE len:", len(n["widgets_values"][0]))
        n["widgets_values"][0] = new_prompt
        if "widgets_values_named" in n and n["widgets_values_named"]:
            n["widgets_values_named"]["prompt"] = new_prompt
        print("AFTER  len:", len(n["widgets_values"][0]))

json.dump(j, open(wf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved")
