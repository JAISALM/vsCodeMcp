# rebuild_vscode_mcp_tasks_admin.ps1
# Run ONCE from an ELEVATED prompt (PowerShell as administrator).
# Re-registers the two daily tasks with LogonType S4U (run whether or not the
# user is logged on - survives locked PC / no session). Non-elevated registration
# of S4U principals is refused by the Task Scheduler (0x80070005), so this
# script is the only path to the hardened version.
# The plain (interactive) versions already exist and work when a session is up;
# running this script replaces them with the S4U versions.

$ErrorActionPreference = "Stop"
$user = $env:USERNAME
Write-Host "Rebuilding VsCodeMcp tasks as S4U for: $user"

$trig = New-ScheduledTaskTrigger -Daily -At 8am

# --- RAG daily ---
$prag = New-ScheduledTaskPrincipal -UserId $user -LogonType S4U
$srag = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$arag = New-ScheduledTaskAction -Execute "D:\models\vsCodeMcp\rag\run_daily_rag.bat" -WorkingDirectory "D:\models\vsCodeMcp\rag"
Register-ScheduledTask -TaskName "VsCodeMcp-RagDaily" -Trigger $trig -Principal $prag -Settings $srag -Action $arag -Description "Daily RAG news fetch + digest (08:00, S4U, wakes PC)" | Out-Null

# --- Batch daily (pva retry + watchers) ---
$pb = New-ScheduledTaskPrincipal -UserId $user -LogonType S4U
$sb = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 4)
$ab = New-ScheduledTaskAction -Execute "powershell" -Argument "-NoProfile -ExecutionPolicy Bypass -File D:\models\vsCodeMcp\utilities\run_batch_daily.ps1" -WorkingDirectory "D:\models\vsCodeMcp"
Register-ScheduledTask -TaskName "VsCodeMcp-BatchDaily" -Trigger $trig -Principal $pb -Settings $sb -Action $ab -Description "Daily batch (08:00, S4U): pvanet.pt retry + rife49/sam31 checks + weekly_watch.py + Monday lab diff + DAILY_WATCH.md entry" | Out-Null

Write-Host "Done. Verify:"
foreach ($n in @("VsCodeMcp-RagDaily", "VsCodeMcp-BatchDaily")) {
    $x = schtasks /query /TN $n /xml 2>&1 | Out-String
    $s4u = if ($x -match "S4U") { "S4U" } else { "NOT-S4U" }
    $w = if ($x -match "WakeToRun") { "wake" } else { "no-wake" }
    Write-Host ("  {0}: {1} {2}" -f $n, $s4u, $w)
}
