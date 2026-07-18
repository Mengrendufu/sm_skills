# Core Practice Skills Design

## Goal

Promote `brainstorming`, `test-driven-development`, and
`systematic-debugging` from upstream candidates into the portable personal
Skill library without carrying Superpowers, Agent-runtime, or visual-tool
coupling into `skills/`.

## Shared Boundary

- Keep the upstream copies under `candidates/superpowers/` unchanged as
  provenance and comparison material.
- Put only runtime-relevant instructions and resources under `skills/`.
- Use only `name` and `description` frontmatter.
- Refer to sibling Skills by neutral name, never by a plugin namespace.
- Do not require subagents, browser companions, native worktree tools, fixed
  runtime paths, or runtime-specific metadata.
- Preserve the behavior-changing core; do not rewrite merely for tone.

## Skill Designs

### `brainstorming`

The Skill stops implementation when the requested outcome or important design
choices are unresolved. It first reads project evidence, then asks one focused
question at a time, compares two or three viable approaches, presents the
smallest adequate design, and obtains approval before implementation.

Remove the visual companion, `docs/superpowers/` paths, mandatory commits, and
hard dependency on `writing-plans`. If the user has already supplied a complete
decision or delegated a bounded choice, record that evidence instead of asking
the same question again.

### `test-driven-development`

Preserve the RED-GREEN-REFACTOR discipline and the requirement to observe the
test fail for the expected reason. Keep the test anti-pattern reference, but
place it under `references/`. No cross-Skill or Agent-runtime dependency is
needed.

### `systematic-debugging`

Preserve the four phases: root-cause evidence, pattern comparison, one
hypothesis at a time, then a failing regression test and minimal fix. Reference
the formal TDD Skill by neutral name.

Keep reusable debugging references and the polluter-search script. Exclude
creation logs and pressure-test authoring artifacts from the runtime Skill.

## Behavior Evaluation

Each Skill receives a control scenario without reading the formal Skill and the
same scenario with the formal Skill explicitly loaded. Controls are expected to
show at least one target failure:

- `brainstorming`: silently choosing an ambiguous interpretation or starting
  implementation without a design decision.
- `test-driven-development`: writing production code or a test that passes
  immediately before observing a meaningful RED result.
- `systematic-debugging`: proposing a symptom patch before reproduction and
  root-cause evidence.

The forward run passes only when it follows the Skill's ordered gate despite
time, authority, and simplicity pressure.

## Acceptance

- All three directories pass repository and Agent Skills format validation.
- No forbidden Agent-runtime term or missing relative resource appears.
- The formal library grows from 11 to 14 Skills.
- Candidate copies remain byte-for-byte unchanged.
- The installer mirrors all 14 formal Skills without copying generated caches.
- Pressure-test evidence records control and forward outcomes.
