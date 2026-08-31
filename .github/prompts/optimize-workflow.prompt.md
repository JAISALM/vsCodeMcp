# Optimize Workflow

First, read:

- AGENTS.md
- project-memory/PROJECT_STATE.md
- project-memory/DECISIONS.md (relevant entries)
- project-memory/WORKFLOW_HISTORY.md (current workflow)

Then inspect the current workflow using @comfy-mcp.

Optimization rules:

1. Preserve the existing working version (never overwrite the saved baseline).
2. Make the smallest useful change for the stated goal.
3. Do not change parts the user asked to keep (check PROJECT_STATE.md and DECISIONS.md).
4. Save the new version under a new name.
5. Run/test if possible.
6. Compare the result with the baseline.
7. Record the change in project-memory/WORKFLOW_HISTORY.md and, if meaningful, in project-memory/EXPERIMENTS.md.

Report: what changed, why, the result, and a keep/revert recommendation.
