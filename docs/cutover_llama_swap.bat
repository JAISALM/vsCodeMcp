@echo off
REM ============================================================
REM CUTOVER — DSH brain @8100 goes through llama-swap.
REM   1. kills the direct llama-server (frees the brain slot)
REM   2. starts llama-swap on :8100 (minimized window = the daemon)
REM   3. health-checks :8100 and reports
REM Run ONLY between tasks (a mid-turn switch costs one retried turn).
REM DSH config stays UNCHANGED (same port 8100).
REM Rollback: rollback_qwen_direct.bat
REM Stop llama-swap later: close its minimized window, or
REM   taskkill /F /IM llama-swap.exe
REM ============================================================
echo [1/4] Stopping direct llama-server...
taskkill /F /IM llama-server.exe >nul 2>&1
timeout /t 2 >nul
echo [2/4] Starting llama-swap on :8100 (minimized window stays open = the daemon)...
start "llama-swap-8100" /min "D:\tools\llama-swap\llama-swap.exe" -config "D:\tools\llama-swap\config.yaml" -listen 8100
timeout /t 4 >nul
echo [3/4] Health check...
curl.exe -s http://127.0.0.1:8100/v1/models >nul 2>&1
if %errorlevel%==0 (
  echo [OK] llama-swap is live on :8100.
  echo.
  echo   Web UI:  http://127.0.0.1:8100/ui/
  echo   Next brain message auto-loads Qwen (cold load ~1-2 min, then fast).
  echo   Rollback:  D:\models\qwen\rollback_qwen_direct.bat
  echo   Optional:  stop the old :8200 test daemon -
  echo              taskkill /F /PID 5464
) else (
  echo [FAIL] llama-swap did not come up on :8100.
  echo        Log: D:\tools\llama-swap  (check the minimized window)
  echo        Rollback NOW:  D:\models\qwen\rollback_qwen_direct.bat
)
echo.
echo [4/4] This window can be closed. KEEP the minimized "llama-swap-8100" window open.
timeout /t 6 >nul
