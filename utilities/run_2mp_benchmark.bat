@echo off
REM ============================================================
REM  MiniMax H3 T2V resolution benchmark (1.0 / 1.5 / 2.0 MP)
REM  Workflow: t2v_beach_sprint_test.json (PURE T2V — no reference images, 10s)
REM
REM  BEFORE RUNNING THIS:
REM    1. ComfyUI must be RUNNING (run_nvidia_gpu.bat)
REM    2. This script stops Qwen (llama-server) automatically
REM
REM  Total runtime: ~45-50 min (10s video: ~4:30 + ~9:00 + ~15:00)
REM  Outputs: E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output\video\T2V_Beach_Sprint_TEST_*.mp4
REM  Results: d:\models\vsCodeMcp\benchmark_results.txt
REM ============================================================

echo Stopping Qwen (llama-server)...
taskkill /F /IM llama-server.exe 2>nul
timeout /t 5 /nobreak >nul

echo Starting T2V benchmark sweep (1.0 / 1.5 / 2.0 MP) on t2v_beach_sprint_test.json...
"E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe" "d:\models\vsCodeMcp\run_2mp_benchmark.py"

echo.
echo Benchmark finished. Results: d:\models\vsCodeMcp\benchmark_results.txt
pause
