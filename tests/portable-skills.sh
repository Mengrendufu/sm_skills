#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
VALIDATOR="$REPO_ROOT/scripts/validate-skills.sh"
INSTALLER="$REPO_ROOT/scripts/install-skills.sh"

fail() {
    printf 'FAIL: %s\n' "$*" >&2
    exit 1
}

expect_success() {
    local label="$1"
    shift
    if ! "$@" >"$test_stdout" 2>"$test_stderr"; then
        printf 'FAIL: %s\n' "$label" >&2
        sed -n '1,120p' "$test_stdout" >&2
        sed -n '1,120p' "$test_stderr" >&2
        exit 1
    fi
}

expect_failure_containing() {
    local label="$1"
    local pattern="$2"
    shift 2
    if "$@" >"$test_stdout" 2>"$test_stderr"; then
        fail "$label unexpectedly succeeded"
    fi
    if ! grep -Fqi -- "$pattern" "$test_stdout" "$test_stderr"; then
        printf 'FAIL: %s did not report %q\n' "$label" "$pattern" >&2
        sed -n '1,120p' "$test_stdout" >&2
        sed -n '1,120p' "$test_stderr" >&2
        exit 1
    fi
}

make_fixture_repo() {
    local fixture_root="$1"

    mkdir -p \
        "$fixture_root/scripts" \
        "$fixture_root/skills/sample-skill/scripts" \
        "$fixture_root/skills/second-skill/references"

    cp "$VALIDATOR" "$INSTALLER" "$fixture_root/scripts/"

    cat >"$fixture_root/skills/sample-skill/SKILL.md" <<'EOF'
---
name: sample-skill
description: Use when a portable sample skill is needed for repository tests.
---

Run `scripts/check.sh`.
EOF
    cat >"$fixture_root/skills/sample-skill/scripts/check.sh" <<'EOF'
#!/usr/bin/env bash
printf 'ok\n'
EOF
    chmod +x "$fixture_root/skills/sample-skill/scripts/check.sh"

    cat >"$fixture_root/skills/second-skill/SKILL.md" <<'EOF'
---
name: second-skill
description: Use when a second portable fixture is required.
---

Read `references/details.md`.
EOF
    printf 'fixture reference\n' >"$fixture_root/skills/second-skill/references/details.md"
}

[[ -x "$VALIDATOR" ]] || fail "missing executable validator: $VALIDATOR"
[[ -x "$INSTALLER" ]] || fail "missing executable installer: $INSTALLER"

tmp_root="$(mktemp -d)"
trap 'rm -rf -- "$tmp_root"' EXIT
test_stdout="$tmp_root/stdout"
test_stderr="$tmp_root/stderr"

fixture_repo="$tmp_root/fixture repo"
make_fixture_repo "$fixture_repo"

expect_success \
    "valid fixture repository" \
    "$fixture_repo/scripts/validate-skills.sh" "$fixture_repo"

printf '\nOpenCode-only instruction\n' >>"$fixture_repo/skills/sample-skill/SKILL.md"
expect_failure_containing \
    "runtime-specific content" \
    "agent-runtime-specific" \
    "$fixture_repo/scripts/validate-skills.sh" "$fixture_repo"
sed -i '$d' "$fixture_repo/skills/sample-skill/SKILL.md"

chmod -x "$fixture_repo/skills/sample-skill/scripts/check.sh"
expect_failure_containing \
    "non-executable bundled script" \
    "not executable" \
    "$fixture_repo/scripts/validate-skills.sh" "$fixture_repo"
chmod +x "$fixture_repo/skills/sample-skill/scripts/check.sh"

mkdir -p "$fixture_repo/skills/sample-skill/scripts/__pycache__"
printf 'generated OpenCode bytecode\n' >"$fixture_repo/skills/sample-skill/scripts/__pycache__/check.pyc"
expect_success \
    "generated Python cache is not a bundled script" \
    "$fixture_repo/scripts/validate-skills.sh" "$fixture_repo"

mv "$fixture_repo/skills/second-skill" "$fixture_repo/skills/wrong-directory"
expect_failure_containing \
    "frontmatter and directory mismatch" \
    "does not match directory" \
    "$fixture_repo/scripts/validate-skills.sh" "$fixture_repo"
mv "$fixture_repo/skills/wrong-directory" "$fixture_repo/skills/second-skill"

install_target="$tmp_root/installed skills"
mkdir -p \
    "$install_target/unrelated-skill" \
    "$install_target/sample-skill/scripts/__pycache__"
printf 'preserve\n' >"$install_target/unrelated-skill/data.txt"
printf 'stale\n' >"$install_target/sample-skill/stale.txt"
printf 'stale bytecode\n' >"$install_target/sample-skill/scripts/__pycache__/stale.pyc"

expect_success \
    "install all fixture skills" \
    "$fixture_repo/scripts/install-skills.sh" "$install_target"

[[ ! -e "$install_target/sample-skill/stale.txt" ]] || fail "selected skill kept a stale file"
[[ -f "$install_target/unrelated-skill/data.txt" ]] || fail "installer deleted an unrelated target skill"
[[ ! -e "$install_target/sample-skill/scripts/__pycache__" ]] || fail "installer copied Python cache files"
diff -qr --exclude='__pycache__' --exclude='*.py[co]' \
    "$fixture_repo/skills/sample-skill" "$install_target/sample-skill" >/dev/null \
    || fail "sample-skill install is not an exact mirror"
diff -qr "$fixture_repo/skills/second-skill" "$install_target/second-skill" >/dev/null \
    || fail "second-skill install is not an exact mirror"

selected_target="$tmp_root/selected skills"
expect_success \
    "install one selected skill" \
    "$fixture_repo/scripts/install-skills.sh" "$selected_target" second-skill
[[ -d "$selected_target/second-skill" ]] || fail "selected skill was not installed"
[[ ! -e "$selected_target/sample-skill" ]] || fail "unselected skill was installed"

atomic_target="$tmp_root/atomic skills"
mkdir -p "$atomic_target/unrelated-skill"
printf 'preserve\n' >"$atomic_target/unrelated-skill/data.txt"
expect_failure_containing \
    "reject invalid selection before copying" \
    "unknown skill" \
    "$fixture_repo/scripts/install-skills.sh" "$atomic_target" second-skill missing-skill
[[ ! -e "$atomic_target/second-skill" ]] || fail "installer partially copied a validated skill"
[[ -f "$atomic_target/unrelated-skill/data.txt" ]] || fail "failed install changed unrelated skill"

expect_failure_containing \
    "reject filesystem root target" \
    "unsafe target" \
    "$fixture_repo/scripts/install-skills.sh" /

if [[ "${1:-}" != "--tooling-only" ]]; then
    expect_success "canonical repository validation" "$VALIDATOR" "$REPO_ROOT"
fi

printf 'PASS: portable skill tooling and repository checks\n'
