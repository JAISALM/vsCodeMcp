@echo off
REM ============================================================
REM Free ComfyUI's GPU after a heavy run (server STAYS UP).
REM Use BEFORE you switch back to Qwen/DSH chat, so Qwen loads
REM into freed VRAM instead of a dirty card.
REM The idle server keeps running (MCP stays alive) - only the
REM loaded models are evicted from VRAM.
REM If this doesn't free enough (orphaned node process squatting),
REM close the ComfyUI GUI instead, or see Berth (stage 2).
REM ============================================================
echo Asking ComfyUI on :8188 to unload all models...
curl.exe -s -X POST http://127.0.0.1:8188/free
echo.
echo Done. Models evicted from VRAM, server still running.
echo You can now talk to Qwen (DSH) - it will auto-load cleanly.
