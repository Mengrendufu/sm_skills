# Error Handling Contract Rubric

Use this rubric when code mixes normal failures, validation, contract violations, invariant breaks, and impossible paths.

Use `REQUIRE`, `ENSURE`, `INVARIANT`, `ASSERT`, `ALLEGE`, and `ERROR` as semantic check names. They describe responsibility and timing, not a required language or macro library.

Score each dimension from `0-3`:

- `0`: missing or misleading
- `1`: mentioned but vague
- `2`: clear and mostly actionable
- `3`: precise, testable, and integrated into the workflow

## Error Categories

| Category | Meaning | Preferred Handling | Anti-Pattern |
| --- | --- | --- | --- |
| Expected runtime failure | Correct code can hit this because the world fails: IO, network, timeout, permission, unavailable dependency | Return/propagate error, retry, degrade, compensate, or report | Contract failure or process abort |
| Invalid external input | Untrusted caller/user/API input is malformed or unauthorized | Validate at boundary, reject with actionable error | Treat as internal bug or let it corrupt state |
| Contract violation | Trusted caller/callee broke an internal obligation or guarantee | Fail fast with evidence using the platform's contract-failure mechanism | Swallow, coerce, silently continue |
| Invariant break | State that must always be true is false; continuation may be unsafe | Isolate, enter safe state, abort, restart, or invoke fatal handling | Patch state casually and proceed |
| Impossible path | Branch should be unreachable if code and model are correct | Mark unreachable explicitly and fail if executed | Empty default, ignored event, silent no-op |

## Semantic Check Placement

| Check | Strong Signal | Anti-Pattern |
| --- | --- | --- |
| `REQUIRE` | Captures a caller obligation at operation entry or trusted internal boundary | Used for raw user input, parse errors, missing files, or other normal failures |
| `ENSURE` | Captures a callee guarantee after successful completion | Used to hide that success was never established |
| `INVARIANT` | Protects state that must hold before/after public operations or critical transitions | Used on temporary internal states before restoration is required |
| `ASSERT` | Captures a local programmer assumption when no more specific check fits | Generic assertion used where `REQUIRE`, `ENSURE`, `INVARIANT`, or `ERROR` would clarify ownership |
| `ALLEGE` | Makes clear that evaluation must still happen even if checks are disabled | Used casually for side-effect-free predicates |
| `ERROR` | Marks an impossible path, forbidden branch, or unexpected event | Silent `default`, ignored state, empty fallback |

## Core Dimensions

| Dimension | Strong Signal | Anti-Pattern |
| --- | --- | --- |
| Classification | The code says what kind of failure this is and why | One generic `error`/`exception`/`false` for everything |
| Check Semantics | The code uses the right semantic check for ownership and timing | Generic assertion everywhere |
| Boundary Placement | External validation, `REQUIRE`, `ENSURE`, and `INVARIANT` checks happen at the correct boundary | Assert on user input or validate trusted internals repeatedly |
| Continuation Safety | The handler decides whether normal execution can safely continue | Continue after corrupted state with no isolation |
| Evidence | Failure preserves module, stable code/label, failed condition, and useful context | Logs only `failed` or loses original cause |
| Verification | Tests, fault injection, static checks, or review cover the failure path | Handler exists but is never exercised |

## Decision Questions

1. Could a correct caller trigger this in normal operation?
   - Yes: do not assert; return, propagate, retry, or reject.
   - No: likely contract violation or impossible path.
2. Is this a caller obligation, callee guarantee, stable state rule, local assumption, must-evaluate action, or impossible path?
   - Map it to `REQUIRE`, `ENSURE`, `INVARIANT`, `ASSERT`, `ALLEGE`, or `ERROR`.
3. Did untrusted input cross a boundary?
   - Yes: validate and reject before it becomes internal state.
4. Is core state now untrustworthy?
   - Yes: prefer isolation, safe state, abort, restart, or fatal handling.
5. Would continuing make later damage harder to diagnose?
   - Yes: fail fast with evidence.
6. Is the handler reliable under degraded conditions?
   - Fatal paths should avoid fragile dependencies and should be tested.

## Handler Design

| Dimension | Strong Signal | Anti-Pattern |
| --- | --- | --- |
| Recoverable Handler | Caller can inspect, retry, compensate, or show a useful message | Error is logged and discarded |
| Fatal Handler | Does not return to unsafe code; preserves evidence; moves toward safe state, abort, restart, or supervisor handoff | Stop path with no evidence or policy |
| Production Policy | Contract checks remain active where they protect safety, correctness, or observability | All assertions disabled with no replacement |
| Stable Identification | Failures use stable labels/codes rather than volatile line numbers when possible | Diagnostics change whenever nearby code moves |

## Severity Guide

- `high`: invariant break is swallowed, impossible path silently continues, fatal handler returns to unsafe code, or operational failure and contract violation are blurred in a way that can corrupt state.
- `medium`: classification is present but weak, evidence is insufficient, or checks are at the wrong boundary.
- `low`: handling is mostly sound but can be clearer, more idiomatic, or better verified.

## Cross-Cutting Anti-Patterns

- Assert used as user input validation.
- `REQUIRE` used before input is trusted.
- `ENSURE` used on a path where the operation already failed.
- `INVARIANT` used for a state that is allowed to be temporarily false inside a properly bracketed mutation.
- `ERROR` replaced with silent fallback for an unexpected state or event.
- Blanket catch/recover that converts bugs into normal responses.
- Silent fallback or coercion that hides contract failure.
- `default:` branch that ignores an unrecognized state or event.
- Fatal path that depends on heap allocation, network logging, locks, or other fragile resources without fallback.
- Comments describing obligations that code never checks.

## Overall Judgment

- `high quality`: errors are classified, continuation safety is explicit, evidence is preserved, and important paths are verified.
- `usable but weak`: the main policy is sound, but at least one boundary, evidence, or verification point is vague.
- `unsafe`: the code treats all failures alike, hides invariant breaks, or continues after untrusted state without isolation.
