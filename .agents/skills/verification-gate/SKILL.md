---
name: verification-gate
description: Require fresh, proportional evidence before a coding task or feature is considered complete. Use after implementation, review fixes, and integration; do not equate a worker's success claim with DONE.
---

# Verification Gate

Read `references/verification-policy.md`.

## Core rule

**Evidence before claims.**

- Code written is not completion.
- Tests written are not completion.
- A worker saying "tests pass" is not sufficient evidence for the lead.
- `READY_FOR_REVIEW` is not `DONE`.

## Worker gate

The worker runs the validation specified by the task or selects the smallest sufficient checks in fast-lane work. Report each meaningful command/check and its exact result.

## Review gate

The Sol lead inspects the diff, task objective/brief, validation evidence, scope/non-goal compliance, simplicity, and correctness. Re-run important checks when risk, uncertainty, or integration context warrants independent evidence.

## Integration gate

After a feature or dependent task wave is integrated, run the relevant broader checks needed to prove the combined behavior.

Only after required review and fresh verification passes may Sol set `DONE`.
