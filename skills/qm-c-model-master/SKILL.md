---
name: qm-c-model-master
description: Explain QM-generated C hierarchical state machines as a semantic model. Use when an agent needs to turn QM/QP C handlers into state hierarchy, initial paths, guarded transitions, traces, or reusable IR for model-level discussion.
---

# QM C Model Master

## Goal

Route QM/QP C state machine analysis into model-level outputs.

## Workflow

1. Confirm the input looks like QM/QP-generated C.
2. Run `scripts/parse_qm_c.py <input.c> --output text --strict` for direct explanation.
3. Switch to `--output json --strict` when another skill or agent will reuse the result.
4. Read `references/disclosure-paths.md` to choose the minimum disclosure level.
5. Read `references/codegen-ir.md` or `references/trace-json.md` only when the requested output requires them.
6. Validate IR with `scripts/validate_ir.py` when reuse matters.

## Do

- Treat the `.c` file as the source of truth for model semantics.
- Keep the discussion at the model level.
- Prefer `--strict` for reusable outputs.
- Use trace output when ordering matters.
- Use IR output when downstream reuse matters.

## Do Not

- Do not narrate the file line by line unless explicitly asked.
- Do not treat unresolved parser diagnostics as usable model truth.
- Do not depend on another artifact when the C handlers are the requested source.

## Resources

- Scripts:
  - `scripts/parse_qm_c.py`
  - `scripts/validate_ir.py`
- References:
  - `references/disclosure-paths.md`
  - `references/codegen-ir.md`
  - `references/trace-json.md`

## Limits

- Keep `SKILL.md` focused on routing to the right parser output and reference layer.
