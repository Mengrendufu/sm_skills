# Official CLI Patterns

Reference: https://obsidian.md/help/cli

This file keeps only the command patterns most useful for agent work.

Resolve `SKILL_DIR` as the directory containing the active `obsidian-master/SKILL.md`. Configure machine-specific values through the environment contract in `SKILL.md`.

## Syntax

- Parameters use `key=value`
- Flags are bare words
- `vault=<name-or-id>` comes before the command
- Quote values with spaces
- Use `\n` in multiline content
- The wrapper discovers the vault from `OBSIDIAN_VAULT`, absolute note targets, then the current directory.
- `OBSIDIAN_VAULT` may point to a vault root or subfolder; subfolder targets are prefixed relative to the real vault root.
- Set `OBSIDIAN_PATH_CONVERTER` when incoming paths use syntax foreign to the current Bash environment. The converter accepts one path and prints its normalized form.

## Environment examples

Use values appropriate to the current machine:

```bash
export OBSIDIAN_CLI="/path/to/obsidian-cli"
export OBSIDIAN_VAULT="/path/to/vault"
export OBSIDIAN_VAULT_NAME="vault-name-or-id"
```

When the `obsidian` command is already on `PATH`, omit `OBSIDIAN_CLI`. When commands run from inside the target vault, omit `OBSIDIAN_VAULT`.

If a platform launcher requires prefix arguments, create a local adapter executable and set `OBSIDIAN_CLI` to that adapter. Do not put shell syntax in `OBSIDIAN_CLI`.

## General

```bash
bash "$SKILL_DIR/scripts/obsidian-local.sh" help
bash "$SKILL_DIR/scripts/obsidian-local.sh" help create
bash "$SKILL_DIR/scripts/obsidian-local.sh" version
```

## Daily notes

```bash
bash "$SKILL_DIR/scripts/obsidian-local.sh" daily
bash "$SKILL_DIR/scripts/obsidian-local.sh" daily:path
bash "$SKILL_DIR/scripts/obsidian-local.sh" daily:read
bash "$SKILL_DIR/scripts/obsidian-local.sh" daily:append content="..."
bash "$SKILL_DIR/scripts/obsidian-local.sh" daily:prepend content="..."
```

## File operations

```bash
bash "$SKILL_DIR/scripts/obsidian-local.sh" create path="Folder/Note.md" content="# Title\n\nBody"
bash "$SKILL_DIR/scripts/obsidian-local.sh" read path="Folder/Note.md"
bash "$SKILL_DIR/scripts/obsidian-local.sh" append path="Folder/Note.md" content="\n## Update\n- Item"
bash "$SKILL_DIR/scripts/obsidian-local.sh" move path="Folder/Old.md" to="Folder/New.md"
bash "$SKILL_DIR/scripts/obsidian-local.sh" delete path="Folder/Note.md"
```

Prefer `path=` over `file=` in automation.

## Search

```bash
bash "$SKILL_DIR/scripts/obsidian-local.sh" search query="rust ownership" format=json
bash "$SKILL_DIR/scripts/obsidian-local.sh" search:context query="borrow checker"
bash "$SKILL_DIR/scripts/obsidian-local.sh" search:open query="ownership"
```

## Tasks and tags

```bash
bash "$SKILL_DIR/scripts/obsidian-local.sh" tasks
bash "$SKILL_DIR/scripts/obsidian-local.sh" tasks daily
bash "$SKILL_DIR/scripts/obsidian-local.sh" tags
bash "$SKILL_DIR/scripts/obsidian-local.sh" tags counts
```
