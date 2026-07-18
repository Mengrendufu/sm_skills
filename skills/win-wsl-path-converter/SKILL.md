---
name: win-wsl-path-converter
description: Convert Windows absolute paths into WSL paths. Use when a user pastes `C:\\...`, `D:\\...`, or WSL UNC-style Windows paths and the path must be used in shell commands, file operations, or local file links.
---

# Win WSL Path Converter

## Goal

Route Windows path conversion through the local script.

## Workflow

1. Run `scripts/convert_windows_path.sh` with the raw path.
2. Use the returned path directly on success.
3. If the script fails, report the specific reason instead of guessing.

## Do

- Prefer the script over ad hoc reasoning.
- Pass the raw user path, including quotes if present.
- Accept `/...` paths unchanged when the script does.
- Let the script handle drive-letter paths and WSL UNC forms.

## Do Not

- Do not invent a path when the script fails.
- Do not guess generic UNC shares.
- Do not guess non-mounted drive behavior.

## Resource

- Script: `scripts/convert_windows_path.sh`

## Validation

```bash
bash "<skill-dir>/scripts/convert_windows_path.sh" '<path>'
```

## Limits

- Keep `SKILL.md` focused on routing to the converter script.
