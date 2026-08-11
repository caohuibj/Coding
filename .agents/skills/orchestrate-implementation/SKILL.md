---
name: orchestrate-implementation
description: Route coding work between the Luna fast lane and the Sol-managed multi-agent lane, schedule Task DAG nodes, compile worker context, and enforce lifecycle, concurrency, worktree, and escalation rules.
---

# Orchestrate Implementation

Read:
- `references/task-lifecycle.md`
- `references/concurrency-and-worktrees.md`
- `references/context-compilation.md`
- `../implementation-planning/references/risk-and-complexity.md`

## Route before designing

Classify complexity and risk before choosing a lane.

### Fast lane

Use `luna_fast` directly when **complexity is low** and **risk is low or medium**, provided objective/scope are clear, an existing repository pattern can be followed, no new system-level architecture decision is needed, no unresolved dependency graph is needed, and the work is one coherent change.

For **low-complexity, high-risk** work, Sol High must make an explicit admission decision. Prefer the managed lane whenever invariants, failure modes, external integration, or persistence semantics are non-trivial.

**Critical risk never uses the fast lane.**

Do not spend Sol tokens producing a full design or Task DAG for admitted fast-lane work. Give `luna_fast` the objective, known constraints/non-goals, and relevant repository location if known. It inspects, makes local design choices, implements, validates, and returns `READY_FOR_REVIEW`. Sol performs final review.

### Managed lane

Use when complexity is medium/high; work is ambiguous, cross-module, architecture-sensitive, dependency-heavy, or meaningfully parallel; high-risk work fails fast-lane admission; or risk is critical.

Run `feature-design -> implementation-planning -> DAG scheduling -> worker review -> integration verification`.

## Schedule the DAG

A task becomes `READY` only when all dependencies are `DONE`, produced interfaces it consumes are stable, and its write scope does not collide with another running writer.

Default to one writer. Spawn additional writers only when the DAG exposes truly independent ready work. Never create work merely to fill available agent slots.

## Fresh-agent lifecycle

- One managed Task Brief -> one fresh `luna_worker` thread -> `READY_FOR_REVIEW` or `ESCALATED` -> close the thread.
- Do not reuse a completed writer for another Task Brief.
- One repository investigation question -> one fresh `luna_explorer` thread -> evidence report -> close the thread, except for a tightly scoped follow-up on the same investigation.

Fresh task-local context is part of the correctness and token-efficiency model; persistent project decisions belong with Sol and repository artifacts, not long-lived workers.

## Context compilation

The lead is a context compiler, not a context forwarder. For each worker, provide only its Task Brief, applicable repository instructions, relevant interfaces, repository evidence, and necessary code context. Do not copy the full conversation, full feature plan, unrelated worker logs, or large exploration output into every worker.

## Concurrency caps

- workflow policy: at most 3 concurrent writers;
- workflow policy: at most 4 concurrent explorers;
- repository hard cap: at most 4 spawned-agent threads total.

The hard cap is not a target. Use fewer threads whenever the DAG or investigation does not justify parallelism.

## Escalation

A writer gets one evidence-based focused repair after a validation failure. If revalidation fails, route the blocker to Sol High. Sol decides whether to clarify the brief and spawn a fresh Luna, repair the plan, change architecture, or take over the difficult implementation.

Escalation transfers reasoning authority; it does not automatically mean Sol must write the code.

## Completion

Worker output is never final. It enters `READY_FOR_REVIEW`. Only the Sol lead can move work to `DONE` after review and fresh evidence.
