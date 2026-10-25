"""Decode-only benchmark on the live 8100 server: short prompt, ~300-token generation.
Separates PREFILL (prompt eval) from DECODE (token generation) tok/s."""
import json
import time
import urllib.request

body = {
    "model": "qwen",
    "messages": [{"role": "user", "content": "List the prime numbers from 2 to 200, one per line. Nothing else."}],
    "max_tokens": 300,
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
print("timings:", timings)
pn, pm = timings.get("prompt_n", 0), timings.get("prompt_ms", 0)
gn, gm = timings.get("predicted_n", 0), timings.get("predicted_ms", 0)
print(f"wall clock: {wall:.1f}s")
if pm:
    print(f"PREFILL: {pn} tok in {pm/1000:.2f}s = {pn/pm*1000:.0f} tok/s")
if gm:
    print(f"DECODE:  {gn} tok in {gm/1000:.2f}s = {gn/gm*1000:.0f} tok/s")
