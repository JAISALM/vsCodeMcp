# watch_progress.ps1 — STANDING download/progress monitor (the reusable "fire")
# Watches ANY folder + log: engine progress line (primary), folder GB (secondary), rate, stage.
# Usage:  powershell -ExecutionPolicy Bypass -File utilities\watch_progress.ps1 [-Root D:\SomeFolder] [-Log D:\SomeFolder\log.txt] [-Pattern install_rgbmocap|Install_RGBMoCap]
param(
    [string]$Root = "D:\RGBMoCapInstaller",
    [string]$Log = "D:\RGBMoCapInstaller\install_log.txt",
    [string]$Pattern = "install_rgbmocap|Install_RGBMoCap"
)
$prevPGB = $null; $prevTime = $null; $rate = 0.0

function Get-Alive {
    $procs = Get-CimInstance Win32_Process -Filter "Name='cmd.exe' OR Name='python.exe' OR Name='uv.exe' OR Name='curl.exe' OR Name='git.exe'" -ErrorAction SilentlyContinue
    $procs | Where-Object { $_.CommandLine -match $Pattern -and $_.ProcessId -ne $PID } | Select-Object -First 1
}

Write-Host "=== progress: $Root ==="
Write-Host "(engine progress line = primary; folder GB = secondary; 20 s poll; close anytime)"
Write-Host ""

while ($true) {
    $alive = [bool](Get-Alive)
    $last = "no log yet"; $stage = ""; $prog = ""; $pGB = $null
    if (Test-Path $Log) {
        $content = Get-Content $Log
        $last = ($content | Where-Object { $_.Trim() -ne "" } | Select-Object -Last 1).Trim()
        $stage = (($content | Select-String "=== \d+/\d+") | Select-Object -Last 1).Line.Trim()
        $progLine = ($content | Where-Object { $_ -match "\d{1,3}\.\d+%" } | Select-Object -Last 1).Trim()
        if ($progLine) {
            $prog = $progLine
            if ($prog -match "(\d+\.\d+)\s*/\s*(\d+\.\d+)\s*GB") { $pGB = [double]$Matches[1] }
        }
    }
    if ($pGB -ne $null -and $prevPGB -ne $null -and (Get-Date) -gt $prevTime) {
        $dt = ((Get-Date) - $prevTime).TotalSeconds
        if ($dt -gt 5) { $rate = [Math]::Round(($pGB - $prevPGB) * 1024 / $dt, 1) }
    }
    $prevPGB = $pGB; $prevTime = Get-Date
    if ($last.Length -gt 70) { $last = $last.Substring(0, 70) + "..." }
    if ($prog.Length -gt 90) { $prog = $prog.Substring(0, 90) + "..." }
    $status = if ($alive) { "RUN" } else { "END" }
    Write-Host ("{0}  {1,-4}  {2,9} MB/s | {3}" -f (Get-Date -Format "HH:mm:ss"), $status, $rate, $(if ($prog) { $prog } else { $last }))
    if ($stage) { Write-Host ("      stage: {0}" -f $stage) }
    if (-not $alive) {
        Write-Host ""
        Write-Host "=== process ENDED — check log tail ==="
        break
    }
    Start-Sleep 20
}
