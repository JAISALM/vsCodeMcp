# WRITING SETUP — Resume Manual (movie-writing DSH)

> Self-contained. Any session (any model) resuming the writing work should read THIS first.
> Built 2026-10-08 (D114). Active project = the AI MOVIE (D115; Jaisal archived).
> Last verified: 2026-10-08.

## What exists
A second DSH profile (`writing`) running the same DSH web GUI in parallel with the main
`web` profile, aimed at the writing models under `D:\models\Writing`, with the web-search
MCP ("wbemcp") attached for research/data-check passes.

## Files
| What | Where |
|---|---|
| DSH writing profile | `C:\Users\user\.dsh\profiles\writing\` (cordis.patch.yml = models + MCP; YAML validated) |
| Main DSH profile | `C:\Users\user\.dsh\profiles\web` (port 3080, default Qwen3.8-27B @8100) — **since 2026-10-08 evening the 4 writing providers are ALSO registered here** (so writing models appear in the main GUI's model dropdown; restart the GUI window to pick them up) |
| One-click Muse starter | `D:\models\Writing\start_muse_dsh.bat` (server @8101 + GUI @3081) |
| One-click Qwen3-VL starter | `D:\models\Writing\start_qwen3vl_dsh.bat` (server @8105 + GUI @3081) |
| Muse 5090-safe runner | `D:\models\Writing\Meta\run-muse-32k.bat` (ctx 32768) |
| Muse ctx probe | `D:\models\Writing\probe-muse-ctx.bat` (260K→131K→98K→65K→32K; first boot wins, leaves server running) |
| **Registry/cheat sheet** | `D:\models\Writing\DSH_MODEL_REGISTRY.md` (how to register + use ANY model in DSH — port map, 3-layer model, add-model checklist, troubleshooting) |
| Raw GUI command (user's own pattern) | `pnpm.cmd -C D:\dsh dsh web --profile writing --port 3081` |
| Writing GUI URL | http://127.0.0.1:3081 |

## Models — ONE AT A TIME (32GB VRAM); the 3081 GUI can run alongside any of them
| Model (size) | Port | Server .bat | Role |
|---|---|---|---|
| **Muse-Glimmer-30B-heretic Q5** (18.7GB) | 8101 | `Meta\Run-Muse-Glimmer.bat` (ctx 260K — **PROVEN BOOTS 2026-10-08**) / `Meta\run-muse-32k.bat` (conservative fallback) | **EDITOR + 260K whole-script/long-context workhorse** ("great as an editor, or as a writer if you hold its hand" — reddit 1wcwa7i); heretic finetune fixes the base's refusal problem |
| Qwen3-VL-32B ultra-uncensored-heretic Q5 (21.6GB) | 8105 | `Qwen\run-qwen3-vl-heretic.bat` (ctx 32K) | vision-capable alternate (storyboard→prose) |
| Qwen3-32B-Uncensored Q5 (21.6GB) | 8102 | `Qwen\run-qwen3-32b-uncensored.bat` (ctx 32K) | text-only creative writing |
| Dolphin-Mistral-24B Venice Q6 (18GB) | 8103 | `Mistral\run-dolphin-venice.bat` (ctx 64K) | implication analysis + data-checks (function-calling + web MCP) |
| Gemma4-26B-A4B MoE (15.6GB) | — | no bat yet (add on request) | fast throwaway drafts |
| **Gemma4-31B-QAT HauhauCS Balanced Q4_K_M (~19GB)** | **8106** | `Gemma\run-gemma4-31b-qat.bat` (ctx 32K) | **⭐ FINAL WRITER (writing-profile DEFAULT, 2026-10-11)** — reddit 1wcwa7i: best character portrayal/consistency/plot of the group, runs unguided; HauhauCS finetune removes its "not X, it's Y" prose tic. **ON DISK 2026-10-12** (17.40 GB model + 1.12 GB mmproj present; bat paths verified exact match; bat auto-adds `--mmproj`; optional 280 MB MTP draft not yet downloaded). |
| **Ortenzya "Creative Wordsmith" 31B (llmfan46) Q5_K_M (21.9GB)** | **8107** | `Gemma\run-ortenzya-31b-q5.bat` (ctx 32K) | **A/B writing-specialist alternate** — most-downloaded uncensored creative-writing GGUF (314K dl; creative writing / visual novels / roleplay, en+ja; non-QAT base). FITS the 32GB card (~24.5 GB w/ 1.2 GB mmproj + 32K q8_0 KV). **ON DISK 2026-10-12** (20.35 GB model + 1.12 GB mmproj present; bat paths verified). **DSH provider `writing-ortenzya` @8107 added to BOTH profiles 2026-10-12** (dump-config clean; dropdown after GUI restart + new session). A/B vs HauhauCS QAT on the same task. Bonus on disk: `Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf` (15.64 GB MoE fast-throwaway — no bat yet). |
| Qwen3-VL MiniMax-H3 (13.9GB + mmproj 2.2GB) | 8104 | `Qwen\run-minimax-h3-heretic.bat` | H3-prompting specialist — NOT for writing |

Uncensored status: ALL creative models are uncensored/low-refusal (heretic / uncensored /
Venice labels) — nothing will refuse mature drama scenes. MiniMax-H3 instruct = the only
non-uncensored one (and not for writing anyway). Qwen3.8-27B @8100 = orchestration/coding
brain only — user confirmed NOT for writing.

## How to run
1. Free the card if needed: stop the main DSH model server (port 8100).
2. Start ONE writing model's .bat (its window = the server; keep open).
3. GUI: the starter bat handles it, or manually `pnpm.cmd -C D:\dsh dsh web --profile writing --port 3081`.
4. Open http://127.0.0.1:3081. Default model = **Gemma4-31B-QAT** (`writing-gemma4`, final writer choice 2026-10-11 — reddit thread evidence; needs the GGUF downloaded + server running, else pick another). Switch per session via the model picker (`writing-gemma4` / `writing-ortenzya` [A/B alternate] / `writing-muse` [editor + 260K ctx] / `writing-qwen3vl` / `writing-qwen3` / `writing-dolphin`).
   To change the DEFAULT permanently: edit `agent-default-model` in `C:\Users\user\.dsh\profiles\writing\cordis.patch.yml` (ask any agent).
5. Web MCP (web-search via `D:\MCP\mcp-gateway`) is attached for research/data-check passes.
6. **Credential:** DSH requires `WRITING_LOCAL_KEY` to resolve (dummy value — llama.cpp ignores it). Set as **user env var** `WRITING_LOCAL_KEY=local` (like `QWEN_LOCAL_KEY=local`) AND in the 3 `start_*.bat` files. If a session errors `no credential for provider route ...`: GUI window must be RESTARTED to pick up the env var (or set the key on the DSH web Models page = credential service). See `D:\models\Writing\DSH_MODEL_REGISTRY.md`.

### Stopping / restarting the MAIN agent server (port 8100)
Needed before running the Muse ctx probe (card needs full 32GB). Find PID:
`Get-CimInstance Win32_Process -Filter "Name='llama-server.exe'" | Select-Object ProcessId, CommandLine`
then `taskkill /F /PID <pid>`. Restart with (captured verbatim from the live process 2026-10-08):
```
"D:\llama\llama-server.exe" -m "D:\models\qwen\Qwen3.8-27B-NVFP4-MTP-LOW.gguf" --mmproj "D:\models\qwen\mmproj-BF16.gguf" --port 8100 -ngl 99 --ctx-size 260000 --cache-type-k q8_0 --cache-type-v q8_0 --kv-unified --flash-attn on --spec-type draft-mtp --spec-draft-n-max 4 --spec-draft-n-min 2 -b 512 -ub 512 --parallel 1 --jinja -n 8192 --metrics
```
NOTE: while 8100 is stopped, NO DSH session can get LLM responses — stop it only as the last step of a session, then restart it.

## PENDING (in order)
1. ~~Muse ctx probe~~ **DONE 2026-10-08: 260000 FITS** (probe's first attempt booted + 200 OK, even with 8100 running). Use the original `Run-Muse-Glimmer.bat` (260K). Caveat: with 8100 ALSO running both servers are slow (~2 tok/s coexistence, GPU 31.9/32.6GB) — stop 8100 for real writing speed. `start_muse_dsh.bat` still launches `run-muse-32k.bat` — update it to `Run-Muse-Glimmer.bat` when convenient.
2. **Movie script from user** → then build the writing workspace: `character_bible.md` (appearance/voice/arc per character — single source of truth for dialogue AND image prompts), `continuity_ledger.md` (timeline/props/locations/costumes), `beats.md`, `drafts/` + the stage→model pipeline (D114.5: analysis→Muse, drafts→Muse/Qwen3-VL, dialogue→Dolphin, continuity+data-check→Dolphin+web-mcp, shot-list conversion→Qwen3-VL).
3. **Character dataset (D113)** — user queues `krea2_dataset_char1.json` + `krea2_dataset_char2.json` (fresh tabs, ComfyUI 8188) → 34 images → review/keep 20 per char → per-character Krea2 LoRA training (`E:\AI-Toolkit-Easy-Install`) → apply LoRAs to movie shot generation.
4. **Offered, not yet done:** 3-model bake-off (Muse vs Qwen3-VL vs Dolphin) on the user's actual synopsis — evidence beats guess.
5. Paused goal `goal-76fa272d-31d4-4dc9-ac8e-b125cef5156e` — resume ONLY on user's exact phrase "let me run the pe3 workflows".
6. **Malayalam input for the script (D116, 2026-10-12):** type in Manglish → convert per scene via `d:\models\vsCodeMcp\prompts\manglish_to_malayalam.txt` (local LLM pass — tone + name consistency lock). Voice: Win+H (quick, Malayalam supported) or `d:\models\vsCodeMcp\utilities\transcribe_malayalam.py` (local Whisper large-v3, Audacity WAV → `.ml.txt` with timestamps; first run auto-installs faster-whisper). Browser tiers: Google Input Tools extension / GitHub `vijithvt-official/Google-Input-Tools` offline installer / malayalam-typing.in.

## Measured facts (2026-10-08, RTX 5090 32GB)
- Agent's own 27B NVFP4 server (port 8100) runs `--ctx-size 260000` q8_0 KV + flash-attn + MTP → uses **29.4GB / 32.6GB** (nvidia-smi).
- Weights: 27B NVFP4 = 14.47GB; Muse Q5 = 18.72GB. **PROBE RESULT (2026-10-08 22:53): Muse BOOTS at 260000 ctx** (first attempt won; even with 8100 co-resident) — the original `Run-Muse-Glimmer.bat` is safe on this machine; both "won't fit" predictions were wrong (Muse's KV is lighter than estimated). Coexistence speed test: Muse 2.3 tok/s + agent 1.4 tok/s (16-token test, GPU 31.9/32.6GB) — stop 8100 for writing work.
- DSH sessions auto-condense (checkpoint) when context fills — session lifetime ≠ context limit (observed 31.4M cumulative tokens, ~60% prefix-cache hit). Project memory files are the permanent handoff record (this manual included).
