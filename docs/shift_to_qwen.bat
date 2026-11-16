@echo off
REM ============================================================
REM ComfyUI -> Qwen BRAIN shift (one click, 2026-11-16).
REM Run AFTER a ComfyUI run: unloads ComfyUI's models (server
REM stays up), verifies the VRAM came back, starts Qwen if dark.
REM See shift_to_qwen.ps1 for the full logic.
REM ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0shift_to_qwen.ps1"
pause
