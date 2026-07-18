# Final Superpowers Skills Implementation Plan

**Goal:** Formally add portable versions of `verification-before-completion`
and `using-git-worktrees`, leaving all other candidates unpromoted.

**Architecture:** Keep immutable upstream candidates as provenance and build
independent runtime Skills under `skills/`. Complete RED control, minimal
adaptation, forward test, validation, and commit for the first Skill before
starting the second.

**Tech Stack:** Agent Skills Markdown, Bash validation, Git.

## Global Constraints

- Do not modify `candidates/superpowers/skills/`.
- Do not add Agent-specific metadata, product names, paths, or proprietary
  worktree commands to formal Skills.
- Do not promote any other candidate.
- Do not move to the next Skill before the current Skill passes its pressure
  test and repository validation.

### Task 1: `verification-before-completion`

**Files:**

- Create: `skills/verification-before-completion/SKILL.md`
- Create: `docs/evals/2026-07-19-final-superpowers-skills.md`

- [x] Run combined-pressure controls without the formal Skill.
- [x] Record stale-evidence, delegated-report, and partial-check behavior.
- [x] Adapt the evidence gate without upstream author-history material.
- [x] Run the same scenarios with the formal Skill loaded.
- [x] Validate the completed Skill.

### Task 2: `using-git-worktrees`

**Files:**

- Create: `skills/using-git-worktrees/SKILL.md`
- Modify: `docs/evals/2026-07-19-final-superpowers-skills.md`

- [ ] Run isolation controls without the formal Skill.
- [ ] Record nested-worktree, ignore-check, and baseline-test behavior.
- [ ] Adapt the workflow around generic capability detection and safe Git
  fallback.
- [ ] Run the same scenarios with the formal Skill loaded.
- [ ] Validate and commit the completed Skill.

### Task 3: Library Closure

**Files:**

- Modify: `README.md`
- Modify: `candidates/superpowers/README.md`

- [ ] Mark only the two selected candidates as promoted.
- [ ] Validate all 16 formal Skills and all eight candidate provenance copies.
- [ ] Install all 16 Skills into a temporary target and compare the mirror.
- [ ] Confirm the configured OpenCode loader discovers all 16 Skills.
- [ ] Commit integration documentation and confirm a clean worktree.
