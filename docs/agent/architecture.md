# Agent Workflow Architecture — V1

## Objective

Build software with a single strong reasoning authority and low-cost ephemeral execution agents, while avoiding orchestration overhead on simple work.

The design borrows the useful discipline of Superpowers-style workflows—design before complex implementation, bounded tasks, systematic debugging, verification before completion, and review—without copying a large agent taxonomy.

## Agent roles

| Role | Model | Effort | Mutability | Purpose |
|---|---|---:|---|---|
| Lead | GPT-5.6 Sol | high | read/write | requirements, architecture, planning, orchestration, normal review, integration, escalation |
| Fast-lane implementer | GPT-5.6 Luna | max | read/write | autonomous simple bounded work |
| Managed worker | GPT-5.6 Luna | xhigh | read/write | implement one Task Brief |
| Explorer | GPT-5.6 Luna | high | read-only | repository evidence and context compression |
| Critical reviewer | GPT-5.6 Sol | xhigh | read-only | adversarial review of critical-risk changes |

Sol `max` is deliberately absent from V1.

## Fast lane

Use when a task is low complexity, bounded, non-critical, and can follow established repository patterns.

```text
user request
  -> lightweight complexity/risk routing
  -> luna_fast
      -> inspect
      -> local minimal design
      -> implement
      -> proportional validate
      -> at most one focused repair
  -> READY_FOR_REVIEW
  -> Sol High review
  -> fresh verification as needed
  -> DONE
```

The main optimization is avoiding the design/planning/subagent orchestration tax for easy work.

## Managed lane

Use for ambiguity, architecture, cross-module behavior, dependencies, meaningful parallelism, or critical risk.

```text
user request
  -> Sol High feature design
      -> optional Luna High explorers
  -> implementation planning
      -> Task DAG
      -> Task Brief quality gates
      -> risk + complexity classification
  -> context compilation
  -> ready tasks
      -> <= 3 Luna XHigh workers
      -> isolated worktrees when writers run concurrently
  -> READY_FOR_REVIEW
  -> Sol High review
      -> critical: Sol XHigh critical reviewer
  -> integration verification
  -> DONE
```

## P0 controls

### Task Brief quality

A managed worker must receive a bounded contract with objective, scope, interfaces, repository evidence, acceptance criteria, validation, non-goals, risk/complexity, and escalation rules.

### Verification

Workers provide evidence; only Sol can declare completion. Verification is proportional to changed behavior and risk.

### Escalation

Luna may perform one evidence-based focused repair after an initial validation failure. Failure after that repair escalates immediately to Sol.

## P1 controls

### Task DAG

The DAG, not the number of available agents, determines parallelism.

### Context compression

Sol compiles task-local context. Explorers reduce noisy repository scans into evidence. Full conversations and plans are not forwarded to every worker.

### Risk + complexity

Risk decides review rigor; complexity decides routing and planning. Critical risk overrides low complexity.

## P2 control: worktree isolation

Read-only exploration shares the repository. Concurrent writers use isolated worktrees by default. Sol owns integration.

## Simplicity contract

The system optimizes for **minimum sufficient design**, not minimum line count.

- defend at trust boundaries;
- trust validated internal invariants;
- reuse existing abstractions aggressively;
- create new abstractions conservatively;
- avoid speculative future-proofing;
- avoid redundant validation and success-shaped fallback;
- use proportional verification;
- require every piece of complexity to serve a current requirement.

This contract is enforced during design, implementation, debugging, verification, and review so simplicity does not depend on a single prompt.
