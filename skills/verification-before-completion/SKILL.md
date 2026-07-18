---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, passing, clean, committed, or ready for delivery, especially after delegated work or partial checks.
---

# Verification Before Completion

Make claims no broader than fresh evidence.

**Core rule:** No completion claim without running and reading the command that
proves that exact claim.

## Evidence Gate

Before stating that work is complete, fixed, passing, clean, or ready:

1. **Identify the claim.** State exactly what will be asserted.
2. **Choose proof.** Select the command or observation that directly proves the
   whole claim.
3. **Run it freshly.** Execute the complete check against the current state.
4. **Read the result.** Inspect exit status, failures, warnings, skipped checks,
   and the scope actually exercised.
5. **Report only supported facts.** If proof is missing or fails, state the
   actual verified scope and remaining uncertainty.

Previous output, confidence, and another worker's summary are context, not
current proof.

## Claim-to-Evidence Contract

| Claim | Required evidence | Insufficient evidence |
|---|---|---|
| Tests pass | Current full test command exits successfully with no failures | Earlier run or one targeted test |
| Build succeeds | Current build command exits successfully | Formatter, linter, or type check alone |
| Bug is fixed | Original reproduction now passes and relevant regressions pass | Code changed or symptom not observed once |
| Worktree is clean | Current version-control status shows no changes | Another worker says it committed |
| Requirements are met | Each requirement is checked against the implementation | Tests alone |
| Delegated task is complete | Inspect the diff and independently run relevant checks | A success message |

When a complete check cannot run, do not turn that limitation into a positive
claim. Report: what ran, its result, what did not run, and the consequence.

## Delegated Work

Treat a delegated result as untrusted until independently verified:

1. Inspect the produced files or version-control diff.
2. Run the checks that prove the delegated requirements.
3. Compare the result with the requested scope.
4. Report discrepancies instead of repeating the worker's conclusion.

## Red Flags

Stop before sending the response if it contains or implies:

- “Should,” “probably,” or “looks good” presented as a result.
- A full-suite claim from a partial check.
- A current-state claim from stale output.
- Trust in an agent, reviewer, or colleague without inspecting evidence.
- “No time to verify” followed by a completion claim.
- A clean-worktree, commit, push, or delivery claim without checking that state.

| Rationalization | Correction |
|---|---|
| “The change is trivial.” | Triviality does not produce evidence. |
| “It passed earlier.” | Earlier state is not current state. |
| “The worker said success.” | Verify delegated output independently. |
| “A partial check is enough.” | Narrow the claim to the partial check. |
| “The user wants a quick answer.” | Give a quick, accurate status. |

## Final Check

Immediately before the final response, ask:

- What exact evidence supports each positive status claim?
- Was that evidence produced from the current state?
- Does the wording exceed the verified scope?

If any answer is unclear, run the proof or narrow the claim.
