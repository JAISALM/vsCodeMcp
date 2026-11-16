@echo off
REM ============================================================
REM Qwen BRAIN -> ComfyUI shift (one click, 2026-11-16).
REM Run BETWEEN tasks: unloads Qwen (llama-swap API if the daemon
REM is up, else taskkill llama-server), starts ComfyUI if dark.
REM The brain goes down while ComfyUI owns the GPU - it comes
REM back via start_qwen_8100.bat / shift_to_qwen.bat.
REM See shift_to_comfy.ps1 for the full logic.
REM ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0shift_to_comfy.ps1"
pause
