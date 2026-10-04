"""Shot A: make the bare bulb FULLY STATIC (user decision 2026-09-26).

Removes the oscillation ("The bare bulb swings gently") so A's last frame =
still bulb -> shot B (static) cuts seamlessly with NO motion discontinuity.

Edits node 138 (PrimitiveStringMultiline) of jaisal_intro_A_walkin.json:
  1. swing line -> bulb COMPLETELY STILL
  2. summary lock -> bulb NEVER moves for the ENTIRE shot incl. LAST frame
  3. negative -> add bulb swinging/oscillating/flickering/moving light

Backup: workflow_backups/jaisal_intro_A_walkin.json.pre_static_bulb.bak
Also prints shot B's bulb wording (read-only) so we know if B needs the same.
"""
import json
import shutil

WF_A = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_A_walkin.json"
WF_B = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\jaisal_intro_B_setup.json"
BAK = r"d:\models\vsCodeMcp\workflow_backups\jaisal_intro_A_walkin.json.pre_static_bulb.bak"

shutil.copy(WF_A, BAK)
wf = json.load(open(WF_A, encoding="utf-8"))
node = next(n for n in wf["nodes"] if n["id"] == 138)
p = node["widgets_values"][0]

old1 = "The bare bulb swings gently; a chair scrapes across the floor"
new1 = ("The bare bulb is COMPLETELY STILL (no swinging, no oscillation, no flicker, "
        "steady light); a chair scrapes across the floor")
assert old1 in p, "swing line not found"
p = p.replace(old1, new1)

old2 = "The room, table, chair and bulb stay EXACTLY the same so the cut to the next shot is seamless."
new2 = (old2 + " The bare bulb NEVER moves, swings, oscillates or flickers - it is a fixed, "
        "steady light source for the ENTIRE shot, including the LAST frame.")
assert old2 in p, "summary lock not found"
p = p.replace(old2, new2)

old3 = ("negative: color, multiple people, second person, duplicate character, extra chairs, "
        "extra figures, bright wall, white wall, cream wall, visible ceiling, text, subtitles, "
        "watermark, logo, the man standing, the man leaving, a second person")
new3 = old3 + ", bulb swinging, bulb oscillating, bulb flickering, moving light, swinging bulb, flickering light"
assert old3 in p, "negative line not found"
p = p.replace(old3, new3)

node["widgets_values"][0] = p
with open(WF_A, "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=1)
print("A prompt updated: bulb now FULLY STATIC. Backup:", BAK)

# --- read-only: shot B bulb wording ---
wfB = json.load(open(WF_B, encoding="utf-8"))
for n in wfB["nodes"]:
    for v in (n.get("widgets_values") or []):
        if isinstance(v, str) and len(v) > 200:
            for kw in ("bulb", "swings", "oscillat", "flicker"):
                i = v.find(kw)
                if i >= 0:
                    print(f"\nB node {n['id']} [{n['type']}] ...{v[max(0,i-60):i+120]}...")
                    break
