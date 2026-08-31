import urllib.request, json

BASE = 'http://127.0.0.1:8188'

def get(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=5) as r:
            return json.load(r)
    except Exception as e:
        return {'ERROR': str(e)}

def post(path, data):
    try:
        req = urllib.request.Request(BASE + path, data=json.dumps(data).encode(),
                                     headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status
    except Exception as e:
        return {'ERROR': str(e)}

print('=== GET /queue ===')
print(json.dumps(get('/queue'), indent=1)[:800])
print()
print('=== GET /system_stats (ram) ===')
ss = get('/system_stats')
dev = ss.get('devices', [{}])[0] if ss.get('devices') else {}
print('ram_total GB:', round(ss.get('system', {}).get('ram_total', 0)/1e9, 1))
print('ram_free  GB:', round(ss.get('system', {}).get('ram_free', 0)/1e9, 1))
print('vram_free GB:', round(dev.get('vram_free', 0)/1e9, 1))
print()
print('=== POST /free (dry check: does the endpoint accept it?) ===')
print('status:', post('/free', {'unload_models': False, 'free_memory': False}))
