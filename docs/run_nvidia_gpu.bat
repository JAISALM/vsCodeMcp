@echo off
cd /d %~dp0

if exist .\python.exe (
    set PYTHON_EXE=python.exe
) else (
    set PYTHON_EXE=.\python_embeded\python.exe
)

echo Starting ComfyUI...
REM auto-unload watcher (2026-11-16): frees loaded models after every run (server stays up)
start "auto-free-comfyui" /min powershell -NoProfile -ExecutionPolicy Bypass -File "D:\models\qwen\auto_free_comfyui.ps1"

%PYTHON_EXE% -s ComfyUI\main.py ^
 --windows-standalone-build ^
 --reserve-vram 4 ^
 --disable-cuda-malloc ^
 --enable-manager

pause
