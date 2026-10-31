# -*- coding: utf-8 -*-
"""
Prep Fizgig LoRA-Isolation dataset for Jaisal + Zidhan (2026-10-31, D209).

Source:  E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input\lora_{jaisal,zidhan}\
         (20 pairs each, trigger-first captions from the v91 v2 run 10/31)
Targets: D:\lora_training\jaisal_3110\  (trigger jeskv  -> fused jeskvman)
         D:\lora_training\zidane_3110\   (trigger dlor   -> fused dlorman)

Caption transform (Fizgig MULTI_PERSON rule 2: "trigger, comma, what they are"):
  old:  jeskvman, Kerala (South Indian) man, about 26, ...
  new:  jeskv, a man, Kerala (South Indian) man, about 26, ...
Everything after the old trigger is kept VERBATIM (identity head + scene).
caption_trigger() auto-detects the folder trigger from the first word of >=50%
of captions, so no manual trigger entry is needed on the Captions tab.

Also prefills the Fizgig state files so the user only has to click Start:
  user_data\prefs.json      input_dataset_dir -> jaisal_3110
  user_data\web_state.json  krea2 + last_run blocks:
      LORA_NAME krea2chars_v3, rank 16/16, 20 epochs, 0.5 MP,
      subjects jaisal_3110 + zidane_3110 (isolation + DOP stay on),
      image_folder -> jaisal_3110, samples every 2 epochs
  user_data\last_used.json  folder_triggers (explicit, belt-and-braces)
"""
import json, os, shutil, re

SRC = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\input"
DST = r"D:\lora_training"
FZ = r"D:\tools\Fizgig\user_data"

CHARS = {
    "jaisal": {"new": "jeskv", "old": "jeskvman", "dir": "jaisal_3110"},
    "zidhan": {"new": "dlor",  "old": "dlorman",  "dir": "zidane_3110"},
}

# ---------------- dataset ----------------
for char, cfg in CHARS.items():
    src_dir = os.path.join(SRC, "lora_%s" % char)
    dst_dir = os.path.join(DST, cfg["dir"])
    os.makedirs(dst_dir, exist_ok=True)
    n_img = n_txt = 0
    for fn in sorted(os.listdir(src_dir)):
        if not fn.lower().endswith((".png", ".jpg")):
            continue
        stem = os.path.splitext(fn)[0]
        png = os.path.join(src_dir, fn)
        shutil.copy2(png, os.path.join(dst_dir, fn))
        n_img += 1
        txt = os.path.join(src_dir, stem + ".txt")
        if not os.path.exists(txt):
            continue
        cap = open(txt, encoding="utf-8", errors="replace").read().strip()
        # swap the leading fused trigger for "trigger, a man" (fusion-friendly head)
        m = re.match(r"^\s*%s\s*," % re.escape(cfg["old"]), cap, re.I)
        if m:
            rest = cap[m.end():].lstrip(" ,")
            newcap = "%s, a man, %s" % (cfg["new"], rest)
        else:
            # fall back: keep the caption, just ensure the trigger word is first
            newcap = "%s, a man, %s" % (cfg["new"], cap)
        open(os.path.join(dst_dir, stem + ".txt"), "w", encoding="utf-8").write(newcap)
        n_txt += 1
    print("%-8s -> %s : %d images, %d captions" % (char, cfg["dir"], n_img, n_txt))
    # show one sample caption
    sample = open(os.path.join(dst_dir, sorted(f for f in os.listdir(dst_dir) if f.endswith(".txt"))[0]), encoding="utf-8").read()
    print("   sample: %s" % sample[:150])

# ---------------- prefs.json ----------------
prefs_p = os.path.join(FZ, "prefs.json")
prefs = json.load(open(prefs_p, encoding="utf-8"))
prefs["input_dataset_dir"] = os.path.join(DST, "jaisal_3110")
json.dump(prefs, open(prefs_p, "w", encoding="utf-8"), indent=2)
print("prefs.json: input_dataset_dir ->", prefs["input_dataset_dir"])

# ---------------- web_state.json ----------------
ws_p = os.path.join(FZ, "web_state.json")
ws = json.load(open(ws_p, encoding="utf-8"))

PATCH = {
    "LORA_NAME": "krea2chars_v3",
    "NETWORK_DIM": 16,
    "NETWORK_ALPHA": 16,
    "MAX_TRAIN_EPOCHS": 20,
    "DATASET_MEGAPIXELS": "0.5",
    "SAVE_EVERY_N_EPOCHS": 1,
    "FAMILY_CONCEPT_DIR": os.path.join(DST, "zidane_3110"),
    "SAMPLE_EVERY_N_EPOCHS": "2",
}
for block in (ws["values"].get("krea2"), ws.get("last_run", {}).get("values")):
    if block:
        block.update(PATCH)
ws["image_folder"] = os.path.join(DST, "jaisal_3110")
ws["last_run"]["image_folder"] = os.path.join(DST, "jaisal_3110")
ws.setdefault("prep", {})["mp"] = "0.5"
json.dump(ws, open(ws_p, "w", encoding="utf-8"), indent=2)
print("web_state.json: krea2 block patched (rank16 / 20ep / 0.5MP / 2 subjects / samples q2)")
print("  image_folder =", ws["image_folder"])
print("  subject2     =", ws["values"]["krea2"]["FAMILY_CONCEPT_DIR"])
print("  people_mode  =", ws["values"]["krea2"].get("FAMILY_PEOPLE_MODE"))
print("  DOP/multi    =", ws["values"]["krea2"].get("FAMILY_DOP"), ws["values"]["krea2"].get("FAMILY_MULTI_PERSON"))

# ---------------- last_used.json (explicit folder triggers) ----------------
lu_p = os.path.join(FZ, "last_used.json")
lu = json.load(open(lu_p, encoding="utf-8"))
ft = lu.get("folder_triggers")
if not isinstance(ft, dict):
    ft = {}
ft[os.path.normcase(os.path.abspath(os.path.join(DST, "jaisal_3110")))] = "jeskv"
ft[os.path.normcase(os.path.abspath(os.path.join(DST, "zidane_3110")))] = "dlor"
lu["folder_triggers"] = ft
json.dump(lu, open(lu_p, "w", encoding="utf-8"), indent=2)
print("last_used.json: folder_triggers =", ft)
print("done")
