#![allow(non_camel_case_types, non_snake_case, non_upper_case_globals)]

// Strict preconditions:
// 1. Input must come from qm-c-model-master --output json --strict
// 2. Input IR must have is_reliable=true and no error diagnostics
// 3. Final code should be checked against qm-c-model-master --output trace --strict
// 4. Do not flatten choice branches or replace SM_RetState::Super with Handled

use rs_hsm_::{SM_Hsm, SM_HsmImpl, SM_HsmState, SM_RetState, SM_StatePtr};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SampleSig {
    START_SIG,
    STOP_SIG,
    TICK_SIG,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SampleEvt {
    pub sig: SampleSig,
}

impl SampleEvt {
    pub const fn new(sig: SampleSig) -> Self {
        Self { sig }
    }
}

#[derive(Default)]
pub struct SampleCtx {
    pub trace: std::string::String,
    pub counter: u32,
}

pub struct SampleChart;

impl SM_HsmImpl for SampleChart {
    type Context = SampleCtx;
    type Event = SampleEvt;

    fn TOP_initial(me: &mut Self::Context) -> SM_StatePtr<Self> {
        trace(me, "top-INIT.");
        &Sample_idle
    }
}

fn trace(me: &mut SampleCtx, msg: &str) {
    me.trace.push_str(msg);
}

fn Sample_active_init_(me: &mut SampleCtx) -> SM_StatePtr<SampleChart> {
    trace(me, "active-INIT.");
    &Sample_working
}

fn Sample_active_entry_(me: &mut SampleCtx) {
    trace(me, "active-ENTRY.");
}

fn Sample_active_exit_(me: &mut SampleCtx) {
    trace(me, "active-EXIT.");
}

fn Sample_active_(me: &mut SampleCtx, e: &SampleEvt) -> SM_RetState<SampleChart> {
    match e.sig {
        SampleSig::STOP_SIG => {
            trace(me, "active-STOP.");
            SM_RetState::Tran(&Sample_idle)
        }
        _ => SM_RetState::Super,
    }
}

fn Sample_idle_entry_(me: &mut SampleCtx) {
    trace(me, "idle-ENTRY.");
}

fn Sample_idle_exit_(me: &mut SampleCtx) {
    trace(me, "idle-EXIT.");
}

fn Sample_idle_(me: &mut SampleCtx, e: &SampleEvt) -> SM_RetState<SampleChart> {
    match e.sig {
        SampleSig::START_SIG => {
            trace(me, "idle-START.");
            SM_RetState::Tran(&Sample_active)
        }
        _ => SM_RetState::Super,
    }
}

fn Sample_working_entry_(me: &mut SampleCtx) {
    trace(me, "working-ENTRY.");
}

fn Sample_working_exit_(me: &mut SampleCtx) {
    trace(me, "working-EXIT.");
}

fn Sample_working_(me: &mut SampleCtx, e: &SampleEvt) -> SM_RetState<SampleChart> {
    match e.sig {
        SampleSig::TICK_SIG if me.counter < 10 => {
            me.counter += 1;
            trace(me, "working-TICK.");
            SM_RetState::Handled
        }
        SampleSig::TICK_SIG => SM_RetState::Super,
        _ => SM_RetState::Super,
    }
}

static Sample_idle: SM_HsmState<SampleChart> = SM_HsmState {
    super_: None,
    init_: None,
    entry_: Some(Sample_idle_entry_),
    exit_: Some(Sample_idle_exit_),
    handler_: Sample_idle_,
};

static Sample_active: SM_HsmState<SampleChart> = SM_HsmState {
    super_: None,
    init_: Some(Sample_active_init_),
    entry_: Some(Sample_active_entry_),
    exit_: Some(Sample_active_exit_),
    handler_: Sample_active_,
};

static Sample_working: SM_HsmState<SampleChart> = SM_HsmState {
    super_: Some(&Sample_active),
    init_: None,
    entry_: Some(Sample_working_entry_),
    exit_: Some(Sample_working_exit_),
    handler_: Sample_working_,
};

pub fn build_machine() -> (SM_Hsm<SampleChart>, SampleCtx) {
    let mut hsm = SM_Hsm::<SampleChart>::new();
    let mut ctx = SampleCtx::default();
    hsm.init(&mut ctx);
    (hsm, ctx)
}
