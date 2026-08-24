# sm_hsm Target Mapping

## Use This File For

- implementing one target runtime in C with `sm_hsm`
- reviewing whether strict IR can map cleanly into `_SM_*` semantics

Read `strict-contract.md` first.

## Runtime Primitives

Core shapes:

```c
typedef struct SM_HsmState {
    struct SM_HsmState SM_HSM_ROM * super;
    struct SM_HsmState SM_HSM_ROM * (*init_)(void * const me);
    SM_ActionHandler entry_;
    SM_ActionHandler exit_;
    SM_StateHandler handler_;
} SM_HsmState;
```

Return macros:

| Macro | Meaning |
| --- | --- |
| `_SM_HANDLED()` | handled, no transition |
| `_SM_SUPER()` | delegate to parent |
| `_SM_TRAN(target_)` | transition to target |
| `_SM_INIT(target_)` | return init target |

## Mapping Checklist

- map each IR state to one ROM `SM_HsmState`
- map IR parent to `super`
- map state `initial` to `init_`
- map `entry` and `exit` snippets to dedicated action handlers
- map `top_initial.target_state_id` to the top-level initial handler
- map one IR event owner to one `switch` arm in the state handler

## Transition Mapping

- `external` -> `_SM_TRAN(&TargetState)`
- `internal` -> `_SM_HANDLED()`
- `super` -> `_SM_SUPER()`
- `unhandled` -> `_SM_SUPER()` only when bubbling matches source semantics
- `choice` -> explicit guarded branches from IR `branches[]`

## Minimal Pattern

```c
static SM_RetState MyState_(SM_Hsm * const me, MyEvt const * const e) {
    switch (MYSIG(e)) {
        case A_SIG: {
            return _SM_TRAN(&MyOtherState);
        }
        case I_SIG: {
            return _SM_HANDLED();
        }
        default: {
            return _SM_SUPER();
        }
    }
}
```

## Practical Rules

- keep `_SM_SUPER()` for true parent delegation
- do not replace delegation with `_SM_HANDLED()`
- keep guarded `choice` branches explicit
- preserve stable IR `transition.id` mapping during review

## Stop If

- a required target cannot be named as a concrete state symbol
- parent delegation would be lost or flattened
- preserving strict-contract semantics would require approximation
