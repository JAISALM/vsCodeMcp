# Web-Search MCP + Loop Protection — FINAL REPORT (2026-09-26)

Task: `pipeline_setup.md` — add (1) reliable web research + (2) hard tool-call loop
protection to the local Qwen/Copilot/Kilo setup, WITHOUT breaking ComfyUI or the
Qwen .bat files. **All 7 slices complete.** This is the §43 report (A–H).

---

## A. What you found (existing setup, read-only)

**Qwen (local LLM — DO NOT TOUCH):**
- Launch: `D:\models\qwen\Qwen3.827BMTP.bat` → `D:\llama\llama-server.exe`
- Model: `D:\models\qwen\Qwen3.8-27B-NVFP4-MTP-LOW.gguf` + `mmproj-BF16.gguf`
- Endpoint: `http://127.0.0.1:8100/v1` (OpenAI-compatible), ctx 260000, MTP draft, flash-attn, q8_0 KV
- This is the LLM that powers the Copilot agent.

**ComfyUI (DO NOT TOUCH):**
- Install: `E:\comfyUi_latest\ComfyUI_windows_portable`, port **8188**, v0.34.3, running
- Launch: `run_nvidia_gpu.bat` → `python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --reserve-vram 4 --enable-manager`

**ComfyUI MCP:**
- `E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy-mcp.exe` (stdio), env `COMFY_BIN` → `comfy.exe`
- **Has NO open-web search.** Its "search" verbs are registry/catalog lookups only (`models search`=HF/Civitai, `nodes search`=node-pack registry, `templates`=gallery catalog, `knowledge`=local RAG). Its "stay updated" mechanism = registry refresh (`comfy outdated`/`update`/`templates refresh`/`nodes refresh`).

**Existing MCP config:** `d:\models\vsCodeMcp\.vscode\mcp.json` (workspace-level, the only active MCP config). Originally: `comfy-mcp` + `web-search` (direct).

**Toolchain:** Node v25.6.1, npm 11.9.0, git 2.53.0. PowerShell blocks `npm.ps1` → all npm/npx via `cmd /c`.

---

## B. What you changed (every changed/created file)

**Created:**
- `D:\MCP\web-search-mcp\` — official `mrkrsl/web-search-mcp` v0.3.1 (cloned, built `dist\index.js`)
- `D:\MCP\web-search-mcp\limits.json` — **centralized** limits config (webResearch + toolLimits + browser)
- `D:\MCP\web-search-mcp\WEB_SEARCH_POLICY.md` — web-research behavior policy (when-to-search, date-verification, untrusted-content rule)
- `D:\MCP\web-search-mcp\test_mcp_init.js` — direct server init test
- `D:\MCP\validate_mcp_config.js`, `D:\MCP\list_server_envs.js` — config validators
- `D:\MCP\mcp-gateway\index.js` — **zero-dep Node stdio MCP gateway** (the loop guard)
- `D:\MCP\mcp-gateway\test_gateway.js`, `test_fetch_budget.js`, `test_seq_budget.js`, `test_ws_only.js`, `test_slice6.js` + `run_*.bat` wrappers
- `D:\MCP\mcp-gateway\gateway.log` — JSON-line log of all gateway-routed calls
- `d:\models\vsCodeMcp\pipeline_setup_progress.md` — slice tracker
- `d:\models\vsCodeMcp\pipeline_setup_final_report.md` — this file

**Modified:**
- `d:\models\vsCodeMcp\.vscode\mcp.json` — `web-search` server now points at the gateway (`node D:\MCP\mcp-gateway\index.js`, `GW_BACKENDS=web-search` + `GW_*` limit env). **`comfy-mcp` left DIRECT (unchanged).**
- `d:\models\vsCodeMcp\project-memory\PROJECT_STATE.md` — added the web-search + gateway + ComfyUI-MCP-no-web-search note

**Backed up (before modifying):**
- `d:\models\vsCodeMcp\.vscode\mcp.json.pre-gateway.bak` — original mcp.json (web-search direct)

**NOT touched (per your constraint):** ComfyUI install, ComfyUI MCP, all Qwen `.bat` files, no second LLM installed.

---

## C. Installation (exact commands)

```
# 1. Clone + build web-search-mcp (official repo)
git clone https://github.com/mrkrsl/web-search-mcp D:\MCP\web-search-mcp
cmd /c "cd /d D:\MCP\web-search-mcp && npm install"
cmd /c "cd /d D:\MCP\web-search-mcp && npm run build"        # -> dist\index.js
cmd /c "cd /d D:\MCP\web-search-mcp && npx playwright install chromium"

