# Repository Agent Instructions

## Purpose

Use a Sol-led, Luna-executed workflow for software engineering. Keep all agent configuration and skills repository-scoped.

## Model roles

- The primary lead is GPT-5.6 Sol at `high`.
- For a simple, bounded, non-critical task, skip Sol design and delegate directly to `luna_fast` (Luna `max`). Sol still performs final review.
- For complex, ambiguous, cross-module, dependency-heavy, or high-risk work, use the managed lane: Sol designs and plans; `luna_explorer` gathers read-only evidence; `luna_worker` implements bounded tasks.
- Use `critical_reviewer` (Sol `xhigh`) for critical-risk review.
- Do not route any V1 workflow to Sol `max`.

## Engineering contract

Implement the **minimum sufficient design**.

Prefer:
- existing repository patterns;
- direct, readable code;
- explicit behavior and strong types;
- narrow changes with clear ownership;
- root-cause fixes.

Avoid unless a current requirement justifies them:
- speculative abstractions or future-proofing;
- new architectural layers;
- redundant validation across trusted internal layers;
- broad `try/catch` blocks that hide failures;
- silent fallbacks for invalid required configuration;
- trivial wrappers and one-use helpers without semantic value;
- unnecessary dependencies or configuration;
- unrelated refactors;
- comments that merely restate the code.

**Defend at trust boundaries; trust validated internal invariants.**
Validate user input, network/external API data, filesystem data, webhooks, security boundaries, and other untrusted inputs. Do not repeatedly revalidate the same invariant after a trusted boundary has established it.

Reuse existing abstractions aggressively. Create new abstractions conservatively, only when there is a real current variation point, policy boundary, or repeated behavior that benefits from a named concept.

## Workflow invariants

- Simple tasks use the fast lane only when scope is clear and risk is below critical.
- Managed work requires a Task DAG and bounded Task Briefs before writer agents are spawned.
- A Task Brief must pass its quality gate before delegation.
- Sol compiles worker-specific context; do not forward the full conversation or full plan to every worker.
- Luna workers may make local implementation choices but must not redesign system architecture.
- A Luna validation failure permits one evidence-based focused repair. If revalidation still fails, stop and escalate to Sol.
- Workers return `READY_FOR_REVIEW`, never `DONE`.
- Only Sol may mark a task `DONE` after review and fresh verification evidence.
- Use proportional verification: targeted checks for low-risk changes; stronger integration/negative-path checks for high-risk changes.
- Concurrent writers are capped at 3 and must have no unresolved dependency, no overlapping write scope, and stable interfaces.
- Read-only explorers are capped at 4.
- When two or more writer agents run concurrently, use isolated worktrees by default.

## Risk and review

- `low`, `medium`, `high`: normal review by Sol `high`.
- `critical`: adversarial review by `critical_reviewer` using Sol `xhigh`.
- Critical examples include authentication/authorization, payment or financial calculations, destructive migrations or data operations, security boundaries, secret handling, concurrency with integrity risk, and irreversible operations.

## Project-specific commands

This repository currently contains the agent workflow scaffold rather than an application. When application code is added, record canonical build, test, lint, typecheck, and integration commands here or in the nearest nested `AGENTS.md`. Do not invent commands that the repository does not define.
