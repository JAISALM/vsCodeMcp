# -*- coding: utf-8 -*-
r"""
Submit a UI-format workflow to the RUNNING ComfyUI (http://127.0.0.1:8188 =
E:\comfyUi_latest instance) and wait for completion.

UI->API conversion with the verified native widget shapes:
  - KSampler widgets_values = [seed, control_after_generate(hidden), steps, cfg,
    sampler_name, scheduler, denoise] -> skip index 1
  - LoadImage widgets_values = [filename, "image"(hidden upload)] -> image=wv[0]
  - all other nodes: positional map onto /object_info widget order
  - bypassed nodes (mode != 0) and Note nodes are excluded

Usage:
  & "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\utilities\submit_krea2_workflow.py" <workflow.json> [timeout_seconds]
"""
import json
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8188"


def get_object_info(node_type: str) -> dict:
    with urllib.request.urlopen(f"{BASE}/object_info/{node_type}", timeout=30) as r:
        return json.load(r)[node_type]["input"]


# Native widgets_values order per node type (verified from native UI-saved files).
# /object_info order is WRONG for the UI (it omits hidden widgets), so we map
# widgets_values positionally onto THIS explicit list instead. A None entry is a
# hidden widget (present in widgets_values but NOT sent to the API).
NATIVE_WIDGETS = {
    "KSampler": ["seed", None, "steps", "cfg", "sampler_name", "scheduler", "denoise"],
    "LoadImage": ["image", None],
    "EmptySD3LatentImage": ["width", "height", "batch_size"],
    "CLIPLoader": ["clip_name", "type", "device"],
    "UNETLoader": ["unet_name", "weight_dtype"],
    "VAELoader": ["vae_name"],
    "LoraLoaderModelOnly": ["lora_name", "strength_model"],
    "Krea2EditGroundedEncode": ["prompt", "grounding_px", "system_prompt"],
    "Krea2EditModelPatch": ["ref_boost", "ref_boost_a", "fit_mode"],
    "SaveImage": ["filename_prefix"],
    "ResolutionSelector": ["aspect_ratio", "megapixels", "multiple"],
}


def build_prompt(wf: dict) -> dict:
    links = {l[0]: l for l in wf.get("links", [])}
    nodes = wf["nodes"]
    included = {str(n["id"]) for n in nodes
                if n.get("mode", 0) == 0 and n["type"] != "Note"}

    prompt = {}
    for n in nodes:
        if str(n["id"]) not in included:
            continue
        ntype = n["type"]
        wv = n.get("widgets_values", [])
        linked_names = {inp["name"] for inp in n.get("inputs", [])
                        if inp.get("link") is not None}

        inputs = {}
        native = NATIVE_WIDGETS.get(ntype)
        if native is not None:
            # Map widgets_values positionally onto the verified native widget
            # order. None = hidden slot (in widgets_values, not an API input).
            # A name in linked_names is wired by a link (handled below), so it
            # is NOT consumed from widgets_values here.
            for i, name in enumerate(native):
                if name is None:
                    continue
                if name in linked_names:
                    continue
                if i < len(wv):
                    inputs[name] = wv[i]
            if len(wv) != len(native):
                print(f"  [warn] node {n['id']} {ntype}: widgets_values has "
                      f"{len(wv)} values, native shape has {len(native)} slots "
                      f"{native}")
        else:
            # Fallback for unknown node types: /object_info positional mapping.
            info = get_object_info(ntype)
            required = info.get("required", {})
            widget_names = [k for k in required if k not in linked_names]
            for i, name in enumerate(widget_names):
                if i < len(wv):
                    inputs[name] = wv[i]
            print(f"  [warn] node {n['id']} {ntype}: no native widget map, "
                  f"using /object_info order {widget_names}")

        for inp in n.get("inputs", []):
            lid = inp.get("link")
            if lid is None:
                continue
            l = links.get(lid)
            if l is None or str(l[1]) not in included:
                continue
            inputs[inp["name"]] = [str(l[1]), l[2]]

        prompt[str(n["id"])] = {"class_type": ntype, "inputs": inputs}
    return prompt


def submit(wf_path: str) -> str:
    wf = json.load(open(wf_path, encoding="utf-8"))
    prompt = build_prompt(wf)
    payload = json.dumps({"prompt": prompt, "client_id": "vscode-submit"}).encode()
    req = urllib.request.Request(f"{BASE}/prompt", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.load(r)
    status = resp.get("status", {})
    if status.get("status_code") == 400:
        print("VALIDATION FAILED:")
        print(json.dumps(status.get("messages"), indent=2))
        sys.exit(1)
    pid = resp["prompt_id"]
    print(f"[submitted] {wf_path} -> prompt_id {pid}")
    return pid


def wait(pid: str, timeout: float) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{BASE}/history/{pid}", timeout=30) as r:
                hist = json.load(r)
            if pid in hist:
                entry = hist[pid]
                st = entry.get("status", {})
                if st.get("status") == "success" or st.get("completed"):
                    outputs = entry.get("outputs", {})
                    files = []
                    for nid, out in outputs.items():
                        for img in out.get("images", []):
                            files.append(f"{img.get('subfolder','')}/{img.get('filename')}")
                    print(f"[done] {pid} outputs: {files}")
                    return entry
                if st.get("status") == "error":
                    print(f"[ERROR] {pid}: {st}")
                    sys.exit(1)
        except Exception:
            pass
        time.sleep(5)
    print(f"[timeout] {pid} after {timeout}s")
    sys.exit(2)


if __name__ == "__main__":
    wf_path = sys.argv[1]
    timeout = float(sys.argv[2]) if len(sys.argv) > 2 else 600
    pid = submit(wf_path)
    wait(pid, timeout)
