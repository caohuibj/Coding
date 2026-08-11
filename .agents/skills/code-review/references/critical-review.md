# Critical Review

Use an adversarial posture for critical-risk changes. Attempt to falsify correctness.

Check explicitly for authentication/authorization bypass, violated invariants, unsafe trust-boundary assumptions, destructive/irreversible paths, data corruption, integrity-sensitive race conditions, payment/financial calculation errors, migration/rollback hazards, secret leakage, missing negative tests, tests that falsely reassure, and broad catches/retries/defaults/fallbacks that convert real failures into apparent success.

Also check whether defensive code itself creates complexity or hides ownership. Prefer one clear validation/error boundary over repeated just-in-case checks.

Return findings ordered by severity with concrete evidence and a safe correction direction.
