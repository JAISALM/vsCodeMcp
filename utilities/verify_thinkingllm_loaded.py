#!/usr/bin/env python
"""Verify server restart loaded the ThinkingLLM pack nodes."""
import json, time, urllib.request

for attempt in range(12):
    try:
        raw = urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=90).read().decode("utf-8", "replace")
        break
    except Exception as e:
        print(f"attempt {attempt+1}: not up yet ({type(e).__name__}), waiting 10s...")
        time.sleep(10)
else:
    raise SystemExit("server never came up")

print("=== ThinkingLLM + H3 + KJ nodes ===")
for name in ["ThinkingLLM_QwenVL_GGUF_Advanced", "ThinkingLLM_QwenVL_GGUF",
             "ThinkingLLM_QwenVL_Advanced", "ThinkingLLM_QwenVL",
             "MiniMaxH3ReferenceToVideo", "FizgigH3StillDecode", "ImageResizeKJv2"]:
    print(("OK  " if raw.find('"' + name + '"') >= 0 else "MISS"), name)
