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
