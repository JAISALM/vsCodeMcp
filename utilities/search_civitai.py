import json, urllib.request, urllib.parse, time

def search(query, limit=20):
    url = "https://civitai.com/api/v1/models?" + urllib.parse.urlencode({
        "query": query,
        "types": "LoRA",
        "limit": limit,
        "sort": "highest Rated",
    })
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
    except Exception as e:
        print(f"ERROR for {query!r}: {e}")
        return
    print(f"\n===== QUERY: {query} ({data.get('count', '?')} results) =====")
    for m in data.get("items", []):
        name = m.get("name", "?")
        model_id = m.get("model", {}).get("id", "?")
        rating = m.get("stats", {}).get("rating", 0)
        downloads = m.get("stats", {}).get("downloadCount", 0)
        tags = [t.get("name") for t in m.get("tags", [])][:8]
        print(f"  {name}  [id={model_id}] rating={rating} dl={downloads}")
        print(f"    tags: {', '.join(tags)}")
        for v in m.get("modelVersions", [])[:2]:
            for f in v.get("files", [])[:2]:
                print(f"    file: {f.get('name')} ({f.get('sizeKB', 0)//1024} MB) type={f.get('type')}")

for q in ["krea 2", "krea2", "krea 2 style", "krea 2 line art", "krea 2 sketch", "krea 2 vector"]:
    search(q, limit=10)
    time.sleep(1)
