# Progressive Disclosure Paths

## Goal

Load only the references and scripts needed for one target runtime and one verification depth.

## Level 1: Target Mapping

Read:

- `SKILL.md`
- one target file:
  - `references/ts-hsm-api.md`
  - `references/sm-hsm-api.md`
  - `references/rs-hsm-api.md`

Use when:

- the task is to sketch, review, or implement one target runtime
- the input IR is already strict and trusted

Do not open:

- verification report docs
- automation scripts
- other target files unless the task explicitly compares targets

## Level 2: Cross-Target Strict Contract

Read:

- `references/input-ir.md`
- `references/strict-contract.md`

Use when:

- the output must preserve the same semantic bar across TypeScript, C, and Rust
- another agent will rely on the implementation output

## Level 3: Verification Artifacts

Read:

- `references/verification-summary.md`
- `references/verification-report-json.md`

Run:

- `scripts/validate_verification_report.py <report.json>`

Use when:

- the implementation needs auditable verification output
- another agent or automation step will consume the report

## Level 4: Full Automation

Run:

- `scripts/build_verification_bundle.py <ir.json> <trace.json> <report.json> <summary.md>`

Use when:

- strict IR and trace JSON already exist
- the goal is reusable verification artifacts, not ad hoc prose

## Level 5: Script Extension Or Debugging

Open only if blocked:

- `scripts/generate_verification_report.py`
- `scripts/render_verification_summary.py`
- `scripts/build_verification_bundle.py`

Use when:

- the automation output shape must change
- the generated report is structurally valid but semantically incomplete
