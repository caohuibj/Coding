# GitHub-First Development Workflow

## Objective

Use GitHub as the primary development control plane while preserving the repository-scoped Sol/Luna agent architecture. Local clones are optional execution environments, not the source of truth.

## Sources of truth

| Concern | Source of truth |
|---|---|
| Requirement and acceptance criteria | GitHub issue or explicit task |
| Agent behavior | `AGENTS.md`, `.agents/skills/`, `.codex/` |
| Implementation | Feature/fix/agent branch |
| Review context | Pull request |
| Deterministic verification | GitHub Actions |
| Accepted repository state | `main` |

## Intake

Prefer the structured issue forms in `.github/ISSUE_TEMPLATE/` for feature and bug work. The issue should make the outcome, acceptance criteria, complexity, risk, non-goals, and expected validation explicit enough to route the work.

A small explicit task does not require an issue when its scope is already unambiguous, but it should still preserve the same information in the pull request.

## Routing

### Fast lane

Use `luna_fast` when the task is bounded, follows established repository patterns, needs no system-level architecture decision, and is not critical-risk.

Expected flow:

```text
issue/task -> luna_fast -> proportional validation -> READY_FOR_REVIEW -> Sol review
```

### Managed lane

Use the managed lane for ambiguous, cross-module, architecture-sensitive, dependency-heavy, parallel, high-risk, or critical-risk work.

Expected flow:

```text
issue/task
  -> feature-design
  -> implementation-planning
  -> Task DAG
  -> Luna workers
  -> READY_FOR_REVIEW
  -> Sol review / critical review
  -> integration verification
```

## Branches

Create a branch for implementation rather than changing `main` directly. Use concise intent-revealing names such as:

- `agent/<workflow-change>` for agent-system changes;
- `feat/<feature>` for product features;
- `fix/<bug>` for defects;
- `docs/<topic>` for documentation-only work.

Concurrent writers should use independent branches or isolated worktrees when their write scopes do not overlap. Sol owns integration.

## Pull request contract

The pull request is the durable handoff from implementation to verification and review. Record:

- objective and linked issue/task;
- lane used and risk classification;
- changed behavior and relevant files;
- validation commands/results or GitHub Actions evidence;
- assumptions, deviations, and residual risk;
- any reviewer focus areas.

A worker result of `READY_FOR_REVIEW` is not equivalent to completion.

## GitHub Actions quality gate

The initial repository check is `.github/workflows/agent-framework.yml`. It runs `scripts/validate_agent_framework.py` on pull requests and pushes to `main`.

The validator intentionally checks only stable repository contracts in V1:

- required agent architecture files exist;
- project-scoped `.codex` TOML files parse successfully;
- required agent configuration fields are present;
- skill `SKILL.md` files have valid frontmatter names/descriptions;
- core roles/skills remain discoverable.

Application-specific test jobs should be added when executable product code enters the repository. Those tests should remain proportional to the changed behavior and should become required merge checks once stable.

## Review and merge

1. GitHub Actions must provide fresh passing evidence for required deterministic checks.
2. Sol reviews correctness, scope, regression risk, test sufficiency, and unnecessary complexity.
3. Critical-risk work also receives the critical reviewer path.
4. Only after review and required verification pass should the pull request be merged.

Branch protection or repository rulesets can later enforce the check mechanically. Until then, the workflow contract treats green Actions plus review as the merge gate.

## Local synchronization

When a local working copy is needed after GitHub changes are accepted:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
```

Local experimentation should return through a branch and pull request so GitHub remains authoritative.
