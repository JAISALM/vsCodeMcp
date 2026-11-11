@echo off
rem ============================================================
rem  Qwen3.5-4B (Q6)  -  ideal llama.cpp server config
rem  Targets the GTX 1660 Ti (6 GB) but works on the 5090 too.
rem
rem  FIXES THE "18s for hi" PROBLEM:
rem    1) -ngl 99      -> EVERY layer on the GPU (4B Q6 is only
rem                       ~3.5 GB, fits in 6 GB with room for KV).
rem                       A CPU-only run is the classic 18s cause.
rem    2) -c 8192      -> sane context. A huge default (32k/128k)
rem                       makes every request pre-process a lot.
rem    3) --flash-attn -> smaller KV cache + faster attention.
rem    4) thinking off -> see the note at the bottom.
rem ============================================================
cd /d D:\llama

rem >>> EDIT THESE TO MATCH YOUR MACHINE <<<
set MODEL=D:\models\qwen3.5-4b-Q6_K_M.gguf
set PORT=8081
set CTX=8192
rem Set THREADS = your CPU's PHYSICAL core count (not logical/HT).
rem e.g. a 6-core/12-thread CPU -> THREADS=6
set THREADS=8

llama-server.exe ^
  -m %MODEL% ^
  --host 127.0.0.1 ^
  --port %PORT% ^
  --alias qwen3.5-4b ^
  -ngl 99 ^
  -c %CTX% ^
  -t %THREADS% ^
  -b 512 ^
  -ub 512 ^
  --flash-attn on ^
  --jinja ^
  --parallel 1 ^
  --cont-batching ^
  --no-mmap ^
  --cache-type-k q8_0 ^
  --cache-type-v q8_0

pause

rem ============================================================
rem VERIFY IT'S ACTUALLY ON THE GPU (watch the console at startup):
rem   * "CUDA: found 1 device(s)"            -> CUDA is active
rem   * "offloaded  N/NN layers to GPU"      -> must be ALL layers
rem   * NO CUDA lines, or "offloaded 0 layers" -> you're on CPU.
rem     That is your bug: use the CUDA build of llama.cpp, or
rem     the model isn't being offloaded.
rem
rem THE OTHER SUSPECT - THINKING MODE:
rem Qwen3.x has a "thinking" mode. When it's ON, the model writes
rem a long hidden reasoning block BEFORE the visible answer, even
rem for "hi". That alone explains 18s + 2min for a hello-world.
rem To turn it OFF with this server:
rem   * put a system prompt containing  /no_think  on line 1, OR
rem   * if you use an OpenAI-compatible client, send
rem       "chat_template_kwargs": {"enable_thinking": false}
rem   * if you're actually on OLLAMA instead:
rem       ollama run qwen3.5:4b /no_think
rem ============================================================
