# mcp_validate.py — drive the local comfy-mcp stdio server to validate workflows.
# Usage: mcp_validate.py <workflow.json> [more.json ...]
# Launches the same exe VS Code uses (per .vscode/mcp.json), speaks MCP JSON-RPC
# over stdio, calls tools/list to discover the validate tool, then validates each file.
import json
import os
import subprocess
import sys

EXE = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy-mcp.exe"
ENV = dict(os.environ)
ENV["COMFY_BIN"] = r"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy.exe"


def main():
    files = sys.argv[1:]
    if not files:
        print("usage: mcp_validate.py <workflow.json> ...")
        sys.exit(2)

    p = subprocess.Popen([EXE], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=ENV)

    def send(obj):
        p.stdin.write((json.dumps(obj) + "\n").encode("utf-8"))
        p.stdin.flush()

    def read_response():
        while True:
            line = p.stdout.readline()
            if not line:
                return None
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except Exception:
                continue  # skip log noise
            if isinstance(msg, dict) and msg.get("id") is not None:
                return msg

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                     "clientInfo": {"name": "dsh-builder", "version": "1.0"}}})
    init = read_response()
    if not init or "result" not in init:
        print("INIT FAILED:", json.dumps(init)[:1000])
        sys.exit(1)
    print("server:", init["result"].get("serverInfo"))
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    tools_msg = read_response()
    tools = tools_msg["result"]["tools"]
    names = [t["name"] for t in tools]
    print("tools:", ", ".join(names))

    # find the validate tool
    vt = next((t for t in tools if "validate" in t["name"]), None)
    if vt is None:
        print("NO VALIDATE TOOL FOUND")
        sys.exit(1)
    print("validate tool schema:", json.dumps(vt.get("inputSchema", vt.get("inputSchema") or {}), indent=1)[:1500])

    # guess the workflow argument name from the schema
    props = (vt.get("inputSchema") or {}).get("properties", {})
    wf_arg = next((k for k in props if "workflow" in k.lower()), None)
    if wf_arg is None:
        wf_arg = next(iter(props), "workflow")

    for i, f in enumerate(files):
        send({"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call",
              "params": {"name": vt["name"], "arguments": {wf_arg: f}}})
        res = read_response()
        print("\n=== VALIDATE", os.path.basename(f), "===")
        if "error" in res:
            print("TOOL ERROR:", json.dumps(res["error"])[:2000])
            continue
        content = res["result"].get("content", [])
        for c in content:
            if c.get("type") == "text":
                print(c["text"][:4000])

    p.terminate()
    try:
        err = p.stderr.read().decode("utf-8", "replace")
        if err.strip():
            print("\n[stderr tail]\n", err[-2000:])
    except Exception:
        pass


if __name__ == "__main__":
    main()
