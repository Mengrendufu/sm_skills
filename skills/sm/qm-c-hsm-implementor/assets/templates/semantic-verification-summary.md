# Semantic Verification Summary

## Input Evidence

- IR: `<path>`
- Trace: `<path>`
- `is_reliable`: `true|false`
- Diagnostics: `none|list`

## Verdict

- `PASS|BLOCKED`
- Reason: `<short reason>`

## Hierarchy Check

- Roots: `<state ids>`
- Parent chains: `<state id -> parent id>`
- Notes: `<none or adaptation>`

## Init Check

- `top_initial`: `<source -> target>`
- Composite initials:
- `<state id -> target state id>`
- Trace alignment: `<confirmed or blocked>`

## Transition Check

- `<transition id>`: `<source> --<trigger>--> <target>` mapped in `<target location>`
- Effect: `<preserved|adapted|none>`

## Choice Check

- `<transition id>`:
- `[<guard or else>]` `<kind>` `<target or handled>` mapped in `<target location>`

## Delegation Check

- `<state id>`: `<trigger>` delegates via `<super mechanism>`
- Notes: `<none or mismatch>`

## Adaptations

- `<none or explicit adaptation>`
