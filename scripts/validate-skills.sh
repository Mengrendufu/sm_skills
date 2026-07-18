#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)}"
SKILLS_ROOT="$REPO_ROOT/skills"
errors=0
skill_count=0

report_error() {
    printf 'ERROR: %s\n' "$*" >&2
    errors=$((errors + 1))
}

if [[ ! -d "$SKILLS_ROOT" ]]; then
    printf 'ERROR: skills directory not found: %s\n' "$SKILLS_ROOT" >&2
    exit 1
fi

while IFS= read -r -d '' skill_dir; do
    skill_count=$((skill_count + 1))
    skill_name="${skill_dir##*/}"
    skill_file="$skill_dir/SKILL.md"

    if [[ "$skill_name" == *.BACKUP ]]; then
        report_error "$skill_name is a discoverable backup directory"
    fi

    if [[ ! "$skill_name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        report_error "$skill_name is not a valid Agent Skills directory name"
    fi

    if [[ ! -f "$skill_file" ]]; then
        report_error "$skill_name is missing SKILL.md"
        continue
    fi

    if [[ "$(sed -n '1p' "$skill_file")" != "---" ]]; then
        report_error "$skill_name/SKILL.md does not start with YAML frontmatter"
        continue
    fi

    frontmatter_end="$(awk 'NR > 1 && $0 == "---" { print NR; exit }' "$skill_file")"
    if [[ -z "$frontmatter_end" ]]; then
        report_error "$skill_name/SKILL.md has no closing frontmatter marker"
        continue
    fi

    declared_name="$(sed -n "2,$((frontmatter_end - 1))p" "$skill_file" \
        | sed -n 's/^name:[[:space:]]*//p' | head -n 1)"
    description="$(sed -n "2,$((frontmatter_end - 1))p" "$skill_file" \
        | sed -n 's/^description:[[:space:]]*//p' | head -n 1)"

    if [[ -z "$declared_name" ]]; then
        report_error "$skill_name/SKILL.md has no name field"
    elif [[ "$declared_name" != "$skill_name" ]]; then
        report_error "$declared_name does not match directory $skill_name"
    fi

    if [[ -z "$description" ]]; then
        report_error "$skill_name/SKILL.md has no description field"
    elif (( ${#description} > 1024 )); then
        report_error "$skill_name/SKILL.md description exceeds 1024 characters"
    fi

    if grep -RInIi -E \
        'opencode|codex|claude|\.config/opencode|\.codex|openai\.yaml|disable-model-invocation|CLAUDE_SKILL_DIR' \
        "$skill_dir" >"${TMPDIR:-/tmp}/portable-skill-runtime-match.$$"; then
        report_error "$skill_name contains agent-runtime-specific content"
        sed -n '1,20p' "${TMPDIR:-/tmp}/portable-skill-runtime-match.$$" >&2
    fi
    rm -f -- "${TMPDIR:-/tmp}/portable-skill-runtime-match.$$"

    while IFS= read -r resource_path; do
        [[ -n "$resource_path" ]] || continue
        if [[ ! -e "$skill_dir/$resource_path" ]]; then
            report_error "$skill_name/SKILL.md references missing $resource_path"
        fi
    done < <(grep -Eo '(scripts|references|assets)/[A-Za-z0-9_./-]*[A-Za-z0-9_]' "$skill_file" \
        | sort -u || true)

    if [[ -d "$skill_dir/scripts" ]]; then
        while IFS= read -r -d '' script_file; do
            if [[ ! -x "$script_file" ]]; then
                report_error "${script_file#"$REPO_ROOT/"} is not executable"
            fi
        done < <(find "$skill_dir/scripts" -type f -print0)
    fi

    if [[ -d "$skill_dir/agents" ]]; then
        report_error "$skill_name contains runtime UI metadata under agents/"
    fi
done < <(find "$SKILLS_ROOT" -mindepth 1 -maxdepth 1 -type d -print0)

if (( skill_count == 0 )); then
    report_error "no skills found under $SKILLS_ROOT"
fi

if (( errors > 0 )); then
    printf 'Validation failed: %d issue(s) across %d skill(s).\n' "$errors" "$skill_count" >&2
    exit 1
fi

printf 'Validated %d portable skill(s).\n' "$skill_count"
