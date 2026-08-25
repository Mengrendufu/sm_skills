---
name: qm-c-hsm-implementor
description: Implement hierarchical state machines in another runtime from QM C semantics. Use when an agent needs strict `qm-c-model-master` IR and must carry QM/QP C hierarchy, guards, actions, and init behavior into `ts_hsm`, `sm_hsm`, `rs_hsm_`, or another target implementation plan.
---

# QM C HSM Implementor

## Goal

Route QM C HSM semantics into a target runtime without losing hierarchy or behavior.

## Workflow

1. Start from strict IR, not raw prose.
2. Read `references/disclosure-paths.md` to select the minimum depth needed.
3. Select one primary target runtime.
4. Read only the matching target reference file:
   - `references/ts-hsm-api.md`
   - `references/sm-hsm-api.md`
   - `references/rs-hsm-api.md`
5. Read `references/input-ir.md` and `references/strict-contract.md` when mapping semantics.
6. Use the verification scripts and reports only when verification output is required.
7. Stop and surface mismatches when the target cannot faithfully express source behavior.

## Do

- Preserve hierarchy, init paths, guarded branches, entry/exit actions, and transition kinds.
- Keep IR identities available when mapping branches.
- Prefer behavioral fidelity over target-language convenience.
- Use verification artifacts when correctness matters.

## Do Not

- Do not start from informal prose when strict IR is available.
- Do not flatten guarded choice behavior into one edge.
- Do not silently rewrite unsupported target semantics.
- Do not read every reference file by default.

## Resources

- Start with:
  - `references/disclosure-paths.md`
  - `references/input-ir.md`
  - `references/strict-contract.md`
- Then read one target file:
  - `references/ts-hsm-api.md`
  - `references/sm-hsm-api.md`
  - `references/rs-hsm-api.md`
- Verification artifacts when needed:
  - `references/verification-summary.md`
  - `references/verification-report-json.md`
- Scripts:
  - `scripts/build_verification_bundle.py`
  - `scripts/generate_verification_report.py`
  - `scripts/render_verification_summary.py`
  - `scripts/validate_verification_report.py`

## Limits

- Keep `SKILL.md` focused on routing by target and disclosure depth.
- Keep target-specific and verification-specific detail in `references/` and `scripts/`.
