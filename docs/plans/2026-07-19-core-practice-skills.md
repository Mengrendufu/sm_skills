# Core Practice Skills Implementation Plan

**Goal:** Formally add portable versions of `brainstorming`,
`test-driven-development`, and `systematic-debugging`.

**Architecture:** Keep immutable upstream candidates as provenance and build
minimal runtime Skills in `skills/`. Develop each Skill independently with a
control pressure scenario, a minimal adaptation, and a forward run before
starting the next Skill.

**Tech Stack:** Agent Skills Markdown, Bash validation, Git.

## Global Constraints

- Do not modify `candidates/superpowers/skills/`.
- Do not add Agent-specific metadata or paths to formal Skills.
- Do not begin the next Skill until the current Skill passes its pressure test
  and repository validation.
- Do not add resources that only document upstream authoring history.

### Task 1: `brainstorming`

**Files:**

- Create: `skills/brainstorming/SKILL.md`
- Record: `docs/evals/2026-07-19-core-practice-skills.md`

- [x] Run an ambiguous-feature control scenario without reading the Skill.
- [x] Record the control's exact decision and rationalization.
- [x] Write the minimal portable workflow from the approved design.
- [x] Run the same scenario with `skills/brainstorming/SKILL.md` loaded.
- [x] Validate `skills/brainstorming` and commit the completed Skill.

### Task 2: `test-driven-development`

**Files:**

- Create: `skills/test-driven-development/SKILL.md`
- Create: `skills/test-driven-development/references/testing-anti-patterns.md`
- Modify: `docs/evals/2026-07-19-core-practice-skills.md`

- [x] Run a time-pressured bug-fix control without reading the Skill.
- [x] Record whether production code appears before a meaningful failing test.
- [x] Adapt the upstream Skill and move its runtime reference under
  `references/`.
- [x] Run the same scenario with the formal Skill loaded.
- [x] Validate `skills/test-driven-development` and commit it.

### Task 3: `systematic-debugging`

**Files:**

- Create: `skills/systematic-debugging/SKILL.md`
- Create: `skills/systematic-debugging/references/*.md`
- Create: `skills/systematic-debugging/scripts/find-polluter.sh`
- Modify: `docs/evals/2026-07-19-core-practice-skills.md`

- [x] Run a quick-timeout-fix control without reading the Skill.
- [x] Record whether it proposes a patch before locating the failing boundary.
- [x] Adapt the four-phase workflow and copy only runtime resources.
- [x] Exclude the Lace-specific TypeScript example after inspecting its runtime
  dependencies.
- [x] Run the same scenario with the formal Skill loaded.
- [x] Execute the bundled script's help/error path and validate the Skill.
- [x] Commit the completed Skill.

### Task 4: Library Integration

**Files:**

- Modify: `README.md`
- Modify: `candidates/superpowers/README.md`

- [x] Mark the three candidates as promoted while retaining their source copies.
- [x] Run `bash scripts/validate-skills.sh` and expect 14 Skills.
- [x] Run `bash tests/portable-skills.sh` and format validation for all Skills.
- [x] Install all Skills into a temporary target and compare the mirror.
- [x] Confirm the three pressure-test forward runs pass.
