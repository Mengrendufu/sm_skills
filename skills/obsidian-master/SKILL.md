---
name: obsidian-master
description: Interact with an Obsidian vault through the local CLI wrapper in this WSL environment. Use when an agent needs to locate the active vault, create, read, append, prepend, move, delete, search, or organize notes with exact path control.
---

# Obsidian Master

## Goal

Route note operations through the local Obsidian CLI wrapper and avoid guessing the vault root.

## Workflow

1. Resolve `<skill-dir>` as the directory containing this `SKILL.md`, then run Obsidian commands through `<skill-dir>/scripts/obsidian-local.sh`.
2. Let the wrapper auto-discover the vault unless the user explicitly provides `OBSIDIAN_VAULT` or `vault=`.
3. Prefer exact note targets with `path=`.
4. Route command-shape questions to `references/official-cli-patterns.md`.
5. Use `search` before `create` when duplicates are plausible.
6. Verify wrapper availability with `version` when needed.

## Vault Discovery

The wrapper discovers the vault in this order:

1. `OBSIDIAN_VAULT`, if the environment variable is set.
2. Absolute `path=`, `to=`, or `folder=` arguments by walking upward to `.obsidian`.
3. The current working directory by walking upward to `.obsidian`.
4. Obsidian's Windows app config at `%APPDATA%/obsidian/obsidian.json`, using the most recently opened vault id.
5. Known local fallback paths.

When a target path is absolute and inside the vault, the wrapper rewrites it to a vault-relative path. When the working directory or `OBSIDIAN_VAULT` is a subfolder inside a vault, relative note paths are prefixed from the real vault root.

## Do

- Use `bash "<skill-dir>/scripts/obsidian-local.sh" ...` after resolving `<skill-dir>` from the loaded skill path.
- Use official CLI `key=value` argument style.
- Prefer `path=` when the target note must be exact.
- Use `append` or `prepend` for deterministic note updates.
- Use `create` for standalone notes.
- Use `\\n` escapes for multi-line content.
- Let the wrapper normalize Windows paths, vault-relative paths, and vault discovery.

## Do Not

- Do not call `obsidian`, `Obsidian.com`, or `cmd.exe` directly unless debugging the wrapper.
- Do not rely on the active note unless the user explicitly asks for it.
- Do not guess vault-relative paths outside the vault root.
- Do not improvise CLI syntax when `references/official-cli-patterns.md` can answer it.

## Resources

- Wrapper: `scripts/obsidian-local.sh`
- Patterns: `references/official-cli-patterns.md`

## Validation

```bash
bash "<skill-dir>/scripts/obsidian-local.sh" version
```

## Limits

- Keep `SKILL.md` focused on routing and wrapper usage.
- Keep command details in `references/` and execution behavior in `scripts/`.
