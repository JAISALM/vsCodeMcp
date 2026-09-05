import urllib.request, json

base = "http://127.0.0.1:8188"

def get(path):
    return json.load(urllib.request.urlopen(base + path))

q = get("/queue")
running = q.get("queue_running", [])
pending = q.get("queue_pending", [])
print(f"queue_running: {len(running)}   queue_pending: {len(pending)}")

for pid in running:
    print(f"  RUNNING prompt_id={pid}")

# recent history
try:
    h = get("/history?max_items=5")
    print(f"\nrecent history: {len(h)}")
    for k, v in list(h.items())[:5]:
        st = v.get("status", {})
        print(f"  {k[:16]}  {st.get('status_str','')}  completed={st.get('completed', st.get('status', False))}")
except Exception as e:
    print("history error:", e)
