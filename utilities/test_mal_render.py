"""Quick test: does ffmpeg drawtext render Malayalam correctly with proper path escaping?"""
import subprocess, os

FFMPEG = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe"
OUT = r"D:\models\vsCodeMcp\Jaisal-intro\subs\cards"
os.makedirs(OUT, exist_ok=True)
tmp = os.path.join(OUT, "_txt")
os.makedirs(tmp, exist_ok=True)

mal = "എന്തുകൊണ്ടാണ AI യൂസ് ചെയ്തിട്ട് ഇത് ചെയ്യണമെന്ന് തോന്നിയത്"
mal_txt = os.path.join(tmp, "test_mal.txt")
with open(mal_txt, "w", encoding="utf-8") as f:
    f.write(mal)

# Forward slashes + escaped drive colon (Python "\\:" -> actual "\:")
fontfile = "C\\:/Windows/Fonts/arialuni.ttf"
textfile = mal_txt.replace("\\", "/").replace("D:", "D\\:")

vf = (
    f"drawtext=fontfile={fontfile}:textfile={textfile}:fontsize=110:fontcolor=white:"
    f"x=(w-text_w)/2:y=(h/2)-70"
)
out = os.path.join(OUT, "test_mal.png")
cmd = [
    FFMPEG, "-y",
    "-f", "lavfi", "-i", "color=c=black:s=2520x1440:d=1:r=24",
    "-vf", vf,
    "-frames:v", "1",
    out,
]
print("CMD filter:", vf)
r = subprocess.run(cmd, capture_output=True, text=True)
print("returncode:", r.returncode)
if r.returncode != 0:
    print(r.stderr[-1500:])
else:
    print("WROTE", out)
