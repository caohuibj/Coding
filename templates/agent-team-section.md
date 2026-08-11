<!-- CODING-AGENT-TEAM:START -->
## Coding agent team

Use the repository-scoped Sol/Luna workflow in `.agents/skills/`.

- Lead: GPT-5.6 Sol `high`.
- Fast lane: `luna_fast` (Luna `max`) for low-complexity low/medium-risk work; high-risk requires explicit Sol admission; critical risk is never fast-lane.
- Managed lane: Sol designs/plans; fresh `luna_explorer` agents gather read-only evidence; one fresh `luna_worker` (Luna `xhigh`) executes each bounded Task Brief.
- Review: Sol `high`; critical-risk review uses `critical_reviewer` (Sol `xhigh`). V1 does not use Sol `max`.

Core invariants:
- minimum sufficient design; no speculative future-proofing;
- defend at trust boundaries and trust validated internal invariants;
- Task DAG, bounded Task Briefs, and context compilation for managed work;
- exactly one evidence-based focused repair after worker validation failure, then escalate to Sol;
- workers return `READY_FOR_REVIEW`; only Sol may declare `DONE` after fresh proportional evidence;
- concurrent writers require independent DAG nodes and isolated worktrees; without isolation, serialize;
- spawned-agent hard cap is 4; do not treat the cap as a utilization target.

### Project commands

These commands are installation-time detections. Verify them against the repository's actual tooling and edit this section when the project changes.

{{PROJECT_COMMANDS}}
<!-- CODING-AGENT-TEAM:END -->
