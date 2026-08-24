---
name: using-git-worktrees
description: Use when starting work that needs an isolated checkout, entering an implementation plan, or deciding whether to create, reuse, or validate a Git worktree.
---

# Using Git Worktrees

Create isolation only after determining whether it already exists and what the
user authorized.

**Core rule:** Detect, choose, create, set up, then verify the baseline.

## 1. Detect Existing Isolation

```bash
repo_git_dir="$(cd "$(git rev-parse --git-dir)" && pwd -P)"
repo_common_dir="$(cd "$(git rev-parse --git-common-dir)" && pwd -P)"
repo_branch="$(git branch --show-current)"
superproject_root="$(git rev-parse --show-superproject-working-tree 2>/dev/null || true)"
```

- Different Git and common directories with an empty `superproject_root` means
  this is already a linked worktree. Report its path and branch and reuse it;
  do not duplicate isolation.
- A non-empty `superproject_root` signals a submodule, not a linked worktree.
  Treat it as a normal checkout for this decision.
- Keep a detached worktree externally managed unless branch creation is
  authorized.

If the requested deliverable is specifically an additional worktree rather
than isolation for the current task, provision it separately after the safety
checks below.

## 2. Resolve Workspace Authority

Honor explicit instructions first: “work here” means stay; “use isolation” is
consent to create or enter it; a named location is part of the boundary. If no
preference exists, ask before creating. Never infer consent from an existing
directory or silently substitute another location.

## 3. Choose the Mechanism

If the execution environment exposes a managed workspace-isolation capability,
use it because it owns placement, branch creation, and cleanup. Do not invent
that capability or bypass it with manual Git state. Otherwise use Git directly.

## 4. Use the Git Fallback Safely

Choose the location in this order: explicit instruction, existing `.worktrees/`,
existing `worktrees/`, then project-local `.worktrees/`.

For a project-local location, verify it is ignored before creation:

```bash
selected_root='<selected-project-relative-root>'
git check-ignore -q -- "$selected_root" "$selected_root/"
```

If the selected project-local directory is not ignored, stop. Propose the
minimal ignore entry and commit only with authority. If that change is
forbidden, ask whether to use an explicit repository-external location.

Resolve the exact branch and path before creation:

```bash
branch_name='<branch-name>'
worktree_path='<worktree-path>'

test ! -e "$worktree_path"
if git worktree list --porcelain | grep -Fxq "branch refs/heads/$branch_name"; then
    printf 'branch is already attached to a worktree: %s\n' "$branch_name" >&2
    exit 1
fi

if git show-ref --verify --quiet "refs/heads/$branch_name"; then
    git worktree add "$worktree_path" "$branch_name"
else
    git worktree add "$worktree_path" -b "$branch_name"
fi
```

Reuse an existing unattached branch without `-b`; use `-b` only to create an
absent branch. Never target an existing path, unresolved variable, or broad
glob.

## 5. Set Up the Project

Read the repository instructions and run only its applicable setup workflow.
Do not introduce a package manager or convention merely because a familiar
manifest exists.

## 6. Verify the Baseline

Run the repository's canonical test or validation command before changing the
implementation.

- Pass: report path, branch, command, and result.
- Fail: report exact failures and preserve them as the pre-change baseline.
  Never say tests pass.
- Proceed from a failing baseline only with explicit authority after the
  failures are visible; otherwise request direction.

## Quick Reference

| Situation | Action |
|---|---|
| Already in linked worktree | Reuse it; do not nest or duplicate isolation |
| Inside a submodule | Treat as a normal checkout for this decision |
| Managed isolation exists | Use the managed capability |
| Project-local directory is unignored | Stop before creation |
| Requested location is unsafe | Surface the conflict; do not substitute |
| Baseline fails | Report failures; never claim tests pass |

## Red Flags

- Creating before detecting current isolation.
- Treating a submodule as a linked worktree.
- Nesting worktrees or switching paths without approval.
- Using an unignored project-local directory.
- Skipping setup, baseline verification, or its actual result.
