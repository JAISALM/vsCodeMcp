# shift_to_qwen.ps1 - ComfyUI -> Qwen brain shift (one click, 2026-11-16)
# Run this AFTER a ComfyUI run, before going back to chat:
#   1. asks ComfyUI to UNLOAD its models (server stays up - open tabs + MCP survive)
#   2. verifies the VRAM actually came back
#   3. starts the Qwen brain if :8100 is dark (direct llama-server setup)
$ErrorActionPreference = "Continue"
$base = "http://127.0.0.1:8188"

Write-Host "=== [1/3] Free ComfyUI's models (server stays up) ==="
try {
    $s0 = Invoke-RestMethod "$base/system_stats" -TimeoutSec 5
    $vram0 = $s0.devices[0].vram_free / 1GB
    $body = @{ unload_models = $true; free_memory = $true } | ConvertTo-Json
    $r = Invoke-WebRequest -Method POST "$base/free" -Body $body -ContentType "application/json" -TimeoutSec 10 -UseBasicParsing
    Write-Host ("ComfyUI asked to unload (HTTP {0}). vram_free was {1:N2} GB" -f $r.StatusCode, $vram0)
    $vram1 = $vram0
    foreach ($i in 1..30) {
        Start-Sleep 2
        $s = Invoke-RestMethod "$base/system_stats" -TimeoutSec 5
        $vram1 = $s.devices[0].vram_free / 1GB
        if ($vram1 -gt $vram0 + 0.5) { break }
    }
    Write-Host ("ComfyUI models evicted: vram_free now {0:N2} GB" -f $vram1)
} catch {
    Write-Host "ComfyUI is not running on :8188 - nothing to free."
}

Write-Host ""
Write-Host "=== [2/3] Brain check (:8100) ==="
$brainUp = $true
try { $null = Invoke-RestMethod "http://127.0.0.1:8100/v1/models" -TimeoutSec 3 } catch { $brainUp = $false }
if ($brainUp) {
    Write-Host "Brain endpoint is up (if this is the llama-swap daemon, the model auto-loads on your next message)."
} else {
    Write-Host "Brain (:8100) is dark - starting Qwen via Qwen3.827BMTP.bat (cold load ~1-2 min)..."
    Start-Process "D:\models\qwen\Qwen3.827BMTP.bat" -WorkingDirectory "D:\models\qwen"
}

Write-Host ""
Write-Host "=== [3/3] Done ==="
Write-Host "ComfyUI server idle (models freed, tabs alive) + Qwen loading/loaded."
Write-Host "The ComfyUI GUI's --reserve-vram 4 keeps 4 GB aside, so both coexist."
