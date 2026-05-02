# Official CLI Patterns

Reference: https://obsidian.md/help/cli

This file keeps only the command patterns most useful for agent work.

## Syntax

- Parameters use `key=value`
- Flags are bare words
- `vault=<name-or-id>` comes before the command
- Quote values with spaces
- Use `\n` in multiline content
- The local wrapper auto-discovers the vault from `OBSIDIAN_VAULT`, absolute note targets, current directory, Obsidian's Windows app config, then known fallback paths.
- In this local wrapper, `OBSIDIAN_VAULT` may point to a vault root or a subfolder inside a vault; when it points at a subfolder, `path=`, `to=`, and `folder=` are prefixed automatically relative to the real vault root.
- In this local wrapper, Windows-style values passed through `OBSIDIAN_VAULT`, `path=`, `to=`, or `folder=` are converted before use by the local path-conversion helper. Absolute targets inside the vault are converted back to vault-relative paths. Unsupported UNC inputs and targets outside the vault fail fast.

## General

```bash
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh help
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh help create
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh version
```

## Daily notes

```bash
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh daily
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh daily:path
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh daily:read
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh daily:append content="..."
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh daily:prepend content="..."
```

## File operations

```bash
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh create path="Folder/Note.md" content="# Title\n\nBody"
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh read path="Folder/Note.md"
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh append path="Folder/Note.md" content="\n## Update\n- Item"
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh move path="Folder/Old.md" to="Folder/New.md"
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh delete path="Folder/Note.md"
```

Prefer `path=` over `file=` in automation.

## Search

```bash
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh search query="rust ownership" format=json
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh search:context query="borrow checker"
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh search:open query="ownership"
```

## Tasks and tags

```bash
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh tasks
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh tasks daily
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh tags
bash /home/sunnymatato/.config/opencode/skills/obsidian-master/scripts/obsidian-local.sh tags counts
```
