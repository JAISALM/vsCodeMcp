# free_comfyui_vram.ps1 - Free ComfyUI's VRAM, server STAYS UP (fixed 2026-11-16)
#
# ROOT CAUSE of the old bat doing nothing:
#   the old bat ran  `curl.exe -s -X POST http://127.0.0.1:8188/free`  - NO BODY.
#   ComfyUI's /free handler (server.py ~line 1294) does:
#       json_data = await request.json()
#       unload_models = json_data.get("unload_models", False)
#       free_memory   = json_data.get("free_memory", False)
#   A body-less POST makes request.json() raise -> the server returns
#   "500 Internal Server Error" (verified 2026-11-16), so NEITHER flag is set
#   and NOTHING is unloaded - while `curl -s` hid the 500 and the bat printed
#   a fake "Done. Models evicted from VRAM".
#
# This version:
#   1. sends the proper JSON body {"unload_models":true,"free_memory":true}
#   2. measures /system_stats BEFORE and AFTER and prints the ACTUAL VRAM freed
#      (no fake success - if nothing was loaded, it says so)
#
# The flag is consumed by the prompt-queue worker on its next iteration (the
# server's own docs: applied at the next worker iteration, does not interrupt a
# running job) - so we poll up to 60 s for the VRAM to actually come back.
$ErrorActionPreference = "Stop"
$base = "http://127.0.0.1:8188"

# --- 1. is the server up? ---
try { $s0 = Invoke-RestMethod "$base/system_stats" -TimeoutSec 5 }
catch {
    Write-Host "[FAIL] ComfyUI is not running on :8188."
    Write-Host "       Start it first: E:\comfyUi_latest\ComfyUI_windows_portable\run_nvidia_gpu.bat"
    exit 1
}
$vram0 = $s0.devices[0].vram_free / 1GB
$ram0  = $s0.system.ram_free / 1GB
Write-Host ("BEFORE  vram_free = {0:N2} GB / {1:N2} GB    ram_free = {2:N2} GB" -f $vram0, ($s0.devices[0].vram_total/1GB), $ram0)

# --- 2. THE actual free request (the part the old bat got wrong) ---
$body = @{ unload_models = $true; free_memory = $true } | ConvertTo-Json
try {
    $r = Invoke-WebRequest -Method POST "$base/free" -Body $body -ContentType "application/json" -TimeoutSec 10 -UseBasicParsing
    if ($r.StatusCode -ne 200) { Write-Host "[FAIL] POST /free returned HTTP $r.StatusCode"; exit 1 }
} catch {
    Write-Host ("[FAIL] POST /free rejected: " + $_.Exception.Message)
    exit 1
}
Write-Host "POST /free accepted (HTTP 200). Waiting for the prompt-queue worker to evict the models (up to 60 s)..."

# --- 3. poll for the VRAM to actually come back ---
$vram1 = $vram0
$ram1  = $ram0
foreach ($i in 1..30) {
    Start-Sleep 2
    try {
        $s = Invoke-RestMethod "$base/system_stats" -TimeoutSec 5
        $vram1 = $s.devices[0].vram_free / 1GB
        $ram1  = $s.system.ram_free / 1GB
        if ($vram1 -gt $vram0 + 0.5) { break }
    } catch { Start-Sleep 1 }
}
Write-Host ("AFTER   vram_free = {0:N2} GB    ram_free = {1:N2} GB" -f $vram1, $ram1)
Write-Host ("FREED   vram {0:N2} GB" -f ($vram1 - $vram0))

if ($vram1 -lt $vram0 + 0.5) {
    Write-Host "NOTE: nothing (or little) was freed - either no models were loaded"
    Write-Host "(fresh/idle server - that is fine, nothing to do) or an orphaned"
    Write-Host "process is squatting VRAM. Check Task Manager for stray python.exe /"
    Write-Host "node processes. Nuclear option: close the ComfyUI console window"
    Write-Host "(run_nvidia_gpu.bat) - that always frees everything."
} else {
    Write-Host "Done - models evicted from VRAM, server STILL RUNNING (open tabs + MCP survive)."
    Write-Host "The brain (Qwen @8100) can load into the freed VRAM now."
}
