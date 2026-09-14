import urllib.request, json, sys
pid = sys.argv[1]
try:
    r = urllib.request.urlopen(f'http://127.0.0.1:8188/history/{pid}', timeout=30)
    d = json.load(r)
    if not d:
        print('NOT DONE YET')
    else:
        for v in d.values():
            print('status:', v.get('status'))
            for k, out in v.get('outputs', {}).items():
                print('node', k, out)
except Exception as e:
    print('ERR', e)
