import json, urllib.request, urllib.parse, time

def search(query, limit=15):
    # try different param combos
    for params in [
        {"query": query, "limit": limit},
        {"query": query, "limit": limit, "type": "LoRA"},
    ]:
        url = "https://civitai.com/api/v1/models?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())
            break
        except Exception as e:
            last_err = e
            continue
    else:
        print(f"ERROR for {query!r}: {last_err}")
        return
    print(f"\n===== QUERY: {query} ({data.get('count', '?')} results) =====")
    for m in data.get("items", []):
        name = m.get("name", "?")
        model_id = m.get("model", {}).get("id", "?")
        rating = m.get("stats", {}).get("rating", 0)
        downloads = m.get("stats", {}).get("downloadCount", 0)
        tags = [t if isinstance(t, str) else t.get("name", "?") for t in m.get("tags", [])][:10]
        print(f"  {name}  [id={model_id}] rating={rating} dl={downloads}")
        print(f"    tags: {', '.join(tags)}")

for q in ["krea 2", "krea2", "krea 2 line art", "krea 2 sketch", "krea 2 vector", "krea 2 style"]:
    search(q)
    time.sleep(1)
