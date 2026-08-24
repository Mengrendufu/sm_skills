import {
  handled,
  HsmMachine,
  HsmState,
  superState,
  transition,
  type HandlerResult,
} from "../src/hsm";

type SM_MasterEvent =
  | { readonly type: "USER_SLASH_COMMAND_MASTER" }
  | { readonly type: "USER_INPUT_PROMPTS" }
  | { readonly type: "BEFORE_AGENT_START" }
  | { readonly type: "TOOL_CALL" }
  | { readonly type: "TOOL_RESULT" }
  | { readonly type: "AGENT_END" }
  | { readonly type: "TIMEOUT" };

class SM_MasterTopState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor() {
    super("top", null);
  }

  public override init(machine: SM_MasterMachine): HsmState<SM_MasterEvent, SM_MasterMachine> {
    machine.push("top-INIT.");
    return machine.inactive;
  }
}

class SM_MasterInactiveState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor(parent: SM_MasterTopState) {
    super("inactive", parent);
  }

  public override handle(
    machine: SM_MasterMachine,
    event: SM_MasterEvent,
  ): HandlerResult<SM_MasterEvent, SM_MasterMachine> {
    switch (event.type) {
      case "USER_SLASH_COMMAND_MASTER":
        machine.push("inactive-USER_SLASH_COMMAND_MASTER.");
        return transition(machine.active);
      default:
        return superState();
    }
  }
}

class SM_MasterActiveState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor(parent: SM_MasterTopState) {
    super("active", parent);
  }

  public override entry(machine: SM_MasterMachine): void {
    machine.loadAgent();
    machine.updateStatus("master -- active");
    machine.push("active-ENTRY.");
  }

  public override init(machine: SM_MasterMachine): HsmState<SM_MasterEvent, SM_MasterMachine> {
    machine.push("active-INIT.");
    return machine.idle;
  }

  public override handle(
    machine: SM_MasterMachine,
    event: SM_MasterEvent,
  ): HandlerResult<SM_MasterEvent, SM_MasterMachine> {
    switch (event.type) {
      case "USER_SLASH_COMMAND_MASTER":
        machine.push("active-USER_SLASH_COMMAND_MASTER.");
        return transition(machine.inactive);
      case "USER_INPUT_PROMPTS":
        machine.notifyWarning("Not today!!!");
        machine.inputEvtResult = "handled";
        machine.push("active-USER_INPUT_PROMPTS.");
        return handled();
      default:
        return superState();
    }
  }
}

class SM_MasterIdleState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor(parent: SM_MasterActiveState) {
    super("idle", parent);
  }

  public override entry(machine: SM_MasterMachine): void {
    machine.subagentBlocks = [];
    machine.push("idle-ENTRY.");
  }

  public override handle(
    machine: SM_MasterMachine,
    event: SM_MasterEvent,
  ): HandlerResult<SM_MasterEvent, SM_MasterMachine> {
    switch (event.type) {
      case "USER_INPUT_PROMPTS":
        machine.inputEvtResult = "continue";
        machine.push("idle-USER_INPUT_PROMPTS.");
        return transition(machine.routing);
      default:
        return superState();
    }
  }
}

class SM_MasterRoutingState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor(parent: SM_MasterActiveState) {
    super("routing", parent);
  }

  public override handle(
    machine: SM_MasterMachine,
    event: SM_MasterEvent,
  ): HandlerResult<SM_MasterEvent, SM_MasterMachine> {
    switch (event.type) {
      case "BEFORE_AGENT_START":
        machine.pushPromptMode("DISPATCH_ONLY");
        machine.push("routing-BEFORE_AGENT_START.");
        return handled();
      case "TOOL_CALL":
        if (machine.validDispatchToolCall()) {
          machine.push("routing-TOOL_CALL.allowed.");
          return handled();
        }
        machine.sendProtocolReminder("Call the dispatch tool using the required block format.");
        machine.push("routing-TOOL_CALL.blocked.");
        return handled();
      case "TOOL_RESULT":
        if (machine.subagentBlockFormatValid()) {
          machine.push("routing-TOOL_RESULT.valid.");
          return transition(machine.successful);
        }
        machine.sendProtocolReminder("Tool result must produce a valid subagent block.");
        machine.push("routing-TOOL_RESULT.invalid.");
        return handled();
      default:
        return superState();
    }
  }
}

class SM_MasterSuccessfulState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor(parent: SM_MasterRoutingState) {
    super("successful", parent);
  }

  public override handle(
    machine: SM_MasterMachine,
    event: SM_MasterEvent,
  ): HandlerResult<SM_MasterEvent, SM_MasterMachine> {
    switch (event.type) {
      case "AGENT_END":
        machine.push("successful-AGENT_END.");
        return transition(machine.delegating);
      default:
        return superState();
    }
  }
}

