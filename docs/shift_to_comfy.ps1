# shift_to_comfy.ps1 - Qwen brain -> ComfyUI shift (one click, 2026-11-16)
# Run BETWEEN tasks - the brain (this chat's LLM) goes down while ComfyUI
# owns the GPU for the run.
#   1. unloads Qwen: llama-swap daemon -> graceful API unload (daemon stays up,
#      brain auto-loads on your next message); direct llama-server -> taskkill
#      (brain comes back via start_qwen_8100.bat)
#   2. starts ComfyUI if :8188 is dark
$ErrorActionPreference = "Continue"

Write-Host "=== [1/3] Free Qwen's VRAM ==="
$viaSwap = $false
try {
    $null = Invoke-RestMethod "http://127.0.0.1:8100/api/models/unload" -Method POST -TimeoutSec 8
    $viaSwap = $true
} catch { }
if ($viaSwap) {
    Write-Host "Qwen unloaded via llama-swap (daemon stays up - brain auto-loads on your next message)."
} else {
    $k = taskkill /F /IM llama-server.exe 2>&1
    Write-Host ("taskkill llama-server: " + ($k -join " "))
    Write-Host "NOTE: this is the DIRECT llama-server setup (pre-cutover). The brain"
    Write-Host "comes back when you double-click start_qwen_8100.bat (or shift_to_qwen.bat)."
}

Write-Host ""
Write-Host "=== [2/3] ComfyUI check (:8188) ==="
$comfyUp = $true
try { $null = Invoke-RestMethod "http://127.0.0.1:8188/system_stats" -TimeoutSec 3 } catch { $comfyUp = $false }
if ($comfyUp) {
    Write-Host "ComfyUI is already running - queue your run."
} else {
    Write-Host "Starting ComfyUI (run_nvidia_gpu.bat, minimized window)..."
    Start-Process "E:\comfyUi_latest\ComfyUI_windows_portable\run_nvidia_gpu.bat" -WorkingDirectory "E:\comfyUi_latest\ComfyUI_windows_portable" -WindowStyle Minimized
    Write-Host "Give it ~30-60 s to come up, then queue."
}

Write-Host ""
Write-Host "=== [3/3] Done ==="
Write-Host "ComfyUI owns the GPU. When the run is done: double-click shift_to_qwen.bat"
Write-Host "(or just run free_comfyui_vram.bat to keep the server up and reload the brain)."
