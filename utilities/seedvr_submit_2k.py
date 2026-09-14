r"""Submit kf5 + kf6 plant keyframes to SeedVR2 Studio for 2K upscale.

Usage:
    & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\seedvr_submit_2k.py"

Writes job IDs to d:\models\vsCodeMcp\data\seedvr_submit.txt
"""
import urllib.request, json, uuid, os, sys

OUT = r"d:\models\vsCodeMcp\data\seedvr_submit.txt"
API = "http://127.0.0.1:7870"

IMAGES = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut\kf5_plants_alive_v9_00004_.png",
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\jaisal_cut\kf6_plants_dead_v9_00004_.png",
]

FIELDS = [
    ("job_type", "full"),
    ("backend_name", "SeedVR2 + TensorRT"),
    ("output_preset", "2K / 1440p"),
    ("crop_policy", "Preserve original aspect ratio"),
    ("resolution", "1440"),
    ("max_resolution", "2560"),
    ("batch_size", "21"),
    ("seed", "42"),
    ("model_label", "7B Sharp FP16 \u2014 maximum quality"),
    ("color_correction", "none"),
    ("attention_mode", "sageattn_2"),
    ("blocks_to_swap", "0"),
    ("vae_tiling", "false"),
    ("stop_before_vae", "false"),
    ("sharpen_enabled", "false"),
    ("sharpen_strength", "0.25"),
    ("grain_enabled", "false"),
    ("grain_intensity", "0.02"),
    ("grain_saturation", "0.5"),
    ("microtexture_enabled", "false"),
    ("microtexture_strength", "0.60"),
    ("skin_finishing_enabled", "false"),
    ("skin_evenness", "0.25"),
    ("skin_smoothing", "0.20"),
    ("skin_redness", "0.15"),
    ("skin_shine", "0.15"),
    ("blemish_mode", "off"),
    ("preserve_marks", "true"),
    ("seam_mode", "match"),
    ("seam_frames", "2"),
    ("chunked_render", "false"),
    ("chunk_seconds", "0"),
    ("decoder_mode", "optimized_fast"),
    ("source_fps", "0"),
]


def submit(path, out):
    boundary = "----seedvr" + uuid.uuid4().hex
    fname = os.path.basename(path)
    data = open(path, "rb").read()
    body = b""
    for k, v in FIELDS:
        body += ("--" + boundary + "\r\nContent-Disposition: form-data; name=\"" + k + "\"\r\n\r\n" + str(v) + "\r\n").encode("utf-8")
    body += ("--" + boundary + "\r\nContent-Disposition: form-data; name=\"file\"; filename=\"" + fname + "\"\r\nContent-Type: image/png\r\n\r\n").encode("utf-8")
    body += data + ("\r\n--" + boundary + "--\r\n").encode("utf-8")
    req = urllib.request.Request(API + "/api/jobs", data=body,
                                 headers={"Content-Type": "multipart/form-data; boundary=" + boundary})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=30))
        out.write("OK " + fname + " -> job " + r["id"] + "\n")
    except Exception as e:
        out.write("ERR " + fname + " " + str(e) + "\n")
        if hasattr(e, "read"):
            out.write(e.read().decode("utf-8", "ignore")[:500] + "\n")
    out.flush()


def main():
    out = open(OUT, "w")
    for p in IMAGES:
        if not os.path.exists(p):
            out.write("MISSING " + p + "\n")
            out.flush()
            continue
        submit(p, out)
    out.write("DONE\n")
    out.close()
    print(open(OUT).read())


if __name__ == "__main__":
    main()
