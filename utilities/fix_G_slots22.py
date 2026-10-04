"""Fix G_revolt MiniMax node slot mapping (deterministic, from frontend ground truth).

ROOT CAUSE: the saved workflow was created with an OLDER MiniMax H3 node (19 inputs).
The LIVE node has 22 inputs in a different order. The saved file's slot indices are
stale, so the frontend mis-maps links to the wrong slots -> type-clash errors:
  - slot 5 ref_image_2 (IMAGE) <- link 275 (INT from math)  -> clash
  - slot 7 ref_video_audio_0 (AUDIO) <- link 318 (IMAGE cricket bat) -> clash

FIX: rebuild the MiniMax node's inputs to the LIVE 22-slot order with the CORRECT
link fields, and set each link's to_slot to match. Verified by source type:
  link 272 CLIPLoader(CLIP) -> slot 0 clip
  link 273 VAELoader(VAE)   -> slot 1 vae
  link 274 VAELoader(VAE)   -> slot 2 audio_vae
  link 300 LoadImage137(IMAGE) -> slot 3 ref_image_0 (kf7a_v4)
  link 317 LoadImage139(IMAGE) -> slot 4 ref_image_1 (keyframe)
  link 318 LoadImage165(IMAGE) -> slot 5 ref_image_2 (cricket bat)
  link 319 LoadImage166(IMAGE) -> slot 16 ref_image_3 (soccer ball)
  link 320 LoadImage167(IMAGE) -> slot 17 ref_image_4 (paper smiley)
  link 275 MathExpr(INT)    -> slot 14 length
  link 279 PrimitiveString(STRING) -> slot 11 prompt
  link 276 ResolutionSelector(INT) -> slot 12 width
  link 277 ResolutionSelector(INT) -> slot 13 height
"""
import json, os, shutil

P = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_G_revolt.json"
BAK = P + ".pre22slot.bak"

d = json.load(open(P, encoding="utf-8"))
nodes = {n["id"]: n for n in d["nodes"]}
mm = [n for n in d["nodes"] if n["type"] == "MiniMaxH3ReferenceToVideo"][0]
mm_id = mm["id"]

# LIVE 22-slot order (ground truth from frontend) with correct link fields
correct = [
    ("clip", "CLIP", 272),
    ("vae", "VAE", 273),
    ("audio_vae", "VAE", 274),
    ("ref_images.ref_image_0", "IMAGE", 300),
    ("ref_images.ref_image_1", "IMAGE", 317),
    ("ref_images.ref_image_2", "IMAGE", 318),
    ("ref_videos.ref_video_0", "IMAGE", None),
    ("ref_video_audios.ref_video_audio_0", "AUDIO", None),
    ("ref_audios.ref_audio_0", "AUDIO", None),
    ("ref_audios.ref_audio_1", "AUDIO", None),
    ("ref_audios.ref_audio_2", "AUDIO", None),
    ("prompt", "STRING", 279),
    ("width", "INT", 276),
    ("height", "INT", 277),
    ("length", "INT", 275),
    ("ref_image_size", "COMBO", None),
    ("ref_images.ref_image_3", "IMAGE", 319),
    ("ref_images.ref_image_4", "IMAGE", 320),
    ("ref_videos.ref_video_1", "IMAGE", None),
    ("ref_videos.ref_video_2", "IMAGE", None),
    ("ref_video_audios.ref_video_audio_1", "AUDIO", None),
    ("ref_images.ref_image_5", "IMAGE", None),
]

# name -> existing input structure (preserve localized_name/widget/etc.)
old_by_name = {inp.get("name"): inp for inp in mm.get("inputs", [])}

new_inputs = []
for i, (name, itype, lid) in enumerate(correct):
    base = dict(old_by_name.get(name, {}))
    base["name"] = name
    base["type"] = itype
    base["link"] = lid
    base.setdefault("localized_name", name)
    new_inputs.append(base)
mm["inputs"] = new_inputs

# update links array to_slot (index 4) for links connected to mm
link_idx = {l[0]: i for i, l in enumerate(d["links"])}
to_slot_map = {lid: i for i, (_, _, lid) in enumerate(correct) if lid is not None}
changes = []
for lid, slot in to_slot_map.items():
    if lid in link_idx:
        li = link_idx[lid]
        old = d["links"][li][4]
        if old != slot:
            d["links"][li][4] = slot
            changes.append((lid, old, slot))

shutil.copy(P, BAK)
json.dump(d, open(P, "w", encoding="utf-8"), indent=1)
print(f"BACKUP -> {os.path.basename(BAK)}")
print(f"inputs rebuilt to {len(new_inputs)} slots")
print(f"to_slot changes ({len(changes)}):")
for lid, old, new in changes:
    print(f"  link {lid}: to_slot {old} -> {new}")
print("Saved.")
