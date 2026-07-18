# Final Superpowers Skills Evaluation

## `verification-before-completion`

### Control Run

Three controls responded without reading the candidate or formal Skill. Unlike
the earlier core-practice controls, all three already preserved the evidence
boundary because the repository instructions independently require fresh
evidence:

- Stale result: refused to describe a parent commit's green suite as validation
  of three later production changes.
- Delegated report: changed the claim to “reported complete, not independently
  verified” when the other agent supplied no command output.
- Partial check: reported only the formatter and targeted unit test as passing,
  not the unexecuted build or full suite.

Result: CONTROL PASS. There is no observed repository-local behavior failure to
patch. Formal promotion provides the same discipline as a portable Skill for
workspaces that do not carry this repository's instructions.

### Forward Run

All three agents read the formal Skill and preserved the same boundary:

- Stale result: reported the parent commit's result and explicitly marked the
  later production changes as unverified.
- Delegated report: decomposed completion, tests, commit, and clean-worktree
  claims, then marked each unsupported state as unverified.
- Partial check: reported the formatter and targeted test as passing while
  naming the full build and suite as not run.

Result: PASS. The portable Skill retains strict claim-to-evidence scope without
depending on repository instructions or upstream author-history anecdotes.

## `using-git-worktrees`

### Control Run

Three controls responded without reading the candidate or formal Skill:

- Existing linked worktree: correctly rejected a nested worktree, but still
  proposed creating a sibling worktree without first deciding whether the
  current isolated checkout already satisfied the task.
- Unignored project directory: refused to create under `.worktrees/`, but
  silently changed the requested location to a repository-external directory
  instead of surfacing the location-policy conflict for approval.
- Failing baseline: honored the user's explicit direction to proceed while
  accurately reporting 12 existing failures and refusing to say tests passed.

Observed failure: general Git knowledge prevented the most dangerous commands,
but did not consistently preserve the ordered reuse and preference gates.

### Forward Run

All three agents read the formal Skill and followed the relevant branch:

- Existing linked worktree: rejected nesting; because the requested deliverable
  was explicitly an additional worktree, it checked ignore status, branch
  existence, and target path before proposing a sibling worktree.
- Unignored project directory: stopped without changing `.gitignore` or
  silently substituting an external path, then requested explicit location
  authority.
- Failing baseline: reused the existing isolated checkout and preserved the 12
  failures as the visible pre-change baseline. It followed the user's explicit
  direction to proceed but refused to claim tests passed.

Result: PASS. The portable Skill distinguishes reuse from explicit provisioning,
preserves workspace authority, and reports baseline state accurately without a
runtime-specific worktree command.
