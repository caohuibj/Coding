# Task Brief Schema

Use this structure for managed-lane Luna workers.

```text
TASK ID

OBJECTIVE
What concrete outcome must be produced.

RATIONALE
Why this change exists.

COMPLEXITY
low | medium | high

RISK
low | medium | high | critical

COMPLEXITY BUDGET
minimal | standard | justified-complex

SCOPE
Subsystems/files conceptually in scope.

READ SCOPE
Where the worker may inspect for context.

WRITE SCOPE
Where the worker is allowed to modify.

DEPENDENCIES
Task IDs, interfaces, or behavior that must already exist.

INPUT CONTRACTS
Stable interfaces/data/behavior the worker may rely on.

OUTPUT CONTRACTS
Interfaces/data/behavior this task must produce.

REPOSITORY EVIDENCE
Existing files, symbols, patterns, tests, or conventions to follow.

REQUIREMENTS
Behavior that must be implemented.

NON-GOALS
Explicitly excluded changes or redesigns.

ACCEPTANCE CRITERIA
Observable conditions that make the task reviewable as successful.

VALIDATION
The smallest sufficient command/check set to establish the changed behavior.

ESCALATE IF
Conditions that invalidate the brief or require a system-level decision.

RETURN CONTRACT
Changed files, implementation summary, validation evidence, assumptions, risks, blockers.
```

## Complexity budget meanings

- `minimal`: direct implementation; no new architecture layer or dependency unless unavoidable.
- `standard`: fit existing architecture; introduce an abstraction only for a current requirement or clear semantic boundary.
- `justified-complex`: additional architecture is explicitly approved because current requirements demand it.

The complexity budget never relaxes correctness.
