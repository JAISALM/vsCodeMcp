# Move ComfyUI batch outputs into the episode1 folder.
# Usage (after a batch run):
#   powershell -File "D:\models\vsCodeMcp\utilities\copy_ep1_outputs.ps1" -Prefix ep1_anchor_ -Dest anchors
#   powershell -File "D:\models\vsCodeMcp\utilities\copy_ep1_outputs.ps1" -Prefix ep1_kit_ -Dest kits
param(
  [Parameter(Mandatory = $true)][string]$Prefix,
  [Parameter(Mandatory = $true)][ValidateSet("anchors", "kits", "special", "identity")][string]$Dest
)
$out = "E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\output"
$dest = "D:\models\vsCodeMcp\episode1\outputs\$Dest"
if (-not (Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
$files = Get-ChildItem $out -File -ErrorAction SilentlyContinue | Where-Object {
  $_.Name -like "$Prefix*" -and ($_.Extension -in ".png", ".jpg", ".jpeg", ".webp")
}
if (-not $files) { Write-Output "NO files matching '$Prefix*' in $out (check the SaveImage prefix)"; exit 0 }
$files | Move-Item -Destination $dest -ErrorAction Stop
Write-Output ("moved " + $files.Count + " file(s) -> " + $dest)
$files | Select-Object -First 5 | ForEach-Object { Write-Output ("  " + $_.Name) }
