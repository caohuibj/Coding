# Coding Agent Team

A repository-scoped Codex workflow for building software with one strong lead model and multiple low-cost execution agents.

## Operating model

- **Lead:** GPT-5.6 Sol, `high`
- **Fast lane:** GPT-5.6 Luna, `max` for simple, bounded, non-critical tasks
- **Managed workers:** GPT-5.6 Luna, `xhigh`, up to 3 concurrent writers
- **Explorers:** GPT-5.6 Luna, `high`, read-only, up to 4 concurrent investigators
- **Normal review:** Sol, `high`
- **Critical review:** Sol, `xhigh`
- **Sol `max`:** intentionally not used in V1

The workflow combines Superpowers-style engineering discipline with Codex subagents, while keeping agent roles narrow and project-scoped.

## Routing

### Fast lane

Use when the task is clear, bounded, follows existing patterns, has no architecture decision, and is not critical-risk.

`request -> luna_fast -> implementation + validation -> Sol review -> done`

### Managed lane

Use when the task is ambiguous, cross-module, architecture-sensitive, dependency-heavy, parallelizable, or high/critical risk.

`request -> Sol design -> exploration -> task DAG -> Luna workers -> Sol review -> integration verification -> done`

## Core rules

1. **Minimum sufficient design.** Implement the simplest complete solution that satisfies current requirements.
2. **Defend at boundaries.** Validate untrusted inputs and external boundaries; trust already-validated internal invariants.
3. **Reuse before inventing.** Reuse existing abstractions aggressively; create new abstractions conservatively.
4. **No speculative future-proofing.** Complexity must serve a current requirement.
5. **Evidence before completion.** A worker may report `READY_FOR_REVIEW`; only the lead may mark work `DONE`.
6. **One repair attempt.** After a failed validation, Luna gets one evidence-based focused repair. A second failure escalates to Sol.
7. **Parallelize only independent work.** Concurrent writers require stable interfaces and isolated write scopes.
8. **Verification is proportional.** Run the checks relevant to the changed behavior and risk; do not run ceremony for its own sake.

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
