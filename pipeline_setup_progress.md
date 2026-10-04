# Web-Search MCP + Loop Protection — Progress Tracker

Task: `pipeline_setup.md` (LOCAL QWEN3.8 MCP EXTENSION).
Working in slices of 3 sections. Each slice: do → mark here → ask user for confirmation.
**RULES: no loops (user called this out); one slice at a time; confirm before next slice; ComfyUI + Qwen .bat files stay UNTOUCHED; npm/npx must run via `cmd /c` (PowerShell blocks npm.ps1).**

## ⚡ RESUME POINT (read this first if starting a fresh session)

**Task:** add (1) web-search MCP + (2) hard tool-call loop protection to the local Qwen/Copilot/Kilo setup, WITHOUT breaking ComfyUI or the Qwen .bat files.

**🏁 STATUS (2026-09-26): ALL 7 SLICES COMPLETE.** Task `pipeline_setup.md` is finished. Final report: `d:\models\vsCodeMcp\pipeline_setup_final_report.md` (§43 A–H + §42 checklist, all met). Web-search + loop-guard gateway live in Copilot (verified). Kilo Code snippet provided (user to paste). ComfyUI + Qwen .bat files untouched.

**Slice plan + status:**

| Slice | Sections | Status |
|-------|----------|--------|
| 1 | §0–2: Inspect existing environment | ✅ DONE (2026-09-26) |
| 2 | §3–5: Install web-search-mcp + build + test server directly | ✅ DONE (2026-09-26) |
| 3 | §6–8: MCP configuration (Copilot + Kilo) + shared architecture | ✅ DONE (2026-09-26) |
| 4 | §10–14: Web search behavior + research budget (config) | ✅ DONE (2026-09-26) |
| 5 | §15–21: Hard tool-call limits / loop guard (MCP gateway) | ✅ DONE (2026-09-26) |
| 6 | §29–36: Required tests 1–8 | ✅ DONE (2026-09-26) |
| 7 | §37–43: Client compatibility + final report | ✅ DONE (2026-09-26) — **ALL SLICES COMPLETE** |