class SM_MasterDelegatingState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor(parent: SM_MasterActiveState) {
    super("delegating", parent);
  }

  public override entry(machine: SM_MasterMachine): void {
    machine.dispatchAllSubagents();
    machine.armTimeout();
    machine.push("delegating-ENTRY.");
  }

  public override handle(
    machine: SM_MasterMachine,
    event: SM_MasterEvent,
  ): HandlerResult<SM_MasterEvent, SM_MasterMachine> {
    switch (event.type) {
      case "TIMEOUT":
        if (machine.areAllSubagentsDone()) {
          machine.push("delegating-TIMEOUT.complete.");
          return transition(machine.working);
        }
        machine.monitorSubagents();
        machine.push("delegating-TIMEOUT.waiting.");
        return handled();
      default:
        return superState();
    }
  }
}

class SM_MasterWorkingState extends HsmState<SM_MasterEvent, SM_MasterMachine> {
  public constructor(parent: SM_MasterActiveState) {
    super("working", parent);
  }

  public override entry(machine: SM_MasterMachine): void {
    machine.sendSubagentCompletionSummary();
    machine.push("working-ENTRY.");
  }

  public override handle(
    machine: SM_MasterMachine,
    event: SM_MasterEvent,
  ): HandlerResult<SM_MasterEvent, SM_MasterMachine> {
    switch (event.type) {
      case "BEFORE_AGENT_START":
        machine.pushPromptMode("WORKING");
        machine.push("working-BEFORE_AGENT_START.");
        return handled();
      case "AGENT_END":
        machine.push("working-AGENT_END.");
        return transition(machine.idle);
      default:
        return superState();
    }
  }
}

export class SM_MasterMachine extends HsmMachine<SM_MasterEvent, SM_MasterMachine> {
  public readonly trace: string[] = [];
  public readonly notifications: string[] = [];
  public readonly prompts: string[] = [];
  public readonly protocolMessages: string[] = [];
  public readonly top: SM_MasterTopState;
  public readonly inactive: SM_MasterInactiveState;
  public readonly active: SM_MasterActiveState;
  public readonly idle: SM_MasterIdleState;
  public readonly routing: SM_MasterRoutingState;
  public readonly successful: SM_MasterSuccessfulState;
  public readonly delegating: SM_MasterDelegatingState;
  public readonly working: SM_MasterWorkingState;

  public status = "inactive";
  public inputEvtResult: "handled" | "continue" | null = null;
  public subagentBlocks: string[] = [];
  public allowDispatchToolCall = false;
  public validSubagentBlock = false;
  public allSubagentsDone = false;

  public constructor() {
    const top = new SM_MasterTopState();
    super(top);
    this.top = top;
    this.inactive = new SM_MasterInactiveState(top);
    this.active = new SM_MasterActiveState(top);
    this.idle = new SM_MasterIdleState(this.active);
    this.routing = new SM_MasterRoutingState(this.active);
    this.successful = new SM_MasterSuccessfulState(this.routing);
    this.delegating = new SM_MasterDelegatingState(this.active);
    this.working = new SM_MasterWorkingState(this.active);
  }

  public push(fragment: string): void {
    this.trace.push(fragment);
  }

  public loadAgent(): void {
    this.trace.push("loadAgent(g_extensionCommandContext)");
  }

  public updateStatus(nextStatus: string): void {
    this.status = nextStatus;
    this.trace.push(`updateStatus(${nextStatus})`);
  }

  public notifyWarning(message: string): void {
    this.notifications.push(message);
  }

  public pushPromptMode(mode: "DISPATCH_ONLY" | "WORKING"): void {
    this.prompts.push(mode);
  }

  public sendProtocolReminder(message: string): void {
    this.protocolMessages.push(message);
  }

  public dispatchAllSubagents(): void {
    this.trace.push("dispatchAllSubagents()");
  }

  public armTimeout(): void {
    this.trace.push("armTimeout()");
  }

  public monitorSubagents(): void {
    this.trace.push("monitorSubagents()");
  }

  public sendSubagentCompletionSummary(): void {
    this.trace.push("sendSubagentCompletionSummary()");
  }

  public validDispatchToolCall(): boolean {
    return this.allowDispatchToolCall;
  }

  public subagentBlockFormatValid(): boolean {
    return this.validSubagentBlock;
  }

  public areAllSubagentsDone(): boolean {
    return this.allSubagentsDone;
  }
}
