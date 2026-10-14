param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$ws = "D:\models\vsCodeMcp"
$noBom = New-Object System.Text.UTF8Encoding($false)
$cp1252 = [System.Text.Encoding]::GetEncoding(1252)
$cp437 = [System.Text.Encoding]::GetEncoding(437)
$wl = New-Object System.Collections.Generic.HashSet[char]
foreach ($c in @([char]0x2013,[char]0x2014,[char]0x2018,[char]0x2019,[char]0x201C,[char]0x201D,[char]0x2022,[char]0x2026,[char]0x2190,[char]0x2192,[char]0x2194,[char]0x2264,[char]0x2265,[char]0x2248,[char]0x00D7,[char]0x00B0,[char]0x00B7,[char]0x00A7,[char]0x00B2,[char]0x26A0,[char]0x2705,[char]0x2714,[char]0x2716,[char]0x274C,[char]0x2605,[char]0x2B50,[char]0x23F3,[char]0x00E9,[char]0x00E8,[char]0x00F1,[char]0x00FC,[char]0xFFFD)) { [void]$wl.Add($c) }

function Test-Wl([string]$s) {
  foreach ($ch in $s.ToCharArray()) {
    $code = [int]$ch
    if ($code -lt 0x80) { continue }
    if ($code -ge 0x0D00 -and $code -le 0x0D7F) { continue }
    if (-not $wl.Contains($ch)) { return $false }
  }
  return $true
}
function Try-Decode([string]$run, [System.Text.Encoding]$enc) {
  try {
    $bytes = $enc.GetBytes($run)
    $decoded = [System.Text.Encoding]::UTF8.GetString($bytes)
    if ((Test-Wl $decoded) -and ($decoded -notmatch '[\u00C2-\u00C3\u00E0\u00E2\u0393]')) { return $decoded }
    return $null
  } catch { return $null }
}

$targets = @("data\recovered\06782206_CURRENT_TASK.txt", "data\recovered\c84b8517_DECISIONS.txt", "data\recovered\turn8_CURRENT_TASK.md.txt", "data\seedvr_cli_help.txt", "data\tauri_tail.txt", "data\vs_check.txt")
foreach ($rel in $targets) {
  $p = Join-Path $ws $rel
  $text = [System.IO.File]::ReadAllText($p, [System.Text.Encoding]::UTF8)
  $runs = [regex]::Matches($text, '[^\x00-\x7F]+')
  $runMap = @{}
  foreach ($r in $runs) {
    $v = $r.Value
    if ($v -match '[\u00C2-\u00C3\u00E0\u00E2\u0393]') {
      if ($runMap.ContainsKey($v)) { $runMap[$v] = [int]$runMap[$v] + 1 } else { $runMap[$v] = 1 }
    }
  }
  $fixed = 0; $unmapped = @()
  $newText = $text
  foreach ($v in ($runMap.Keys | Sort-Object { $_.Length } -Descending)) {
    $d = Try-Decode $v $cp1252
    if ($null -eq $d) { $d = Try-Decode $v $cp437 }
    if ($null -eq $d) { $unmapped += ("{0} x{1}" -f $v.Substring(0, [Math]::Min(20, $v.Length)), $runMap[$v]); continue }
    $newText = $newText.Replace($v, $d)
    $fixed += [int]$runMap[$v]
  }
  $left = 0
  foreach ($ch in $newText.ToCharArray()) { $c = [int]$ch; if ($c -eq 0x00E2 -or $c -eq 0x00C3 -or $c -eq 0x00C2 -or $c -eq 0x0393) { $left++ } }
  $status = if ($Apply) {
    if ($unmapped.Count -eq 0) {
      [System.IO.File]::WriteAllText($p, $newText, $noBom)
      "WRITTEN (remaining mojibake chars: {0})" -f $left
    } else { "PARTIAL - unmapped runs kept as-is: {0}" -f ($unmapped | Select-Object -Unique) }
  } else {
    "DRY-RUN (would fix {0}, unmapped: {1})" -f $fixed, $unmapped.Count
  }
  Write-Output ("{0}: {1}" -f $rel, $status)
  if ($Apply -and $unmapped.Count -gt 0) { Write-Output ("   unmapped: " + (($unmapped | Select-Object -Unique) -join ' | ')) }
}