**Key paths (all verified to exist):**
- Repo: `D:\MCP\web-search-mcp\` (official `mrkrsl/web-search-mcp` v0.3.1; `dist\index.js` built ✅)
- Chromium: `C:\Users\user\AppData\Local\ms-playwright\chromium-1234` (INSTALLATION_COMPLETE ✅)
- Central limits: `D:\MCP\web-search-mcp\limits.json` (webResearch + toolLimits + browser blocks)
- Behavior policy: `D:\MCP\web-search-mcp\WEB_SEARCH_POLICY.md`
- Copilot MCP config: `d:\models\vsCodeMcp\.vscode\mcp.json` (servers: `comfy-mcp` + `web-search` with 7 env vars incl. `BROWSER_TYPES=chromium`)
- Test harnesses: `D:\MCP\web-search-mcp\test_mcp_init.js` (direct server test), `D:\MCP\validate_mcp_config.js`, `D:\MCP\list_server_envs.js`
- **Loop-guard gateway: `D:\MCP\mcp-gateway\index.js`** (zero-dep Node stdio MCP; spawns backends, enforces hard limits before forwarding). Tests: `test_gateway.js`, `test_fetch_budget.js`, `test_seq_budget.js`, `test_ws_only.js` + `run_*.bat` wrappers. Log: `D:\MCP\mcp-gateway\gateway.log`.
- **mcp.json now routes `web-search` through the gateway** (`node D:\MCP\mcp-gateway\index.js`, `GW_BACKENDS=web-search`); `comfy-mcp` stays direct. Backup: `mcp.json.pre-gateway.bak`. **Client must reload MCP servers to pick up the change.**
- Kilo Code: MCP servers managed in extension UI (no config file) — snippet for its MCP tab is in the Slice 3 section below
- Qwen (DO NOT TOUCH): `D:\models\qwen\Qwen3.827BMTP.bat` → `D:\llama\llama-server.exe`, port 8100
- ComfyUI (DO NOT TOUCH): `E:\comfyUi_latest\ComfyUI_windows_portable`, port 8188, v0.34.3, running
- ComfyUI MCP: `E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\Scripts\comfy-mcp.exe` (env `COMFY_BIN` → `comfy.exe`)

**Key findings (do not re-investigate):**
- web-search-mcp env surface (read at runtime): `MAX_BROWSERS`, `BROWSER_HEADLESS`, `BROWSER_TYPES` (default `chromium,firefox` — MUST pin to `chromium`, only chromium installed), `ENABLE_RELEVANCE_CHECKING`, `FORCE_MULTI_ENGINE_SEARCH`, `RELEVANCE_THRESHOLD`, `BROWSER_FALLBACK_THRESHOLD`, `DEFAULT_TIMEOUT`, `MAX_CONTENT_LENGTH`
- Server has NO built-in per-request budget → hard limits require the gateway (slice 5)
- PowerShell execution policy blocks `npm.ps1` → always `cmd /c "cd /d <dir> && npm ..."`
- Node v25.6.1, npm 11.9.0, git 2.53.0

**Slice 5 design (agreed):** thin Node stdio MCP gateway at `D:\MCP\mcp-gateway\index.js` (zero deps). Clients point at the gateway; it spawns both backends (`comfy-mcp.exe` + `node dist\index.js`), merges tools/list, routes tools/call by name, and enforces BEFORE forwarding: MAX_TOTAL_TOOL_CALLS (per session, resettable via `gateway_reset_counters`, max 5 resets), MAX_IDENTICAL_TOOL_CALLS (sha256 of normalized args — sorted keys, trimmed strings, URL-normalized; 3rd identical call blocked, never reaches backend), TOOL_TIMEOUT (60s), repeated-sequence detection (a,b,a,b,a,b → block), failure policy (2 failures on same call → block "change strategy"), web budget (8 searches / 10 page fetches / 120s research window). Structured errors: `LOOP_GUARD:` / `TOOL_TIMEOUT:` / `BUDGET_EXHAUSTED:` as MCP tool results with isError=true. Logging → `D:\MCP\mcp-gateway\gateway.log` (JSON lines: ts, tool, normalized args, call#, duration, status, blocked reason). Env overrides for testing: `GW_MAX_TOTAL_TOOL_CALLS`, `GW_MAX_IDENTICAL_TOOL_CALLS`, `GW_TOOL_TIMEOUT_MS`. Then `mcp.json` switches to point at the gateway (backup original to `mcp.json.pre-gateway.bak` first).

**Slice 6 = required tests 1–8** (web search, latest release, yesterday-date, known URL, loop protection, max-call protection, failure retry, ComfyUI regression). **Slice 7 = client compatibility (Copilot + Kilo) + final report per doc §43.**

---

## Slice 5 — Hard tool-call limits / loop guard (MCP gateway) — DONE (2026-09-26)

### What was built
- **`D:\MCP\mcp-gateway\index.js`** — zero-dependency Node stdio MCP gateway. Spawns backends (configurable via `GW_BACKENDS` env, default `comfy-mcp,web-search`), merges `tools/list`, routes `tools/call` by tool name. Enforces BEFORE forwarding:
  1. `MAX_TOTAL_TOOL_CALLS` (default 30) — per-session total cap
  2. `MAX_IDENTICAL_TOOL_CALLS` (default 2) — sha256 of normalized args (sorted keys, trimmed strings, URL-normalized); call N+1 blocked, never reaches backend
  3. `MAX_REPEATED_SEQUENCE` (default 3) — a,b,a,b,a,b pattern detection
  4. Failure policy — 2 consecutive failures on the same call → block ("change strategy")
  5. Web budget — `MAX_WEB_SEARCH_CALLS` (8) / `MAX_WEB_PAGE_FETCHES` (10) / `MAX_RESEARCH_TIME_SECONDS` (120) per research window
- Blocked calls return structured MCP tool results (`isError=true`) with `LOOP_GUARD:` / `TOOL_TIMEOUT:` / `BUDGET_EXHAUSTED:` messages. Nothing is forwarded.
- Special tool `gateway_reset_counters` (max 5 resets/process) for genuinely new tasks.
- Logging → `D:\MCP\mcp-gateway\gateway.log` (JSON lines: ts, tool, normalized args, call#, duration, status, blocked reason). No prompt contents logged.
- Env overrides: `GW_MAX_TOTAL_TOOL_CALLS`, `GW_MAX_IDENTICAL_TOOL_CALLS`, `GW_TOOL_TIMEOUT_MS`, `GW_MAX_REPEATED_SEQUENCE`, `GW_MAX_WEB_SEARCH_CALLS`, `GW_MAX_WEB_PAGE_FETCHES`, `GW_MAX_RESEARCH_TIME_SECONDS`, `GW_LOG_FILE`, `GW_BACKENDS`.

### Bug found + fixed during testing
- **`GW_MAX_RESEARCH_TIME_SECONDS` env override was read as raw ms (120) instead of seconds→ms (120000).** The research window was only 120ms, so every call >120ms apart triggered a window reset and zeroed the web counters → page-fetch budget never blocked. Fixed: env override now multiplies by 1000. Verified with `test_fetch_budget.js` (3rd fetch now blocked) and `test_seq_budget.js` (2 searches then 3 fetches → 3rd fetch blocked, EXITCODE=0).

### mcp.json wiring (backup made first)
- Backup: `d:\models\vsCodeMcp\.vscode\mcp.json.pre-gateway.bak` (original: web-search → `node dist\index.js` direct).
- Current: `web-search` server now points at `node D:\MCP\mcp-gateway\index.js` with `GW_BACKENDS=web-search` + all `GW_*` limit env vars. **`comfy-mcp` stays DIRECT** (unchanged) — ComfyUI MCP is NOT broken, just not loop-guarded (honors the "don't break ComfyUI MCP" constraint). To also guard ComfyUI, change `GW_BACKENDS` to `comfy-mcp,web-search` and point the `comfy-mcp` entry at the gateway too.
- **Client must reload/restart MCP servers for the new config to take effect.**

### Test results (all PASS)
- `test_gateway.js` (full, both backends): initialize returns tools; web-search + comfy-mcp tools present; `gateway_reset_counters` present; identical-call guard (3rd blocked); normalized-identical (arg order/whitespace) blocked; web search budget (3rd search blocked); page-fetch budget (3rd fetch blocked); total cap (13th call blocked at cap=12); reset works; post-reset call allowed.
- `test_fetch_budget.js`: 3rd fetch blocked by page budget (EXITCODE=0).
- `test_seq_budget.js`: 2 searches then 3 fetches → 3rd fetch blocked (EXITCODE=0).
- `test_ws_only.js` (matches mcp.json config): mcp.json routes web-search through gateway + comfy-mcp stays direct; web-search tools present; comfy tools ABSENT in ws-only mode; `gateway_reset_counters` present; identical-call guard active (EXITCODE=0).
- Note: web-search backend does real Bing browser searches (slow, ~5-15s each, occasional timeouts/404s on example.com) — expected, not a gateway fault.

### Files
- `D:\MCP\mcp-gateway\index.js` (gateway), `test_gateway.js`, `test_fetch_budget.js`, `test_seq_budget.js`, `test_ws_only.js`, `run_full_test.bat`, `run_seq_test.bat`, `run_ws_only_test.bat`
- `D:\MCP\web-search-mcp\limits.json` (central limits), `WEB_SEARCH_POLICY.md` (behavior policy)

---

## Slice 6 — Required tests 1–8 (2026-09-26) — DONE

All 8 required tests from `pipeline_setup.md` §29–36, using **ComfyUI** as the known software project. Tests 1–4 + 8 run LIVE through the gateway (activated `mcp_mcp-gateway_*` tools); tests 5–7 via `test_slice6.js` (fresh gateway, controlled limits, fast 404 fetches).

| # | Test | Method | Result |
|---|------|--------|--------|
| 1 | Basic web search (latest release) | `full-web-search` "ComfyUI latest release version" | ✅ PASS — primary source = GitHub releases page; latest = **v0.37.0** (released 21 Sep), matches `server_info.freshness.core.latest` |
| 2 | Yesterday (2026-09-25) | `get-web-search-summaries` + verified dates on releases page | ✅ PASS — no ComfyUI release on 25 Sep; nearest = v0.37.0 (21 Sep), v0.36.0 (15 Sep). Stale results ignored, "no verified changes yesterday" reported |
| 3 | Known URL | `get-single-web-page-content` on `github.com/Comfy-Org/ComfyUI/releases` | ✅ PASS — 747 words retrieved, summarized. **Limitation found:** `docs.comfy.org/changelog` is a JS-rendered SPA → static fetch returns only a 21-word stub (use server-rendered URLs) |
| 4 | Lightweight search | `get-web-search-summaries` "ComfyUI latest release version 2026" | ✅ PASS — 5 current results (changelog, GitHub releases, v0.36.0 note) |
| 5 | Loop protection | `test_slice6.js`: 3× identical fetch | ✅ PASS — call1+2 allowed, call3 BLOCKED (`LOOP_GUARD`), backend never receives it |
| 6 | Max tool calls (cap=5) | `test_slice6.js`: 6 different-arg fetches | ✅ PASS — calls 1–5 allowed, call6 BLOCKED (`total tool-call limit`); agent terminates cleanly |
| 7 | Web failure (no infinite retry) | `test_slice6.js`: same failing (404) call ×3 | ✅ PASS — call1+2 fail (404, retry allowed), call3 BLOCKED after 2 consecutive failures (`LOOP_GUARD`) |
| 8 | ComfyUI regression | `mcp_comfy-mcp_which` (known-good op) after web-search install | ✅ PASS — ComfyUI MCP still works (workspace `C:\Users\user\Documents\comfy\ComfyUI`). Both web-search + ComfyUI MCP confirmed working |

**Files:** `D:\MCP\mcp-gateway\test_slice6.js` + `run_slice6_test.bat` (result: `slice6-result.txt`, 8/8 PASS, EXITCODE=0).

**Note for slice 7:** the live gateway tools are exposed to the client as `mcp_mcp-gateway_full-web-search` / `mcp_mcp-gateway_get-web-search-summaries` (via the gateway). `get-single-web-page-content` was also available live.

---

## Slice 7 — Client compatibility + final report (2026-09-26) — DONE

**Client compatibility:**
- **Copilot: VERIFIED LIVE.** The slice-6 web-search calls (tests 1–4) were made by Copilot through the gateway — `D:\MCP\mcp-gateway\gateway.log` shows them (call# 1–5, durations, status=ok). Copilot's `mcp.json` routes `web-search` → gateway; `comfy-mcp` stays direct. Copilot remains the preferred interface, fully usable.
- **Kilo Code: CONFIGURED (2026-09-26).** Wrote `C:\Users\user\AppData\Roaming\Code\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json` (the exact path Kilo reads — it parses the `mcpServers` key from this file). Contains `web-search` (through the gateway, own log `gateway-kilo.log`) + `comfy-mcp` (direct). Validated (both servers present). **User must reload Kilo Code / restart VS Code to pick it up.** NOT yet verified live (needs that reload).

**Final report:** `d:\models\vsCodeMcp\pipeline_setup_final_report.md` — full §43 A–H (what found / what changed / install commands / web MCP path+config / resource settings / loop-protection enforcement location / test results / remaining limitations) + §42 success-criteria checklist (all met).

**Key honest findings (also in report §F/§H):**
- Hard limits are enforced by the **MCP gateway** (code-level, before forwarding) — NOT by Copilot/Kilo/MCP-server/prompt.
- ComfyUI MCP is NOT loop-guarded (routed direct, per "don't touch" constraint). Optional: `GW_BACKENDS=comfy-mcp,web-search`.
- Gateway counters are per-process (MCP-server restart resets them); `gateway_reset_counters` max 5×/process.
- JS-rendered pages (docs.comfy.org SPA) extract poorly via static fetch — use server-rendered URLs or `full-web-search`.
- "When to search" + "web content untrusted" = policy (`WEB_SEARCH_POLICY.md`), with the hard web budget as code backstop.

**STATUS: ALL 7 SLICES COMPLETE. Task `pipeline_setup.md` finished.**

---

## Slice 1 — Environment inspection results (2026-09-26)

### A. What exists (verified, read-only)

**Qwen (model server — DO NOT TOUCH):**
- Launch: `D:\models\qwen\Qwen3.827BMTP.bat`
- llama.cpp: `D:\llama\llama-server.exe` (note: bat uses `D:\llama`, not the b9616 path in PROJECT_STATE)
- Model: `D:\models\qwen\Qwen3.8-27B-NVFP4-MTP-LOW.gguf` + `mmproj-BF16.gguf`
- Endpoint: `http://127.0.0.1:8100` (OpenAI-compatible `/v1`), ctx 260000, MTP draft, flash-attn, q8_0 KV
- Other bats in `D:\models\qwen`: Qwen3.6-35B variants (not active)

