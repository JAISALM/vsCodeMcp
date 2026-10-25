import os, io
def safe(s): return s.encode("cp1252","replace").decode("cp1252")
out = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"
cand = [
  r"output\refset_v6\zidane_bench_b25_00001_.png",
  r"output\refset_v6\zidane_bench_00001_.png",
  r"output\refset_v7\zidane_t2i_b.png",
  r"output\krea2_char2_face_a_00001_.png",
]
# also glob char2 face + zidane refs
import glob
for pat in [r"output\refset_v6\zidane*", r"output\refset_v7\zidane*", r"output\krea2_char2_face*", r"output\refset_v7\jaisal_face_lock*"]:
    for f in sorted(glob.glob(os.path.join(out, pat))):
        print("%8d  %s" % (os.path.getsize(f), safe(os.path.relpath(f, out))))
