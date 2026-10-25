#!/usr/bin/env python
"""After restart: confirm the PE-I2I GGUF is now in the ThinkingLLM model_name options."""
import json, time, urllib.request

for attempt in range(12):
    try:
        d = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info/ThinkingLLM_QwenVL_GGUF_Advanced", timeout=90))
        break
    except Exception as e:
        print(f"attempt {attempt+1}: {type(e).__name__}, waiting 10s...")
        time.sleep(10)
else:
    raise SystemExit("server never came up")

node = d.get("ThinkingLLM_QwenVL_GGUF_Advanced", d)
spec = node["input"]["required"]["model_name"]
opts = spec[0] if isinstance(spec, list) else spec
pe = [o for o in opts if "PE-I2I" in str(o)]
print("PE-I2I options:", pe)
print("total options:", len(opts))
