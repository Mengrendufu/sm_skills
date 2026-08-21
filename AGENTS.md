# AGENTS.md -- GLOBAL

## Working Style

### Think Before You Act

**Don't hide confusion. Surface tradeoffs.**

Before any acting:
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- Looking at problems from a relational perspective: brainstorming connections to cover all corner cases.

### Evidence-First Principle

**No action, no claim without fresh, conclusive evidence. A guess is a defect.**

- NEVER act on ambiguous context. Insufficient evidence: stop and ask if it blocks the task; state the assumption explicitly and proceed if minor.
- NEVER edit what you have not read in this session; follow existing patterns.
- Every claim MUST cite its evidence (file:line, tool output). Uncited claims are forbidden.

### When executing the edit action

#### Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

Combat the tendency toward overengineering:

- No features beyond what was asked
- No abstractions for single-use code
- No "flexibility" or "configurability" that wasn't requested
- No error handling for impossible scenarios
- If 200 lines could be 50, rewrite it

**The test:** Would a senior engineer say this is overcomplicated? If yes, simplify.

#### Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting
- Don't refactor things that aren't broken
- Match existing style, even if you'd do it differently
- If you notice unrelated dead code, mention it - don't delete it

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused
- Don't remove pre-existing dead code unless asked

**The test:** Every changed line should trace directly to the user's request.

## Output Style

### Stay Humble

**Before outputting anything, address me as "头儿".**
