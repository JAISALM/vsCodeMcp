# run_batch_daily.ps1 - Daily 08:00 batch runner (VsCodeMcp-BatchDaily task)
# PS 5.1 compatible: PURE ASCII ONLY (D273 rule).
# Runs each batch job ONE BY ONE, logged, idempotent (present + size OK = skip),
# resume-aware (.part + curl -C -).
#
# Jobs (NETWORK only, no GPU work - D192). Direct curl to the app's model dir
# (NO CLI = no app-lock collision: CLI "models download" fails with
# "Close RGB MoCap..." while the app is open). Specs from mocap/models.py:
#   [pva]           pvanet.pt (3 GB) - Google Drive, anonymous limit fresh at 08:00
#   [rife49]        rife\rife49.pth (21 MB) - HuggingFace
#   [sam31_people]  sam31\sam3.1_multiplex_fp16.safetensors (1.7 GB) - HuggingFace
# Log: D:\models\vsCodeMcp\batch_logs\batch_<stamp>.log

$modelsDir = "D:\RGBMoCapInstaller\toyxyz_RGBMocap\models"
$proxyPy = "D:\models\vsCodeMcp\utilities\ipv4_proxy.py"
$proxyExe = "C:\Program Files\Python310\python.exe"
$py = "C:\Program Files\Python310\python.exe"
$logdir = "D:\models\vsCodeMcp\batch_logs"
if (-not (Test-Path $logdir)) { New-Item -ItemType Directory -Path $logdir | Out-Null }
$stamp = Get-Date -Format "yyyyMMdd_HHmm"
$log = Join-Path $logdir ("batch_{0}.log" -f $stamp)

function Log([string]$m) {
  $line = ((Get-Date -Format "HH:mm:ss") + " " + $m)
  Add-Content -Path $log -Value $line -Encoding ASCII
  Write-Host $line
}

function Get-Sha256([string]$file) {
  return & $py -c "import hashlib,sys;h=hashlib.sha256();f=open(sys.argv[1],'rb');d=f.read(1048576);`nwhile d: h.update(d); d=f.read(1048576)`nprint(h.hexdigest())" $file 2>&1 | Out-String
}

$jobs = @(
  @{ key = "pva"; target = "pvanet.pt"; kind = "drive"; id = "1dffyj3cdH1Myw2-tzgKTXryaO72Gbys1"; min = 3000000000; sha = "a6e5f95a287a45dc1e4944fe7381e7d0c5fe02d4009c5794b09717077a4e1a26" },
  @{ key = "rife49"; target = "rife\rife49.pth"; kind = "hf"; url = "https://huggingface.co/Isi99999/Frame_Interpolation_Models/resolve/bfbc870b7155e71d1ec2255f8dd800d065650e3d/rife49.pth"; min = 21345274; sha = "e55fd00f3cc184e3c65961f4bb827a9da022e78eed36b055242c0ac30000d533" },
  @{ key = "sam31_people"; target = "sam31\sam3.1_multiplex_fp16.safetensors"; kind = "hf"; url = "https://huggingface.co/Comfy-Org/sam3.1/resolve/5febd4769e8802cdfdb75e1f733abd8c68434a85/checkpoints/sam3.1_multiplex_fp16.safetensors"; min = 1745546848; sha = "9ba99c92703c2e8b4f47de2d34a539bb8e18923049e238b780d70dbe6368eb03" }
)

Log "=== BATCH DAILY START (log: $log) modelsDir: $modelsDir"

