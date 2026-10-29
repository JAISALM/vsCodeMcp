# swap_llama_build.ps1 — in-place llama.cpp upgrade (D205 pattern, 2026-10-29)
#
# Replaces D:\llama with a new prebuilt build folder (same binary names, same
# path) so NO config files / bats / DSH providers change. Same pattern as the
# 2026-10-13 b9616 release.
#
# Usage (from a NORMAL session — the running 8100 agent server is STOPPED by
# this script, which briefly disconnects any DSH session on it; the session
# auto-reconnects when the server is back):
#   powershell -ExecutionPolicy Bypass -File "D:\models\vsCodeMcp\utilities\swap_llama_build.ps1" -NewBuildDir "D:\llama-b11960-bin-win-cuda-13.4-x64"
#
# Steps: verify new build -> stop 8100 (+ other llama-servers, listed) ->
# back up D:\llama -> move new files in -> restart 8100 via the user's bat ->
# poll health. Old build stays at D:\llama_bkp_<tag>_<date> (reversible).
param(
    [string]$NewBuildDir = "D:\llama-b11960-bin-win-cuda-13.4-x64",
    [string]$BackupTag = "b11960"
)
$ErrorActionPreference = "Stop"
$llamaDir = "D:\llama"
$bat8100  = "D:\models\qwen\start_qwen_8100.bat"

Write-Host "== 1) verify new build =="
$exe = Join-Path $NewBuildDir "llama-server.exe"
if (-not (Test-Path $exe)) {
    # zip may have extracted into a nested folder
    $nested = Get-ChildItem $NewBuildDir -Recurse -Filter "llama-server.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $nested) { throw "llama-server.exe not found under $NewBuildDir — extract the zip first" }
    $NewBuildDir = $nested.DirectoryName
    $exe = $nested.FullName
}
Write-Host "new build dir: $NewBuildDir"
& $exe --version

Write-Host "== 2) stop running llama-server processes =="
$procs = Get-CimInstance Win32_Process -Filter "Name like 'llama%server%'"
if ($procs) {
    $procs | ForEach-Object {
        Write-Host ("stopping PID {0}: {1}" -f $_.ProcessId, ($_.CommandLine.Substring(0, [Math]::Min(160, $_.CommandLine.Length))))
        Stop-Process -Id $_.ProcessId -Force
    }
    Start-Sleep -Seconds 4
} else {
    Write-Host "(no llama-server running)"
}

Write-Host "== 3) back up current D:\llama =="
$date = Get-Date -Format "yyyyMMdd"
$bak = "D:\llama_bkp_$BackupTag_$date"
$n = 1
while (Test-Path $bak) { $bak = "D:\llama_bkp_$BackupTag_$date_$n"; $n++ }
Rename-Item $llamaDir $bak
Write-Host "old build moved to: $bak"

Write-Host "== 4) move new build into D:\llama =="
# move the CONTENTS of the new build dir into D:\llama
Get-ChildItem $NewBuildDir | ForEach-Object { Move-Item $_.FullName $llamaDir -Force }
Write-Host ("files now in D:\llama: {0}" -f (Get-ChildItem $llamaDir).Count)
& (Join-Path $llamaDir "llama-server.exe") --version

Write-Host "== 5) restart 8100 via $bat8100 =="
if (-not (Test-Path $bat8100)) { throw "restart bat not found: $bat8100" }
Start-Process -FilePath $bat8100
Write-Host "bat launched — polling health up to 5 min (27B load takes 1-2 min)..."

Write-Host "== 6) health poll =="
$ok = $false
for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 5
    try {
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:8100/v1/models" -TimeoutSec 5
        if ($r) { Write-Host "HEALTHY: 8100 up after $([int]($i*5))s — $($r.data.name)"; $ok = $true; break }
    } catch { }
}
if (-not $ok) {
    Write-Host "!! 8100 not healthy after 5 min — check $bat8100 console window. Old build still at $bak (restore: move it back over D:\llama)."
    exit 1
}
Write-Host "== DONE: D:\llama = $BackupTag build, 8100 healthy, no config files touched. Old build: $bak =="
