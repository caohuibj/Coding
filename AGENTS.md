# Repository Agent Instructions

## Purpose

Use a repository-scoped Sol-led, Luna-executed workflow. Keep the primary reasoning authority with Sol and delegate bounded execution to ephemeral Luna agents.

## Roles and routing

- Primary lead: GPT-5.6 Sol at `high`.
- Fast lane: `luna_fast` (Luna `max`) for low-complexity, bounded low/medium-risk work that follows established patterns. Low-complexity high-risk work requires an explicit Sol admission decision. Critical risk never uses the fast lane.
- Managed lane: Sol designs/plans; `luna_explorer` gathers read-only evidence; `luna_worker` implements bounded Task Briefs.
- Normal review: Sol `high`.
- Critical-risk review: `critical_reviewer` using Sol `xhigh`.
- V1 does not route work to Sol `max`.

## Authority and engineering principles

Sol owns product/architecture decisions, task decomposition, integration, review, escalation, and `DONE` status. Luna workers may make local implementation choices inside their delegated contract but must not redesign system architecture.

Implement the **minimum sufficient design**. Reuse existing repository patterns and abstractions before creating new ones. Create new abstraction only for a current requirement, real variation point, policy boundary, or meaningful repeated concept. Do not future-proof speculatively.

**Defend at trust boundaries; trust validated internal invariants.** Avoid redundant validation, broad error catches, silent success-shaped fallbacks, trivial wrappers, unnecessary dependencies/configuration, unrelated refactors, and comments that restate code.

## Workflow invariants

- Managed work uses a Task DAG and quality-gated bounded Task Briefs.
- Sol compiles task-local context rather than forwarding full conversations/plans.
- One Task Brief uses one fresh `luna_worker`; close it after `READY_FOR_REVIEW` or `ESCALATED`.
- One exploration question uses a fresh `luna_explorer`; close it after evidence is returned unless a tightly scoped follow-up is required.
- A Luna validation failure permits exactly one evidence-based focused repair. A second failure escalates to Sol.
- Workers return `READY_FOR_REVIEW`, never `DONE`. Sol marks `DONE` only after review and fresh proportional verification.
- Implementation parallelism is conservative. If two or more writers run concurrently, each must use an isolated worktree. If isolation is unavailable, serialize writers.
- Global spawned-agent hard cap is 4; workflow policy still limits writers to 3 and explorers to 4.

Detailed routing, risk, verification, worktree, and task-state rules live in `.agents/skills/` and their `references/` files; do not duplicate them here.

## Project commands

This repository currently contains the workflow scaffold rather than an application. When application code is added, record canonical build, test, lint, typecheck, and integration commands here or in the nearest nested `AGENTS.md`. Do not invent commands the repository does not define.
