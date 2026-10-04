"""Wait for ComfyUI to come back up after restart, then verify ApplyKrea2NegPiP is registered.

Run:
  & "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\python.exe" "d:\\models\\vsCodeMcp\\utilities\\wait_and_verify_negpip.py"
"""
import json, time, urllib.request, sys

URL = "http://127.0.0.1:8188/object_info"
deadline = time.time() + 180  # up to 3 min for startup
last_err = None
d = None
while time.time() < deadline:
    try:
        d = json.load(urllib.request.urlopen(URL, timeout=30))
        break
    except Exception as e:
        last_err = e
        time.sleep(5)

if d is None:
    print("SERVER DID NOT COME UP in time. last error:", last_err)
    sys.exit(1)

print("SERVER UP. total nodes:", len(d))
print("ApplyKrea2NegPiP present:", "ApplyKrea2NegPiP" in d)
print("NegPipPrompt present (vendored pack still alive):", "NegPipPrompt" in d)

# show the ApplyKrea2NegPiP schema
if "ApplyKrea2NegPiP" in d:
    print("\nApplyKrea2NegPiP INPUT_TYPES:")
    print(json.dumps(d["ApplyKrea2NegPiP"].get("input", {}), indent=1))
