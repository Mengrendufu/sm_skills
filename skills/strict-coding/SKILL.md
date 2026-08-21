---
name: strict-coding
description: "Use when implementing, refactoring, designing, modeling, or reviewing code whose interfaces, ownership, dependencies, state, or execution boundaries are unclear or tightly coupled."
---

# Strict Coding

## Goal

Produce code whose contracts and execution boundaries are easy to reason about.

This skill merges three concerns:

- Interaction boundary: which logical entities touch and who owns each contract, dependency, and lifetime.
- Interface boundary: what the caller is allowed to know and depend on.
- Implementation boundary: how data production, data cleanup, and logic branching are separated inside the boundary.

## Core Rule

First decide whether the target is:

- A narrow interface / contract problem.
- A linear black-box implementation.
- A state-machine implementation.
- A mixed boundary that must be split before coding.

If behavior depends on current state, mode, event, timing, retry, timeout, initialization phase, previous input, or hidden call order, treat it as state-machine code.

If behavior is "given input, produce output", treat it as linear black-box code.

Do not hide a state machine behind ordinary helper, service, process, handle, or execute functions.

## Workflow

1. Identify the scope, caller, object, and single responsibility.
2. For cross-entity work, list logical entities and real interaction touch points.
3. State the contract in plain language before naming methods or fields.
4. Separate interface ownership, source dependency, runtime flow, and data lifetime.
5. Define minimum inputs, outputs, errors, side effects, and invariants.
6. Classify the implementation as black-box, state-machine, or mixed.
7. Split mixed responsibilities before proposing or editing code.
8. Identify data production, data cleanup, and logic branching points.
9. Keep those points separate unless the code is trivially small.
10. Return the narrowest viable interface, implementation, or review findings.

Read `references/boundary-rubric.md` when the boundary feels wide, leaky, fragmented, stateful, or mixed.

## Interface Boundary Rules

Prefer:

- One interface, one responsibility.
- Explicit inputs, outputs, errors, side effects, and invariants.
- Behavior contracts over exposed structure.
- Separate operations over control flags.
- Query/command separation unless shared atomicity is essential.
- Short steps and shallow call chains.

Reject:

- Do-everything entrypoints.
- Vague helpers such as `process`, `handle`, or `execute_all` when they hide control flow.
- Interfaces that require callers to understand internal state layout.
- Mixed read/write responsibilities unless the coupling is essential.
- Raw data exposure when behavior is the real contract.
- Splitting purely for aesthetics.

## Interaction-Boundary Modeling

Use this before changing module boundaries.

Model logical entities with independent responsibilities, then list their real,
stable touch points. Start from this textual boundary.

Keep these four views separate because their directions can differ:

- Interface ownership: identify separately who states the requirement, who
  defines and evolves the contract, and who supplies its implementation.
- Source dependency: which source imports which abstraction, and where the
  wiring point binds an implementation.
- Runtime flow: who initiates and handles the interaction, how decision authority
  is split between requesting and fulfillment, and whether delivery is
  synchronous or asynchronous.
- Data ownership and lifetime: identify separately the storage owner, mutation
  authority, copy/borrow/transfer/share mode of each value and pointee, validity
  period, and cleanup owner.

A provided interface normally belongs to the module whose behavior it exposes.
A required port belongs to the module that states the need and absorbs changes
to that contract; another module supplies the implementation. Name concrete
source-dependency arrows and the wiring point instead of inferring dependency
from runtime direction.

Do not infer ownership from an action alone:

- Implementing a callback does not imply ownership of its required contract.
- Requesting a state change does not imply ownership of the target state.
- Holding a pointer does not imply ownership of its pointee.
- Copying a descriptor does not imply copying or owning referenced objects.

- Keep a direct dependency when the concrete call is already the stable contract.
- Use dependency inversion when a module must call outward without importing the
  outer implementation.
- Use containment for static organization; use composition only for real runtime
  lifetime ownership.
- Classify runtime delivery as synchronous or asynchronous. Keep event flow
  separate from source dependency so ordering and reactions stay visible.

Model a data structure in detail only when it carries an interaction contract:

- It crosses a module, thread, process, or device boundary.
- Its fields drive receiver branching or state transitions.
- Its ownership or lifetime must be coordinated.
- Its shape forces coordinated changes across entities.

For each cross-boundary value and pointee, record whether it is copied, borrowed,
transferred, or shared, its validity period, mutation authority, and cleanup
owner. Treat the containing descriptor and referenced objects independently.

Otherwise defer fields, helpers, storage layout, algorithms, and private classes.
Do not promote every call to a named interface. Stop when private internals can
change without changing the graph, while the model still explains what crosses
each boundary, who owns it, and how it is handled.

## Linear Black-Box Code

Use linear black-box code for:

- Pure algorithms.
- Encoding and decoding.
- Parsers.
- Numeric computation.
- Data conversion pipelines.
- Clear input-to-output processing steps.

Requirements:

- Keep the interface narrow.
- Keep execution linear.
- Avoid persistent state.
- Avoid hidden temporal dependency.
- Make all required inputs explicit.
- Return explicit output or explicit error.
- Do not introduce state-machine structure unless real state changes exist.

Linear code should be boring, local, testable, and replaceable.

## State-Machine Code

Use explicit state-machine code when behavior involves:

- Rich state.
- Timing sensitivity.
- Event-driven behavior.
- Initialization phases.
- Retries.
- Timeouts.
- Interrupts.
- External messages.
- Pending operations.
- Different behavior for the same input in different modes.

Requirements:

- Make the state owner explicit.
- Make allowed events or inputs explicit.
- Make processing order clear.
- Make state transitions visible in code.
- Define ignored, invalid, and deferred events deliberately.
- Avoid scattered boolean flags that imply hidden states.
- Keep state mutation inside a clear state-handling boundary.
- Provide trace points or test-visible observations for important transitions.

Do not implement stateful behavior as unrelated functions that depend on hidden call order.

## Three-Point Partition

Every implementation should identify:

- Data production point.
- Data cleanup point.
- Logic branching point.

Preferred flow:

```text
data production -> data cleanup -> logic branching
```

### Data Production Point

This is where external or lower-level data enters the system.

Examples:

- User input.
- Files.
- Network.
- Serial port or bus.
- Interrupts.
- Timers.
- Sensors.
- Hardware registers.
- Upstream events.

Rules:

- Make the source explicit.
- Convert raw input into internal types early.
- Do not spread raw input deep into the system.
- Do not perform complex business decisions here.
- Do not mutate long-lived state here unless this point is explicitly the state owner.

### Data Cleanup Point

This is where raw or newly produced data becomes safe to consume.

Cleanup includes:

- Validation.
- Normalization.
- Filtering invalid values.
- Defaults.
- Unit conversion.
- Clamping.
- Denoising.
- Deduplication.
- Decode repair.
- Turning bad input into explicit errors or ignored events.

Rules:

- Centralize validation and normalization.
- Strengthen invariants before data reaches branching logic.
- Make cleanup failure explicit.
- Do not silently pass invalid data into state logic.
- Do not perform state transitions here.

### Logic Branching Point

This is where cleaned data and current state decide behavior.

Common forms:

- Event dispatch.
- State handler.
- Guard condition.
- Transition decision.
- Policy dispatch.
- Mode switch handling.
- State table or transition table lookup.
- State-machine processing function.

Rules:

- Consume only cleaned data.
- Keep branch conditions readable.
- Make state transitions explicit.
- Do not parse raw input inside deep branches.
- Do not duplicate validation across many branches.
- Do not hide state changes behind helpers with unclear side effects.

## Review Focus

When reviewing code, look first for:

- Linear-looking APIs that depend on hidden call order.
- Shared mutable state modified from many places.
- Boolean flag clusters acting as implicit state machines.
- Ordinary functions that mutate long-lived state and trigger follow-up effects without event semantics.
- Retry, timeout, lifecycle, or scheduling behavior hidden in helpers.
- Raw external data flowing directly into state handlers.
- Validation duplicated across many branches.
- State transitions hidden inside cleanup code.
- Interfaces that are too wide, leaky, or coupled to implementation shape.
- Logical entities mixed with helpers, fields, or storage details in one view.
- Interface ownership inferred incorrectly from runtime call direction.
- Source dependency, event flow, and data lifetime collapsed into one arrow.
- Contract ownership inferred from who implements a callback.
- Decision authority confused with target-state or storage ownership.
- A copied descriptor mistaken for ownership of borrowed pointees.
- Containment shown as composition without real lifetime ownership.

## Output

For design tasks, use this skeleton:

```md
Goal:

Caller:

Object:

Responsibility:

Inputs:

Outputs:

Errors / Side Effects:

Constraints / Invariants:

Proposed Interface:

Implementation Shape:

Why This Boundary:

Narrower Alternative:

Non-goals:

Assumptions:
```

For interaction-boundary tasks, also include:

```md
Interface Ownership (requirement / contract / implementation):
Source Dependencies / Wiring Point:
Runtime Flow (initiator / decision / handler / delivery mode):
Data Ownership (mode / storage / mutation / validity / cleanup):
```

For review tasks, use this skeleton:

```md
Findings:

Why The Boundary Is Too Wide, Leaky, Or Stateful:

Data Production / Cleanup / Branching Issues:

Revised Interface Or Implementation Shape:

Why The Revision Is Narrower:

Residual Risks:

Assumptions / Open Questions:
```

## Limits

- Do not do full system architecture decomposition here.
- Do not turn every concrete call into an interface.
- Do not model private data unless it carries a cross-boundary contract.
- Do not equate calling, implementing, storing, or pointing with ownership.
- Do not split purely for aesthetics.
- Do not force state-machine structure onto pure data transformations.
- Do not optimize for abstract future flexibility over current contract clarity.
- Keep recommendations contract-first and evidence-based.
