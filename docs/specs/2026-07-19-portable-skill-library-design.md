# Portable Personal Agent Skills Library Design

## Goal

Turn this repository into the canonical, tool-neutral source for personal Agent
Skills that can be migrated into any compatible agent runtime.

## Boundary

- `skills/` owns reusable workflows, references, scripts, and assets.
- Agent runtimes consume copied skill directories but do not shape their content.
- `README.md` may document runtime-specific destination directories.
- Runtime configuration, plugins, agents, caches, and system skills stay outside
  this repository.

The dependency direction is one-way:

```text
portable skill library -> copied skill directory -> agent runtime loader
```

No skill may depend on the destination runtime's name, configuration layout, or
tool-specific frontmatter.

## Repository Shape

```text
.
├── AGENTS.md
├── README.md
├── docs/
│   ├── plans/
│   └── specs/
├── scripts/
│   ├── install-skills.sh
│   └── validate-skills.sh
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── assets/
│       ├── references/
│       └── scripts/
└── tests/
    └── portable-skills.sh
```

Only files required by a specific skill are kept below that skill directory.

## Portability Contract

Each skill must satisfy these rules:

1. The directory contains `SKILL.md` with standard `name` and `description`
   frontmatter.
2. The frontmatter name matches the directory name and uses lowercase letters,
   digits, and single hyphens.
3. Supporting files are referenced relative to the skill root.
4. Bundled scripts are executable and use documented external dependencies.
5. Skill content contains no Codex, OpenCode, Claude, or agent-specific install
   paths or frontmatter.
6. Example artifacts contain no personal agent configuration paths.
7. Machine-specific application defaults are allowed only when environment
   variables can override them; they are not agent-runtime dependencies.

## Canonical Skill Set

The initial library contains the eleven user-managed skills currently stored in
the local Codex user skill area:

- `design-by-contract`
- `grill-me`
- `grill-with-docs`
- `handoff`
- `obsidian-master`
- `plantuml-master`
- `qm-c-hsm-implementor`
- `qm-c-model-master`
- `strict-coding`
- `win-wsl-path-converter`
- `zoom-out`

Codex system skills, third-party plugin skills, and `agents/openai.yaml` metadata
are excluded because this repository does not own them.

## Migration Flow

`scripts/install-skills.sh <target-skills-directory> [skill ...]` copies all or
selected canonical skills. It mirrors each selected skill directory, including
removing obsolete files inside that selected destination, but never deletes
unselected target skills.

The caller owns selection of the destination directory. The installer contains
no built-in knowledge of any agent product.

## Validation

`scripts/validate-skills.sh` checks:

- required frontmatter and directory/name agreement;
- standard skill naming;
- supported file layout and executable scripts;
- absence of agent-runtime names, paths, metadata, and backup skill directories;
- absence of dangling relative resource references used by `SKILL.md`.

`tests/portable-skills.sh` verifies validation failures, full installation,
selected installation, exact replacement of one selected skill, and preservation
of unrelated target skills.

## Repository Cleanup

- Delete `opencode.jsonc` and the obsolete `agents/` tree.
- Delete the three `.BACKUP` skill directories, which are still discoverable as
  active skills by current OpenCode.
- Rewrite `README.md` around the portable library and migration workflow.
- Keep `AGENTS.md` only as tool-neutral repository maintenance guidance.

## Non-goals

- Do not deploy into any live agent configuration directory in this change.
- Do not vendor external plugins or system-provided skills.
- Do not make application-specific scripts portable beyond removing agent-runtime
  coupling.
- Do not rename the Git repository or remote.
