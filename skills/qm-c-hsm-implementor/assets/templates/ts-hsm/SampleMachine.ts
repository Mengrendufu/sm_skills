/**
 * TypeScript State Machine Template for ts_hsm driver
 *
 * Strict preconditions:
 * 1. Input must come from qm-c-model-master --output json --strict
 * 2. Input IR must have is_reliable=true and no error diagnostics
 * 3. Final code should be checked against qm-c-model-master --output trace --strict
 * 4. Do not flatten choice branches or replace super delegation with handled()
 *
 * Usage:
 * 1. Copy this file to your project
 * 2. Replace "Sample" with your machine name
 * 3. Implement states based on your UML JSON model
 * 4. Fill in entry/exit/init/handle methods
 */

import {
  handled,
  HsmMachine,
  HsmState,
  superState,
  transition,
  type HandlerResult,
} from "../src/hsm";

// ============================================================================
// Step 1: Define Event Types
// ============================================================================
// Copy signal names from your UML JSON model
type SampleEvent =
  | { readonly type: "A" }
  | { readonly type: "B" }
  | { readonly type: "C" }
  | { readonly type: "D" }
  | { readonly type: "E" }
  | { readonly type: "F" }
  | { readonly type: "G" }
  | { readonly type: "H" }
  | { readonly type: "I" };

// ============================================================================
// Step 2: Implement State Classes
// ============================================================================
// Create one class per state from your UML model

/**
 * Top State (initial)
 * Parent: null
 * From JSON: top_initial.target = "s2"
 * Verify with trace: default init path
 */
class SampleTopState extends HsmState<SampleEvent, SampleMachine> {
  constructor() {
    super("top", null);
  }

  init(machine: SampleMachine): HsmState<SampleEvent, SampleMachine> {
    // From JSON: top_initial.action = "..."
    machine.trace("top-INIT.");
    return machine.s2;  // From JSON: top_initial.target
  }
}

/**
 * State S
 * Parent: top (via SampleTopState)
 * From JSON: {"name": "s", "parent": null, "entry": "...", "exit": "...", "initial": {...}}
 * Review anchor: map every generated branch back to the IR transition id
 */
class SampleSState extends HsmState<SampleEvent, SampleMachine> {
  constructor(parent: SampleTopState) {
    super("s", parent);
  }

  entry(machine: SampleMachine): void {
    // From JSON: s.entry
    machine.trace("s-ENTRY.");
  }

  exit(machine: SampleMachine): void {
    // From JSON: s.exit
    machine.trace("s-EXIT.");
  }

  init(machine: SampleMachine): HsmState<SampleEvent, SampleMachine> {
    // From JSON: s.initial.action, s.initial.target
    machine.trace("s-INIT.");
    return machine.s11;
  }

  handle(
    machine: SampleMachine,
    event: SampleEvent,
  ): HandlerResult<SampleEvent, SampleMachine> {
    switch (event.type) {
      case "I":
        // From JSON: {"trigger": "I", "guard": "me->foo", "kind": "internal"}
        if (machine.foo) {
          machine.foo = 0;
          machine.trace("s-I.");
          return handled();
        }
        return superState();

      case "E":
        // From JSON: {"trigger": "E", "target": "s11", "action": "..."}
        machine.trace("s-E.");
        return transition(machine.s11);

      default:
        return superState();
    }
  }
}

/**
 * State S1
 * Parent: s
 * From JSON: {"name": "s1", "parent": "s", ...}
 */
class SampleS1State extends HsmState<SampleEvent, SampleMachine> {
  constructor(parent: SampleSState) {
    super("s1", parent);
  }

  entry(machine: SampleMachine): void {
    machine.trace("s1-ENTRY.");
  }

  exit(machine: SampleMachine): void {
    machine.trace("s1-EXIT.");
  }

  init(machine: SampleMachine): HsmState<SampleEvent, SampleMachine> {
    machine.trace("s1-INIT.");
    return machine.s11;
  }

  handle(
    machine: SampleMachine,
    event: SampleEvent,
  ): HandlerResult<SampleEvent, SampleMachine> {
    switch (event.type) {
      case "I":
        // Internal transition (no target)
        machine.trace("s1-I.");
        return handled();

      case "A":
        // Self-transition to s1
        machine.trace("s1-A.");
        return transition(machine.s1);

      case "B":
        machine.trace("s1-B.");
        return transition(machine.s11);

      case "C":
        machine.trace("s1-C.");
        return transition(machine.s2);

      case "D":
        // Guard: !me->foo
        if (!machine.foo) {
          machine.foo = 1;
          machine.trace("s1-D.");
          return transition(machine.s);
        }
        return superState();

      case "F":
        machine.trace("s1-F.");
        return transition(machine.s211);

      default:
        return superState();
    }
  }
}

/**
 * State S11
 * Parent: s1
 * From JSON: {"name": "s11", "parent": "s1", ...}
 */
