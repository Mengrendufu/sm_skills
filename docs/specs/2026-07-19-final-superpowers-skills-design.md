# Final Superpowers Skills Design

## Goal

Promote `verification-before-completion` and `using-git-worktrees` into the
portable personal Skill library, then close the Superpowers selection work.
All other staged candidates remain unchanged and unpromoted.

## Shared Boundary

- Preserve every upstream candidate under `candidates/superpowers/skills/` as
  an exact provenance copy.
- Put only runtime-generic instructions in `skills/`.
- Use only `name` and `description` frontmatter.
- Do not name an Agent product, runtime configuration path, plugin namespace,
  or proprietary worktree command.
- Develop and verify the two Skills independently before library integration.

## Skill Designs

### `verification-before-completion`

Preserve the evidence gate: identify the command that proves a claim, execute
it freshly and completely, inspect its exit status and failures, then make only
the claim supported by that output. Delegated work must be independently
checked rather than trusted from a report.

Exclude upstream author-history anecdotes. They do not change runtime behavior
and are not reusable evidence for a personal portable Skill.

### `using-git-worktrees`

Preserve the isolation sequence: detect whether the checkout is already a
linked worktree, distinguish submodules, honor an explicit workspace
preference, prefer an environment-managed isolation capability when one is
available, and otherwise use a safe Git worktree fallback.

The fallback must select a predictable project-local directory, verify that it
is ignored before creation, run project setup only when applicable, and execute
the project baseline before implementation. Do not name or assume a particular
Agent runtime's worktree feature.

## Behavior Evaluation

For each Skill, run combined-pressure controls without the formal Skill and the
same scenarios with the formal Skill loaded.

- Verification controls tempt an agent to reuse stale output, trust another
  agent's success report, or infer a full result from a partial check.
- Worktree controls tempt an agent to nest worktrees, skip the submodule guard,
  create an unignored project-local directory, or proceed after a failing
  baseline.

The forward run passes only when it follows the ordered gate and reports the
actual evidence instead of the desired outcome.

## Acceptance

- Both formal directories pass repository and Agent Skills format validation.
- No forbidden Agent-runtime term or missing relative resource appears.
- The formal library grows from 14 to 16 Skills.
- All eight Superpowers candidate directories remain exact upstream copies.
- The installer mirrors all 16 formal Skills and the configured OpenCode loader
  discovers all 16 through the portable custom path.
- Control and forward-run evidence is recorded.

