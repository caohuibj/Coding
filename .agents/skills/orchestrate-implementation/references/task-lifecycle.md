# Task Lifecycle

Use these states:

- `PLANNED`: defined but dependencies or interfaces are not ready.
- `BLOCKED`: cannot proceed because an explicit dependency or decision is missing.
- `READY`: dependency, interface, and write-scope checks pass.
- `RUNNING`: assigned to a worker.
- `READY_FOR_REVIEW`: worker reports implementation and validation evidence.
- `NEEDS_FIX`: reviewer found a bounded correction that can return to a worker.
- `ESCALATED`: worker could not safely complete within its contract.
- `DONE`: Sol review passed and required fresh verification evidence exists.

Only the Sol lead may set `DONE`.

## Worker failure state machine

```text
IMPLEMENT
  -> VALIDATE
      -> PASS -> READY_FOR_REVIEW
      -> FAIL
          -> collect evidence
          -> one focused repair
          -> REVALIDATE
              -> PASS -> READY_FOR_REVIEW
              -> FAIL -> ESCALATED -> SOL HIGH
```

There is no second Luna repair attempt in V1.
