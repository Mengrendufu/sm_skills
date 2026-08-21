---
name: design-by-contract
description: Assertion discipline and error-handling philosophy for coding and code review. Use when an agent must decide whether a check deserves an ASSERT/internal assumption versus another failure route, place assertions correctly, or choose recovery, propagation, rejection, fail-fast, or fatal handling across any programming language.
---

# Design By Contract

## Goal

Decide what deserves an assertion, then handle every other failure deliberately.

`ASSERT` covers only local internal assumptions that hold when the surrounding code is correct. Anything else is either a contract boundary owned by a more specific check, or a failure that needs an explicit handling strategy. Misusing assert for those cases turns recoverable failures into crashes, or loses protection entirely when release builds strip checks.

## Routing: Is It an ASSERT?

These names describe intent, not a required language or macro system.

| Signal | Verdict | Route |
| --- | --- | --- |
| A correct caller can trigger it in normal operation (IO, timeout, permission) | Expected runtime failure | Handling policy: return, propagate, retry, degrade |
| Untrusted input crossing the system edge | Input validation | Validate and reject at the boundary |
| Caller obligation before a trusted internal operation | `REQUIRE` | Contract check at operation entry |
| Callee guarantee after successful completion | `ENSURE` | Contract check before returning the result |
| State rule that must hold across public operations or transitions | `INVARIANT` | Contract check around state mutation |
| Branch unreachable if code and model are correct | Impossible path | Mark explicitly (`ERROR`), never silent default |
| Evaluation itself must execute even when checks are disabled | Must-evaluate | `ALLEGE`, keep it side-effect-free |
| None of the above: a local assumption true when this code is correct | **`ASSERT`** | Place near the assumption |

## ASSERT Discipline

- Assert only what is impossible when the surrounding code is correct; everything else has a route above.
- Place the check near the assumption it protects; keep predicates local, executable, and side-effect-free.
- Make violations diagnosable: stable label or error code plus a readable failed condition and caller context.
- Assume the platform may compile assertions out of release builds; never put required behavior inside the expression.
- Prefer the most specific check over a generic assertion when ownership would otherwise stay unclear.

## Failure Categories and Handling Policy

Classify before choosing how to respond:

- expected runtime failure → recover, retry, degrade, return, or propagate
- invalid external input → validate and reject with actionable error
- contract violation → platform's contract-failure mechanism or fail fast with evidence
- invariant break or corrupted state → isolate, enter safe state, abort, restart, or invoke fatal handling
- impossible path → explicit unreachable marker that fails loudly if executed

Without this step, assertion becomes the answer to everything; it must stay the answer to almost nothing.

## Workflow

1. Ask first: could a correct caller hit this in normal operation? If yes, stop - it is not an ASSERT; classify the failure and pick a handling policy.
2. Check for a more specific owner: `REQUIRE`, `ENSURE`, `INVARIANT`, `ERROR`, or `ALLEGE`. Only when none fits does the check remain an ASSERT.
3. Classify the failure category (expected failure, invalid input, contract violation, invariant break, impossible path).
4. Choose the handling policy for everything routed away from ASSERT.
5. For confirmed ASSERTs: place near the assumption, keep the predicate side-effect-free, attach diagnostic evidence.
6. For reviews: flag asserts on user input or expected failures, assertions carrying required behavior, generic assertions hiding a specific check's ownership, swallowed invariant failures, catch-all handling, and fatal handlers that lose evidence or return to unsafe code.
7. Read `references/rubric.md` when classification, placement, continuation safety, or handler design is subtle.
8. Return the verdict (ASSERT or routed alternative), failure category, handling policy, concrete code guidance, and verification path.

## Do

- Treat expected environmental failures as normal control/data flow handled by policy.
- Treat contract violations as bugs, not user-facing validation errors.
- Preserve diagnostic evidence: module, stable label or error code, failed predicate, caller/context.
- Use the host platform's normal error-reporting mechanisms while keeping recoverable failures, rejected input, contract violations, and unsafe state distinct.

## Do Not

- Do not assert user input, missing files, network timeouts, permissions, or any expected runtime failure.
- Do not put required behavior inside an assert expression; release builds may remove it entirely.
- Do not hide impossible paths behind silent defaults instead of an explicit marker.
- Do not catch and flatten distinct failures into one generic status.
- Do not continue after an invariant break unless the code explicitly isolates or re-establishes trustworthy state.
- Do not disable production contract checks without an equivalent safety and observability policy.

## Output

- For implementation tasks, state the ASSERT-or-route verdict and error classification, then apply the matching handling strategy in code.
- For review tasks, list findings first, ordered by severity, with the confused error category and safer policy.
- For design tasks, define only the minimal checks needed to protect the boundary and preserve failure evidence.

## Resources

- Read `references/rubric.md` when reviewing error handling or when classification is unclear.

## Limits

- Keep `SKILL.md` procedural.
- Keep detailed language examples and evaluation criteria in `references/`.
