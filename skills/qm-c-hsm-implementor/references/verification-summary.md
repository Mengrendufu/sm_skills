# Semantic Verification Summary Format

## Goal

Return one stable Markdown summary shape across `ts_hsm`, `sm_hsm`, and `rs_hsm_`.

## Required Sections

1. `Input Evidence`
2. `Verdict`
3. `Hierarchy Check`
4. `Init Check`
5. `Transition Check`
6. `Choice Check`
7. `Delegation Check`
8. `Adaptations`

## Section Requirements

### Input Evidence

- IR source path
- trace source path
- `is_reliable`
- whether diagnostics are empty

### Verdict

- `PASS` only when every required semantic invariant is preserved
- `BLOCKED` when any stop condition remains

### Hierarchy Check

- root states
- parent-child chains
- any adaptation

### Init Check

- `top_initial`
- each composite `initial`
- trace alignment

### Transition Check

List representative transitions by IR `transition.id`:

- source state
- trigger
- target state
- effect handling
- implementation location

### Choice Check

List every guarded `choice` transition by IR `transition.id`:

- each branch guard
- branch kind
- branch target or handled behavior
- implementation location

### Delegation Check

- every `super` or `unhandled` behavior still delegated correctly
- states that intentionally own an event instead of delegating it

### Adaptations

- runtime rewrites that preserve semantics
- `none` when no adaptation was needed beyond syntax

## Rules

- keep section names stable across all targets
- anchor major statements to IR state ids or transition ids
- do not mark the result `PASS` if any section depends on guesswork
- keep this summary aligned with `verification-report-json.md`
