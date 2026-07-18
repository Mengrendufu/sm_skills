# Portable Personal Agent Skills Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the OpenCode-specific configuration repository into a validated, tool-neutral personal Agent Skills library.

**Architecture:** `skills/` is the canonical Agent Skills source. A generic validator enforces the portability contract, and a generic installer mirrors selected skill directories into an explicit caller-provided destination without knowing which agent runtime owns it.

**Tech Stack:** Bash, standard Unix utilities, rsync, Markdown, Agent Skills `SKILL.md` format.

## Global Constraints

- Keep exactly the eleven user-managed skills named in the design spec.
- Do not vendor Codex system skills, plugin-cache skills, or `agents/openai.yaml`.
- Do not deploy into `/home/sunnymatato/.config/opencode` or another live runtime directory.
- Keep skill resources relative to each skill root.
- Do not retain Agent-runtime names, paths, or proprietary frontmatter below `skills/`.
- Preserve unrelated runtime-independent skill behavior.

---

### Task 1: Portable library contract and migration tooling

**Files:**
- Create: `tests/portable-skills.sh`
- Create: `scripts/validate-skills.sh`
- Create: `scripts/install-skills.sh`

**Interfaces:**
- Consumes: repository root containing `skills/`.
- Produces: `scripts/validate-skills.sh [repo-root]` and `scripts/install-skills.sh <target> [skill ...]`.

- [ ] **Step 1: Write failing portability and installer tests**

  Cover the current runtime-name/path violations, invalid frontmatter, a
  non-executable bundled script, all-skill installation, selected installation,
  stale-file removal inside a selected skill, and preservation of unrelated
  target skills.

- [ ] **Step 2: Run the tests and verify RED**

  Run: `bash tests/portable-skills.sh`

  Expected: FAIL because the validator and installer do not exist.

- [ ] **Step 3: Implement the minimum validator and installer**

  The validator must inspect only the supplied repository. The installer must
  reject `/`, the user's home directory, the repository root, and the canonical
  `skills/` source as targets; then use `rsync -a --delete` only within each
  selected destination skill directory.

- [ ] **Step 4: Run the tests and verify GREEN**

  Run: `bash tests/portable-skills.sh`

  Expected: installer tests pass; repository validation still reports the known
  legacy coupling until Task 2 and Task 3 remove it.

- [ ] **Step 5: Commit**

  ```bash
  git add scripts tests docs
  git commit -m "feat: add portable skill migration checks"
  ```

### Task 2: Synchronize and decouple the canonical skills

**Files:**
- Modify: `skills/grill-with-docs/SKILL.md`
- Move: `skills/grill-with-docs/{ADR-FORMAT.md,CONTEXT-FORMAT.md}` to `references/`
- Modify: `skills/handoff/SKILL.md`
- Modify: `skills/obsidian-master/SKILL.md`
- Modify: `skills/obsidian-master/references/official-cli-patterns.md`
- Modify: `skills/obsidian-master/scripts/obsidian-local.sh`
- Modify: `skills/qm-c-hsm-implementor/assets/examples/sm-master/sm_master.verification.{bundle,scaffold}.json`
- Modify: `skills/strict-coding/SKILL.md`
- Modify: `skills/strict-coding/references/boundary-rubric.md`
- Modify: `skills/win-wsl-path-converter/SKILL.md`
- Modify: `skills/zoom-out/SKILL.md`
- Mode-only: six Python files under the QM skills' `scripts/` directories.

**Interfaces:**
- Consumes: the eleven current user-managed Codex skills as the semantic baseline.
- Produces: the same behavior with Agent-runtime coupling removed.

- [ ] **Step 1: Capture the current validation failure**

  Run: `bash scripts/validate-skills.sh`

  Expected: FAIL on OpenCode names/paths, unsupported frontmatter, `.BACKUP`
  directories, and non-executable QM scripts.

- [ ] **Step 2: Apply the current semantic updates**

  Bring `grill-with-docs`, `strict-coding`, `boundary-rubric.md`, and `zoom-out`
  in line with the current user-managed source. Preserve the other eight skills'
  behavior.

- [ ] **Step 3: Remove runtime coupling**

  Replace OpenCode references in `handoff`; use `<skill-dir>/scripts/...` in
  skill instructions and references; make the Obsidian wrapper locate the
  sibling converter from its own script directory; replace agent-config paths in
  QM example metadata with portable relative paths.

- [ ] **Step 4: Restore executable modes**

  Run: `chmod +x skills/qm-c-hsm-implementor/scripts/*.py skills/qm-c-model-master/scripts/*.py`

- [ ] **Step 5: Re-run focused skill checks**

  Run: `bash scripts/validate-skills.sh`

  Expected: only top-level obsolete repository artifacts remain to be removed by
  Task 3, or PASS if the validator scopes only to canonical skill directories.

- [ ] **Step 6: Commit**

  ```bash
  git add skills
  git commit -m "refactor: make personal skills agent neutral"
  ```

### Task 3: Remove runtime configuration and document migration

**Files:**
- Delete: `opencode.jsonc`
- Delete: `agents/code-reviewer.md.BACKUP`
- Delete: `skills/diagnose.BACKUP/`
- Delete: `skills/tdd.BACKUP/`
- Delete: `skills/write-a-skill.BACKUP/`
- Modify: `AGENTS.md`
- Replace: `README.md`

**Interfaces:**
- Consumes: the portable library and scripts from Tasks 1-2.
- Produces: a repository containing no runtime configuration and concise install guidance.

- [ ] **Step 1: Remove obsolete runtime-owned files**

  Delete the OpenCode config, obsolete custom-agent backup, and three discoverable
  backup skills.

- [ ] **Step 2: Rewrite repository guidance**

  Keep `AGENTS.md` behavior-oriented and replace its concrete subagent/model
  wording with capability-based delegation guidance.

- [ ] **Step 3: Rewrite the README**

  Document the eleven skills, the Agent Skills portability contract, generic
  validation and installation commands, and a destination-path table for known
  compatible runtimes. Link to each runtime's official documentation.

- [ ] **Step 4: Verify repository cleanup**

  Run: `bash scripts/validate-skills.sh && bash tests/portable-skills.sh`

  Expected: PASS.

- [ ] **Step 5: Commit**

  ```bash
  git add -A
  git commit -m "refactor: make repository a portable skill library"
  ```

### Task 4: Full verification and independent review

**Files:**
- Review: all changed files.

**Interfaces:**
- Consumes: completed Tasks 1-3.
- Produces: evidence that the repository is portable, internally consistent, and clean.

- [ ] **Step 1: Run all automated checks**

  ```bash
  bash scripts/validate-skills.sh
  bash tests/portable-skills.sh
  git diff --check HEAD~3..HEAD
  ```

  Expected: all commands exit zero.

- [ ] **Step 2: Exercise representative bundled scripts**

  Run the Windows/WSL converter cases and the QM validators/generators against
  their bundled example assets. Expected: zero exit status and no repository
  modifications.

- [ ] **Step 3: Inspect runtime discovery from a temporary install**

  Install into a temporary directory and compare the eleven installed skill
  names and file trees with the canonical source. Expected: exact match.

- [ ] **Step 4: Request independent code review**

  Ask a reviewer to check spec compliance first, then portability, deletion
  scope, shell safety, and documentation accuracy.

- [ ] **Step 5: Resolve findings and re-run verification**

  Apply only findings that trace to the approved goal; repeat every affected
  command before completion.