# --- Job 0: IPv4 proxy prereq (D273) ---
$proxyUp = (Get-NetTCPConnection -LocalPort 8888 -State Listen -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
if ($proxyUp) {
  Log "[proxy] already up (port 8888)"
} else {
  Start-Process -WindowStyle Hidden -FilePath $proxyExe -ArgumentList "`"$proxyPy`""
  Start-Sleep -Seconds 6
  $proxyUp = (Get-NetTCPConnection -LocalPort 8888 -State Listen -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
  Log ("[proxy] launched -> up={0}" -f $proxyUp)
}
if ($proxyUp) {
  $env:HTTP_PROXY = "http://127.0.0.1:8888"
  $env:HTTPS_PROXY = "http://127.0.0.1:8888"
  $env:NO_PROXY = "localhost,127.0.0.1,::1"
  Log "[proxy] env vars set (D273 IPv4-forcing)"
}

# --- Download jobs, one by one (failure of one does not stop the rest) ---
foreach ($job in $jobs) {
  $key = $job.key
  $target = Join-Path $modelsDir $job.target
  $part = $target + ".part"
  $parent = Split-Path $target -Parent
  if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }

  if ((Test-Path $target) -and ((Get-Item $target).Length -ge $job.min)) {
    Log ("[{0}] already present ({1} MB) - skip" -f $key, [Math]::Round((Get-Item $target).Length / 1MB))
    continue
  }

  Log ("[{0}] missing/undersized -> downloading (proxy up={1})..." -f $key, $proxyUp)
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $resume = @()
  if (Test-Path $part) {
    $partSize = (Get-Item $part).Length
    if ($partSize -lt 1048576) {
      # sub-1MB .part = leftover HTML error page (quota/confirm), not real data
      Remove-Item $part -Force
      Log ("[{0}] discarded sub-1MB .part (HTML error page, not data)" -f $key)
    } else {
      $resume = @("-C", "-")
      Log ("[{0}] resuming .part ({1} MB so far)" -f $key, [Math]::Round($partSize / 1MB))
    }
  }

  if ($job.kind -eq "drive") {
    $probe = Join-Path $env:TEMP ("batch_probe_{0}.html" -f $key)
    $cookies = Join-Path $env:TEMP ("batch_cookies_{0}.txt" -f $key)
    $driveUrl = "https://drive.google.com/uc?export=download&id=" + $job.id
    & curl.exe -4 -s -L -c $cookies $driveUrl -o $probe
    $probeSize = 0
    if (Test-Path $probe) { $probeSize = (Get-Item $probe).Length }
    if ($probeSize -lt 10485760) {
      # HTML confirm / virus-warning page (large file) - extract token + form action
      $text = Get-Content $probe -Raw
      $action = "https://drive.usercontent.google.com/download"
      if ($text -match 'action="([^"]+)"') { $action = $matches[1] }
      $uuidTok = $null
      $confTok = $null
      if ($text -match 'name="uuid" value="([\w-]+)"') { $uuidTok = $matches[1] }
      elseif ($text -match 'uuid=([\w-]+)') { $uuidTok = $matches[1] }
      if ($text -match 'name="confirm" value="([^"]+)"') { $confTok = $matches[1] }
      elseif ($text -match 'confirm=([^"&\s]+)') { $confTok = $matches[1] }
      if (-not ($uuidTok -or $confTok)) {
        Log ("[{0}] DRIVE: no confirm/uuid token in probe page ({1} bytes) - manual import needed" -f $key, $probeSize)
        continue
      }
      $dlUrl = $action + "?id=" + $job.id + "&export=download"
      if ($confTok) { $dlUrl += "&confirm=" + [uri]::EscapeDataString($confTok) }
      if ($uuidTok) { $dlUrl += "&uuid=" + $uuidTok }
      Log ("[{0}] DRIVE: token found (uuid={1} confirm={2})" -f $key, $uuidTok, $confTok)
      & curl.exe -4 -L -b $cookies $dlUrl -o $part @resume
    } else {
      # probe IS the file (small direct response)
      Move-Item $probe $part -Force
    }
  } else {
    & curl.exe -4 -L $job.url -o $part @resume
  }
  $curlCode = $LASTEXITCODE
  $sw.Stop()
  Log ("[{0}] curl exit={1} in {2:N0}s (part {3} MB)" -f $key, $curlCode, $sw.Elapsed.TotalSeconds, [Math]::Round((Get-Item $part -ErrorAction SilentlyContinue).Length / 1MB))

  if ($curlCode -ne 0) { Log ("[{0}] CURL FAILED (exit {1}) - will resume next run" -f $key, $curlCode); continue }
  $partNow = $null
  if (Test-Path $part) { $partNow = (Get-Item $part).Length }
  if ($partNow -eq $null -or $partNow -lt $job.min) {
    # small .part may be a Drive quota/HTML error page - detect and log it clearly
    $quota = $false
    if ($partNow -ne $null -and $partNow -lt 10485760) {
      $head = Get-Content $part -TotalCount 5 -ErrorAction SilentlyContinue
      if (($head -join " ") -match "Quota exceeded|Too many users") { $quota = $true; Remove-Item $part -Force }
    }
    if ($quota) {
      Log ("[{0}] DRIVE QUOTA EXCEEDED (per-file popularity limit, up to 24h) - auto-retry next run" -f $key)
    } else {
      Log ("[{0}] size check failed (part {1} MB < min {2} MB) - resume next run" -f $key, [Math]::Round(($partNow / 1MB)), [Math]::Round($job.min / 1MB))
    }
    continue
  }
  $actual = (Get-Sha256 $part).Trim()
  if ($actual -eq $job.sha) {
    Move-Item $part $target -Force
    Log ("[{0}] SHA256 OK -> moved to {1} ({2} MB) - DONE" -f $key, $target, [Math]::Round((Get-Item $target).Length / 1MB))
  } else {
    Log ("[{0}] SHA256 MISMATCH (actual {1}) - keeping .part for inspection, NOT installing" -f $key, $actual)
  }
}

# --- Watch jobs (D228): community watch (daily) + lab watch (Mondays) ---
# Replaces the session reminders (which only fired while a session was active).
# Appends the consolidated DAILY_WATCH.md entry (the 11-25/11-26 miss).
$pyWatch = "E:\comfyUi_latest\ComfyUI_windows_portable\python_embeded\python.exe"
$dw = "D:\models\vsCodeMcp\docs\research_watch\DAILY_WATCH.md"
$today = Get-Date -Format "yyyy-MM-dd"
$isMonday = (Get-Date).DayOfWeek -eq "Monday"
if (Select-String -Path $dw -Pattern ("^## {0} " -f $today) -ErrorAction SilentlyContinue) {
  Log "[watch] DAILY_WATCH.md already has today's entry - skip watches"
} else {
  Log "[watch] community watch (rag\weekly_watch.py)..."
  $sw2 = [Diagnostics.Stopwatch]::StartNew()
  $wout = (& $pyWatch "D:\models\vsCodeMcp\rag\weekly_watch.py" 2>&1 | Out-String)
  $wcode = $LASTEXITCODE
  $sw2.Stop()
  $wsummary = (($wout -split "`n" | Where-Object { $_ -match "reddit \d" } | Select-Object -First 1) -as [string])
  Log ("[watch] community exit={0} in {1:N0}s: {2}" -f $wcode, $sw2.Elapsed.TotalSeconds, $wsummary)
  $lfresh = $null
  if ($isMonday) {
    Log "[labwatch] lab watch (utilities\weekly_lab_diff.py, Mondays only)..."
    $sw3 = [Diagnostics.Stopwatch]::StartNew()
    $lout = (& $pyWatch "D:\models\vsCodeMcp\utilities\weekly_lab_diff.py" 2>&1 | Out-String)
    $lcode = $LASTEXITCODE
    $sw3.Stop()
    $lfresh = (($lout -split "`n" | Where-Object { $_ -match "fresh items:" } | Select-Object -First 1) -as [string])
    Log ("[labwatch] exit={0} in {1:N0}s: {2}" -f $lcode, $sw3.Elapsed.TotalSeconds, $lfresh)
  } else {
    Log "[labwatch] not Monday - skip (runs Mondays only)"
  }
  $entry = "## $today (auto - VsCodeMcp-BatchDaily)`n- community watch: $wsummary (details: rag\news\weekly_watch_$today.md)"
  if ($isMonday) { $entry += "`n- lab watch: $lfresh (details: rag\news\lab_watch_$today.md)" }
  Add-Content -Path $dw -Value $entry -Encoding UTF8
  Log "[watch] DAILY_WATCH.md entry appended for $today"
}

# --- Final status (CLI list is lock-free; wrap in try) ---
try {
  $j = (& "D:\RGBMoCapInstaller\toyxyz_RGBMocap\RGBMoCapCLI.cmd" models list --json 2>&1 | Out-String | ConvertFrom-Json)
  foreach ($job in $jobs) {
    $r = [bool]($j.models | Where-Object { $_.key -eq $job.key } | Select-Object -ExpandProperty ready)
    Log ("[final] {0} ready={1}" -f $job.key, $r)
  }
} catch { Log "[final] could not read model list (app lock?)" }
Log "=== BATCH DAILY END ==="
