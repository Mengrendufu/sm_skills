#!/usr/bin/env bash
set -euo pipefail

if [[ $# -gt 1 ]]; then
    printf 'usage: %s <path>\n' "${0##*/}" >&2
    exit 2
fi

if [[ $# -eq 1 ]]; then
    raw="$1"
else
    IFS= read -r raw || true
fi

if [[ -z "${raw:-}" ]]; then
    printf 'no path provided\n' >&2
    exit 2
fi

strip_outer_quotes() {
    local s="$1"
    if [[ "$s" =~ ^\".*\"$ ]] || [[ "$s" =~ ^\'.*\'$ ]]; then
        s="${s:1:${#s}-2}"
    fi
    printf '%s\n' "$s"
}

path="$(strip_outer_quotes "$raw")"

if [[ "$path" == /* ]]; then
    printf '%s\n' "$path"
    exit 0
fi

if [[ "$path" =~ ^\\\\wsl(\.localhost)?\$?\\[^\\]+\\(.*)$ ]]; then
    rest="${BASH_REMATCH[2]}"
    printf '/%s\n' "${rest//\\//}"
    exit 0
fi

if [[ "$path" =~ ^[A-Za-z]:(\\|/).* ]]; then
    if out="$(wslpath "$path" 2>/dev/null)"; then
        printf '%s\n' "$out"
        exit 0
    fi
    printf 'wslpath failed for drive-letter path; the drive may be unavailable or unmounted in this WSL environment: %s\n' "$path" >&2
    exit 1
fi

if [[ "$path" =~ ^\\\\ ]]; then
    printf 'unsupported UNC path in this environment: %s\n' "$path" >&2
    exit 1
fi

printf '%s\n' "$path"
