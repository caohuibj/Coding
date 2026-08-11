# Context Compilation

The lead should minimize repeated context across subagents.

## Include

- current Task Brief or fast-lane objective;
- applicable `AGENTS.md` rules;
- stable interfaces and invariants;
- repository evidence and file/symbol pointers;
- only the code context necessary for the task.

## Exclude

- the entire user conversation;
- unrelated architecture history;
- the complete multi-task plan when a worker needs only one node;
- logs from unrelated workers;
- raw exploration output after it has been distilled;
- speculative information not needed for implementation.

## Explorer contract

Use `luna_explorer` as a repository context filter. Ask narrow questions in parallel, then distill its evidence before passing context downstream.

A good explorer response identifies files, symbols, observed behavior, conventions, conflicts, and unknowns. It should not become an alternate architect.

## Principle

**Do not forward context; compile it.**

The goal is sufficient task-local context with minimal repeated tokens and minimal contamination from unrelated reasoning.
