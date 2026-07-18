#!/usr/bin/env bash
set -euo pipefail

OBSIDIAN_EXE="${OBSIDIAN_EXE:-/mnt/c/mengrendufu/software_ins/obisidian/Obsidian/Obsidian.com}"
OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-}"
OBSIDIAN_VAULT_NAME="${OBSIDIAN_VAULT_NAME:-}"
OBSIDIAN_PATH_PREFIX="${OBSIDIAN_PATH_PREFIX:-}"
CMD_EXE="${CMD_EXE:-/mnt/c/Windows/System32/cmd.exe}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
SKILLS_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd -P)"
WINDOWS_PATH_CONVERTER="${WINDOWS_PATH_CONVERTER:-$SKILLS_ROOT/win-wsl-path-converter/scripts/convert_windows_path.sh}"

normalize_path_arg() {
    local value="$1"
    local converted

    if [[ -x "$WINDOWS_PATH_CONVERTER" ]]; then
        if converted="$(bash "$WINDOWS_PATH_CONVERTER" "$value")"; then
            printf '%s\n' "$converted"
            return 0
        fi
        return 1
    fi

    printf '%s\n' "$value"
}

find_vault_root() {
    local dir="$1"

    [[ -n "$dir" ]] || return 1
    [[ "$dir" == /* ]] || return 1

    if [[ ! -d "$dir" ]]; then
        dir="$(dirname "$dir")"
    fi

    dir="$(realpath -m "$dir")"
    while [[ -n "$dir" && "$dir" != "/" ]]; do
        if [[ -d "$dir/.obsidian" ]]; then
            printf '%s\n' "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

obsidian_config_vaults() {
    local config
    local configs=(
        "/mnt/c/Users/1/AppData/Roaming/obsidian/obsidian.json"
        "/mnt/c/Users/1/AppData/Roaming/Obsidian/obsidian.json"
    )

    for config in "${configs[@]}"; do
        [[ -f "$config" ]] || continue
        python3 - "$config" <<'PY'
import json
import sys
from pathlib import Path

config = Path(sys.argv[1])
try:
    data = json.loads(config.read_text(encoding="utf-8"))
except Exception:
    raise SystemExit(0)

items = []
for vault_id, vault in (data.get("vaults") or {}).items():
    if not isinstance(vault, dict):
        continue
    path = vault.get("path")
    if not path:
        continue
    open_rank = 0 if vault.get("open") else 1
    try:
        ts_rank = -int(vault.get("ts") or 0)
    except Exception:
        ts_rank = 0
    items.append((open_rank, ts_rank, str(vault_id), str(path)))

seen = set()
for _, _, vault_id, path in sorted(items):
    key = (vault_id, path)
    if key in seen:
        continue
    seen.add(key)
    print(f"{vault_id}\t{path}")
PY
    done
}

arg_candidate_paths() {
    local arg
    local raw
    local normalized

    for arg in "$@"; do
        case "$arg" in
            path=*|to=*|folder=*)
                raw="${arg#*=}"
                if normalized="$(normalize_path_arg "$raw" 2>/dev/null)" && [[ "$normalized" == /* ]]; then
                    printf '_\t%s\n' "$normalized"
                fi
                ;;
        esac
    done
}

try_vault_candidate() {
    local source="$1"
    local vault_id="$2"
    local raw_path="$3"
    local normalized
    local root

    [[ -n "$raw_path" ]] || return 1

    if ! normalized="$(normalize_path_arg "$raw_path" 2>/dev/null)"; then
        return 1
    fi

    if [[ "$normalized" != /* ]]; then
        return 1
    fi

    if ! root="$(find_vault_root "$normalized")"; then
        return 1
    fi

    vault_root="$root"
    vault_source="$source"
    vault_source_path="$normalized"

    if [[ -z "$OBSIDIAN_VAULT_NAME" && -n "$vault_id" && "$vault_id" != "_" ]]; then
        OBSIDIAN_VAULT_NAME="$vault_id"
    fi

    return 0
}

discover_vault() {
    local line
    local vault_id
    local path
    local pwd_path
    local common
    local config_lines=()

    if [[ -n "$OBSIDIAN_VAULT" ]] && try_vault_candidate "env" "" "$OBSIDIAN_VAULT"; then
        return 0
    fi

    while IFS=$'\t' read -r vault_id path; do
        if try_vault_candidate "arg" "$vault_id" "$path"; then
            return 0
        fi
    done < <(arg_candidate_paths "${args[@]}")

    pwd_path="$(pwd -P)"
    if try_vault_candidate "cwd" "" "$pwd_path"; then
        return 0
    fi

    mapfile -t config_lines < <(obsidian_config_vaults)
    for line in "${config_lines[@]}"; do
        IFS=$'\t' read -r vault_id path <<< "$line"
        if try_vault_candidate "obsidian-config" "$vault_id" "$path"; then
            return 0
        fi
    done

    for common in \
        "/mnt/c/mengrendufu/workshop/obsidian" \
        "/mnt/c/Users/1/Documents/Obsidian Vault" \
        "/mnt/c/Users/1/Documents/Obsidian" \
        "/mnt/c/Users/1/OneDrive/Documents/Obsidian Vault" \
        "$HOME/Obsidian" \
        "$HOME/obsidian"
    do
        if try_vault_candidate "fallback" "" "$common"; then
            return 0
        fi
    done

    return 1
}

relativize_to_vault_if_needed() {
    local value="$1"
    local root="$2"
    local root_abs
    local value_abs
    local relative

    if [[ -z "$root" || "$value" != /* ]]; then
        printf '%s\n' "$value"
        return 0
    fi

    root_abs="$(realpath -m "$root")"
    value_abs="$(realpath -m "$value")"
    relative="$(realpath -m --relative-to="$root_abs" "$value_abs")"

    case "$relative" in
        ..|../*)
            printf 'obsidian-local.sh: absolute note path is outside the vault root: %s\n' "$value" >&2
            return 1
            ;;
        *)
            printf '%s\n' "$relative"
            ;;
    esac
}

rewrite_note_target() {
    local raw="$1"
    local root="$2"
    local prefix="$3"
    local normalized

    if ! normalized="$(normalize_path_arg "$raw")"; then
        return 1
    fi

    if [[ "$normalized" == /* ]]; then
        relativize_to_vault_if_needed "$normalized" "$root"
        return 0
    fi

    prefix_if_needed "$normalized" "$prefix"
}

prefix_if_needed() {
    local value="$1"
    local prefix="$2"

    if [[ -z "$prefix" ]]; then
        printf '%s\n' "$value"
        return 0
    fi

    case "$value" in
        /*|./*|../*)
            printf '%s\n' "$value"
            ;;
        "$prefix"|"$prefix"/*)
            printf '%s\n' "$value"
            ;;
        *)
            printf '%s/%s\n' "$prefix" "$value"
            ;;
    esac
}

vault_root=""
vault_source=""
vault_source_path=""
path_prefix=""
args=("$@")

if discover_vault; then
    cd "$vault_root"

    if [[ -z "$OBSIDIAN_VAULT_NAME" ]]; then
        OBSIDIAN_VAULT_NAME="$(basename "$vault_root")"
    fi

    path_prefix="$OBSIDIAN_PATH_PREFIX"

    if [[ -z "$path_prefix" && ( "$vault_source" == "env" || "$vault_source" == "cwd" ) ]]; then
        if [[ -d "$vault_source_path" && "$vault_source_path" != "$vault_root" ]]; then
            path_prefix="$(realpath -m --relative-to="$vault_root" "$vault_source_path")"
        fi
    fi
else
    path_prefix="$OBSIDIAN_PATH_PREFIX"
fi

has_vault_arg=0
for arg in "${args[@]}"; do
    if [[ "$arg" == vault=* ]]; then
        has_vault_arg=1
        break
    fi
done

rewritten_args=()
if [[ -n "$OBSIDIAN_VAULT_NAME" && $has_vault_arg -eq 0 ]]; then
    rewritten_args+=("vault=$OBSIDIAN_VAULT_NAME")
fi

for arg in "${args[@]}"; do
    case "$arg" in
        path=*)
            if ! target="$(rewrite_note_target "${arg#path=}" "$vault_root" "$path_prefix")"; then
                exit 1
            fi
            rewritten_args+=("path=$target")
            ;;
        to=*)
            if ! target="$(rewrite_note_target "${arg#to=}" "$vault_root" "$path_prefix")"; then
                exit 1
            fi
            rewritten_args+=("to=$target")
            ;;
        folder=*)
            if ! target="$(rewrite_note_target "${arg#folder=}" "$vault_root" "$path_prefix")"; then
                exit 1
            fi
            rewritten_args+=("folder=$target")
            ;;
        *)
            rewritten_args+=("$arg")
            ;;
    esac
done

if [[ -x "$OBSIDIAN_EXE" ]]; then
    exec "$OBSIDIAN_EXE" "${rewritten_args[@]}"
fi

if [[ -x "$CMD_EXE" ]]; then
    exec "$CMD_EXE" /d /c obsidian "${rewritten_args[@]}"
fi

printf 'obsidian-local.sh: could not find Obsidian.com or cmd.exe\n' >&2
exit 127