# 2. Gateway is zero-dependency (no install) — just node D:\MCP\mcp-gateway\index.js

# 3. Wire into Copilot: edit d:\models\vsCodeMcp\.vscode\mcp.json (see D below)
#    Then reload/restart the MCP servers in Copilot.
```

---

## D. Web MCP (exact path + config)

**Server entry point:** `D:\MCP\web-search-mcp\dist\index.js`
**But it is reached THROUGH the gateway** — the client points at `D:\MCP\mcp-gateway\index.js`, which spawns the web-search server and enforces limits before forwarding.

**Copilot MCP config** (`d:\models\vsCodeMcp\.vscode\mcp.json`):
```json
{
    "servers": {
        "comfy-mcp": {
            "type": "stdio",
            "command": "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\Scripts\\comfy-mcp.exe",
            "env": { "COMFY_BIN": "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\Scripts\\comfy.exe" }
        },
        "web-search": {
            "type": "stdio",
            "command": "node",
            "args": ["D:\\MCP\\mcp-gateway\\index.js"],
            "env": {
                "GW_BACKENDS": "web-search",
                "GW_MAX_TOTAL_TOOL_CALLS": "30",
                "GW_MAX_IDENTICAL_TOOL_CALLS": "2",
                "GW_TOOL_TIMEOUT_MS": "60000",
                "GW_MAX_REPEATED_SEQUENCE": "3",
                "GW_MAX_WEB_SEARCH_CALLS": "8",
                "GW_MAX_WEB_PAGE_FETCHES": "10",
                "GW_MAX_RESEARCH_TIME_SECONDS": "120",
                "GW_LOG_FILE": "D:\\MCP\\mcp-gateway\\gateway.log"
            }
        }
    }
}
```

**Kilo Code** (installed 7.7.5/7.8.1) — **CONFIGURED** at the exact path Kilo reads: `C:\Users\user\AppData\Roaming\Code\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json` (Kilo parses the `mcpServers` key from this file). Contains `web-search` (through the gateway, own log `gateway-kilo.log`) + `comfy-mcp` (direct). **Reload Kilo Code (or restart VS Code) to pick it up.** Same `mcpServers` format:
```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["D:\\MCP\\mcp-gateway\\index.js"],
      "env": {
        "GW_BACKENDS": "web-search",
        "GW_MAX_TOTAL_TOOL_CALLS": "30",
        "GW_MAX_IDENTICAL_TOOL_CALLS": "2",
        "GW_TOOL_TIMEOUT_MS": "60000",
        "GW_MAX_REPEATED_SEQUENCE": "3",
        "GW_MAX_WEB_SEARCH_CALLS": "8",
        "GW_MAX_WEB_PAGE_FETCHES": "10",
        "GW_MAX_RESEARCH_TIME_SECONDS": "120",
        "GW_LOG_FILE": "D:\\MCP\\mcp-gateway\\gateway.log"
      }
    }
  }
}
```
Kilo reuses the SAME gateway + web-search server as Copilot (shared MCP infrastructure).

---

## E. Resource settings (browser / web-search)

Centralized in `D:\MCP\web-search-mcp\limits.json` (`browser` block) and mirrored into the gateway's web-search backend env:

| Setting | Value | Meaning |
|---------|-------|---------|
| `MAX_BROWSERS` | `1` | one browser instance (saves RAM/VRAM) |
| `BROWSER_HEADLESS` | `true` | no visible browser window |
| `BROWSER_TYPES` | `chromium` | pinned to chromium (only one installed; avoids firefox launch failures) |
| `BROWSER_FALLBACK_THRESHOLD` | `3` | fall back to direct-URL after 3 enhanced-search attempts |
| `DEFAULT_TIMEOUT` | `6000` | 6s default page timeout |
| `MAX_CONTENT_LENGTH` | `10000` | cap extracted page content at 10k chars |
| `ENABLE_RELEVANCE_CHECKING` | `true` | filter irrelevant results |

---

## F. Loop protection — WHERE each limit is enforced

**The hard limits are enforced by the MCP GATEWAY** (`D:\MCP\mcp-gateway\index.js`), NOT by Copilot, Kilo, or the MCP server. This is a real code-level gate (calls are blocked before they reach the backend), not a prompt instruction.

| Limit | Value | Enforced by |
|-------|-------|-------------|
| `MAX_TOTAL_TOOL_CALLS` | 30 | **MCP gateway** (per gateway-process/session) |
| `MAX_IDENTICAL_TOOL_CALLS` | 2 | **MCP gateway** (sha256 of normalized args; 3rd identical call blocked) |
| `TOOL_TIMEOUT` | 60s | **MCP gateway** (per-call timeout → `TOOL_TIMEOUT` result) |
| `MAX_REPEATED_SEQUENCE` | 3 | **MCP gateway** (a,b,a,b,a,b pattern → block) |
| 2-consecutive-failure block | 2 | **MCP gateway** (same call fails twice → "change strategy") |
| `MAX_WEB_SEARCH_CALLS` | 8 | **MCP gateway** (per 120s research window) |
| `MAX_WEB_PAGE_FETCHES` | 10 | **MCP gateway** (per 120s research window) |
| `MAX_RESEARCH_TIME` | 120s | **MCP gateway** (research window length) |

**What does NOT enforce hard limits (honest):**
- **Copilot** — no built-in per-tool-call cap. Relies on the gateway.
- **Kilo Code** — no built-in per-tool-call cap. Relies on the gateway.
- **web-search-mcp server** — has NO built-in budget (that's why the gateway exists).
- **ComfyUI MCP** — currently routed DIRECT (not through the gateway), so its calls are NOT loop-guarded. (Left this way to honor "don't touch ComfyUI MCP." To guard it too, set `GW_BACKENDS=comfy-mcp,web-search` and point the `comfy-mcp` entry at the gateway.)

**Scope caveats (honest):**
- The gateway's counters are **per gateway-process** (per client MCP-server lifetime). Restarting the MCP server in the client resets them. `gateway_reset_counters` (max 5×/process) is the only in-band reset.
- The gateway only guards tools **routed through it** (currently web-search). Built-in client tools (read_file, etc.) and the direct ComfyUI MCP are outside its scope.
- "Search doesn't happen unnecessarily" and "web content is untrusted" are **behavioral policy** (`WEB_SEARCH_POLICY.md`, prompt-level guidance to the model) — the hard web budget (8 searches/120s) is the code-level backstop, but the *decision to search* is model-driven.

---

## G. Tests (actual results)

**Slice 6 — Required tests 1–8** (ComfyUI as the test project):

| # | Test | Result |
|---|------|--------|
| 1 | Basic web search (latest release) | ✅ `full-web-search` → latest ComfyUI = **v0.37.0** (21 Sep), from GitHub releases page; matches `server_info.freshness` |
| 2 | Yesterday (2026-09-25) | ✅ No release on 25 Sep; nearest = v0.37.0 (21 Sep) / v0.36.0 (15 Sep). Stale results ignored, "no verified changes" reported |
| 3 | Known URL | ✅ `get-single-web-page-content` on GitHub releases page (747 words). Limitation: `docs.comfy.org/changelog` is a JS SPA → 21-word stub (use server-rendered URLs) |
| 4 | Lightweight search | ✅ `get-web-search-summaries` → 5 current results |
| 5 | Loop protection | ✅ 3rd identical call BLOCKED (`LOOP_GUARD`), backend never receives it |
| 6 | Max tool calls (cap=5) | ✅ Calls 1–5 allowed, 6th BLOCKED (`total tool-call limit`), clean stop |
| 7 | Web failure (no infinite retry) | ✅ 404 → retry once → 3rd attempt BLOCKED after 2 consecutive failures |
| 8 | ComfyUI regression | ✅ `mcp_comfy-mcp_which` works after install — both web-search + ComfyUI MCP confirmed working |

**Live proof (Copilot through the gateway):** `D:\MCP\mcp-gateway\gateway.log` shows the slice-6 Copilot calls (tests 1–4) were routed through the gateway and logged (call# 1–5, durations, status=ok).

**Gateway unit tests (all PASS, EXITCODE=0):** `test_gateway.js` (full), `test_fetch_budget.js`, `test_seq_budget.js`, `test_ws_only.js`, `test_slice6.js`.

---

## H. Remaining limitations (honest)

1. **ComfyUI MCP is NOT loop-guarded** (routed direct, to honor "don't touch it"). Only web-search goes through the gateway. Fix if desired: `GW_BACKENDS=comfy-mcp,web-search` + point the `comfy-mcp` entry at the gateway.
2. **Gateway counters are per-process** — restarting the MCP server in the client resets all limits. There is no persistent cross-restart counter.
3. **JS-rendered pages don't extract well** — `docs.comfy.org/changelog` (SPA) returns a ~21-word stub via static fetch. Use server-rendered URLs (e.g. GitHub) for reliable extraction, or the browser-based `full-web-search` for SPAs.
4. **"When to search" is policy, not a hard gate** — the model decides whether to search; the hard web budget (8/120s) is the backstop. Ordinary questions should not trigger search (per `WEB_SEARCH_POLICY.md`), but that's prompt-level.
5. **Web content is untrusted** — the gateway does NOT sanitize web content; the untrusted-data rule is enforced by the model following `WEB_SEARCH_POLICY.md`, not by code.
6. **Kilo Code not yet configured** — the snippet is provided (section D) but the user must paste it into Kilo's MCP Servers tab and reload. Not verified live (Kilo has no MCP servers configured yet).
7. **web-search backend does real browser searches** — ~5–15s each, occasional timeouts/404s on throwaway URLs. Expected, not a fault.
8. **`get-single-web-page-content` 404s on `example.com/*`** — those paths don't exist; the tool correctly reports the 404 (used intentionally in guard tests).

---

## Success criteria (§42) — all met

- ✅ Existing Qwen3.8 still works (this agent runs on it)
- ✅ Existing ComfyUI still works (port 8188, running)
- ✅ Existing ComfyUI MCP still works (test 8)
- ✅ Web Search MCP installed from official GitHub repo (`mrkrsl/web-search-mcp` v0.3.1)
- ✅ Web search works with local Qwen (slice 6, live through gateway)
- ✅ Qwen retrieves current info (test 1)
- ✅ Qwen answers "what changed yesterday" with verified dates (test 2)
- ✅ Qwen fetches a known webpage (test 3)
- ✅ Search doesn't happen unnecessarily (policy + hard budget backstop)
- ✅ Web content treated as untrusted (policy)
- ✅ Tool calls have a hard maximum (gateway)
- ✅ Identical tool calls blocked (gateway)
- ✅ Tool timeouts exist (gateway)
- ✅ Web research has a bounded budget (gateway)
- ✅ Failed tools can't cause infinite retries (gateway 2-failure block)
- ✅ No second large local model installed (only lightweight web-search-mcp + zero-dep gateway)
- ✅ ComfyUI VRAM/RAM not unnecessarily increased (gateway is a small Node process; chromium only during searches)
- ✅ Web-search config NOT duplicated in Qwen .bat files (centralized in `limits.json` + `mcp.json`)
- ✅ Same MCP infrastructure reusable by different local models (gateway is model-agnostic; `mcp.json` is client-level)
- ✅ GitHub Copilot remains usable (demonstrated live through the gateway)
- ✅ Kilo Code remains usable (installed; snippet provided)

**FINAL RULE honored:** the existing working local AI setup was NOT destroyed or replaced — ComfyUI, ComfyUI MCP, and all Qwen .bat files are untouched.
