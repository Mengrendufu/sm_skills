# QP Source Pattern Hints

## Use This File Only When

- the source QM/QP C pattern must be checked directly against familiar QP macros
- a parser or mapping review needs quick recognition help

Do not load this file for normal target implementation work when strict IR already exists.

## Core QM/QP Signals

| Pattern | Meaning |
| --- | --- |
| `Q_ENTRY_SIG` | entry action |
| `Q_EXIT_SIG` | exit action |
| `Q_INIT_SIG` | initial transition |

## Core QM/QP Results

| Pattern | Meaning |
| --- | --- |
| `Q_TRAN(&Target)` | external transition |
| `Q_HANDLED()` | handled with no transition |
| `Q_UNHANDLED()` | explicitly unhandled here |
| `Q_SUPER(&Parent)` | delegate to parent |

## Recognition Checklist

- state handler shape: `QState <Class>_<state>(<Class> * const me)`
- top initial shape: returns `Q_TRAN(&Target)`
- nested state default case: `Q_SUPER(&Parent)`
- guarded branch: explicit `if` / `else` around `Q_TRAN`, `Q_HANDLED`, `Q_UNHANDLED`, or `Q_SUPER`
- QM metadata comment: `/*${...} */`

## Use These Hints For

- confirming that a transition is `external`, `internal`, `super`, or `unhandled`
- checking whether a branch is a `choice`
- confirming parent delegation in generated C

## Do Not

- do not treat this file as a substitute for strict IR
- do not generate target code directly from these hints when strict IR is available
