# Concurrency and Worktree Rules

## Parallelism

Exploration can be relatively aggressive because explorers are read-only. Implementation must be conservative because writers mutate shared state.

A managed task may run concurrently only when every dependency is `DONE`, required interfaces are stable, and write scope does not overlap another active writer.

Limits:
- at most 3 concurrent writers;
- at most 4 concurrent explorers.

Do not split work solely to increase agent utilization.

## Worktree isolation

- one writer: a separate worktree is optional;
- read-only explorers: no worktree required;
- two or more concurrent writers: use isolated worktrees by default.

Each writer should own one task/worktree and return a reviewable diff/commit. The Sol lead owns integration.

If a worker's attempt is abandoned, discard its isolated worktree rather than carrying partial state into another task.

Do not create separate merge, conflict, or integration agents in V1. Escalate integration conflicts to the Sol lead.
