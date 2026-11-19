# resync_workflows.ps1 — directory-based mirror (2026-11-19; replaces the 2026-10-25 flat curated list)
#
# Mirrors the reusable movies/ subtree (8 stage folders) from the canonical ComfyUI
# workflows dir into this repo dir. Safe: only touches the mirror, never the canonical.
#
# `special/` (char-specific one-offs / tests / LoRA-training / intro-video-era) is
# intentionally NOT mirrored — one-shot tests and broken attempts are never committed
# (AGENTS.md repo rule).
$src = "E:\comfyUi_latest\ComfyUI_windows_portable\ComfyUI\user\default\workflows\movies"
$dst = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "movies"
robocopy $src $dst /MIR /NJH /NDL /NP /NC /NS | Out-Null
$count = (Get-ChildItem $dst -Recurse -Filter *.json -ErrorAction SilentlyContinue).Count
Write-Output "resync done: $count mirror files under workflows\movies\ (8 stage folders)."
