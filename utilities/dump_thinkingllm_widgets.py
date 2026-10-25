#!/usr/bin/env python
"""Get the EXACT widget order + defaults of ThinkingLLM_QwenVL_GGUF_Advanced from object_info."""
import json, urllib.request

d = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info/ThinkingLLM_QwenVL_GGUF_Advanced", timeout=90))
n = d.get("ThinkingLLM_QwenVL_GGUF_Advanced", d)
req = n["input"]["required"]
order = n["input_order"]["required"]
print("=== widget order (input_order.required) ===")
for i, k in enumerate(order):
    spec = req[k]
    default = spec[1].get("default") if (isinstance(spec, list) and len(spec) > 1 and isinstance(spec[1], dict)) else (spec[0] if isinstance(spec, list) and isinstance(spec[0], list) else spec)
    print(f"[{i}] {k}: {json.dumps(default)[:120] if not isinstance(default, list) else str(default)[:150]}")
print("\n=== link inputs (non-widget) ===")
for k in order:
    spec = req[k]
    if isinstance(spec, list) and spec and isinstance(spec[0], str) and spec[0] in ("IMAGE", "LATENT", "AUDIO", "MODEL", "CONDITIONING", "STRING", "MASK"):
        print(f"  {k}: {spec[0]}")
