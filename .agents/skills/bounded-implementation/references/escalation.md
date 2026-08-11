# Escalation Contract

## One repair rule

The initial implementation may fail validation. That is not an immediate escalation.

Before the single allowed repair, record the observed failure, expected behavior, relevant code path/evidence, root-cause hypothesis, and smallest correction that tests the hypothesis.

Make the focused repair and revalidate.

If revalidation still fails, do not make a second repair attempt. Return `BLOCKED` / `ESCALATED`.

## Escalate immediately when

- an architecture assumption is false;
- a required interface cannot satisfy the task;
- success requires crossing a non-goal or materially expanding write scope;
- the task requires an unrelated subsystem change;
- security/authorization/migration semantics are unclear;
- requirements contradict actual repository behavior;
- a critical-risk decision was not already owned by Sol;
- the problem is no longer bounded.

## Blocked report

Return `OBSERVED`, `EXPECTED`, `EVIDENCE`, `ROOT-CAUSE HYPOTHESIS`, `WHY THE CURRENT CONTRACT IS INSUFFICIENT`, and `DECISION REQUIRED`.

The lead may clarify the task for a fresh Luna worker, change the plan/architecture, or take over.
