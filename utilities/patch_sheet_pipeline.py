#!/usr/bin/env python
"""1) Strip character-attribute re-descriptions from sheet prompts (identity = ref image ONLY).
2) 09j Qwen CLIP: int8_convrot -> fp8_scaled (strongest on-disk clip, zero download).
Both copies of each file. Asserts each old string appears exactly once."""
import json

BASES = [
    r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows",
    r"D:\models\vsCodeMcp\challenge\consistent-short\workflows",
]

ATTR_OLD = "<CHARACTER> character from <Picture 1> — a ~26-year-old Indian man, wavy medium-length black hair, a small patchy short beard, slim build, medium-brown Indian skin."
ATTR_NEW = "<CHARACTER> = the exact man from <Picture 1> — face, hair, beard, skin and build come ONLY from <Picture 1> (the image is the sole identity source — do not add or alter any character attributes)."

QWEN_555_OLD = "the man from the reference image, keep his exact face, wavy medium-length black hair, small patchy short beard, slim build."
QWEN_555_NEW = "the man from the reference image — face, hair, beard, skin and build EXACTLY as in the reference image (the image is the sole identity source — do not add or alter any character attributes)."

# (filename, [(location, old, new)])
PATCHES = {
    "05d_charsheet_H3_wide_jaisal.json": [("28 widget0", ATTR_OLD, ATTR_NEW)],
    "05e_charsheet_H3_fizgig_jaisal.json": [("28 widget0", ATTR_OLD, ATTR_NEW)],
    "09j_QWEN21_JAISAL_sheet.json": [("555 widget0", QWEN_555_OLD, QWEN_555_NEW)],
}

for base in BASES:
    # main-canvas prompt patches
    for fname, specs in PATCHES.items():
        p = f"{base}\\{fname}"
        j = json.load(open(p, encoding="utf-8"))
        for loc, old, new in specs:
            nid = int(loc.split()[0])
            for n in j["nodes"]:
                if n["id"] == nid:
                    cnt = n["widgets_values"][0].count(old)
                    assert cnt == 1, f"{fname} {loc}: x{cnt}"
                    n["widgets_values"][0] = n["widgets_values"][0].replace(old, new)
        # 09j subgraph CLIP upgrade
        if fname == "09j_QWEN21_JAISAL_sheet.json":
            for sg in j["definitions"]["subgraphs"]:
                for n in sg["nodes"]:
                    if n["id"] == 453:
                        assert n["widgets_values"][0] == "qwen3vl_8b_int8_convrot.safetensors", n["widgets_values"]
                        n["widgets_values"][0] = "qwen3vl_8b_fp8_scaled.safetensors"
                        print(f"  CLIP -> {n['widgets_values'][0]}")
        json.dump(j, open(p, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        print("patched", p)
print("all done")
