---
name: bounded-implementation
description: Implement a simple fast-lane change or a managed Task Brief with minimum sufficient design, strict scope control, proportional tests, and one evidence-based repair before escalation.
---

# Bounded Implementation

Read `references/escalation.md`.

## Shared implementation contract

Implement the simplest complete solution that satisfies the current task and fits the repository.

Prefer existing patterns and abstractions, direct code with explicit behavior, strong types and clear ownership, small coherent patches, and tests for observable behavior/invariants/regressions/trust boundaries.

Avoid unless justified by the current task: speculative future-proofing, new architectural layers, redundant validation, broad catches or silent fallbacks, trivial wrappers, one-use helpers without semantic meaning, unnecessary configuration/dependencies, unrelated cleanup, and comments that restate code.

Defend at external/untrusted boundaries. Once a boundary has validated an invariant, internal code should rely on the resulting trusted contract instead of repeating the same defense.

## Fast-lane mode

When running as `luna_fast`:
1. inspect relevant existing code;
2. choose a minimal local design;
3. implement the task;
4. run proportional validation;
5. self-check scope and simplicity;
6. return `READY_FOR_REVIEW`.

If the task reveals architecture ambiguity, critical risk, cross-module instability, or a need to expand scope materially, stop and escalate rather than redesigning the system.

## Managed-worker mode

When running as `luna_worker`, the Task Brief is authoritative. Stay within its write scope and non-goals, consume/produce declared interfaces, and escalate when the brief is invalidated.

## Failure

After a validation failure, use one evidence-based focused repair only. If revalidation fails, stop.
