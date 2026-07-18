---
name: brainstorming
description: Use when creating or changing behavior while important requirements, boundaries, success criteria, or tradeoffs remain unresolved.
---

# Brainstorming

Turn an ambiguous request into the smallest explicit design that is safe to
implement.

**Core rule:** Do not edit implementation files while a material design choice
is hidden or unresolved.

## Workflow

1. **Inspect evidence.** Read the exact project surface, nearby documentation,
   existing patterns, and recent relevant changes. Do not ask for facts the
   workspace can answer.
2. **Name the decision gaps.** Identify the outcome, constraints, non-goals,
   compatibility requirements, failure behavior, and proof of success. Ask one
   focused question at a time when an answer would materially change the
   design.
3. **Check scope.** If the request contains independent subsystems, split them
   and design the first independently testable slice.
4. **Compare approaches.** When more than one viable design remains, present
   two or three options with concrete tradeoffs and recommend the simplest one
   that meets the evidence.
5. **Present the design.** State responsibilities, ownership and boundaries,
   data or control flow, error behavior, and verification. Scale this from a few
   sentences for a local change to short sections for a system change.
6. **Resolve approval.** Ask for approval when the user still owns a material
   choice. If the user already made the decision or explicitly delegated that
   bounded choice, state the decision and evidence; that counts as approval.

Only after this gate may implementation planning or edits begin.

## Output Contract

Before implementation, make these visible:

- Evidence and explicit assumptions.
- Decision gaps that still block implementation.
- Options and recommendation when a meaningful branch exists.
- The selected design and why it satisfies the constraints.
- Approval state: requested, explicitly given, or covered by prior delegation.

## Guardrails

- Do not turn “use reasonable defaults” into permission to invent product
  semantics with irreversible or compatibility impact.
- Do not ask the user to repeat a decision already present in the request or
  project instructions.
- Do not manufacture multiple approaches when the evidence leaves only one
  sensible local change.
- Do not skip design because the code change is small; make a small design.
- Do not force a specific document path, planning system, visual tool, Agent
  capability, or commit workflow.

For durable or multi-step work, record the accepted design under the project's
documentation convention before implementation.
