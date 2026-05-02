---
name: strict-coding
description: "Use when implementing, refactoring, designing, or reviewing code that needs strict boundaries: narrow interfaces, explicit contracts, black-box transformations, state-machine behavior, and separated data production, cleanup, and branching."
---

# Strict Coding

## Goal

Produce code whose contracts and execution boundaries are easy to reason about.

This skill merges two concerns:

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

1. Identify the caller, object, and single responsibility.
2. State the contract in plain language before naming methods or fields.
3. Define minimum inputs, outputs, errors, side effects, and invariants.
4. Classify the implementation as black-box, state-machine, or mixed.
5. Split mixed responsibilities before proposing or editing code.
6. Identify data production, data cleanup, and logic branching points.
7. Keep those points separate unless the code is trivially small.
8. Return the narrowest viable interface, implementation, or review findings.

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
- Do not split purely for aesthetics.
- Do not force state-machine structure onto pure data transformations.
- Do not optimize for abstract future flexibility over current contract clarity.
- Keep recommendations contract-first and evidence-based.
