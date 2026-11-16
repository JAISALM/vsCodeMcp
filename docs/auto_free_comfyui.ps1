# auto_free_comfyui.ps1 - resident auto-unload watcher (2026-11-16)
#
# Polls ComfyUI's /queue. When a run FINISHES (queue was busy, then empty
# for ~9 s = 3 polls), it automatically POSTs /free with the proper JSON
# body ({"unload_models":true,"free_memory":true}) - models evicted from
# VRAM + executor cache cleared - so the Qwen brain can load into the freed
# VRAM. The ComfyUI server is NEVER stopped (open tabs + MCP stay alive).
#
# Start: double-click auto_free_comfyui.bat (minimized window), or the logon
# scheduled task "VsCodeMcp-AutoFreeComfyui" runs it automatically.
# Stop : close the minimized window, or
#         Stop-ScheduledTask VsCodeMcp-AutoFreeComfyui  (stops the next start)
#       + kill the powershell window.
#
# The ~9 s grace (3 consecutive empty polls) means a quick follow-up run
# queued right after the previous one does NOT trigger a free - the models
# stay warm for it.
$base = "http://127.0.0.1:8188"
$busy = $false
$emptyPolls = 0
Write-Host ("[{0}] auto-free watcher up (polling {1}/queue every 3 s)" -f (Get-Date -Format "HH:mm:ss"), $base)
Write-Host "The ComfyUI server is NEVER stopped - only loaded models are evicted."
Write-Host "Close this window (or Stop-ScheduledTask VsCodeMcp-AutoFreeComfyui) to stop."
while ($true) {
    try {
        $q = Invoke-RestMethod "$base/queue" -TimeoutSec 5
        $running = $q.queue_running.Count
        $pending = $q.queue_pending.Count
        if ($running -gt 0 -or $pending -gt 0) {
            $busy = $true
            $emptyPolls = 0
        }
        elseif ($busy) {
            $emptyPolls += 1
            if ($emptyPolls -ge 3) {
                $body = @{ unload_models = $true; free_memory = $true } | ConvertTo-Json
                $r = Invoke-WebRequest -Method POST "$base/free" -Body $body -ContentType "application/json" -TimeoutSec 10 -UseBasicParsing
                Write-Host ("[{0}] run finished - models auto-freed (HTTP {1}), server still running" -f (Get-Date -Format "HH:mm:ss"), $r.StatusCode)
                $busy = $false
                $emptyPolls = 0
            }
        }
    } catch {
        # ComfyUI down or port busy - keep polling, never die
        $busy = $false
        $emptyPolls = 0
    }
    Start-Sleep 3
}
