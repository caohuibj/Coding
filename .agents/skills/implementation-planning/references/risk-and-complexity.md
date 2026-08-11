# Risk and Complexity Classification

Risk and complexity are separate axes.

## Complexity

### Low
Clear objective, local scope, existing pattern, stable interfaces, no system-level architecture decision.

### Medium
Multiple files or components, some coordination, but architecture and interfaces are largely known.

### High
Cross-module behavior, significant refactor, ambiguous requirements, new subsystem, unstable interfaces, or a meaningful dependency graph.

## Risk

### Low
Presentation, copy, docs, fixtures, or other changes with limited correctness impact.

### Medium
Ordinary application behavior, API logic, state handling, non-destructive database reads/writes.

### High
Complex business logic, important external integration, broad persistence changes, or failure with meaningful operational impact.

### Critical
Authentication/authorization, payment or financial calculations, destructive migration/data operations, security boundaries, secret handling, integrity-sensitive concurrency, or irreversible operations.

## Routing

| Complexity | Risk | Route |
|---|---|---|
| Low | Low/Medium | Fast lane: `luna_fast` -> Sol High review |
| Low | High | Sol High admission gate. Use fast lane only when scope, invariants, and failure modes remain simple; otherwise managed lane |
| Any | Critical | Managed lane + `critical_reviewer` Sol XHigh |
| Medium/High | Low/Medium/High | Managed lane |

Critical risk always overrides low complexity. High risk never enters the fast lane automatically.
