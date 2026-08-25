#![allow(non_camel_case_types, non_snake_case, non_upper_case_globals)]

use rs_hsm_::{SM_Hsm, SM_HsmImpl, SM_HsmState, SM_RetState, SM_StatePtr};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SM_MasterSig {
    USER_SLASH_COMMAND_MASTER_SIG,
    USER_INPUT_PROMPTS_SIG,
    BEFORE_AGENT_START_SIG,
    TOOL_CALL_SIG,
    TOOL_RESULT_SIG,
    AGENT_END_SIG,
    TIMEOUT_SIG,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SM_MasterEvt {
    pub sig: SM_MasterSig,
}

impl SM_MasterEvt {
    pub const fn new(sig: SM_MasterSig) -> Self {
        Self { sig }
    }
}

#[derive(Default)]
pub struct SM_MasterCtx {
    pub trace: String,
    pub notifications: Vec<String>,
    pub prompts: Vec<String>,
    pub protocol_messages: Vec<String>,
    pub status: String,
    pub input_evt_result: Option<&'static str>,
    pub subagent_blocks: Vec<String>,
    pub allow_dispatch_tool_call: bool,
    pub valid_subagent_block: bool,
    pub all_subagents_done: bool,
}

pub struct SM_MasterChart;

impl SM_HsmImpl for SM_MasterChart {
    type Context = SM_MasterCtx;
    type Event = SM_MasterEvt;

    fn TOP_initial(me: &mut Self::Context) -> SM_StatePtr<Self> {
        trace(me, "top-INIT.");
        &SM_Master_inactive
    }
}

fn trace(me: &mut SM_MasterCtx, msg: &str) {
    me.trace.push_str(msg);
    me.trace.push('\n');
}

fn load_agent(me: &mut SM_MasterCtx) {
    trace(me, "loadAgent(g_extensionCommandContext)");
}

fn update_status(me: &mut SM_MasterCtx, status: &str) {
    me.status.clear();
    me.status.push_str(status);
    trace(me, "updateStatus(master -- active)");
}

fn notify_warning(me: &mut SM_MasterCtx, message: &str) {
    me.notifications.push(message.to_owned());
}

fn send_protocol_reminder(me: &mut SM_MasterCtx, message: &str) {
    me.protocol_messages.push(message.to_owned());
}

fn push_prompt_mode(me: &mut SM_MasterCtx, mode: &str) {
    me.prompts.push(mode.to_owned());
}

fn dispatch_all_subagents(me: &mut SM_MasterCtx) {
    trace(me, "dispatchAllSubagents()");
}

fn arm_timeout(me: &mut SM_MasterCtx) {
    trace(me, "armTimeout()");
}

fn monitor_subagents(me: &mut SM_MasterCtx) {
    trace(me, "monitorSubagents()");
}

fn send_subagent_completion_summary(me: &mut SM_MasterCtx) {
    trace(me, "sendSubagentCompletionSummary()");
}

fn validDispatchToolCall(me: &SM_MasterCtx) -> bool {
    me.allow_dispatch_tool_call
}

fn subagentBlockFormatValid(me: &SM_MasterCtx) -> bool {
    me.valid_subagent_block
}

fn areAllSubagentsDone(me: &SM_MasterCtx) -> bool {
    me.all_subagents_done
}

fn SM_Master_inactive_(me: &mut SM_MasterCtx, e: &SM_MasterEvt) -> SM_RetState<SM_MasterChart> {
    match e.sig {
        SM_MasterSig::USER_SLASH_COMMAND_MASTER_SIG => {
            trace(me, "inactive-USER_SLASH_COMMAND_MASTER.");
            SM_RetState::Tran(&SM_Master_active)
        }
        _ => SM_RetState::Super,
    }
}

fn SM_Master_active_init_(me: &mut SM_MasterCtx) -> SM_StatePtr<SM_MasterChart> {
    trace(me, "active-INIT.");
    &SM_Master_idle
}

fn SM_Master_active_entry_(me: &mut SM_MasterCtx) {
    load_agent(me);
    update_status(me, "master -- active");
    trace(me, "active-ENTRY.");
}

fn SM_Master_active_exit_(_me: &mut SM_MasterCtx) {}

fn SM_Master_active_(me: &mut SM_MasterCtx, e: &SM_MasterEvt) -> SM_RetState<SM_MasterChart> {
    match e.sig {
        SM_MasterSig::USER_SLASH_COMMAND_MASTER_SIG => {
            trace(me, "active-USER_SLASH_COMMAND_MASTER.");
            SM_RetState::Tran(&SM_Master_inactive)
        }
        SM_MasterSig::USER_INPUT_PROMPTS_SIG => {
            notify_warning(me, "Not today!!!");
            me.input_evt_result = Some("handled");
            trace(me, "active-USER_INPUT_PROMPTS.");
            SM_RetState::Handled
        }
        _ => SM_RetState::Super,
    }
}

fn SM_Master_idle_entry_(me: &mut SM_MasterCtx) {
    me.subagent_blocks.clear();
    trace(me, "idle-ENTRY.");
}

fn SM_Master_idle_exit_(_me: &mut SM_MasterCtx) {}

fn SM_Master_idle_(me: &mut SM_MasterCtx, e: &SM_MasterEvt) -> SM_RetState<SM_MasterChart> {
    match e.sig {
        SM_MasterSig::USER_INPUT_PROMPTS_SIG => {
            me.input_evt_result = Some("continue");
            trace(me, "idle-USER_INPUT_PROMPTS.");
            SM_RetState::Tran(&SM_Master_routing)
        }
        _ => SM_RetState::Super,
    }
}

fn SM_Master_routing_entry_(_me: &mut SM_MasterCtx) {}

fn SM_Master_routing_exit_(_me: &mut SM_MasterCtx) {}

fn SM_Master_routing_(me: &mut SM_MasterCtx, e: &SM_MasterEvt) -> SM_RetState<SM_MasterChart> {
    match e.sig {
        SM_MasterSig::BEFORE_AGENT_START_SIG => {
            push_prompt_mode(me, "DISPATCH_ONLY");
            trace(me, "routing-BEFORE_AGENT_START.");
            SM_RetState::Handled
        }
        SM_MasterSig::TOOL_CALL_SIG => {
            if validDispatchToolCall(me) {
                trace(me, "routing-TOOL_CALL.allowed.");
                SM_RetState::Handled
            } else {
                send_protocol_reminder(me, "Call the dispatch tool using the required block format.");
                trace(me, "routing-TOOL_CALL.blocked.");
                SM_RetState::Handled
            }
        }
        SM_MasterSig::TOOL_RESULT_SIG => {
            if subagentBlockFormatValid(me) {
                trace(me, "routing-TOOL_RESULT.valid.");
                SM_RetState::Tran(&SM_Master_successful)
            } else {
                send_protocol_reminder(me, "Tool result must produce a valid subagent block.");
                trace(me, "routing-TOOL_RESULT.invalid.");
                SM_RetState::Handled
            }
        }
        _ => SM_RetState::Super,
    }
}

fn SM_Master_successful_entry_(_me: &mut SM_MasterCtx) {}

fn SM_Master_successful_exit_(_me: &mut SM_MasterCtx) {}

fn SM_Master_successful_(me: &mut SM_MasterCtx, e: &SM_MasterEvt) -> SM_RetState<SM_MasterChart> {
    match e.sig {
        SM_MasterSig::AGENT_END_SIG => {
            trace(me, "successful-AGENT_END.");
            SM_RetState::Tran(&SM_Master_delegating)
        }
        _ => SM_RetState::Super,
    }
}

fn SM_Master_delegating_entry_(me: &mut SM_MasterCtx) {
    dispatch_all_subagents(me);
    arm_timeout(me);
    trace(me, "delegating-ENTRY.");
}

fn SM_Master_delegating_exit_(_me: &mut SM_MasterCtx) {}

fn SM_Master_delegating_(me: &mut SM_MasterCtx, e: &SM_MasterEvt) -> SM_RetState<SM_MasterChart> {
    match e.sig {
        SM_MasterSig::TIMEOUT_SIG => {
            if areAllSubagentsDone(me) {
                trace(me, "delegating-TIMEOUT.complete.");
                SM_RetState::Tran(&SM_Master_working)
            } else {
                monitor_subagents(me);
                trace(me, "delegating-TIMEOUT.waiting.");
                SM_RetState::Handled
            }
        }
        _ => SM_RetState::Super,
    }
}

fn SM_Master_working_entry_(me: &mut SM_MasterCtx) {
    send_subagent_completion_summary(me);
    trace(me, "working-ENTRY.");
}

fn SM_Master_working_exit_(_me: &mut SM_MasterCtx) {}

fn SM_Master_working_(me: &mut SM_MasterCtx, e: &SM_MasterEvt) -> SM_RetState<SM_MasterChart> {
    match e.sig {
        SM_MasterSig::BEFORE_AGENT_START_SIG => {
            push_prompt_mode(me, "WORKING");
            trace(me, "working-BEFORE_AGENT_START.");
            SM_RetState::Handled
        }
        SM_MasterSig::AGENT_END_SIG => {
            trace(me, "working-AGENT_END.");
            SM_RetState::Tran(&SM_Master_idle)
        }
        _ => SM_RetState::Super,
    }
}

static SM_Master_inactive: SM_HsmState<SM_MasterChart> = SM_HsmState {
    super_: None,
    init_: None,
    entry_: None,
    exit_: None,
    handler_: SM_Master_inactive_,
};

static SM_Master_active: SM_HsmState<SM_MasterChart> = SM_HsmState {
    super_: None,
    init_: Some(SM_Master_active_init_),
    entry_: Some(SM_Master_active_entry_),
    exit_: Some(SM_Master_active_exit_),
    handler_: SM_Master_active_,
};

static SM_Master_idle: SM_HsmState<SM_MasterChart> = SM_HsmState {
    super_: Some(&SM_Master_active),
    init_: None,
    entry_: Some(SM_Master_idle_entry_),
    exit_: Some(SM_Master_idle_exit_),
    handler_: SM_Master_idle_,
};

static SM_Master_routing: SM_HsmState<SM_MasterChart> = SM_HsmState {
    super_: Some(&SM_Master_active),
    init_: None,
    entry_: Some(SM_Master_routing_entry_),
    exit_: Some(SM_Master_routing_exit_),
    handler_: SM_Master_routing_,
};

static SM_Master_successful: SM_HsmState<SM_MasterChart> = SM_HsmState {
    super_: Some(&SM_Master_routing),
    init_: None,
    entry_: Some(SM_Master_successful_entry_),
    exit_: Some(SM_Master_successful_exit_),
    handler_: SM_Master_successful_,
};

static SM_Master_delegating: SM_HsmState<SM_MasterChart> = SM_HsmState {
    super_: Some(&SM_Master_active),
    init_: None,
    entry_: Some(SM_Master_delegating_entry_),
    exit_: Some(SM_Master_delegating_exit_),
    handler_: SM_Master_delegating_,
};

static SM_Master_working: SM_HsmState<SM_MasterChart> = SM_HsmState {
    super_: Some(&SM_Master_active),
    init_: None,
    entry_: Some(SM_Master_working_entry_),
    exit_: Some(SM_Master_working_exit_),
    handler_: SM_Master_working_,
};

pub fn build_machine() -> (SM_Hsm<SM_MasterChart>, SM_MasterCtx) {
    let mut hsm = SM_Hsm::<SM_MasterChart>::new();
    let mut ctx = SM_MasterCtx::default();
    hsm.init(&mut ctx);
    (hsm, ctx)
}
