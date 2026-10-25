#!/usr/bin/env python
"""Logo v2: monochrome spec — white fill + black separator lines (no colors), all 4 branches."""
import json

p = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\logo_fists_compare.json"

P_H3_1FIST = """iintegrated_multimodal_description:

subject_definitions:
<EML> a monochrome flat vector sports-club emblem: exactly ONE single raised clenched fist inside a thin white circle (roundel), like the central fist in <Picture 1> — but in WHITE FILL ONLY: the entire fist and forearm are solid white with a clean black outline, NO colors at all (no red, no green, no colored fills). Where colored zones would be, thin black separator lines are used instead: thin black lines across the knuckles separating all four fingers and the thumb, and two thin black horizontal lines across the forearm dividing it into three white zones.
<Picture 1> is the SHAPES and LAYOUT reference for <EML> — its colors are ignored completely.

summary:
[reference generation] static image of a single clean flat vector emblem, keep the exactly same flat vector art style and line weight of <Picture 1>.

retention_analysis:
<Picture 1>: partially_preserved — only the fist shape, layout and line style are copied; all colors are replaced by white fill + thin black separator lines.
<EML>: fully_preserved — rendered on a new plain royal blue background, no other elements.

detailed_description:
The target image is a single static image: one monochrome flat vector sports-club emblem <EML> centered on a solid plain royal blue background (the same royal blue as a soccer jersey). Exactly ONE raised clenched fist (the middle one from <Picture 1>) enclosed in a thin white circle (roundel). The fist and forearm are SOLID WHITE FILL with a clean black outline — no red, no green, no other colors anywhere. Thin black separator lines where colored zones would be: thin black lines across the knuckles separating all four fingers and the thumb (all five clearly visible), and two thin black horizontal lines across the forearm dividing the white forearm into three equal zones. Crisp sharp edges, flat 2D vector logo style, even lighting, no gradients, no drop shadows. Only one fist in the image — no other hands, no duplicates. NO text, NO letters, NO words, NO numbers anywhere. The roundel fills about 70% of the image, perfectly centered, plenty of plain royal blue space around it.

overall_soundscape: N/A

non_diegetic_music: N/A
"""

P_H3_3FIST = """iintegrated_multimodal_description:

subject_definitions:
<EML> a monochrome flat vector sports-club emblem: exactly three raised clenched fists side by side, like the resistance/solidarity symbol in <Picture 1> — the middle fist slightly taller and in front, the outer two slightly behind and lower. Each fist in WHITE FILL ONLY: solid white hand and forearm with a clean black outline, NO colors at all (no red, no green, no colored fills). Where colored zones would be, thin black separator lines are used instead: thin black lines across the knuckles separating all four fingers and the thumb, and two thin black horizontal lines across each forearm dividing it into three white zones.
<Picture 1> is the SHAPES and LAYOUT reference for <EML> — its colors are ignored completely.

summary:
[reference generation] static image of a single clean flat vector emblem, keep the exactly same flat vector art style and line weight of <Picture 1>.

retention_analysis:
<Picture 1>: partially_preserved — only the fist shapes, layout and line style are copied; all colors are replaced by white fill + thin black separator lines.
<EML>: fully_preserved — rendered on a new plain royal blue background, no other elements.

detailed_description:
The target image is a single static image: one monochrome flat vector sports-club emblem <EML> centered on a solid plain royal blue background (the same royal blue as a soccer jersey). Three raised clenched fists in a row, middle fist slightly larger and in front, exactly as in <Picture 1>. All fists and forearms are SOLID WHITE FILL with clean black outlines — no red, no green, no other colors anywhere. Thin black separator lines where colored zones would be: thin black lines across the knuckles separating all four fingers and the thumb (all five clearly visible on every fist), and two thin black horizontal lines across each forearm dividing it into three white zones. Crisp sharp edges, flat 2D vector logo style, even lighting, no gradients, no drop shadows. NO text, NO letters, NO words, NO numbers anywhere. The emblem fills about 70% of the image, perfectly centered, plenty of plain royal blue space around it.

overall_soundscape: N/A

non_diegetic_music: N/A
"""

P_QWEN_1FIST = """Monochrome flat vector sports-club emblem logo: one single raised clenched fist enclosed in a thin white circle (roundel). The fist and forearm are SOLID WHITE FILL with a clean black outline — NO colors at all (no red, no green, no colored fills). Thin black separator lines where colored zones would be: thin black lines across the knuckles separating all four fingers and the thumb (all five clearly visible), and two thin black horizontal lines across the forearm dividing it into three white zones. Perfectly centered on a solid plain royal blue background. Flat 2D vector logo style, crisp sharp edges, even lighting, no gradients, no shadows, only one fist, no duplicates. NO text, NO letters, NO words, NO numbers."""

P_QWEN_3FIST = """Monochrome flat vector sports-club emblem logo: exactly three raised clenched fists side by side (solidarity / resistance symbol), the middle fist slightly taller and in front. Each fist and forearm SOLID WHITE FILL with a clean black outline — NO colors at all (no red, no green, no colored fills). Thin black separator lines where colored zones would be: thin black lines across the knuckles separating all four fingers and the thumb (all five clearly visible on every fist), and two thin black horizontal lines across each forearm dividing it into three white zones. Perfectly centered on a solid plain royal blue background. Flat 2D vector logo style, crisp sharp edges, even lighting, no gradients, no shadows. NO text, NO letters, NO words, NO numbers."""

j = json.load(open(p, encoding="utf-8"))
byid = {n["id"]: n for n in j["nodes"]}
byid[903]["widgets_values"][0] = P_H3_1FIST
byid[902]["widgets_values"][0] = P_H3_3FIST
byid[957]["widgets_values"][0] = P_QWEN_1FIST
byid[956]["widgets_values"][0] = P_QWEN_3FIST
json.dump(j, open(p, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
print("prompts updated (902/903 H3, 956/957 Qwen) — monochrome white-fill spec")
