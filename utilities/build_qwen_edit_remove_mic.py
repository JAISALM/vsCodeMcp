"""Clone the WORKING qwen_edit_small_mic.json (Qwen-Image-Edit-2509 dedicated
editing model) -> qwen_edit_remove_mic.json. Swap only:
  node 1  LoadImage image: mic+paper.png -> mic_small_id_00001_.png
  node 5  positive: remove the black mic, keep the small silver mic
  node 10 negative
  node 9  SaveImage prefix: jaisal_cut/mic_single
Everything else (UnetLoaderGGUF Qwen-Image-Edit-2509-Q8_0.gguf,
CLIPLoader qwen_2.5_vl_7b_fp8_scaled type qwen_image, VAEEncode,
KSampler denoise 1.0, VAEDecode) stays EXACTLY as the working file.
"""
import json
import os

WF = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows"
SRC = os.path.join(WF, "qwen_edit_small_mic.json")
DST = os.path.join(WF, "qwen_edit_remove_mic.json")

POS = ("Remove the black microphone on the right side of the table completely. "
       "Keep ONLY the small silver microphone on its short low stand, exactly as it is, "
       "unchanged. The area where the black microphone was becomes plain empty "
       "weathered wooden table surface, matching the surrounding wood grain and "
       "lighting exactly. Keep EVERYTHING ELSE exactly the same: the wooden table, "
       "the empty chair, the floating sheets of paper, the bare bulb, the pure "
       "black void background. Black-and-white high-contrast cinematic style, "
       "fine film grain. No other changes.")
NEG = ("microphone, mic, mic stand, black microphone, two microphones, extra "
       "objects, person, a boy, color, any color, text, watermark, glowing "
       "effects, holograms, fire, smoke")

d = json.load(open(SRC, encoding="utf-8"))
for n in d["nodes"]:
    if n["id"] == 1:
        n["widgets_values"][0] = "mic_small_id_00001_.png"
    elif n["id"] == 5:
        n["widgets_values"][0] = POS
    elif n["id"] == 10:
        n["widgets_values"][0] = NEG
    elif n["id"] == 9:
        n["widgets_values"][0] = "jaisal_cut/mic_single"

d["id"] = "qwen-edit-remove-mic"
json.dump(d, open(DST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("WROTE", DST)
