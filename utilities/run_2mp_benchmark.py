"""
Standalone MiniMax H3 resolution benchmark — runs UNATTENDED (no agent/Qwen needed).

Workflow: t2v_beach_sprint_test.json (PURE T2V — no reference images; production workflows NOT touched)
          - beach/dune sprint prompt (node 138), 10s (node 132), save prefix video/T2V_Beach_Sprint_TEST
Sweeps:  1.0 / 1.5 / 2.0 MP (node 115 ResolutionSelector megapixels widget)
Output:  E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\video\T2V_Beach_Sprint_TEST_*.mp4
         + d:\models\vsCodeMcp\benchmark_results.txt (timing table)

PREREQUISITES (do these FIRST, in this order):
  1. STOP Qwen:   Stop-Process -Name llama-server
  2. ComfyUI must be RUNNING (run_nvidia_gpu.bat, --lowvram already removed)
  3. Run this:    & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\run_2mp_benchmark.py"

The script:
  - warns (but proceeds) if llama-server is still running
  - waits for ComfyUI to be reachable
  - for each MP: sets node 115, converts UI->API (comfy_cli.workflow_to_api),
    POSTs /prompt, polls /history until done, records wall time
  - prints a live progress line every 15s so you can see it is NOT stuck
  - writes benchmark_results.txt at the end
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8188"
WORKFLOW = r"E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\t2v_beach_sprint_test.json"
RESULTS = r"d:\models\vsCodeMcp\data\benchmark_results.txt"
RES_NODE_ID = 115          # ResolutionSelector
MP_VALUES = [1.0, 1.5, 2.0]
POLL_SEC = 15              # progress poll interval
HARD_TIMEOUT = 90 * 60    # per-run safety cap (2.5MP ~37min; 90min is generous)
CLIENT_ID = "bench-script"


def log(msg):
    print(time.strftime("[%H:%M:%S] ") + msg, flush=True)


def get(path, timeout=10):
    with urllib.request.urlopen(BASE + path, timeout=timeout) as r:
        return json.load(r)


def post(path, data, timeout=30):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def qwen_running():
    try:
        import subprocess
        out = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq llama-server.exe", "/NH"],
            text=True,
        )
        return "llama-server" in out
    except Exception:
        return False


def wait_for_comfyui():
    log("Waiting for ComfyUI at %s ..." % BASE)
    while True:
        try:
            get("/system_stats")
            log("ComfyUI reachable.")
            return
        except Exception as e:
            log("  not up yet (%s) — retrying in 10s" % e)
            time.sleep(10)


def set_resolution(workflow, mp):
    for n in workflow["nodes"]:
        if n["id"] == RES_NODE_ID:
            n["widgets_values"][1] = mp
            return
    raise RuntimeError("ResolutionSelector node %d not found" % RES_NODE_ID)


def convert(workflow, object_info):
    from comfy_cli.workflow_to_api import convert_ui_to_api
    return convert_ui_to_api(workflow, object_info)


def queue(api_prompt):
    r = post("/prompt", {"prompt": api_prompt, "client_id": CLIENT_ID})
    return r["prompt_id"]


def wait_for_completion(prompt_id):
    """Poll /history until the prompt appears with a terminal status."""
    start = time.time()
    last_print = 0.0
    while True:
        elapsed = time.time() - start
        if elapsed > HARD_TIMEOUT:
            return "TIMEOUT", elapsed
        try:
            hist = get("/history/" + prompt_id)
        except Exception:
            hist = {}
        if prompt_id in hist:
            entry = hist[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                msgs = status.get("messages", [])
                return "ERROR: %s" % json.dumps(msgs)[:500], elapsed
            if status.get("completed") or status.get("status_str") == "success":
                return "SUCCESS", elapsed
        now = time.time()
        if now - last_print >= POLL_SEC:
            last_print = now
            log("  ... still running (%.0fs elapsed)" % elapsed)
        time.sleep(5)


def main():
    log("=== MiniMax H3 resolution benchmark ===")
    if qwen_running():
        log("WARNING: llama-server (Qwen) IS RUNNING — it will hold GPU VRAM and")
        log("         the 2.0/2.5 MP runs may stall/OOM. Stop it first:")
        log("         Stop-Process -Name llama-server")
        time.sleep(10)
    wait_for_comfyui()

    workflow = json.load(open(WORKFLOW, encoding="utf-8"))
    object_info = get("/object_info", timeout=60)
    log("object_info loaded (%d node types)" % len(object_info))

    rows = []
    for mp in MP_VALUES:
        set_resolution(workflow, mp)
        api_prompt = convert(workflow, object_info)
        pid = queue(api_prompt)
        log("MP=%.1f  queued  prompt_id=%s" % (mp, pid[:12]))
        status, elapsed = wait_for_completion(pid)
        rows.append((mp, status, elapsed))
        log("MP=%.1f  %s  (%.0fs)" % (mp, status, elapsed))
        # free VRAM between runs
        try:
            post("/free", {"unload_models": True, "free_memory": True})
            log("  /free called (models unloaded)")
        except Exception as e:
            log("  /free failed: %s" % e)
        time.sleep(10)

    log("=== RESULTS ===")
    lines = ["MiniMax H3 resolution benchmark — %s" % time.strftime("%Y-%m-%d %H:%M"),
             "workflow: t2v_beach_sprint_test.json (PURE T2V, 10s, 20 steps, ref2va + turbo 4-step + SLA)",
             "",
             "MP    status    time"]
    for mp, status, elapsed in rows:
        m, s = divmod(int(elapsed), 60)
        lines.append("%-5.1f %-10s %02d:%02d" % (mp, status, m, s))
    report = "\n".join(lines)
    print(report)
    with open(RESULTS, "w", encoding="utf-8") as f:
        f.write(report + "\n")
    log("Results written to %s" % RESULTS)


if __name__ == "__main__":
    main()
