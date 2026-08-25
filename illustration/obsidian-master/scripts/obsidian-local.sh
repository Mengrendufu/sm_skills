#!/usr/bin/env bash
set -euo pipefail

OBSIDIAN_CLI="${OBSIDIAN_CLI:-obsidian}"
OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-}"
OBSIDIAN_VAULT_NAME="${OBSIDIAN_VAULT_NAME:-}"
OBSIDIAN_PATH_PREFIX="${OBSIDIAN_PATH_PREFIX:-}"
OBSIDIAN_PATH_CONVERTER="${OBSIDIAN_PATH_CONVERTER:-}"

resolve_command() {
    local candidate="$1"
    local variable_name="$2"

    if [[ "$candidate" == */* ]]; then
        if [[ ! -x "$candidate" ]]; then
            printf 'obsidian-local.sh: %s is not executable: %s\n' "$variable_name" "$candidate" >&2
            return 127
        fi
        printf '%s\n' "$candidate"
        return 0
    fi

    if ! command -v "$candidate"; then
        printf 'obsidian-local.sh: %s command not found: %s\n' "$variable_name" "$candidate" >&2
        return 127
    fi
}

path_converter=""
if [[ -n "$OBSIDIAN_PATH_CONVERTER" ]]; then
    path_converter="$(resolve_command "$OBSIDIAN_PATH_CONVERTER" "OBSIDIAN_PATH_CONVERTER")" || exit $?
fi

normalize_path_arg() {
    local value="$1"
    local converted

    if [[ -n "$path_converter" ]]; then
        if converted="$("$path_converter" "$value")"; then
            printf '%s\n' "$converted"
            return 0
        fi
        return 1
    fi
    case "$value" in
        [A-Za-z]:\\*|[A-Za-z]:/*|\\\\*)
            printf 'obsidian-local.sh: foreign path requires OBSIDIAN_PATH_CONVERTER: %s\n' "$value" >&2
            return 2
            ;;
    esac

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
    local vault_id
    local path
    local pwd_path
    local explicit_vault

    if [[ -n "$OBSIDIAN_VAULT" ]]; then
        if ! explicit_vault="$(normalize_path_arg "$OBSIDIAN_VAULT")"; then
            return 2
        fi
        if try_vault_candidate "env" "" "$explicit_vault"; then
            return 0
        fi
        printf 'obsidian-local.sh: OBSIDIAN_VAULT does not identify an Obsidian vault: %s\n' "$OBSIDIAN_VAULT" >&2
        return 2
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
    discovery_status=$?
    if [[ $discovery_status -eq 2 ]]; then
        exit 2
    fi
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

obsidian_cli="$(resolve_command "$OBSIDIAN_CLI" "OBSIDIAN_CLI")" || exit $?

exec "$obsidian_cli" "${rewritten_args[@]}"
