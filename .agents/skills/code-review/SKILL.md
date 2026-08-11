---
name: code-review
description: Review completed coding tasks for spec compliance, correctness, risk, tests, and unnecessary complexity. Use Sol High normally and the Sol XHigh critical reviewer for critical-risk changes.
---

# Code Review

For critical-risk changes, also read `references/critical-review.md`.

## Pass 1: Requirement and scope compliance

Check every acceptance criterion, missing behavior, extra behavior not requested, interface compatibility, and write-scope/non-goal violations.

## Pass 2: Engineering correctness

Prioritize behavioral correctness, error paths/state transitions, regressions, data integrity, security/trust boundaries, missing meaningful tests, and consistency with repository architecture.

## Pass 3: Simplicity

Ask whether each new abstraction serves a current requirement or semantic boundary; validation is duplicated after a trusted boundary; error handling preserves failures; wrappers/helpers add meaning; dependencies/configuration/layers are necessary; unrelated code was refactored; or materially less machinery could provide the same correctness and clarity.

Do not optimize for line count. Complexity is acceptable when the requirement actually needs it.

## Findings policy

Report actionable findings only. Rank by severity and include concrete evidence. Avoid style-only comments unless they hide a bug or meaningful maintenance risk.

## Routing

- low/medium/high risk: Sol High;
- critical risk: `critical_reviewer`, Sol XHigh;
- no V1 code-review path uses Sol Max.
