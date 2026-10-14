# HANDOVER — new session, read first (2026-10-12)

Compact resume note. Full detail lives in the files referenced. Read order:
PROJECT_STATE.md → this file → CURRENT_TASK.md header → WRITING_SETUP.md.

## What just happened (last few hours)
- **Final writer chosen: Gemma4-31B-QAT (HauhauCS Balanced)** — writing-profile DEFAULT = `writing-gemma4` (port 8106, ctx 32K, `Gemma\run-gemma4-31b-qat.bat`). Evidence: reddit 1wcwa7i + arena creative-writing leaderboard (gemma-4-31b = #16 of 223 open-source, 1418). Muse-Glimmer-30B-heretic = editor + 260K long-context workhorse (port 8101).
- **User is downloading Gemma4-31B** → `D:\models\Writing\Gemma\Gemma4-31B-QAT-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf` (~19GB). URLs for all candidates in DECISIONS (D114 tail). When it lands: run the bat → restart GUI → pick it in dropdown.
- **Web MCP (web-search, headless Chromium, NO keys) — ROOT CAUSE FOUND + FIXED (2026-10-12, D117):** the profile entries were declared as bare top-level `id:` entries, which the patch loader treats as id-targeted OVERRIDES — all three web-profile MCP clients were silently dropped (`patch: entry "mcp-websearch" not found` warning, non-fatal) and never loaded. Rewritten as `insert:` lists in both `cordis.patch.yml` files; verified clean via `--dump-config` (zero warnings, entries in composed tree). Chain itself verified healthy end-to-end (test `D:\MCP\mcp-gateway\dsh-attach-test.js` → 3 tools + reset). **STILL PENDING: GUI restart (`cd D:\dsh` + `pnpm.cmd -C D:\dsh dsh web`, @3080) + NEW session** — MCP tools attach per session. **VERIFY FIRST THING IN NEW SESSION: tool list includes `mcp__websearch__full-web-search` / `get-web-search-summaries` / `get-single-web-page-content`? If yes — keyless web access works. If no — check GUI console for `[gateway] ready. tools: ...` and whether a `node D:\MCP\mcp-gateway\index.js` child process exists under the GUI node process.** Keyless fallback until then: `web_fetch` + DDG html + HF API. (Built-in harness `web_search` = DeepSeek-backend feature needing `DEEPSEEK_API_KEY` — never needed.)
- **Reddit direct access** — works via session cookie: user env `REDDIT_SESSION_COOKIE` (stored), helper `d:\models\vsCodeMcp\utilities\reddit_fetch.py` (auto-solves the JS challenge, persists cookies in `C:\Users\user\.dsh\fetch_creds\reddit_cookies.txt`). Edge may 403-block after bursts — back off a few minutes or use mirror `red.artemislena.eu`. X: single tweets work anonymously (syndication endpoint); user DECLINED sharing X cookies — MCP browser route is the plan.
- **Credential hygiene (user decision):** no auth details shared for X; `REDDIT_USER`/`REDDIT_PASS` env vars exist from earlier offer — user may want them removed (ask). `WRITING_LOCAL_KEY=local` + `QWEN_LOCAL_KEY=local` user-env vars are the DSH LLM credentials.

## Standing setup (unchanged)
- Agent brain: Qwen3.8-27B @8100 (NEVER stop it — kills all DSH sessions; restart command in WRITING_SETUP.md).
- Writing servers: one at a time (32GB). Port map + registry sheet: `D:\models\Writing\DSH_MODEL_REGISTRY.md`.
- Movie project: Krea2 char1/char2 datasets built (validate clean), awaiting user queue; movie script still owed by user. Jaisal archived (D115).
- Goal `goal-76fa272d` PAUSED — resume ONLY on user's "let me run the pe3 workflows".

## Pending queue (in priority order)
1. Confirm web-MCP tools present in new session (above).
2. Gemma4-31B download → run bat → first writing test vs Muse (same prompt, both models). **mmproj update (2026-10-11): BOTH repos ship their own 1.2 GB mmproj** (HauhauCS: `mmproj-Gemma4-31B-QAT-...-BF16.gguf`; Ortenzya: `...-mmproj-BF16.gguf` — URLs in the bat headers; both bats auto-add `--mmproj` when the file exists). Mixing is safe (same gemma4 arch/base lineage) but use each model's own. **Ortenzya Q5_K_M FITS the 32GB card** (~24.5 GB w/ mmproj + 32K q8_0 KV) → new runner `Gemma\run-ortenzya-31b-q5.bat` @8107 for the A/B.
3. Movie script arrives → build writing workspace (character bible, continuity ledger — see WRITING_SETUP.md stage→model map).
4. Dataset phase (D113) on user's queue (fresh ComfyUI tabs, 34 images, then per-char LoRA).
5. Optional: A/B HauhauCS-QAT vs `llmfan46/gemma-4-Ortenzya-The-Creative-Wordsmith-31B-it-uncensored-heretic-GGUF` (writing-specific, non-QAT).
6. Remove `REDDIT_USER`/`REDDIT_PASS` env vars if user confirms.
