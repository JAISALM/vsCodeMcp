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

## "Strata" (from the Reddit thread)
**Not something we need.** Strata (`Niko1221/Strata`, MIT) is an inference engine
for **huge MoE models** (e.g. 125B): it splits one checkpoint across GPU VRAM +
RAM + NVMe and streams dormant experts from the slow tiers — that's how it runs a
125B model on a 12 GB card. It came up in the thread as one of the many engines
people swap between (alongside llama.cpp, vllm, ComfyUI). Our brain (Qwen 27B
NVFP4) **fits fully in the 32 GB GPU** and runs on plain llama.cpp — no expert
streaming needed, so no Strata. llama-swap is the *broker*; Strata would just be
another engine it could broker if we ever wanted to run a 100B+ MoE model locally.
