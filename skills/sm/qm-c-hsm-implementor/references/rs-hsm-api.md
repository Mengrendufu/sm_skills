# rs_hsm_ Target Mapping

## Use This File For

- implementing one target runtime in Rust with `rs_hsm_`
- reviewing whether strict IR can map cleanly into `rs_hsm_`

Read `strict-contract.md` first.

## Runtime Primitives

Use:

```rust
use rs_hsm_::{SM_Hsm, SM_HsmImpl, SM_HsmState, SM_RetState, SM_StatePtr};
```

Core shapes:

```rust
pub trait SM_HsmImpl: Sized + 'static {
    type Context;
    type Event;

    fn TOP_initial(me: &mut Self::Context) -> SM_StatePtr<Self>;
}

pub struct SM_HsmState<C: SM_HsmImpl> {
    pub super_: Option<SM_StatePtr<C>>,
    pub init_: Option<SM_InitHandler<C>>,
    pub entry_: Option<SM_ActionHandler<C::Context>>,
    pub exit_: Option<SM_ActionHandler<C::Context>>,
    pub handler_: SM_StateHandler<C>,
}

pub enum SM_RetState<C: SM_HsmImpl> {
    Handled,
    Super,
    Tran(SM_StatePtr<C>),
}
```

## Mapping Checklist

- map each IR state to one static `SM_HsmState<Chart>`
- map IR parent to `super_`
- map state `initial` to `init_`
- map `entry` and `exit` snippets to action helpers
- map `top_initial.target_state_id` to `TOP_initial()`
- map one IR event owner to one handler function

## Transition Mapping

- `external` -> `SM_RetState::Tran(&TargetState)`
- `internal` -> `SM_RetState::Handled`
- `super` -> `SM_RetState::Super`
- `unhandled` -> `SM_RetState::Super` only when bubbling is the faithful runtime behavior
- `choice` -> explicit `if` or `match` branches from IR `branches[]`

## Minimal Pattern

```rust
fn MyState_(me: &mut MyCtx, e: &MyEvt) -> SM_RetState<MyChart> {
    match e.sig {
        MySig::A_SIG => SM_RetState::Tran(&MyOtherState),
        MySig::I_SIG => SM_RetState::Handled,
        _ => SM_RetState::Super,
    }
}

static MyState: SM_HsmState<MyChart> = SM_HsmState {
    super_: Some(&ParentState),
    init_: None,
    entry_: Some(MyState_entry_),
    exit_: Some(MyState_exit_),
    handler_: MyState_,
};
```

## Practical Rules

- `rs_hsm_` is pointer-linked; resolve every `target_state_id` to a concrete static state symbol
- do not collapse guarded `choice` behavior into one unconditional transition
- move action code into helpers when inline snippets become noisy
- keep `Super` semantics intact; do not replace them with `Handled`

## Stop If

- a required target cannot be resolved to a static state symbol
- guarded delegation cannot be expressed faithfully
- preserving strict-contract semantics would require approximation
