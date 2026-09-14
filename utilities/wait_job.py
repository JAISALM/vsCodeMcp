import urllib.request, json, sys, time
pid = sys.argv[1]
timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 300
deadline = time.time() + timeout
while time.time() < deadline:
    try:
        r = urllib.request.urlopen(f'http://127.0.0.1:8188/history/{pid}', timeout=30)
        d = json.load(r)
        if d:
            for v in d.values():
                st = v.get('status', {})
                print('status:', st.get('status_str'), 'completed:', st.get('completed'))
                for k, out in v.get('outputs', {}).items():
                    print('node', k, out)
                sys.exit(0)
    except Exception as e:
        pass
    time.sleep(10)
print('TIMEOUT - not done yet')
