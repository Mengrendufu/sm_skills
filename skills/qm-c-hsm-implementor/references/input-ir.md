# QM C Input IR

## Goal

Treat strict IR from `qm-c-model-master` as the only structured input for downstream HSM implementation.

## Required Input Gate

Require:

- `qm-c-model-master --output json --strict`
- `is_reliable=true`
- no error-level diagnostics

Stop if this gate fails.

## Required Top-Level Fields

- `machine_name`
- `top_initial`
- `states[]`
- `transitions[]`
- `diagnostics[]`
- `is_reliable`

## State Fields

Read these fields when mapping state identity and hierarchy:

- `id`
- `name`
- `path`
- `parent`
- `parent_id`
- `entry`
- `exit`
- `initial`
- `transitions[]`
- `children[]`

Use `id` and `path` as stable identity. Do not rely on bare `name` when names may repeat.

## Initial Fields

`top_initial` and state-local `initial` may contain:

- `target`
- `target_state_id`
- `action`
- `kind`

Prefer `target_state_id` over `target` when both exist.

## Transition Fields

Each transition must contain:

- `id`
- `owner_state`
- `owner_state_id`
- `trigger`
- `kind`
- `target`
- `target_state_id`
- `action`
- `guard`

For guarded transitions, read `branches[]`:

- `guard`
- `target`
- `target_state_id`
- `action`
- `kind`
- `is_else`

## Mapping Rules

- `external` -> target-state transition
- `internal` -> handled without transition
- `super` -> explicit parent delegation
- `unhandled` -> runtime equivalent of "not handled here"
- `choice` -> explicit branch-by-branch implementation

## Stop If

- `is_reliable=false`
- any error-level diagnostic exists
- a required `target_state_id` is missing
- `kind=unknown`
- a `choice` branch cannot be represented clearly in the target runtime
- `strict-contract.md` would be violated
