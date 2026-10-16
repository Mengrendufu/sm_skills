# ts_hsm Target Mapping

## Use This File For

- implementing one target runtime in TypeScript with `ts_hsm`
- reviewing whether the confirmed model can map cleanly into `handled`, `superState`, and `transition`

## Workflow

1. Read the confirmed topology from `qm-model-understand` and inspect the source action/data context.
2. Inspect the target project's actual runtime API, imports and naming conventions; the shapes below are adapter examples.
3. Adapt the matching template from `assets/templates/` to every source state, initial target and guarded branch. With no user-specified output path, write generated files to the OS temporary task directory defined in `SKILL.md`.
4. Build and test in the target project, covering initialization, self/cross-level transitions, both guard outcomes, actions and parent delegation. Check against source semantics rather than a generated verification report.

## Runtime Primitives

Core shapes:

```typescript
abstract class HsmState<E extends EventObject, M extends HsmMachine<E, M>> {
  public readonly id: string;
  public readonly parent: HsmState<E, M> | null;

  public entry(_machine: M): void;
  public exit(_machine: M): void;
  public init(_machine: M): HsmState<E, M> | null;
  public handle(_machine: M, _event: E): HandlerResult<E, M>;
}

abstract class HsmMachine<E extends EventObject, M extends HsmMachine<E, M>> {
  public start(): void;
  public dispatch(event: E): DispatchStatus;
}
```

Handler results:

```typescript
handled();
superState();
transition(machine.s11);
transition(machine.s1, sourceState);
```

## Mapping Checklist

- map each IR state to one `HsmState` subclass
- map IR parent to constructor parent
- map state `initial` to `init()`
- map `entry` and `exit` snippets to overrides
- map `top_initial.target_state_id` to top-state `init()`
- map one IR event owner to one `switch (event.type)` case set

## Transition Mapping

- `external` -> `transition(target)`
- `internal` -> `handled()`
- `super` -> `superState()`
- `unhandled` -> `superState()` only when bubbling matches source semantics
- `choice` -> explicit branch-by-branch `if` or `switch` logic from IR `branches[]`

## Minimal Pattern

```typescript
class SampleS1State extends HsmState<SampleEvent, SampleMachine> {
  public override handle(
    machine: SampleMachine,
    event: SampleEvent,
  ): HandlerResult<SampleEvent, SampleMachine> {
    switch (event.type) {
      case "A":
        return transition(machine.s1);
      case "I":
        return handled();
      default:
        return superState();
    }
  }
}
```

## Practical Rules

- preserve `superState()` for real parent delegation
- do not replace delegated behavior with `handled()`
- keep guarded `choice` branches explicit
- keep target runtime rewrites visible in the returned mapping summary

## Stop If

- a required target cannot be mapped to a concrete state instance
- choice or delegation behavior would be approximated
- preserving source hierarchy, actions, guards, and delegation would require invention
