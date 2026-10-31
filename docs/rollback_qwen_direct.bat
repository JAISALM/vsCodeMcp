@echo off
REM ============================================================
REM ROLLBACK — back to the direct llama-server on :8100
REM (the pre-llama-swap setup). Run if llama-swap misbehaves.
REM ============================================================
taskkill /F /IM llama-swap.exe >nul 2>&1
timeout /t 2 >nul
echo Relaunching direct Qwen brain on :8100...
start "" "D:\models\qwen\start_qwen_8100.bat"
echo Done — brain returns on :8100.