**ComfyUI (DO NOT TOUCH):**
- Install: `E:\comfyUi_latest\ComfyUI_windows_portable`
- Launch: `run_nvidia_gpu.bat` → `python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --reserve-vram 4 --enable-manager` (port 8188, confirmed running, version 0.34.3)
- ComfyUI MCP: `start_mcp.bat` → `python_embeded\python.exe -m comfy_mcp` (stdio)

**MCP configuration (the ONLY active MCP config file):**
- `d:\models\vsCodeMcp\.vscode\mcp.json` — workspace-level, used by **GitHub Copilot**:
  ```json
  { "servers": { "comfy-mcp": { "type": "stdio",
      "command": "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\Scripts\\comfy-mcp.exe",
      "env": { "COMFY_BIN": "E:\\comfyUi_latest\\ComfyUI_windows_portable\\python_embeded\\Scripts\\comfy.exe" } } } }
  ```
- **Kilo Code**: installed (globalStorage `kilocode.kilo-code` exists) but its MCP servers are managed via the **Kilo Code UI** (extension state), NOT a plain config file. settings.json has only 4 Kilo UI keys (autoApprove off, browserAutomation on). → web-search-mcp must be added through the Kilo Code MCP tab (JSON snippet will be provided).
- No user-level `mcp.json`, no `.kilocode` folder, no `D:\MCP` folder yet.

