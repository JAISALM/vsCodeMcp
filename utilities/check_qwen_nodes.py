#!/usr/bin/env python
"""Check object_info availability for all node types in the new Qwen workflow."""
import json, urllib.request

raw = urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60).read().decode("utf-8", "replace")
names = ["QwenImage21Cache", "ModelAttentionBackend", "VAEDeGrid", "TextEncodeQwenImage21",
         "ImageResizeKJv2", "ThinkingLLM_QwenVL_GGUF_Advanced", "ThinkingLLM_QwenVL_Advanced",
         "ImageStitch", "SaveImageAdvanced", "PrimitiveString", "FloatConstant",
         "StringReplace", "PrimitiveStringMultiline", "ResolutionSelector", "PreviewAny",
         "UNETLoader", "CLIPLoader", "VAELoader", "KSampler", "EmptyLatentImage", "LoadImage"]
for name in names:
    idx = raw.find('"' + name + '"')
    print(("OK  " if idx >= 0 else "MISS"), name)
