r"""Build black-screen question cards for the Jaisal intro (2026-09-30, v2).

The camera guy's questions are OFF-SCREEN in the clips (Jaisal's mouth closed).
Per user decision (D096 update 16): instead of holding a still frame, show a
BLACK SCREEN with the question text (Malayalam large + English below) as an
intentional "interviewer asks" beat.

WHY v2 (2026-09-30): v1 burned the text with ffmpeg's `subtitles` (libass)
filter, but this ffmpeg build's libass has NO HarfBuzz shaping, so Malayalam
COMBINING MARKS rendered as separate visible characters (e.g. "എന്താണ" ->
"എന്‌ത ാ ണ"). English was fine (no shaping needed). FIX: render the text with a
REAL shaping engine -- headless Edge/Chromium (full HarfBuzz) -- screenshot the
2520x1440 canvas to a PNG, then encode that PNG into the 3s card. Malayalam
shapes correctly; English stays clean.

Specs (match the completed upscaled clips):
  - 2520x1440, 24 fps, 3 seconds (72 frames) each
  - pure black background
  - Malayalam question centered (large, white, Kartika)
  - English translation below (smaller, grey, Arial)
  - H.264 yuv420p (DaVinci-friendly)

Output: D:\models\vsCodeMcp\Jaisal-intro\subs\cards\card_<shot>_<slug>.mp4

Assembly order in DaVinci (cards replace the off-screen question beats):
  A -> card_B -> B -> card_D -> D -> E -> card_F -> F1 -> F2 -> card_G -> G
"""
import subprocess, os, sys

FFMPEG = r"D:\ffmpeg\ffmpeg-2025-08-25-git-1b62f9d3ae-full_build\bin\ffmpeg.exe"
OUT = r"D:\models\vsCodeMcp\Jaisal-intro\subs\cards"
W, H, FPS, DUR = 2520, 1440, 24, 3

# Headless browser (full HarfBuzz shaping -> correct Malayalam).
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BROWSER = next((b for b in (EDGE, CHROME) if os.path.exists(b)), None)

# (shot, slug, malayalam, english)
CARDS = [
    ("B", "you_ready",
     "ആ പറഞ്ഞോ ..!",
     "Go ahead"),
    ("D", "purpose",
     "എന്താണ് ഈ ചാനൽ കൊണ്ട് ഉദ്ദേശിക്കുന്നത് ?",
     "What's the purpose of this channel?"),
    ("F", "why_ai",
     "എന്തുകൊണ്ടാണ് AI ഉപയോഗിച്ച് ഇത് ചെയ്യണമെന്ന് തോന്നിയത് ?",
     "Why did you feel like doing this using AI?"),
    ("G", "expect",
     "ഈ ചാനലിൽ നിന്ന് ആൾക്കാർക്ക് എന്തൊക്കെ പ്രതീക്ഷിക്കാം ?",
     "What can people expect from this channel?"),
]


HTML = """<!doctype html><html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;width:2520px;height:1440px;background:#000;
    overflow:hidden;}
  .wrap{width:2520px;height:1440px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;box-sizing:border-box;}
  .mal{font-family:'Kartika','Nirmala UI',sans-serif;font-size:110px;
    line-height:1.35;color:#ffffff;text-align:center;}
  .eng{font-family:Arial,sans-serif;font-size:52px;line-height:1.3;
    color:#aaaaaa;margin-top:40px;white-space:nowrap;text-align:center;}
</style>
<script>
window.addEventListener('load',function(){
  var el=document.querySelector('.mal');
  el.style.whiteSpace='nowrap';
  el.style.maxWidth='none';
  var w=el.scrollWidth;
  if(w<=2300){return;}
  var size=110;
  while(size>54&&w>2300){size-=4;el.style.fontSize=size+'px';w=el.scrollWidth;}
  if(w>2300){el.style.whiteSpace='normal';el.style.maxWidth='2300px';}
});
</script>
</head><body><div class="wrap">
  <div class="mal">{mal}</div>
  <div class="eng">{eng}</div>
</div></body></html>"""


def build(shot, slug, mal, eng):
    html = os.path.join(OUT, f"card_{shot}_{slug}.html")
    png = os.path.join(OUT, f"card_{shot}_{slug}.png")
    out = os.path.join(OUT, f"card_{shot}_{slug}.mp4")
    with open(html, "w", encoding="utf-8") as f:
        # .replace (not .format) -- the CSS braces would break .format().
        f.write(HTML.replace("{mal}", mal).replace("{eng}", eng))
    # Headless screenshot of the 2520x1440 canvas (device-scale 1 = 1:1 px).
    r = subprocess.run([
        BROWSER, "--headless=new", "--disable-gpu",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        "--virtual-time-budget=3000",
        f"--window-size={W},{H}", f"--screenshot={png}",
        f"file:///{html.replace(os.sep, '/')}",
    ], capture_output=True, text=True, timeout=90)
    if not os.path.exists(png) or os.path.getsize(png) < 1000:
        print(f"[{shot}] SCREENSHOT FAILED:\n" + (r.stderr or r.stdout)[-800:])
        return False
    # Encode the still PNG into a 3s H.264 card.
    r = subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", png,
        "-vf", f"scale={W}:{H}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-t", str(DUR), out,
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[{shot}] FFMPEG FAILED:\n" + r.stderr[-1200:])
        return False
    print(f"[{shot}] {slug}: {mal}  ->  {out}")
    return True


def main():
    os.makedirs(OUT, exist_ok=True)
    if not BROWSER:
        print("NO headless browser found (Edge/Chrome). Install one or set BROWSER.")
        sys.exit(1)
    print(f"Using browser: {BROWSER}\n")
    ok = 0
    for shot, slug, mal, eng in CARDS:
        if build(shot, slug, mal, eng):
            ok += 1
    print(f"\n{ok}/{len(CARDS)} cards built in {OUT}")
    sys.exit(0 if ok == len(CARDS) else 1)


if __name__ == "__main__":
    main()
