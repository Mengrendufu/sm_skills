# QM C Trace JSON

## Goal

Use trace JSON when downstream automation needs machine-readable semantic ordering.

## Use This File When

- init ordering matters
- entry and exit ordering matters
- verification depends on transition phase order
- another script or agent will consume traces directly

## Required Top-Level Fields

- `machine_name`
- `is_reliable`
- `diagnostics[]`
- `default_init_trace`
- `external_transition_traces[]`
- `handled_event_ownership[]`

## Default Init Trace

Must contain:

- `target_state_id`
- `steps[]`

Allowed `phase` values:

- `top_init`
- `enter`
- `init`
- `effect`

## External Transition Trace

Each item must contain:

- `transition_id`
- `source_state_id`
- `trigger`
- `guard`
- `is_else`
- `target_state_id`
- `steps[]`

Allowed `phase` values:

- `transition`
- `exit`
- `enter`
- `init`
- `effect`

## Handled Event Ownership

Each item must contain:

- `state_id`
- `owned[]`
- `delegated[]`

## Policy

- use trace JSON together with strict IR
- do not use trace JSON as a replacement for strict IR
- stop if trace output is needed but `is_reliable=false`
