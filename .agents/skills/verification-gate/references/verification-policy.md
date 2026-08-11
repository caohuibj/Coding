# Proportional Verification Policy

Verification depth should match changed behavior and risk.

## Low risk

Examples: copy, CSS, docs, isolated presentation changes. Use targeted rendering/build/lint checks when relevant. Do not run unrelated heavyweight suites as ceremony.

## Medium risk

Examples: ordinary UI behavior, API endpoint, state logic. Use targeted behavior tests plus typecheck/lint/build checks that can detect realistic regressions.

## High risk

Examples: complex business logic, external integration, broad persistence behavior. Add integration coverage, important error paths, and broader regression checks where they provide evidence.

## Critical risk

Examples: auth/authorization, payments, destructive migrations, security boundaries, integrity-sensitive concurrency.

Require positive and negative-path tests, explicit invariant checks, relevant integration/e2e coverage, critical review by Sol `xhigh`, and fresh verification after review fixes.

## Test quality

Prefer tests for observable behavior, important invariants, regressions, real edge cases, and trust/security boundaries.

Avoid tests that merely duplicate implementation details, impossible states already excluded by types/contracts, or framework behavior unrelated to repository logic.
