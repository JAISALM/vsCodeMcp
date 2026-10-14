# commit_md.ps1 - vsCodeMcp repo safety standard (2026-10-14)
#
# Commits ALL .md files (project memory, docs, scripts, root) + .gitignore.
# Run manually after significant .md changes, and it is ALSO scheduled to run
# daily at 22:30 as a safety net (Windows task "VsCodeMcp-MdDailyCommit").
#
# Why: sessions can corrupt/nuke files (Gemma incident, 2026-10-14). The git
# commit history is the safety net - if a file is ever nuked again:
#   git log --oneline -- <file>          # find the last good commit
#   git checkout <commit> -- <file>      # restore it
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File "D:\models\vsCodeMcp\utilities\commit_md.ps1"

$ErrorActionPreference = 'Stop'
$repo = "D:\models\vsCodeMcp"
Set-Location $repo

# Stash nothing, add nothing destructive: only .md files + .gitignore.
# Quoted '*.md' so PowerShell does NOT glob-expand it (git matches it at all depths).
git add -- '*.md'
git add -- '.gitignore'

if (git diff --cached --quiet) {
  Write-Output "commit_md: no .md changes to commit (already up to date)."
} else {
  $summary = git diff --cached --stat | Select-Object -Last 1
  $stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
  $msg = "md-safety-commit $stamp - all .md changes (daily standard)"

  git commit -m $msg | Out-Null
  Write-Output "commit_md: committed."
  git log -1 --format="commit_md: %h %s"
  Write-Output ("commit_md: {0}" -f $summary)
}

# Always try to push so the GitHub remote (origin/main) is the true safety net
# (D131). `git push -q` is silent on success; a failed push never fails the
# local commit (the next run retries it).
try {
  $prevEAP = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  $pushOut = (git push -q origin main 2>&1 | Out-String).Trim()
  $ErrorActionPreference = $prevEAP
  if ($LASTEXITCODE -eq 0 -and $pushOut -eq "") {
    Write-Output "commit_md: push OK (origin/main up to date)"
  } else {
    Write-Output ("commit_md: PUSH FAILED - local commits still safe: " + $pushOut)
  }
} catch {
  Write-Output ("commit_md: PUSH ERROR - local commits still safe: " + $_.Exception.Message)
}
