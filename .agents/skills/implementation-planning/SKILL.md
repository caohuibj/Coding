---
name: implementation-planning
description: Convert an approved managed-lane feature design into a dependency-aware Task DAG and high-quality bounded Task Briefs. Do not use for simple fast-lane work.
---

# Implementation Planning

The plan is the contract between the Sol lead and ephemeral Luna workers.

Read:
- `references/task-brief-schema.md`
- `references/risk-and-complexity.md`

## Build the DAG

Decompose by coherent, independently reviewable changes, not by tiny editing steps.

Each task node must declare task ID, dependencies, read scope, write scope, interfaces consumed/produced, complexity, risk, and status.

A task is eligible for parallel execution only when dependencies are done, interfaces are stable, and write scopes do not collide.

## Write each Task Brief

Use the schema in `references/task-brief-schema.md`.

The brief must give the worker enough context to succeed without forwarding the full feature conversation or entire plan. Include repository evidence and relevant interfaces; omit unrelated history.

## Task Brief quality gate

Do not delegate until all are true:
- objective is unambiguous;
- acceptance criteria are objectively verifiable;
- interfaces are stable enough for implementation;
- dependencies are complete;
- write scope is bounded;
- non-goals are explicit;
- repository evidence identifies patterns to follow when available;
- risk and complexity are classified;
- validation is proportional to behavior and risk;
- escalation conditions are explicit;
- the task can be completed without a new system-level architecture decision.

If any item fails, refine the design or split/reorder the task.

## Granularity

Prefer one task per coherent reviewable change. Avoid microscopic editing steps and broad tasks that still contain unresolved architecture.