class SampleS11State extends HsmState<SampleEvent, SampleMachine> {
  constructor(parent: SampleS1State) {
    super("s11", parent);
  }

  entry(machine: SampleMachine): void {
    machine.trace("s11-ENTRY.");
  }

  exit(machine: SampleMachine): void {
    machine.trace("s11-EXIT.");
  }

  handle(
    machine: SampleMachine,
    event: SampleEvent,
  ): HandlerResult<SampleEvent, SampleMachine> {
    switch (event.type) {
      case "G":
        machine.trace("s11-G.");
        return transition(machine.s211);

      case "H":
        machine.trace("s11-H.");
        return transition(machine.s);

      case "D":
        // Guard: me->foo
        if (machine.foo) {
          machine.foo = 0;
          machine.trace("s11-D.");
          return transition(machine.s1);
        }
        return superState();

      default:
        return superState();
    }
  }
}

/**
 * State S2
 * Parent: s
 */
class SampleS2State extends HsmState<SampleEvent, SampleMachine> {
  constructor(parent: SampleSState) {
    super("s2", parent);
  }

  entry(machine: SampleMachine): void {
    machine.trace("s2-ENTRY.");
  }

  exit(machine: SampleMachine): void {
    machine.trace("s2-EXIT.");
  }

  init(machine: SampleMachine): HsmState<SampleEvent, SampleMachine> {
    machine.trace("s2-INIT.");
    return machine.s21;
  }

  handle(
    machine: SampleMachine,
    event: SampleEvent,
  ): HandlerResult<SampleEvent, SampleMachine> {
    switch (event.type) {
      case "I":
        // Guard: !me->foo
        if (!machine.foo) {
          machine.foo = 1;
          machine.trace("s2-I.");
          return handled();
        }
        return superState();

      case "C":
        machine.trace("s2-C.");
        return transition(machine.s1);

      case "F":
        machine.trace("s2-F.");
        return transition(machine.s11);

      default:
        return superState();
    }
  }
}

/**
 * State S21
 * Parent: s2
 */
class SampleS21State extends HsmState<SampleEvent, SampleMachine> {
  constructor(parent: SampleS2State) {
    super("s21", parent);
  }

  entry(machine: SampleMachine): void {
    machine.trace("s21-ENTRY.");
  }

  exit(machine: SampleMachine): void {
    machine.trace("s21-EXIT.");
  }

  init(machine: SampleMachine): HsmState<SampleEvent, SampleMachine> {
    machine.trace("s21-INIT.");
    return machine.s211;
  }

  handle(
    machine: SampleMachine,
    event: SampleEvent,
  ): HandlerResult<SampleEvent, SampleMachine> {
    switch (event.type) {
      case "A":
        // Self-transition
        machine.trace("s21-A.");
        return transition(machine.s21);

      case "B":
        machine.trace("s21-B.");
        return transition(machine.s211);

      case "G":
        machine.trace("s21-G.");
        return transition(machine.s1);

      default:
        return superState();
    }
  }
}

/**
 * State S211
 * Parent: s21
 */
class SampleS211State extends HsmState<SampleEvent, SampleMachine> {
  constructor(parent: SampleS21State) {
    super("s211", parent);
  }

  entry(machine: SampleMachine): void {
    machine.trace("s211-ENTRY.");
  }

  exit(machine: SampleMachine): void {
    machine.trace("s211-EXIT.");
  }

  handle(
    machine: SampleMachine,
    event: SampleEvent,
  ): HandlerResult<SampleEvent, SampleMachine> {
    switch (event.type) {
      case "D":
        machine.trace("s211-D.");
        return transition(machine.s21);

      case "H":
        machine.trace("s211-H.");
        return transition(machine.s);

      default:
        return superState();
    }
  }
}

// ============================================================================
// Step 3: Machine Class
// ============================================================================

interface TraceCarrier {
  trace: string[];
}

class SampleMachine extends HsmMachine<SampleEvent, SampleMachine> implements TraceCarrier {
  // State machine variables (from your UML model)
  public foo = 0;

  // State instances - declare all states
  public readonly top: SampleTopState;
  public readonly s: SampleSState;
  public readonly s1: SampleS1State;
  public readonly s11: SampleS11State;
  public readonly s2: SampleS2State;
  public readonly s21: SampleS21State;
  public readonly s211: SampleS211State;

  // Trace for testing/verification
  public readonly trace: string[] = [];

  constructor() {
    // Create top state
    const top = new SampleTopState();
    super(top);

    // Initialize all states with parent references
    this.top = top;
    this.s = new SampleSState(this.top);
    this.s1 = new SampleS1State(this.s);
    this.s11 = new SampleS11State(this.s1);
    this.s2 = new SampleS2State(this.s);
    this.s21 = new SampleS21State(this.s2);
    this.s211 = new SampleS211State(this.s21);
  }

  trace(fragment: string): void {
    this.trace.push(fragment);
  }
}

// ============================================================================
// Export
// ============================================================================

export { SampleMachine, SampleEvent };
