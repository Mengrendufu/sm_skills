#!/usr/bin/env bash
set -euo pipefail

unset OBSIDIAN_CLI OBSIDIAN_VAULT OBSIDIAN_VAULT_NAME OBSIDIAN_PATH_PREFIX OBSIDIAN_PATH_CONVERTER

TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
WRAPPER="$TEST_DIR/../scripts/obsidian-local.sh"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

fail() {
    printf 'FAIL: %s\n' "$1" >&2
    exit 1
}

assert_file_equals() {
    local expected="$1"
    local actual_file="$2"
    local actual

    [[ -f "$actual_file" ]] || fail "missing output file: $actual_file"
    actual="$(cat "$actual_file")"
    [[ "$actual" == "$expected" ]] || fail "expected [$expected], got [$actual]"
}

FAKE_CLI="$TMP_DIR/fake-obsidian"
cat > "$FAKE_CLI" <<'FAKE'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$PWD" > "$CAPTURE_CWD"
printf '%s\n' "$@" > "$CAPTURE_ARGS"
FAKE
chmod +x "$FAKE_CLI"

VAULT="$TMP_DIR/Portable Vault"
mkdir -p "$VAULT/.obsidian" "$VAULT/Folder"

CAPTURE_CWD="$TMP_DIR/cwd" \
CAPTURE_ARGS="$TMP_DIR/args" \
OBSIDIAN_CLI="$FAKE_CLI" \
OBSIDIAN_VAULT="$VAULT" \
OBSIDIAN_VAULT_NAME="portable-vault" \
bash "$WRAPPER" read path="Folder/Note.md"

assert_file_equals "$VAULT" "$TMP_DIR/cwd"
assert_file_equals $'vault=portable-vault\nread\npath=Folder/Note.md' "$TMP_DIR/args"
printf 'PASS: explicit CLI and vault environment\n'

if CAPTURE_CWD="$TMP_DIR/invalid-cwd" \
    CAPTURE_ARGS="$TMP_DIR/invalid-args" \
    OBSIDIAN_CLI="$FAKE_CLI" \
    OBSIDIAN_VAULT="$TMP_DIR/missing-vault" \
    bash "$WRAPPER" read path="Note.md" 2>"$TMP_DIR/invalid-error"
then
    fail "invalid OBSIDIAN_VAULT was accepted"
fi

assert_file_equals \
    "obsidian-local.sh: OBSIDIAN_VAULT does not identify an Obsidian vault: $TMP_DIR/missing-vault" \
    "$TMP_DIR/invalid-error"
[[ ! -e "$TMP_DIR/invalid-args" ]] || fail "CLI ran for invalid OBSIDIAN_VAULT"
printf 'PASS: invalid explicit vault fails without fallback\n'

FAKE_CONVERTER="$TMP_DIR/fake-path-converter"
cat > "$FAKE_CONVERTER" <<'CONVERTER'
#!/usr/bin/env bash
set -euo pipefail
case "$1" in
    'Q:\Portable Vault')
        printf '%s\n' "$CONVERTER_VAULT"
        ;;
    'Q:\Portable Vault\Folder\Note.md')
        printf '%s/Folder/Note.md\n' "$CONVERTER_VAULT"
        ;;
    *)
        printf '%s\n' "$1"
        ;;
esac
CONVERTER
chmod +x "$FAKE_CONVERTER"

CAPTURE_CWD="$TMP_DIR/converted-cwd" \
CAPTURE_ARGS="$TMP_DIR/converted-args" \
CONVERTER_VAULT="$VAULT" \
OBSIDIAN_CLI="$FAKE_CLI" \
OBSIDIAN_VAULT='Q:\Portable Vault' \
OBSIDIAN_VAULT_NAME="converted-vault" \
OBSIDIAN_PATH_CONVERTER="$FAKE_CONVERTER" \
bash "$WRAPPER" read path='Q:\Portable Vault\Folder\Note.md'

assert_file_equals "$VAULT" "$TMP_DIR/converted-cwd"
assert_file_equals $'vault=converted-vault\nread\npath=Folder/Note.md' "$TMP_DIR/converted-args"
printf 'PASS: injected path converter handles foreign paths\n'

if CAPTURE_CWD="$TMP_DIR/foreign-cwd" \
    CAPTURE_ARGS="$TMP_DIR/foreign-args" \
    OBSIDIAN_CLI="$FAKE_CLI" \
    OBSIDIAN_VAULT='Q:\Unconverted Vault' \
    bash "$WRAPPER" read path="Note.md" 2>"$TMP_DIR/foreign-error"
then
    fail "foreign OBSIDIAN_VAULT was accepted without a path converter"
fi

assert_file_equals \
    'obsidian-local.sh: foreign path requires OBSIDIAN_PATH_CONVERTER: Q:\Unconverted Vault' \
    "$TMP_DIR/foreign-error"
[[ ! -e "$TMP_DIR/foreign-args" ]] || fail "CLI ran for unconverted foreign path"
printf 'PASS: foreign path without converter fails clearly\n'
