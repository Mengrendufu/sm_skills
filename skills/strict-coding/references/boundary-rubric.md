# Strict Boundary Rubric

Use this rubric to review an interface or implementation boundary. Favor qualitative judgment over scoring.

## Contract Checks

| Check | Good Signal | Failure Signal |
| --- | --- | --- |
| Responsibility | One clear job stated in one sentence | Multiple verbs or mixed goals |
| Caller burden | Caller passes explicit inputs and gets explicit outputs/errors | Caller must know hidden context, ordering, fields, or lifecycle |
| Side effects | Side effects are named and expected | Side effects are surprising or hidden behind vague helpers |
| State exposure | Internal data and sequencing stay behind the boundary | Caller must inspect flags, fields, or internal modes |
| Evolvability | Contract can change internally without breaking callers | Callers depend on incidental implementation shape |

## Implementation Checks

| Check | Good Signal | Failure Signal |
| --- | --- | --- |
| Black-box fit | Pure input-to-output behavior stays linear and local | Pure transformation is wrapped in unnecessary state machinery |
| State-machine fit | Stateful behavior has explicit states/events/transitions | Stateful behavior is scattered across helpers and flags |
| Data production | Raw input is converted near the source | Raw input flows deep into branching logic |
| Data cleanup | Validation/normalization is centralized | Cleanup is duplicated across branches |
| Logic branching | Branches consume cleaned data and explicit state | Branches parse, clean, mutate state, and decide behavior at once |

## Precision Checks

| Check | Good Signal | Failure Signal |
| --- | --- | --- |
| Query / command shape | Reads and writes are separate unless coupling is essential | One call both fetches and mutates for convenience |
| Flag pressure | Separate operations model distinct behavior | Flags or modes switch unrelated workflows |
| Lifecycle clarity | Setup, use, and teardown rules are explicit or hidden safely | Caller must memorize sequencing rules |
| Assumption load | Preconditions are few and explicit | Success depends on ambient context or unstated setup |

## High-Signal Anti-Patterns

- One interface validates, stores, mutates, and reports.
- Control flags switch unrelated behaviors.
- Caller must prepare or inspect internal state to call safely.
- A public API exposes raw structure because behavior was never modeled.
- A helper named `process`, `handle`, or `execute` hides multiple phases.
- Boolean flags form an implicit state machine.
- Validation is repeated in many branches.
- State transitions happen during data cleanup.

## Revision Direction

When tightening a boundary, prefer:

- Separate operations over behavior flags.
- Explicit values over ambient context.
- Behavior methods over exposed state.
- One stable public contract plus internal helpers.
- Centralized cleanup before branching.
- Explicit states and transitions when behavior is stateful.

## Do Not Over-Correct

Narrowing is not fragmentation. Avoid splitting when:

- One invariant must hold across the whole operation.
- The split would force callers to coordinate broken intermediate state.
- The result is only multiple pass-through wrappers around one unchanged hidden workflow.
