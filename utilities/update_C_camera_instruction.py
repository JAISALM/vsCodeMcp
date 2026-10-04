# -*- coding: utf-8 -*-
"""
Update shot C's CAMERA NODE (H3LocalCameraEditor) instruction widget with the
head-turn motion + Malayalam dialogue.

The camera node compiles the 3D trajectory into a prompt. The `instruction`
widget (widgets_values[3]) is appended as "Additional direction: ..." to that
prompt. We put the head-turn motion + Malayalam dialogue there so the subject
ACTS (head turns 180 degrees) while the camera orbits at the same rate.

The node source (experimental.py) was patched to allow subject motion + audio
(removed the 'Freeze the captured scene' + 'Silence.' defaults). See
experimental.py.bak_headturn for the original.

Run:
    cmd /c "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe D:\\models\\vsCodeMcp\\utilities\\update_C_camera_instruction.py"
"""
import json
from pathlib import Path

WF = Path(r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_C_headtwist_180.json")

INSTRUCTION = (
    "The boy <Subject 1> is seated at the table, seen from his LEFT side. "
    "His EYES shift first - his gaze turns toward the lens before anything else moves. "
    "Then his head rotates SLOWLY, deliberately, 180 degrees (from the left-back side to fully facing the camera) "
    "at exactly the same rate as the camera orbits, while his BODY stays still and lit the same. "
    "His eyes stay LOCKED on the lens the whole turn. "
    "As the head completes the turn, he speaks, quiet and a little uncertain: "
    "<Subject 1> (S1) says, <d>[Malayalam] <breath> \u0d10\u0d28\u0d4d\u0d24\u0d3e \u0d2a\u0d3e\u0d31\u0d10\u0d4d\u0d2f\u0d47\u0d28\u0d4d\u0d24\u0d4d \u0d12\u0d31\u0d3f\u0d2f\u0d3f\u0d33\u0d4d\u0d33... <pause> \u0d09\u0d4d\u0d35\u0d3f\u0d21\u0d41\u0d28\u0d4d\u0d28\u0d3e \u0d24\u0d41\u0d1f\u0d02\u0d17\u0d47\u0d28\u0d4d\u0d24\u0d4d \u0d09\u0d23\u0d3f\u0d31\u0d3f\u0d33\u0d4d\u0d33. <long pause> \u0d2a\u0d3e\u0d15\u0d4d\u0d37\u0d47... <inhale> \u0d07\u0d24\u0d3e\u0d28\u0d4d\u0d31 \u0d09\u0d1f\u0d23\u0d47 \u0d1f\u0d41\u0d21\u0d3e\u0d15\u0d02. <pause> \u0d38\u0d4b \u0d35\u0d47\u0d33\u0d4d\u0d15\u0d02 \u0d1f\u0d41 \u0d26\u0d3f \u0d1c\u0d3f\u0d33\u0d33\u0d4d \u0d15\u0d1f\u0d4d\u0d31\u0d4d. </d> "
    "Black & white, high contrast, fine film grain. The room, table, chair and single bare bulb stay exactly the same. "
    "ONLY ONE boy, no duplicates."
)


def main() -> int:
    d = json.loads(WF.read_text(encoding="utf-8"))
    found = False
    for n in d["nodes"]:
        if n["type"] == "H3LocalCameraEditor":
            print("Found camera node", n["id"])
            print("Old instruction (%d chars): %s..." % (len(n["widgets_values"][3]), n["widgets_values"][3][:60]))
            n["widgets_values"][3] = INSTRUCTION
            print("New instruction set (%d chars)" % len(INSTRUCTION))
            found = True
            break
    if not found:
        raise SystemExit("Camera node (H3LocalCameraEditor) not found")
    WF.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    print("Wrote", WF.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
