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

## GitHub-first delivery

GitHub is the system of record for development. Issues define work, branches contain implementation, pull requests carry review context, and GitHub Actions provides the deterministic quality gate. Local clones are downstream working copies that can be synchronized after changes are merged.

```text
Issue / explicit task
  -> risk + complexity routing
  -> fast lane or managed lane
  -> implementation branch
  -> pull request
  -> GitHub Actions
  -> Sol review
  -> merge
  -> local sync when needed
```

Use the structured issue forms under `.github/ISSUE_TEMPLATE/` and the pull-request template to preserve the handoff contract across GitHub-native work.

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
.github/
  ISSUE_TEMPLATE/
  workflows/
  pull_request_template.md
scripts/
  validate_agent_framework.py
docs/
  agent/
    architecture.md
    github-workflow.md
```

## GitHub Actions

`Agent framework checks` runs on pull requests and pushes to `main`. It validates repository contracts, parses project-scoped Codex TOML configuration, and checks skill frontmatter before changes are merged.

All configuration is repository-scoped. Nothing in this project requires changes under `~/.codex` or `$HOME/.agents`.

See `docs/agent/architecture.md` for the agent architecture and `docs/agent/github-workflow.md` for the GitHub execution workflow.