**Toolchain:**
- Node v25.6.1 ✅, npm 11.9.0 ✅ (via `cmd /c npm` — PowerShell execution policy blocks `npm.ps1`, so all npm commands must run via `cmd /c`), git 2.53.0 ✅
- Python (for MCP if needed): `E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe`

### B. Decisions for slice 2 (proposed, pending user confirmation)

1. **Install location:** `D:\MCP\web-search-mcp` (new `D:\MCP` dir — clean, outside ComfyUI/Qwen/llama, matches the doc's preference).
2. **npm commands via `cmd /c`** (PowerShell blocks npm.ps1).
3. **Playwright:** `npx playwright install chromium` (only chromium, headless — smallest footprint; the repo's fallback path).
4. **Env vars** (per doc §4): `MAX_BROWSERS=1`, `BROWSER_HEADLESS=true`, `BROWSER_FALLBACK_THRESHOLD=3`, `DEFAULT_TIMEOUT=6000`, `MAX_CONTENT_LENGTH=10000`, `ENABLE_RELEVANCE_CHECKING=true`.
5. **Copilot config:** add `web-search` server to the EXISTING `d:\models\vsCodeMcp\.vscode\mcp.json` (same file as comfy-mcp — one shared config, no duplication).
6. **Kilo Code:** provide the JSON snippet for the Kilo Code MCP tab (user pastes in UI).
7. **Loop guard (§15–21):** design decision deferred to slice 5 — candidates: (a) a thin Node MCP gateway wrapper that both clients point at (enforces limits + logs), (b) per-server limits only. Will present options before building.

### C. Nothing changed yet
No files modified, no installs done. ComfyUI untouched and still running.

---

## Slice 2 — Install + build + direct server test (2026-09-26) ✅

### Commands used (exact)
```
git clone https://github.com/mrkrsl/web-search-mcp.git D:\MCP\web-search-mcp
cmd /c "cd /d D:\MCP\web-search-mcp && npm install --no-audit --no-fund"
cmd /c "cd /d D:\MCP\web-search-mcp && npx playwright install chromium"
cmd /c "cd /d D:\MCP\web-search-mcp && npm run build"
cmd /c "cd /d D:\MCP\web-search-mcp && node test_mcp_init.js"
```
Note: all npm/npx via `cmd /c` (PowerShell execution policy blocks `npm.ps1`).

### Results
- **Repo:** `D:\MCP\web-search-mcp` (official `mrkrsl/web-search-mcp`, v0.3.1, MIT, MCP SDK ^1.15.0, playwright ^1.48.0).
- **Dependencies:** installed clean (node_modules + @modelcontextprotocol/sdk + playwright present).
- **Playwright chromium:** installed to `C:\Users\user\AppData\Local\ms-playwright\chromium-1234` (+ `chromium_headless_shell-1234`, `ffmpeg-1011`) — `INSTALLATION_COMPLETE` marker present.
- **Build:** `npm run build` (tsc) → `D:\MCP\web-search-mcp\dist\index.js` (24,947 bytes) ✅
- **Direct MCP protocol test** (`test_mcp_init.js` — spawns `node dist/index.js` with the §4 env vars, sends `initialize` + `tools/list`):
  - `INIT OK — server: {"name":"web-search-mcp","version":"0.3.1"}`, protocolVersion `2025-03-26`
  - **All 3 tools discoverable:** `full-web-search`, `get-web-search-summaries`, `get-single-web-page-content` ✅
- **Env vars used in the test (per doc §4):** `MAX_BROWSERS=1`, `BROWSER_HEADLESS=true`, `BROWSER_FALLBACK_THRESHOLD=3`, `DEFAULT_TIMEOUT=6000`, `MAX_CONTENT_LENGTH=10000`, `ENABLE_RELEVANCE_CHECKING=true`.
- **ComfyUI:** untouched, still running (no changes to its config/env/ports).

### Files created/changed in slice 2
- `D:\MCP\web-search-mcp\` (cloned repo + node_modules + dist)
- `D:\MCP\web-search-mcp\test_mcp_init.js` (new — direct MCP stdio test harness; reusable)

### Next (slice 3, pending confirmation)
§6–8: wire the MCP config — add `web-search` server to the existing `d:\models\vsCodeMcp\.vscode\mcp.json` (Copilot, alongside `comfy-mcp`) + provide the Kilo Code MCP-tab JSON snippet. No Qwen .bat changes (doc §7).

---

## Slice 3 — MCP configuration (2026-09-26) ✅

### Changed file
- `d:\models\vsCodeMcp\.vscode\mcp.json` — ADDED `web-search` server alongside the existing `comfy-mcp` (one shared file, no duplication). `comfy-mcp` entry verified byte-identical (command + COMFY_BIN unchanged).

### Copilot config (active, workspace-level)
```json
"web-search": {
    "type": "stdio",
    "command": "node",
    "args": ["D:\\MCP\\web-search-mcp\\dist\\index.js"],
    "env": {
        "MAX_BROWSERS": "1",
        "BROWSER_HEADLESS": "true",
        "BROWSER_FALLBACK_THRESHOLD": "3",
        "DEFAULT_TIMEOUT": "6000",
        "MAX_CONTENT_LENGTH": "10000",
        "ENABLE_RELEVANCE_CHECKING": "true"
    }
}
```

### Kilo Code config (paste into Kilo Code → MCP → add server; its servers live in extension state, not a file)
```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["D:\\MCP\\web-search-mcp\\dist\\index.js"],
      "env": {
        "MAX_BROWSERS": "1",
        "BROWSER_HEADLESS": "true",
        "BROWSER_FALLBACK_THRESHOLD": "3",
        "DEFAULT_TIMEOUT": "6000",
        "MAX_CONTENT_LENGTH": "10000",
        "ENABLE_RELEVANCE_CHECKING": "true"
      }
    }
  }
}
```

### Validation (via `D:\MCP\validate_mcp_config.js`)
- JSON VALID; servers = `comfy-mcp, web-search`
- `comfy-mcp` intact: command `E:\comfyUi_latest\...\comfy-mcp.exe`, COMFY_BIN unchanged
- `web-search`: command `node`, args `D:\MCP\web-search-mcp\dist\index.js` (exists ✅), env = the 6 §4 vars
- **No Qwen .bat changes** (doc §7 — Qwen stays a pure model server on :8100)
- **ComfyUI untouched** (doc §25)

### Activation note
Copilot picks up `mcp.json` changes on the next MCP refresh (reload window / MCP panel refresh). Kilo needs the snippet pasted in its MCP tab.

### Next (slice 4, pending confirmation)
§10–14: web-search BEHAVIOR + research budget. Deliverable = a central config file (`D:\MCP\web-search-mcp\limits.json` or env) carrying `MAX_WEB_SEARCH_CALLS=8`, `MAX_WEB_PAGE_FETCHES=10`, `MAX_RESEARCH_TIME=120`, `MAX_IDENTICAL_WEB_CALLS=2` + the behavior rules (when to search / tool selection / date verification / untrusted content) as an instruction block for the clients. Design decision on WHERE the budget is enforced (server-side vs gateway) is finalized in slice 5.

---

## Slice 4 — Web-search behavior + research budget (2026-09-26) ✅

### Server env surface (verified from source — all read at RUNTIME, so the mcp.json `env` block is the correct mechanism)
- `browser-pool.ts`: `MAX_BROWSERS`, `BROWSER_HEADLESS`, `BROWSER_TYPES` (default `chromium,firefox`)
- `search-engine.ts`: `ENABLE_RELEVANCE_CHECKING`, `FORCE_MULTI_ENGINE_SEARCH`, `RELEVANCE_THRESHOLD`, `DEBUG_BING_SEARCH`, `DEBUG_BROWSER_LIFECYCLE`
- `enhanced-content-extractor.ts` / `content-extractor.ts`: `BROWSER_FALLBACK_THRESHOLD`, `DEFAULT_TIMEOUT`, `MAX_CONTENT_LENGTH`
- **KEY FIX:** `BROWSER_TYPES` defaults to `chromium,firefox` but only chromium is installed → pinned `BROWSER_TYPES=chromium` in the mcp.json env (prevents firefox launch failures).

### Files created/changed
- **`D:\MCP\web-search-mcp\limits.json`** (NEW) — CENTRAL config, single source of truth:
  - `webResearch`: `MAX_WEB_SEARCH_CALLS=8`, `MAX_WEB_PAGE_FETCHES=10`, `MAX_RESEARCH_TIME_SECONDS=120`, `MAX_IDENTICAL_WEB_CALLS=2`
  - `toolLimits`: `MAX_TOTAL_TOOL_CALLS=30`, `MAX_IDENTICAL_TOOL_CALLS=2`, `TOOL_TIMEOUT_SECONDS=60`, `MAX_REPEATED_SEQUENCE=3`
  - `browser`: the 7 env vars (incl. `BROWSER_TYPES=chromium`)
- **`D:\MCP\web-search-mcp\WEB_SEARCH_POLICY.md`** (NEW) — behavior policy for the clients: when-to-search triggers, current-info workflow, date-verification procedure, tool selection (summaries vs full vs single-page), research budget, untrusted-web-content rule.
- **`d:\models\vsCodeMcp\.vscode\mcp.json`** — added `BROWSER_TYPES=chromium` to the `web-search` env (now 7 vars). `comfy-mcp` untouched.

### Enforcement note (for slice 5)
The budget values in `limits.json` are NOT yet enforced by the server (the server has no built-in per-request budget). They will be enforced by the **local MCP gateway** built in slice 5 (doc section 15–21, 38). The policy md + limits.json are the inputs to that gateway.

### Next (slice 5, pending confirmation)
§15–21: build the **local MCP gateway** (thin Node stdio proxy) that both clients point at. It enforces: MAX_TOTAL_TOOL_CALLS, MAX_IDENTICAL_TOOL_CALLS (normalized-arg hash), TOOL_TIMEOUT, per-request web budget, repeated-sequence detection, failure-retry policy, structured LOOP_GUARD/TOOL_TIMEOUT errors, + logging. Reads limits from `limits.json`. Forwards valid calls unchanged to comfy-mcp + web-search.
