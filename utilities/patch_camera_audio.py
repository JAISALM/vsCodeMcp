import io, os, py_compile, shutil

CAM = r'E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\custom_nodes\3d-Camera-control-H3-Minimax\camera.py'
BAK = CAM + '.bak_headturn'

# 1. Back up (only if no backup yet)
if not os.path.exists(BAK):
    shutil.copyfile(CAM, BAK)
    print("Backed up ->", BAK)
else:
    print("Backup already exists, leaving it:", BAK)

src = io.open(CAM, encoding='utf-8').read()

AMBIENT = "Natural ambient sound only - room tone, bulb hum, breath, his quiet voice. NO music."

replacements = [
    # sound field in the plan (this is what the compact-JSON prompt carries)
    ("        sound='Silence.',",
     "        sound='" + AMBIENT + "',"),
    # allow the head to turn (body stays still)
    ("        forbid='No cuts, subject rotation, subject animation, digital zoom, lighting changes, or visible planning annotations.',",
     "        forbid='No cuts, digital zoom, lighting changes, or visible planning annotations. The subject may turn the head as directed in the additional direction; the body stays still.',"),
    # relax the rigid-scene contract so the head turn is allowed
    ("        preserve='The scene and subjects remain rigid in world space: identity, pose, materials, lighting and physical contacts stay unchanged. Only the camera moves. Hold the captured instant: fire, smoke, water and particles keep their captured shapes and world positions; do not continue their motion.',",
     "        preserve='The scene remains in world space: identity, materials, lighting and physical contacts stay unchanged. The camera moves as directed. The subject may turn the head as directed in the additional direction; the body stays still.',"),
    # plan_text non-sections path
    ("        return text+'\\nSilence.'",
     "        return text+'\\n' + AMBIENT"),
    # plan_text H3-sections path
    ("'detailed_description:\\n'+text+'\\n\\noverall_soundscape:\\nSilence.\\n\\nnon_diegetic_music:\\nN/A'",
     "'detailed_description:\\n'+text+'\\n\\noverall_soundscape:\\n' + AMBIENT + '\\n\\nnon_diegetic_music:\\nNO music, natural ambient sounds only'"),
]

for old, new in replacements:
    count = src.count(old)
    if count != 1:
        print("!! expected exactly 1 occurrence, found", count, "for:", old[:60])
        raise SystemExit("Aborting - string not unique. No changes written.")
    src = src.replace(old, new)
    print("Replaced:", old[:50], "...")

io.open(CAM, 'w', encoding='utf-8').write(src)
print("Wrote", CAM)

# 2. Verify it still compiles
py_compile.compile(CAM, doraise=True)
print("COMPILE_OK")
