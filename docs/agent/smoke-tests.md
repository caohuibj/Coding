# Codex Smoke Tests

Run these on a disposable branch or a non-critical pilot project after installation. The goal is to verify runtime routing, not to benchmark model quality.

## 0. Static doctor

```bash
python3 /path/to/Coding/scripts/agent_team.py doctor .
```

Do not continue if the doctor reports failures.

## 1. Fast lane

Choose a genuinely small, low-risk task that follows an existing repository pattern, such as a localized copy/UI change or a tiny already-understood fix.

Expected behavior:

- no full Sol feature-design / Task-DAG ceremony;
- `luna_fast` handles local inspection, minimal design, implementation, and proportional validation;
- the result is `READY_FOR_REVIEW`, not `DONE`;
- Sol High reviews before completion.

Failure condition: the fast agent makes a system-level architecture decision, accepts critical risk, or bypasses final Sol review.

## 2. Managed lane

Choose a medium-complexity change spanning multiple files or a feature with a real dependency boundary.

Expected behavior:

- Sol High owns design and planning;
- read-heavy questions may be delegated to fresh Luna High explorers;
- planning produces a Task DAG and bounded Task Briefs;
- each Task Brief gets a fresh Luna XHigh worker;
- independent writers run concurrently only with isolated worktrees;
- Sol reviews and runs integration-level verification before `DONE`.

## 3. Critical review routing

On a disposable branch, use a small change that touches an authentication/authorization boundary, destructive data behavior, payment logic, or another clearly critical class. It can be a synthetic change that you will discard.

Expected behavior:

- critical risk is never admitted to the fast lane;
- implementation follows the managed lane;
- final critical review uses `critical_reviewer` (Sol XHigh), not Sol Max;
- review is adversarial and checks negative paths/invariants, not just style.

## 4. One-repair escalation

Use a disposable task where the first implementation will encounter a reproducible validation failure. Keep the task safe and reversible.

Expected behavior:

1. Luna records evidence and a root-cause hypothesis;
2. Luna performs exactly one focused repair;
3. if revalidation still fails, the worker stops and escalates to Sol High;
4. there is no second Luna repair loop.

## 5. Parallel writer isolation

Choose two genuinely independent, non-overlapping tasks.

Expected behavior:

- writer #2 is not spawned until isolated worktrees are available;
- each writer owns one task/worktree;
- if worktree isolation cannot be established, tasks are serialized instead;
- Sol owns integration.

## Pilot acceptance

Treat the installation as V1 Stable for that project after Fast Lane, Managed Lane, review routing, and verification behavior have been observed at least once without a policy violation. The escalation and parallel-writer tests may be run when those paths are relevant, but should be completed before relying on them in production work.
