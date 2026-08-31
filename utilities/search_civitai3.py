import json, urllib.request, urllib.parse, time

def search(query, limit=15):
    url = "https://civitai.com/api/v1/models?" + urllib.parse.urlencode({"query": query, "limit": limit})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def show(m):
    name = m.get("name", "?")
    model_id = m.get("model", {}).get("id", "?")
    dl = m.get("stats", {}).get("downloadCount", 0)
    tags = [t if isinstance(t, str) else t.get("name", "?") for t in m.get("tags", [])][:12]
    print(f"\n### {name}  [model_id={model_id}] dl={dl}")
    print(f"    tags: {', '.join(tags)}")
    for v in m.get("modelVersions", [])[:3]:
        print(f"    version: {v.get('name')} (id={v.get('id')})")
        for f in v.get("files", [])[:4]:
            print(f"      file: {f.get('name')}  type={f.get('type')}  {f.get('sizeKB',0)//1024}MB  url={f.get('downloadUrl','')[:80]}")

# targeted searches for the best candidates
targets = [
    "Krea2 Line Art Style",
    "Krea2 Coloring Book",
    "Friendly Sketch Krea2",
    "Simple Fine Vector Krea2",
    "Krea 2 Official Loras",
    "Wanderer's Sketch Style",
]
for t in targets:
    data = search(t, limit=5)
    items = data.get("items", [])
    if not items:
        print(f"\n===== {t}: NO RESULTS =====")
        continue
    print(f"\n===== SEARCH: {t} =====")
    # pick the best match (name contains key words)
    for m in items[:3]:
        show(m)
    time.sleep(1)
