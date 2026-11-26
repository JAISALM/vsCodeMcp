# watch_progress.ps1 - STANDING download/progress monitor (the reusable "fire")
# PURE ASCII ONLY (Windows PowerShell 5.1 reads .ps1 as cp1252; any UTF-8 symbol breaks parsing)
# MB/s = folder growth rate (works in EVERY stage). Engine line = % / package / ETA when the
# engine emits a GB counter. 20 s poll; ends when the process exits.
# Usage:  powershell -ExecutionPolicy Bypass -File utilities\watch_progress.ps1 [-Root D:\SomeFolder] [-Log D:\SomeFolder\console.log] [-Pattern install_rgbmocap|Install_RGBMoCap]
param(
    [string]$Root = "D:\RGBMoCapInstaller",
    [string]$Log = "",
    [string]$Pattern = "install_rgbmocap|Install_RGBMoCap"
)
if (-not $Log) { $Log = Join-Path $Root "console.log"; if (-not (Test-Path $Log)) { $Log = Join-Path $Root "install_log.txt" } }
$prevSize = $null; $prevTime = $null; $rate = 0.0

function Get-Alive {
    $procs = Get-CimInstance Win32_Process -Filter "Name='cmd.exe' OR Name='python.exe' OR Name='uv.exe' OR Name='curl.exe' OR Name='git.exe'" -ErrorAction SilentlyContinue
    $procs | Where-Object { $_.CommandLine -match $Pattern -and $_.ProcessId -ne $PID } | Select-Object -First 1
}

Write-Host "=== progress: $Root ==="
Write-Host "(MB/s = folder growth; engine line = % / package / ETA; 20 s poll; close anytime)"
Write-Host ""

while ($true) {
    $alive = [bool](Get-Alive)
    $size = 0.0
    $r = Get-ChildItem $Root -Recurse -File -ErrorAction SilentlyContinue
    $sum = ($r | Measure-Object Length -Sum).Sum
    if ($sum) { $size = [Math]::Round($sum / 1GB, 1) }
    if ($prevSize -ne $null -and $prevTime -ne $null -and $size -gt 0) {
        $dt = ((Get-Date) - $prevTime).TotalSeconds
        if ($dt -gt 5) { $rate = [Math]::Round(($size - $prevSize) * 1024 / $dt, 1); if ($rate -lt 0) { $rate = 0.0 } }
    }
    $prevSize = $size
    $prevTime = Get-Date
    $last = "no log yet"
    $stage = ""
    $prog = ""
    if (Test-Path $Log) {
        $tail = (Get-Content $Log -Tail 1 -ErrorAction SilentlyContinue)
        if ($tail) {
            $chunks = @($tail -split "`r" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" })
            $last = if ($chunks.Count) { $chunks[-1] } else { "" }
            $progLine = @($chunks | Where-Object { $_ -match "\d{1,3}\.\d+%" } | Select-Object -Last 1)
            if ($progLine.Count) { $prog = $progLine[0] }
            $stageLine = @($tail -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -match "=== \d+/\d+" } | Select-Object -Last 1)
            $stage = if ($stageLine.Count) { $stageLine[0] } else { "" }
        }
    }
    if ($last.Length -gt 70) { $last = $last.Substring(0, 70) + "..." }
    if ($prog.Length -gt 90) { $prog = $prog.Substring(0, 90) + "..." }
    $status = if ($alive) { "RUN" } else { "END" }
    $main = if ($prog) { $prog } else { $last }
    Write-Host ("{0}  {1,-4}  {2,8} MB/s  {3,6} GB | {4}" -f (Get-Date -Format "HH:mm:ss"), $status, $rate, $size, $main)
    if ($stage) { Write-Host ("      stage: {0}" -f $stage) }
    if (-not $alive) {
        Write-Host ""
        Write-Host "=== process ENDED - check the log tail for the Result list ==="
        break
    }
    Start-Sleep 20
}
