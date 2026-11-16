# llama-swap — how it works + what you do (2026-10-31, D207)

## What it is (30 seconds)
llama-swap is a small proxy that sits in front of your AI servers and **starts/stops
them on demand** so they stop fighting over the 5090.

- **Today:** DSH brain → `llama-server` @8100 (always-on, ~17 GB VRAM all the time)
- **After cutover:** DSH brain → **llama-swap** @8100 (tiny, 0 VRAM) → it starts
  `llama-server` on a spare port only when a brain message arrives, and can stop
  it to make room. Your DSH config changes **nothing** (same port 8100).

## Current state (right now)
- Test daemon **running on :8200** = an OBSERVER only. It is not wired to anything,
  so its UI correctly shows **nothing running** — that is the healthy state.
- ⚠️ **Do NOT click "Load" on the model card in the :8200 UI.** That would start a
  SECOND Qwen (17 GB) next to your live brain (17 GB) = 34 GB > 32 GB → OOM.
  The :8200 UI is there only to show the tool is alive.
- The real brain path is still the direct `llama-server` on :8100.

## The ONE action (when you're between tasks — not mid-conversation)
1. Double-click `D:\models\qwen\cutover_llama_swap.bat`
2. It kills the direct llama-server, starts llama-swap **on :8100** (a minimized
   window appears = the daemon — **keep that window open**, closing it stops the brain),
   health-checks, and reports OK/FAIL.
3. Send me a message. Your first reply after the cutover is slow (~1–2 min cold
   load of Qwen through llama-swap), then it's as fast as today.
4. Watch it in the **production UI: http://127.0.0.1:8100/ui/** (model card flips
   to loaded, token metrics + live logs appear).

## Day-to-day
- **Stop llama-swap:** close its minimized window, or `taskkill /F /IM llama-swap.exe`
- **Back to the old setup:** `D:\models\qwen\rollback_qwen_direct.bat`
  (kills llama-swap, relaunches the direct brain — the pre-llama-swap state)
- **Old :8200 test daemon** (redundant after cutover): `taskkill /F /PID 5464`
  (if that PID is stale after a reboot: `Get-Process llama-swap` and kill the one
  whose command line says 8200)
- **Handoff before video runs (stage-1 win):** ask me (or run)
  `curl -X POST http://127.0.0.1:8100/api/models/unload` → Qwen unloads gracefully →
  you queue your ComfyUI run → next brain message auto-loads Qwen again.
  This replaces the manual "kill qwen, wait 10 min, restart both" dance.
- **Web UI extras:** manual load/unload buttons, `/logs` live streams,
  `POST /api/models/pause` (frees everything while the daemon stays up).

## What is NOT automated yet (stage 2)
- **ComfyUI stays your manual GUI instance on :8188.** A llama-swap `comfyui` entry
  forces ComfyUI onto a dynamic port (breaks your 8188 UI + the ComfyUI MCP), so it
  is parked as a commented block in `D:\tools\llama-swap\config.yaml`.
- Later options if it's behaving well: Berth on top (orphan-process detection,
  mid-render protection, RAM parking) — the two are designed to coexist.

## Files
- `D:\tools\llama-swap\llama-swap.exe` · `config.yaml` · README/CHANGELOG
- `D:\models\qwen\cutover_llama_swap.bat` · `rollback_qwen_direct.bat`
- `D:\models\qwen\start_qwen_8100.bat` = the permanent manual fallback (untouched)

## Coexisting with ComfyUI + why the MCP still works (the server vs models distinction)
The ComfyUI **server** is cheap (~2-3 GB idle); **loaded models** are expensive (~20 GB).
After `/free`, server + Qwen coexist (≈20 GB < 32 GB):

| Time | Qwen (the agent) | ComfyUI | What happens |
|---|---|---|---|
| **Chat time** (default) | loaded | server up, **models freed** | agent builds/edits/validates workflows via MCP — all coexists |
| **Video time** | unloaded | models loaded, user presses Enter | user owns the GUI; agent is offline (agent IS Qwen) |
| **Transition** | — | `free_comfyui_vram.bat` OR close GUI | one click, then talk to Qwen → auto-loads clean |

