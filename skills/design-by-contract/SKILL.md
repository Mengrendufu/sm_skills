---
name: design-by-contract
description: Contract-checking and error-handling philosophy for coding and code review. Use when an agent must classify failures and place semantic checks such as REQUIRE/precondition, ENSURE/postcondition, INVARIANT/state rule, ASSERT/internal assumption, ALLEGE/must-evaluate check, or ERROR/impossible path, then choose recovery, propagation, rejection, fail-fast, or fatal handling across any programming language.
---

# Design By Contract

## Goal

Classify errors before choosing a handling strategy.

Use contracts to separate normal operational failure from broken programmer assumptions. Name the contract check by responsibility and timing. Recover from expected failures. Expose contract violations early. Stop or isolate execution when state is no longer trustworthy.

## Semantic Checks

These names describe intent, not a required language or macro system.

| Check | Meaning | Where It Belongs |
| --- | --- | --- |
| `REQUIRE` | Precondition: caller obligation before an operation starts | Trusted internal boundary or API after external input has already been validated |
| `ENSURE` | Postcondition: callee guarantee after successful completion | Before returning or publishing a successful result |
| `INVARIANT` | State rule that must remain true across public operations or critical transitions | Around state mutation, lifecycle changes, and concurrency-sensitive boundaries |
| `ASSERT` | Local internal assumption that should be true if the code is correct | Near the assumption, when no more specific check fits |
| `ALLEGE` | Must-evaluate check: the expression/action must still execute even if contract checks are disabled | Rare paths where evaluation itself is required; avoid side effects in other checks |
| `ERROR` | Impossible path or forbidden branch | `default`/fallback branches, unreachable states, unexpected events |

## Workflow

1. Identify the boundary: external input, API boundary, internal call, state transition, concurrency edge, or unreachable branch.
2. Choose the semantic check, if this is a contract check:
   - `REQUIRE` for caller obligations
   - `ENSURE` for callee guarantees
   - `INVARIANT` for stable state rules
   - `ASSERT` for internal assumptions
   - `ALLEGE` when evaluation must happen regardless of check configuration
   - `ERROR` for impossible paths
3. Classify the failure category:
   - expected runtime failure
   - invalid external input
   - contract violation
   - invariant break or corrupted state
   - impossible path
4. Choose the handling policy:
   - recover, retry, degrade, return, or propagate for expected failures
   - reject and report invalid external input
   - trigger the platform's contract-failure mechanism or fail fast for contract violations
   - enter safe state, abort, restart, or invoke fatal handling for untrusted state
5. Place checks at the right boundary:
   - validate untrusted input at system edges
   - use `REQUIRE` for caller obligations at trusted internal boundaries
   - use `ENSURE` for successful-result guarantees
   - use `INVARIANT` around state transitions
   - use `ERROR` for impossible branches
6. For reviews, flag wrong semantic checks, blurred categories, swallowed invariant failures, catch-all handling, assertions on user input, and fatal handlers that lose evidence or return to unsafe code.
7. Read `references/rubric.md` when check placement, classification, continuation safety, or handler design is subtle.
8. Return the semantic check, failure category, handling policy, concrete code guidance, and verification path.

## Do

- Treat expected environmental failures as normal control/data flow.
- Treat contract violations as bugs, not user-facing validation errors.
- Treat broken invariants as evidence that normal continuation may be unsafe.
- Use `REQUIRE`, `ENSURE`, `INVARIANT`, `ASSERT`, `ALLEGE`, and `ERROR` as intent labels even when the target language uses different syntax.
- Prefer the most specific semantic check over a generic assertion.
- Preserve diagnostic evidence: module, stable label or error code, failed predicate, caller/context, and safe state snapshot when possible.
- Use the host platform's normal error-reporting and failure mechanisms while preserving the semantic distinction between recoverable failures, rejected input, contract violations, and unsafe state.
- Keep checks local, executable, and proportionate to the blast radius.

## Do Not

- Do not use assertions for normal user input, missing files, network timeouts, permissions, or other expected runtime failures.
- Do not use `REQUIRE` as a substitute for validating untrusted external input.
- Do not use `ENSURE` to compensate for ignored operational failures.
- Do not use `INVARIANT` for temporary intermediate states unless the code clearly brackets restoration before the boundary is crossed.
- Do not use `ALLEGE` when a side-effect-free check is enough.
- Do not hide impossible paths behind silent defaults.
- Do not catch and flatten distinct failures into one generic status.
- Do not continue after an invariant break unless the code explicitly isolates or re-establishes trustworthy state.
- Do not disable production contract checks without an equivalent safety and observability policy.
- Do not create contract comments that are not checked by code, tests, static analysis, or review.

## Output

- For implementation tasks, state the semantic check and error classification, then apply the matching handling strategy in code.
- For review tasks, list findings first, ordered by severity, with the confused error category and safer policy.
- For design tasks, define only the minimal checks needed to protect the boundary and preserve failure evidence.

## Resources

- Read `references/rubric.md` when reviewing error handling or when classification is unclear.

## Limits

- Keep `SKILL.md` procedural.
- Keep detailed language examples and evaluation criteria in `references/`.
