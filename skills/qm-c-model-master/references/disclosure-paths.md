# Progressive Disclosure Paths

## Goal

Load the minimum parser output and reference surface needed for the task.

## Level 1: Fast Semantic Read

Read:

- `SKILL.md`

Run:

- `scripts/parse_qm_c.py <input.c> --output text --strict`

Use when:

- the task is explanation, review, hierarchy reading, or guarded-transition reading

Do not open:

- parser internals
- machine-readable trace docs
- validator scripts

## Level 2: Strict Reuse Contract

Read:

- `references/codegen-ir.md`

Run:

- `scripts/parse_qm_c.py <input.c> --output json --strict`
- `scripts/validate_ir.py <ir.json>`

Use when:

- another skill or agent will reuse the result
- the IR will be stored
- downstream code generation depends on the output

## Level 3: Automation And Trace Checking

Read:

- `references/trace-json.md`

Run:

- `scripts/parse_qm_c.py <input.c> --output trace-json --strict`

Use when:

- another script or agent needs machine-readable traces
- semantic verification depends on init, entry, exit, or effect ordering

## Level 4: Parser Extension Or Debugging

Open only if blocked:

- `scripts/parse_qm_c.py`

Use when:

- the generated C uses an unusual pattern
- diagnostics point to a parser limitation rather than workflow choice
