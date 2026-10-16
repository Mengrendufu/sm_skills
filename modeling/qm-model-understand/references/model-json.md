# QM Model JSON

## Goal

Use this JSON to read and share model topology. Action snippets are source annotations, not an execution trace.

## Use This File When

- the parser output must be stored
- another skill will consume the model
- a diagram or implementation task needs explicit state and transition identities

## Required Top-Level Fields

- `machine_name`
- `top_initial`
- `states[]`
- `transitions[]`
- `diagnostics[]`
- `is_reliable`
- `state_count`
- `transition_count`

## Required State Fields

- `id`
- `name`
- `path`
- `parent`
- `parent_id`
- `entry`
- `exit`
- `initial` when present

Use `id` and `path` as stable identity. Do not key downstream logic by bare `name`.

## Required Transition Fields

- `id`
- `owner_state`
- `owner_state_id`
- `trigger`
- `kind`
- `target`
- `target_state_id`
- `action`
- `guard`

For guarded transitions, read `branches[]` and keep each branch explicit.

## Semantic Meanings

- `external`: modeled as a state transition
- `internal`: handled with no state change
- `super`: delegated upward
- `unhandled`: not handled here
- `choice`: one guarded transition with explicit `branches[]`

## Resolution Rules

- prefer `target_state_id` over raw `target` when both exist
- keep unresolved targets unresolved
- never invent missing destinations
- assign stable transition `id` only after ownership and target resolution are stable

## Validation Gate

Run:

- `scripts/validate_ir.py <ir.json>`

Require:

- `is_reliable=true`
- no error-level diagnostics

`is_reliable` records the absence of parser error diagnostics. The validator checks structure and references; neither proves equivalence to QP runtime behavior. Review critical semantics against the source C and the [QP state-machine requirements](https://www.state-machine.com/qpc/srs-qp_sm.html).

## Stop If

- `is_reliable=false`
- any error-level diagnostic exists
- required parent or target resolution is missing
- `kind=unknown`
- understanding a relation would require inventing a parent, destination, or guard
