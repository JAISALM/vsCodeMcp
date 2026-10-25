#!/usr/bin/env python
import json, urllib.request
raw = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info/ImageResizeKJv2", timeout=60))
print("top keys:", list(raw.keys())[:10])
n = raw.get("ImageResizeKJv2", raw)
print("node keys:", list(n.keys()))
print(json.dumps(n, indent=1)[:3000])
