# Concurrency and Worktree Rules

## Parallelism

Exploration can be relatively aggressive because explorers are read-only. Implementation must be conservative because writers mutate shared state.

A managed task may run concurrently only when every dependency is `DONE`, required interfaces are stable, and write scope does not overlap another active writer.

Workflow limits:
- at most 3 concurrent writers;
- at most 4 concurrent explorers;
- repository hard cap: at most 4 spawned-agent threads total.

The hard cap is not a utilization target. Do not split work solely to fill agent slots.

## Worktree isolation

- one writer: a separate worktree is optional;
- read-only explorers: no worktree required;
- two or more concurrent writers: every writer must use an isolated worktree.

Before spawning writer #2, confirm isolated worktrees are available and assign one worktree per writer. If isolation cannot be established, **do not run concurrent writers; serialize the tasks**.

Each writer owns one task/worktree and returns a reviewable diff/commit. The Sol lead owns integration.

If a worker attempt is abandoned, discard its isolated worktree rather than carrying partial state into a different task.

Do not create separate merge, conflict, or integration agents in V1. Escalate integration conflicts to the Sol lead.
