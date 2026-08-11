# Task and Agent Lifecycle

## Task states

- `PLANNED`: defined but dependencies or interfaces are not ready.
- `BLOCKED`: cannot proceed because an explicit dependency or decision is missing.
- `READY`: dependency, interface, and write-scope checks pass.
- `RUNNING`: assigned to a fresh worker.
- `READY_FOR_REVIEW`: worker reports implementation and validation evidence.
- `NEEDS_FIX`: reviewer found a bounded correction that can be delegated as a new focused task/brief.
- `ESCALATED`: worker could not safely complete within its contract.
- `DONE`: Sol review passed and required fresh verification evidence exists.

Only the Sol lead may set `DONE`.

## Fresh agent rule

A managed Task Brief is executed by one fresh `luna_worker`. Once it returns `READY_FOR_REVIEW` or `ESCALATED`, close that worker thread. Do not reuse it for a different Task Brief.

A repository investigation normally uses one fresh `luna_explorer` per question. Close it after the evidence report; a tightly scoped follow-up on the same investigation may reuse the thread when that avoids redundant repository reads.

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

Reviewer findings that require code changes are not an extension of the failed implementation loop. Sol turns accepted findings into a bounded correction brief and delegates it to a fresh worker when appropriate.
