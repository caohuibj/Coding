# Coding Agent Team

A repository-scoped Codex workflow for building software with one strong Sol lead and ephemeral Luna execution agents.

## Operating model

- **Lead:** GPT-5.6 Sol, `high`
- **Fast lane:** GPT-5.6 Luna, `max` for low-complexity low/medium-risk work; high-risk requires explicit Sol admission
- **Managed workers:** GPT-5.6 Luna, `xhigh`, fresh worker per Task Brief, up to 3 writers by policy
- **Explorers:** GPT-5.6 Luna, `high`, read-only, fresh per investigation, up to 4 by policy
- **Normal review:** Sol, `high`
- **Critical review:** Sol, `xhigh`
- **Sol `max`:** intentionally not used in V1
- **Hard subagent cap:** 4 spawned threads total

The workflow combines Superpowers-style engineering discipline with Codex subagents while keeping roles narrow and project-scoped.

## Routing

### Fast lane

Use directly for low-complexity, bounded low/medium-risk work that follows existing patterns and needs no system-level architecture decision. Low-complexity high-risk work needs Sol High admission. Critical risk never uses the fast lane.

`request -> risk/complexity gate -> luna_fast -> implementation + validation -> Sol review -> done`

### Managed lane

Use for medium/high complexity, ambiguity, cross-module/architecture work, dependency-heavy work, meaningful parallelism, high-risk work not admitted to fast lane, or any critical risk.

`request -> Sol design -> exploration -> task DAG -> fresh Luna workers -> Sol review -> integration verification -> done`

## Core rules

1. **Minimum sufficient design.** Implement the simplest complete solution that satisfies current requirements.
2. **Defend at boundaries.** Validate untrusted inputs and external boundaries; trust already-validated internal invariants.
3. **Reuse before inventing.** Reuse existing abstractions aggressively; create new abstractions conservatively.
4. **No speculative future-proofing.** Complexity must serve a current requirement.
5. **Evidence before completion.** Workers may report `READY_FOR_REVIEW`; only Sol may mark work `DONE`.
6. **One repair attempt.** After failed validation, Luna gets one evidence-based focused repair; another failure escalates to Sol.
7. **Fresh execution contexts.** One Task Brief uses one fresh worker; investigations use fresh explorers.
8. **Parallelize only independent work.** Concurrent writers require stable interfaces, non-overlapping write scope, and isolated worktrees; otherwise serialize.
9. **Verification is proportional.** Run checks relevant to changed behavior and risk, not ceremony.

## Repository layout

```text
AGENTS.md
.codex/
  config.toml
  agents/
    luna-fast.toml
    luna-worker.toml
    luna-explorer.toml
    critical-reviewer.toml
.agents/
  skills/
    feature-design/
    implementation-planning/
    orchestrate-implementation/
    bounded-implementation/
    systematic-debugging/
    verification-gate/
    code-review/
docs/
  agent/
    architecture.md
```

All configuration is repository-scoped. Nothing in this project requires changes under `~/.codex` or `$HOME/.agents`.

See `docs/agent/architecture.md` for the full workflow.
