---
name: obsidian-master
description: Interact with an Obsidian vault through a configurable local CLI wrapper. Use when an agent needs to locate a vault, create, read, append, prepend, move, delete, search, or organize notes with exact path control.
---

# Obsidian Master

## Goal

Route note operations through the bundled wrapper without embedding any user's executable, configuration, or vault paths.

## Environment Contract

- `OBSIDIAN_CLI`: Obsidian CLI executable path or command name. Defaults to `obsidian` on `PATH`.
- `OBSIDIAN_VAULT`: Optional vault root or subfolder. Invalid explicit values fail; they never fall back to another vault.
- `OBSIDIAN_VAULT_NAME`: Optional Obsidian vault name or id. Defaults to the discovered vault directory name.
- `OBSIDIAN_PATH_PREFIX`: Optional vault-relative prefix for note targets.
- `OBSIDIAN_PATH_CONVERTER`: Optional executable path or command name that accepts one path and prints the path syntax used by the current Bash environment.

`OBSIDIAN_CLI` must identify one executable that accepts the official Obsidian CLI arguments. If a platform launcher needs prefix arguments, point `OBSIDIAN_CLI` to a local adapter executable rather than embedding shell syntax in the variable.

## Workflow

1. Resolve `<skill-dir>` as the directory containing this `SKILL.md`.
2. Configure `OBSIDIAN_CLI` and, when discovery is insufficient, `OBSIDIAN_VAULT`.
3. Run commands through `<skill-dir>/scripts/obsidian-local.sh`.
4. Prefer exact note targets with `path=`.
5. Use `search` before `create` when duplicates are plausible.
6. Route command-shape questions to `references/official-cli-patterns.md`.
7. Verify the configured CLI with `version` when needed.

## Vault Discovery

The wrapper discovers the vault in this order:

1. `OBSIDIAN_VAULT`.
2. Absolute `path=`, `to=`, or `folder=` arguments by walking upward to `.obsidian`.
3. The current working directory by walking upward to `.obsidian`.

The wrapper never guesses user directories, application configuration paths, or common vault names. Commands that do not require a discovered vault, such as `version` and `help`, still run.

When a target path is absolute and inside the vault, the wrapper rewrites it to a vault-relative path. When the working directory or `OBSIDIAN_VAULT` is a subfolder, relative note paths are prefixed from the real vault root.

Paths must use the syntax understood by the current Bash environment. Set `OBSIDIAN_PATH_CONVERTER` when callers provide foreign path syntax, such as Windows paths from WSL. Foreign paths fail clearly when no converter is configured.

## Do

- Keep machine-specific values in environment configuration, not in this skill.
- Use `bash "<skill-dir>/scripts/obsidian-local.sh" ...`.
- Use official CLI `key=value` argument style.
- Prefer `path=` when the target note must be exact.
- Use `append` or `prepend` for deterministic updates.
- Use `\\n` escapes for multi-line content.

## Do Not

- Do not call a platform-specific Obsidian path directly from the workflow.
- Do not rely on the active note unless the user explicitly asks for it.
- Do not guess a vault or silently recover from an invalid `OBSIDIAN_VAULT`.
- Do not place shell pipelines or prefix arguments in `OBSIDIAN_CLI`.

## Resources

- Wrapper: `scripts/obsidian-local.sh`
- Patterns: `references/official-cli-patterns.md`
- Tests: `tests/obsidian-local-test.sh`

## Validation

```bash
bash "<skill-dir>/scripts/obsidian-local.sh" version
bash "<skill-dir>/tests/obsidian-local-test.sh"
```

## Limits

- Requires Bash, GNU `realpath`, and an Obsidian CLI executable compatible with the official CLI.
- Keep command details in `references/` and execution behavior in `scripts/`.
