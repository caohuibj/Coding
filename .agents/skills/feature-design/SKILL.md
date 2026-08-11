---
name: feature-design
description: Design complex, ambiguous, cross-module, or architecture-sensitive features before implementation. Do not use for simple fast-lane tasks that can follow an existing pattern directly.
---

# Feature Design

Use this skill in the managed lane before implementation planning.

## Goal

Produce the minimum sufficient design needed to make implementation tasks bounded and reviewable.

## Process

1. Restate the current user outcome and explicit non-goals.
2. Inspect the existing repository before inventing architecture. Delegate read-only exploration when parallel evidence gathering would reduce main-thread context.
3. Identify existing patterns, interfaces, invariants, and trust boundaries.
4. Resolve material ambiguity. Do not manufacture design questions whose answers do not affect implementation.
5. Consider alternatives only when there is a real tradeoff. Prefer the approach that best fits the repository and current requirements.
6. Define scope/non-goals, required architecture decisions, interfaces and ownership boundaries, important invariants, trust boundaries/error ownership, compatibility concerns, and measurable acceptance criteria.
7. Apply the simplicity contract: no hypothetical extensibility, no new layer without a current reason, no duplicate validation after a trusted boundary, and no fallback that turns a real error into apparent success.
8. Stop when the design is sufficient to create bounded tasks. Do not specify line-by-line implementation.

## Output

A concise Feature Spec containing objective, repository evidence, chosen design and rationale, interfaces/invariants, trust boundaries, scope/non-goals, acceptance criteria, and open risks.

Hand the approved spec to `implementation-planning`.
