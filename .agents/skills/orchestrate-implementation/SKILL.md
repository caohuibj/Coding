---
name: orchestrate-implementation
description: Route coding work between the Luna fast lane and the Sol-managed multi-agent lane, schedule Task DAG nodes, compile worker context, and enforce concurrency, worktree, and escalation rules.
---

# Orchestrate Implementation

Read:
- `references/task-lifecycle.md`
- `references/concurrency-and-worktrees.md`
- `references/context-compilation.md`

## Route before designing

Classify complexity and risk.

### Fast lane

Use `luna_fast` when objective/scope are clear, an existing repository pattern can be followed, no new system-level architecture decision is needed, no unresolved dependency graph is needed, the work is one coherent change, and risk is not critical.

Do not spend Sol tokens producing a full design or Task DAG for fast-lane work. Give `luna_fast` the user objective, known constraints/non-goals, and relevant repository location if known. Let it inspect, make local design choices, implement, validate, and return `READY_FOR_REVIEW`. Sol performs the final review.

### Managed lane

Use when work is ambiguous, cross-module, architecture-sensitive, dependency-heavy, meaningfully parallel, high/critical risk, or no longer bounded.

Run `feature-design -> implementation-planning -> DAG scheduling -> worker review -> integration verification`.

## Schedule the DAG

A task becomes `READY` only when all dependencies are `DONE`, produced interfaces it consumes are stable, and its write scope does not collide with another running writer.

Default to one writer. Spawn additional writers only when the DAG exposes truly independent ready work. Never create work merely to fill available agent slots.

## Context compilation

The lead is a context compiler, not a context forwarder. For each worker, provide only its Task Brief, applicable repository instructions, relevant interfaces, repository evidence, and necessary code context. Do not copy the full conversation, full feature plan, unrelated worker logs, or large exploration output into every worker.

## Agent caps

- writer agents (`luna_fast` or `luna_worker`): at most 3 concurrent;
- `luna_explorer`: at most 4 concurrent;
- global repository config allows up to 7 spawned threads.

## Escalation

A writer gets one evidence-based focused repair after a validation failure. If revalidation fails, route the blocker to Sol High. Sol decides whether to clarify the brief and spawn a fresh Luna, repair the plan, change architecture, or take over the difficult implementation.

Escalation transfers reasoning authority; it does not automatically mean Sol must write the code.

## Completion

Worker output is never final. It enters `READY_FOR_REVIEW`. Only the Sol lead can move work to `DONE` after review and fresh evidence.
