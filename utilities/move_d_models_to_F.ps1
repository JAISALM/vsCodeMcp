# Move 4 unused D:\models folders to F:\ModelArchive, then replace each with a
# directory junction so ALL existing paths (DSH profiles, .bat files, ComfyUI refs)
# keep working. Reversible: delete junction, move folder back.
$ErrorActionPreference = "Continue"
$archive = "F:\ModelArchive"
New-Item -ItemType Directory -Force -Path $archive | Out-Null
$names = @("Writing", "ai-movie", "SeedVR2-TensorRT-Studio", "blobs")
foreach ($name in $names) {
    $src = "D:\models\$name"
    $dst = "$archive\$name"
    Write-Output "==============================================="
    Write-Output "=== $name : $src -> $dst"
    if (-not (Test-Path $src)) { Write-Output "SKIP: source missing"; continue }
    if (Test-Path $dst) { Write-Output "SKIP: destination already exists"; continue }
    $t0 = Get-Date
    # /MOVE = copy then delete source. /XJD = never descend into junctions. /R:1 /W:2 = don't hang on locked files.
    robocopy $src $dst /E /MOVE /XJD /NFL /NDL /R:1 /W:2 /NP /LOG:"$archive\robocopy_$name.log"
    $rc = $LASTEXITCODE
    Write-Output "robocopy exit code: $rc (0-7 = OK, 8+ = errors; see log)"
    $elapsed = (Get-Date) - $t0
    Write-Output "elapsed: $([math]::Round($elapsed.TotalMinutes,1)) min"
    # remove source if fully moved (robocopy /MOVE leaves empty tree sometimes)
    if (Test-Path $src) {
        $left = @(Get-ChildItem $src -Recurse -File -Force -ErrorAction SilentlyContinue)
        if ($left.Count -eq 0) {
            Remove-Item $src -Force -Recurse -ErrorAction SilentlyContinue
            Write-Output "source tree removed"
        } else {
            Write-Output "WARNING: $left.Count files still in source (locked?) - NOT creating junction"
            continue
        }
    }
    # create the junction
    cmd /c mklink /J "$src" "$dst" | Out-Null
    if (Test-Path $src) {
        $spot = Get-ChildItem $src -Force -ErrorAction SilentlyContinue | Select-Object -First 1
        Write-Output "JUNCTION OK: $src -> $dst  (spot check: $($spot.Name))"
    } else {
        Write-Output "ERROR: junction not visible"
    }
}
Write-Output "=== ALL DONE ==="
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='D:'" | ForEach-Object { Write-Output ("D: free now: {0:N0} GB" -f ($_.FreeSpace/1GB)) }
