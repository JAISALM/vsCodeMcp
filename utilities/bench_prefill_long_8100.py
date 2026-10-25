"""Long-context prefill benchmark: ~20K-token prompt, minimal generation.
Reproduces a real agentic-session turn (big prompt) and shows why the
'average tok/s' drops far below the 200 tok/s decode rate."""
import json
import time
import urllib.request

# ~19K tokens of filler prompt
unit = "The quick brown fox jumps over the lazy dog near the river bank in Kerala. "
text = unit * 1200
body = {
    "model": "qwen",
    "messages": [{"role": "user", "content": text + "Now reply with exactly: OK"}],
    "max_tokens": 8,
    "temperature": 0.0,
    "stream": False,
}
req = urllib.request.Request(
    "http://127.0.0.1:8100/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json"},
)
t0 = time.time()
resp = json.loads(urllib.request.urlopen(req, timeout=600).read())
wall = time.time() - t0
usage = resp.get("usage", {})
timings = resp.get("timings", {})
print("usage:", usage)
pn, pm = timings.get("prompt_n", 0), timings.get("prompt_ms", 0)
gn, gm = timings.get("predicted_n", 0), timings.get("predicted_ms", 0)
print(f"wall clock: {wall:.1f}s")
if pm:
    print(f"LONG PREFILL: {pn} tok in {pm/1000:.2f}s = {pn/pm*1000:.0f} tok/s")
if gm:
    print(f"decode: {gn} tok in {gm/1000:.2f}s = {gn/gm*1000:.0f} tok/s")
# the number the UI likely shows: generated tokens / total wall time
if wall > 0 and gn:
    print(f"UI-style AVERAGE: {gn} gen tok / {wall:.1f}s total wall = {gn/wall:.0f} tok/s")