- **The MCP needs the SERVER (object_info/validate/inspect), not loaded models** — so
  "both can't be up" only applies to *loaded models*, which is exactly what the
  turn-taking serializes. During a video run the user is at the GUI and the agent
  is unloaded anyway (it can't watch its own run — the run that evicted it).
- **`D:\models\qwen\free_comfyui_vram.bat`** = `POST http://127.0.0.1:8188/free`
  (ComfyUI's own unload endpoint; server stays up, models evicted). Run it after a
  heavy run BEFORE switching back to chat. If it doesn't free enough (orphaned node
  process squatting), close the GUI instead — or add Berth (stage 2) which names
  the squatter by PID.

## 2026-11-16 FIX — why `free_comfyui_vram.bat` was a NO-OP + the one-click shift pair

**Root cause (proven):** the bat ran `curl.exe -s -X POST http://127.0.0.1:8188/free`
with **NO JSON body**. The handler (`server.py` ~1294) does `json_data = await
request.json()` → a body-less request makes the server return **`500 Internal
Server Error`** (verified live), so neither `unload_models` nor `free_memory` is
ever set and nothing is unloaded — while `curl -s` swallowed the 500 and the bat
printed a fake `Done. Models evicted from VRAM`. That's why a full manual
ComfyUI stop was needed after the H3 run. **No custom node is needed for this —
`POST /free` is a CORE ComfyUI endpoint** (no installed pack provides a
free-memory node; the "FreeVideo" hits in the H3 packs are unrelated).

**Fixed 11-16 (files in `D:\models\qwen\`, mirrored in `docs\`):**
- **`free_comfyui_vram.bat` → `free_comfyui_vram.ps1`** — sends the proper body
  `{"unload_models":true,"free_memory":true}` (verified HTTP 200), then POLLS
  `/system_stats` before/after and prints the ACTUAL VRAM freed (the flag is
  consumed by the prompt-queue worker on its next iteration, not instantly).
  No fake success: a fresh/idle server honestly reports "nothing was loaded".
- **`shift_to_qwen.bat`** — ComfyUI→brain shift: POST `/free` (server stays up)
  → verify VRAM came back → start `start_qwen_8100.bat` if :8100 is dark.
- **`shift_to_comfy.bat`** — brain→ComfyUI shift: llama-swap daemon →
  `POST /api/models/unload` (graceful); direct `llama-server` → `taskkill /F /IM
  llama-server.exe`; then starts `run_nvidia_gpu.bat` if :8188 is dark.
  (Run between tasks — the brain goes down while ComfyUI owns the GPU.)

**State check 11-16:** :8100 is still the DIRECT `llama-server.exe` (PID 2084) —
the llama-swap cutover was never run. The cutover (`cutover_llama_swap.bat`,
between tasks) is still the upgrade that makes shifts graceful (daemon stays up,
brain auto-loads on the next message, `POST /api/models/unload` from the UI).
Until then, the shift bats handle the direct-server case (taskkill +
`start_qwen_8100.bat`).

**2026-11-16 addition — `auto_free_comfyui` watcher (the zero-click tier):**
`D:\models\qwen\auto_free_comfyui.ps1` (+ `.bat` launcher) polls ComfyUI's
`/queue` every 3 s; when a run FINISHES (queue busy → empty for ~9 s = 3
polls, the grace so a quick follow-up run keeps models warm) it auto-POSTs the
proper `/free` body — models evicted, **server never stopped**. It is now
auto-started (minimized window) by `run_nvidia_gpu.bat`, so it lives exactly as
long as ComfyUI. The logon scheduled-task variant could not be registered from
the agent session (`Register-ScheduledTask` → Access denied) — the launcher-bat
auto-start makes it unnecessary. Stop it: close the minimized
"auto-free-comfyui" window. **RAM note (measured 11-16):** the idle ComfyUI
server costs only ~1.9 GB RAM + ~2 GB VRAM — after `/free` the model files'
page cache is reclaimable, so the server happily coexists with the loaded
brain (Qwen ~17 GB RAM); stopping the server buys only ~2 GB and is not needed.
Desktop shortcuts added for all four bats (Free VRAM / Shift to Qwen /
Shift to ComfyUI / Auto-Free Watcher).

## "Strata" (from the Reddit thread)
**Not something we need.** Strata (`Niko1221/Strata`, MIT) is an inference engine
for **huge MoE models** (e.g. 125B): it splits one checkpoint across GPU VRAM +
RAM + NVMe and streams dormant experts from the slow tiers — that's how it runs a
125B model on a 12 GB card. It came up in the thread as one of the many engines
people swap between (alongside llama.cpp, vllm, ComfyUI). Our brain (Qwen 27B
NVFP4) **fits fully in the 32 GB GPU** and runs on plain llama.cpp — no expert
streaming needed, so no Strata. llama-swap is the *broker*; Strata would just be
another engine it could broker if we ever wanted to run a 100B+ MoE model locally.
