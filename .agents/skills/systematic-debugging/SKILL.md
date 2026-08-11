---
name: systematic-debugging
description: Diagnose test failures, regressions, runtime errors, or unexpected behavior using evidence and root-cause hypotheses before changing code. Use a single focused Luna repair; escalate persistent or cross-cutting failures to Sol.
---

# Systematic Debugging

Do not patch symptoms blindly.

## Process

1. Reproduce or precisely observe the failure.
2. Capture the exact error, failing assertion, state transition, or behavioral mismatch.
3. Trace the actual execution path.
4. Find a nearby working comparison or established repository pattern when available.
5. Form one falsifiable root-cause hypothesis.
6. Choose the smallest experiment or code change that tests/fixes that hypothesis.
7. Re-run the relevant validation.
8. Confirm the root cause is addressed rather than hidden.

## Anti-defensive rules

Do not fix a bug by swallowing an exception, returning a success-shaped fallback, adding repeated checks for an invariant already guaranteed upstream, layering retries without evidence of transience, or adding defaults that hide required missing configuration.

Fix the owner of the violated invariant or the real boundary where failure should be handled.

## Luna circuit breaker

A Luna writer has exactly one evidence-based focused repair after its initial validation failure. If revalidation still fails, stop and escalate to Sol High.

Sol may perform deeper root-cause work, revise the Task Brief or architecture, or give a fresh worker a corrected bounded task.
