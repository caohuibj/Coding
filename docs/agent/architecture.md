# Agent Workflow Architecture — V1

## Objective

Build software with one strong reasoning authority and low-cost ephemeral execution agents, while avoiding orchestration overhead on simple work.

The design borrows useful Superpowers-style discipline—design before complex implementation, bounded tasks, systematic debugging, verification before completion, and review—without creating a large agent taxonomy.

## Agent roles

| Role | Model | Effort | Mutability | Purpose |
|---|---|---:|---|---|
| Lead | GPT-5.6 Sol | high | read/write | requirements, architecture, planning, orchestration, normal review, integration, escalation |
| Fast-lane implementer | GPT-5.6 Luna | max | read/write | autonomous simple bounded work |
| Managed worker | GPT-5.6 Luna | xhigh | read/write | implement one Task Brief |
| Explorer | GPT-5.6 Luna | high | read-only | repository evidence and context compression |
| Critical reviewer | GPT-5.6 Sol | xhigh | read-only | adversarial review of critical-risk changes |

Sol `max` is deliberately absent from V1.

## Complexity- and risk-aware routing

### Fast lane

Default admission requires low complexity and low/medium risk. Low-complexity high-risk work requires an explicit Sol High admission decision; critical risk is never admitted.

```text
user request
  -> classify complexity + risk
  -> admitted simple work
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

The optimization is avoiding Sol design/planning orchestration tax when the problem is already bounded.

### Managed lane

Use for medium/high complexity, ambiguity, architecture, cross-module behavior, dependencies, meaningful parallelism, high-risk work not admitted to fast lane, or any critical risk.

```text
user request
  -> Sol High feature design
      -> optional fresh Luna High explorers
  -> implementation planning
      -> Task DAG
      -> Task Brief quality gates
      -> risk + complexity classification
  -> context compilation
  -> ready tasks
      -> fresh Luna XHigh worker per Task Brief
      -> <= 3 writer policy
      -> isolated worktrees for concurrent writers
  -> READY_FOR_REVIEW
  -> Sol High review
      -> critical: Sol XHigh critical reviewer
  -> integration verification
  -> DONE
```

## Agent lifecycle

Workers and explorers are ephemeral execution contexts, not long-lived personas.

- one managed Task Brief -> one fresh worker -> review/escalation -> close;
- one investigation question -> one fresh explorer -> evidence -> close, except tightly scoped follow-up;
- repository decisions, architecture, and history stay with Sol and durable repository artifacts.

## P0 controls

### Task Brief quality
Managed workers receive bounded contracts with objective, scope, interfaces, repository evidence, acceptance criteria, validation, non-goals, risk/complexity, and escalation rules. A quality gate runs before delegation.

### Verification
Workers provide evidence; only Sol can declare completion. Verification is proportional to changed behavior and risk.

### Escalation
Luna may perform one evidence-based focused repair after an initial validation failure. Failure after that repair escalates immediately to Sol.

## P1 controls

### Task DAG
The DAG, not available agent count, determines parallelism.

### Context compression
Sol compiles task-local context. Explorers reduce noisy repository scans into evidence. Full conversations and plans are not forwarded to every worker.

### Risk + complexity
Complexity determines planning/routing; risk determines admission and review rigor. Critical risk overrides low complexity.

## P2 control: worktree isolation

Read-only exploration shares the repository. One writer may use the current workspace. Two or more concurrent writers require isolated worktrees; if isolation is unavailable, writers are serialized. Sol owns integration.

## Concurrency

The repository hard cap is 4 spawned-agent threads. Workflow policy permits up to 3 concurrent writers and up to 4 concurrent explorers, but the hard cap always wins and is not a utilization target.

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

This contract is enforced during design, implementation, debugging, verification, and review so simplicity does not depend on one prompt.
