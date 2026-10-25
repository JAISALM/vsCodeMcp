"""Read obvpm node docs: Unbundle, Bundle, LoadImagesCompose from object_info."""
import urllib.request, json

d = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=60))
for name in ("Unbundle (obvpm)", "Bundle (obvpm)", "LoadImagesCompose (obvpm)"):
    n = d.get(name)
    if not n:
        print(f"== {name}: NOT FOUND")
        continue
    print(f"== {name} ==")
    for k, v in n.get("input", {}).get("required", {}).items():
        print(f"  req {k}: {json.dumps(v)[:200]}")
    for k, v in n.get("input", {}).get("optional", {}).items():
        print(f"  opt {k}: {json.dumps(v)[:200]}")
    print(f"  output: {n.get('output')}")
    desc = n.get("description")
    if desc:
        print(f"  desc: {str(desc)[:400]}")
    print()
