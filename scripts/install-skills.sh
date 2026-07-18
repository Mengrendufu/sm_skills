#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'usage: %s <target-skills-directory> [skill ...]\n' "${0##*/}" >&2
    exit 2
}

[[ $# -ge 1 ]] || usage
command -v rsync >/dev/null 2>&1 || {
    printf 'ERROR: rsync is required\n' >&2
    exit 1
}

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
SOURCE_ROOT="$REPO_ROOT/skills"
TARGET_ARG="$1"
shift

[[ -n "$TARGET_ARG" ]] || usage
TARGET_ROOT="$(realpath -m -- "$TARGET_ARG")"
HOME_ROOT="$(realpath -m -- "$HOME")"

case "$TARGET_ROOT" in
    /|"$HOME_ROOT"|"$REPO_ROOT"|"$SOURCE_ROOT")
        printf 'ERROR: unsafe target skills directory: %s\n' "$TARGET_ROOT" >&2
        exit 1
        ;;
esac

"$SCRIPT_DIR/validate-skills.sh" "$REPO_ROOT" >/dev/null

skills=()
if (( $# == 0 )); then
    while IFS= read -r -d '' source_dir; do
        [[ -f "$source_dir/SKILL.md" ]] || continue
        skills+=("${source_dir##*/}")
    done < <(find "$SOURCE_ROOT" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
else
    skills=("$@")
fi

(( ${#skills[@]} > 0 )) || {
    printf 'ERROR: no skills selected\n' >&2
    exit 1
}

mkdir -p -- "$TARGET_ROOT"

for skill_name in "${skills[@]}"; do
    if [[ ! "$skill_name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        printf 'ERROR: invalid skill name: %s\n' "$skill_name" >&2
        exit 1
    fi

    source_dir="$SOURCE_ROOT/$skill_name"
    target_dir="$TARGET_ROOT/$skill_name"

    if [[ ! -f "$source_dir/SKILL.md" ]]; then
        printf 'ERROR: unknown skill: %s\n' "$skill_name" >&2
        exit 1
    fi
    if [[ -L "$target_dir" ]]; then
        printf 'ERROR: refusing to replace symlinked skill directory: %s\n' "$target_dir" >&2
        exit 1
    fi
    if [[ -e "$target_dir" && ! -d "$target_dir" ]]; then
        printf 'ERROR: target skill path is not a directory: %s\n' "$target_dir" >&2
        exit 1
    fi

    mkdir -p -- "$target_dir"
    rsync -a --delete \
        --exclude='__pycache__/' \
        --exclude='*.pyc' \
        --exclude='*.pyo' \
        -- "$source_dir/" "$target_dir/"
    printf 'Installed %s -> %s\n' "$skill_name" "$target_dir"
done
