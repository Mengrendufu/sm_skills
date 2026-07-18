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

## Interaction Modeling Checks

| Check | Good Signal | Failure Signal |
| --- | --- | --- |
| Entity choice | Logical responsibility with a stable boundary | Helper, field bundle, or storage detail promoted to component |
| Touch point | Real cross-entity contract | Every internal call becomes an interface |
| Contract ownership | Requirement owner owns required port; behavior owner owns provided API | Implementer or runtime target is assumed to own the contract |
| Implementation | Contract owner and implementer are identified separately | Callback implementation is treated as contract ownership |
| Source dependency | Concrete import arrows and wiring point are named | Dependency is guessed from runtime direction |
| Runtime flow | Request and fulfillment authority, handler, and delivery mode are explicit | Calling or handling is treated as ownership |
| Data authority | Storage, mutation, and cleanup authority are distinct | Requesting a change is treated as owning target state |
| Data mode | Value and pointee each state copy, borrow, transfer, or share plus validity | Pointer or descriptor copy is treated as pointee ownership |
| Data detail | Detail exists only for contract-bearing data | Private layout dominates the top-level view |
| Containment | Composition means real lifetime ownership | Package nesting is shown as runtime ownership |

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
- Runtime flow is mistaken for source-dependency direction.
- Event flow, source dependency, and data lifetime are collapsed into one arrow.
- A callback exists, but the concrete modules still import each other.
- Implementing a callback is mistaken for owning its required contract.
- A request is mistaken for ownership of the state it changes.
- A copied descriptor hides borrowed or shorter-lived pointees.

## Revision Direction

When tightening a boundary, prefer:

- Separate operations over behavior flags.
- Explicit values over ambient context.
- Behavior methods over exposed state.
- One stable public contract plus internal helpers.
- Centralized cleanup before branching.
- Explicit states and transitions when behavior is stateful.
- Textual logical entities and touch points before diagram details.
- Separate requirement, contract, implementation, decision, storage, and cleanup
  authority within the four boundary views.
- Explicit copy, borrow, transfer, or share semantics and validity periods.
- Direct dependencies unless inversion solves a real outward dependency.

## Do Not Over-Correct

Narrowing is not fragmentation. Avoid splitting when:

- One invariant must hold across the whole operation.
- The split would force callers to coordinate broken intermediate state.
- The result is only multiple pass-through wrappers around one unchanged hidden workflow.
- A concrete dependency is already stable and does not need substitution or inversion.
