@echo off
REM ============================================================
REM ComfyUI AUTO-FREE watcher (2026-11-16).
REM Launches the resident watcher in a MINIMIZED window - keep
REM that window open (it is the watcher). After every ComfyUI
REM run it auto-unloads the loaded models (the server STAYS UP)
REM so the Qwen brain can load into the freed VRAM.
REM Stop: close the minimized "auto-free-comfyui" window, or
REM   Stop-ScheduledTask VsCodeMcp-AutoFreeComfyui
REM See auto_free_comfyui.ps1 for the full logic.
REM ============================================================
start "auto-free-comfyui" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0auto_free_comfyui.ps1"
echo Watcher launched (minimized window "auto-free-comfyui").
echo This window can be closed - the watcher runs in its own minimized window.
