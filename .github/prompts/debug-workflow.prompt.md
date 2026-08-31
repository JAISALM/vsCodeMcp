# Debug Workflow

First, read:

- AGENTS.md
- project-memory/PROJECT_STATE.md
- project-memory/WORKFLOW_HISTORY.md (current and previous versions)

Then inspect the failing workflow using @comfy-mcp.

Diagnosis rules:

1. Do not replace or modify the known-good saved version.
2. Find the root cause before changing anything (node parameters, model files, resolutions, sampler settings).
3. Never invent node names or parameters — verify them with @comfy-mcp.
4. Propose the smallest fix; apply it to a copy, not the baseline.
5. Test the fix.
6. Record the diagnosis and outcome in project-memory/WORKFLOW_HISTORY.md.

Report: root cause, fix applied, test result, and a keep/revert recommendation.
