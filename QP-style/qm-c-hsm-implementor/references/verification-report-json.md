# Machine-Readable Verification Report

## Goal

Return one JSON verification shape that another agent or script can validate mechanically.

## Required Top-Level Fields

- `version`
- `machine_name`
- `inputs`
- `verdict`
- `hierarchy_check`
- `init_check`
- `transition_checks[]`
- `choice_checks[]`
- `delegation_checks[]`
- `adaptations[]`
- `blockers[]`

## Required Nested Fields

### `inputs`

- `ir_path`
- `trace_path`
- `is_reliable`
- `diagnostics[]`

### `verdict`

- `status`
- `reason`

Allowed `status`:

- `PASS`
- `BLOCKED`

### `hierarchy_check`

- `status`
- `roots[]`
- `parent_chains[]`
- `notes[]`

Each `parent_chains[]` item:

- `state_id`
- `parent_id`

### `init_check`

- `status`
- `top_initial`
- `composite_initials[]`
- `trace_alignment`
- `notes[]`

`top_initial`:

- `source`
- `target_state_id`

Each `composite_initials[]` item:

- `state_id`
- `target_state_id`

### `transition_checks[]`

Each item:

- `transition_id`
- `status`
- `source_state_id`
- `trigger`
- `target_state_id`
- `effect`
- `mappings[]`
- `notes[]`

Each `mappings[]` item:

- `runtime`
- `location`

Allowed `runtime` values:

- `ts_hsm`
- `sm_hsm`
- `rs_hsm_`

### `choice_checks[]`

Each item:

- `transition_id`
- `status`
- `branches[]`
- `notes[]`

Each branch:

- `guard`
- `kind`
- `behavior`
- `mappings[]`

### `delegation_checks[]`

Each item:

- `state_id`
- `trigger`
- `status`
- `mechanisms`
- `notes[]`

`mechanisms` must contain:

- `ts_hsm`
- `sm_hsm`
- `rs_hsm_`

## Consistency Rules

- `PASS` requires `inputs.is_reliable=true`
- `PASS` requires empty `inputs.diagnostics[]`
- `PASS` requires empty `blockers[]`
- `PASS` requires every section and every item status to be `PASS`
- `BLOCKED` requires at least one blocker or one non-pass section/item

## Output Rules

- keep this JSON aligned with `verification-summary.md`
- use this JSON as the machine-checkable artifact when automation consumes the result
