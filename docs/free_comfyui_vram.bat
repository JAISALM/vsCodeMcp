@echo off
REM ============================================================
REM Free ComfyUI's VRAM after a heavy run (server STAYS UP).
REM FIXED 2026-11-16: the old version ran `curl -X POST /free`
REM with NO JSON body - the handler (server.py /free) crashes on
REM a body-less request (500) and frees NOTHING, while `curl -s`
REM hid the error and this bat printed a fake "Done". The real
REM work is now in free_comfyui_vram.ps1: proper JSON body
REM {"unload_models":true,"free_memory":true} + measured
REM before/after VRAM (no fake success).
REM Use BEFORE switching back to Qwen/DSH chat.
REM If this doesn't free enough (orphaned node process squatting),
REM close the ComfyUI GUI instead.
REM ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0free_comfyui_vram.ps1"
pause
