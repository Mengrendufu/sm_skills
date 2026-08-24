# Cross-Target Strict Contract

## Goal

Apply one semantic acceptance bar across `ts_hsm`, `sm_hsm`, and `rs_hsm_`.

## Require Before Mapping

- strict IR from `qm-c-model-master --output json --strict`
- trace output from `qm-c-model-master --output trace --strict` when verification needs ordering
- `is_reliable=true`
- no error-level diagnostics

## Preserve These Invariants

- exact parent-child hierarchy from `state.id` and `parent_id`
- `top_initial` and every composite-state `initial`
- `entry`, `exit`, and transition `action` as separate phases
- `external`, `internal`, `super`, `unhandled`, and `choice` meanings
- every guarded `branches[]` arm
- every resolved `target_state_id`
- transition ownership via stable IR `transition.id`

## Verify These Things

- default init path against parser trace
- representative external transitions against parser trace
- delegation behavior for `super` and `unhandled`
- no flattened `choice` branch set
- no silent loss of `entry`, `exit`, `init`, or transition effect

## Stop If

- `is_reliable=false`
- any error-level diagnostic exists
- any required `target_state_id` is missing
- any transition or branch `kind` is `unknown`
- the target runtime cannot faithfully express required `super`, `unhandled`, or `choice` behavior
- action code would require semantic invention instead of translation

## Output Rules

- include a short semantic mapping summary with generated code
- call out every adaptation explicitly
- never claim semantic equivalence while any stop condition remains unresolved
