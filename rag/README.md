# Local RAG — project memory + daily AI news (2026-10-24)

**Purpose (user directive):** stop manually lurking AI subs every weekend. A daily
pipeline fetches AI news (Reddit / X / HuggingFace), indexes it, and — together with our
project MD files — makes everything searchable instead of dumping all MD into the model.

## Architecture

```
chunking → embedding → vector DB → search back into prompt
```

- **Sources** (`config.json`):
  - **Reddit** (3-tier ladder, all best-effort, every tier logged):
    1. JSON API (unauth) — fast when the IP isn't flagged.
    2. `mcp_fetch.js` (repo root of ag/) — **the same engine VS Code's websearch MCP uses**
       (`D:\MCP\web-search-mcp`: axios fast path → randomized chromium fallback,
       same env as `D:\MCP\mcp-gateway`). Reuses the proven tooling instead of
       duplicating it.
    3. `C:\Program Files\Python310\python.exe D:\models\vsCodeMcp\utilities\reddit_browser_fetch.py <url> --text`
       (playwright, **persistent profile** — challenge state carries over).
    Subreddits: r/StableDiffusion · r/LocalLLaMA · r/ComfyUI · r/comfyui_workflows · r/artificial.
    **Reality check (2026-10-25):** Reddit walls hard rotate — one day the JSON API 403s,
    another day even the full browser engine hits "Prove your humanity" / "blocked by
    network security" (verified same-day against VS Code's own gateway: it got the SAME
    wall). When all 3 tiers fail, the run logs it and retries next day — the digest shows
    which source was blocked. Public redlib mirrors were probed: 429/502 (unreliable, not used).
  - **HuggingFace** (API, unauth): trending models (25) · top-downloads models (25) ·
    trending datasets (15). The reliable source today.
  - **X** (best-effort, unauth, 8 s spacing between accounts): syndication `timeline-profile`
    widget JSON for the tracked accounts in `config.json` (BennyDaBall_OG, xieenze_jr,
    PixelAigc, Alissonerdx, MaxLiu09, diodiogod, akatz_ai) + the `mcp_fetch.js` tier as
    fallback. Endpoint is unofficial + rate-limited (429 windows reset) — failures are
    logged, not fatal. Individual tweets can also be pulled on demand (used in P10 items 2/3/5):
    `https://cdn.syndication.twimg.com/tweet-result?id=<id>&lang=en&token=x`.
- **Storage:**
  - `news/<YYYY-MM-DD>/<source>_<id>.md` — one file per item (text-only, gitignored).
  - `news/digest_<date>.md` — human-readable daily digest (appended per run).
  - `news/state/seen.json` — dedup set (never re-index the same item).
  - `data/` — ChromaDB persistent store + `manifest_project.json` / `manifest_news.json`
    (content-hash manifests → idempotent incremental ingest).
- **Embedding:** `all-MiniLM-L6-v2` (384-dim) via **sentence-transformers on CPU ONLY**
  (zero VRAM contention with ComfyUI/llama.cpp — D192). Ollama is NOT installed on this box
  (checked 2026-10-24) — if Ollama is added later, `embed.py` can switch to `nomic-embed-text`.
- **Vector DB:** **FAISS-cpu `IndexIDMap(IndexFlatIP)`** (cosine on L2-normalized vectors),
  `data/<col>.faiss` + `data/<col>.meta.json` (id→metadata) + `manifest_*.json`
  (content-hash manifests → idempotent incremental ingest; changed files have their
  previous chunk ids deleted before re-adding — no orphans; `store.prune()` cleans any).
  (ChromaDB was tried first and is **broken on this machine** — Rust bindings fail with
  SQLITE_CANTOPEN code 14 on every path; left installed but unused. See D194.)
  Collections:
  - `project` — chunked sections of `project-memory/**` + `docs/**` + `episode1/**`
    (chunk ≈1600 chars, 150 overlap; each chunk prefixed with `[H1 > section]` context).
  - `news` — one embedding per news item (title+body, 9 k-char cap).

## Files

| File | Role |
|---|---|
| `config.json` | sources, accounts, chunk params — **edit this to add subreddits/accounts** |
| `chunk.py` | section-aware markdown chunker (stable ids) |
| `embed.py` | CPU MiniLM embedder (lazy load) |
| `fetch_news.py` | reddit + HF + X fetchers; saves items + digest; logs failures |
| `ingest_project.py` | incremental project-MD ingest (hash manifest) |
| `ingest_news.py` | incremental news ingest |
| `daily.py` | orchestrator: fetch → index news → reindex changed project files |
| `query.py` | CLI search (see below) |
| `run_daily_rag.bat` | scheduled-task entry |

## Usage

```bat
rem manual daily run
D:\models\vsCodeMcp\rag\run_daily_rag.bat

rem search (agent or user)
D:\models\vsCodeMcp\rag\.venv\Scripts\python.exe D:\models\vsCodeMcp\rag\query.py "character swap LoRA"
D:\models\vsCodeMcp\rag\.venv\Scripts\python.exe D:\models\vsCodeMcp\rag\query.py "HyperFlow" --collection project
D:\models\vsCodeMcp\rag\.venv\Scripts\python.exe D:\models\vsCodeMcp\rag\query.py "trending" --collection news --days 2 -k 12
```

## Scheduled task

`VsCodeMcp-RagDaily` — daily 08:00 (Asia/Calcutta) → `run_daily_rag.bat` (log:
`news\logs\scheduled.log` + `news\logs\daily_<date>.log`). Re-register if the task was removed:

```bat
schtasks /Create /TN VsCodeMcp-RagDaily /SC DAILY /ST 08:00 /TR "cmd /c D:\models\vsCodeMcp\rag\run_daily_rag.bat" /F
```

## For the agent (DSH)

Instead of loading ALL project MD files, call `query.py` with the task's keywords and feed
the top hits into context. Cross-reference: when a new post/repo is found (P-style batches),
query the RAG first — a hit in `project` = "we already tried/documented this"; a miss =
genuinely new.

## Failure modes

- **Network flake** (common on this box): every fetcher logs + skips; next run retries.
  News items are never lost (dedup is content/id based, files persist).
- **X syndication endpoint dead**: logged per account; drop the account from `config.json`
  or accept best-effort.
- **ChromaDB lock**: only one daily run at a time (the scheduled task is the only runner;
  don't run two `daily.py` concurrently).
